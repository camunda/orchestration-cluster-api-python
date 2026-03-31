def test_spec_hash_is_accessible():
    from camunda_orchestration_sdk import SPEC_HASH

    assert SPEC_HASH is not None
    assert isinstance(SPEC_HASH, str)
    assert len(SPEC_HASH) > 0


def test_spec_hash_format():
    from camunda_orchestration_sdk import SPEC_HASH

    assert SPEC_HASH.startswith("sha256:")
    # sha256: prefix + 64 hex chars
    assert len(SPEC_HASH) == len("sha256:") + 64
