def test_can_import_generated_package():
    # Import a couple of common entry points to ensure the generated SDK is loadable
    from camunda_orchestration_sdk import Client  # noqa: F401  # pyright: ignore[reportUnusedImport]


def test_api_client_constructible():
    # The generated client should be importable and constructible without side effects
    from camunda_orchestration_sdk import semantic_types

    from camunda_orchestration_sdk import Client

    client = Client(base_url="http://localhost")

    assert client is not None
    # lifter smoke
    assert hasattr(semantic_types, "lift_element_instance_key")
    assert semantic_types.lift_process_definition_key("123") == "123"
    assert hasattr(semantic_types, "ProcessDefinitionId")


def test_camunda_client_constructible():
    from camunda_orchestration_sdk import CamundaClient, CamundaAsyncClient

    client = CamundaClient()
    assert client is not None
    assert client.client is not None

    async_client = CamundaAsyncClient()
    assert async_client is not None
    assert async_client.client is not None
