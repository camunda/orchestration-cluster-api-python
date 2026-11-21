"""Metadata must correspond to the *selected* spec (issue #489, PR #490 review).

``generate.py`` drives default-tenant injection, semantic types and the spec
hash from bundler metadata (``spec-metadata.json``). That metadata is only valid
for the spec it was produced from. Previously the committed
``external-spec/bundled/spec-metadata.json`` snapshot was supplied *unconditionally*
— even when ``--local-spec`` / ``--spec-ref`` / ``--bundled-spec`` selected a
different spec — so a tenant-scoped operation present only in the selected spec
silently lost default-tenant injection.

This guards the class (fail-open metadata selection), not the instance: for every
non-default spec source the resolver must either return metadata that was produced
alongside that exact spec or return ``None`` (so hooks skip metadata-driven
behaviour) — it must never fall back to the unrelated committed snapshot.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parents[2]


def _load_generate_module():
    spec = importlib.util.spec_from_file_location("generate", REPO_ROOT / "generate.py")
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


@pytest.fixture(scope="module")
def generate():
    return _load_generate_module()


def test_bundled_spec_uses_sibling_metadata(generate, tmp_path: Path):
    """--bundled-spec resolves metadata co-located with that spec, not the snapshot."""
    bundled = tmp_path / "rest-api.bundle.json"
    bundled.write_text("{}", encoding="utf-8")
    sibling = tmp_path / "spec-metadata.json"
    sibling.write_text("{}", encoding="utf-8")

    result = generate._resolve_metadata_path(bundled, spec_overridden=False)
    assert result == sibling


def test_bundled_spec_generic_sidecar_rejected_for_other_bundle_name(
    generate, tmp_path: Path
):
    """A generic ``spec-metadata.json`` must not describe a differently named bundle.

    The generic name is this repo's convention for the *default* bundle
    (``rest-api.bundle.json``, written by ``scripts/bundle-spec.sh``). Pointing
    ``--bundled-spec`` at ``other.bundle.json`` in the same directory must not
    silently reuse it — tenant injection and ``SPEC_HASH`` would be built from
    the wrong spec (PR #490 adversarial review). The resolver must fail closed
    instead of guessing.
    """
    bundled = tmp_path / "other.bundle.json"
    bundled.write_text("{}", encoding="utf-8")
    generic = tmp_path / "spec-metadata.json"
    generic.write_text("{}", encoding="utf-8")

    with pytest.raises(FileNotFoundError):
        generate._resolve_metadata_path(bundled, spec_overridden=False)


def test_bundled_spec_generic_sidecar_rejected_when_other_bundles_present(
    generate, tmp_path: Path
):
    """Even for ``rest-api.bundle.json``, a generic sidecar is ambiguous when the
    directory holds other bundles — it may describe any of them. Fail closed."""
    bundled = tmp_path / "rest-api.bundle.json"
    bundled.write_text("{}", encoding="utf-8")
    (tmp_path / "other.bundle.json").write_text("{}", encoding="utf-8")
    generic = tmp_path / "spec-metadata.json"
    generic.write_text("{}", encoding="utf-8")

    with pytest.raises(FileNotFoundError):
        generate._resolve_metadata_path(bundled, spec_overridden=False)


def test_bundled_spec_uses_stem_metadata_convention(generate, tmp_path: Path):
    """--bundled-spec also accepts the bundler's ``<stem>-metadata.json`` naming."""
    bundled = tmp_path / "rest-api.bundle.json"
    bundled.write_text("{}", encoding="utf-8")
    sibling = tmp_path / "rest-api.bundle-metadata.json"
    sibling.write_text("{}", encoding="utf-8")

    result = generate._resolve_metadata_path(bundled, spec_overridden=False)
    assert result == sibling


def test_bundled_spec_prefers_stem_metadata_over_generic(generate, tmp_path: Path):
    """When both sidecars exist, the bundle-specific one must win.

    A directory can hold ``spec-metadata.json`` for the *default* bundle (as
    written by ``scripts/bundle-spec.sh``) alongside ``<stem>-metadata.json``
    produced for an alternate ``--bundled-spec alternate.bundle.json``. The
    generic name describes a *different* spec, so selecting it would silently
    omit the alternate operations' tenant injection and emit the wrong
    ``SPEC_HASH`` (PR #490 review). The bundle-specific sidecar is the only
    metadata guaranteed to match the selected spec, so it takes precedence.
    """
    bundled = tmp_path / "alternate.bundle.json"
    bundled.write_text("{}", encoding="utf-8")
    generic = tmp_path / "spec-metadata.json"
    generic.write_text("{}", encoding="utf-8")
    specific = tmp_path / "alternate.bundle-metadata.json"
    specific.write_text("{}", encoding="utf-8")

    result = generate._resolve_metadata_path(bundled, spec_overridden=False)
    assert result == specific


def test_bundled_spec_without_sibling_metadata_fails(generate, tmp_path: Path):
    """--bundled-spec with no matching metadata must fail, not reuse the snapshot."""
    bundled = tmp_path / "rest-api.bundle.json"
    bundled.write_text("{}", encoding="utf-8")

    with pytest.raises(FileNotFoundError):
        generate._resolve_metadata_path(bundled, spec_overridden=False)


def test_local_spec_returns_none_not_committed_snapshot(generate):
    """--local-spec must not fall back to the committed (unrelated) snapshot."""
    result = generate._resolve_metadata_path(None, spec_overridden=True)
    assert result is None


def test_spec_ref_override_returns_none_not_committed_snapshot(generate):
    """A non-default --spec-ref must not fall back to the committed snapshot."""
    result = generate._resolve_metadata_path(None, spec_overridden=True)
    assert result is None


def test_default_source_uses_committed_snapshot(generate):
    """The committed-snapshot flow keeps using the committed snapshot.

    That flow is reachable only when the committed bundle itself is the input
    (``--bundled-spec external-spec/bundled/rest-api.bundle.json``, as used by
    ``make generate``); the resolver then returns the sibling generic sidecar.
    """
    bundled = REPO_ROOT / "external-spec" / "bundled" / "rest-api.bundle.json"
    if not bundled.exists():
        pytest.skip("committed bundle not present in this checkout")
    result = generate._resolve_metadata_path(bundled, spec_overridden=False)
    committed = REPO_ROOT / "external-spec" / "bundled" / "spec-metadata.json"
    assert result == committed


def test_no_argument_fetch_flow_returns_none_not_committed_snapshot(generate):
    """The no-argument flow fetches *live* upstream main, so the pinned snapshot is wrong.

    ``uv run generate.py ...`` with no ``--bundled-spec``/``--local-spec`` fetches
    the spec from live camunda ``main`` via ``fetch_spec``. The committed
    ``external-spec/bundled/spec-metadata.json`` snapshot was bundled from that
    same upstream spec but is *pinned* and drifts from live main, so applying it
    is the same wrong-spec mismatch class (PR #490 adversarial review). The
    resolver must return ``None`` so hooks skip metadata-driven behaviour; the
    committed snapshot is used only when the committed bundle itself is the
    input (``--bundled-spec external-spec/bundled/rest-api.bundle.json``).
    """
    result = generate._resolve_metadata_path(None, spec_overridden=False)
    assert result is None


def _load_spec_hash_hook():
    path = REPO_ROOT / "hooks" / "post_gen" / "0025_emit_spec_hash.py"
    spec = importlib.util.spec_from_file_location("hook_0025_emit_spec_hash", path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_spec_hash_hook_skips_when_metadata_path_empty(tmp_path: Path):
    """--local-spec / --spec-ref pass metadata_path="" — post-gen must not crash,
    and must not leave a stale SPEC_HASH from an unrelated spec."""
    pkg = tmp_path / "camunda_orchestration_sdk"
    pkg.mkdir()
    stale = pkg / "_spec_hash.py"
    stale.write_text('SPEC_HASH = "stale"\n', encoding="utf-8")
    _load_spec_hash_hook().run({"out_dir": str(tmp_path), "metadata_path": ""})
    assert not stale.exists()


def test_spec_hash_hook_fails_when_explicit_metadata_missing(tmp_path: Path):
    (tmp_path / "camunda_orchestration_sdk").mkdir()
    with pytest.raises(FileNotFoundError):
        _load_spec_hash_hook().run(
            {"out_dir": str(tmp_path), "metadata_path": str(tmp_path / "nope.json")}
        )
