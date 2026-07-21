"""Tests for the markdown post-processing that renders the API reference.

These guard the class of rendering defects reported on the generated docs:

* keyword-only ``*`` separators dropped from method signatures, leaving an
  empty comma slot (``restore(, data, **kwargs)``);
* multi-paragraph method descriptions escaping their blockquote;
* the "Parameters" field list rendering as a hard-to-scan nested bullet list.

They import the post-processing module directly (no Sphinx build required).
"""

import importlib.util
from pathlib import Path

_SCRIPT = Path(__file__).resolve().parents[2] / "scripts" / "postprocess_markdown.py"
_spec = importlib.util.spec_from_file_location("postprocess_markdown", _SCRIPT)
assert _spec and _spec.loader
postprocess_markdown = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(postprocess_markdown)

_restore_keyword_only_marker = postprocess_markdown._restore_keyword_only_marker
fix_description_blockquotes = postprocess_markdown.fix_description_blockquotes
convert_parameter_lists_to_tables = postprocess_markdown.convert_parameter_lists_to_tables
run = postprocess_markdown.postprocess_markdown


class TestKeywordOnlyMarker:
    """The dropped ``*`` keyword-only separator must be restored."""

    def test_leading_dropped_marker_restored(self):
        assert _restore_keyword_only_marker(", data, **kwargs") == "*, data, **kwargs"

    def test_middle_dropped_marker_restored(self):
        assert (
            _restore_keyword_only_marker("tenant_id, , data, **kwargs")
            == "tenant_id, *, data, **kwargs"
        )

    def test_empty_parameter_list_untouched(self):
        assert _restore_keyword_only_marker("") == ""

    def test_existing_marker_preserved(self):
        assert (
            _restore_keyword_only_marker("*, mode, dry_run=<Unset>, **kwargs")
            == "*, mode, dry_run=<Unset>, **kwargs"
        )

    def test_no_empty_comma_slot_survives_full_pipeline(self):
        source = "#### *async* restore(, data, \\*\\*kwargs)\n"
        result = run(source)
        assert "def restore(*, data, **kwargs)" in result
        assert "(, data" not in result
        assert ", ," not in result

    def test_no_arg_method_stays_empty(self):
        result = run("#### run_workers()\n")
        assert "def run_workers()" in result
        assert "(*)" not in result

    def test_path_parameter_method(self):
        result = run("#### *async* update_tenant(tenant_id, , data, \\*\\*kwargs)\n")
        assert "def update_tenant(tenant_id, *, data, **kwargs)" in result


class TestDescriptionBlockquotes:
    """Continuation paragraphs fold back into the method-description blockquote."""

    def test_continuation_paragraph_folded(self):
        source = (
            "> Restores the cluster from a backup. It is described either by a\n"
            "\n"
            "time range that selects the backups to restore. This endpoint is only\n"
            "accessible while the cluster is in recovery mode.\n"
            "\n"
            "* **Parameters:**\n"
            "  * **data** (*RestoreRequest*)\n"
        )
        result = fix_description_blockquotes(source)
        assert "> time range that selects the backups to restore." in result
        assert "> accessible while the cluster is in recovery mode." in result
        # No flush-left continuation line escapes the blockquote.
        assert "\ntime range that selects" not in result

    def test_stops_at_boundary(self):
        source = "> Summary line.\n\n* **Parameters:**\n  * **data** (*X*)\n"
        result = fix_description_blockquotes(source)
        assert result == source

    def test_non_blockquote_content_untouched(self):
        source = "Close the client.\n\nThis closes both clients.\n\n* **Return type:**\n  None\n"
        assert fix_description_blockquotes(source) == source

    def test_blockquote_followed_by_blockquote_terminates(self):
        # A blockquote followed (after blank lines) by another blockquote must
        # not hang: the second ``>`` is a separate blockquote, not a
        # continuation paragraph, so both are preserved verbatim.
        source = "> First blockquote.\n\n> Second blockquote.\n"
        result = fix_description_blockquotes(source)
        assert result == source

    def test_blockquote_abutting_field_list_gets_blank_separator(self):
        # A description blockquote *immediately* followed (no blank line) by a
        # field-list boundary must be separated by a blank line. Otherwise
        # CommonMark lazy continuation absorbs the boundary into the quote,
        # rendering e.g. the "Parameters:" header *inside* the blockquote.
        source = (
            "> Search for decision instances based on given criteria.\n"
            "* **Parameters:**\n"
            "  * **body** (*X*)\n"
        )
        result = fix_description_blockquotes(source)
        assert (
            "> Search for decision instances based on given criteria.\n"
            "\n"
            "* **Parameters:**" in result
        )

    def test_blockquote_abutting_boundary_gets_blank_separator(self):
        # Class-scoped guard: *any* non-blockquote structural boundary that
        # directly abuts a blockquote (no blank line) must be separated, not
        # just the Parameters field list.
        source = "> Summary with no trailing blank.\n### Heading\n"
        result = fix_description_blockquotes(source)
        assert "> Summary with no trailing blank.\n\n### Heading" in result

    def test_hardwrap_continuation_stays_one_paragraph(self):
        # A continuation line whose preceding quoted line does not end in
        # sentence-terminating punctuation is a hard-wrap of the same
        # sentence. Folding it must NOT insert an empty ``>`` separator, which
        # would render as two paragraphs for a single sentence.
        source = (
            "> Search for incidents caused by the specified element instance, "
            "including incidents of any child\n"
            "\n"
            "instances created from this element instance.\n"
            "\n"
            "* **Parameters:**\n"
            "  * **body** (*X*)\n"
        )
        result = fix_description_blockquotes(source)
        assert (
            "> Search for incidents caused by the specified element instance, "
            "including incidents of any child\n"
            "> instances created from this element instance." in result
        )
        # No empty ``>`` separator splits the single sentence.
        assert ">\n> instances created" not in result

    def test_sentence_boundary_keeps_separate_paragraph(self):
        # A continuation whose preceding quoted line ends in terminal
        # punctuation is a genuinely new paragraph and must remain separated by
        # an empty ``>`` line inside the blockquote.
        source = (
            "> First complete sentence.\n"
            "\n"
            "Second distinct paragraph here.\n"
            "\n"
            "* **Parameters:**\n"
            "  * **body** (*X*)\n"
        )
        result = fix_description_blockquotes(source)
        assert (
            "> First complete sentence.\n>\n> Second distinct paragraph here." in result
        )


class TestParameterTables:
    """The Parameters field list renders as a markdown table."""

    def test_parameters_become_table(self):
        source = (
            "* **Parameters:**\n"
            "  * **data** (*RestoreRequest*) – Describes a restore request. Provide either a\n"
            "    list of backup IDs or a time range.\n"
            "  * **kwargs** (*Any*)\n"
            "* **Raises:**\n"
            "  * **errors.BadRequestError** – If the response status code is 400.\n"
        )
        result = convert_parameter_lists_to_tables(source)
        assert "| Parameter | Type | Description |" in result
        assert "| --- | --- | --- |" in result
        assert "| `data` | `RestoreRequest` |" in result
        assert "list of backup IDs or a time range." in result
        assert "| `kwargs` | `Any` |  |" in result
        # The nested bullet form is gone for parameters ...
        assert "  * **data**" not in result
        # ... but sibling field lists (Raises) are left untouched.
        assert "* **Raises:**" in result
        assert "  * **errors.BadRequestError**" in result
        # The table is terminated by a blank line before the Raises field list.
        assert "|\n\n* **Raises:**" in result

    def test_link_type_preserved(self):
        source = (
            "* **Parameters:**\n"
            "  * **configuration** ([*CamundaSdkConfiguration*](runtime.md#cfg))\n"
        )
        result = convert_parameter_lists_to_tables(source)
        assert "[CamundaSdkConfiguration](runtime.md#cfg)" in result
        assert "| `configuration` |" in result

    def test_union_type_rendered(self):
        source = "* **Parameters:**\n  * **name** (*str* *|* *None*) – The name.\n"
        result = convert_parameter_lists_to_tables(source)
        assert "`str` \\| `None`" in result

    def test_pipe_in_description_escaped(self):
        source = "* **Parameters:**\n  * **name** (*str*) – Either a | b.\n"
        result = convert_parameter_lists_to_tables(source)
        assert "Either a \\| b." in result
