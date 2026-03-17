"""Tests for deploy_resources_from_files and deployment response parsing.

The server may omit nullable fields from the deployment response (older
gateways omit null-valued keys instead of sending them explicitly).
These tests verify the SDK handles both shapes.
"""

from camunda_orchestration_sdk.models.deployment_metadata_result import (
    DeploymentMetadataResult,
)
from camunda_orchestration_sdk.models.deployment_result import DeploymentResult


class TestDeploymentMetadataFromDict:
    """DeploymentMetadataResult.from_dict must tolerate missing nullable keys."""

    def test_bpmn_only_all_keys_present(self) -> None:
        """New gateway: all keys present, non-applicable ones are null."""
        raw = {
            "processDefinition": {
                "processDefinitionId": "my-process",
                "processDefinitionVersion": 1,
                "resourceName": "my-process.bpmn",
                "tenantId": "<default>",
                "processDefinitionKey": "123",
            },
            "decisionDefinition": None,
            "decisionRequirements": None,
            "form": None,
            "resource": None,
        }
        meta = DeploymentMetadataResult.from_dict(raw)
        assert meta.process_definition is not None
        assert meta.process_definition.process_definition_id == "my-process"
        assert meta.decision_definition is None
        assert meta.decision_requirements is None
        assert meta.form is None
        assert meta.resource is None

    def test_bpmn_only_missing_nullable_keys(self) -> None:
        """Old gateway: only processDefinition present, others omitted."""
        raw = {
            "processDefinition": {
                "processDefinitionId": "my-process",
                "processDefinitionVersion": 1,
                "resourceName": "my-process.bpmn",
                "tenantId": "<default>",
                "processDefinitionKey": "456",
            },
        }
        meta = DeploymentMetadataResult.from_dict(raw)
        assert meta.process_definition is not None
        assert meta.process_definition.process_definition_key == "456"
        assert meta.decision_definition is None
        assert meta.decision_requirements is None
        assert meta.form is None
        assert meta.resource is None

    def test_dmn_only_missing_nullable_keys(self) -> None:
        """Old gateway deploying a DMN: only decisionDefinition present."""
        raw = {
            "decisionDefinition": {
                "decisionDefinitionId": "my-decision",
                "version": 1,
                "name": "My Decision",
                "decisionDefinitionKey": "789",
                "decisionRequirementsId": "req-1",
                "decisionRequirementsKey": "101",
                "tenantId": "<default>",
            },
        }
        meta = DeploymentMetadataResult.from_dict(raw)
        assert meta.process_definition is None
        assert meta.decision_definition is not None
        assert meta.decision_definition.decision_definition_id == "my-decision"
        assert meta.form is None
        assert meta.resource is None

    def test_empty_dict(self) -> None:
        """Edge case: completely empty metadata entry."""
        meta = DeploymentMetadataResult.from_dict({})
        assert meta.process_definition is None
        assert meta.decision_definition is None
        assert meta.decision_requirements is None
        assert meta.form is None
        assert meta.resource is None


class TestDeploymentResultFromDict:
    """Full deployment response round-trip."""

    def test_bpmn_deployment_old_gateway(self) -> None:
        """Simulate an old gateway BPMN deployment response (missing nullable keys)."""
        raw = {
            "deploymentKey": "2251799813696020",
            "tenantId": "<default>",
            "deployments": [
                {
                    "processDefinition": {
                        "processDefinitionId": "Process_1s9882u",
                        "processDefinitionVersion": 1,
                        "resourceName": "test.bpmn",
                        "tenantId": "<default>",
                        "processDefinitionKey": "2251799813696021",
                    }
                }
            ],
        }
        result = DeploymentResult.from_dict(raw)
        assert result.deployment_key == "2251799813696020"
        assert len(result.deployments) == 1
        meta = result.deployments[0]
        assert meta.process_definition is not None
        assert meta.decision_definition is None


class TestExtendedDeploymentResult:
    """ExtendedDeploymentResult convenience wrapper."""

    def test_processes_extracted_old_gateway(self) -> None:
        """BPMN-only deployment with old gateway response shape."""
        from camunda_orchestration_sdk.client import ExtendedDeploymentResult

        raw = {
            "deploymentKey": "100",
            "tenantId": "<default>",
            "deployments": [
                {
                    "processDefinition": {
                        "processDefinitionId": "my-proc",
                        "processDefinitionVersion": 1,
                        "resourceName": "proc.bpmn",
                        "tenantId": "<default>",
                        "processDefinitionKey": "200",
                    }
                }
            ],
        }
        base = DeploymentResult.from_dict(raw)
        extended = ExtendedDeploymentResult(base)
        assert len(extended.processes) == 1
        assert extended.processes[0].process_definition_id == "my-proc"
        assert extended.decisions == []
        assert extended.decision_requirements == []
        assert extended.forms == []

    def test_mixed_deployment(self) -> None:
        """Deploy both BPMN and DMN — new gateway with all keys present."""
        from camunda_orchestration_sdk.client import ExtendedDeploymentResult

        raw = {
            "deploymentKey": "300",
            "tenantId": "<default>",
            "deployments": [
                {
                    "processDefinition": {
                        "processDefinitionId": "proc-1",
                        "processDefinitionVersion": 1,
                        "resourceName": "proc.bpmn",
                        "tenantId": "<default>",
                        "processDefinitionKey": "400",
                    },
                    "decisionDefinition": None,
                    "decisionRequirements": None,
                    "form": None,
                    "resource": None,
                },
                {
                    "processDefinition": None,
                    "decisionDefinition": {
                        "decisionDefinitionId": "dec-1",
                        "version": 1,
                        "name": "Decision 1",
                        "decisionDefinitionKey": "500",
                        "decisionRequirementsId": "req-1",
                        "decisionRequirementsKey": "600",
                        "tenantId": "<default>",
                    },
                    "decisionRequirements": None,
                    "form": None,
                    "resource": None,
                },
            ],
        }
        base = DeploymentResult.from_dict(raw)
        extended = ExtendedDeploymentResult(base)
        assert len(extended.processes) == 1
        assert len(extended.decisions) == 1
        assert extended.processes[0].process_definition_id == "proc-1"
        assert extended.decisions[0].decision_definition_id == "dec-1"
