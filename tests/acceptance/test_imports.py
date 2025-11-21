def test_can_import_generated_package():
    # Import a couple of common entry points to ensure the generated SDK is loadable
    import camunda_orchestration_sdk  # noqa: F401
    from camunda_orchestration_sdk import api_client  # noqa: F401


def test_api_client_constructible():
    # The generated client should be importable and constructible without side effects
    from camunda_orchestration_sdk import api_client
    from camunda_orchestration_sdk import semantic_types

    client = api_client.ApiClient()
    assert client is not None
    # lifter smoke
    assert hasattr(semantic_types, "lift_element_instance_key")

