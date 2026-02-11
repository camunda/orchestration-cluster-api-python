from __future__ import annotations

from pathlib import Path
from typing import Any, cast
from urllib.request import urlopen

import yaml
import jsonref as _jsonref  # type: ignore[import-untyped]

jsonref: Any = _jsonref

def yaml_loader(uri: str, **kwargs: Any) -> Any:
    """Loader for jsonref that handles YAML files."""
    # Handle file:// URIs or plain paths (though jsonref usually passes URIs)
    if uri.startswith("file://"):
        path = uri[7:]
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)
    else:
        # Fallback for http/https if needed, or just fail
        with urlopen(uri) as response:
            return yaml.safe_load(response.read().decode("utf-8"))

def bundle_spec(input_path: Path, output_path: Path) -> None:
    with open(input_path, "r", encoding="utf-8") as f:
        spec = yaml.safe_load(f)
    
    # jsonref resolves references. We need to tell it the base URI so it can find relative files.
    # We use the input_path's parent directory as the base.
    base_uri = input_path.absolute().as_uri()
    
    resolved = jsonref.replace_refs(spec, base_uri=base_uri, loader=yaml_loader, load_on_repr=False)
    
    # Force resolution by traversing the object
    # jsonref is lazy, so we need to dump it to string or traverse it to trigger loading.
    # However, jsonref objects are proxies. To get a clean dict, we can dump to JSON and load back,
    # or use a recursive function to convert proxies to dicts.
    # Dumping to JSON is safer/easier.
    
    # Note: We use JSON dump/load to resolve all proxies.
    # resolved_dict = json.loads(json.dumps(resolved, default=str))
    
    # Let's try to just use the proxy directly and see if yaml.safe_dump handles it, 
    # or convert it recursively.
    # But first, let's debug what resolved looks like.
    # print(f"Type of resolved path: {type(resolved['paths']['/audit-logs/search'])}")
    # print(f"Value: {resolved['paths']['/audit-logs/search']}")

    # If jsonref proxies are not being treated as dicts by json.dumps, it might be because 
    # they are not exactly dicts.
    # Let's try a recursive conversion function instead of json.dumps/loads.
    
    def unwrap(obj: Any) -> Any:
        if isinstance(obj, dict):
            obj_dict = cast(dict[Any, Any], obj)
            return {k: unwrap(v) for k, v in obj_dict.items()}
        elif isinstance(obj, list):
            obj_list = cast(list[Any], obj)
            return [unwrap(v) for v in obj_list]
        else:
            return obj
            
    resolved_dict = unwrap(resolved)
    
    with open(output_path, "w", encoding="utf-8") as f:
        yaml.safe_dump(resolved_dict, f, sort_keys=False)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 3:
        print("Usage: python bundle.py <input_yaml> <output_yaml>")
        sys.exit(1)
    
    bundle_spec(Path(sys.argv[1]), Path(sys.argv[2]))
