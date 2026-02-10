## Provided auth strategies

The Python SDK supports pluggable authentication strategies. Out of the box, the following strategies are available:

- **Basic authentication** (username and password or API token)
- **OAuth 2.0** (access token obtained from an identity provider)

At runtime, the SDK selects the appropriate strategy based on how you configure the client:

- If you provide basic credentials (for example, a username and password or an API token), the client uses **Basic authentication**.
- If you provide OAuth-related settings (for example, an access token or configuration to obtain one), the client uses **OAuth 2.0**.

Refer to the client configuration documentation for the exact parameters and examples of how to:

- Configure Basic authentication when creating a client instance.
- Configure OAuth 2.0, including how to supply or refresh access tokens.

In most cases you only need to supply the appropriate credentials; the SDK handles the selection and application of the correct authentication strategy for each request.