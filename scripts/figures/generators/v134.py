"""
Los cinco generadores de «One object instead of a choice of vacuum…»
registrados con @register.

El código de dibujo y de comprobación (assert) vive en
``figuras_v134.py`` (extraído por el autor de ``reproduce_v134.py``) y
NO se toca aquí: este módulo sólo lo registra en la convención familiar
y redirige la salida —los ``savefig`` del autor son relativos al CWD—
al ``output_dir`` (``images/``) con un ``chdir`` temporal.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

_parent_dir = Path(__file__).resolve().parent.parent
if str(_parent_dir) not in sys.path:
    sys.path.insert(0, str(_parent_dir))

from generators import register  # noqa: E402
from generators.rc import apply_rc  # noqa: E402  (rcParams deterministas)

import figuras_v134  # noqa: E402  (código del autor, intacto)


def _run_redirected(fn, output_dir: Path) -> None:
    """Ejecuta ``fn()`` con el CWD dentro de ``output_dir``.

    Los generadores del autor escriben con ``savefig("fig_X.pdf", …)``
    (CWD); el chdir es toda la adaptación de rutas.  Antes de cada figura
    se reaplican los rcParams deterministas: ``generate_fig_background`` termina con
    ``plt.rcParams.update(matplotlib.rcParamsDefault)`` y los dejaría en
    los valores por defecto (Type 3 sin /ToUnicode).
    """
    previous = os.getcwd()
    os.chdir(output_dir)
    try:
        apply_rc()
        fn()
    finally:
        os.chdir(previous)


def _make_generator(fn, section: int, pdf: str):
    def generate(output_dir: Path, verbose: bool = False) -> None:
        if verbose:
            print(f"  guardando {pdf} en {output_dir}")
        _run_redirected(fn, output_dir)
        if verbose:
            print(f"  ok: {Path(output_dir) / pdf}")

    generate.__name__ = f"generate_{Path(pdf).stem}"
    generate.__doc__ = f"Figura del artículo en sección {section} -> {pdf}"
    return generate


# FIGURAS = {n: (sección, función, pdf)} en figuras_v134.py — fuente única.
for _num, (_section, _fn, _pdf) in sorted(figuras_v134.FIGURAS.items()):
    register(Path(_pdf).stem)(_make_generator(_fn, _section, _pdf))
