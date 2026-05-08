#!/usr/bin/env python3
"""Linter for enforcing the layered architecture."""

import ast
import sys
from pathlib import Path
from typing import Optional


# Layer order (for dependency checking)
LAYERS = ['utils', 'providers', 'config', 'types', 'repo', 'service', 'runtime', 'ui']

# Legal imports for each layer
LEGAL_IMPORTS = {
    'types': ['types'],
    'config': ['types', 'config'],
    'repo': ['types', 'config', 'repo'],
    'providers': ['types', 'config', 'utils', 'providers'],
    'service': ['types', 'config', 'repo', 'providers', 'service'],
    'runtime': ['types', 'config', 'repo', 'service', 'providers', 'runtime'],
    'ui': ['types', 'config', 'service', 'runtime', 'providers', 'ui'],
}

MAX_LINES = 300
SRC_DIR = Path(__file__).parent / 'pong'


class LintError:
    """Represents a linting error."""
    
    def __init__(self, file_path: str, line: int, message: str):
        self.file_path = file_path
        self.line = line
        self.message = message
    
    def __str__(self) -> str:
        return f"{self.file_path}:{self.line}: {self.message}"


def get_layer(file_path: Path) -> Optional[str]:
    """Get the layer name for a file."""
    rel_path = file_path.relative_to(SRC_DIR)
    parts = rel_path.parts
    if len(parts) > 0:
        return parts[0]
    return None


def check_layer_imports(file_path: Path, tree: ast.Module) -> list[LintError]:
    """Check that imports respect layer boundaries."""
    errors = []
    layer = get_layer(file_path)
    
    if layer is None or layer not in LEGAL_IMPORTS:
        return errors
    
    legal = LEGAL_IMPORTS[layer]
    
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom):
            if node.module:
                # Get the top-level module name
                module_parts = node.module.split('.')
                top_level = module_parts[0]
                
                # Check if importing from a layer
                if top_level in LAYERS and top_level not in legal:
                    errors.append(LintError(
                        str(file_path),
                        node.lineno,
                        f"Cannot import from '{top_level}' layer. Layer '{layer}' may only import from: {', '.join(legal)}"
                    ))
    
    return errors


def check_file_lines(file_path: Path) -> list[LintError]:
    """Check that file doesn't exceed line limit."""
    errors = []
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            if len(lines) > MAX_LINES:
                errors.append(LintError(
                    str(file_path),
                    1,
                    f"File has {len(lines)} lines (max {MAX_LINES})"
                ))
    except IOError:
        pass
    return errors


def check_layer_membership(file_path: Path) -> list[LintError]:
    """Check that file is in a valid layer directory."""
    errors = []
    rel_path = file_path.relative_to(SRC_DIR)
    parts = rel_path.parts
    
    if len(parts) == 0:
        errors.append(LintError(str(file_path), 1, "File is not in src/ directory"))
        return errors
    
    # Skip __init__.py and __main__.py at package root (pong/__init__.py, pong/__main__.py)
    if len(parts) == 1 and parts[0] in ('__init__.py', '__main__.py'):
        return errors
    
    layer = parts[0]
    if layer not in LAYERS:
        errors.append(LintError(
            str(file_path),
            1,
            f"File is in '{layer}' directory, which is not a valid layer. Valid layers: {', '.join(LAYERS)}"
        ))
    
    return errors


def lint_file(file_path: Path) -> list[LintError]:
    """Lint a single Python file."""
    errors = []
    
    # Check layer membership
    errors.extend(check_layer_membership(file_path))
    
    # Check file size
    errors.extend(check_file_lines(file_path))
    
    # Parse and check imports
    try:
        with open(file_path, 'r') as f:
            source = f.read()
        tree = ast.parse(source, filename=str(file_path))
        errors.extend(check_layer_imports(file_path, tree))
    except SyntaxError as e:
        errors.append(LintError(str(file_path), e.lineno or 1, f"Syntax error: {e.msg}"))
    except IOError:
        pass
    
    return errors


def collect_python_files(src_dir: Path) -> list[Path]:
    """Collect all Python files under src/."""
    return list(src_dir.rglob('*.py'))


def main() -> int:
    """Run the linter."""
    if not SRC_DIR.exists():
        print(f"Error: {SRC_DIR} does not exist", file=sys.stderr)
        return 1
    
    python_files = collect_python_files(SRC_DIR)
    all_errors: list[LintError] = []
    
    for file_path in python_files:
        errors = lint_file(file_path)
        all_errors.extend(errors)
    
    if all_errors:
        print("Linting failed:")
        for error in sorted(all_errors, key=lambda e: (e.file_path, e.line)):
            print(f"  {error}")
        return 1
    else:
        print("Linting passed!")
        return 0


if __name__ == '__main__':
    sys.exit(main())
