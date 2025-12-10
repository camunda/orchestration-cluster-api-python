import ast
import os
from pathlib import Path
import re

def to_camel_case(snake_str):
    components = snake_str.split('_')
    return components[0] + ''.join(x.title() for x in components[1:])

def get_imports_and_signature(file_path, package_root):
    with open(file_path, "r") as f:
        code = f.read()
    
    tree = ast.parse(code)
    
    imports = []
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
    
    adjusted_imports = []
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

def generate_flat_client(package_path):
    api_dir = package_path / "api"
    if not api_dir.exists():
        print(f"API directory not found at {api_dir}")
        return

    methods = []
    all_imports = set()

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
                    ann = f": {ast.unparse(args.kwarg.annotation)}" if args.kwarg.annotation else ""
                    arg_strs.append(f"**{args.kwarg.arg}{ann}")
                else:
                    arg_strs.append("**kwargs")
                
                sig_str = ", ".join(arg_strs)
                return_ann = f" -> {ast.unparse(sync_func.returns)}" if sync_func.returns else ""
                docstring = ast.get_docstring(sync_func)
                docstring_str = f'        """{docstring}"""\n' if docstring else ""
                
                methods.append(f"""
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
                    ann = f": {ast.unparse(args.kwarg.annotation)}" if args.kwarg.annotation else ""
                    arg_strs.append(f"**{args.kwarg.arg}{ann}")
                else:
                    arg_strs.append("**kwargs")

                sig_str = ", ".join(arg_strs)
                return_ann = f" -> {ast.unparse(async_func.returns)}" if async_func.returns else ""
                docstring = ast.get_docstring(async_func)
                docstring_str = f'        """{docstring}"""\n' if docstring else ""
                
                methods.append(f"""
    async def {method_name}_async({sig_str}){return_ann}:
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
    imports_content += "\nfrom .runtime.job_worker import JobWorker, WorkerConfig"

    # Prepare TYPE_CHECKING block
    type_checking_block = "\nif TYPE_CHECKING:\n"
    sorted_imports = sorted(list(all_imports))
    for imp in sorted_imports:
        type_checking_block += f"    {imp}\n"

    new_methods = "\n".join(methods)

    camunda_client_code = f"""
class CamundaClient:
    client: Client | AuthenticatedClient
    _workers: list[JobWorker]

    def __init__(self, base_url: str, token: str | None = None, **kwargs):
        if token:
            self.client = AuthenticatedClient(base_url=base_url, token=token, **kwargs)
        else:
            self.client = Client(base_url=base_url, **kwargs)
        self._workers = []

    def __enter__(self):
        self.client.__enter__()
        return self

    def __exit__(self, *args, **kwargs):
        return self.client.__exit__(*args, **kwargs)

    async def __aenter__(self):
        await self.client.__aenter__()
        return self

    async def __aexit__(self, *args, **kwargs):
        await self.client.__aexit__(*args, **kwargs)

    def create_job_worker(self, job_type: str, callback: Callable, timeout: int = 30000, auto_start: bool = True, **kwargs) -> JobWorker:
        config = WorkerConfig(job_type=job_type, timeout=timeout, **kwargs)
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

{new_methods}
"""
    
    final_content = f"{imports_content}\n{type_checking_block}\n{class_content}\n{camunda_client_code}"

    with open(client_file, "w") as f:
        f.write(final_content)
    
    print(f"Successfully added CamundaClient to {client_file}")

    init_file = package_path / "__init__.py"
    if init_file.exists():
        with open(init_file, "r") as f:
            init_content = f.read()
        
        if "CamundaClient" not in init_content:
            init_content = init_content.replace(
                '"Client",',
                '"Client",\n    "CamundaClient",'
            )
            init_content = init_content.replace(
                "from .client import AuthenticatedClient, Client",
                "from .client import AuthenticatedClient, Client, CamundaClient"
            )
            
            with open(init_file, "w") as f:
                f.write(init_content)
            print(f"Successfully exported CamundaClient in {init_file}")

def run(context):
    out_dir = Path(context["out_dir"])
    package_dir = out_dir / "camunda_orchestration_sdk"
    if not package_dir.exists():
        print(f"Could not find package directory in {out_dir}")
        return
    generate_flat_client(package_dir)

if __name__ == "__main__":
    base_dir = Path(__file__).parent.parent
    package_dir = base_dir / "generated" / "camunda_orchestration_sdk"
    generate_flat_client(package_dir)
