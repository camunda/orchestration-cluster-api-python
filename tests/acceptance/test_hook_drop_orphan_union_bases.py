"""Tests for hooks/post_gen/1450_drop_orphan_union_bases.py.

Regression guards for the orphan discriminator-only union-base cleanup. The
detection runs against synthetic specs, and the init-file rewriting runs
against synthetic snippets (single-line and parenthesised multi-line import
forms), so the guards stay meaningful regardless of the current upstream spec.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path
from typing import Any

# Import the numbered hook module via importlib (filename starts with a digit).
_hook_path = (
    Path(__file__).resolve().parents[2]
    / "hooks"
    / "post_gen"
    / "1450_drop_orphan_union_bases.py"
)
_spec = importlib.util.spec_from_file_location("_drop_orphan_union_bases", _hook_path)
assert _spec and _spec.loader
_hook = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_hook)

_find_orphan_bases = _hook._find_orphan_bases
_class_to_module = _hook._class_to_module
_strip_symbol = _hook._strip_symbol


def _object_schema(props: dict[str, Any], required: list[str]) -> dict[str, Any]:
    return {"type": "object", "required": required, "properties": props}


def _union(discriminator: str, mapping: dict[str, str]) -> dict[str, Any]:
    return {
        "discriminator": {"propertyName": discriminator, "mapping": mapping},
        "oneOf": [{"$ref": f"#/components/schemas/{v}"} for v in mapping.values()],
    }


class TestFindOrphanBases:
    def _spec(self) -> dict[str, Any]:
        schemas: dict[str, Any] = {
            # Union 1: discriminator-only base referenced ONLY by its variants.
            "Pet": _union("petType", {"CAT": "Cat", "DOG": "Dog"}),
            "BasePet": _object_schema({"petType": {"type": "string"}}, ["petType"]),
            "Cat": {
                "type": "object",
                "required": ["petType", "meow"],
                "allOf": [
                    {"$ref": "#/components/schemas/BasePet"},
                    # A shared mixin with real fields, composed alongside the base.
                    {"$ref": "#/components/schemas/Timestamped"},
                ],
                "properties": {"meow": {"type": "string"}},
            },
            "Dog": {
                "type": "object",
                "required": ["petType"],
                "allOf": [{"$ref": "#/components/schemas/BasePet"}],
                "properties": {"bark": {"type": "string"}},
            },
            "Timestamped": _object_schema(
                {"createdAt": {"type": "string"}}, ["createdAt"]
            ),
            # Union 2: discriminator-only base ALSO referenced by a property.
            "Vehicle": _union("vehicleType", {"CAR": "Car", "TRUCK": "Truck"}),
            "BaseVehicle": _object_schema(
                {"vehicleType": {"type": "string"}}, ["vehicleType"]
            ),
            "Car": {
                "type": "object",
                "required": ["vehicleType"],
                "allOf": [{"$ref": "#/components/schemas/BaseVehicle"}],
                "properties": {"doors": {"type": "integer"}},
            },
            "Truck": {
                "type": "object",
                "required": ["vehicleType"],
                "allOf": [{"$ref": "#/components/schemas/BaseVehicle"}],
                "properties": {"axles": {"type": "integer"}},
            },
            "Garage": _object_schema(
                {"spec": {"$ref": "#/components/schemas/BaseVehicle"}}, []
            ),
            # Union 3: discriminator-only base referenced ONLY by a response body.
            "Shape": _union("shapeType", {"BOX": "Box", "SPHERE": "Sphere"}),
            "BaseShape": _object_schema(
                {"shapeType": {"type": "string"}}, ["shapeType"]
            ),
            "Box": {
                "type": "object",
                "required": ["shapeType"],
                "allOf": [{"$ref": "#/components/schemas/BaseShape"}],
                "properties": {"width": {"type": "integer"}},
            },
            "Sphere": {
                "type": "object",
                "required": ["shapeType"],
                "allOf": [{"$ref": "#/components/schemas/BaseShape"}],
                "properties": {"radius": {"type": "integer"}},
            },
        }
        return {
            "components": {"schemas": schemas},
            "paths": {
                "/shapes/base": {
                    "get": {
                        "operationId": "getShapeBase",
                        "responses": {
                            "200": {
                                "description": "ok",
                                "content": {
                                    "application/json": {
                                        "schema": {
                                            "$ref": "#/components/schemas/BaseShape"
                                        }
                                    }
                                },
                            }
                        },
                    }
                }
            },
        }

    def test_only_truly_orphan_discriminator_base_is_reported(self) -> None:
        orphans = _find_orphan_bases(self._spec())

        # BasePet is referenced only as the allOf base of Cat/Dog -> orphan.
        assert orphans == {"BasePet"}, orphans

    def test_referenced_and_mixin_bases_are_preserved(self) -> None:
        orphans = _find_orphan_bases(self._spec())

        # Referenced via a property (BaseVehicle), via a response body
        # (BaseShape), and a real mixin composed via allOf (Timestamped).
        assert "BaseVehicle" not in orphans
        assert "BaseShape" not in orphans
        assert "Timestamped" not in orphans

    def test_no_unions_yields_no_orphans(self) -> None:
        assert _find_orphan_bases({"components": {"schemas": {}}}) == set()


class TestClassToModule:
    def test_maps_single_and_multi_line_imports(self, tmp_path: Path) -> None:
        models_init = tmp_path / "__init__.py"
        models_init.write_text(
            "from .base_pet import BasePet\n"
            "from .some_very_long_module_name import (\n"
            "    SomeVeryLongClassName,\n"
            ")\n"
            '__all__ = ["BasePet", "SomeVeryLongClassName"]\n',
            encoding="utf-8",
        )

        mapping = _class_to_module(models_init)

        assert mapping["BasePet"] == "base_pet"
        assert mapping["SomeVeryLongClassName"] == "some_very_long_module_name"


class TestStripSymbol:
    def test_removes_single_line_dedicated_import_and_all_entry(
        self, tmp_path: Path
    ) -> None:
        path = tmp_path / "__init__.py"
        path.write_text(
            "from .base_pet import BasePet\n"
            "from .other import Other\n"
            '__all__ = [\n    "BasePet",\n    "Other",\n]\n',
            encoding="utf-8",
        )

        _strip_symbol(path, "BasePet", "base_pet")
        result = path.read_text(encoding="utf-8")

        assert "BasePet" not in result
        assert "from .other import Other" in result
        assert '"Other",' in result

    def test_removes_multiline_dedicated_import_block_without_leaving_stub(
        self, tmp_path: Path
    ) -> None:
        path = tmp_path / "__init__.py"
        path.write_text(
            "from .base_pet import (\n    BasePet,\n)\n"
            "from .other import Other\n"
            '__all__ = [\n    "BasePet",\n    "Other",\n]\n',
            encoding="utf-8",
        )

        _strip_symbol(path, "BasePet", "base_pet")
        result = path.read_text(encoding="utf-8")

        assert "BasePet" not in result
        # No stale empty import block left behind.
        assert "from .base_pet import" not in result
        assert "import (\n)" not in result
        assert "from .other import Other" in result

    def test_removes_member_from_shared_grouped_import(self, tmp_path: Path) -> None:
        path = tmp_path / "__init__.py"
        path.write_text(
            "from camunda_orchestration_sdk.models import (\n"
            "    Alpha,\n"
            "    BasePet,\n"
            "    Beta,\n"
            ")\n"
            '__all__: list[str] = [\n    "Alpha",\n    "BasePet",\n    "Beta",\n]\n',
            encoding="utf-8",
        )

        _strip_symbol(path, "BasePet", "base_pet")
        result = path.read_text(encoding="utf-8")

        assert "BasePet" not in result
        assert "Alpha," in result
        assert "Beta," in result
        assert '"Alpha",' in result
        assert '"Beta",' in result

    def test_does_not_strip_prefixed_sibling_symbols(self, tmp_path: Path) -> None:
        path = tmp_path / "__init__.py"
        path.write_text(
            "from .base_pet import BasePet\n"
            "from .base_pet_extended import BasePetExtended\n"
            '__all__ = [\n    "BasePet",\n    "BasePetExtended",\n]\n',
            encoding="utf-8",
        )

        _strip_symbol(path, "BasePet", "base_pet")
        result = path.read_text(encoding="utf-8")

        assert "from .base_pet_extended import BasePetExtended" in result
        assert '"BasePetExtended",' in result
        assert "from .base_pet import BasePet" not in result
