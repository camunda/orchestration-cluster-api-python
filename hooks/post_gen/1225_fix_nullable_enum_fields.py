"""Restore ``nullable: true`` on enum-typed model fields.

``openapi-python-client`` honours ``nullable: true`` for plain scalar
properties -- ``type: string, nullable: true`` correctly becomes
``None | str``. It drops the flag when the property also carries an ``enum``
(or an ``allOf`` reference to an enum schema), emitting a bare, non-optional
enum field instead. A response that legitimately sends ``null`` for such a
field then fails to deserialise with ``ValueError``.

This hook is spec-driven rather than keyed to a fixed list of models: it
re-reads every ``nullable: true`` property from the bundled spec and, wherever
the generator produced the bare-enum shape, rewrites the annotation, the
docstring, ``to_dict`` and ``from_dict`` to admit ``None``.

A property whose generated code does not look like the bare-enum shape at all
is left alone -- the generator handled it correctly, or an earlier hook (e.g.
1000_patch_semantic_types_in_models) already rewrote it. A property that
matches *partially* raises, because a half-rewritten model is worse than an
unpatched one.
"""

from __future__ import annotations

import re
from pathlib import Path

import yaml

# from_dict site, e.g.
#     result = ClusterRebalanceOperationPartitionResult(d.pop("result"))
# The generator wraps long lines, so allow newlines inside the call.
_FROM_DICT = (
    r"^(?P<indent>[ ]+)(?P<field>\w+) = (?P<enum>[A-Z]\w*)"
    r'\(\s*d\.pop\("{json_name}"\)\s*\)'
)


def _snake(name: str) -> str:
    s1 = re.sub(r"(.)([A-Z][a-z]+)", r"\1_\2", name)
    s2 = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", s1)
    return s2.replace("__", "_").lower()


def _mapping(value: object) -> dict[str, object]:
    """Narrow an untyped parsed-spec node to a string-keyed mapping.

    Anything that is not a mapping becomes an empty one, so callers can chain
    ``.get()`` without asserting a shape the spec does not promise.
    """
    if not isinstance(value, dict):
        return {}
    return {key: val for key, val in value.items() if isinstance(key, str)}


def _nullable_properties(spec: object) -> dict[str, set[str]]:
    """Schema name -> JSON property names marked ``nullable: true``."""
    result: dict[str, set[str]] = {}
    schemas = _mapping(_mapping(_mapping(spec).get("components")).get("schemas"))

    for schema_name, schema in schemas.items():
        properties = _mapping(_mapping(schema).get("properties"))
        names = {
            prop_name
            for prop_name, prop in properties.items()
            if _mapping(prop).get("nullable") is True
        }
        if names:
            result[schema_name] = names
    return result


def _patch_field(content: str, json_name: str, model: Path) -> tuple[str, bool]:
    match = re.search(_FROM_DICT.format(json_name=re.escape(json_name)), content, re.M)
    if not match:
        return content, False

    indent = match.group("indent")
    field = match.group("field")
    enum = match.group("enum")

    annotation = re.compile(rf"^    {field}: {enum}$", re.M)
    to_dict = re.compile(rf"^([ ]+){field} = self\.{field}\.value$", re.M)

    if not annotation.search(content) or not to_dict.search(content):
        raise RuntimeError(
            f"{model.name}: field '{field}' deserialises as a bare {enum} but its "
            f"annotation or to_dict body does not match the expected shape. "
            f"Refusing to half-patch the model -- update this hook instead."
        )

    # Splice from_dict first, while the match offsets are still valid.
    content = (
        content[: match.start()]
        + f"{indent}def _parse_{field}(data: object) -> None | {enum}:\n"
        + f"{indent}    if data is None:\n"
        + f"{indent}        return None\n"
        + f"{indent}    return {enum}(data)\n"
        + "\n"
        + f'{indent}{field} = _parse_{field}(d.pop("{json_name}"))'
        + content[match.end() :]
    )
    content = annotation.sub(f"    {field}: None | {enum}", content, count=1)
    content = to_dict.sub(
        rf"\g<1>{field}: None | str\n"
        rf"\g<1>{field} = self.{field}.value if self.{field} is not None else None",
        content,
        count=1,
    )
    content = re.sub(
        rf"^(?P<indent>[ ]+){field} \({enum}\):",
        rf"\g<indent>{field} (None | {enum}):",
        content,
        count=1,
        flags=re.M,
    )
    return content, True


def run(context: dict[str, str]) -> None:
    spec_path = context.get("bundled_spec_path") or context.get("spec_path", "")
    if not spec_path or not Path(spec_path).is_file():
        print("[1225_fix_nullable_enum_fields] no bundled spec, skipping")
        return

    # The bundler always emits a single self-contained document; YAML parses
    # JSON too, so this covers both `bundled_spec.yaml` and a `.json` bundle.
    with open(spec_path, encoding="utf-8") as handle:
        spec: object = yaml.safe_load(handle)

    models = Path(context["out_dir"]).resolve() / "camunda_orchestration_sdk" / "models"

    patched = 0
    for schema_name, json_names in _nullable_properties(spec).items():
        model = models / f"{_snake(schema_name)}.py"
        if not model.exists():
            continue
        content = original = model.read_text(encoding="utf-8")
        for json_name in sorted(json_names):
            content, changed = _patch_field(content, json_name, model)
            patched += changed
        if content != original:
            model.write_text(content, encoding="utf-8")

    print(f"[1225_fix_nullable_enum_fields] made {patched} enum fields nullable")
