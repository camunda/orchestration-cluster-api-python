#!/bin/bash
# Syncs Python SDK documentation to the local Camunda docs site
# Run this after generating docs with `make docs-api` from the project root

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/../.." && pwd)"
CAMUNDA_DOCS="$SCRIPT_DIR/../camunda-docs"

# Source markdown from Sphinx build
SOURCE_MD="$PROJECT_ROOT/public/markdown/index.md"

# Target directories
DOCS_DIR="$CAMUNDA_DOCS/docs/apis-tools/python"
VERSIONED_DOCS_DIR="$CAMUNDA_DOCS/versioned_docs/version-8.8/apis-tools/python"
VERSIONED_SIDEBARS="$CAMUNDA_DOCS/versioned_sidebars/version-8.8-sidebars.json"

# Check prerequisites
if [ ! -f "$SOURCE_MD" ]; then
    echo "Error: Source markdown not found at $SOURCE_MD"
    echo "Run 'make docs-api' from the project root first"
    exit 1
fi

if [ ! -d "$CAMUNDA_DOCS" ]; then
    echo "Error: Camunda docs not found at $CAMUNDA_DOCS"
    echo "Clone it first with: cd demo && git clone https://github.com/camunda/camunda-docs.git"
    exit 1
fi

echo "Syncing Python SDK docs to Camunda docs..."

# Create target directories
mkdir -p "$DOCS_DIR"
mkdir -p "$VERSIONED_DOCS_DIR"

# Copy API reference
cp "$SOURCE_MD" "$DOCS_DIR/api-reference.md"
cp "$SOURCE_MD" "$VERSIONED_DOCS_DIR/api-reference.md"
echo "  Copied API reference"

# Create python-sdk.md (overview page)
cat > "$DOCS_DIR/python-sdk.md" << 'EOF'
---
id: python-sdk
title: Python SDK
description: Camunda 8 Python SDK overview.
---

Build Camunda 8 applications using the Camunda Python SDK and Orchestration Cluster API Python client.

## Get started

The Python SDK provides a simple, typed interface to interact with Camunda 8 via the Orchestration Cluster REST API.

- [Orchestration Cluster API Python client](oca-client.md) - Get started with the Python client
- [API Reference](api-reference.md) - Full API documentation

## Features

The Python SDK provides:

- **Async-first design** - Built on `httpx` for efficient async HTTP operations
- **Type hints** - Full type annotations for better IDE support and code quality
- **Job workers** - Create workers to handle service tasks
- **Process management** - Deploy processes, start instances, and manage process lifecycle
- **User task handling** - Query, assign, and complete user tasks

## When to use this SDK

Use the Python SDK if:

- You are building Python applications that interact with Camunda 8
- You need to deploy process models programmatically
- You want to create job workers in Python
- You are using Camunda 8.9 or later with the Orchestration Cluster REST API

:::info
Learn more about the [Orchestration Cluster REST API](/apis-tools/orchestration-cluster-api-rest/orchestration-cluster-api-rest-overview.md).
:::
EOF
cp "$DOCS_DIR/python-sdk.md" "$VERSIONED_DOCS_DIR/python-sdk.md"
echo "  Created python-sdk.md"

# Create oca-client.md (getting started guide)
cat > "$DOCS_DIR/oca-client.md" << 'EOF'
---
id: oca-client
title: Orchestration Cluster API Python client
sidebar_label: Orchestration Cluster API Python client
description: Use the camunda-orchestration-sdk package to connect to Camunda 8 and interact with the Orchestration Cluster REST API.
---

Use the Orchestration Cluster API Python client to connect to Camunda 8, deploy process models, and interact with the Orchestration Cluster REST API.

## About this client

This package provides a typed Python interface to the Orchestration Cluster REST API.

### When to use this package

Use the `camunda-orchestration-sdk` package if:

- You are building Python applications that interact with Camunda 8.
- You are using Camunda 8.9 or later.
- You want async-first design built on `httpx`.
- You need type hints and IDE support.

## Installation

Install the package using pip:

```bash
pip install camunda-orchestration-sdk
```

Or with uv:

```bash
uv add camunda-orchestration-sdk
```

## Use the Orchestration Cluster API package

The following example retrieves the cluster topology:

```python
import asyncio
from camunda_orchestration_sdk import CamundaAsyncClient

async def main():
    async with CamundaAsyncClient(base_url="http://localhost:8080/v2") as camunda:
        response = await camunda.get_topology()
        print(response)

asyncio.run(main())
```

For synchronous usage:

```python
from camunda_orchestration_sdk import CamundaClient

with CamundaClient(base_url="http://localhost:8080/v2") as camunda:
    response = camunda.get_topology()
    print(response)
```

## Configure the connection

### Self-managed configuration

For a local or self-managed Camunda 8 instance:

```python
from camunda_orchestration_sdk import CamundaAsyncClient

camunda = CamundaAsyncClient(base_url="http://localhost:8080/v2")
```

### Authenticated configuration

For environments requiring authentication:

```python
from camunda_orchestration_sdk import CamundaAsyncClient

camunda = CamundaAsyncClient(
    base_url="https://your-cluster.camunda.io/v2",
    token="your-access-token"
)
```

## Deploy a process model

Deploy a BPMN process model from a file:

```python
import asyncio
from camunda_orchestration_sdk import CamundaAsyncClient

async def main():
    async with CamundaAsyncClient(base_url="http://localhost:8080/v2") as camunda:
        result = await camunda.deploy_resources_from_files(["process.bpmn"])

        for process in result.processes:
            print(f"Deployed process: {process.process_definition_id}")

asyncio.run(main())
```

## Create a process instance

Start a new process instance:

```python
import asyncio
from camunda_orchestration_sdk import CamundaAsyncClient
from camunda_orchestration_sdk.models.processcreationbykey import Processcreationbykey

async def main():
    async with CamundaAsyncClient(base_url="http://localhost:8080/v2") as camunda:
        process_instance = await camunda.create_process_instance(
            data=Processcreationbykey(
                process_definition_key=2251799814900879,
                variables={"orderId": "12345"}
            )
        )
        print(f"Started process instance: {process_instance.process_instance_key}")

asyncio.run(main())
```

## Create a job worker

Create a worker to handle service tasks:

```python
import asyncio
from camunda_orchestration_sdk import CamundaAsyncClient
from camunda_orchestration_sdk.runtime.job_worker import WorkerConfig, JobContext

def handle_job(job: JobContext):
    print(f"Processing job: {job.job_key}")
    # Your business logic here
    return  # Returning completes the job

async def main():
    async with CamundaAsyncClient(base_url="http://localhost:8080/v2") as camunda:
        config = WorkerConfig(
            job_type="my-service-task",
            execution_strategy="auto",
            job_timeout_milliseconds=30_000,
        )

        worker = camunda.create_job_worker(config=config, callback=handle_job)

        # Keep the worker running
        await asyncio.sleep(60)

asyncio.run(main())
```

## Search process instances

Query process instances with filters:

```python
import asyncio
from camunda_orchestration_sdk import CamundaAsyncClient
from camunda_orchestration_sdk.models.search_process_instances_data import SearchProcessInstancesData
from camunda_orchestration_sdk.models.search_process_instances_data_filter import SearchProcessInstancesDataFilter
from camunda_orchestration_sdk.models.state_advancedfilter_6 import StateAdvancedfilter6
from camunda_orchestration_sdk.models.state_advancedfilter_6_eq import StateAdvancedfilter6Eq

async def main():
    async with CamundaAsyncClient(base_url="http://localhost:8080/v2") as camunda:
        query = SearchProcessInstancesData(
            filter_=SearchProcessInstancesDataFilter(
                state=StateAdvancedfilter6(eq=StateAdvancedfilter6Eq("ACTIVE")),
            )
        )

        result = await camunda.search_process_instances(data=query)

        for instance in result.items:
            print(f"Process instance: {instance.process_instance_key}")

asyncio.run(main())
```

## API documentation

See the [full API documentation](api-reference.md) for details on all available methods and models.
EOF
cp "$DOCS_DIR/oca-client.md" "$VERSIONED_DOCS_DIR/oca-client.md"
echo "  Created oca-client.md"

# Update versioned sidebars
echo "  Updating version-8.8-sidebars.json..."
if grep -q '"apis-tools/python/python-sdk"' "$VERSIONED_SIDEBARS" 2>/dev/null; then
    echo "    Python SDK already in sidebar"
else
    # Use sed to insert Python SDK after TypeScript SDK
    # The pattern matches the end of TypeScript items and start of Community clients
    sed -i.bak 's/"apis-tools\/typescript\/eventual-consistency"\n          \]\n        },\n        {\n          "Community clients": \[/"apis-tools\/typescript\/eventual-consistency"\
          ]\
        },\
        {\
          "type": "category",\
          "label": "Python SDK",\
          "link": {\
            "type": "doc",\
            "id": "apis-tools\/python\/python-sdk"\
          },\
          "items": [\
            "apis-tools\/python\/oca-client",\
            "apis-tools\/python\/api-reference"\
          ]\
        },\
        {\
          "Community clients": [/g' "$VERSIONED_SIDEBARS"

    # If sed didn't work (multiline issues), use Python
    if ! grep -q '"apis-tools/python/python-sdk"' "$VERSIONED_SIDEBARS" 2>/dev/null; then
        python3 << PYEOF
import re

with open("$VERSIONED_SIDEBARS", "r") as f:
    content = f.read()

# Pattern to find TypeScript SDK section end and Community clients start
pattern = r'("apis-tools/typescript/eventual-consistency"\s*\]\s*\},\s*\{\s*"Community clients": \[)'

replacement = '''"apis-tools/typescript/eventual-consistency"
          ]
        },
        {
          "type": "category",
          "label": "Python SDK",
          "link": {
            "type": "doc",
            "id": "apis-tools/python/python-sdk"
          },
          "items": [
            "apis-tools/python/oca-client",
            "apis-tools/python/api-reference"
          ]
        },
        {
          "Community clients": ['''

content = re.sub(pattern, replacement, content)

with open("$VERSIONED_SIDEBARS", "w") as f:
    f.write(content)
PYEOF
    fi

    rm -f "$VERSIONED_SIDEBARS.bak"

    if grep -q '"apis-tools/python/python-sdk"' "$VERSIONED_SIDEBARS" 2>/dev/null; then
        echo "    Added Python SDK to sidebar"
    else
        echo "    Warning: Could not add Python SDK to sidebar automatically"
    fi
fi

# Clear Docusaurus cache
rm -rf "$CAMUNDA_DOCS/.docusaurus" 2>/dev/null || true

echo ""
echo "Done! Python SDK docs synced to Camunda docs."
