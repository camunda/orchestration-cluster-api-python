from pathlib import Path
from typing import Any, Dict

def run(context: Dict[str, Any]) -> None:
    """Patch configuration.py 
     Remediation for https://github.com/OpenAPITools/openapi-generator/issues/22415 
     PR in, can remove when https://github.com/OpenAPITools/openapi-generator/pull/22418 is merged
    """
    out_dir = Path(context["out_dir"])
    config_file = out_dir / "camunda_orchestration_sdk" / "configuration.py"
    
    if not config_file.exists():
        print(f"Warning: {config_file} does not exist, skipping patch.")
        return

    print(f"Patching {config_file} to remove urllib3 dependency... (Remove when upstream patch is merged.)")
    content = config_file.read_text(encoding="utf-8")
    
    # 1. Remove urllib3 import
    content = content.replace("import urllib3", "")
    
    # 2. Update logger
    content = content.replace('logging.getLogger("urllib3")', 'logging.getLogger("httpx")')
    
    # 3. Update docstrings
    content = content.replace("override urllib3 default value", "override httpx default value")
    content = content.replace("underlying urllib3 socket", "underlying httpx socket")
    
    # 4. Fix Basic Auth
    # The original code uses urllib3.util.make_headers
    old_basic_auth_pattern = """        return urllib3.util.make_headers(
            basic_auth=username + ':' + password
        ).get('authorization')"""
        
    new_basic_auth = """        import base64
        token = base64.b64encode(f"{username}:{password}".encode('utf-8')).decode("ascii")
        return f"Basic {token}" """
    
    if old_basic_auth_pattern in content:
        content = content.replace(old_basic_auth_pattern, new_basic_auth)
    else:
        print("Warning: Could not find urllib3 basic auth pattern to replace.")

    # 5. Fix HostSettingVariable type error
    # We need to add 'enum_values': [] to the variables in get_host_settings
    # The pattern is:
    # 'default_value': "some_value",
    # }
    # We want to change it to:
    # 'default_value': "some_value",
    # 'enum_values': []
    # }
    
    # Host variable
    content = content.replace(
        "'default_value': \"localhost\",\n                        }",
        "'default_value': \"localhost\",\n                        'enum_values': []\n                        }"
    )
    # Port variable
    content = content.replace(
        "'default_value': \"8080\",\n                        }",
        "'default_value': \"8080\",\n                        'enum_values': []\n                        }"
    )
    # Schema variable
    content = content.replace(
        "'default_value': \"http\",\n                        }",
        "'default_value': \"http\",\n                        'enum_values': []\n                        }"
    )

    config_file.write_text(content, encoding="utf-8")
    print("Successfully patched configuration.py")
