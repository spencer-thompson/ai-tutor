import asyncio
import sys
from pathlib import Path

# Ensure repo root is on sys.path so `backend` package is importable when tests run from pytest
ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

import ast

def _load_read_root_from_file(path: Path):
    """Parse the `backend/main.py` file, extract the async function `read_root`,
    compile it into a callable object and return it.

    This avoids importing `backend.main` (which has heavy external dependencies)
    and keeps the smoke test fast and hermetic.
    """
    source = path.read_text()
    module_ast = ast.parse(source, filename=str(path))

    for node in module_ast.body:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == "read_root":
            # Remove decorators (e.g. @app.get) so the function can be compiled in isolation.
            node.decorator_list = []
            func_ast = ast.Module(body=[node], type_ignores=[])
            compiled = compile(func_ast, filename=str(path), mode="exec")
            namespace = {}
            exec(compiled, namespace)
            return namespace["read_root"]

    raise RuntimeError("read_root function not found in backend/main.py")


def test_root_returns_hello_world():
    """Call the async endpoint function directly (avoids running FastAPI lifespan/startup).

This keeps the smoke test fast and independent of external services (Mongo, OpenAI).
"""
    repo_root = Path(__file__).resolve().parents[1]
    backend_main = repo_root / "backend" / "main.py"
    read_root = _load_read_root_from_file(backend_main)
    result = asyncio.run(read_root())
    assert result == {"Hello": "World"}
