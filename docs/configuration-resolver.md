## Configuration feature

We need to add a configuration resolver.

This should be a new class that is created in the runtime directory. 

We want this configuration resolver to take two arguments: 

An environment and an optional explicit configuration.

The environment and the explicit configuration are both typed as a Partial of a Pydantic schema. 

In the configuration resolver, we merge the environment and the explicit config, with the explicit config overriding the environment, then validate against the Pydantic schema.

We return an object that has the effective configuration, and also the original env and explicit configs (for debugging purposes).

Here is the initial schema (pseudocode) that we will expose: 


ZEEBE_REST_ADDRESS | type: string | default: 'http://localhost:8080/v2'
CAMUNDA_REST_ADDRESS | alias for ZEEBE_REST_ADDRESS 
CAMUNDA_TOKEN_AUDIENCE | type: string | default: 'zeebe.camunda.io'
CAMUNDA_CLIENT_ID | type: string
CAMUNDA_CLIENT_SECRET | type: string
CAMUNDA_OAUTH_URL | type: string | default: 'https://login.cloud.camunda.io/oauth/token'
CAMUNDA_CLIENT_AUTH_CLIENTID | alias for CAMUNDA_CLIENT_ID
CAMUNDA_CLIENT_AUTH_CLIENTSECRET | alias for CAMUNDA_CLIENT_SECRET
CAMUNDA_AUTH_STRATEGY: {
    type: 'enum',
    choices: ['NONE', 'OAUTH', 'BASIC'],
    default: 'NONE',
    doc: 'Authentication strategy.',
  },
  CAMUNDA_BASIC_AUTH_USERNAME: {
    type: 'string',
    doc: 'Basic auth username (required when CAMUNDA_AUTH_STRATEGY=BASIC).',
    requiredWhen: { key: 'CAMUNDA_AUTH_STRATEGY', equals: 'BASIC' },
  },
  CAMUNDA_BASIC_AUTH_PASSWORD: {
    type: 'string',
    secret: true,
    doc: 'Basic auth password (required when CAMUNDA_AUTH_STRATEGY=BASIC).',
    requiredWhen: { key: 'CAMUNDA_AUTH_STRATEGY', equals: 'BASIC' },
  },
  CAMUNDA_CLIENT_ID: {
    type: 'string',
    doc: 'OAuth client id (required when CAMUNDA_AUTH_STRATEGY=OAUTH).',
    requiredWhen: { key: 'CAMUNDA_AUTH_STRATEGY', equals: 'OAUTH' },
  },
  CAMUNDA_CLIENT_SECRET: {
    type: 'string',
    secret: true,
    doc: 'OAuth client secret (required when CAMUNDA_AUTH_STRATEGY=OAUTH).',
    requiredWhen: { key: 'CAMUNDA_AUTH_STRATEGY', equals: 'OAUTH' },
  }
  CAMUNDA_SDK_LOG_LEVEL: {
    type: 'enum',
    choices: ['silent', 'error', 'warn', 'info', 'debug', 'trace', 'silly'] as const,
    default: 'error',
    doc: 'SDK log level. "silly" adds unsafe deep diagnostics including HTTP request and response bodies.',
  }

## Resolution logic

Here is the logic for aliases: 

- If one is set in the merged config, use that and populate the effective schema for both aliases with the value.
- If neither is set, use the default.
- If both are set, and they differ, raise an error. 
- If both are set, and they are the same, use that value.

## Testing 

We need comprehensive unit tests in the tests/acceptance directory to prove the operation of the resolver.

-----

We don't wire it into init.py. We will copy it into the generated SDK during post-processing.

The method of wiring it in will be this:

The CamundaClient and CamundaAsyncClient will take an optional configuration partial as a parameter in their constructor.

We pass this and the concrete environment to a configuration resolver instance and get back the effective configuration of the client which is stored as a property.

----

Let's remove the base_url and token parameters from the CamundaClient and CamundaAsyncClient and use the configuration resolver to configure the base_url via the CAMUNDA_REST_ADDRESS property