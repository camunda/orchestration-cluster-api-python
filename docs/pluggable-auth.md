## Pluggable auth

We want to be able to use different authentication strategies, and we want to be able to configure them.

A custom implementation can be provided by the end-user, allowing for strategies that we don't support out of the box. 

But for most use-cases, the auth strategy will be set via configuration, and we will provide an implementation.

The auth provider is a class that implements the following interface:

get_headers() -> Mapping[str, str]

The protocol uses the general `Mapping[str, str]` type, but concrete implementations will typically return a `dict[str, str]`, which is compatible.
A CamundaClient and CamundaAsyncClient will use a null provider by default. It returns a zero-length dict every time. 

The auth provider is used by every call that the client makes to authenticate with the server. Possibly the best place to locate this concern is a hook on the httpx client, if one is available, rather than on every single method call. 

We will build Basic and OAuth providers in a future sprint. For now, we want to provide the integration surface for auth header provider implementations, and wire in a null provider by default.