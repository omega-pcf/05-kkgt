"""
Figure generator module (convención de la familia Ω_PCF, igual que
01-hilbert-polya/scripts/figures).

Cada generador se registra con el decorador ``@register("nombre")`` y
recibe ``(output_dir, verbose)``.  Al final de este módulo se importan
los módulos de ``generators/`` para que se registren solos.
"""

import sys
from pathlib import Path
from typing import Callable, Dict

# Generator registry
_generators: Dict[str, Callable[[Path, bool], None]] = {}


def register(name: str):
    """
    Decorator to register a figure generator.

    Usage:
        @register("fig_background")
        def generate_fig_background(output_dir: Path, verbose: bool = False):
            # Generate figure...
            pass
    """
    def decorator(func: Callable[[Path, bool], None]):
        _generators[name] = func
        return func
    return decorator


def generate(name: str, output_dir: Path, verbose: bool = False) -> None:
    """Execute a specific generator.

    Raises:
        KeyError: If the generator does not exist
    """
    if name not in _generators:
        available = ", ".join(_generators.keys())
        raise KeyError(
            f"Generator '{name}' not found. "
            f"Available generators: {available}"
        )

    if verbose:
        print(f"  → Running generator: {name}")

    _generators[name](output_dir, verbose)


def generate_all(output_dir: Path, verbose: bool = False) -> None:
    """Execute all registered generators."""
    if verbose:
        print(f"Generating {len(_generators)} figure(s)...")

    for name in sorted(_generators.keys()):
        generate(name, output_dir, verbose)


def list_figures() -> list[str]:
    """Return list of all registered generators."""
    return sorted(_generators.keys())


# Ensure parent directory is in path for imports (figuras_v134.py vive aquí)
_parent_dir = Path(__file__).parent.parent
if str(_parent_dir) not in sys.path:
    sys.path.insert(0, str(_parent_dir))

# Import existing generators (they register automatically via @register)
import generators.v134  # noqa: E402, F401
