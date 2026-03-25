# Compilable usage examples for decision instances, documents, jobs, and user task extras.
# These examples are type-checked during build to guard against API regressions.
from __future__ import annotations

from camunda_orchestration_sdk import (
    CamundaClient,
    DecisionDefinitionKey,
    DecisionEvaluationInstanceKey,
    DecisionEvaluationKey,
    DecisionInstanceSearchQuery,
    DecisionRequirementsKey,
    DecisionRequirementsSearchQuery,
    DocumentId,
    DocumentLinkRequest,
    JobChangeset,
    JobErrorRequest,
    JobKey,
    JobSearchQuery,
    JobUpdateRequest,
    Unset,
    UserTaskAuditLogSearchQueryRequest,
    UserTaskKey,
)


# region GetDecisionDefinitionXml
def get_decision_definition_xml_example() -> None:
    client = CamundaClient()

    xml = client.get_decision_definition_xml(
        decision_definition_key=DecisionDefinitionKey("123456"),
    )

    print(f"XML length: {len(xml)}")
# endregion GetDecisionDefinitionXml


# region GetDecisionInstance
def get_decision_instance_example() -> None:
    client = CamundaClient()

    result = client.get_decision_instance(
        decision_evaluation_instance_key=DecisionEvaluationInstanceKey("123456"),
    )

    print(f"Decision instance: {result.decision_definition_id}")
# endregion GetDecisionInstance


# region SearchDecisionInstances
def search_decision_instances_example() -> None:
    client = CamundaClient()

    result = client.search_decision_instances(
        data=DecisionInstanceSearchQuery(),
    )

    if not isinstance(result.items, Unset):
        for di in result.items:
            print(f"Decision instance: {di.decision_definition_id}")
# endregion SearchDecisionInstances


# region DeleteDecisionInstance
def delete_decision_instance_example() -> None:
    client = CamundaClient()

    client.delete_decision_instance(
        decision_evaluation_key=DecisionEvaluationKey("123456"),
    )
# endregion DeleteDecisionInstance


# region GetDecisionRequirements
def get_decision_requirements_example() -> None:
    client = CamundaClient()

    result = client.get_decision_requirements(
        decision_requirements_key=DecisionRequirementsKey("123456"),
    )

    print(f"DRD: {result.decision_requirements_name}")
# endregion GetDecisionRequirements


# region GetDecisionRequirementsXml
def get_decision_requirements_xml_example() -> None:
    client = CamundaClient()

    xml = client.get_decision_requirements_xml(
        decision_requirements_key=DecisionRequirementsKey("123456"),
    )

    print(f"XML length: {len(xml)}")
# endregion GetDecisionRequirementsXml


# region SearchDecisionRequirements
def search_decision_requirements_example() -> None:
    client = CamundaClient()

    result = client.search_decision_requirements(
        data=DecisionRequirementsSearchQuery(),
    )

    if not isinstance(result.items, Unset):
        for drd in result.items:
            print(f"DRD: {drd.decision_requirements_name}")
# endregion SearchDecisionRequirements


# region CreateDocumentLink
def create_document_link_example() -> None:
    client = CamundaClient()

    result = client.create_document_link(
        document_id=DocumentId("doc-123"),
        data=DocumentLinkRequest(),
    )

    print(f"Document link: {result.url}")
# endregion CreateDocumentLink


# region DeleteDocument
def delete_document_example() -> None:
    client = CamundaClient()

    client.delete_document(document_id=DocumentId("doc-123"))
# endregion DeleteDocument


# region ThrowJobError
def throw_job_error_example() -> None:
    client = CamundaClient()

    client.throw_job_error(
        job_key=JobKey("123456"),
        data=JobErrorRequest(
            error_code="VALIDATION_ERROR",
            error_message="Input validation failed",
        ),
    )
# endregion ThrowJobError


# region UpdateJob
def update_job_example() -> None:
    client = CamundaClient()

    client.update_job(
        job_key=JobKey("123456"),
        data=JobUpdateRequest(
            changeset=JobChangeset(
                retries=3,
            ),
        ),
    )
# endregion UpdateJob


# region SearchJobs
def search_jobs_example() -> None:
    client = CamundaClient()

    result = client.search_jobs(
        data=JobSearchQuery(),
    )

    if not isinstance(result.items, Unset):
        for job in result.items:
            print(f"Job: {job.job_key}")
# endregion SearchJobs


# region GetUserTask
def get_user_task_example() -> None:
    client = CamundaClient()

    result = client.get_user_task(
        user_task_key=UserTaskKey("123456"),
    )

    print(f"User task: {result.user_task_key}")
# endregion GetUserTask


# region UpdateUserTask
def update_user_task_example() -> None:
    from camunda_orchestration_sdk import Changeset, UserTaskUpdateRequest

    client = CamundaClient()

    client.update_user_task(
        user_task_key=UserTaskKey("123456"),
        data=UserTaskUpdateRequest(
            changeset=Changeset(
                priority=80,
            ),
        ),
    )
# endregion UpdateUserTask


# region GetUserTaskForm
def get_user_task_form_example() -> None:
    client = CamundaClient()

    result = client.get_user_task_form(
        user_task_key=UserTaskKey("123456"),
    )

    print(f"Form: {result.form_key}")
# endregion GetUserTaskForm


# region SearchUserTaskVariables
def search_user_task_variables_example() -> None:
    client = CamundaClient()

    result = client.search_user_task_variables(
        user_task_key=UserTaskKey("123456"),
    )

    if not isinstance(result.items, Unset):
        for var in result.items:
            print(f"Variable: {var.name}")
# endregion SearchUserTaskVariables


# region SearchUserTaskAuditLogs
def search_user_task_audit_logs_example() -> None:
    client = CamundaClient()

    result = client.search_user_task_audit_logs(
        user_task_key=UserTaskKey("123456"),
        data=UserTaskAuditLogSearchQueryRequest(),
    )

    if not isinstance(result.items, Unset):
        for log in result.items:
            print(f"Audit log: {log.audit_log_key}")
# endregion SearchUserTaskAuditLogs
