#!/usr/bin/env python3
import argparse
import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path


REPO_URL = "https://github.com/camunda/camunda-orchestration-cluster-api.git"
SPEC_PATH_IN_REPO = "specification/rest-api.yaml"


def log(msg: str) -> None:
    print(msg)


def which(cmd: str) -> bool:
    return shutil.which(cmd) is not None


def ensure_cache_dir(cache_dir: Path) -> None:
    cache_dir.mkdir(parents=True, exist_ok=True)


def fetch_spec(cache_dir: Path, ref: str) -> Path:
    """Clone repo shallowly and return path to the spec; fallback to local copy."""
    ensure_cache_dir(cache_dir)
    repo_dir = cache_dir / "camunda-orchestration-cluster-api"
    spec_path = repo_dir / SPEC_PATH_IN_REPO

    try:
        if repo_dir.exists():
            # Update existing shallow clone
            log("Updating existing cached repository...")
            subprocess.run([
                "git", "-C", str(repo_dir), "fetch", "--depth", "1", "origin", ref
            ], check=True)
            subprocess.run([
                "git", "-C", str(repo_dir), "checkout", "-f", ref
            ], check=True)
            subprocess.run([
                "git", "-C", str(repo_dir), "reset", "--hard", f"origin/{ref}"
            ], check=True)
        else:
            log("Cloning repository (shallow)...")
            subprocess.run([
                "git", "clone", "--depth", "1", "--branch", ref, REPO_URL, str(repo_dir)
            ], check=True)
    except Exception as e:
        log(f"Warning: failed to update/clone remote repo: {e}")

    if spec_path.exists():
        log(f"Using spec from cache: {spec_path}")
        return spec_path

    # Fallback to local working copy
    local_repo = Path(__file__).resolve().parent.parent / "camunda-orchestration-cluster-api"
    local_spec = local_repo / SPEC_PATH_IN_REPO
    if local_spec.exists():
        log(f"Using local fallback spec: {local_spec}")
        return local_spec

    # As the last resort, allow a workspace-level file
    workspace_spec = Path(__file__).resolve().parent.parent / SPEC_PATH_IN_REPO
    if workspace_spec.exists():
        log(f"Using workspace fallback spec: {workspace_spec}")
        return workspace_spec

    raise FileNotFoundError("OpenAPI spec not found via network or local fallbacks")


def run_openapi_generator(spec: Path, out_dir: Path, config_path: Path, generator: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd = None
    if which("npx"):
        cmd = [
            "npx", "--yes", "@openapitools/openapi-generator-cli", "generate",
            "-g", generator,
            "-i", str(spec),
            "-o", str(out_dir),
            "-c", str(config_path),
            "--skip-validate-spec"
        ]
    elif which("docker"):
        cmd = [
            "docker", "run", "--rm",
            "-v", f"{spec.parent}:/spec",
            "-v", f"{out_dir}:/out",
            "-v", f"{config_path.parent}:/cfg",
            "openapitools/openapi-generator-cli", "generate",
            "-g", generator,
            "-i", f"/spec/{spec.name}",
            "-o", "/out",
            "-c", f"/cfg/{config_path.name}",
            "--skip-validate-spec"
        ]
    else:
        raise RuntimeError("Neither npx nor docker is available to run openapi-generator")

    log("Running OpenAPI Generator...")
    subprocess.run(cmd, check=True)


def load_hooks(hooks_dir: Path):
    hooks = []
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


def run_hooks(hooks, context: dict) -> None:
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
    parser.add_argument("--generator", default="python", help="OpenAPI generator name (default: python)")
    parser.add_argument("--config", default="generator-config.yaml", help="Path to generator config")
    parser.add_argument("--skip-generate", action="store_true", help="Skip generation (run hooks only)")
    parser.add_argument("--package-name", default=None, help="Override packageName in config (in-memory)")
    parser.add_argument("--skip-tests", action="store_true", help="Skip acceptance tests")
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    out_dir = (root / args.out_dir).resolve()
    cache_dir = (root / args.cache_dir).resolve()
    config_path = (root / args.config).resolve()
    hooks_dir = root / "hooks"

    spec_path = fetch_spec(cache_dir, args.spec_ref)

    # If package name override is provided, create a temp config copy
    effective_config = config_path
    tmp_config = None
    if args.package_name is not None:
        import yaml  # lazy import
        with open(config_path, "r", encoding="utf-8") as f:
            cfg = yaml.safe_load(f) or {}
        cfg["packageName"] = args.package_name
        tmp_config = root / ".openapi-cache" / "generator-config.effective.yaml"
        tmp_config.parent.mkdir(parents=True, exist_ok=True)
        with open(tmp_config, "w", encoding="utf-8") as f:
            yaml.safe_dump(cfg, f, sort_keys=False)
        effective_config = tmp_config

    if not args.skip_generate:
        run_openapi_generator(spec_path, out_dir, effective_config, args.generator)

    hooks = load_hooks(hooks_dir)
    context = {
        "out_dir": str(out_dir),
        "spec_path": str(spec_path),
        "config_path": str(effective_config),
        "generator": args.generator,
    }
    run_hooks(hooks, context)

    # Run acceptance tests as final stage
    if not args.skip_tests:
        run_acceptance_tests(root, out_dir)

    log("Done.")


if __name__ == "__main__":
    main()


