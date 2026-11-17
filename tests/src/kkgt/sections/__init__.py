"""kkgt.sections: every number and the five figures of
«The Kaluza–Klein spectrum of the golden throat», v136.

Usage:  PYTHONPATH=tests/src python -m kkgt.sections          all sections
        PYTHONPATH=tests/src python -m kkgt.sections 2 14     only those sections

Each section is one of the earlier scripts, unchanged, in its own namespace,
registered in ``SECCIONES`` as ``(number, title, function)``; the test suite
runs them one at a time through ``kkgt.harness.run_section``.
Figures: 1 (section 44), 2 (section 13), 3 (section 10), 4 (section 39),
5 (section 41). Python 3.13, NumPy, SciPy, Matplotlib; section 2
also needs mpmath.

The computation is a package (SEC-001, layer 2): this file only assembles
the registry from the parts -- the sections not yet moved live in
``kkgt.sections._rest``, the migrated lots live in their own sibling module
(``s17_24`` ...) -- and ``SECCIONES`` is always the whole registry, in
numeric order.
"""
from . import s09_16
from . import s17_24
from ._rest import SECCIONES as _REST_SECCIONES
from ._rest import _C, _LamP  # the module-level names of the original sections file

SECCIONES = sorted(
    (*_REST_SECCIONES, *s09_16.SECCIONES, *s17_24.SECCIONES),
    key=lambda entry: entry[0],
)
