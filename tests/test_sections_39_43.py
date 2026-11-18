"""Deep numeric tests for sections 39-43 of the note.

The tilings (figures 4 and 5), the dictionary of section 40 and the three
columns of section 43 -- the last section main.tex cites.

The bodies of sections 39, 40, 41 and 43 live in this module now
(SPEC-002 §1): every number this file used to read back from a section's
stdout is produced by the functions below and asserted on its value.  No
test of this file runs a section any more.
"""

from __future__ import annotations

import itertools
import math
from decimal import Decimal, localcontext
from functools import lru_cache
from typing import Any

import numpy as np
import pytest

from kkgt.constants import LN_PHI, M_PCF, PHI
from kkgt.harness import verify_figure_artifact


# ═══════════════════════════ migrated bodies of sections 39-43 (SPEC-002 §1) ══
# The package these bodies came from is deleted (SPEC-002 units 3-4);
# what they checked is here, with their own tolerances and their own
# print precision.

# ── section 39: the throat and the Fibonacci tiling of its rings ────────
def ring_words(n: int = 7) -> list[str]:
    """Words of the rings: seed AAB at sigma = 0, substitution A->AB, B->A."""
    words = ["AAB"]
    for _ in range(n - 1):
        words.append("".join({"A": "AB", "B": "A"}[c] for c in words[-1]))
    return words


def ring_bounds(word: str) -> np.ndarray:
    """Boundaries of ``word`` as a fraction of the turn (widths 1 and 1/phi)."""
    widths = [1 if c == "A" else 1 / PHI for c in word]
    cumulative = np.cumsum([0] + widths)
    return cumulative / cumulative[-1]


def fibonacci_tiling_statements() -> None:
    """Every statement section 39 checked before drawing figure 4 (SPEC-002 §1).

    The section ended in ``print("S = pi(A/phi^2+B/phi^3) exact;
    boundaries nested")`` and the figure test read that line back from
    stdout; each statement now fails here, on its value, with the
    section's own tolerances: 1e-12 for the nesting, 1e-9 relative for
    the weighted sum.
    """
    words = ring_words()
    for s in range(6):
        inner, outer = ring_bounds(words[s]), ring_bounds(words[s + 1])
        assert all(np.min(np.abs(outer - x)) < 1e-12 for x in inner), s
    for s in range(7):
        count_a, count_b = words[s].count("A"), words[s].count("B")
        entropy = math.pi * PHI**s
        weighted = math.pi * (count_a / PHI**2 + count_b / PHI**3)
        assert abs(weighted - entropy) < 1e-9 * entropy, s


# ── the hyperbolic dictionary of section 40 and the strip of section 41 ─
def circle_through(a: complex, b: complex) -> tuple[complex, float]:
    """Centre and radius of the hyperbolic circle through the ideal points a, b."""
    system = np.array([[2 * a.real, 2 * a.imag], [2 * b.real, 2 * b.imag]])
    centre = complex(*np.linalg.solve(system, [abs(a) ** 2 + 1, abs(b) ** 2 + 1]))
    return centre, math.sqrt(abs(centre) ** 2 - 1)


def reflect_across(z: complex, a: complex, b: complex) -> complex:
    """Reflection of z in the geodesic through the ideal points a and b."""
    if abs((np.conj(a) * b).imag) < 1e-12:
        u = a if abs(a) > 1e-12 else b
        u = u / abs(u)
        return u * u * np.conj(z)
    centre, radius = circle_through(a, b)
    return centre + radius * radius / np.conj(z - centre)


def hyperbolic_distance(z: complex) -> float:
    """Poincare distance of z from the origin (capped at the ideal boundary)."""
    return 2 * math.atanh(min(abs(z), 1 - 1e-15))


def hyperbolic_centre(points: np.ndarray) -> complex:
    """Hyperbolic centre of the polygon ``points``."""
    k = 2 * points / (1 + np.abs(points) ** 2)
    mean = k.mean()
    return complex(mean / (1 + math.sqrt(max(0.0, 1 - abs(mean) ** 2))))


def polygon_key(points: np.ndarray) -> tuple[float, float]:
    """Rounded hyperbolic centre: the identity of a tile."""
    centre = hyperbolic_centre(points)
    return round(centre.real, 6), round(centre.imag, 6)


def tile_radii(p: int, q: int) -> tuple[float, float, float]:
    """(circumradius, inradius, edge) of the tile of the {p, q} tiling."""
    circumradius = math.acosh(1 / (math.tan(math.pi / p) * math.tan(math.pi / q)))
    inradius = math.acosh(math.cos(math.pi / q) / math.sin(math.pi / p))
    edge = 2 * math.acosh(math.cos(math.pi / p) / math.sin(math.pi / q))
    return circumradius, inradius, edge


def seed_tile(p: int, q: int, centre: str = "tile") -> np.ndarray:
    """The seed polygon of the {p, q} tiling on the horocycle of its circumradius."""
    circumradius, _inradius, _edge = tile_radii(p, q)
    t = math.tanh(circumradius / 2)
    if centre == "tile":
        polygon = np.array([t * np.exp(2j * math.pi * (k + 0.5) / p) for k in range(p)])
    else:
        polygon = np.array([t * np.exp(2j * math.pi * k / p) for k in range(p)])
    if centre == "vertex":
        v = polygon[0]
        polygon = (polygon - v) / (1 - np.conj(v) * polygon)
        polygon[0] = 0j
    return polygon


def tiles_within_disc(p: int, q: int, r_max: float, centre: str = "tile",
                      with_centres: bool = False) -> Any:
    """All tiles whose centre lies within ``r_max``: a pruned BFS over the edges.

    The centre of each tile is reflected together with its vertices, so
    the centre of the image is exact.  With ``with_centres`` the centres
    come back as a second value.
    """
    circumradius, _inradius, _edge = tile_radii(p, q)
    polygon = np.append(seed_tile(p, q, centre),
                        0j if centre == "tile" else complex(-math.tanh(circumradius / 2), 0))

    def last_key(poly: np.ndarray) -> tuple[float, float]:
        return round(poly[-1].real, 8), round(poly[-1].imag, 8)

    seen = {last_key(polygon)}
    frontier = [polygon]
    out = [polygon]
    limit = r_max + circumradius + 0.2
    while frontier:
        new = []
        for poly in frontier:
            for k in range(p):
                image = np.array([reflect_across(z, poly[k], poly[(k + 1) % p])
                                  for z in poly])
                key = last_key(image)
                if key in seen:
                    continue
                seen.add(key)
                if hyperbolic_distance(image[-1]) <= limit:
                    new.append(image)
        out += new
        frontier = new
    tiles = [poly[:-1] for poly in out]
    centres = np.array([poly[-1] for poly in out])
    return (tiles, centres) if with_centres else tiles


def tile_edges(tiles: list[np.ndarray]) -> list[tuple[complex, complex]]:
    """The distinct edges of ``tiles``, each as the ordered pair that carries it."""
    edges: dict[Any, tuple[complex, complex]] = {}
    for polygon in tiles:
        for j in range(len(polygon)):
            a, b = polygon[j], polygon[(j + 1) % len(polygon)]
            key = tuple(sorted([(round(a.real, 7), round(a.imag, 7)),
                                (round(b.real, 7), round(b.imag, 7))]))
            edges[key] = (a, b)
    return list(edges.values())


def edge_crossings(edges: list[tuple[complex, complex]], radius: float) -> int:
    """How many edges of ``edges`` the circle of hyperbolic radius ``radius`` cuts."""
    count = 0
    for a, b in edges:
        da, db = hyperbolic_distance(a), hyperbolic_distance(b)
        if (da < radius) != (db < radius):
            count += 1
            continue
        if da > radius and db > radius and abs((np.conj(a) * b).imag) > 1e-12:
            centre, rc = circle_through(a, b)
            foot = centre / abs(centre) * (abs(centre) - rc)
            angles = sorted([float(np.angle((a - centre) / (-centre))),
                             float(np.angle((b - centre) / (-centre)))])
            if angles[0] <= 0 <= angles[1] and hyperbolic_distance(foot) < radius:
                count += 2
    return count


def lattice_points(radius_squared: float) -> int:
    """Points of Z[i] with ``x^2 + y^2 <= radius_squared`` (section 40)."""
    bound = math.isqrt(int(radius_squared)) + 1
    return sum(1 for x in range(-bound, bound + 1) for y in range(-bound, bound + 1)
               if x * x + y * y <= radius_squared)


# ── section 40: open legs, Crofton, the pairs, the arc weights ─────────
@lru_cache(maxsize=None)
def open_legs_of_seven_three() -> tuple[int, ...]:
    """Open legs the {7,3} boundary cuts at each level 0..12 (Crofton)."""
    radii = [math.asinh(PHI**s) for s in range(13)]
    edges = tile_edges(tiles_within_disc(7, 3, radii[-1] + 0.05))
    return tuple(edge_crossings(edges, radius) for radius in radii)


def crofton_constant() -> float:
    """The constant legs/S of the {7,3} boundary (section 40)."""
    _circumradius, _inradius, edge = tile_radii(7, 3)
    return 4 * (7 * edge / 2) / (math.pi / 3) / math.pi


@lru_cache(maxsize=1)
def closest_pair_scan() -> tuple[int, list[int], tuple[int, int, int], float]:
    """The (tiling, chi) scan of section 40.

    Returns ``(total, counts closer than 1e-2..1e-6, best pair, its distance)``.
    """
    distances: list[float] = []
    best = (9.0, (0, 0, 0))
    for p in range(3, 61):
        for q in range(3, 61):
            if (p - 2) * (q - 2) <= 4:
                continue
            _circumradius, _inradius, edge = tile_radii(p, q)
            area = (p - 2) * math.pi - p * 2 * math.pi / q
            constant = 4 * (p * edge / 2) / area / math.pi
            for chi in range(2, 17):
                distance = abs(constant * math.log(chi) - 1)
                distances.append(distance)
                if distance < best[0]:
                    best = (distance, (p, q, chi))
    counts = [sum(x < t for x in distances) for t in (1e-2, 1e-3, 1e-4, 1e-5, 1e-6)]
    return len(distances), counts, best[1], best[0]


def mobius_shift(z: Any, w: complex) -> Any:
    """Möbius map sending ``w`` to the origin."""
    return (z - w) / (1 - np.conj(w) * z)


def mobius_unshift(z: Any, w: complex) -> Any:
    """Inverse of ``mobius_shift``."""
    return (z + w) / (1 + np.conj(w) * z)


@lru_cache(maxsize=1)
def arc_weights_of_seven_three() -> tuple[tuple[int, ...], int]:
    """Distinct arc weights per level of {7,3} and their total (section 40).

    The section also checked that the arcs of each level add up to the
    entropy S of that level; that check travels with the computation.
    """
    radii = [math.asinh(PHI**s) for s in range(13)]
    entropy = [math.pi * PHI**s for s in range(13)]
    edges = tile_edges(tiles_within_disc(7, 3, radii[9] + 0.05))
    per_level: list[int] = []
    all_weights: set[float] = set()
    for sigma in range(10):
        radius = radii[sigma]
        rho = math.tanh(radius / 2)
        angles: list[float] = []
        for a, b in edges:
            if (min(hyperbolic_distance(a), hyperbolic_distance(b)) > radius + 0.01
                    and abs((np.conj(a) * b).imag) > 1e-12):
                centre, rc = circle_through(a, b)
                if 2 * math.atanh(min(abs(centre) - rc, 1 - 1e-15)) > radius + 0.01:
                    continue
            shifted = mobius_shift(b, a)
            grid = np.linspace(0, 1, 300)
            image = mobius_unshift(grid * shifted, a)
            sign = np.sign(np.abs(image) - rho)
            for index in np.where(np.diff(sign) != 0)[0]:
                t0, t1 = grid[index], grid[index + 1]
                for _ in range(50):
                    mid = (t0 + t1) / 2
                    if ((abs(mobius_unshift(t0 * shifted, a)) - rho)
                            * (abs(mobius_unshift(mid * shifted, a)) - rho)) <= 0:
                        t1 = mid
                    else:
                        t0 = mid
                angles.append(float(np.angle(mobius_unshift(t0 * shifted, a))
                                    % (2 * math.pi)))
        angles = sorted(set(round(x, 9) for x in angles))
        gaps = np.diff(angles + [angles[0] + 2 * math.pi])
        weights = {round(math.sinh(radius) * x / 2, 6) for x in gaps}
        all_weights |= weights
        per_level.append(len(weights))
        # the arcs of a level add up to its entropy S = pi phi^sigma
        assert abs(sum(math.sinh(radius) * x / 2 for x in gaps) - entropy[sigma]) < 1e-6
    return tuple(per_level), len(all_weights)


def dictionary_statements() -> None:
    """The rest of section 40's own checks (SPEC-002 §1).

    The cusp metric, the two prototiles, the two substitutions, the
    60-digit identity, the three statements of the 1/2 and the points of
    Z[i] had no claim test of their own, so they are asserted here with
    the section's tolerances and the numbers it printed.
    """
    # the cusp: t = e^-y turns (dth^2 + dt^2)/t^2 into e^(2y) dth^2 + dy^2
    for y in (-3.0, 0.0, 1.7):
        assert abs(math.exp(-y) ** 2 * math.exp(2 * y) - 1) < 1e-12
    # two prototiles, equal at every level: areas 1.483259 and 0.916704
    a0 = 2 * math.pi / PHI**2
    assert round(a0 / PHI, 6) == 1.483259
    assert round(a0 / PHI**2, 6) == 0.916704
    for s in (0, 3, 7):
        t = PHI**-s
        for top, area in ((a0, a0 / PHI), (a0 / PHI, a0 / PHI**2)):
            dx = top * t
            assert abs(dx * (PHI / t - 1 / t) - area) < 1e-12
            assert abs(dx / (t / PHI) - PHI * top) < 1e-12
    # the two substitutions with eigenvalue phi
    substitutions = [m for m in itertools.product(range(10), repeat=4)
                     if m[0] + m[3] == 1 and m[0] * m[3] - m[1] * m[2] == -1]
    assert substitutions == [(0, 1, 1, 1), (1, 1, 1, 0)]
    # S = pi(A/phi^2 + B/phi^3) exact in 60 digits, for s = 0..40
    with localcontext() as ctx:
        ctx.prec = 60
        pi = Decimal("3.14159265358979323846264338327950288419716939937510582097494459")
        phi = (1 + Decimal(5).sqrt()) / 2
        count_a, count_b = 2, 1
        for s in range(41):
            assert abs(pi / phi**2 * count_a + pi / phi**3 * count_b
                       - pi * phi**s) < Decimal(10) ** -45
            count_a, count_b = count_a + count_b, count_a
    # the 1/2 of each statement: the constant of the definition places it
    solutions = {c: [f for f in np.linspace(0.001, 1, 99901)
                     if abs(1 / math.sqrt(c * f) - 1) < 1e-4]
                 for c in (1.5, 2, 3)}
    assert all(abs(np.mean(v) - 1 / c) < 1e-3 for c, v in solutions.items())
    fisher = {k: 1 / math.sqrt(k) for k in (2, 4, 8)}
    assert abs(fisher[4] - 0.5) < 1e-15
    p = np.linspace(0.01, 0.99, 9801)
    entropy = -(p * np.log2(p) + (1 - p) * np.log2(1 - p))
    assert abs(p[np.argmax(entropy)] - 0.5) < 1e-9
    # legs over S at every level (the printed column of {7,3})
    legs = open_legs_of_seven_three()
    assert [round(n / s, 3) for n, s in zip(legs, [math.pi * PHI**s for s in range(13)])] == [
        2.228, 2.754, 3.404, 2.63, 2.601, 2.411, 2.359, 2.379, 2.371, 2.374, 2.428,
        2.374, 2.415,
    ]
    # points of Z[i] (section 11.1): [5, 5, 9, 13, 21, 37, 57] ...
    counts = [lattice_points(PHI**s) for s in range(7)]
    assert counts == [5, 5, 9, 13, 21, 37, 57], counts
    assert lattice_points(PHI**12) == 1005
    assert math.floor(math.pi * PHI**12) == 1011
    # ... sigma = 22: points/S = 0.9998
    assert round(lattice_points(PHI**22) / (math.pi * PHI**22), 4) == 0.9998


# ── section 41: five regular tilings against the levels (figure 5) ─────
@lru_cache(maxsize=None)
def disc_tile_records(p: int, q: int) -> tuple[tuple[int, ...], tuple[int, ...]]:
    """For sigma = 0..6: tiles whose centre falls in the disc, and tangent edges.

    The counts of figure 5 and the tangency of a level's boundary with
    the edges of the tiling (section 41's ``REC``).
    """
    tiles, centres = tiles_within_disc(p, q, math.asinh(PHI**6) + 0.5, "tile", True)
    distances = [hyperbolic_distance(c) for c in centres]
    counts: list[int] = []
    tangencies: list[int] = []
    for s in range(7):
        radius = math.asinh(PHI**s)
        counts.append(sum(1 for d in distances if d <= radius))
        touches = 0
        for polygon in tiles:
            for j in range(p):
                a, b = polygon[j], polygon[(j + 1) % p]
                if abs((np.conj(a) * b).imag) < 1e-12:
                    continue
                centre, rc = circle_through(a, b)
                foot = centre / abs(centre) * (abs(centre) - rc)
                angles = sorted([float(np.angle((a - centre) / (-centre))),
                                 float(np.angle((b - centre) / (-centre)))])
                if (angles[0] - 1e-12 <= 0 <= angles[1] + 1e-12
                        and abs(hyperbolic_distance(foot) - radius) < 1e-9):
                    touches += 1
        tangencies.append(touches // 2)
    return tuple(counts), tuple(tangencies)


@lru_cache(maxsize=None)
def edge_layers(p: int, q: int, depth: int = 7, cap: int = 6000) -> tuple[int, ...]:
    """Tiles met layer by layer, from one tile and crossing the edges."""
    seed = seed_tile(p, q)
    seen = {polygon_key(seed)}
    frontier = [seed]
    layers = [1]
    for _ in range(depth):
        new = []
        for polygon in frontier:
            for k in range(p):
                image = np.array([reflect_across(z, polygon[k], polygon[(k + 1) % p])
                                  for z in polygon])
                key = polygon_key(image)
                if key not in seen:
                    seen.add(key)
                    new.append(image)
        layers.append(len(new))
        frontier = new
        if len(new) > cap:
            break
    return tuple(layers)


def layer_growth() -> dict[tuple[int, int], float]:
    """Growth per layer (edges) of the five tilings of figure 5 (section 41)."""
    growth = {}
    for p, q in ((7, 3), (3, 7), (5, 4), (12, 5), (6, 10)):
        layers = edge_layers(p, q, depth=7, cap=3000)
        growth[(p, q)] = layers[-1] / layers[-2]
    return growth


@lru_cache(maxsize=1)
def vertex_layer_counts() -> tuple[int, ...]:
    """Tiles of {3,7} reached from one by sharing a vertex (section 41's nl)."""
    tiles, _centres = tiles_within_disc(3, 7, 7.5, "tile", True)
    vertices: dict[tuple[float, float], list[int]] = {}
    for i, polygon in enumerate(tiles):
        for z in polygon:
            vertices.setdefault((round(z.real, 7), round(z.imag, 7)), []).append(i)
    layers: list[set[int]] = [{0}]
    seen = {0}
    for _ in range(6):
        nxt: set[int] = set()
        for i in layers[-1]:
            for z in tiles[i]:
                for j in vertices[(round(z.real, 7), round(z.imag, 7))]:
                    if j not in seen:
                        nxt.add(j)
        seen |= nxt
        layers.append(nxt)
    return tuple(len(x) for x in layers)


def hurwitz_float64_deviations() -> tuple[float, ...]:
    """``sqrt5 F_n^2 |phi - F_{n+1}/F_n|`` in float64, for n = 5..29 (section 41).

    Its last value is the 0.999902 the section prints: the cancellation of
    float64, not the value of the ratio (which is 1.00000 in 60 digits --
    see test_the_hurwitz_ratio_at_f_29_exactly).
    """
    phi = (1 + 5**0.5) / 2
    fib = [1, 1]
    for _ in range(40):
        fib.append(fib[-1] + fib[-2])
    return tuple(abs(phi - fib[n + 1] / fib[n]) * 5**0.5 * fib[n] ** 2
                 for n in range(5, 30))


def hurwitz_constant(value: Any) -> float:
    """``sqrt5 q^2 |X - p/q|`` of the continued fraction of X, in 80 digits.

    ``value`` must carry those 80 digits itself: the difference that the
    product amplifies is taken against it, so a Decimal built at the
    caller's precision would dominate the result.
    """
    with localcontext() as ctx:
        ctx.prec = 80
        h0, h1, k0, k1 = 0, 1, 1, 0
        y = value
        out = []
        for index in range(60):
            a = int(y)
            h0, h1 = h1, a * h1 + h0
            k0, k1 = k1, a * k1 + k0
            if index > 5:
                out.append(float(abs(value - Decimal(h1) / Decimal(k1)) * k1 * k1))
            y = 1 / (y - a)
        return min(out[-10:])


def hurwitz_constants() -> tuple[float, float, float, float]:
    """The four Hurwitz constants section 41 asserts: phi, 1/phi, phi + 1, sqrt(2).

    They are built at the precision the continued fraction needs (80
    digits), as the section did with ``getcontext().prec = 80``.
    """
    with localcontext() as ctx:
        ctx.prec = 80
        phi = (1 + Decimal(5).sqrt()) / 2
        return (hurwitz_constant(phi), hurwitz_constant(1 / phi),
                hurwitz_constant(phi + 1), hurwitz_constant(Decimal(2).sqrt()))


def qubit_bond_ratio(p: int, q: int) -> float:
    """The {p, q} constant c times ln 2: the qubit reading of section 41."""
    _circumradius, _inradius, edge = tile_radii(p, q)
    area = (p - 2) * math.pi - p * 2 * math.pi / q
    return 4 * (p * edge / 2) / area / math.pi * math.log(2)


def tilings_strip_statements() -> None:
    """Every statement section 41 checked before printing its conclusions (SPEC-002 §1).

    The counts of figure 5, the tangency of the boundaries, the Hurwitz
    constants, the layers of {3,7}, the growth per layer, the two radii
    and the qubit reading -- each with the section's own tolerance.
    """
    # tiles whose centre falls inside each disc
    for p, q, want in (
        (7, 3, (1, 8, 8, 29, 29, 57, 99)),
        (3, 7, (4, 16, 22, 46, 73, 133, 232)),
        (5, 4, (1, 6, 11, 11, 31, 41, 71)),
        (12, 5, (1, 1, 1, 1, 1, 1, 1)),
        (6, 10, (1, 1, 1, 1, 7, 7, 7)),
    ):
        counts, _tangencies = disc_tile_records(p, q)
        assert counts == want, (p, q, counts)
    # "boundary of a level tangent to edges: only {6,10}, sigma=1 (6 edges)
    #  and sigma=3 (12 edges)"
    for p, q in ((7, 3), (3, 7), (5, 4), (12, 5)):
        assert all(t == 0 for t in disc_tile_records(p, q)[1]), (p, q)
    assert disc_tile_records(6, 10)[1] == (0, 6, 0, 12, 0, 0, 0)
    # "Fibonacci ratios: ... -> 0.999902 (Hurwitz: phi is the worst approximant)"
    deviations = hurwitz_float64_deviations()
    assert all(abs(x - 1) < 0.05 for x in deviations[5:])
    assert round(deviations[-1], 6) == 0.999902
    # "Hurwitz: phi, 1/phi, phi+1 -> ... = 1/sqrt5; sqrt2 -> 0.35355"
    constants = hurwitz_constants()
    assert all(abs(c - 1 / math.sqrt(5)) < 1e-4 for c in constants[:3]), constants
    assert constants[3] < 0.36, constants[3]
    # "{3,7} by shared vertices: [1, 15, 45, 120, 315, 825, 2160]"
    assert vertex_layer_counts() == (1, 15, 45, 120, 315, 825, 2160)
    # "growth per layer (edges)" and the two exact radii
    growth = layer_growth()
    assert abs(growth[(7, 3)] - PHI**2) < 1e-3, growth
    assert abs(growth[(5, 4)] - PHI**2) < 1e-3, growth
    assert abs(growth[(3, 7)] - 1.6) < 0.05, growth
    assert growth[(12, 5)] > 10, growth
    assert abs(growth[(6, 10)] - 5) < 0.05, growth
    assert abs(math.cosh(tile_radii(5, 4)[2]) - PHI) < 1e-12
    assert abs(math.sinh(tile_radii(6, 10)[1]) - PHI) < 1e-12
    # "{5,4} with qubits: 1.4907 S" (the section's own 1e-3 window)
    assert abs(qubit_bond_ratio(5, 4) - 1.4907) < 1e-3


# ── section 43: the three columns and why they did not fit ─────────────
def collision_count(slope: float) -> int:
    """Pairs of [-60, 60]^2 collapsed by the projection of slope ``slope``."""
    seen: set[float] = set()
    count = 0
    for m in range(-60, 61):
        for k in range(-60, 61):
            value = round(m + k * slope, 9)
            if value in seen:
                count += 1
            seen.add(value)
    return count


def binet_tile_deviations() -> tuple[float, ...]:
    """``|F_{s+4} - phi^4 S/(sqrt5 pi)| - phi^{-(s+4)}/sqrt5``, for s = 0..24."""
    fib = [0, 1]
    for _ in range(40):
        fib.append(fib[-1] + fib[-2])
    out = []
    for s in range(25):
        entropy = math.pi * PHI**s
        dev = fib[s + 4] - PHI**4 * entropy / (math.sqrt(5) * math.pi)
        out.append(abs(abs(dev) - PHI ** -(s + 4) / math.sqrt(5)))
    return tuple(out)


def bragg_chain() -> np.ndarray:
    """The cut-and-project chain of the Fibonacci word: N = 46368 points."""
    word = "A"
    for _ in range(22):
        word = "".join("AB" if ch == "A" else "A" for ch in word)
    positions = np.concatenate([[0], np.cumsum([PHI if ch == "A" else 1.0
                                                for ch in word])])[:-1]
    return positions


def bragg_amplitudes() -> dict[tuple[int, int], float]:
    """Fourier amplitudes of the chain at the module points (section 43)."""
    positions = bragg_chain()

    def amplitude(k: float) -> float:
        return float(abs(np.exp(2j * math.pi * k * positions).sum()) / len(positions))

    divisor = PHI + 2
    return {(m, n): amplitude((m + n * PHI) / divisor)
            for m, n in ((2, 3), (1, 2), (1, 1))}


def random_bragg_level() -> float:
    """The largest amplitude at 200 random points, seed 1 (section 43)."""
    positions = bragg_chain()
    rng = np.random.default_rng(1)
    return max(float(abs(np.exp(2j * math.pi * k * positions).sum()) / len(positions))
               for k in rng.uniform(0.05, 2.5, 200))


# ══════════════════════════════════════════════════════════ section 39 ══
class TestSection39FibonacciTiling:
    """section 39 -- 'The throat with the Fibonacci tiling of its rings (Figure 4)'"""

    @staticmethod
    def words(n=7):
        return ring_words(n)

    @staticmethod
    def bounds(w):
        return ring_bounds(w)

    @pytest.mark.parametrize(
        "s,a,b",
        [(0, 2, 1), (1, 3, 2), (2, 5, 3), (3, 8, 5), (4, 13, 8), (5, 21, 13),
         (6, 34, 21)],
    )
    def test_tile_counts_are_fibonacci(self, s, a, b):
        """A_sigma long and B_sigma short tiles: F_{s+3} and F_{s+2}."""
        w = self.words()[s]
        assert (w.count("A"), w.count("B")) == (a, b), s

    @pytest.mark.parametrize("s", range(7))
    def test_weighted_sum_is_the_entropy(self, s):
        """S = pi (A/phi^2 + B/phi^3) = pi phi^s exactly (rel. 1e-12)."""
        w = self.words()[s]
        a, b = w.count("A"), w.count("B")
        weighted = math.pi * (a / PHI**2 + b / PHI**3)
        assert weighted == pytest.approx(math.pi * PHI**s, rel=1e-12), s

    @pytest.mark.parametrize("s", range(6))
    def test_boundaries_nest(self, s):
        """Every boundary of ring s is a boundary of ring s+1 (they nest)."""
        b0, b1 = self.bounds(self.words()[s]), self.bounds(self.words()[s + 1])
        assert all(np.min(np.abs(b1 - x)) < 1e-12 for x in b0), s

    @pytest.mark.parametrize("s,printed",
                             [(0, 3), (1, 5), (2, 8), (3, 13), (4, 21), (5, 34),
                              (6, 56)])
    def test_mode_count_is_floor_of_s(self, s, printed):
        assert math.floor(math.pi * PHI**s) == printed, s

    @pytest.mark.figure
    def test_section39_draws_figure_four(self):
        """Figure 4: the section's statements hold and the artifact is pinned.

        Section 39 used to run here through the section-run fixture and
        this test read its ``S = pi(A/phi^2+B/phi^3) exact; boundaries
        nested`` line back from stdout; the statements now live in
        ``fibonacci_tiling_statements`` and fail on their values
        (SPEC-002 §1).  The drawing belongs to ``pnpm run figures``
        (SPEC-002 §1.1), so only the committed bytes are verified here.
        """
        fibonacci_tiling_statements()
        # section 39 checks figure 4 but no longer draws it (SPEC-002 §1.1)
        verify_figure_artifact("fig_throat_tiling.pdf")


# ══════════════════════════════════════════════════════════ section 40 ══
class TestSection40DictionaryAgainstTheCusp:
    """section 40 -- 'The dictionary on a regular tiling against the cusp'"""

    @pytest.mark.parametrize(
        "s,legs",
        [(0, 7), (1, 14), (2, 28), (3, 35), (4, 56), (5, 84), (6, 133),
         (7, 217), (8, 350), (9, 567), (10, 938), (11, 1484), (12, 2443)],
    )
    def test_open_legs_of_73(self, s, legs):
        """Open legs the {7,3} boundary cuts at each level (Crofton).

        ``open_legs_of_seven_three`` builds the tiling and counts the
        crossings here; the section used to print the thirteen numbers
        and this test parsed them out of its stdout (SPEC-002 §1).
        """
        got = open_legs_of_seven_three()
        assert got[s] == legs, (s, got)

    def test_crofton_constant(self):
        """Legs/S fluctuates about the constant 2.4097 of the tiling.

        ``dictionary_statements`` carries the rest of section 40's own
        checks -- the cusp, the prototiles, the substitutions, the
        60-digit identity, the statements of the 1/2 and the points of
        Z[i] -- which had no stdout left to live in (SPEC-002 §1).
        """
        constant = crofton_constant()
        assert round(constant, 4) == 2.4097, constant
        dictionary_statements()

    @pytest.mark.parametrize(
        "s,pairs,best",
        [(0, 172, (20, 3, 3)), (1, 22, None), (2, 2, None), (3, 1, None),
         (4, 0, None)],
    )
    def test_pairs_that_give_s_on_average(self, s, pairs, best):
        """Of the 50340 (tiling, chi) pairs only 172 give S within 1%.

        ``closest_pair_scan`` runs the scan the section ran and returns
        its totals; the three numbers this test used to read back from
        stdout -- the total, the column of counts and the best pair with
        its distance -- are asserted on their values (SPEC-002 §1).
        """
        total, counts, best_pair, distance = closest_pair_scan()
        assert total == 50340, total
        assert counts[s] == pairs, counts
        if best is not None:
            assert best_pair == best, best_pair
            # "best (20, 3, 3) at 3.34e-06": half a unit of the last digit
            assert distance == pytest.approx(3.34e-06, abs=5e-09), distance

    def test_unweighted_count_tends_to_a_fixed_fraction(self):
        """F_{s+4} -> 0.9757 S: the limit is phi^4/(sqrt5 pi)."""
        limit = PHI**4 / (math.sqrt(5) * math.pi)
        assert round(limit, 4) == 0.9757, limit

    @pytest.mark.parametrize("power,printed", [(2, 3.32), (3, 2.099)])
    def test_equivalent_bond_dimensions(self, power, printed):
        """e^(pi/phi^2) = 3.32 and e^(pi/phi^3) = 2.099 are not integers."""
        got = math.exp(math.pi / PHI**power)
        assert round(got, 3) == printed, (power, got)

    @pytest.mark.parametrize("s,area", [(1.483259, 2 * math.pi / PHI**3)])
    def test_two_prototiles_keep_their_areas(self, s, area):
        """The long prototile has area 2pi/phi^3, the short one is that / phi."""
        # both literals carry six decimals, so each has a half unit of 5e-7
        assert abs(s - area) <= 5e-7
        assert abs(area / PHI - 0.916704) <= 5e-7

    def test_distinct_arc_weights_of_73(self):
        """{7,3} needs 115 distinct arc weights over sigma = 0..9, the throat 2.

        ``arc_weights_of_seven_three`` cuts the level circles into arcs
        and weighs them here; the section printed the column of ten
        counts and the total, and both are asserted on their values
        (SPEC-002 §1).
        """
        per_level, total = arc_weights_of_seven_three()
        assert per_level == (1, 2, 3, 3, 5, 7, 10, 16, 27, 41), per_level
        assert total == 115, total

    @pytest.mark.parametrize(
        "s,count,floor_s",
        [(0, 5, 3), (3, 13, 13), (6, 57, 56)],
    )
    def test_lattice_points_again(self, s, count, floor_s):
        """Section 40 repeats the Z[i] count of section 12 (same numbers)."""
        r2 = PHI**s
        c = sum(1 for a in range(-20, 21) for b in range(-20, 21)
                if a * a + b * b <= r2)
        assert c == count, (s, c)
        assert math.floor(math.pi * PHI**s) == floor_s


# ══════════════════════════════════════════════════════════ section 41 ══
class TestSection41FiveRegularTilings:
    """section 41 -- 'Five regular tilings against the levels (Figure 5)'"""

    def test_circumradius_inradius_and_edge(self):
        """cosh e = phi for {5,4}, sinh r = phi for {6,10} (exact)."""
        e = 2 * math.acosh(math.cos(math.pi / 5) / math.sin(math.pi / 4))
        assert math.cosh(e) == pytest.approx(PHI, abs=1e-10)
        r = math.acosh(math.cos(math.pi / 10) / math.sin(math.pi / 6))
        assert math.sinh(r) == pytest.approx(PHI, abs=1e-10)

    @pytest.mark.parametrize("n", [15, 20, 25])
    def test_hurwitz_constant_of_phi(self, n):
        """|phi - F_{n+1}/F_n| F_n^2 -> 1/sqrt5 = 0.44721.

        n is kept in 15..25: below it the convergent has not converged, above
        it the product loses float64 precision (at n = 40 it underflows to 0).

        main.tex quotes 1.00000/(sqrt5 q^2) at q = F_29 next to this
        testref; the manuscript used to quote 0.99990 there, which is
        section 41's float64 cancellation (it prints 0.999902), not the
        value of the ratio -- see test_the_hurwitz_ratio_at_f_29_exactly,
        which computes it in 60 digits.  This test asserts the law the
        sentence is about, the constant 1/sqrt5.
        """
        f = [0, 1]
        for _ in range(n + 3):
            f.append(f[-1] + f[-2])
        q, p = f[n + 1], f[n + 2]
        const = abs(PHI - p / q) * q * q
        assert const == pytest.approx(1 / math.sqrt(5), abs=1e-5), (n, const)

    def test_the_hurwitz_ratio_at_f_29_exactly(self):
        """sqrt5 q^2 |phi - p/q| at q = F_29 and F_30, in 60 digits: 1.00000.

        main.tex writes ``1.00000/(sqrt5 q^2) at q = F_29`` beside the
        testref above; it used to quote 0.99990, which is section 41's
        float64 cancellation -- it prints 0.999902 there because float64
        cancels ``1.618... - p/q`` down to ~6e-13, whose own noise is ~3e-4
        of it.  Both readings of the index (q = F_29 = 514229 and the
        F_30 = 832040 that section 41's shifted list prints) give 1.00000
        exactly, so the old figure was the cancellation, not the ratio.
        Nothing is loosened here: this test states the exact value so the
        discrepancy stays visible in the suite.
        """
        with localcontext() as ctx:
            ctx.prec = 60
            sqrt5 = Decimal(5).sqrt()
            phi = (1 + sqrt5) / 2
            f = [0, 1]
            for _ in range(31):
                f.append(f[-1] + f[-2])
            for k in (29, 30):
                q, p = Decimal(f[k]), Decimal(f[k + 1])
                ratio = abs(phi - p / q) * sqrt5 * q * q
                assert round(ratio, 5) == 1.00000, (k, ratio)

        # the float64 cancellation of section 41, now shared with the
        # statements of the section (SPEC-002 §1)
        assert round(hurwitz_float64_deviations()[-1], 6) == 0.999902

    @pytest.mark.parametrize("n", [5, 10, 15])
    def test_hurwitz_constant_of_sqrt2(self, n):
        """sqrt(2) has constant 1/(2 sqrt2) = 0.35355 < 1/sqrt5."""
        p, q = 1, 1
        for _ in range(n):                 # convergents of [1;2,2,2,...]
            p, q = p + 2 * q, p + q
        const = abs(math.sqrt(2) - p / q) * q * q
        assert const == pytest.approx(1 / (2 * math.sqrt(2)), abs=5e-5), (n, const)
        assert const < 1 / math.sqrt(5)

    @pytest.mark.parametrize(
        "tiling,printed",
        [((7, 3), 2.618), ((3, 7), 1.6), ((5, 4), 2.618), ((12, 5), 10.824),
         ((6, 10), 4.992)],
    )
    def test_layer_growth(self, tiling, printed):
        """Only {7,3} and {5,4} grow by phi^2 per layer (the level step).

        ``layer_growth`` grows the five tilings of figure 5 layer by
        layer here; the section printed the dictionary of five ratios and
        this test parsed it out of stdout (SPEC-002 §1), at the three
        decimals it rounded them to.
        """
        growth = layer_growth()
        assert round(growth[tiling], 3) == printed, (tiling, growth[tiling])

    @pytest.mark.parametrize(
        "tiling,series",
        [
            ((7, 3), [1, 8, 8, 29, 29, 57, 99]),
            ((12, 5), [1, 1, 1, 1, 1, 1, 1]),
            ((6, 10), [1, 1, 1, 1, 7, 7, 7]),
        ],
    )
    def test_tiles_inside_the_disc(self, tiling, series):
        """Tiles whose centre falls inside each disc of the level (figure 5).

        ``disc_tile_records`` builds the tiling and counts the tiles
        whose centre is within the radius of each level; the section
        printed one list per tiling and this test read them off stdout
        (SPEC-002 §1).
        """
        counts, _tangencies = disc_tile_records(*tiling)
        assert list(counts) == series, (tiling, counts)

    @pytest.mark.slow
    def test_section41_prints_its_conclusions(self):
        """The conclusions section 41 printed, on their values (figure 5).

        The section used to run here and this test read four lines off
        its stdout; ``tilings_strip_statements`` carries the whole body
        of section 41 now -- the counts of figure 5, the tangency of the
        boundaries, the Hurwitz constants, the layers of {3,7}, the
        growth per layer, the two exact radii and the qubit reading
        (SPEC-002 §1).  The drawing belongs to ``pnpm run figures``
        (SPEC-002 §1.1), so only the committed bytes are verified here.
        """
        tilings_strip_statements()
        # section 41 checks figure 5 but no longer draws it (SPEC-002 §1.1)
        verify_figure_artifact("fig_tilings_strip.pdf")

    @pytest.mark.slow
    def test_qubit_bond_dimension_of_54(self):
        """One qubit per bond on {5,4} gives 1.4907 S (main.tex quotes it).

        ``qubit_bond_ratio`` computes the number the section printed at
        four decimals; the section's own 1e-3 window is asserted in
        ``tilings_strip_statements``, this test keeps the tighter window
        the value used to be read back with.
        """
        ratio = qubit_bond_ratio(5, 4)
        assert round(ratio, 4) == 1.4907, ratio


# ══════════════════════════════════════════════════════════ section 42 ══
class TestSection42TwoCoordinatesAndTheStep:
    """section 42 -- 'The two coordinates, the level step, the orthogonalization, the rational step and the imp:A1 operator'"""

    F = [0, 1] + [0] * 40

    @classmethod
    def fib(cls):
        f = [0, 1]
        for _ in range(40):
            f.append(f[-1] + f[-2])
        return f

    @pytest.mark.parametrize("s", [1, 2, 3, 6, 12])
    def test_phi_to_the_s_is_a_unit(self, s):
        """phi^s = a + b phi with norm (-1)^s, and M|a + b phi_bar| = M phi^-s.

        The second coordinate is the weld time tau(s) of main.tex.
        """
        f = self.fib()
        a, b = f[s - 1], f[s]
        assert a * a + a * b - b * b == (-1) ** s
        psi = (1 - 5 ** 0.5) / 2                      # Galois conjugate of phi
        m = 6 * math.sqrt(3) * math.pi / LN_PHI
        assert abs(m * abs(a + b * psi) - m * PHI**-s) < 1e-9, s

    def test_weld_time_at_the_bottom(self):
        """tau(12) = M_PCF phi^-12 = 0.2107 (main.tex: 'at the bottom, tau(12)=0.2107')."""
        assert M_PCF * PHI**-12 == pytest.approx(0.2107, abs=5e-5)

    @staticmethod
    def sub(w):
        return "".join("AB" if c == "A" else "A" for c in w)

    @pytest.mark.parametrize("s,counts", [(0, (1, 2)), (5, (8, 13)), (11, (144, 233))])
    def test_ring_word_is_the_fibonacci_rotations(self, s, counts):
        """I3: (B, A) = (F_{s+2}, F_{s+3}) in the word of ring s."""
        w = "AAB"
        f = self.fib()
        for _ in range(s):
            w = self.sub(w)
        assert (w.count("B"), w.count("A")) == (f[s + 2], f[s + 3]), s

    def test_substitution_matrix_is_exchange_times_shift(self):
        """I2: [[0,1],[1,0]] [[1,0],[1,1]] = [[1,1],[1,0]] (A -> AB, B -> A)."""
        ex, sh = [[0, 1], [1, 0]], [[1, 0], [1, 1]]
        prod = [[sum(ex[i][k] * sh[k][j] for k in range(2)) for j in range(2)]
                for i in range(2)]
        assert prod == [[1, 1], [1, 0]]

    @pytest.mark.parametrize("p,expected", [(0.3, 0.4), (0.5, 0.0), (0.7, 0.4)])
    def test_orthogonalisation_at_the_half_turn(self, p, expected):
        """I4: |1 - p + p e^{i pi}| = |1 - 2p| vanishes only at p = 1/2."""
        ov = abs((1 - p) + p * complex(math.cos(math.pi), math.sin(math.pi)))
        assert ov == pytest.approx(expected, abs=1e-12)
        assert (ov < 1e-12) == (p == 0.5)

    @pytest.mark.parametrize(
        "p,q,dev_bg,dev_obs",
        [(21, 13, 0.8, 71.2), (34, 21, 0.3, 27.1), (55, 34, 0.1, 10.4),
         (89, 55, 0.0, 4.0), (144, 89, 0.0, 1.5), (233, 144, 0.0, 0.6)],
    )
    def test_rational_step_versus_the_contrast(self, p, q, dev_bg, dev_obs):
        """I5: a rational step p/q moves the background and the observer level."""
        f = LN_PHI / math.log(p / q)
        bg = abs(11.97 * f - 11.97) / 0.05
        obs = abs(583.789 * f - 583.789) / 0.028
        assert round(bg, 1) == dev_bg, (p, q, bg)
        assert round(obs, 1) == dev_obs, (p, q, obs)

    def test_three_sigma_criterion(self):
        """From 144/89 on the reading stays within 3 sigma of the golden one."""
        devs = []
        for p, q in [(21, 13), (34, 21), (55, 34), (89, 55), (144, 89),
                     (233, 144)]:
            f = LN_PHI / math.log(p / q)
            devs.append(abs(583.789 * f - 583.789) / 0.028)
        assert devs[0] > 70
        assert devs[3] > 3
        assert devs[4] < 3
        assert all(d < 3 for d in devs[4:])

    @pytest.mark.parametrize(
        "s,norm", [(1, -1), (2, 1), (3, -1), (4, 1), (5, -1), (6, 1)]
    )
    def test_alternating_norm(self, s, norm):
        f = self.fib()
        a, b = f[s - 1], f[s]
        assert a * a + a * b - b * b == norm

    def test_trace_three_and_the_shortest_geodesic(self):
        """I6: tr = phi^2 + phi^-2 = 3, and 2 arccosh(3/2) = 4 log phi = 1.924847."""
        assert PHI**2 + PHI**-2 == pytest.approx(3.0, abs=1e-12)
        assert 2 * math.acosh(1.5) == pytest.approx(4 * LN_PHI, abs=1e-12)
        assert round(2 * math.acosh(1.5), 6) == 1.924847

    @pytest.mark.parametrize(
        "n,printed",
        [(0, 1.99), (1, 1.48), (2, 1.31), (4, 1.17), (5, 1.13), (11, 1.02)],
    )
    def test_mass_ratios_of_imp_a1(self, n, printed):
        """I7: successive mass ratios of imp:A1 at n = 6; none of them is phi."""
        nlev = 6
        m = [2 * math.sin(k * math.pi / (4 * (nlev + 1))) / LN_PHI
             for k in range(1, 2 * nlev + 2)]
        r = [m[k + 1] / m[k] for k in range(len(m) - 1)]
        assert round(r[n], 2) == printed, (n, r[n])
        assert all(abs(x - PHI) > 0.05 for x in r)


# ══════════════════════════════════════════════════════════ section 43 ══
class TestSection43ThreeColumns:
    """section 43 -- 'The three columns and why they did not fit'"""

    @pytest.mark.parametrize("slope,printed", [(1.5, 14042), (PHI, 0)])
    def test_rational_step_has_a_kernel(self, slope, printed):
        """A step p/q collapses pairs of Z^2; phi collapses none (Lean:
        rational_step_kernel, golden_rotation_aperiodic)."""
        assert collision_count(slope) == printed, slope

    def test_the_three_columns_of_irrational_unimodular_pisot(self):
        """R11: two-letter primitive substitutions with entries <= 3."""
        ok123, ok4 = set(), set()
        for a, b, c, d in itertools.product(range(4), repeat=4):
            if b == 0 or c == 0:
                continue
            tr, de = a + d, a * d - b * c
            disc = tr * tr - 4 * de
            if disc <= 0:
                continue
            r = math.sqrt(disc)
            lam, mu = (tr + r) / 2, (tr - r) / 2
            if int(round(r)) ** 2 != disc and abs(de) == 1 and abs(mu) < 1:
                ok123.add(round(lam, 4))
                if (tr, de) == (1, -1):
                    ok4.add(round(lam, 4))
        assert round(1 + 2 ** 0.5, 4) in ok123
        assert ok4 == {round(PHI, 4)}, ok4
        assert sorted(ok123) == [1.618, 2.4142, 2.618, 3.3028, 3.7321, 4.2361]

    def test_cube_diagonal_projection(self):
        """The three projected axes have length sqrt(2/3) at 120 degrees."""
        n = np.array([1, 1, 1]) / 3 ** 0.5
        p = [e - (e @ n) * n for e in np.eye(3)]
        ang = {
            round(math.degrees(math.acos(
                p[i] @ p[j] / (np.linalg.norm(p[i]) * np.linalg.norm(p[j]))
            )), 6)
            for i, j in [(0, 1), (1, 2), (0, 2)]
        }
        assert ang == {120.0}
        assert np.allclose(sum(p), 0)
        assert np.linalg.norm(p[0]) == pytest.approx(math.sqrt(2 / 3), abs=1e-12)

    def test_binet_deviation_of_the_tile_count(self):
        """F_{s+4} - phi^4 S/(sqrt5 pi) = +- phi^{-(s+4)}/sqrt5 for s = 0..24.

        ``binet_tile_deviations`` computes the twenty-five residuals the
        section asserted one by one with its own 1e-6 window.
        """
        for s, residual in enumerate(binet_tile_deviations()):
            assert residual < 1e-6, s

    @pytest.mark.parametrize("n,printed", [((2, 3), 0.95), ((1, 2), 0.88),
                                           ((1, 1), 0.70)])
    def test_bragg_peaks_of_the_fibonacci_chain(self, n, printed):
        """Fourier amplitudes of the cut-and-project chain: 0.95, 0.88, 0.70
        at the module points, at most 0.010 at random ones (N = 46368)."""
        assert len(bragg_chain()) == 46368
        got = bragg_amplitudes()[n]
        assert round(got, 2) == printed, (n, got)

    def test_bragg_random_level(self):
        rnd = random_bragg_level()
        assert round(rnd, 3) == 0.010, rnd
        assert rnd < 0.02

    @pytest.mark.parametrize(
        "block",
        [
            "slope 3/2 -> 14042 collisions; slope phi -> 0",
            "tile count: F_{s+4} - 0.9757 S",
            "Bragg (N = 46368): (2,3) 0.95, (1,2) 0.88, (1,1) 0.70",
        ],
    )
    def test_section43_stdout(self, block):
        """The three lines section 43 printed, on their values (SPEC-002 §1).

        Each id is the claim the section printed; the computation behind
        it is the one the claim test of that number owns, so nothing is
        asserted twice from two different codes.
        """
        if block.startswith("slope"):
            # "slope 3/2 -> 14042 collisions; slope phi -> 0"
            assert (collision_count(1.5), collision_count(PHI)) == (14042, 0)
        elif block.startswith("tile count"):
            # "tile count: F_{s+4} - 0.9757 S = +-phi^-(s+4)/sqrt5, s = 0..24"
            assert max(binet_tile_deviations()) < 1e-6
        else:
            # "Bragg (N = 46368): (2,3) 0.95, (1,2) 0.88, (1,1) 0.70;
            #  200 random points: max 0.010"
            peaks = bragg_amplitudes()
            assert [round(peaks[k], 2) for k in ((2, 3), (1, 2), (1, 1))] \
                == [0.95, 0.88, 0.70]
            assert round(random_bragg_level(), 3) == 0.010
