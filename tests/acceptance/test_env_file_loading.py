"""Test .env file loading functionality."""
import os
import tempfile
from pathlib import Path
import pytest
from camunda_orchestration_sdk.runtime.configuration_resolver import read_environment



def test_load_envfile_with_true_boolean():
    """Test loading .env file with CAMUNDA_LOAD_ENVFILE=true."""
    # Create a temporary .env file
    with tempfile.TemporaryDirectory() as tmpdir:
        env_file = Path(tmpdir) / ".env"
        env_file.write_text(
            "CAMUNDA_CLIENT_ID=test_client_id\n"
            "CAMUNDA_CLIENT_SECRET=test_secret\n"
            "CAMUNDA_REST_ADDRESS=https://test.camunda.io\n"
        )
        
        # Change to temp directory
        original_cwd = Path.cwd()
        try:
            os.chdir(tmpdir)
            # Set CAMUNDA_LOAD_ENVFILE to trigger loading
            env = {"CAMUNDA_LOAD_ENVFILE": "true"}
            result = read_environment(env)
            
            # Verify values were loaded from .env file
            assert result.get("CAMUNDA_CLIENT_ID") == "test_client_id"
            assert result.get("CAMUNDA_CLIENT_SECRET") == "test_secret"
            assert result.get("CAMUNDA_REST_ADDRESS") == "https://test.camunda.io"
        finally:
            os.chdir(original_cwd)


def test_load_envfile_with_explicit_path():
    """Test loading .env file with explicit path."""
    with tempfile.TemporaryDirectory() as tmpdir:
        env_file = Path(tmpdir) / "custom.env"
        env_file.write_text(
            "CAMUNDA_CLIENT_ID=custom_client_id\n"
            "CAMUNDA_REST_ADDRESS=https://custom.camunda.io\n"
        )
        
        # Use explicit path
        env = {"CAMUNDA_LOAD_ENVFILE": str(env_file)}
        result = read_environment(env)
        
        # Verify values were loaded
        assert result.get("CAMUNDA_CLIENT_ID") == "custom_client_id"
        assert result.get("CAMUNDA_REST_ADDRESS") == "https://custom.camunda.io"


def test_load_envfile_nonexistent_file():
    """Test that nonexistent .env file is silently ignored."""
    env = {"CAMUNDA_LOAD_ENVFILE": "/nonexistent/path/to/.env"}
    result = read_environment(env)
    
    # Should not raise an error, just return empty result
    assert "CAMUNDA_CLIENT_ID" not in result


def test_load_envfile_disabled():
    """Test that .env file is not loaded when CAMUNDA_LOAD_ENVFILE is not set."""
    with tempfile.TemporaryDirectory() as tmpdir:
        env_file = Path(tmpdir) / ".env"
        env_file.write_text("CAMUNDA_CLIENT_ID=should_not_load\n")
        
        original_cwd = Path.cwd()
        try:
            os.chdir(tmpdir)
            # Don't set CAMUNDA_LOAD_ENVFILE
            env = {}
            result = read_environment(env)
            
            # Values should not be loaded from .env
            assert result.get("CAMUNDA_CLIENT_ID") != "should_not_load"
        finally:
            os.chdir(original_cwd)


def test_load_envfile_with_override():
    """Test that environment variables override .env file values."""
    with tempfile.TemporaryDirectory() as tmpdir:
        env_file = Path(tmpdir) / ".env"
        env_file.write_text(
            "CAMUNDA_CLIENT_ID=from_env_file\n"
            "CAMUNDA_REST_ADDRESS=https://file.camunda.io\n"
        )
        
        original_cwd = Path.cwd()
        try:
            os.chdir(tmpdir)
            # Provide explicit environment variable that should take precedence
            env = {
                "CAMUNDA_LOAD_ENVFILE": "true",
                "CAMUNDA_CLIENT_ID": "from_environment"
            }
            result = read_environment(env)
            
            # Environment variable should take precedence
            assert result.get("CAMUNDA_CLIENT_ID") == "from_environment"
            # But .env file value should still be loaded for other keys
            assert result.get("CAMUNDA_REST_ADDRESS") == "https://file.camunda.io"
        finally:
            os.chdir(original_cwd)


def test_load_envfile_with_numeric_boolean():
    """Test loading .env file with CAMUNDA_LOAD_ENVFILE=1."""
    with tempfile.TemporaryDirectory() as tmpdir:
        env_file = Path(tmpdir) / ".env"
        env_file.write_text("CAMUNDA_CLIENT_ID=numeric_test\n")
        
        original_cwd = Path.cwd()
        try:
            os.chdir(tmpdir)
            env = {"CAMUNDA_LOAD_ENVFILE": "1"}
            result = read_environment(env)
            
            assert result.get("CAMUNDA_CLIENT_ID") == "numeric_test"
        finally:
            os.chdir(original_cwd)


def test_load_envfile_with_yes():
    """Test loading .env file with CAMUNDA_LOAD_ENVFILE=yes."""
    with tempfile.TemporaryDirectory() as tmpdir:
        env_file = Path(tmpdir) / ".env"
        env_file.write_text("CAMUNDA_CLIENT_ID=yes_test\n")
        
        original_cwd = Path.cwd()
        try:
            os.chdir(tmpdir)
            env = {"CAMUNDA_LOAD_ENVFILE": "yes"}
            result = read_environment(env)
            
            assert result.get("CAMUNDA_CLIENT_ID") == "yes_test"
        finally:
            os.chdir(original_cwd)


def test_load_envfile_via_explicit_configuration():
    """Test loading .env file when enabled via explicit configuration dict."""
    from camunda_orchestration_sdk.runtime.configuration_resolver import ConfigurationResolver

    with tempfile.TemporaryDirectory() as tmpdir:
        env_file = Path(tmpdir) / ".env"
        env_file.write_text(
            "CAMUNDA_CLIENT_ID=explicit_client_id\n"
            "CAMUNDA_CLIENT_SECRET=explicit_secret\n"
        )

        original_cwd = Path.cwd()
        try:
            os.chdir(tmpdir)
            resolved = ConfigurationResolver(
                environment={},
                explicit_configuration={"CAMUNDA_LOAD_ENVFILE": "true"},
            ).resolve()

            assert resolved.effective.CAMUNDA_CLIENT_ID == "explicit_client_id"
            assert resolved.effective.CAMUNDA_CLIENT_SECRET == "explicit_secret"
        finally:
            os.chdir(original_cwd)


def test_load_envfile_from_process_environ(monkeypatch: pytest.MonkeyPatch):
    """Test loading .env file when using the real process environment (environ=None)."""
    with tempfile.TemporaryDirectory() as tmpdir:
        env_file = Path(tmpdir) / ".env"
        env_file.write_text("CAMUNDA_CLIENT_ID=from_process_environ\n")

        original_cwd = Path.cwd()
        try:
            os.chdir(tmpdir)
            monkeypatch.setenv("CAMUNDA_LOAD_ENVFILE", "true")

            result = read_environment()
            assert result.get("CAMUNDA_CLIENT_ID") == "from_process_environ"
        finally:
            os.chdir(original_cwd)
