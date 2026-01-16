## Provided auth strategies

We will support pluggable authentication strategies Basic and OAuth. 

Take a look at the TypeScript implementation of these auth providers: https://raw.githubusercontent.com/camunda/orchestration-cluster-api-js/refs/heads/main/src/runtime/auth.ts

Implement both providers for the Python client. The appropriate one should be activated automatically based on the effective configuration of the client at runtime.