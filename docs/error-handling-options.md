# Error handling options for “value-or-throw” wrappers

This repo currently generates endpoint modules with:

- `*_detailed()` / `*_asyncio_detailed()` returning `Response[Success | ErrorModel1 | ErrorModel2 | ...]`
- `_parse_response()` that **already resolves** documented non-2xx HTTP status codes into typed error models (e.g. `GetAuthenticationResponse401`)
- convenience wrappers `sync()` / `asyncio()` that are post-processed to **raise on non-2xx**

Today, the convenience wrappers raise `errors.UnexpectedStatus` for every non-2xx, which loses the parsed error model information.

This document outlines three options to preserve typed error resolution while keeping “value-or-throw” ergonomics.

---

## Common example endpoint

We’ll use `GET /authentication/me` as a running example.

The generated response models are:

- success: `GetAuthenticationResponse200`
- documented errors: `GetAuthenticationResponse401`, `GetAuthenticationResponse403`, `GetAuthenticationResponse500`

The goal is: calling `sync()`/`asyncio()` is still simple, but callers can recover the parsed error model when the server returns a documented non-2xx.

---

## Option A — One generic `ApiResponseError` carrying `.parsed`

### Idea

Introduce a new exception type that carries the parsed error model:

- `errors.ApiResponseError`: raised on non-2xx when the response status code is *documented* and `_parse_response()` returned a model instance
- `errors.UnexpectedStatus`: still used for truly undocumented status codes (ideally as a subclass of `ApiResponseError` for catch ergonomics)

This keeps the exception surface small (one main type), while preserving runtime access to “what error model did I get?”

### Runtime behavior

- 2xx: return `SuccessModel`
- non-2xx + parsed model exists: raise `ApiResponseError(parsed=<ErrorModel>, status_code=..., content=...)`
- non-2xx + parsed model is `None`: raise `UnexpectedStatus(...)`

### Example usage (sync)

```python
from camunda_orchestration_sdk import CamundaClient
from camunda_orchestration_sdk import errors
from camunda_orchestration_sdk.models.get_authentication_response_401 import GetAuthenticationResponse401

client = CamundaClient(base_url="http://localhost:8080/v2", token="...")

try:
    me = client.get_authentication()
    # type: GetAuthenticationResponse200
    print(me)
except errors.ApiResponseError as e:
    # e.parsed is the parsed error model (documented non-2xx)
    if isinstance(e.parsed, GetAuthenticationResponse401):
        # handle unauthenticated
        print("Not authenticated")
    else:
        # handle other documented errors
        print(f"Request failed: status={e.status_code}, parsed={type(e.parsed).__name__}")
except errors.UnexpectedStatus as e:
    # truly undocumented status codes (or when parsing wasn’t possible)
    print(f"Unexpected status: {e.status_code}")
```

### Example usage (async)

```python
from camunda_orchestration_sdk import CamundaClient
from camunda_orchestration_sdk import errors

client = CamundaClient(base_url="http://localhost:8080/v2", token="...")

async def main() -> None:
    try:
        me = await client.get_authentication_async()
        print(me)
    except errors.ApiResponseError as e:
        print(e.status_code)
```

### Pros

- Small, stable exception surface
- Preserves error model resolution at runtime
- Easy to teach: “catch `ApiResponseError`, inspect `.parsed`”

### Cons

- The *constrained set* of possible error models is not obvious from the function signature
- Static typing of `.parsed` can be improved with generics, but type checkers won’t always infer it at the catch site

---

## Option C1 — One per-endpoint exception type with a typed payload union

### Idea

Generate **one exception class per endpoint**, whose payload is typed to the union of that endpoint’s documented error models.

Example:

- `errors.GetAuthenticationError` with `parsed: GetAuthenticationResponse401 | GetAuthenticationResponse403 | GetAuthenticationResponse500`

The convenience wrapper raises this per-endpoint error for documented non-2xx codes.

### Runtime behavior

- 2xx: return `SuccessModel`
- documented non-2xx: raise `GetAuthenticationError(parsed=<one of the error models>, status_code=...)`
- undocumented status codes: raise `UnexpectedStatus(...)` (or a shared base)

### Example usage (sync)

```python
from camunda_orchestration_sdk import CamundaClient
from camunda_orchestration_sdk import errors
from camunda_orchestration_sdk.models.get_authentication_response_401 import GetAuthenticationResponse401

client = CamundaClient(base_url="http://localhost:8080/v2", token="...")

try:
    me = client.get_authentication()
except errors.GetAuthenticationError as e:
    # e.parsed is statically constrained to the endpoint’s error-model union
    if isinstance(e.parsed, GetAuthenticationResponse401):
        print("Not authenticated")
    else:
        print(f"Auth error: {e.status_code}")
```

### Example usage (async)

```python
from camunda_orchestration_sdk import CamundaClient
from camunda_orchestration_sdk import errors

client = CamundaClient(base_url="http://localhost:8080/v2", token="...")

async def main() -> None:
    try:
        me = await client.get_authentication_async()
    except errors.GetAuthenticationError as e:
        print(type(e.parsed).__name__)
```

### Pros

- Much better discoverability (endpoint-specific “this endpoint can fail with …”)
- Better type narrowing: `e.parsed` is constrained to the endpoint’s union
- Still relatively low class-count (one per endpoint)

### Cons

- Still not encoded as “raises types” in the function signature (Python limitation)
- Adds many exported symbols (one per endpoint), requires naming + organization decisions

---

## Option C2 — Per-endpoint, per-status exception classes (typed exceptions)

### Idea

Generate distinct exception classes per endpoint *and* per status code, each carrying one error model.

Example:

- `errors.GetAuthenticationUnauthorized` (401) carrying `GetAuthenticationResponse401`
- `errors.GetAuthenticationForbidden` (403) carrying `GetAuthenticationResponse403`
- `errors.GetAuthenticationInternalServerError` (500) carrying `GetAuthenticationResponse500`

The wrapper raises the most specific exception based on status code.

### Runtime behavior

- 2xx: return `SuccessModel`
- documented non-2xx: raise the status-specific exception
- undocumented status codes: raise `UnexpectedStatus(...)`

### Example usage (sync)

```python
from camunda_orchestration_sdk import CamundaClient
from camunda_orchestration_sdk import errors

client = CamundaClient(base_url="http://localhost:8080/v2", token="...")

try:
    me = client.get_authentication()
except errors.GetAuthenticationUnauthorized as e:
    # e.parsed is exactly GetAuthenticationResponse401
    print("Need to login")
except errors.GetAuthenticationForbidden as e:
    print("No permission")
except errors.GetAuthenticationInternalServerError as e:
    print("Server error")
```

### Example usage (async)

```python
from camunda_orchestration_sdk import CamundaClient
from camunda_orchestration_sdk import errors

client = CamundaClient(base_url="http://localhost:8080/v2", token="...")

async def main() -> None:
    try:
        me = await client.get_authentication_async()
    except errors.GetAuthenticationUnauthorized:
        ...
```

### Pros

- Most ergonomic `except` blocks; no need to inspect `.parsed` for the common cases
- Strongest typing: the exception implies the model type

### Cons

- Many exception classes (endpoints × status codes)
- Naming needs care (HTTP reason phrases vs stable names)
- More code generation + more public API surface to maintain

---

## Summary table

| Option | Exception surface | Type precision | Ergonomics | Complexity |
|---|---:|---:|---:|---:|
| A | small (1–2 shared types) | medium (runtime) / medium+ (with generics) | good | low |
| C1 | medium (≈1 per endpoint) | good (payload union per endpoint) | good | medium |
| C2 | large (endpoint × status) | best (one model per exception) | best | high |

---

## Notes on Python typing

Python type checkers generally do not model “raised exception types” as part of a function’s type. These options improve:

- discoverability via exception classes
- type narrowing inside `except` blocks (especially C1/C2)

…but they won’t behave like Rust/Swift “throws types” at the signature level.
