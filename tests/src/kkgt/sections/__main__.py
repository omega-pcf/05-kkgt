"""The entry point of the computation: ``python -m kkgt.sections [N ...]``."""
import sys

from . import SECCIONES

if __name__ == "__main__":
    requested = {int(a) for a in sys.argv[1:]}
    for n, title, f in SECCIONES:
        if requested and n not in requested:
            continue
        print(f"\n{'#' * 72}\n# {n}. {title}\n{'#' * 72}")
        try:
            f()
        except ModuleNotFoundError as e:
            print(f"[section {n} skipped: missing module {e.name}]")
