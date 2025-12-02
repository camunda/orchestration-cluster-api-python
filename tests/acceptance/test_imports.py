def test_can_import_generated_package():
    # Import a couple of common entry points to ensure the generated SDK is loadable
    import camunda_orchestration_sdk  # noqa: F401
    from camunda_orchestration_sdk import Client  # noqa: F401

def test_api_client_constructible():
    # The generated client should be importable and constructible without side effects
    from camunda_orchestration_sdk import semantic_types

    from camunda_orchestration_sdk import Client
    client = Client(base_url="http://localhost")

    assert client is not None
    # lifter smoke
    assert hasattr(semantic_types, "lift_element_instance_key")
    semantic_types.ProcessDefinitionId 
