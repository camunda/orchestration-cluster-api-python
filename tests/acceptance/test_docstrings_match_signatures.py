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

    # The previous (incorrect) wording we want to ensure is gone.
    assert "undocumented status code" not in doc
    assert "Client.raise_on_unexpected_status" not in doc

    # Should document raising on non-2xx.
    assert "errors.UnexpectedStatus" in doc
    assert "response status code is not 2xx" in doc

    expected_return = _annotation_to_doc_return_text(inspect.signature(func).return_annotation)
    returns_line = _get_returns_line(doc)
    assert returns_line == expected_return, f"Returns line mismatch: {returns_line!r} != {expected_return!r}"


def test_api_wrapper_docstrings_match_rewritten_signature():
    from camunda_orchestration_sdk.api.group.get_group import sync as get_group_sync
    from camunda_orchestration_sdk.api.job.fail_job import sync as fail_job_sync

    _assert_value_or_throw_doc(get_group_sync)
    _assert_value_or_throw_doc(fail_job_sync)


def test_camunda_client_docstrings_match_rewritten_signature():
    from camunda_orchestration_sdk.client import CamundaClient

    _assert_value_or_throw_doc(CamundaClient.get_group)
    _assert_value_or_throw_doc(CamundaClient.fail_job)
