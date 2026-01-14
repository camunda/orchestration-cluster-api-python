# QuickLoan Bank - Quick Start Guide

## The Issue You're Facing

The error `"For input string: \"loan-application-process\""` occurs because Camunda expects a **numeric process definition key**, not a BPMN process ID string.

### Understanding the Difference:

- **BPMN Process ID** (like `loan-application-process`): This is the ID you define in your BPMN file, a human-readable string
- **Process Definition Key** (like `2251799813686749`): This is a numeric key that Camunda generates when you deploy a BPMN process

## Solution: Deploy a Process First

You need to deploy a BPMN process to Camunda and get the numeric key it returns.

### Option 1: Use an Existing Deployed Process

If you already have a process deployed in Camunda:

1. Check which processes are deployed (you can use Camunda Operate UI or the API)
2. Get the `process_definition_key` (numeric) from a deployed process
3. Update [app.js](app.js) line 6:
   ```javascript
   const PROCESS_DEFINITION_KEY = '2251799813686749'; // Replace with your actual numeric key
   ```

### Option 2: Deploy a New BPMN Process

#### Step 1: Create or use a BPMN file

You need a BPMN file for your loan application process. If you don't have one, here's the simplest possible process for testing:

Create `loan-process.bpmn` with this content:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<bpmn:definitions xmlns:bpmn="http://www.omg.org/spec/BPMN/20100524/MODEL"
                   xmlns:bpmndi="http://www.omg.org/spec/BPMN/20100524/DI"
                   xmlns:dc="http://www.omg.org/spec/DD/20100524/DC"
                   id="Definitions_1"
                   targetNamespace="http://bpmn.io/schema/bpmn">
  <bpmn:process id="loan-application" name="Loan Application Process" isExecutable="true">
    <bpmn:startEvent id="StartEvent_1" name="Application Received">
      <bpmn:outgoing>Flow_1</bpmn:outgoing>
    </bpmn:startEvent>
    <bpmn:endEvent id="EndEvent_1" name="Application Processed">
      <bpmn:incoming>Flow_1</bpmn:incoming>
    </bpmn:endEvent>
    <bpmn:sequenceFlow id="Flow_1" sourceRef="StartEvent_1" targetRef="EndEvent_1"/>
  </bpmn:process>
</bpmn:definitions>
```

#### Step 2: Deploy via API

Use curl or the API to deploy:

```bash
curl -X POST http://localhost:8000/deploy/resource \
  -H "Content-Type: application/json" \
  -d '{"file_path": "/path/to/loan-process.bpmn"}'
```

Response will include:
```json
{
  "deployment_key": "2251799813685249",
  "tenant_id": "<default>",
  "processes": [
    {
      "process_definition_id": "loan-application",
      "process_definition_key": "2251799813686749",  // <- USE THIS!
      "process_definition_version": 1,
      "resource_name": "loan-process.bpmn",
      "tenant_id": "<default>"
    }
  ]
}
```

#### Step 3: Update the Frontend

Copy the `process_definition_key` value and update [app.js](app.js):

```javascript
const PROCESS_DEFINITION_KEY = '2251799813686749'; // Your numeric key here
```

#### Step 4: Restart and Test

Restart your FastAPI server if needed, then visit `http://localhost:8000` and submit the form.

### Option 3: Use the Python Test Script

If you have a BPMN file in your project (like in `tests/integration/resources/`), you can use Python:

```python
import asyncio
from camunda_orchestration_sdk import CamundaAsyncClient

async def deploy_process():
  camunda = CamundaAsyncClient(base_url="http://localhost:8080/v2")

    # Deploy your BPMN file
    result = await camunda.deploy_resources_from_files(
        files=["./path/to/your/process.bpmn"]
    )

    # Print the process definition key
    print(f"Process Definition Key: {result.processes[0].process_definition_key}")
    print(f"Process ID: {result.processes[0].process_definition_id}")

    return result.processes[0].process_definition_key

if __name__ == "__main__":
    key = asyncio.run(deploy_process())
    print(f"\nUpdate app.js with: const PROCESS_DEFINITION_KEY = '{key}';")
```

## Summary

The fix is:

1. **Deploy a BPMN process** to Camunda (via API, Camunda Modeler, or code)
2. **Get the numeric `process_definition_key`** from the deployment response
3. **Update [app.js](app.js) line 6** with that numeric key
4. **Test the form** - it should now work!

## Why This Happens

Camunda's REST API uses numeric keys internally for efficiency. When you deploy a process, Camunda:
1. Takes your BPMN file with a process ID like `"loan-application"`
2. Generates a unique numeric key like `"2251799813686749"`
3. Returns both in the deployment response
4. Requires the numeric key for creating process instances

This is similar to how databases use numeric primary keys instead of string IDs.

## Need Help?

- Check if Camunda is running: `curl http://localhost:8080/v2/topology`
- Check FastAPI health: `curl http://localhost:8000/health`
- List your deployed processes using Camunda Operate UI (if available)
