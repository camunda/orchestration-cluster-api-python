from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.conditional_evaluation_instruction import (
    ConditionalEvaluationInstruction,
)
from ...models.evaluate_conditional_result import EvaluateConditionalResult
from ...models.problem_detail import ProblemDetail
from ...types import Response

def _get_kwargs(body: ConditionalEvaluationInstruction) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> EvaluateConditionalResult | ProblemDetail | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[EvaluateConditionalResult | ProblemDetail]: ...
def sync_detailed(
    client: AuthenticatedClient | Client, body: ConditionalEvaluationInstruction
) -> Response[EvaluateConditionalResult | ProblemDetail]: ...
def sync(
    client: AuthenticatedClient | Client,
    body: ConditionalEvaluationInstruction,
    **kwargs: Any,
) -> EvaluateConditionalResult: ...
async def asyncio_detailed(
    client: AuthenticatedClient | Client, body: ConditionalEvaluationInstruction
) -> Response[EvaluateConditionalResult | ProblemDetail]: ...
async def asyncio(
    client: AuthenticatedClient | Client,
    body: ConditionalEvaluationInstruction,
    **kwargs: Any,
) -> EvaluateConditionalResult: ...
