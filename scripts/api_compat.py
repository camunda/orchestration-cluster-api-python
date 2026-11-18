#!/usr/bin/env python3
"""Public API compatibility check against the last published release of a major.

Stable branches regenerate from a moving upstream spec, and the release pipeline commits
that drift without review. This compares the public API of a published release (the
baseline, downloaded from PyPI) with the package in ``generated/`` and lists every change
that would stop customer code written against the baseline from type-checking or running.

Each package is imported in its own subprocess and described as JSON: modules and their
public names, classes (members, constructor, enum members, bases) and every annotation,
resolved to a canonical type tree. The two descriptions are then compared.

Direction matters for types. A value the SDK hands to the caller (a return type, an
attribute of a result model) may only narrow: ``str`` becoming ``str | None`` breaks
``x.upper()``. A value the caller hands to the SDK (a parameter, a request model field)
may only widen. Data models (attrs, dataclasses, TypedDicts, pydantic) are classified by
how the baseline API reaches them: reached only through parameters -> request model
(constructor checked, attribute reads not); reached only through return values -> result
model (attribute reads checked, constructor not); both -> both. A model that no API
accepts or returns (an orphan schema) only has to keep existing.

Exit codes: 0 compatible, 1 breaking changes found, 2 tool or setup error.
"""

from __future__ import annotations

import argparse
import ast
import collections.abc
import enum
import hashlib
import importlib
import importlib.util
import inspect
import json
import os
import pkgutil
import re
import subprocess
import sys
import tempfile
import textwrap
import traceback
import types
import typing
import urllib.request
import warnings
import zipfile
from collections.abc import Iterator
from pathlib import Path
from typing import Any

PACKAGE = "camunda_orchestration_sdk"
DISTRIBUTION = "camunda-orchestration-sdk"
PYPI_URL = "https://pypi.org/pypi/{dist}/json"
REPO_ROOT = Path(__file__).resolve().parents[1]

INPUT = "input"
OUTPUT = "output"

Json = dict[str, Any]


class SetupError(Exception):
    """The check could not run (network, download, import). Maps to exit code 2."""


# --------------------------------------------------------------------------------------
# Baseline resolution (PyPI)
# --------------------------------------------------------------------------------------

_RELEASE_RE = re.compile(r"^(\d+)\.(\d+)\.(\d+)$")


def fetch_pypi_metadata(dist: str = DISTRIBUTION) -> Json:
    url = PYPI_URL.format(dist=dist)
    try:
        with urllib.request.urlopen(url, timeout=60) as resp:
            return json.load(resp)
    except Exception as exc:
        raise SetupError(f"cannot read {url}: {exc}") from exc


def latest_release(metadata: Json, major: int) -> str | None:
    """Newest non-prerelease, non-yanked ``major.x.y`` on the registry, or None."""
    best: tuple[int, int, int] | None = None
    for version, files in metadata.get("releases", {}).items():
        m = _RELEASE_RE.match(version)
        if not m or int(m.group(1)) != major:
            continue
        if not files or all(f.get("yanked") for f in files):
            continue
        key = (int(m.group(1)), int(m.group(2)), int(m.group(3)))
        if best is None or key > best:
            best = key
    return None if best is None else ".".join(map(str, best))


def download_baseline(metadata: Json, version: str, dest: Path) -> Path:
    """Download and unpack the release's pure-Python wheel; return the import root."""
    files = metadata.get("releases", {}).get(version)
    if not files:
        raise SetupError(f"{DISTRIBUTION} {version} is not published on PyPI")
    wheels = [f for f in files if f.get("filename", "").endswith("-py3-none-any.whl")]
    if not wheels:
        raise SetupError(f"{DISTRIBUTION} {version} has no py3-none-any wheel")
    wheel = wheels[0]
    try:
        with urllib.request.urlopen(wheel["url"], timeout=120) as resp:
            payload = resp.read()
    except Exception as exc:
        raise SetupError(f"cannot download {wheel['url']}: {exc}") from exc
    expected = wheel.get("digests", {}).get("sha256")
    if not expected or hashlib.sha256(payload).hexdigest() != expected:
        raise SetupError(f"sha256 mismatch for {wheel['filename']}")
    archive = dest / wheel["filename"]
    archive.write_bytes(payload)
    root = dest / "site"
    with zipfile.ZipFile(archive) as zf:
        zf.extractall(root)
    return root


# --------------------------------------------------------------------------------------
# Describing a package (runs in a subprocess with the package root first on sys.path)
# --------------------------------------------------------------------------------------

_ABCS = [
    getattr(collections.abc, name)
    for name in collections.abc.__all__
    if isinstance(getattr(collections.abc, name), type)
]

_NUMERIC_PROMOTION = {
    "builtins:int": {"builtins:float", "builtins:complex"},
    "builtins:float": {"builtins:complex"},
}

# Variance of each type argument of a generic: "+" covariant, "-" contravariant, "="
# invariant. A trailing "*" repeats the last entry. Generics not listed are invariant.
_VARIANCE = {
    "builtins:tuple": "+*",
    "builtins:frozenset": "+",
    "builtins:type": "+",
    "collections.abc:Iterable": "+",
    "collections.abc:Iterator": "+",
    "collections.abc:Reversible": "+",
    "collections.abc:Collection": "+",
    "collections.abc:Container": "+",
    "collections.abc:Sequence": "+",
    "collections.abc:Set": "+",
    "collections.abc:KeysView": "+",
    "collections.abc:ValuesView": "+",
    "collections.abc:ItemsView": "++",
    "collections.abc:Mapping": "=+",
    "collections.abc:Awaitable": "+",
    "collections.abc:AsyncIterable": "+",
    "collections.abc:AsyncIterator": "+",
    "collections.abc:Generator": "+-+",
    "collections.abc:Coroutine": "+-+",
    "collections.abc:AsyncGenerator": "+-",
}


def _variance(origin: str, index: int) -> str:
    spec = _VARIANCE.get(origin, "=*")
    if spec.endswith("*"):
        spec = spec[:-1]
        return spec[min(index, len(spec) - 1)]
    return spec[index] if index < len(spec) else "="


# Special methods that are construction or serialisation hooks, not API callers use.
_HOOK_DUNDERS = frozenset(
    {
        "__init_subclass__",
        "__class_getitem__",
        "__post_init__",
        "__attrs_pre_init__",
        "__attrs_post_init__",
        "__attrs_init__",
        "__getstate__",
        "__setstate__",
        "__replace__",
        # Generated by the 3.14 compiler for annotated class bodies (PEP 649).
        "__annotate__",
        "__annotate_func__",
    }
)


def _is_public_dunder(name: str, raw: Any) -> bool:
    """A special method callers reach through syntax (``with``, ``x[k]``, ``len(x)``)."""
    return (
        name.startswith("__")
        and name.endswith("__")
        and name not in _HOOK_DUNDERS
        and not hasattr(object, name)  # __init__, __eq__, __repr__, ...: always present
        and (inspect.isfunction(raw) or isinstance(raw, (staticmethod, classmethod)))
    )


def _canon(cls: type) -> str:
    return f"{cls.__module__}:{cls.__qualname__}"


def _is_private_module(name: str) -> bool:
    return any(part.startswith("_") for part in name.split(".")[1:])


def _defined_names(module: types.ModuleType) -> list[str]:
    """Names bound at module level by the module's own code, plus, for a package, the SDK
    names it imports (its re-exports). A plain module's imports are incidental."""
    explicit = getattr(module, "__all__", None)
    if explicit is not None:
        return [str(n) for n in explicit]
    path = getattr(module, "__file__", None)
    if not path or not path.endswith(".py"):
        return []
    tree = ast.parse(Path(path).read_text(encoding="utf-8"))
    is_package = hasattr(module, "__path__")
    root_package = module.__name__.split(".")[0]
    names: list[str] = []

    def visit(body: list[ast.stmt]) -> None:
        for node in body:
            if isinstance(
                node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
            ):
                names.append(node.name)
            elif isinstance(node, ast.ImportFrom) and is_package and (
                node.level > 0 or (node.module or "").split(".")[0] == root_package
            ):
                for alias in node.names:
                    if alias.name != "*":
                        names.append(alias.asname or alias.name)
                        continue
                    target = importlib.util.resolve_name(
                        "." * node.level + (node.module or ""), module.__name__
                    )
                    source = sys.modules.get(target)
                    if source is not None:
                        exported = getattr(source, "__all__", vars(source))
                        names.extend(name for name in exported if name in vars(module))
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        names.append(target.id)
            elif isinstance(node, ast.AnnAssign) and isinstance(node.target, ast.Name):
                names.append(node.target.id)
            elif isinstance(node, ast.If):
                if not (
                    isinstance(node.test, ast.Name)
                    and node.test.id == "TYPE_CHECKING"
                ):
                    visit(node.body)
                    visit(node.orelse)
            elif isinstance(node, ast.Try):
                visit(node.body)
                for handler in node.handlers:
                    visit(handler.body)
                visit(node.orelse)
                visit(node.finalbody)

    visit(tree.body)
    return [n for n in dict.fromkeys(names) if not n.startswith("_")]


class Describer:
    def __init__(self, package: str) -> None:
        self.package = package
        self.symbols: dict[str, Json] = {}
        self.classes: dict[str, Json] = {}
        self.supertypes: dict[str, list[str]] = {}
        self._root_ns: dict[str, Any] = {}
        self._tc_cache: dict[str, dict[str, Any]] = {}

    # ---- entry point -------------------------------------------------------------

    def describe(self, expected_root: Path) -> Json:
        root = importlib.import_module(self.package)
        origin = Path(getattr(root, "__file__", "") or "").resolve()
        if expected_root.resolve() not in origin.parents:
            raise SetupError(
                f"{self.package} was imported from {origin}, not from {expected_root}"
            )
        for name in ("models",):
            sub = getattr(root, name, None)
            if isinstance(sub, types.ModuleType):
                self._root_ns.update(vars(sub))
        self._root_ns.update(vars(root))

        broken: dict[str, str] = {}

        def onerror(name: str) -> None:
            broken[name] = repr(sys.exc_info()[1])

        modules = {self.package} | {
            info.name
            for info in pkgutil.walk_packages(
                root.__path__, self.package + ".", onerror=onerror
            )
        }
        for modname in sorted(modules | broken.keys()):
            if _is_private_module(modname):
                continue
            # A module that does not import cannot be used; record it rather than abort,
            # so a release that shipped one can still serve as a baseline.
            try:
                module = importlib.import_module(modname)
            except Exception as exc:
                self.symbols[modname] = {"kind": "module", "broken": repr(exc)}
                continue
            self.symbols[modname] = {"kind": "module"}
            for attr in _defined_names(module):
                if attr.startswith("_") or not hasattr(module, attr):
                    continue
                obj = getattr(module, attr)
                if isinstance(obj, typing.TypeVar):
                    continue
                self.symbols[f"{modname}:{attr}"] = self._describe_obj(obj, module, attr)
        return {
            "package": self.package,
            "symbols": self.symbols,
            "classes": self.classes,
            "supertypes": self.supertypes,
        }

    # ---- objects -----------------------------------------------------------------

    def _describe_obj(self, obj: Any, module: types.ModuleType, attr: str) -> Json:
        if isinstance(obj, types.ModuleType):
            return {"kind": "module"}
        if isinstance(obj, type):
            self._add_class(obj)
            return {"kind": "class", "ref": _canon(obj)}
        if inspect.isroutine(obj):
            return {"kind": "function", "sig": self._signature(obj, vars(module))}
        if typing.get_origin(obj) is not None or isinstance(obj, types.UnionType):
            return {"kind": "alias", "type": self._type(obj, vars(module))}
        # The declared type, if any: `X: T | None = T()` may become None later.
        try:
            ann = inspect.get_annotations(module).get(attr, type(obj))
        except Exception:
            ann = type(obj)
        return {"kind": "value", "type": self._type(ann, self._ns(vars(module)))}

    def _ns(self, *namespaces: dict[str, Any]) -> dict[str, Any]:
        merged = dict(self._root_ns)
        for ns in namespaces:
            merged.update(self._type_checking_imports(ns))
            merged.update(ns)
        return merged

    def _type_checking_imports(self, ns: dict[str, Any]) -> dict[str, Any]:
        """Names a module imports only under ``if TYPE_CHECKING:`` (for annotations)."""
        modname = ns.get("__name__")
        if not isinstance(modname, str) or modname not in sys.modules:
            return {}
        if modname in self._tc_cache:
            return self._tc_cache[modname]
        found: dict[str, Any] = {}
        path = ns.get("__file__")
        if isinstance(path, str) and path.endswith(".py"):
            tree = ast.parse(Path(path).read_text(encoding="utf-8"))
            imports: list[ast.stmt] = [
                stmt
                for node in tree.body
                if isinstance(node, ast.If)
                and isinstance(node.test, (ast.Name, ast.Attribute))
                and ast.unparse(node.test).endswith("TYPE_CHECKING")
                for stmt in node.body
                if isinstance(stmt, (ast.Import, ast.ImportFrom))
            ]
            if imports:
                scope: dict[str, Any] = {
                    "__name__": modname,
                    "__package__": ns.get("__package__"),
                }
                code = compile(ast.Module(body=imports, type_ignores=[]), path, "exec")
                exec(code, scope)  # the module's own imports, already trusted above
                found = {k: v for k, v in scope.items() if not k.startswith("__")}
        self._tc_cache[modname] = found
        return found

    def _record_supertypes(self, cls: type) -> None:
        key = _canon(cls)
        if key in self.supertypes:
            return
        names = [_canon(c) for c in cls.__mro__]
        for abc in _ABCS:
            try:
                if issubclass(cls, abc):
                    names.append(_canon(abc))
            except TypeError:
                pass
        self.supertypes[key] = list(dict.fromkeys(names))

    def _typevar_key(self, var: typing.TypeVar) -> str:
        return f"{var.__module__}:{var.__name__}"

    def _substitute_typevars(self, value: Any, substitutions: dict[str, Json]) -> Any:
        if isinstance(value, list):
            return [self._substitute_typevars(item, substitutions) for item in value]
        if not isinstance(value, dict):
            return value
        if value.get("k") == "typevar" and value["n"] in substitutions:
            return substitutions[value["n"]]
        return {
            key: self._substitute_typevars(child, substitutions)
            for key, child in value.items()
        }

    def _class_specializations(
        self, cls: type, ns: dict[str, Any]
    ) -> dict[type, dict[str, Json]]:
        specializations: dict[type, dict[str, Json]] = {}

        def visit(current: type, substitutions: dict[str, Json]) -> None:
            if current in specializations:
                return
            specializations[current] = substitutions
            current_ns = self._ns(vars(sys.modules[current.__module__]))
            for base in getattr(current, "__orig_bases__", current.__bases__):
                origin = typing.get_origin(base) or base
                if not isinstance(origin, type) or not self._is_ours(origin):
                    continue
                args = typing.get_args(base)
                base_substitutions: dict[str, Json] = {}
                for index, param in enumerate(getattr(origin, "__parameters__", ())):
                    actual = args[index] if index < len(args) else typing.Any
                    described = self._type(actual, current_ns)
                    base_substitutions[self._typevar_key(param)] = self._substitute_typevars(
                        described, substitutions
                    )
                visit(origin, base_substitutions)

        initial = {
            self._typevar_key(param): self._type(param, ns)
            for param in getattr(cls, "__parameters__", ())
        }
        visit(cls, initial)
        return specializations

    def _is_ours(self, cls: type) -> bool:
        mod = getattr(cls, "__module__", "") or ""
        return mod == self.package or mod.startswith(self.package + ".")

    def _add_class(self, cls: type) -> None:
        self._record_supertypes(cls)
        key = _canon(cls)
        if key in self.classes or not self._is_ours(cls):
            return
        info: Json = {"bases": [_canon(c) for c in cls.__mro__[1:] if c is not object]}
        self.classes[key] = info
        module_ns = vars(sys.modules[cls.__module__])
        ns = self._ns(module_ns)
        specializations = self._class_specializations(cls, ns)

        if isinstance(cls, enum.EnumMeta):
            info["kind"] = "enum"
            info["members"] = {
                name: repr(member.value) for name, member in cls.__members__.items()
            }
        elif typing.is_typeddict(cls):
            info["kind"] = "typeddict"
            try:
                annotations = typing.get_type_hints(
                    cls, globalns=ns, localns=ns, include_extras=True
                )
            except Exception:
                annotations = inspect.get_annotations(cls)
            required = getattr(cls, "__required_keys__", frozenset())
            info["keys"] = {
                key_name: {
                    "type": self._type(
                        typing.get_args(ann)[0]
                        if getattr(typing.get_origin(ann), "__name__", "")
                        in ("Required", "NotRequired")
                        else ann,
                        ns,
                    ),
                    "required": (
                        getattr(typing.get_origin(ann), "__name__", "") == "Required"
                        if getattr(typing.get_origin(ann), "__name__", "")
                        in ("Required", "NotRequired")
                        else key_name in required
                    ),
                }
                for key_name, ann in annotations.items()
            }
            return
        elif _is_protocol(cls):
            info["kind"] = "protocol"
        elif hasattr(cls, "__attrs_attrs__"):
            info["kind"] = "attrs"
        elif hasattr(cls, "__dataclass_fields__"):
            info["kind"] = "dataclass"
        elif hasattr(cls, "model_fields") and hasattr(cls, "model_validate"):
            info["kind"] = "pydantic"
        else:
            info["kind"] = "class"

        if info["kind"] != "enum":
            init = inspect.getattr_static(cls, "__init__", None)
            get_overloads = getattr(typing, "get_overloads", None)
            has_init_overloads = (
                inspect.isfunction(init) and get_overloads is not None and bool(get_overloads(init))
            )
            init_overloads = (
                self._signature(init, ns, skip_first=True) if has_init_overloads else None
            )
            if init_overloads and init_overloads.get("overloads"):
                info["init"] = self._substitute_typevars(
                    init_overloads, specializations.get(cls, {})
                )
            else:
                try:
                    ctor = inspect.signature(cls)
                except (TypeError, ValueError):
                    ctor = None
                if ctor is not None:
                    info["init"] = self._substitute_typevars(
                        self._signature_from(ctor, ns, is_async=False),
                        specializations.get(cls, {}),
                    )

        attributes: dict[str, Json] = {}
        annotated: set[str] = set()
        members: dict[str, Json] = {}
        for klass in reversed(cls.__mro__):
            if not self._is_ours(klass):
                continue
            klass_ns = self._ns(vars(sys.modules[klass.__module__]))
            substitutions = specializations.get(klass, {})
            declarations = inspect.get_annotations(klass)
            for name, ann in declarations.items():
                if name.startswith("_"):
                    continue
                annotated.add(name)
                attributes[name] = self._substitute_typevars(
                    self._type(ann, klass_ns), substitutions
                )
            for name, raw in vars(klass).items():
                if name.startswith("_") and not _is_public_dunder(name, raw):
                    continue
                if info["kind"] == "enum" and name in cls.__members__:
                    continue
                member = self._describe_member(raw, klass_ns)
                if member is not None:
                    members[name] = self._substitute_typevars(member, substitutions)
            if info["kind"] == "class":
                for name, (t, explicit) in self._init_attributes(klass, klass_ns).items():
                    if name not in declarations and (explicit or name not in annotated):
                        attributes[name] = self._substitute_typevars(t, substitutions)
                        if explicit:
                            annotated.add(name)
        for name, member in list(members.items()):
            # A defaulted field's class-level value is the default, not the member's type.
            if member["kind"] == "value" and name in attributes:
                del members[name]
            else:
                attributes.pop(name, None)
        info["attributes"] = attributes
        info["methods"] = members

    def _init_attributes(self, klass: type, ns: dict[str, Any]) -> dict[str, tuple[Json, bool]]:
        """Public ``self.x = ...`` assignments in ``__init__``, read from its source."""
        init = vars(klass).get("__init__")
        if not inspect.isfunction(init):
            return {}
        try:
            tree = ast.parse(textwrap.dedent(inspect.getsource(init)))
            params = inspect.signature(init).parameters
        except (OSError, TypeError, ValueError, SyntaxError):
            return {}
        fn = tree.body[0]
        if not isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)) or not fn.args.args:
            return {}
        self_name = fn.args.args[0].arg
        found: dict[str, tuple[Json, bool]] = {}
        for node in ast.walk(fn):
            if isinstance(node, ast.AnnAssign):
                targets, ann, value = [node.target], node.annotation, node.value
            elif isinstance(node, ast.Assign):
                targets, ann, value = node.targets, None, node.value
            else:
                continue
            for target in targets:
                if not (
                    isinstance(target, ast.Attribute)
                    and isinstance(target.value, ast.Name)
                    and target.value.id == self_name
                    and not target.attr.startswith("_")
                ):
                    continue
                if ann is not None:
                    t = self._type(ast.unparse(ann), ns)
                elif isinstance(value, ast.Name) and value.id in params:
                    t = self._type(params[value.id].annotation, {**ns, **init.__globals__})
                else:
                    t = {"k": "any"}
                if ann is not None or target.attr not in found:
                    found[target.attr] = (t, ann is not None)
        return found

    def _describe_member(self, raw: Any, ns: dict[str, Any]) -> Json | None:
        if isinstance(raw, property):
            ret = inspect.signature(raw.fget).return_annotation if raw.fget else None
            return {"kind": "property", "type": self._type(ret, ns)}
        if isinstance(raw, staticmethod):
            return {
                "kind": "method",
                "binding": "static",
                "sig": self._signature(raw.__func__, ns),
            }
        if isinstance(raw, classmethod):
            return {
                "kind": "method",
                "binding": "class",
                "sig": self._signature(raw.__func__, ns, skip_first=True),
            }
        if inspect.isfunction(raw):
            return {
                "kind": "method",
                "binding": "instance",
                "sig": self._signature(raw, ns, skip_first=True),
            }
        if hasattr(raw, "__get__") and hasattr(raw, "func"):  # functools.cached_property
            ret = inspect.signature(raw.func).return_annotation
            return {"kind": "property", "type": self._type(ret, ns)}
        if isinstance(raw, (types.MemberDescriptorType, types.GetSetDescriptorType)):
            return None
        return {"kind": "value", "type": self._type(type(raw), ns)}

    # ---- signatures --------------------------------------------------------------

    def _signature(
        self,
        func: Any,
        ns: dict[str, Any],
        *,
        skip_first: bool = False,
        with_overloads: bool = True,
    ) -> Json:
        globs = getattr(func, "__globals__", None)
        ns = self._ns(ns, globs) if isinstance(globs, dict) else ns
        try:
            sig = inspect.signature(func)
        except (TypeError, ValueError):
            return {"params": [], "returns": {"k": "any"}, "async": False, "opaque": True}
        if skip_first:
            params = list(sig.parameters.values())[1:]
            sig = sig.replace(parameters=params)
        is_async = inspect.iscoroutinefunction(func)
        described = self._signature_from(sig, ns, is_async=is_async)
        if not with_overloads:
            return described
        get_overloads = getattr(typing, "get_overloads", None)
        if get_overloads is None:
            raise SetupError("recording @overload signatures needs Python 3.11+")
        overloads = [
            self._signature(o, ns, skip_first=skip_first, with_overloads=False)
            for o in get_overloads(func)
        ]
        if overloads:
            # Type checkers see only the overloads; their async-ness is the implementation's.
            for o in overloads:
                o["async"] = is_async
            described["overloads"] = overloads
        return described

    def _signature_from(
        self, sig: inspect.Signature, ns: dict[str, Any], *, is_async: bool
    ) -> Json:
        return {
            "params": [
                {
                    "name": p.name,
                    "kind": p.kind.name,
                    "has_default": p.default is not inspect.Parameter.empty,
                    "type": self._type(p.annotation, ns),
                }
                for p in sig.parameters.values()
            ],
            "returns": self._type(sig.return_annotation, ns),
            "async": is_async,
        }

    # ---- types -------------------------------------------------------------------

    def _type(self, ann: Any, ns: dict[str, Any]) -> Json:
        if ann is inspect.Parameter.empty or ann is inspect.Signature.empty:
            return {"k": "any"}
        if isinstance(ann, typing.ForwardRef):
            ann = ann.__forward_arg__
        for _ in range(3):  # quoted names inside a postponed annotation
            if not isinstance(ann, str):
                break
            text = ann
            try:
                ann = eval(text, ns)  # annotations of code already imported above
            except Exception:
                return {"k": "unresolved", "text": text}
        if ann is None or ann is type(None):
            return {"k": "none"}
        if ann is typing.Any:
            return {"k": "any"}
        if isinstance(ann, typing.TypeVar):
            if ann.__bound__ is not None:
                bound = self._type(ann.__bound__, ns)
                domain_kind = "bound"
            elif ann.__constraints__:
                bound = {"k": "union", "items": [self._type(c, ns) for c in ann.__constraints__]}
                domain_kind = "constraints"
            else:
                bound = {"k": "name", "n": "builtins:object"}
                domain_kind = "unbounded"
            return {
                "k": "typevar",
                "n": f"{ann.__module__}:{ann.__name__}",
                "display": ann.__name__,
                "domain_kind": domain_kind,
                "domain": bound,
            }
        if repr(ann) in ("typing.Self", "typing_extensions.Self", "typing.LiteralString"):
            return {"k": "any"}
        if getattr(ann, "__supertype__", None) is not None:  # typing.NewType
            return {
                "k": "newtype",
                "n": f"{ann.__module__}:{ann.__qualname__}",
                "super": self._type(ann.__supertype__, ns),
            }
        origin = typing.get_origin(ann)
        args = typing.get_args(ann)
        if origin is typing.Union or isinstance(ann, types.UnionType):
            items: list[Json] = []
            for arg in args:
                t = self._type(arg, ns)
                items.extend(t["items"] if t["k"] == "union" else [t])
            return {"k": "union", "items": items}
        if origin is typing.Literal:
            return {
                "k": "literal",
                "values": [[_canon(type(v)), repr(v)] for v in args],
            }
        if origin is typing.Annotated:
            return self._type(args[0], ns)
        if origin is collections.abc.Callable:
            if args and isinstance(args[0], list):
                params = [self._type(a, ns) for a in args[0]]
            else:
                params = None
            ret = self._type(args[-1], ns) if args else {"k": "any"}
            return {"k": "callable", "params": params, "returns": ret}
        if origin is not None and isinstance(origin, type):
            self._record_supertypes(origin)
            return {
                "k": "generic",
                "n": _canon(origin),
                "args": [
                    {"k": "ellipsis"} if a is Ellipsis else self._type(a, ns)
                    for a in args
                ],
            }
        if isinstance(ann, type):
            self._add_class(ann)
            return {"k": "name", "n": _canon(ann)}
        return {"k": "unresolved", "text": repr(ann)}


def _is_protocol(cls: type) -> bool:
    return bool(getattr(cls, "_is_protocol", False)) and typing.Protocol in getattr(
        cls, "__mro__", ()
    )


def describe_in_subprocess(root: Path, package: str) -> Json:
    """Describe ``package`` as importable from ``root``, isolated from this process."""
    cmd = [sys.executable, str(Path(__file__).resolve()), "--describe", str(root)]
    cmd += ["--package", package]
    env = dict(os.environ)
    env.pop("PYTHONPATH", None)
    proc = subprocess.run(cmd, capture_output=True, text=True, env=env, check=False)
    if proc.returncode != 0:
        raise SetupError(
            f"describing {package} from {root} failed:\n{proc.stderr.strip()[-4000:]}"
        )
    return json.loads(proc.stdout)


# --------------------------------------------------------------------------------------
# Comparison
# --------------------------------------------------------------------------------------


def render(t: Json) -> str:
    k = t["k"]
    if k == "any":
        return "Any"
    if k == "none":
        return "None"
    if k == "ellipsis":
        return "..."
    if k == "typevar":
        return t["display"]
    if k in ("name", "newtype"):
        mod, qual = t["n"].split(":", 1)
        return qual if mod != "typing" else f"typing.{qual}"
    if k == "union":
        return " | ".join(render(i) for i in t["items"])
    if k == "literal":
        return "Literal[" + ", ".join(v for _, v in t["values"]) + "]"
    if k == "generic":
        name = render({"k": "name", "n": t["n"]})
        if not t["args"]:
            return name
        return f"{name}[" + ", ".join(render(a) for a in t["args"]) + "]"
    if k == "callable":
        params = "..." if t["params"] is None else ", ".join(map(render, t["params"]))
        return f"Callable[[{params}], {render(t['returns'])}]"
    return t.get("text", "?")


def render_sig(sig: Json) -> str:
    stars = {"VAR_POSITIONAL": "*", "VAR_KEYWORD": "**"}
    params = ", ".join(
        f"{stars.get(p['kind'], '')}{p['name']}: {render(p['type'])}" for p in sig["params"]
    )
    return f"({params}) -> {render(sig['returns'])}"


class Checker:
    def __init__(self, old: Json, new: Json) -> None:
        self.old = old
        self.new = new
        self.breaks: list[str] = []
        self.directions: dict[str, set[str]] = {}

    def run(self) -> list[str]:
        self._classify_models()
        for key, old_sym in sorted(self.old["symbols"].items()):
            self._check_symbol(key, old_sym)
        for key in sorted(self.old["classes"]):
            if key in self.new["classes"]:
                self._check_class(key)
        return sorted(dict.fromkeys(self.breaks))

    def _break(self, where: str, what: str) -> None:
        self.breaks.append(f"{where}: {what}")

    # ---- assignability -----------------------------------------------------------

    def _supers(self, side: Json, name: str) -> list[str]:
        return side["supertypes"].get(name, [name])

    def assignable(self, src: Json, dst: Json, src_side: Json, dst_side: Json) -> bool:
        """Whether a value typed ``src`` (described in src_side) fits ``dst``."""
        sk, dk = src["k"], dst["k"]
        if sk == "any" or dk == "any":
            return True
        if dk == "name" and dst["n"] == "builtins:object":
            return True
        if sk == "union":
            return all(self.assignable(i, dst, src_side, dst_side) for i in src["items"])
        if dk == "union":
            return any(self.assignable(src, i, src_side, dst_side) for i in dst["items"])
        # A type variable keeps its identity and the domain of values it accepts.
        if sk == "typevar":
            if dk == "typevar":
                return (
                    src["n"] == dst["n"]
                    and src["domain_kind"] == dst["domain_kind"]
                    and self.assignable(src["domain"], dst["domain"], src_side, dst_side)
                )
            return self.assignable(src["domain"], dst, src_side, dst_side)
        if dk == "typevar":
            return False
        if sk == "unresolved" or dk == "unresolved":
            return sk == dk and src["text"] == dst["text"]
        if sk == "none":
            return dk == "none"
        if sk == "literal":
            if dk == "literal":
                return all(v in dst["values"] for v in src["values"])
            return all(
                self._name_fits(cls, dst, src_side) for cls, _ in src["values"]
            )
        if sk == "newtype":
            if dk == "newtype" and dst["n"] == src["n"]:
                return True
            return self.assignable(src["super"], dst, src_side, dst_side)
        if sk == "callable":
            if dk != "callable":
                return dk == "name" and dst["n"] == "collections.abc:Callable"
            if not self.assignable(src["returns"], dst["returns"], src_side, dst_side):
                return False
            if src["params"] is None or dst["params"] is None:
                return True
            if len(src["params"]) != len(dst["params"]):
                return False
            return all(
                self.assignable(d, s, dst_side, src_side)
                for s, d in zip(src["params"], dst["params"], strict=True)
            )
        if sk in ("name", "generic"):
            if dk == "newtype":
                return False
            if not self._name_fits(src["n"], dst, src_side):
                return False
            if sk == "generic" and dk == "generic":
                sa, da = src["args"], dst["args"]
                if not sa or not da:
                    return True
                if len(sa) != len(da):
                    return False
                return all(
                    a["k"] == b["k"] == "ellipsis"
                    or self._arg_fits(a, b, _variance(dst["n"], i), src_side, dst_side)
                    for i, (a, b) in enumerate(zip(sa, da, strict=True))
                )
            return True
        return False

    def _arg_fits(
        self, src: Json, dst: Json, variance: str, src_side: Json, dst_side: Json
    ) -> bool:
        forward = variance == "-" or self.assignable(src, dst, src_side, dst_side)
        backward = variance == "+" or self.assignable(dst, src, dst_side, src_side)
        return forward and backward

    def _name_fits(self, src_name: str, dst: Json, src_side: Json) -> bool:
        if dst["k"] not in ("name", "generic"):
            return False
        target = dst["n"]
        if target in self._supers(src_side, src_name):
            return True
        return target in _NUMERIC_PROMOTION.get(src_name, ())

    def widened_output(self, old_t: Json, new_t: Json) -> bool:
        return not self.assignable(new_t, old_t, self.new, self.old)

    def narrowed_input(self, old_t: Json, new_t: Json) -> bool:
        return not self.assignable(old_t, new_t, self.old, self.new)

    # ---- model direction ---------------------------------------------------------

    def _data_class(self, name: str) -> bool:
        info = self.old["classes"].get(name)
        return bool(info) and info["kind"] in ("attrs", "dataclass", "typeddict", "pydantic")

    def _classify_models(self) -> None:
        pending: list[tuple[Json, str]] = []

        def sig_roots(sig: Json) -> None:
            for p in sig["params"]:
                pending.append((p["type"], INPUT))
            pending.append((sig["returns"], OUTPUT))
            for form in sig.get("overloads", []):
                sig_roots(form)

        for sym in self.old["symbols"].values():
            if sym["kind"] == "function":
                sig_roots(sym["sig"])
        for info in self.old["classes"].values():
            if info["kind"] in ("enum", "typeddict"):
                continue
            data = info["kind"] in ("attrs", "dataclass", "pydantic")
            if not data and "init" in info:
                sig_roots(info["init"])
            for name, member in info["methods"].items():
                if member["kind"] == "method":
                    if data and name == "from_dict":
                        continue
                    sig_roots(member["sig"])
                elif member["kind"] == "property":
                    pending.append((member["type"], OUTPUT))
            if not data:
                for t in info["attributes"].values():
                    pending.append((t, OUTPUT))

        while pending:
            t, direction = pending.pop()
            for name, d in self._walk(t, direction):
                if not self._data_class(name):
                    continue
                seen = self.directions.setdefault(name, set())
                if d in seen:
                    continue
                seen.add(d)
                info = self.old["classes"][name]
                if info["kind"] == "typeddict":
                    pending.extend((k["type"], d) for k in info["keys"].values())
                else:
                    pending.extend((a, d) for a in info["attributes"].values())

    def _walk(self, t: Json, direction: str) -> Iterator[tuple[str, str]]:
        k = t["k"]
        if k in ("name", "generic"):
            yield t["n"], direction
            for a in t.get("args", []):
                yield from self._walk(a, direction)
        elif k == "union":
            for i in t["items"]:
                yield from self._walk(i, direction)
        elif k == "callable":
            flipped = OUTPUT if direction == INPUT else INPUT
            for p in t["params"] or []:
                yield from self._walk(p, flipped)
            yield from self._walk(t["returns"], direction)
        elif k == "typevar":
            yield from self._walk(t["domain"], direction)

    def model_directions(self, name: str) -> set[str]:
        # A model no API accepts or returns (an orphan schema) only has to keep existing.
        return self.directions.get(name, set())

    # ---- symbols -----------------------------------------------------------------

    def _check_symbol(self, key: str, old_sym: Json) -> None:
        new_sym = self.new["symbols"].get(key)
        where = key
        if new_sym is None:
            self._break(where, f"{old_sym['kind']} removed")
            return
        if new_sym["kind"] != old_sym["kind"]:
            self._break(where, f"changed from {old_sym['kind']} to {new_sym['kind']}")
            return
        if old_sym["kind"] == "module":
            if "broken" in new_sym and "broken" not in old_sym:
                self._break(where, f"module no longer imports: {new_sym['broken']}")
            return
        if old_sym["kind"] == "function":
            self._check_signature(where, old_sym["sig"], new_sym["sig"])
        elif old_sym["kind"] == "class" and old_sym["ref"] != new_sym["ref"]:
            self._break(where, f"now refers to {new_sym['ref']} instead of {old_sym['ref']}")
        elif old_sym["kind"] == "alias":
            if self.widened_output(old_sym["type"], new_sym["type"]) or self.narrowed_input(
                old_sym["type"], new_sym["type"]
            ):
                self._break(
                    where,
                    f"type alias changed from {render(old_sym['type'])} "
                    f"to {render(new_sym['type'])}",
                )
        elif old_sym["kind"] == "value" and self.widened_output(
            old_sym["type"], new_sym["type"]
        ):
            self._break(
                where,
                f"type widened from {render(old_sym['type'])} to {render(new_sym['type'])}",
            )

    def _check_signature(
        self, where: str, old: Json, new: Json, *, implemented: bool = False
    ) -> None:
        if old.get("opaque") or new.get("opaque"):
            return
        if "overloads" not in old and "overloads" not in new:
            self._check_form(where, old, new, implemented)
            return
        # Callers type-check against the overloads, not the implementation: every
        # baseline form must still be accepted by some current form.
        new_forms = new.get("overloads") or [new]
        for form in old.get("overloads") or [old]:
            if not any(
                not self._form_breaks(where, form, nf, implemented) for nf in new_forms
            ):
                self._break(where, f"no longer supports the signature {render_sig(form)}")

    def _form_breaks(self, where: str, old: Json, new: Json, implemented: bool) -> bool:
        saved, self.breaks = self.breaks, []
        try:
            self._check_form(where, old, new, implemented)
            return bool(self.breaks)
        finally:
            self.breaks = saved

    def _check_param_type(
        self, where: str, label: str, p: Json, q: Json, implemented: bool
    ) -> None:
        if self.narrowed_input(p["type"], q["type"]):
            self._break(
                where,
                f"parameter '{label}' no longer accepts {render(p['type'])} "
                f"(now {render(q['type'])})",
            )
        if implemented and self.widened_output(p["type"], q["type"]):
            self._break(
                where,
                f"implementations of parameter '{label}' now receive "
                f"{render(q['type'])} (was {render(p['type'])})",
            )

    def _check_form(self, where: str, old: Json, new: Json, implemented: bool) -> None:
        if old["async"] != new["async"]:
            self._break(where, "changed between sync and async")
        new_params = {p["name"]: (i, p) for i, p in enumerate(new["params"])}
        old_names = {p["name"] for p in old["params"]}
        old_var = {
            p["kind"]: p for p in old["params"] if p["kind"] in ("VAR_POSITIONAL", "VAR_KEYWORD")
        }
        for i, p in enumerate(old["params"]):
            name, kind = p["name"], p["kind"]
            if kind in ("VAR_POSITIONAL", "VAR_KEYWORD"):
                star = "*" if kind == "VAR_POSITIONAL" else "**"
                var = next((q for q in new["params"] if q["kind"] == kind), None)
                if var is None:
                    self._break(where, f"no longer accepts {star}{name}")
                else:
                    self._check_param_type(where, f"{star}{name}", p, var, implemented)
                continue
            hit = new_params.get(name)
            if hit is None:
                self._break(where, f"parameter '{name}' removed")
                continue
            j, q = hit
            if q["kind"] in ("VAR_POSITIONAL", "VAR_KEYWORD"):
                self._break(where, f"parameter '{name}' removed")
                continue
            if kind != "POSITIONAL_ONLY" and q["kind"] == "POSITIONAL_ONLY":
                self._break(where, f"parameter '{name}' can no longer be passed by keyword")
            # f("x", label="y") passed "x" through *args; now it binds label as well.
            if (
                kind == "KEYWORD_ONLY"
                and q["kind"] == "POSITIONAL_OR_KEYWORD"
                and "VAR_POSITIONAL" in old_var
            ):
                self._break(
                    where,
                    f"parameter '{name}' now takes positional arguments previously "
                    f"passed through *{old_var['VAR_POSITIONAL']['name']}",
                )
            # Optional parameters can be passed positionally too.
            if kind in ("POSITIONAL_ONLY", "POSITIONAL_OR_KEYWORD"):
                if q["kind"] == "KEYWORD_ONLY":
                    self._break(
                        where, f"parameter '{name}' can no longer be passed positionally"
                    )
                elif j != i:
                    self._break(where, f"parameter '{name}' moved from position {i} to {j}")
            if p["has_default"] and not q["has_default"]:
                self._break(where, f"parameter '{name}' is now required")
            self._check_param_type(where, name, p, q, implemented)
        for q in new["params"]:
            if q["kind"] in ("VAR_POSITIONAL", "VAR_KEYWORD"):
                if implemented and q["kind"] not in old_var:
                    star = "*" if q["kind"] == "VAR_POSITIONAL" else "**"
                    self._break(where, f"implementations must accept new parameter '{star}{q['name']}'")
                continue
            if q["name"] in old_names:
                continue
            if not q["has_default"]:
                self._break(where, f"new required parameter '{q['name']}'")
            elif implemented:
                self._break(where, f"implementations must accept new parameter '{q['name']}'")
            if (
                q["kind"] == "POSITIONAL_OR_KEYWORD"
                and old_var.get("VAR_POSITIONAL") is not None
                and old_var.get("VAR_KEYWORD") is not None
            ):
                self._break(
                    where,
                    f"new parameter '{q['name']}' can bind both positional and keyword "
                    "arguments previously accepted by *args and **kwargs",
                )
            # Arguments the baseline's *args/**kwargs took now bind to this parameter.
            captured = []
            if q["kind"] in ("POSITIONAL_ONLY", "POSITIONAL_OR_KEYWORD"):
                captured.append(("*", old_var.get("VAR_POSITIONAL")))
            if q["kind"] in ("POSITIONAL_OR_KEYWORD", "KEYWORD_ONLY"):
                captured.append(("**", old_var.get("VAR_KEYWORD")))
            for star, var in captured:
                if var is not None and self.narrowed_input(var["type"], q["type"]):
                    self._break(
                        where,
                        f"new parameter '{q['name']}' no longer accepts "
                        f"{render(var['type'])} passed through {star}{var['name']} "
                        f"(now {render(q['type'])})",
                    )
        if self.widened_output(old["returns"], new["returns"]):
            self._break(
                where,
                f"return type widened from {render(old['returns'])} "
                f"to {render(new['returns'])}",
            )
        if implemented and self.narrowed_input(old["returns"], new["returns"]):
            self._break(
                where,
                f"implementations' return type narrowed from {render(old['returns'])} "
                f"to {render(new['returns'])}",
            )

    # ---- classes -----------------------------------------------------------------

    def _check_class(self, key: str) -> None:
        old = self.old["classes"][key]
        new = self.new["classes"][key]
        dirs = self.model_directions(key) if self._data_class(key) else {INPUT, OUTPUT}
        if not dirs:
            return
        where = key
        if old["kind"] != new["kind"] and "protocol" in (old["kind"], new["kind"]):
            self._break(where, f"changed from {old['kind']} to {new['kind']}")
            return
        for base in old["bases"]:
            if base not in new["bases"]:
                self._break(where, f"no longer derives from {base}")

        if old["kind"] == "enum":
            new_members = new.get("members", {})
            for name, value in old["members"].items():
                if name not in new_members:
                    self._break(f"{where}.{name}", "enum member removed")
                elif new_members[name] != value:
                    self._break(
                        f"{where}.{name}",
                        f"enum value changed from {value} to {new_members[name]}",
                    )
            return

        if old["kind"] == "typeddict":
            self._check_typeddict(where, old, new)
            return

        protocol = old["kind"] == "protocol"

        if "init" in old and "init" in new and INPUT in dirs and not protocol:
            self._check_signature(f"{where}()", old["init"], new["init"])

        reads = OUTPUT in dirs or protocol
        for name, old_t in old["attributes"].items():
            new_t = new["attributes"].get(name)
            if new_t is None:
                replacement = new["methods"].get(name)
                if replacement is None:
                    self._break(f"{where}.{name}", "attribute removed")
                elif replacement["kind"] == "method":
                    self._break(f"{where}.{name}", "changed from attribute to method")
                elif replacement["kind"] in ("property", "value"):
                    new_t = replacement["type"]
                if new_t is None:
                    continue
            if not reads:
                continue
            if self.widened_output(old_t, new_t):
                self._break(
                    f"{where}.{name}",
                    f"type widened from {render(old_t)} to {render(new_t)}",
                )
            if protocol and self.narrowed_input(old_t, new_t):
                self._break(
                    f"{where}.{name}",
                    f"implementations' type narrowed from {render(old_t)} "
                    f"to {render(new_t)}",
                )

        for name, old_m in old["methods"].items():
            new_m = new["methods"].get(name)
            member = f"{where}.{name}"
            if new_m is None:
                new_t = new["attributes"].get(name)
                if new_t is None:
                    self._break(member, f"{old_m['kind']} removed")
                elif old_m["kind"] == "method":
                    self._break(member, "changed from method to attribute")
                elif old_m["kind"] in ("property", "value") and self.widened_output(
                    old_m["type"], new_t
                ):
                    self._break(
                        member,
                        f"type widened from {render(old_m['type'])} to {render(new_t)}",
                    )
                continue
            if new_m["kind"] != old_m["kind"]:
                self._break(member, f"changed from {old_m['kind']} to {new_m['kind']}")
            elif old_m["kind"] == "method":
                # Instance calls work for every binding; class-level calls need class/static.
                if old_m["binding"] != new_m["binding"] and (
                    protocol or new_m["binding"] == "instance"
                ):
                    self._break(
                        member,
                        f"changed from {old_m['binding']} method to "
                        f"{new_m['binding']} method",
                    )
                self._check_signature(member, old_m["sig"], new_m["sig"], implemented=protocol)
            elif old_m["kind"] == "property" and self.widened_output(
                old_m["type"], new_m["type"]
            ):
                self._break(
                    member,
                    f"type widened from {render(old_m['type'])} to {render(new_m['type'])}",
                )
            elif old_m["kind"] == "value" and self.widened_output(
                old_m["type"], new_m["type"]
            ):
                self._break(
                    member,
                    f"type widened from {render(old_m['type'])} to {render(new_m['type'])}",
                )
        if protocol:
            for name in new["methods"].keys() | new["attributes"].keys():
                if name not in old["methods"] and name not in old["attributes"]:
                    self._break(f"{where}.{name}", "new member required of implementations")

    def _check_typeddict(self, where: str, old: Json, new: Json) -> None:
        dirs = self.model_directions(where)
        old_keys, new_keys = old["keys"], new["keys"]
        for name, ok in old_keys.items():
            nk = new_keys.get(name)
            if nk is None:
                self._break(f"{where}[{name!r}]", "key removed")
                continue
            if OUTPUT in dirs:
                if ok["required"] and not nk["required"]:
                    self._break(f"{where}[{name!r}]", "key is no longer always present")
                if self.widened_output(ok["type"], nk["type"]):
                    self._break(
                        f"{where}[{name!r}]",
                        f"type widened from {render(ok['type'])} to {render(nk['type'])}",
                    )
            if INPUT in dirs:
                if not ok["required"] and nk["required"]:
                    self._break(f"{where}[{name!r}]", "key is now required")
                if self.narrowed_input(ok["type"], nk["type"]):
                    self._break(
                        f"{where}[{name!r}]",
                        f"no longer accepts {render(ok['type'])} (now {render(nk['type'])})",
                    )
        if INPUT in dirs:
            for name, nk in new_keys.items():
                if name not in old_keys and nk["required"]:
                    self._break(f"{where}[{name!r}]", "new required key")


def find_breaks(old: Json, new: Json) -> list[str]:
    return Checker(old, new).run()


# --------------------------------------------------------------------------------------
# CLI
# --------------------------------------------------------------------------------------


def _summary(lines: list[str]) -> None:
    path = os.environ.get("GITHUB_STEP_SUMMARY")
    if path:
        with open(path, "a", encoding="utf-8") as fh:
            fh.write("\n".join(lines) + "\n")


def _run(args: argparse.Namespace) -> int:
    if args.describe:
        sys.path.insert(0, args.describe)
        # Deprecated aliases warn on access; describing them is not using them.
        warnings.simplefilter("ignore")
        json.dump(Describer(args.package).describe(Path(args.describe)), sys.stdout)
        return 0

    metadata: Json | None = None
    if args.print_baseline_major is not None:
        metadata = fetch_pypi_metadata()
        print(latest_release(metadata, args.print_baseline_major) or "")
        return 0

    current_root = Path(args.current).resolve()
    with tempfile.TemporaryDirectory(prefix="api-compat-") as tmp:
        if args.baseline_dir:
            baseline_root = Path(args.baseline_dir).resolve()
            label = str(baseline_root)
        else:
            metadata = fetch_pypi_metadata()
            if args.baseline_version:
                version = args.baseline_version
            else:
                version = latest_release(metadata, args.baseline_major)
                if version is None:
                    print(
                        f"::notice::No {args.baseline_major}.x release of {DISTRIBUTION} "
                        "is published yet; nothing to compare against."
                    )
                    return 0
            baseline_root = download_baseline(metadata, version, Path(tmp))
            label = f"{DISTRIBUTION} {version}"
        print(f"Baseline: {label}")
        print(f"Current:  {current_root}")
        old = describe_in_subprocess(baseline_root, args.package)
        new = describe_in_subprocess(current_root, args.package)

    breaks = find_breaks(old, new)
    if not breaks:
        print(f"Compatible: no breaking changes to the public API since {label}.")
        _summary([f"### API compatibility\n\nNo breaking changes since `{label}`."])
        return 0
    print(f"{len(breaks)} breaking change(s) to the public API since {label}:")
    for b in breaks:
        print(f"  - {b}")
    _summary(
        [f"### API compatibility\n\n{len(breaks)} breaking change(s) since `{label}`:\n"]
        + [f"- `{b}`" for b in breaks]
    )
    return 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    which = parser.add_mutually_exclusive_group(required=True)
    which.add_argument("--baseline-major", type=int, help="compare with the newest N.x.y")
    which.add_argument("--baseline-version", help="compare with this published version")
    which.add_argument("--baseline-dir", help="compare with a package root on disk")
    which.add_argument(
        "--print-baseline-major",
        type=int,
        metavar="N",
        help="print the newest published N.x.y (empty if none) and exit",
    )
    which.add_argument("--describe", help=argparse.SUPPRESS)
    parser.add_argument(
        "--current",
        default=str(REPO_ROOT / "generated"),
        help="package root of the build to check (default: generated/)",
    )
    parser.add_argument("--package", default=PACKAGE, help=argparse.SUPPRESS)
    args = parser.parse_args(argv)
    try:
        return _run(args)
    except SetupError as exc:
        print(f"::error::api-compat: {exc}", file=sys.stderr)
        return 2
    except Exception as exc:  # any other failure is a tool error, never a verdict
        traceback.print_exc()
        print(f"::error::api-compat failed: {exc!r}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
