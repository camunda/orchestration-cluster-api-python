import inspect
from typing import Any


def _annotation_to_doc_return_text(annotation: Any) -> str:
    if annotation is inspect.Signature.empty:
        return "Any"
    if annotation is Any:
        return "Any"
    if annotation is None:
        return "None"
    if isinstance(annotation, str):
        return annotation
    name = getattr(annotation, "__name__", None)
    if name:
        return name
    text = str(annotation)
    return text.removeprefix("typing.")


def _get_returns_line(doc: str) -> str | None:
    lines = doc.splitlines()
    for i, line in enumerate(lines):
        if line.strip() == "Returns:" and i + 1 < len(lines):
            return lines[i + 1].strip()
    return None


def _assert_value_or_throw_doc(func: Any) -> None:
    doc = inspect.getdoc(func) or ""
    assert doc, f"Expected a docstring for {func}"

    # Convenience wrappers should not claim Response[...] unions.
    assert "Response[" not in doc

    # The previous wording we want to ensure is gone.
    assert "undocumented status code" not in doc
    assert "Client.raise_on_unexpected_status" not in doc

    # Should document typed exceptions + fallback UnexpectedStatus.
    assert "errors.UnexpectedStatus" in doc

    expected_return = _annotation_to_doc_return_text(inspect.signature(func).return_annotation)
    returns_line = _get_returns_line(doc)
    assert returns_line == expected_return, f"Returns line mismatch: {returns_line!r} != {expected_return!r}"


def test_api_wrapper_docstrings_match_rewritten_signature():
    from camunda_orchestration_sdk.api.group.get_group import sync as get_group_sync
    from camunda_orchestration_sdk.api.job.fail_job import sync as fail_job_sync
    from camunda_orchestration_sdk.api.process_instance.create_process_instance import (
        sync as create_process_instance_sync,
    )

    doc_group = inspect.getdoc(get_group_sync) or ""
    assert "errors.GetGroupUnauthorized" in doc_group
    assert "errors.GetGroupForbidden" in doc_group

    doc_fail = inspect.getdoc(fail_job_sync) or ""
    assert "errors.FailJobBadRequest" in doc_fail
    assert "errors.FailJobNotFound" in doc_fail

    doc_create_pi = inspect.getdoc(create_process_instance_sync) or ""
    assert "errors.CreateProcessInstanceServiceUnavailable" in doc_create_pi
    assert "backpressure" in doc_create_pi

    _assert_value_or_throw_doc(get_group_sync)
    _assert_value_or_throw_doc(fail_job_sync)
    _assert_value_or_throw_doc(create_process_instance_sync)


def test_camunda_client_docstrings_match_rewritten_signature():
    from camunda_orchestration_sdk.client import CamundaClient
    from camunda_orchestration_sdk import errors

    doc_group = inspect.getdoc(CamundaClient.get_group) or ""
    assert "errors.GetGroupUnauthorized" in doc_group

    doc_fail = inspect.getdoc(CamundaClient.fail_job) or ""
    assert "errors.FailJobBadRequest" in doc_fail

    doc_create_pi = inspect.getdoc(CamundaClient.create_process_instance) or ""
    assert "errors.CreateProcessInstanceServiceUnavailable" in doc_create_pi
    assert "backpressure" in doc_create_pi

    exc_doc = inspect.getdoc(errors.CreateProcessInstanceServiceUnavailable) or ""
    assert "backpressure" in exc_doc

    _assert_value_or_throw_doc(CamundaClient.get_group)
    _assert_value_or_throw_doc(CamundaClient.fail_job)
    _assert_value_or_throw_doc(CamundaClient.create_process_instance)
