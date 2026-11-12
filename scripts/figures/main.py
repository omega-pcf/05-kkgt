#!/usr/bin/env python3
"""
Entry point for figure generation for the golden-throat paper.

This module coordinates the execution of all figure generators.
It can be run individually or as part of the build pipeline.

The generators are the author's own code (``figuras_v134.py``, five
figures: ``fig_background``, ``fig_mobius_throat``, ``fig_granularity``,
``fig_throat_tiling``, ``fig_tilings_strip``); each one checks what it
draws numerically (assert) before saving.  This entry point only
registers them and redirects their ``savefig`` (relative to the CWD)
into ``images/``.

Usage:
    python scripts/figures/main.py                 # generate all
    python scripts/figures/main.py --list          # list generators
    python scripts/figures/main.py --figure fig_background
    python scripts/figures/main.py --figure 1      # by article number
    python scripts/figures/main.py --output-dir ../images
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path
from typing import Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

from generators.registry import (  # noqa: E402
    generate,
    generate_all,
    list_figures,
)

import figuras_v134  # noqa: E402


def main(args: Optional[list[str]] = None) -> int:
    """
    Main function that executes figure generators.

    Args:
        args: Command line arguments (optional, for testing)

    Returns:
        Exit code (0 = success, >0 = error)
    """
    parser = argparse.ArgumentParser(
        description="Generate figures for the golden-throat paper",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate all figures
  python main.py

  # Generate a specific figure (by name or by article number)
  python main.py --figure fig_background
  python main.py --figure 1

  # List available figures
  python main.py --list
        """
    )

    parser.add_argument(
        "--figure",
        "-f",
        type=str,
        help="Generate only a specific figure (by name or article number 1-5)"
    )

    parser.add_argument(
        "--list",
        "-l",
        action="store_true",
        help="List all available figures"
    )

    parser.add_argument(
        "--output-dir",
        "-o",
        type=str,
        default="images",
        help="Output directory for figures (default: images)"
    )

    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Verbose mode (show more information)"
    )

    parsed_args = parser.parse_args(args)

    # Resolve absolute path for output directory
    project_root = Path(__file__).resolve().parent.parent.parent
    output_dir = project_root / parsed_args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    if parsed_args.list:
        print("Available figures:")
        for name in list_figures():
            print(f"  - {name}")
        return 0

    figure = parsed_args.figure
    if figure and figure.isdigit():
        # article number -> pdf stem, como en figuras_v134.FIGURAS
        number = int(figure)
        if number not in figuras_v134.FIGURAS:
            print(f"❌ Unknown figure number: {figure}", file=sys.stderr)
            return 1
        figure = Path(figuras_v134.FIGURAS[number][2]).stem

    try:
        if figure:
            if parsed_args.verbose:
                print(f"Generating figure: {figure}")
            generate(figure, output_dir, verbose=parsed_args.verbose)
        else:
            if parsed_args.verbose:
                print(f"Generating all figures in: {output_dir}")
            generate_all(output_dir, verbose=parsed_args.verbose)

        if parsed_args.verbose:
            print(f"\n✓ Figures generated successfully in: {output_dir}")

        return 0

    except Exception as e:
        print(f"❌ Error generating figures: {e}", file=sys.stderr)
        if parsed_args.verbose:
            import traceback
            traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
