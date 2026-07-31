"""
Architectural tests that enforce layer dependency rules.

- domain must not import from application, infrastructure, or presentation
- application must not import from infrastructure or presentation
"""

from __future__ import annotations

import ast
from pathlib import Path

import pytest

_SRC = Path(__file__).parent.parent.parent / "src" / "codexathenae"

_FORBIDDEN: dict[str, list[str]] = {
    "domain": ["application", "infrastructure", "presentation", "fastapi", "pymongo", "pydantic"],
    "application": ["infrastructure", "presentation", "fastapi", "pymongo"],
}


def _collect_imports(filepath: Path) -> list[str]:
    source = filepath.read_text(encoding="utf-8")
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return []
    imports: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.append(alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module:
            imports.append(node.module)
    return imports


def _get_layer_files(layer: str) -> list[Path]:
    layer_path = _SRC / layer
    if not layer_path.exists():
        return []
    return list(layer_path.rglob("*.py"))


@pytest.mark.parametrize("layer,forbidden_modules", list(_FORBIDDEN.items()))
def test_layer_does_not_import_forbidden(layer: str, forbidden_modules: list[str]) -> None:
    violations: list[str] = []
    for filepath in _get_layer_files(layer):
        imports = _collect_imports(filepath)
        for imp in imports:
            for forbidden in forbidden_modules:
                if forbidden in imp:
                    violations.append(
                        f"{filepath.relative_to(_SRC)}: imports '{imp}' (forbidden: {forbidden})"
                    )
    assert not violations, "Layer dependency violations:\n" + "\n".join(violations)
