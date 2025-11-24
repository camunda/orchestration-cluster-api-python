#!/usr/bin/env python3
import argparse
import importlib.util
import os
import shutil
import subprocess
import sys
from pathlib import Path


REPO_URL = "https://github.com/camunda/camunda.git"
SPEC_DIR = "zeebe/gateway-protocol/src/main/proto/v2"
SPEC_FILE = "rest-api.yaml"


def log(msg: str) -> None:
    print(msg)


def which(cmd: str) -> bool:
    return shutil.which(cmd) is not None


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


def run_openapi_generator(spec: Path, out_dir: Path, config_path: Path, generator: str) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    cmd = None
    # This is for testing patches to the upstream generator using a local build
    if os.environ.get("CAMUNDA_OPENAPI_GEN_LOCAL") == "1":
        cmd = [
            "java", "-jar", "/Users/jwulf/workspace/openapi-generator/modules/openapi-generator-cli/target/openapi-generator-cli.jar", "generate",
            "-g", generator,
            "-i", str(spec),
            "-o", str(out_dir),
            "-c", str(config_path),
            "--skip-validate-spec"
        ]
    elif which("npx"):
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


