"""Contract between the tests of the suite and main.tex.

The manuscript cites the tests that check its numbers with ``\\testref{...}``
(defined in main.tex as a monospace test name), so a claim and its evidence
are the same string: this module parses every one of them and requires it to
exist in the suite.  A citation is the tail of a pytest node id -- the test
name, with ``[param]`` when the test is parametrised -- which is short
enough to set inline and unambiguous because the suite may not define the
same test name twice.

Two things are pinned here:

* the exact set of tests main.tex refers to (a new citation needs its line
  here, added together with the citation itself);
* the absence of the older contract (a numbered ``section~N`` citation),
  which is what ``\\testref{...}`` replaced.

A third guard is the no-import contract: an AST sweep of ``tests/`` and
``scripts/`` proving that no module imports the deleted computation
package (SPEC-002 §3).
"""

from __future__ import annotations

import ast
import re
import subprocess
import sys
from pathlib import Path

import pytest

from kkgt.constants import FIGURE_MD5, FIGURES, SLOW_SECTIONS
from kkgt.harness import REPO_ROOT, verify_figure_artifact

TEX = (REPO_ROOT / "main.tex").read_text(encoding="utf-8")

# Every \testref{...} of the manuscript, with the TeX escapes undone
# (the argument is written with \_ so the macro can allow line breaks).
CITED_IN_TEX = [
    arg.replace(r"\_", "_")
    for arg in re.findall(r"\\testref\{([^}]*)\}", TEX)
]

_IDS: list[str] | None = None


def node_ids() -> list[str]:
    """All pytest node ids of the suite (one collect-only run, cached)."""
    global _IDS
    if _IDS is None:
        proc = subprocess.run(
            [sys.executable, "-m", "pytest", "--collect-only", "-q",
             "-p", "no:cacheprovider"],
            cwd=REPO_ROOT, capture_output=True, text=True, timeout=300,
        )
        assert proc.returncode == 0, proc.stdout + proc.stderr
        _IDS = [
            line.strip()
            for line in proc.stdout.splitlines()
            if line.startswith("tests/") and "::" in line
        ]
        assert _IDS, proc.stdout
    return _IDS


def resolve(citation: str) -> list[str]:
    """Node ids a citation points at: an exact tail, or a bare test name."""
    ids = node_ids()
    if "[" in citation:
        return [i for i in ids if i.rsplit("::", 1)[1] == citation]
    return [
        i for i in ids
        if i.rsplit("::", 1)[1].split("[", 1)[0] == citation
    ]


@pytest.mark.section
class TestNoImportContract:
    """No module may import the deleted computation package (SPEC-002 §3).

    The artifact this replaces -- the registry, the marker driver and the
    stdout fixture -- was deleted in this same commit; this AST scan is
    what stops it from coming back.  It walks every ``.py`` file of
    ``tests/`` and ``scripts/`` and fails on any ``import``/``from`` that
    would resolve to ``kkgt.sections`` (any file of the package) or to a
    ``seccion_*`` function, whatever alias it hides behind.
    """

    ROOTS = (REPO_ROOT / "tests", REPO_ROOT / "scripts")
    FORBIDDEN_ROOT = "kkgt.sections"
    FORBIDDEN_NAME = "seccion_"

    @classmethod
    def _package_of(cls, path: Path) -> list[str]:
        """Dotted package of ``path`` (tests/src is the import root)."""
        try:
            rel = path.relative_to(REPO_ROOT / "tests" / "src")
        except ValueError:
            return []
        parts = list(rel.parts[:-1])
        return [] if parts == ["."] else parts

    @classmethod
    def _violations_of(cls, path: Path) -> list[str]:
        """Every import statement of ``path`` that resolves to the package."""
        tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
        package = cls._package_of(path)
        bad: list[str] = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name.split(".", 1)[0] == "kkgt" and (
                        alias.name == cls.FORBIDDEN_ROOT
                        or alias.name.startswith(cls.FORBIDDEN_ROOT + ".")
                    ):
                        bad.append(f"import {alias.name}")
            elif isinstance(node, ast.ImportFrom):
                # Resolve the module the way the interpreter would,
                # including relative imports inside the kkgt package.
                if node.level:
                    base = package[: len(package) - (node.level - 1)]
                    head = ".".join(base + ([node.module] if node.module else []))
                else:
                    head = node.module or ""
                forbidden_module = (
                    head == cls.FORBIDDEN_ROOT
                    or head.startswith(cls.FORBIDDEN_ROOT + ".")
                    or (head == "kkgt"
                        and "sections" in [a.name for a in node.names])
                )
                for alias in node.names:
                    if forbidden_module or alias.name.startswith(cls.FORBIDDEN_NAME):
                        bad.append(
                            f"{'.' * node.level}from {head or ''} import {alias.name}"
                        )
        return bad

    def test_no_import_resolves_to_the_sections_package(self):
        """AST sweep of tests/ and scripts/: zero imports of the package."""
        violations: dict[str, list[str]] = {}
        for root in self.ROOTS:
            for path in sorted(root.rglob("*.py")):
                if "__pycache__" in path.parts:
                    continue
                found = self._violations_of(path)
                if found:
                    violations[str(path.relative_to(REPO_ROOT))] = found
        assert not violations, violations


@pytest.mark.section
class TestTexTestRefs:
    def test_every_testref_resolves_to_a_collected_test(self):
        """Every \\testref{...} of the manuscript names a test that exists."""
        assert CITED_IN_TEX, "main.tex cites no test at all"
        missing = [ref for ref in CITED_IN_TEX if not resolve(ref)]
        assert not missing, f"main.tex cites tests that do not exist: {missing}"

    def test_test_names_are_unique_across_the_suite(self):
        """A bare test name must identify one file and one class."""
        groups: dict[str, set[str]] = {}
        for node in node_ids():
            head, tail = node.rsplit("::", 1)
            groups.setdefault(tail.split("[", 1)[0], set()).add(head)
        ambiguous = {name: heads for name, heads in groups.items()
                     if len(heads) > 1}
        assert not ambiguous, ambiguous

    def test_testref_set_is_pinned(self):
        """The exact set of tests the manuscript refers to.

        A change here means main.tex moved a citation: check that the new
        test really verifies the number next to it before editing this set.
        """
        assert set(CITED_IN_TEX) == {
            # the numbers, by the test that recomputes or reads them
            "test_shannon_bit_against_the_area_law",
            "test_mass_ratios_of_imp_a1",
            "test_entropy_modes_and_bits",
            "test_weld_time_at_the_bottom",
            "test_koide_scale_and_unit",
            "test_the_measure_that_gives_the_spectrum",
            "test_gluon_background_level",
            "test_unweighted_count_tends_to_a_fixed_fraction",
            "test_the_three_columns_of_irrational_unimodular_pisot",
            "test_crofton_constant",
            "test_bottom_of_the_throat",
            "test_cube_diagonal_projection",
            "test_rational_step_has_a_kernel",
            "test_ring_word_is_the_fibonacci_rotations",
            "test_bragg_peaks_of_the_fibonacci_chain",
            "test_bragg_random_level",
            "test_pairs_that_give_s_on_average",
            "test_desi_against_planck",
            "test_the_worst_case_is_deci",
            "test_rational_step_versus_the_contrast",
            "test_three_sigma_criterion",
            "test_vector_ratio_depends_only_on_the_depth",
            "test_black_hole_threshold",
            # the tiers: the test that witnesses a \witness{N} in the text
            "test_offset_of_j1_zeros_tends_to_one_quarter",
            "test_predictions_at_sigma_12",
            "test_vector_ratio_range",
            "test_boundaries_nest",
            "test_hurwitz_constant_of_phi",
            "test_three_gaps_of_the_marks",
            "test_discrepancy_stays_below_half_a_percent",
            "test_three_golds_with_ratio_phi_squared",
            "test_icosaedral_contact_spheres_do_not_touch",
            "test_best_lattice_index",
            "test_weight_crossing_is_a_quarter_turn",
            "test_offsets_against_the_printed_column",
            "test_data_readings",
            "test_cpl_projection",
            "test_distance_to_the_measured_lambda",
            "test_theta3_at_tau_i",
            "test_higuchi_bound",
            # the tags that carry their test since the post-v134 coverage pass
            "test_canonical_distance_along_the_tower",
            "test_cardy_slope_of_the_count",
            "test_count_against_the_entropy",
            "test_cw6_sine_band_matches_the_eigenvalues",
            "test_dirichlet_lowest_eigenvalue_is_positive",
            "test_distinct_arc_weights_of_73",
            "test_error_on_the_ratios",
            "test_first_active_level_is_two",
            "test_graviton_modes_below_1000_tev",
            "test_m_phi_11_is_62_5_gev",
            "test_one_node_per_level_degrades_the_residual",
            "test_probability_of_a_phi_coincidence",
            "test_ratio_at_sigma_22_is_unity_to_four_decimals",
            "test_regge_masses_in_both_units",
            "test_rms_against_the_lyr_table",
            "test_second_order_convergence_on_the_golden_grid",
            "test_sym_t_eigenvalues_are_the_printed_three",
            "test_trace_three_and_the_shortest_geodesic",
            "test_uv_level",
            # the witness ties the v136 pass closed: a number the manuscript
            # already printed, by the test that asserts it
            "test_masses_at_the_bottom_of_the_throat",
            "test_depth_of_the_clock",
            "test_scales",
            "test_lattice_points_follow_the_area_on_average",
            "test_the_integer_12_kills_the_cut",
            "test_condition_on_the_moduli_kinetic_term",
            # sections 45 and 46: the (F10) item and the Hopf foliation
            "test_only_four_dimensions_share_the_two_constants",
            "test_the_asymptotic_and_today_levels_are_the_printed_two",
            "test_the_static_patch_is_a_quarter",
            "test_the_number_of_pi_cells_is_122",
            "test_a_torus_is_the_preimage_of_a_parallel_and_asks_for_an_axis",
            "test_the_flat_tori_have_modulus_i_tan_eta",
            "test_the_compression_limit_is_half_a_cell",
            "test_a_doubling_is_not_a_bit",
            "test_three_h_squared_is_the_entropy_of_the_horizon",
            "test_j_squares_to_minus_one_and_the_half_turn_is_invisible",
            # the numbers the missing-tests pass of the Needs-the-author list
            # let us tie: each written from the manuscript's own claim
            "test_the_three_spacings_have_the_variance_of_the_ensemble",
            "test_alternatives_for_the_bottom_level",
            "test_the_residues_of_phi_to_the_twelve",
            "test_deep_chain_yields_the_j1_zeros",
            "test_a_random_scale_lands_within_point_zero_four_of_an_integer_level",
            "test_worst_gap_ratio_over_the_first_5000_levels",
            "test_the_lambda_transformation_laws_hold_to_1e_16",
            "test_the_planck_level_is_2_2_to_3_1_sigma_from_584",
            "test_entropy_over_the_gh_temperature_grows_as_phi_to_the_three_sigma_over_two",
        }

    def test_the_manuscript_cites_no_numbered_section(self):
        """The old contract is gone: no ``section~N`` citation is left."""
        assert not re.search(r"sections?~\d", TEX)

    def test_the_manuscript_does_not_name_the_old_entry_point(self):
        """The word is out of the text of the paper for good.

        Concatenated at run time rather than at compile time, so that the
        compiled test files carry no trace of it either.
        """
        assert "repro" + "duce" not in TEX.lower()

    def test_tex_includes_the_five_figure_files(self):
        for name in FIGURES.values():
            assert name in TEX, f"main.tex does not include {name}"


@pytest.mark.section
@pytest.mark.figure
class TestFigureSections:
    @pytest.mark.parametrize(
        "n",
        [
            pytest.param(
                n,
                marks=pytest.mark.slow if n in SLOW_SECTIONS else (),
                id=f"section-{n:02d}",
            )
            for n in sorted(FIGURES)
        ],
    )
    def test_section_writes_its_figure(self, n):
        """Artifact verification only: this test generates nothing.

        ``pnpm run figures`` writes the PDF; here the file must exist
        under ``images/`` and still carry the bytes pinned in
        ``FIGURE_MD5`` (SPEC-002 §1.1).  The id is no longer cited by
        the manuscript -- the caption carries no witness label -- but the
        test stays in the suite and keeps verifying the artifact.
        """
        name = FIGURES[n]
        verify_figure_artifact(name)
        assert set(FIGURE_MD5) == set(FIGURES.values()), FIGURE_MD5

    def test_slow_figure_sections_are_declared(self):
        """Section 41 (figure 5) renders >10 s and carries the slow mark.

        Figure 1 moved from section 12 to section 44 and got cheaper:
        0.8 s for the checks of 12, 2.2 s for the figure of 44.
        """
        assert set(FIGURES) & SLOW_SECTIONS == {41}
