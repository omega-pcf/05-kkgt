"""Sections 17-24, moved out of ``_rest`` (SEC-001, layer 2, lot 1).

They are the bodies of ``seccion_17`` … ``seccion_24`` verbatim; the
registry is assembled by ``kkgt.sections.__init__``.
"""

from ..constants import (
    M_GEV,
    M_KOIDE_MEV,
    M_PLANCK_GEV,
    M_TAU_MEV,
)
from ._rest import _C, _LamP   # shared with _rest: single origin (kkgt.constants / kkgt.harness)

SECCIONES = []

# ======================================================================
# 17. The observer level from the value of Lambda, below (F9) and the unit of (F1)
# ======================================================================
def seccion_17():
    import math, random
    phi = (1 + 5 ** 0.5) / 2
    L = math.log(phi)
    u = M_KOIDE_MEV * 1e6 / (6 * 3 ** 0.5 * math.pi / L)        # eV, the unit of (F1)
    hbar, Mpc = 6.582119569e-16, 3.0856775814913673e19   # eV s, km
    def sigma_obs(H0, OL):                              # Lambda = 3 H0^2 Omega_L, curvatura
        lam = 3 * (hbar * H0 / Mpc) ** 2 * OL
        return math.log(6 * u ** 2 / lam) / L
    random.seed(1)
    v = [sigma_obs(random.gauss(67.36, 0.54), random.gauss(0.6847, 0.0073)) for _ in range(200000)]
    m = sum(v) / len(v); sd = (sum((x - m) ** 2 for x in v) / len(v)) ** 0.5
    print(f"unit of (F1): {u/1e6:.4f} MeV")
    print(f"sigma_obs = {sigma_obs(67.36, 0.6847):.3f} +- {sd:.3f}  (Planck 2018: H0 = 67.36 +- 0.54, Omega_L = 0.6847 +- 0.0073)")

SECCIONES.append((17, 'The observer level from the value of Lambda, below (F9) and the unit of (F1)', seccion_17))

# ======================================================================
# 18. The observer level and the unit of the curvature
# ======================================================================
def seccion_18():
    import math, random
    phi = (1 + 5 ** 0.5) / 2; L = math.log(phi)
    u = M_KOIDE_MEV * 1e6 / (6 * 3 ** 0.5 * math.pi / L)      # eV, unit of (F1)
    M = M_KOIDE_MEV * 1e6; MP = M_PLANCK_GEV * 1e9                    # eV
    hbar, Mpc_km = 6.582119569e-16, 3.0856775814913673e19
    lP2, c, Mpc_m = (1.616255e-35) ** 2, 2.99792458e8, 3.0856775814913673e22
    def readings(H0, OL):
        lam_eV2 = 3 * (hbar * H0 / Mpc_km) ** 2 * OL                 # curvature, eV^2
        s_curv = math.log(6 * u ** 2 / lam_eV2) / L                  # W8, unit of (F1)
        lam_m = 3 * (H0 * 1e3 / Mpc_m) ** 2 * OL / c ** 2            # m^-2
        S = 3 * math.pi / (lam_m * lP2)                              # de Sitter entropy
        s_ent = math.log(S / math.pi) / L                            # W4, dimensionless
        return s_curv, s_ent, S
    random.seed(2)
    v = [readings(random.gauss(67.36, 0.54), random.gauss(0.6847, 0.0073)) for _ in range(100000)]
    def ms(i):
        x = [t[i] for t in v]; m = sum(x) / len(x); return m, (sum((y - m) ** 2 for y in x) / len(x)) ** 0.5
    sc, se, S = readings(67.36, 0.6847)
    print(f"observer level (W4 = W8 in the gravitational unit l = sqrt2 l_P): sigma = {se:.3f} +- {ms(1)[1]:.3f};  S = {S:.3e}")
    print(f"the same curvature measured in the particle unit (F1), removed: {sc:.3f}; difference {se - sc:.3f} = 2 log_phi(M_Pl/u) - log_phi 2 = {2*math.log(MP/u)/L - math.log(2)/L:.3f}, a unit conversion")
    print(f"Lambda(sigma) S(sigma) = 6 pi = 3 pi / G_N with G_N = 1/2:", abs(6*phi**-7.3*math.pi*phi**7.3 - 6*math.pi) < 1e-12)

SECCIONES.append((18, 'The observer level and the unit of the curvature', seccion_18))

# ======================================================================
# 19. The phase offset of the tower: exact zeros against the asymptotic form, and the Maldacena–Qi form
# ======================================================================
def seccion_19():
    import math
    from scipy.special import jn_zeros
    j = jn_zeros(1, 8)
    print("k  j_1,k/pi - k   (asymptote 1/4 = 1/d at d = 4; the exact k = 0 is j_1,0 = 0)")
    print("0  exact: j_1,0 = 0;  the asymptote would give 0.25")
    for k, x in enumerate(j, 1):
        print(f"{k}  {x/math.pi - k:.4f}")
    for d in range(2, 9):
        print(f"d = {d}: d/4 - 3/4 = {d/4-0.75:+.3f},  1/d = {1/d:.3f}", "  iguales" if abs(d/4-0.75-1/d) < 1e-12 else "")
    print("Maldacena-Qi: E_n = t'(n + 1/4); tower: m_k ~ pi M phi^12 (k + 1/4), with k = 0 replaced by the zero mode")

SECCIONES.append((19, 'The phase offset of the tower: exact zeros against the asymptotic form, and the Maldacena–Qi form', seccion_19))

# ======================================================================
# 20. The contrast with the two observed candidates (380 and 700 GeV)
# ======================================================================
def seccion_20():
    import math
    from scipy.special import jn_zeros
    phi = (1 + 5 ** 0.5) / 2; M = M_GEV
    j = jn_zeros(1, 6)
    def fit(m, e):
        w = [1 / x ** 2 for x in e]; mu = j[:len(m)]
        lam = sum(a * b * c for a, b, c in zip(w, m, mu)) / sum(a * c * c for a, c in zip(w, mu))
        dl = 1 / math.sqrt(sum(a * c * c for a, c in zip(w, mu)))
        return math.log(lam / M) / math.log(phi), dl / lam / math.log(phi)
    s, ds = fit([380, 700], [20, 20])
    print(f"two data points: sigma_IR = {s:.2f} +- {ds:.2f}  ({abs(s-12)/ds:.1f} standard deviations from 12)")
    print(f"ratio 700/380 = {700/380:.3f};  j_1,2/j_1,1 = {j[1]/j[0]:.3f}")
    print("predictions with sigma = 12 (GeV):", [round(x * M * phi ** 12) for x in j[2:6]], " against RS (LYR): 1000, 1322")

SECCIONES.append((20, 'The contrast with the two observed candidates (380 and 700 GeV)', seccion_20))

# ======================================================================
# 21. The two-brane rival fitted to the same two candidates
# ======================================================================
def seccion_21():
    import math
    from scipy.special import jn_zeros
    phi = (1 + 5 ** 0.5) / 2; M = M_GEV
    j = jn_zeros(1, 4); m, e = [380, 700], [20, 20]
    w = [1 / x ** 2 for x in e]
    lam = sum(a * b * c for a, b, c in zip(w, m, j)) / sum(a * c * c for a, c in zip(w, j))
    lg = M * phi ** 12
    print(f"fitted free scale: {lam:.2f} GeV -> modes 3 and 4: {j[2]*lam:.0f}, {j[3]*lam:.0f} GeV")
    print(f"throat (sigma = 12): {lg:.2f} GeV -> {j[2]*lg:.0f}, {j[3]*lg:.0f} GeV; difference {100*(lg/lam-1):.1f} %")
    print(f"split: {j[2]*(lg-lam):.0f} and {j[3]*(lg-lam):.0f} GeV, against the +-30 and +-40 GeV assumed in section 2")

SECCIONES.append((21, 'The two-brane rival fitted to the same two candidates', seccion_21))

# ======================================================================
# 22. The unit of the curvature and the observer level
# ======================================================================
def seccion_22():
    import math
    phi = (1 + 5 ** 0.5) / 2; L = math.log(phi); GN = 0.5
    lp = _LamP(67.36, 0.6847)
    s_l = math.log(6 / (lp / GN)) / L; s_S = math.log(3 / lp) / L; s_cw6 = math.log(6 / lp) / L
    print(f"l = l_P/sqrt(G_N) = {1/math.sqrt(GN):.4f} l_P (I12, tau = i)")
    print(f"W8 in unit l: {s_l:.3f};  W4: {s_S:.3f}  (equal because Lambda S = 6 pi)")
    print(f"sigma-obs eq. of CW6 (Lambda in l_P with the 6 of G_N = 1/2): {s_cw6:.3f} = W4 + log_phi 2")
    for name, H0, OL in [("Planck 2018", 67.36, 0.6847), ("SH0ES, fixed omega_m", 73.04, 1 - 0.1430 / 0.7304 ** 2)]:
        print(f"  {name:20s}: sigma_obs = {math.log(3/_LamP(H0, OL))/L:.3f}")

SECCIONES.append((22, 'The unit of the curvature and the observer level', seccion_22))

# ======================================================================
# 23. The lattice: units of Z[phi], the background and the observer
# ======================================================================
def seccion_23():
    import math
    phi = (1 + 5 ** 0.5) / 2; L = math.log(phi); F = [0, 1]
    for _ in range(30): F.append(F[-1] + F[-2])
    for n in (1, 2, 3, 6, 12):
        a, b = F[n - 1], F[n]
        print(f"  phi^{n} = {a} + {b} phi, norm {a*a + a*b - b*b:+d}")
    print("background: 11.97 +- 0.05 against lattice point 12 (0.6 standard deviations)")
    wm = 0.1430
    def H0_for(n, mode):
        lo, hi = 40.0, 120.0
        for _ in range(100):
            h = (lo + hi) / 2; OL = 1 - wm / (h / 100) ** 2 if mode == 'wm' else 0.6847
            if math.log(3 / _LamP(h, OL)) / L > n: lo = h
            else: hi = h
        return h
    for n in (583, 584, 585):
        print(f"  observer at point {n}: H0 = {H0_for(n,'wm'):.2f} (omega_m fijo), {H0_for(n,'OL'):.2f} (Omega_Lambda fijo)")
    h = H0_for(584, 'wm')
    print(f"  584: {(h-67.36)/0.54:+.1f} sigma from Planck (67.36 +- 0.54), {(h-73.04)/1.04:+.1f} sigma from SH0ES (73.04 +- 1.04)")

SECCIONES.append((23, 'The lattice: units of Z[phi], the background and the observer', seccion_23))

# ======================================================================
# 24. The two dimensionful data and the top
# ======================================================================
def seccion_24():
    import math
    phi = (1 + 5 ** 0.5) / 2; L = math.log(phi)
    GeVJ = 1.602176634e-10
    MPl = math.sqrt(_C['hbar'] * _C['c'] ** 5 / _C['G']) / GeVJ
    me, mmu, mtau = 0.51099895, 105.6583755, M_TAU_MEV
    M = (math.sqrt(me) + math.sqrt(mmu) + math.sqrt(mtau)) ** 2 / 9 / 1e3
    Mpcf = 6 * math.sqrt(3) * math.pi / L; u = M / Mpcf
    r = 2 * math.log(MPl * math.sqrt(0.5) / u) / L
    print(f"M = {M*1e3:.3f} MeV (Koide-Brannen), u = {u*1e3:.4f} MeV, M_Pl = {MPl:.5e} GeV")
    print(f"2 log_phi(l_u / l), l = sqrt2 l_P: {r:.3f}  (a {abs(r-round(r)):.2f} from the integer): the lattice does not fix the top")
    print(f"sigma_UV = log_phi(M_Pl/M) = {math.log(MPl/M)/L:.3f}")

SECCIONES.append((24, 'The two dimensionful data and the top', seccion_24))
