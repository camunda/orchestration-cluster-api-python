# How to Monitor Your Loan Application Processes

There are several ways to see how your processes are progressing:

## Option 1: Using Camunda REST API Directly (Simplest)

Use curl or your browser to query Camunda directly:

### List All Process Instances

```bash
curl -s http://localhost:8080/v2/process-instances/search \
  -H "Content-Type: application/json" \
  -d '{"page": {"limit": 10}}' | python3 -m json.tool
```

### Filter by Your Loan Process

```bash
curl -s http://localhost:8080/v2/process-instances/search \
  -H "Content-Type: application/json" \
  -d '{"filter": {"processDefinitionKey": "2251799813843646"}, "page": {"limit": 10}}' | python3 -m json.tool
```

### Get Specific Process Instance

```bash
# Replace with your actual process instance key
curl -s http://localhost:8080/v2/process-instances/2251799813843700 | python3 -m json.tool
```

## Option 2: Using FastAPI Swagger UI

1. **Open the API docs**: Visit `http://localhost:8000/docs`
2. **Try the endpoints**:
   - `/process-instance/create` - Create new instances
   - `/topology` - Check cluster health
   - `/health` - Check API health

## Option 3: Check Process Instance State

After submitting a loan application, you'll get a `process_instance_key` in the response. Use it to check the status:

```bash
# Example with process instance key from your submission
INSTANCE_KEY="2251799813843700"

curl -s "http://localhost:8080/v2/process-instances/${INSTANCE_KEY}" | python3 -m json.tool
```

**Response will show**:
- `state`: "ACTIVE" (still running) or "COMPLETED" (finished)
- `processDefinitionId`: "loanApplicationProcess"
- `startDate`: When it started
- `endDate`: When it finished (if completed)

## Option 4: Query Flow Nodes (See Where Process Is Stuck)

To see exactly which task the process is waiting on:

```bash
INSTANCE_KEY="2251799813843700"

curl -s "http://localhost:8080/v2/flownode-instances/search" \
  -H "Content-Type: application/json" \
  -d "{
    \"filter\": {\"processInstanceKey\": \"${INSTANCE_KEY}\"},
    \"size\": 50
  }" | python3 -m json.tool
```

This shows:
- All flow nodes (tasks, gateways, events) in the process
- Their `state`: "ACTIVE", "COMPLETED", "TERMINATED"
- The `flowNodeId`: Which task it is (e.g., "Task_ValidateApplication")

## Option 5: Query Jobs (See Waiting Service Tasks)

To see which service tasks are waiting for workers:

```bash
curl -s "http://localhost:8080/v2/jobs/search" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {"processDefinitionKey": "2251799813843646"},
    "size": 10
  }' | python3 -m json.tool
```

This shows:
- `type`: The job type (e.g., "validate-loan-application")
- `state`: "ACTIVATABLE" (waiting for worker), "ACTIVATED" (being processed)
- `retries`: Number of retries remaining

## Understanding Process States

### Process Instance States:
- **ACTIVE**: Process is running, waiting for a task to complete
- **COMPLETED**: Process finished successfully
- **TERMINATED**: Process was cancelled

### Flow Node States:
- **ACTIVE**: Currently at this step
- **COMPLETED**: This step finished
- **TERMINATED**: This step was cancelled

### Job States:
- **ACTIVATABLE**: Ready for a worker to pick up
- **ACTIVATED**: Worker is processing it
- **COMPLETED**: Worker finished successfully
- **FAILED**: Worker encountered an error

## Quick Status Check Script

Create a file `check_processes.sh`:

```bash
#!/bin/bash

echo "=== Recent Process Instances ==="
curl -s http://localhost:8080/v2/process-instances/search \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {"processDefinitionKey": "2251799813843646"},
    "size": 5,
    "sort": [{"field": "startDate", "order": "desc"}]
  }' | python3 -c "
import sys, json
data = json.load(sys.stdin)
for item in data.get('items', []):
    print(f\"  Key: {item['processInstanceKey']}, State: {item['state']}, Started: {item['startDate']}\")
"

echo -e "\n=== Waiting Jobs (Tasks Without Workers) ==="
curl -s "http://localhost:8080/v2/jobs/search" \
  -H "Content-Type: application/json" \
  -d '{
    "filter": {"processDefinitionKey": "2251799813843646", "state": "ACTIVATABLE"},
    "size": 10
  }' | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(f\"  Total waiting jobs: {data.get('total', 0)}\")
for item in data.get('items', []):
    print(f\"  - Job Type: {item['type']}, Process: {item['processInstanceKey']}\")
"
```

Make it executable and run:
```bash
chmod +x check_processes.sh
./check_processes.sh
```

## Common Scenarios

### Scenario 1: Process Created, Nothing Happens

**Symptom**: Process instance is ACTIVE, but nothing is happening

**Cause**: No workers are running to process the service tasks

**Check**:
```bash
curl -s "http://localhost:8080/v2/jobs/search" \
  -H "Content-Type: application/json" \
  -d '{"filter": {"state": "ACTIVATABLE"}, "size": 10}' | python3 -m json.tool
```

**Solution**: Start workers (see `LOAN_PROCESS_README.md`)

### Scenario 2: Process Stuck at First Task

**Symptom**: Process stays at "Task_ValidateApplication"

**Cause**: No worker registered for "validate-loan-application" job type

**Check**:
```bash
curl -s "http://localhost:8080/v2/jobs/search" \
  -H "Content-Type: application/json" \
  -d '{"filter": {"type": "validate-loan-application"}}' | python3 -m json.tool
```

**Solution**: Register a worker for that job type

### Scenario 3: Process Completed Successfully

**Symptom**: Process instance state is "COMPLETED"

**Congratulations!**: All workers processed the tasks successfully

**View details**:
```bash
# Check the flow node instances to see the path taken
INSTANCE_KEY="your-instance-key"
curl -s "http://localhost:8080/v2/flownode-instances/search" \
  -H "Content-Type: application/json" \
  -d "{\"filter\": {\"processInstanceKey\": \"${INSTANCE_KEY}\"}}" | python3 -m json.tool
```

## Camunda Operate UI (If Available)

If you have Camunda Operate running:

1. **Access**: Usually at `http://localhost:8081` or similar
2. **View**:
   - All process instances
   - Visual process diagram with current position
   - Variables at each step
   - Detailed execution history

## Next Steps

1. **Start monitoring**: Run the status check script
2. **Implement workers**: See `LOAN_PROCESS_README.md` for worker examples
3. **Test the full flow**: Submit applications and watch them complete
4. **Build a dashboard**: Create a simple web UI showing process statistics

Happy monitoring! 🔍
