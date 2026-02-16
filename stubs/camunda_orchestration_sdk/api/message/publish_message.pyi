from typing import Any
import httpx
from ...client import AuthenticatedClient, Client
from ...models.message_publication_request import MessagePublicationRequest
from ...models.problem_detail import ProblemDetail
from ...models.publish_message_response_200 import PublishMessageResponse200
from ...types import Response

def _get_kwargs(body: MessagePublicationRequest) -> dict[str, Any]: ...
def _parse_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> ProblemDetail | PublishMessageResponse200 | None: ...
def _build_response(
    client: AuthenticatedClient | Client, response: httpx.Response
) -> Response[ProblemDetail | PublishMessageResponse200]: ...
def sync_detailed(
    client: AuthenticatedClient | Client, body: MessagePublicationRequest
) -> Response[ProblemDetail | PublishMessageResponse200]: ...
def sync(
    client: AuthenticatedClient | Client, body: MessagePublicationRequest, **kwargs: Any
) -> PublishMessageResponse200: ...
async def asyncio_detailed(
    client: AuthenticatedClient | Client, body: MessagePublicationRequest
) -> Response[ProblemDetail | PublishMessageResponse200]: ...
async def asyncio(
    client: AuthenticatedClient | Client, body: MessagePublicationRequest, **kwargs: Any
) -> PublishMessageResponse200: ...
