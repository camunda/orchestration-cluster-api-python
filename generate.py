#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import os
import subprocess
import sys
from collections.abc import Callable
from pathlib import Path
from typing import Any

REPO_URL = "https://github.com/camunda/camunda.git"
SPEC_DIR = "zeebe/gateway-protocol/src/main/proto/v2"
SPEC_FILE = "rest-api.yaml"

def log(msg: str) -> None:
    print(msg)

def ensure_cache_dir(cache_dir: Path) -> None:
    cache_dir.mkdir(parents=True, exist_ok=True)

def fetch_spec(cache_dir: Path, ref: str) -> Path:
    """Clone repo sparsely and return path to the spec."""
    ensure_cache_dir(cache_dir)
    repo_dir = cache_dir / "camunda"
    spec_path = repo_dir / SPEC_DIR / SPEC_FILE

    try:
        if not repo_dir.exists():
            log("Initializing sparse clone...")
            repo_dir.mkdir(parents=True, exist_ok=True)
            subprocess.run(["git", "init"], cwd=str(repo_dir), check=True)
            subprocess.run(["git", "remote", "add", "origin", REPO_URL], cwd=str(repo_dir), check=True)
            subprocess.run(["git", "config", "core.sparseCheckout", "true"], cwd=str(repo_dir), check=True)
            
            sparse_checkout_file = repo_dir / ".git" / "info" / "sparse-checkout"
            sparse_checkout_file.parent.mkdir(parents=True, exist_ok=True)
            with open(sparse_checkout_file, "w") as f:
                f.write(f"{SPEC_DIR}\n")

        log("Updating repository...")
        # Fetch specific ref
        subprocess.run(["git", "fetch", "--depth", "1", "origin", ref], cwd=str(repo_dir), check=True)
        # Checkout FETCH_HEAD
        subprocess.run(["git", "checkout", "-f", "FETCH_HEAD"], cwd=str(repo_dir), check=True)

    except Exception as e:
        log(f"Warning: failed to update/clone remote repo: {e}")

    if spec_path.exists():
        log(f"Using spec from cache: {spec_path}")
        return spec_path

    raise FileNotFoundError(f"OpenAPI spec not found at {spec_path}")

def load_hooks(hooks_dir: Path) -> list[Callable[[dict[str, str]], None]]:
    hooks: list[Callable[[dict[str, str]], None]] = []
    if not hooks_dir.exists():
        return hooks
    for hook_file in sorted(hooks_dir.glob("*.py")):
        spec = importlib.util.spec_from_file_location(hook_file.stem, hook_file)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, "run") and callable(getattr(module, "run")):
                hooks.append(module.run)
    return hooks

def run_hooks(hooks: list[Callable[[dict[str, str]], None]], context: dict[str, str]) -> None:
    for hook in hooks:
        log(f"Running hook: {hook.__module__}")
        hook(context)

def run_acceptance_tests(root: Path, out_dir: Path) -> None:
    log("Running acceptance tests...")
    env = os.environ.copy()
    existing = env.get("PYTHONPATH", "")
    # Ensure generated code is importable by tests
    env["PYTHONPATH"] = f"{str(out_dir)}{os.pathsep}{existing}" if existing else str(out_dir)
    tests_dir = root / "tests" / "acceptance"
    cmd = [sys.executable, "-m", "pytest", "-q", str(tests_dir)]
    subprocess.run(cmd, check=True, env=env, cwd=str(root))

def main():
    parser = argparse.ArgumentParser(description="Generate Python SDK for Camunda Orchestration Cluster API")
    parser.add_argument("--out-dir", default="generated", help="Output directory for generated SDK")
    parser.add_argument("--cache-dir", default=".openapi-cache", help="Cache directory for spec repo")
    parser.add_argument("--spec-ref", default="main", help="Git ref/branch/tag for the spec repo")
    parser.add_argument("--generator", default="openapi-python-client", help="OpenAPI generator name")
    parser.add_argument("--config", default="generator-config.yaml", help="Path to generator config")
    parser.add_argument("--skip-generate", action="store_true", help="Skip generation (run hooks only)")
    parser.add_argument("--package-name", default=None, help="Override packageName in config (in-memory)")
    parser.add_argument("--skip-tests", action="store_true", help="Skip acceptance tests")
    parser.add_argument("--local-spec", help="Path to local OpenAPI spec file (skips git fetch)")
    parser.add_argument("--bundled-spec", help="Path to a pre-bundled spec (from camunda-schema-bundler). Skips fetch and bundling.")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    out_dir = (root / args.out_dir).resolve()
    cache_dir = (root / args.cache_dir).resolve()
    config_path = (root / args.config).resolve()

    bundled_spec_input: Path | None = None
    if args.bundled_spec:
        bundled_spec_input = Path(args.bundled_spec).resolve()
        if not bundled_spec_input.exists():
            raise FileNotFoundError(f"Bundled spec not found: {bundled_spec_input}")
        log(f"Using pre-bundled spec: {bundled_spec_input}")
        spec_path = bundled_spec_input
    elif args.local_spec:
        spec_path = Path(args.local_spec).resolve()
        if not spec_path.exists():
            raise FileNotFoundError(f"Local spec file not found: {spec_path}")
        log(f"Using local spec: {spec_path}")
    else:
        spec_path = fetch_spec(cache_dir, args.spec_ref)

    # If package name override is provided, create a temp config copy
    effective_config = config_path
    tmp_config = None
    if args.package_name is not None:
        import yaml  # lazy import
        with open(config_path, "r", encoding="utf-8") as f:
            cfg: dict[str, Any] = yaml.safe_load(f) or {}
        cfg["packageName"] = args.package_name
        tmp_config = root / ".openapi-cache" / "generator-config.effective.yaml"
        tmp_config.parent.mkdir(parents=True, exist_ok=True)
        with open(tmp_config, "w", encoding="utf-8") as f:
            yaml.safe_dump(cfg, f, sort_keys=False)
        effective_config = tmp_config

    if not args.skip_generate:
        hooks_root = root / "hooks"
        pre_gen_hooks_dir = hooks_root / "pre_gen"
        post_gen_hooks_dir = hooks_root / "post_gen"

        import yaml

        out_dir.mkdir(parents=True, exist_ok=True)
        bundled_spec_path = out_dir / "bundled_spec.yaml"

        if args.bundled_spec:
            # Use pre-bundled spec from camunda-schema-bundler
            import shutil as _shutil
            assert bundled_spec_input is not None
            _shutil.copy2(bundled_spec_input, bundled_spec_path)
            log(f"Using pre-bundled spec: {bundled_spec_input}")
        else:
            # Bundle from raw spec
            from bundle import bundle_spec
            log(f"Bundling spec from {spec_path} to {bundled_spec_path}...")
            bundle_spec(spec_path, bundled_spec_path)

        # Build context shared by all hooks
        metadata_path = root / "external-spec" / "bundled" / "spec-metadata.json"
        context = {
            "out_dir": str(out_dir),
            "spec_path": str(spec_path),
            "bundled_spec_path": str(bundled_spec_path),
            "metadata_path": str(metadata_path) if metadata_path.exists() else "",
            "config_path": str(effective_config),
            "generator": args.generator,
        }

        # 1. Pre-gen hooks (spec transforms)
        pre_hooks = load_hooks(pre_gen_hooks_dir)
        run_hooks(pre_hooks, context)

        # 2. Generate
        with open(effective_config, "r", encoding="utf-8") as f:
            config = yaml.safe_load(f)
        package_name = config.get("package_name_override", "client")
        actual_out_dir = out_dir / package_name

        cmd = [
            "openapi-python-client", "generate",
            "--path", str(bundled_spec_path),
            "--config", str(effective_config),
            "--output-path", str(actual_out_dir),
            "--overwrite",
            "--meta", "none"
        ]
        log(f"Running openapi-python-client with config {effective_config}...")
        subprocess.run(cmd, check=True)

        # 3. Post-gen hooks (code transforms)
        post_hooks = load_hooks(post_gen_hooks_dir)
        run_hooks(post_hooks, context)

    # Run acceptance tests as final stage
    if not args.skip_tests:
        run_acceptance_tests(root, out_dir)

    log("Done.")

if __name__ == "__main__":
    main()


