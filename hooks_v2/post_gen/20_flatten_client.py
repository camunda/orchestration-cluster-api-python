import ast
import os
from pathlib import Path
import re

def to_camel_case(snake_str: str) -> str:
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def get_imports_and_signature(file_path: Path, package_root: str):
    with open(file_path, "r") as f:
        code = f.read()
    
    tree = ast.parse(code)
    
    imports: list[ast.stmt] = []
    sync_func = None
    async_func = None
    
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            imports.append(node)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            if node.name == "sync":
                sync_func = node
            elif node.name == "asyncio":
                async_func = node
                
    rel_path = file_path.relative_to(package_root)
    # depth = number of parts in parent directory
    # e.g. api/group/module.py -> api/group -> depth=2
    depth = len(rel_path.parent.parts)
    
    adjusted_imports: list[ast.stmt] = []
    for node in imports:
        if isinstance(node, ast.ImportFrom):
            if node.level > 0:
                steps_up = node.level - 1
                current_parts = list(rel_path.parent.parts)
                
                if steps_up > len(current_parts):
                    continue
                
                target_parts = current_parts[:len(current_parts) - steps_up]
                base_module = ".".join(target_parts)
                
                if node.module:
                    if base_module:
                        final_module = f"{base_module}.{node.module}"
                    else:
                        final_module = node.module
                else:
                    final_module = base_module
                
                if final_module == "client" or (final_module and final_module.startswith("client.")):
                    continue
                
                new_node = ast.ImportFrom(
                    module=final_module,
                    names=node.names,
                    level=1
                )
                adjusted_imports.append(new_node)
            else:
                adjusted_imports.append(node)
        else:
            adjusted_imports.append(node)
            
    return adjusted_imports, sync_func, async_func

def generate_flat_client(package_path: str):
    api_dir = package_path / "api"
    if not api_dir.exists():
        print(f"API directory not found at {api_dir}")
        return

    sync_methods: list[str] = []
    async_methods: list[str] = []
    all_imports: set[ast.stmt] = set()

    for root, dirs, files in os.walk(api_dir):
        for file in files:
            if file == "__init__.py" or not file.endswith(".py"):
                continue

            file_path = Path(root) / file
            imports, sync_func, async_func = get_imports_and_signature(file_path, package_path)
            
            for imp in imports:
                if isinstance(imp, ast.ImportFrom):
                    module = imp.module
                    names = ", ".join(n.name + (f" as {n.asname}" if n.asname else "") for n in imp.names)
                    level = "." * imp.level
                    import_stmt = f"from {level}{module} import {names}" if module else f"from {level} import {names}"
                    all_imports.add(import_stmt)
                else:
                    names = ", ".join(n.name + (f" as {n.asname}" if n.asname else "") for n in imp.names)
                    import_stmt = f"import {names}"
                    all_imports.add(import_stmt)

            rel_path = Path(root).relative_to(package_path)
            module_name = file[:-3]
            import_path = f".{'.'.join(rel_path.parts)}.{module_name}"
            method_name = module_name
            
            if sync_func:
                args = sync_func.args
                new_args = []
                for arg in args.posonlyargs:
                    if arg.arg != 'client':
                        new_args.append(arg)
                for arg in args.args:
                    if arg.arg != 'client':
                        new_args.append(arg)
                
                new_kwonlyargs = []
                new_kw_defaults = []
                for arg, default in zip(args.kwonlyargs, args.kw_defaults):
                    if arg.arg != 'client':
                        new_kwonlyargs.append(arg)
                        new_kw_defaults.append(default)
                
                arg_strs = ["self"]
                for arg in new_args:
                    arg_name = "data" if arg.arg == "body" else arg.arg
                    ann = f": {ast.unparse(arg.annotation)}" if arg.annotation else ""
                    arg_strs.append(f"{arg_name}{ann}")
                    
                if args.vararg:
                    ann = f": {ast.unparse(args.vararg.annotation)}" if args.vararg.annotation else ""
                    arg_strs.append(f"*{args.vararg.arg}{ann}")
                elif new_kwonlyargs:
                    arg_strs.append("*")
                    
                for arg, default in zip(new_kwonlyargs, new_kw_defaults):
                    arg_name = "data" if arg.arg == "body" else arg.arg
                    ann = f": {ast.unparse(arg.annotation)}" if arg.annotation else ""
                    default_str = f" = {ast.unparse(default)}" if default else ""
                    arg_strs.append(f"{arg_name}{ann}{default_str}")
                    
                if args.kwarg:
                    ann = f": {ast.unparse(args.kwarg.annotation)}" if args.kwarg.annotation else ": Any"
                    arg_strs.append(f"**{args.kwarg.arg}{ann}")
                else:
                    arg_strs.append("**kwargs: Any")
                
                sig_str = ", ".join(arg_strs)
                return_ann = f" -> {ast.unparse(sync_func.returns)}" if sync_func.returns else ""
                docstring = ast.get_docstring(sync_func)
                docstring_str = f'        """{docstring}"""\n' if docstring else ""
                
                sync_methods.append(f"""
    def {method_name}({sig_str}){return_ann}:
{docstring_str}        from {import_path} import sync as {method_name}_sync
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return {method_name}_sync(**_kwargs)
""")

            if async_func:
                args = async_func.args
                new_args = []
                for arg in args.posonlyargs:
                    if arg.arg != 'client':
                        new_args.append(arg)
                for arg in args.args:
                    if arg.arg != 'client':
                        new_args.append(arg)
                
                new_kwonlyargs = []
                new_kw_defaults = []
                for arg, default in zip(args.kwonlyargs, args.kw_defaults):
                    if arg.arg != 'client':
                        new_kwonlyargs.append(arg)
                        new_kw_defaults.append(default)
                
                arg_strs = ["self"]
                for arg in new_args:
                    arg_name = "data" if arg.arg == "body" else arg.arg
                    ann = f": {ast.unparse(arg.annotation)}" if arg.annotation else ""
                    arg_strs.append(f"{arg_name}{ann}")
                    
                if args.vararg:
                    ann = f": {ast.unparse(args.vararg.annotation)}" if args.vararg.annotation else ""
                    arg_strs.append(f"*{args.vararg.arg}{ann}")
                elif new_kwonlyargs:
                    arg_strs.append("*")
                    
                for arg, default in zip(new_kwonlyargs, new_kw_defaults):
                    arg_name = "data" if arg.arg == "body" else arg.arg
                    ann = f": {ast.unparse(arg.annotation)}" if arg.annotation else ""
                    default_str = f" = {ast.unparse(default)}" if default else ""
                    arg_strs.append(f"{arg_name}{ann}{default_str}")
                    
                if args.kwarg:
                    ann = f": {ast.unparse(args.kwarg.annotation)}" if args.kwarg.annotation else ": Any"
                    arg_strs.append(f"**{args.kwarg.arg}{ann}")
                else:
                    arg_strs.append("**kwargs: Any")

                sig_str = ", ".join(arg_strs)
                return_ann = f" -> {ast.unparse(async_func.returns)}" if async_func.returns else ""
                docstring = ast.get_docstring(async_func)
                docstring_str = f'        """{docstring}"""\n' if docstring else ""
                
                async_methods.append(f"""
    async def {method_name}({sig_str}){return_ann}:
{docstring_str}        from {import_path} import asyncio as {method_name}_asyncio
        _kwargs = locals()
        _kwargs.pop("self")
        _kwargs["client"] = self.client
        if "data" in _kwargs:
            _kwargs["body"] = _kwargs.pop("data")
        return await {method_name}_asyncio(**_kwargs)
""")

    client_file = package_path / "client.py"
    if not client_file.exists():
        print(f"Client file not found at {client_file}. Skipping flattening.")
        return

    with open(client_file, "r") as f:
        content = f.read()

    # Split content
    lines = content.splitlines()
    import_lines = []
    class_lines = []
    in_classes = False
    
    for line in lines:
        if line.startswith("class ") or line.startswith("@define"):
            in_classes = True
        
        if in_classes:
            class_lines.append(line)
        else:
            import_lines.append(line)

    # Remove existing CamundaClient
    class_content = "\n".join(class_lines)
    if "class CamundaClient" in class_content:
        class_content = class_content.split("class CamundaClient")[0]

    # Prepare imports
    imports_content = "\n".join(import_lines)
    if "from __future__ import annotations" not in imports_content:
        imports_content = "from __future__ import annotations\n" + imports_content
    
    if "from .types import UNSET, Unset" not in imports_content:
        imports_content += "\nfrom .types import UNSET, Unset"

    if "from typing import TYPE_CHECKING" not in imports_content:
        imports_content += "\nfrom typing import TYPE_CHECKING"

    imports_content += "\nimport asyncio"
    imports_content += "\nfrom typing import Callable"
    imports_content += "\nfrom .runtime.job_worker import JobWorker, WorkerConfig, JobHandler"
    imports_content += "\nfrom pathlib import Path"
    imports_content += "\nfrom .models.create_deployment_response_200 import CreateDeploymentResponse200"
    imports_content += "\nfrom .models.create_deployment_response_200_deployments_item_process_definition import CreateDeploymentResponse200DeploymentsItemProcessDefinition"
    imports_content += "\nfrom .models.create_deployment_response_200_deployments_item_decision_definition import CreateDeploymentResponse200DeploymentsItemDecisionDefinition"
    imports_content += "\nfrom .models.create_deployment_response_200_deployments_item_decision_requirements import CreateDeploymentResponse200DeploymentsItemDecisionRequirements"
    imports_content += "\nfrom .models.create_deployment_response_200_deployments_item_form import CreateDeploymentResponse200DeploymentsItemForm"

    # Prepare TYPE_CHECKING block
    type_checking_block = "\nif TYPE_CHECKING:\n"
    sorted_imports = sorted(list(all_imports))
    for imp in sorted_imports:
        type_checking_block += f"    {imp}\n"

    new_sync_methods = "\n".join(sync_methods)
    new_async_methods = "\n".join(async_methods)

    extended_result_code = """
class ExtendedDeploymentResult(CreateDeploymentResponse200):
    processes: list[CreateDeploymentResponse200DeploymentsItemProcessDefinition]
    decisions: list[CreateDeploymentResponse200DeploymentsItemDecisionDefinition]
    decision_requirements: list[CreateDeploymentResponse200DeploymentsItemDecisionRequirements]
    forms: list[CreateDeploymentResponse200DeploymentsItemForm]
    
    def __init__(self, response: CreateDeploymentResponse200):
        self.deployment_key = response.deployment_key
        self.tenant_id = response.tenant_id
        self.deployments = response.deployments
        self.additional_properties = response.additional_properties
        
        self.processes = [d.process_definition for d in self.deployments if not isinstance(d.process_definition, Unset)]
        self.decisions = [d.decision_definition for d in self.deployments if not isinstance(d.decision_definition, Unset)]
        self.decision_requirements = [d.decision_requirements for d in self.deployments if not isinstance(d.decision_requirements, Unset)]
        self.forms = [d.form for d in self.deployments if not isinstance(d.form, Unset)]
"""

    camunda_client_code = f'''
class CamundaClient:
    client: Client | AuthenticatedClient

    def __init__(self, base_url: str = "http://localhost:8080/v2", token: str | None = None, **kwargs):
        if token:
            self.client = AuthenticatedClient(base_url=base_url, token=token, **kwargs)
        else:
            self.client = Client(base_url=base_url, **kwargs)

    def __enter__(self):
        self.client.__enter__()
        return self

    def __exit__(self, *args, **kwargs):
        return self.client.__exit__(*args, **kwargs)

    def deploy_resources_from_files(self, files: list[str | Path], tenant_id: str | None = None) -> ExtendedDeploymentResult:
        """Deploy BPMN/DMN/Form resources from local files.

        This is a convenience wrapper around :meth:`create_deployment` that:

        - Reads each path in ``files`` as bytes.
        - Wraps the bytes in :class:`camunda_orchestration_sdk.types.File` using the file's basename
          as ``file_name``.
        - Builds :class:`camunda_orchestration_sdk.models.CreateDeploymentData` and calls
          :meth:`create_deployment`.
        - Returns an :class:`ExtendedDeploymentResult`, which is the deployment response plus
          convenience lists (``processes``, ``decisions``, ``decision_requirements``, ``forms``).

        Args:
            files: File paths (``str`` or ``Path``) to deploy.
            tenant_id: Optional tenant identifier. If not provided, the default tenant is used.

        Returns:
            ExtendedDeploymentResult: The deployment result with extracted resource lists.

        Raises:
            FileNotFoundError: If any file path does not exist.
            PermissionError: If any file path cannot be read.
            IsADirectoryError: If any file path is a directory.
            OSError: For other I/O failures while reading files.
            Exception: Propagates any exception raised by :meth:`create_deployment` (including
                typed API errors in :mod:`camunda_orchestration_sdk.errors` and ``httpx.TimeoutException``).
        """
        from .models.create_deployment_data import CreateDeploymentData
        from .types import File, UNSET
        import os

        resources = []
        for file_path in files:
            file_path = str(file_path)
            with open(file_path, "rb") as f:
                content = f.read()
            resources.append(File(payload=content, file_name=os.path.basename(file_path)))

        data = CreateDeploymentData(resources=resources, tenant_id=tenant_id if tenant_id is not None else UNSET)
        return ExtendedDeploymentResult(self.create_deployment(data=data))

{new_sync_methods}


class CamundaAsyncClient:
    client: Client | AuthenticatedClient
    _workers: list[JobWorker]

    def __init__(self, base_url: str = "http://localhost:8080/v2", token: str | None = None, **kwargs):
        if token:
            self.client = AuthenticatedClient(base_url=base_url, token=token, **kwargs)
        else:
            self.client = Client(base_url=base_url, **kwargs)
        self._workers = []

    async def __aenter__(self):
        await self.client.__aenter__()
        return self

    async def __aexit__(self, *args, **kwargs):
        await self.client.__aexit__(*args, **kwargs)

    def create_job_worker(self, config: WorkerConfig, callback: JobHandler, auto_start: bool = True) -> JobWorker:
        worker = JobWorker(self, callback, config)
        self._workers.append(worker)
        if auto_start:
            worker.start()
        return worker

    async def run_workers(self):
        stop_event = asyncio.Event()
        try:
            await stop_event.wait()
        except asyncio.CancelledError:
            pass
        finally:
            for worker in self._workers:
                worker.stop()

    async def deploy_resources_from_files(self, files: list[str | Path], tenant_id: str | None = None) -> ExtendedDeploymentResult:
        """Deploy BPMN/DMN/Form resources from local files.

        Async variant of :meth:`CamundaClient.deploy_resources_from_files`.

        This reads each file path in ``files`` as bytes, wraps them into
        :class:`camunda_orchestration_sdk.types.File`, calls :meth:`create_deployment`, and returns
        an :class:`ExtendedDeploymentResult`.

        Note: file reads are currently performed using blocking I/O (``open(...).read()``). If you
        need fully non-blocking file access, load the bytes yourself and call :meth:`create_deployment`.

        Args:
            files: File paths (``str`` or ``Path``) to deploy.
            tenant_id: Optional tenant identifier. If not provided, the default tenant is used.

        Returns:
            ExtendedDeploymentResult: The deployment result with extracted resource lists.

        Raises:
            FileNotFoundError: If any file path does not exist.
            PermissionError: If any file path cannot be read.
            IsADirectoryError: If any file path is a directory.
            OSError: For other I/O failures while reading files.
            Exception: Propagates any exception raised by :meth:`create_deployment` (including
                typed API errors in :mod:`camunda_orchestration_sdk.errors` and ``httpx.TimeoutException``).
        """
        from .models.create_deployment_data import CreateDeploymentData
        from .types import File, UNSET
        import os

        resources = []
        for file_path in files:
            file_path = str(file_path)
            with open(file_path, "rb") as f:
                content = f.read()
            resources.append(File(payload=content, file_name=os.path.basename(file_path)))

        data = CreateDeploymentData(resources=resources, tenant_id=tenant_id if tenant_id is not None else UNSET)
        return ExtendedDeploymentResult(await self.create_deployment(data=data))

{new_async_methods}
'''
    
    final_content = f"{imports_content}\n{type_checking_block}\n{class_content}\n{extended_result_code}\n{camunda_client_code}"

    with open(client_file, "w") as f:
        f.write(final_content)
    
    print(f"Successfully added CamundaClient and CamundaAsyncClient to {client_file}")

    init_file = package_path / "__init__.py"
    if init_file.exists():
        with open(init_file, "r") as f:
            init_content = f.read()

        def _ensure_all_tuple_exports(content: str, exports: list[str]) -> str:
            lines = content.splitlines()
            out: list[str] = []
            i = 0
            while i < len(lines):
                line = lines[i]
                if line.startswith("__all__"):
                    out.append(line)
                    i += 1

                    tuple_lines: list[str] = []
                    while i < len(lines) and lines[i].strip() != ")":
                        tuple_lines.append(lines[i])
                        i += 1

                    closing = lines[i] if i < len(lines) else ")"

                    existing: set[str] = set()
                    for tl in tuple_lines:
                        stripped = tl.strip()
                        if stripped.startswith('"') and stripped.endswith(','):
                            existing.add(stripped.strip(',').strip('"'))

                    indent = "    "
                    for tl in tuple_lines:
                        m = re.match(r"^(\s*)\"", tl)
                        if m:
                            indent = m.group(1)
                            break

                    for export in exports:
                        if export not in existing:
                            tuple_lines.append(f'{indent}"{export}",')

                    out.extend(tuple_lines)
                    out.append(closing)
                    i += 1
                    continue

                out.append(line)
                i += 1

            return "\n".join(out) + "\n"

        # Ensure clients are exported
        if "from .client import AuthenticatedClient, Client, CamundaClient, CamundaAsyncClient" not in init_content:
            if "from .client import AuthenticatedClient, Client, CamundaClient" in init_content:
                init_content = init_content.replace(
                    "from .client import AuthenticatedClient, Client, CamundaClient",
                    "from .client import AuthenticatedClient, Client, CamundaClient, CamundaAsyncClient",
                )
            else:
                init_content = init_content.replace(
                    "from .client import AuthenticatedClient, Client",
                    "from .client import AuthenticatedClient, Client, CamundaClient, CamundaAsyncClient",
                )

        init_content = _ensure_all_tuple_exports(
            init_content,
            ["CamundaClient", "CamundaAsyncClient", "WorkerConfig"],
        )

        if "from .runtime.job_worker import WorkerConfig" not in init_content:
            init_content += "\nfrom .runtime.job_worker import WorkerConfig"

        with open(init_file, "w") as f:
            f.write(init_content)
        print(f"Successfully exported CamundaClient, CamundaAsyncClient, and WorkerConfig in {init_file}")

def run(context):
    out_dir = Path(context["out_dir"])
    package_dir = out_dir / "camunda_orchestration_sdk"
    if not package_dir.exists():
        print(f"Could not find package directory in {out_dir}")
        return
    generate_flat_client(package_dir)

if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent.parent
    package_dir = base_dir / "generated" / "camunda_orchestration_sdk"
    generate_flat_client(package_dir)
