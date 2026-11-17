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
"""
import sys

from ..constants import (
    C_LIGHT,
    G_NEWTON,
    HBAR,
    MPC_M,
    M_GEV,
    M_KOIDE_MEV,
    M_PLANCK_GEV,
    M_TAU_MEV,
)
from ..harness import lam_planck

SECCIONES = []

# ======================================================================
# 1. Every number in order of appearance; alternatives for m0 (§10)
# ======================================================================
def seccion_1():
    """Recompute every number of kk_golden_throat.tex, in order of appearance.
    Python 3.13, NumPy 2.5.3, SciPy 1.18.1.  Run:  python -m kkgt.sections 1"""
    import numpy as np
    from scipy.linalg import eigh, expm, eigvalsh
    from scipy.special import jn_zeros, jv
    from scipy.optimize import brentq

    phi = (1 + 5**0.5) / 2; lp = np.log(phi)
    obs = np.array([380., 700, 1000, 1322])
    def resid(mu):                                   # Methods: residual
        lam = (obs @ mu) / (mu @ mu)
        return 100 * np.sqrt(np.mean(((obs - lam * mu) / obs) ** 2))
    def sl(a, b, M, kp, kw):                         # Methods: discretisation
        s = np.linspace(a, b, int(round((b - a) * M)) + 1); h = lp / M; n = len(s)
        p = phi ** (-kp * (s[:-1] + 0.5 / M)); K = np.zeros((n, n))
        for i in range(n - 1):
            K[i, i] += p[i]; K[i+1, i+1] += p[i]; K[i, i+1] -= p[i]; K[i+1, i] -= p[i]
        return eigh(K / h**2, trap(phi ** (-kw * s)), eigvals_only=True)
    def ratios(w): m = np.sqrt(np.clip(w, 0, None))[1:5]; return m / m[0], m
    def trap(v):                                     # half weight at the two end nodes
        v = np.array(v, dtype=float); v[0] /= 2; v[-1] /= 2; return np.diag(v)
    def P(tag, val): print(f"{tag:58s} {val}")

    print("== §1 data")
    P("data ratios (1, 1.842, 2.632, 3.479)", np.round(obs / obs[0], 3))
    j1 = jn_zeros(1, 4)
    P("J1 ratios (1, 1.831, 2.655, 3.477)", np.round(j1 / j1[0], 3))
    P("residual J1 (0.54%, abstract 0.5%)", round(resid(j1), 2))
    P("j_{1,k}/pi - k  (-> 1/4)", np.round(j1 / np.pi - np.arange(1, 5), 3))
    x = jn_zeros(1, 9); G = np.array([3, 20, 60, 130, 260, 440, 680, 1042, 1440.])
    P("LYR widths / 0.06x^3 (~1: they are the RS law)", np.round(G / (0.06 * x**3), 2))
    P("gluon m2/m1 range 8600/(3600..4000) (2.39..2.15)", (round(8600/3600, 2), round(8600/4000, 2)))

    print("== §3 tower operator (2), sigma = 0..6")
    N = 7; K = np.diag(np.full(N, 2.))
    for i in range(1, N): K[i, i-1] = -phi**2; K[i-1, i] = -phi**-2
    K /= lp**2; eta = np.diag(phi ** (-4. * np.arange(N)))
    P("eta K symmetric", np.allclose(eta @ K, (eta @ K).T))
    P("eta == e^{4A}, A=-sigma log phi", np.allclose(np.diag(eta), np.exp(-4 * np.arange(N) * lp)))
    for a in (0.05, 0.2, 1.0):
        T = expm(-a * K)
        P(f"a={a}: min eig sym(T) standard (+0.35,-0.06,-2.8)", f"{eigvalsh((T+T.T)/2).min():+.3f}")
        GT = eta @ T
        P(f"a={a}: min eig sym(eta T) (>0)", f"{eigvalsh((GT+GT.T)/2).min():.2e}")
    P("ring constant mode = -1/(log phi)^2 (-4.318)", round((2 - phi**2 - phi**-2) / lp**2, 3))

    print("== §4 spectrum of (sl)")
    w = sl(-6, 6, 32, 4, 2); r, m = ratios(w)
    P("sigma[-6,6], M=32 ratios (1.8308, 2.6545, 3.4757)", np.round(r, 4))
    P("lowest eigenvalue (1.3e-11)", f"{w[0]:.1e}")
    P("residual (0.54%)", round(resid(m), 2))
    r0, m0 = ratios(sl(0, 6, 32, 4, 2))
    P("sigma[0,6], M=32 residual (1.0%)", round(resid(m0), 2))
    P("  m2/m1 depth phi^6 vs J1 (diff ~0.6%)", f"{r0[1]:.4f} vs {j1[1]/j1[0]:.4f} ({100*(r0[1]/(j1[1]/j1[0])-1):.2f}%)")
    for a in (0, -6):
        P(f"one node per level, sigma[{a},6] residual (11-12%)", round(resid(ratios(sl(a, 6, 1, 4, 2))[1]), 1))
    def jzeros(nu, n=4):
        xs = np.linspace(0.5, 20, 4000); f = lambda t: jv(nu, t); out = []
        for u, v in zip(xs[:-1], xs[1:]):
            if f(u) * f(v) < 0: out.append(brentq(f, u, v))
        return np.array(out[:n])
    for d in (3, 4, 5, 6):
        P(f"d={d}: phase (d-3)/4={(d-3)/4}, residual (6.25,0.54,4.77,8.83)", round(resid(jzeros(d/2 - 1)), 2))

    print("== §5 look-elsewhere")
    rng = np.random.default_rng(1); q = np.exp(rng.uniform(np.log(1.3), np.log(4.5), 200000))
    grid = phi ** (np.arange(1, 9) / 2)
    P("P(within 1% of phi^{k/2}) (0.08)", round(np.mean(np.min(abs(q[:, None]/grid - 1), 1) < 0.01), 2))

    print("== §6 vector, M=24")
    for a in (0, -6, -24):
        rv, _ = ratios(sl(a, 6, 24, 2, 0))
        P(f"sigma[{a},6] m2/m1 (2.093, 2.171, 2.241)", round(rv[1], 3))
    j0 = jn_zeros(0, 2); P("J0 limit (2.295)", round(j0[1] / j0[0], 3))

    print("== §7 sectors")
    g1 = ratios(sl(-6, 6, 32, 4, 2))[1][0]; v1 = ratios(sl(-6, 6, 32, 2, 0))[1][0]
    for mg in (3600, 4000):
        P(f"gluon {mg}: log_phi(gluon/graviton scale) (5.39, 5.61)", round(np.log((mg/v1)/(380/g1)) / lp, 2))

    print("== Methods: assumed errors")
    for mm, dm in ((700, 20), (1000, 30), (1322, 40)):
        P(f"{mm}/380 error (0.11..0.21)", round(mm/380 * np.hypot(dm/mm, 20/380), 2))

    print("== §7 the scale (orientation e^A = phi^sigma)")
    def sl_r(a, b, M):                               # A = +w: stiffness e^{4A}, weight e^{2A}
        s = np.linspace(a, b, int(round((b - a) * M)) + 1); h = lp / M; n = len(s)
        p = phi ** (4 * (s[:-1] + 0.5 / M)); K = np.zeros((n, n))
        for i in range(n - 1):
            K[i, i] += p[i]; K[i+1, i+1] += p[i]; K[i, i+1] -= p[i]; K[i+1, i] -= p[i]
        return eigh(K / h**2, trap(phi ** (2 * s)), eigvals_only=True)
    for a in (0, 2, 4):
        w = sl_r(a, a + 12, 32); m = np.sqrt(w[1:5])
        P(f"[{a},{a+12}] m1/phi^sigma_IR (3.8319); ratios", (round(m[0]/phi**a, 4), np.round(m/m[0], 4)))
    M_lep = ((np.sqrt(0.51099895)+np.sqrt(105.6583755)+np.sqrt(M_TAU_MEV))/3)**2
    P("M (Koide) MeV (313.84)", round(M_lep, 2))
    err = np.array([20, 20, 30, 40.]); wgt = 1/err**2
    sc = np.sum(wgt*obs*j1)/np.sum(wgt*j1*j1); dsc = 1/np.sqrt(np.sum(wgt*j1*j1))
    sIR = np.log(sc*1000/M_lep)/lp
    P("scale GeV (99.1) ; sigma_IR (11.96 +- 0.03)", (round(sc, 2), round(sIR, 3), round(dsc/sc/lp, 3)))
    P("same number in powers of 2 (8.30)", round(np.log2(sc*1000/M_lep), 2))
    pred = j1*M_lep*phi**12/1000
    P("masses with sigma_IR=12 (387, 709, 1028, 1346)", np.round(pred))
    P("deviation of phi^12 scale (1.2 sigma)", round((M_lep*phi**12/1000 - sc)/dsc, 2))

    print("== Proposition: phi^12 is the half-turn of the 24-clock")
    def gmul(x, y, m): a, b = x; c, d = y; return ((a*c + b*d) % m, (a*d + b*c + b*d) % m)
    def gpow(n, m):
        r = (1, 0)
        for _ in range(n): r = gmul(r, (0, 1), m)
        return r
    def gorder(m):
        k, c = 1, (0, 1)
        while c != (1, 0): c = gmul(c, (0, 1), m); k += 1
        return k
    for N in (16, 9, 12, 24, 48, 72, 5):
        h = gpow(12, N)
        P(f"N={N}: clock (24 except 5:20); phi^12 order 2", (gorder(N), gmul(h, h, N) == (1, 0) and h != (1, 0), h))
    P("-1/zeta(-1) = 12 ; -2/zeta(-1) = 24", (-1/(-1/12), -2/(-1/12)))

    print("== Additions A-C")
    # A1 look-elsewhere for an integer level (fractional part of log_phi uniform for a random scale)
    rng2 = np.random.default_rng(2); u = rng2.uniform(0, 30, 200000)
    P("P(|log_phi(scale) - integer| < 0.04) (0.08)", round(np.mean(np.abs(u - np.round(u)) < 0.04), 3))
    # A2 pi face
    r = sc*1000/M_lep
    P("log_pi(scale/M) (5.03); pi^5 deviation (-1.9 sd)", (round(np.log(r)/np.log(np.pi), 3), round((np.pi**5 - r)/(dsc*1000/M_lep), 1)))
    # A3 gluon level on the phi ladder (deep throat, J0 first zero)
    j01 = jn_zeros(0, 1)[0]
    for mg in (3600, 4000):
        P(f"gluon {mg} GeV: log_phi(m1/(j01 M)) (17.6..17.8)", round(np.log(mg*1000/(j01*M_lep))/lp, 2))
    # B5 rigidity: unfolded spacing variance of the data vs GUE (Wigner surmise beta=2)
    sp = np.diff(obs); sp = sp/sp.mean()
    P("data unfolded spacing variance (~0)", round(np.var(sp), 4))
    P("GUE (beta=2) spacing variance 3pi/8 - 1 (0.178)", round(3*np.pi/8 - 1, 3))
    # B4 twisted sector energy 1/2 zeta(-1, theta) = -B2(theta)/4 at theta = 1/4 and 0
    B2 = lambda t: t*t - t + 1/6
    P("E(theta=1/4) = -B2(1/4)/4 (1/192); E(0) = -1/24", (round(-B2(0.25)/4, 6), round(1/192, 6), round(-B2(0)/4, 6)))

    print("== RS = golden throat (UV end)")
    from scipy.special import j0 as J0, y0 as Y0, j1 as J1f, y1 as Y1
    from scipy.optimize import brentq as _br
    def _roots(f, n=4):
        xs = np.linspace(0.5, 15, 6000); out = []
        for a_, b_ in zip(xs[:-1], xs[1:]):
            if f(a_) * f(b_) < 0: out.append(_br(f, a_, b_))
        return np.array(out[:n])
    grav2 = lambda e: _roots(lambda x: J1f(e*x)*Y1(x) - Y1(e*x)*J1f(x))
    vec2  = lambda e: _roots(lambda x: J0(e*x)*Y0(x) - Y0(e*x)*J0(x))
    # (1) same operator: RS chain in y (k=1) vs golden chain in sigma, same depth
    def rs_chain(L, Qy, kp, kw):                     # -d(e^{-kp y} d f) = m^2 e^{-kw y} f on [0,L]
        y = np.linspace(0, L, int(L*Qy)+1); h = y[1]-y[0]; n = len(y)
        p = np.exp(-kp*(y[:-1]+h/2)); K = np.zeros((n, n))
        for i in range(n-1): K[i,i]+=p[i]; K[i+1,i+1]+=p[i]; K[i,i+1]-=p[i]; K[i+1,i]-=p[i]
        w_ = eigh(K/h**2, trap(np.exp(-kw*y)), eigvals_only=True); return np.sqrt(np.clip(w_,0,None))[1:4]
    mg = np.sqrt(sl_r(0, 6, 32)[1:4]); mr = rs_chain(6*lp, 32/lp, 4, 2)
    P("RS chain (y) vs golden chain (sigma), graviton m_k", (np.round(mr*phi**6, 4), np.round(mg, 4)))
    # (2) exact two-brane condition matches the golden-chain vector table
    P("exact vector m2/m1 at phi^6, phi^12, phi^30 (2.093, 2.171, 2.241)",
      [round((lambda v: v[1]/v[0])(vec2(phi**-L)), 3) for L in (6, 12, 30)])
    # (3) bottom at 12, top at Planck
    mKK = M_lep*phi**12/1000                          # GeV per zero
    for nm, MP in (("M_Pl", M_PLANCK_GEV), ("reduced M_Pl", 2.435e18)):
        kpr = np.log(MP/mKK); e = np.exp(-kpr); g_, v_ = grav2(e), vec2(e)
        P(f"{nm}: k pi r (39.33/37.72); sigma_UV (93.74/90.39)", (round(kpr, 2), round(12 + kpr/lp, 2)))
        P(f"  graviton zeros (3.8317, 7.0156, 10.1735, 13.3237)", np.round(g_, 4))
        P(f"  vector zeros (2.4448, 5.5615, 8.6958, 11.835) vs LYR 2.45 5.57 8.7 11.84", np.round(v_, 4))

    print("== Boundary conditions: zero mode")
    def _bc(dirichlet):
        Q = 32; s_ = np.linspace(0, 12, 12*Q+1); h = lp/Q; n = len(s_)
        p = phi**(4*(s_[:-1]+.5/Q)); K = np.zeros((n, n))
        for i in range(n-1): K[i,i]+=p[i]; K[i+1,i+1]+=p[i]; K[i,i+1]-=p[i]; K[i+1,i]-=p[i]
        R = np.diag(phi**(2*s_))
        if dirichlet: K, R = K[1:-1,1:-1], R[1:-1,1:-1]
        return eigh(K/h/h, R, eigvals_only=True)[0]
    P("lowest m^2: Neumann (~0) ; Dirichlet (26.4)", (f"{_bc(False):.1e}", round(_bc(True), 1)))

    print("== Summary/Discussion: next graviton modes at sigma_IR = 12 (no free parameter)")
    z6 = jn_zeros(1, 6)
    P("m_k = j_{1,k} M phi^12, k=1..6 (GeV)", np.round(z6*mKK, 0))

    print("== Remark 2: the ring")
    _n = 7; Kr = np.zeros((_n, _n))
    for i in range(_n):
        Kr[i, i] = 2; Kr[i, (i-1) % _n] -= phi**2; Kr[i, (i+1) % _n] -= phi**-2
    ev = np.linalg.eigvals(Kr/lp**2)
    P("ring: max |Im m^2| (>0: complex spectrum)", round(float(np.max(np.abs(ev.imag))), 3))
    P("ring: constant mode m^2 = -1/(log phi)^2 ; BF bound -4", (round(float(np.min(ev.real)), 4), round(-1/lp**2, 4)))
    _o = Kr.copy(); _o[0, -1] = _o[-1, 0] = 0
    P("open tower: max |Im m^2| (0: real spectrum)", round(float(np.max(np.abs(np.linalg.eigvals(_o/lp**2).imag))), 6))
    print("== Clock of phi mod N (Pisano period); phi^12 on it")
    def _phipow(k, N):                      # phi^k = a + b phi in Z[phi]/N
        a, b = 1, 0
        for _ in range(k): a, b = b % N, (a + b) % N
        return a, b
    def _ord(N):
        k = 1
        while _phipow(k, N) != (1 % N, 0): k += 1
        return k
    for N in (16, 9, 12, 24, 48, 72, 5):
        h = _phipow(12, N)
        P(f"N={N}: clock, phi^12, phi^12 involution", (_ord(N), h, _phipow(24, N) == (1 % N, 0) and h != (1 % N, 0)))

    print("== Operator (K) of CW6: Dirichlet sine band, phase 0")
    _K = np.zeros((7, 7))
    for i in range(7):
        _K[i, i] = 2
        if i > 0: _K[i, i-1] = -phi**2
        if i < 6: _K[i, i+1] = -phi**-2
    _ev = np.sort(np.linalg.eigvals(_K/lp**2).real)
    _th = np.sort((2 - 2*np.cos(np.pi*np.arange(1, 8)/8))/lp**2)
    P("eig(K) = (2-2cos(pi k/8))/(log phi)^2 (max diff)", f"{np.max(np.abs(_ev-_th)):.1e}")
    print("== Convergence of m1 on [0,12] (exact two-brane 3.8318)")
    P("Q = 16, 32, 64, 128", [round(float(np.sqrt(sl_r(0, 12, Q)[1])), 3) for Q in (16, 32, 64, 128)])

    print("== v2: alternatives for m0 (golden valuation of the scale)")
    _sc = 99.12
    for _nm, _m in (("M", M_GEV), ("m_p/3", 0.938272/3), ("m_e", 0.000510999)):
        P(f"sigma_IR with m0 = {_nm}", round(float(np.log(_sc/_m)/lp), 2))
    P("M_PCF log phi = 6 sqrt3 pi (framework units): M_PCF", round(6*np.sqrt(3)*np.pi/lp, 3))

    print("== v3: second short cycle")
    P("leading order pi(k+1/4) M phi^12, k=1 (GeV) ; exact j11", (round(np.pi*1.25*mKK, 0), round(jn_zeros(1,1)[0]*mKK, 0)))
    _v24 = vec2(phi**-24)
    P("vector m2/m1, T-dual throat [-12,12] (2.228) ; Planck top (2.275)", (round(_v24[1]/_v24[0], 3), round((lambda v: v[1]/v[0])(vec2(np.exp(-np.log(M_PLANCK_GEV/mKK)))), 3)))
    P("M phi^11 (GeV), CW6 M-theory level read as a scale", round(M_GEV*phi**11, 1))
    _th = 2*np.sin(np.pi*np.arange(1, 8)/16)/lp
    P("CW6 (160): m_k = 2 sin(k pi/16)/log phi vs eig(K)", f"{np.max(np.abs(np.sort(_th**2) - np.sort(np.linalg.eigvals(_K/lp**2).real))):.1e}")

    print("== v4: second-order convergence (trapezoidal end weights)")
    P("relative error of m1 on [0,12], Q=16,32,64,128 vs 3.83182", [f"{abs(np.sqrt(sl_r(0,12,Q)[1])-3.83182)/3.83182:.1e}" for Q in (16,32,64,128)])
    P("vector m2/m1, 24 nodes vs exact (diff < 4e-4)", [round(abs(ratios(sl(a,6,24,2,0))[0][1]-(lambda v:v[1]/v[0])(vec2(phi**-(6-a)))),5) for a in (0,-6,-24)])

    print("== v5: SL2(Z) facts of Imported statement I9")
    _S = np.array([[0, -1], [1, 0]]); _T = np.array([[1, 1], [0, 1]]); _ST = _S @ _T
    _I = np.eye(2, dtype=int)
    _ord = lambda A: next(k for k in range(1, 13) if np.array_equal(np.linalg.matrix_power(A, k), _I))
    P("order S (4), order ST (6)", (_ord(_S), _ord(_ST)))
    P("S^2 = (ST)^3 = -1", np.array_equal(np.linalg.matrix_power(_S, 2), -_I) and np.array_equal(np.linalg.matrix_power(_ST, 3), -_I))
    P("ST mod 2 = [[0,1],[1,1]]", (_ST % 2).tolist())
    _e = lambda a, b, ea, eb: a/b*np.hypot(ea/a, eb/b)
    P("ratio errors m2/m1, m3/m1, m4/m1 (0.11, 0.16, 0.21)", (round(_e(700,380,20,20),2), round(_e(1000,380,30,20),2), round(_e(1322,380,40,20),2)))
    P("v6: phi^s + phi^(s+1) = phi^(s+2) at s = 0.37, -5, 12 (True)", all(abs(phi**s + phi**(s+1) - phi**(s+2)) < 1e-9*phi**(s+2) for s in (0.37, -5, 12)))
    P("v6: pi/phi is transcendental (phi algebraic, pi transcendental): pi/phi =", round(np.pi/phi, 6))

SECCIONES.append((1, 'Every number in order of appearance; alternatives for m0 (§10)', seccion_1))

# ======================================================================
# 2. Vacuum energy of the tower, exact zeros of J1 (§10; requires mpmath)
# ======================================================================
def seccion_2():
    """Casimir (Coleman-Weinberg) energy of the graviton tower with EXACT zeros of J1.
    Sum f(j_k), f = j^4 log j^2 (A) and j^4 (B), regularized: K exact zeros + McMahon tail
    (j = b + c1/b + c3/b^3 + c5/b^5, b = pi(k+1/4)) summed with the Hurwitz zeta, a = 5/4."""
    import mpmath as mp
    mp.mp.dps = 30
    phi = (1 + mp.sqrt(5)) / 2
    c1, c3, c5 = mp.mpf(-3)/8, mp.mpf(36)/1536, -mp.mpf(32*3*1179)/(15*32768)
    eps = lambda u: c1*u**2 + c3*u**4 + c5*u**6
    P = mp.taylor(lambda u: (1+eps(u))**4, 0, 8)                       # L coefficients
    Q = mp.taylor(lambda u: 2*(1+eps(u))**4*mp.log(1+eps(u)) if u != 0 else 0, 0, 8)
    a = mp.mpf(5)/4
    def S(m, conlog):                    # sum_k beta^m (log beta^2 if conlog), regularized
        z, dz = mp.zeta(-m, a), mp.zeta(-m, a, 1)
        return mp.pi**m * ((2*mp.log(mp.pi)*z - 2*dz) if conlog else z)
    def asym(beta, conlog):
        L = mp.log(beta**2); out = 0
        for n in range(0, 9, 2):
            out += beta**(4-n) * ((P[n]*L + Q[n]) if conlog else P[n])
        return out
    def regularized_sum(conlog, K):
        reg = sum((P[n]*S(4-n, True) + Q[n]*S(4-n, False)) if conlog else P[n]*S(4-n, False)
                  for n in range(0, 9, 2))
        corr = 0
        for k in range(1, K+1):
            j = mp.besseljzero(1, k); beta = mp.pi*(k + mp.mpf(1)/4)
            f = j**4*mp.log(j**2) if conlog else j**4
            corr += f - asym(beta, conlog)
        return reg + corr
    for K in (20, 60):
        A, B = regularized_sum(True, K), regularized_sum(False, K)
        ls = -A/(2*B) - mp.mpf(1)/4
        print(f"K={K}: A={mp.nstr(A,8)}  B={mp.nstr(B,8)}  log s*={mp.nstr(ls,8)}  "
              f"depth log_phi(1/s*) = {mp.nstr(-ls/mp.log(phi),8)}   sign B: {'+' if B>0 else '-'}")

SECCIONES.append((2, 'Vacuum energy of the tower, exact zeros of J1 (§10; requires mpmath)', seccion_2))

# ======================================================================
# 3. Two-brane spectra (Proposition of the two-brane model)
# ======================================================================
def seccion_3():
    """RS and golden-tower equations side by side: exact KK masses with two branes.
    Graviton:  J1(eps x) Y1(x) - Y1(eps x) J1(x) = 0 ;  vector: J0(eps x) Y0(x) - Y0(eps x) J0(x) = 0
    with x = m z_IR, eps = z_UV/z_IR = e^{-k pi r} = phi^{-(sigma_UV - sigma_IR)}."""
    import numpy as np
    from scipy.special import j0, y0, j1, y1
    from scipy.optimize import brentq
    phi = (1 + 5**0.5) / 2; lp = np.log(phi)
    def roots(f, n=3):
        xs = np.linspace(0.5, 15, 6000); out = []
        for a, b in zip(xs[:-1], xs[1:]):
            if f(a) * f(b) < 0: out.append(brentq(f, a, b))
        return np.array(out[:n])
    def grav(eps): return roots(lambda x: j1(eps*x)*y1(x) - y1(eps*x)*j1(x))
    def vec(eps):  return roots(lambda x: j0(eps*x)*y0(x) - y0(eps*x)*j0(x))
    print("validation against the golden chain (article table):")
    for lev in (6, 12, 30):
        v = vec(phi**-lev); print(f"  depth phi^{lev}: vector m2/m1 = {v[1]/v[0]:.3f}")
    M = M_GEV; mKK = M*phi**12          # scale per zero on the background sigma_IR = 12 (GeV)
    for nm, MP in (("M_Pl", M_PLANCK_GEV), ("reduced M_Pl", 2.435e18)):
        kpr = np.log(MP/mKK); levels = kpr/lp; eps = np.exp(-kpr)
        g, v = grav(eps), vec(eps)
        print(f"\nUV at {nm}: k pi r = {kpr:.2f} = {levels:.2f} levels; sigma_UV = {12+levels:.2f}")
        print(f"  graviton x_n = {np.round(g,4)}  (deep J1: 3.8317, 7.0156)")
        print(f"  vector   x_n = {np.round(v,4)}  m2/m1 = {v[1]/v[0]:.4f}")
        print(f"  gluon/graviton per universal zero: x1_vec/x1_grav = {v[0]/g[0]:.4f}")
    print("\nLYR: gluon 3600-4000 GeV / graviton 380 GeV =", round(3600/380,2), "-", round(4000/380,2))

SECCIONES.append((3, 'Two-brane spectra (Proposition of the two-brane model)', seccion_3))

# ======================================================================
# 4. Metric and reflection positivity (Proposition of the metric, §5)
# ======================================================================
def seccion_4():
    import numpy as np
    from scipy.linalg import expm, eigvalsh
    phi=(1+5**.5)/2; l2=np.log(phi)**2; N=7; s=np.arange(N)
    L=np.diag(np.full(N,-2.))
    for i in range(1,N): L[i,i-1]=phi**2; L[i-1,i]=phi**-2
    L/=l2; K=-L                                   # mass^2 operator, spectrum >0
    # 1. standard product <u,v> = u.v  (basis |sigma> orthonormal, as in Prop 5.16/5.22)
    print("K self-adjoint in the standard product:", np.allclose(K,K.T))
    for a in (0.05,0.2,1.0):
        T=expm(-a*K); m=eigvalsh((T+T.T)/2).min()
        print(f"  a={a}: min eigenvalue of sym(T)={m:.3e}  -> <f,Tf> >= 0 for all f: {m>-1e-12}")
    # 2. metric eta = D^T D with D = diag(phi^{-2 sigma})
    eta=np.diag(phi**(-4.*s))
    print("K self-adjoint in <u,v>_eta = u.eta.v :", np.allclose(eta@K,(eta@K).T))
    for a in (0.05,0.2,1.0):
        T=expm(-a*K); G=eta@T
        print(f"  a={a}: <f,Tf>_eta min = {eigvalsh((G+G.T)/2).min():.3e}")
    # 3. eta against the throat warp (87): z = phi^sigma, A = -log z
    A=-s*np.log(phi)
    print("eta_sigma == e^{4A(sigma)} (sqrt(-g) of ds^2=e^{2A}eta dx dx + dz^2):",
          np.allclose(np.diag(eta),np.exp(4*A)))
    # 4. widths in the eta metric == biorthogonal
    w,V=np.linalg.eig(K); o=np.argsort(w.real); w,V=w[o].real,V[:,o].real
    V=V/np.sqrt(np.einsum('ij,ij->j',V,eta@V))     # normalize in eta
    p=np.array([eta[0,0]*V[0,j]**2 for j in range(4)])
    print("weight at the edge (eta), relative to mode 2 x20:",np.round(p/p[1]*20,1))

SECCIONES.append((4, 'Metric and reflection positivity (Proposition of the metric, §5)', seccion_4))

# ======================================================================
# 5. Phase 1/4 (Corollary of the phase)
# ======================================================================
def seccion_5():
    import numpy as np
    from scipy.special import jn_zeros, jv
    from scipy.optimize import brentq
    obs=np.array([380.,700,1000,1322])
    def zeros(nu,n=4):
        f=lambda x: jv(nu,x); xs=np.linspace(0.5,20,4000); r=[]
        for a,b in zip(xs[:-1],xs[1:]):
            if f(a)*f(b)<0: r.append(brentq(f,a,b))
        return np.array(r[:n])
    def fit(m): A=(obs@m)/(m@m); return np.sqrt(np.mean(((obs-A*m)/obs)**2))*100, A
    print("1) Free phase: m = A (n + theta), 2 parameters")
    best=min((fit(np.arange(1,5)+t)[0],t) for t in np.linspace(-.5,1,3001))
    print(f"   optimal theta = {best[1]:.3f}  rms={best[0]:.2f}%")
    print("2) Zeros of J_nu with nu = d/2 - 1 (graviton profile in AdS_{d+1}), 1 parameter")
    for d in (3,4,5,6):
        nu=d/2-1; z=zeros(nu); r,A=fit(z)
        ph=np.mean(z/np.pi-np.arange(1,5))
        print(f"   d={d}: nu={nu:.1f}  asympt. phase (d-3)/4={ (d-3)/4:.2f}  measured phase={ph:.3f}  rms={r:.2f}%")
    print("3) Discrete chain of A.7 (Dirichlet at both edges): phase 0 -> rms",
          f"{fit(np.arange(1,5)*1.0)[0]:.2f}%")

SECCIONES.append((5, 'Phase 1/4 (Corollary of the phase)', seccion_5))

# ======================================================================
# 6. Bessel chain (Bessel theorem, Observation of levels)
# ======================================================================
def seccion_6():
    import numpy as np
    from scipy.linalg import eigh
    from scipy.special import jn_zeros
    phi=(1+5**.5)/2; h0=np.log(phi); obs=np.array([380.,700,1000,1322]); j1=jn_zeros(1,4)
    def chain(s_uv,s_ir,M,peso=True):
        # sigma nodes s_uv .. s_ir with M substeps per golden level; Neumann at both edges
        sig=np.linspace(s_uv,s_ir,int(round((s_ir-s_uv)*M))+1); h=h0/M; n=len(sig)
        p=phi**(-4*(sig[:-1]+0.5/M))            # stiffness e^{4A} at the midpoints
        K=np.zeros((n,n))
        for i in range(n-1):
            K[i,i]+=p[i];K[i+1,i+1]+=p[i];K[i,i+1]-=p[i];K[i+1,i]-=p[i]
        K/=h*h
        R=np.diag(phi**(-2*sig)) if peso else np.eye(n)   # mass weight e^{2A}
        R[0,0]/=2; R[-1,-1]/=2                # half weight at the ends (trapezoid): second order
        w=eigh(K,R,eigvals_only=True); m=np.sqrt(np.clip(w,0,None))
        return m[1:5]                         # m[0]=0: the massless graviton (zero mode)
    def rms(m): A=(obs@m)/(m@m); return np.sqrt(np.mean(((obs-A*m)/obs)**2))*100
    print("normalized J1 zeros:",np.round(j1/j1[0],4),"  LYR:",np.round(obs/380,4))
    for (a,b) in [(0,6),(-6,6),(-20,6),(-60,6)]:
        for M in (1,4,32):
            m=chain(a,b,M); print(f"sigma[{a},{b}] M={M:2d}: m/m1={np.round(m/m[0],4)}  rms LYR={rms(m):.2f}%")
    # without weight: on [-20,6] the problem is ill-conditioned (weights ~1e17) and the solver returns spurious modes
    # depending on M; shown on [-6,6], where it is stable.
    print("without the e^{2A} weight (as in A.7), sigma[-6,6], M=32:",np.round((lambda m:m/m[0])(chain(-6,6,32,False)),3))

SECCIONES.append((6, 'Bessel chain (Bessel theorem, Observation of levels)', seccion_6))

# ======================================================================
# 7. Prediction and what is not claimed (§11, §12)
# ======================================================================
def seccion_7():
    import numpy as np
    from scipy.linalg import eigh
    from scipy.special import jn_zeros
    phi=(1+5**.5)/2; h0=np.log(phi)
    def chain(a,b,M,kp,kw):          # -d(e^{kp A} d f) = m^2 e^{kw A} f, A=-w, Neumann
        s=np.linspace(a,b,int((b-a)*M)+1); h=h0/M; n=len(s)
        p=phi**(-kp*(s[:-1]+.5/M)); K=np.zeros((n,n))
        for i in range(n-1): K[i,i]+=p[i];K[i+1,i+1]+=p[i];K[i,i+1]-=p[i];K[i+1,i]-=p[i]
        r_=phi**(-kw*s); r_[0]/=2; r_[-1]/=2   # half weight at the ends (trapezoid)
        w=eigh(K/h/h,np.diag(r_),eigvals_only=True); return np.sqrt(np.clip(w,0,None))[1:4]
    g=chain(-6,6,32,4,2); v=chain(-6,6,32,2,0)
    print("graviton tower:",np.round(g/g[0],4)," J1:",np.round(jn_zeros(1,3)/jn_zeros(1,1),4))
    print("vector   tower:",np.round(v/v[0],4)," J0:",np.round(jn_zeros(0,3)/jn_zeros(0,1),4))
    print(" gluon LYR 8600/3600 =",round(8600/3600,3),"(vector tower",round(v[1]/v[0],3),")")
    print(" quark LYR 2150/1040 =",round(2150/1040,3))
    print("\n== E4: scale per sector (m1 / first zero of its operator) ==")
    x1g=g[0]; x1v=v[0]
    Sg=380/x1g; Sgl=3600/x1v; Sq=1040/x1v
    for n_,S in (("graviton",Sg),("gluon",Sgl),("quark*",Sq)):
        print(f"  {n_:8s} scale={S:9.2f}  log_phi(scale/graviton)={np.log(S/Sg)/np.log(phi):.2f}")
    print("  CW6: sigma_G=2, U(1)=3, SU(2)=4, SU(3)=5  -> gluon/graviton would require Delta sigma = 3")
    print("  (*quark with vector normalization, only indicative)")
    print("\n== E5: uncertainty of the LYR ratios ==")
    for m,dm in ((700,20),(1000,30),(1322,40)):
        print(f"  {m}/380: {m/380:.3f} +- {m/380*np.hypot(dm/m,20/380):.3f}")
    print("  finite tower sigma[0,6] vs J1 (infinite): m2/m1 1.8419 vs 1.8309, m4/m1 3.5284 vs 3.4772")

SECCIONES.append((7, 'Prediction and what is not claimed (§11, §12)', seccion_7))

# ======================================================================
# 8. Look-elsewhere (§7, §10)
# ======================================================================
def seccion_8():
    """
    Comparativa: Le Yaouanc & Richard (2026), "Evidence for KK excitations of the
    graviton, gluon and quark at LHC"  vs  CW6_paper_v4.tex (Crystalline Worldsheet).

    Question: which spectral structure best describes the reported KK masses,
    the Randall-Sundrum one (Bessel zeros, ~linear spacing) or the golden tower
    of CW6 (z = phi^sigma, geometric spacing)?  And what does the discrete KK
    operator of CW6 (Prop. kk-discrete-spectrum) say about the mass ratios?
    """
    import numpy as np
    from scipy.special import jn_zeros
    from scipy.optimize import minimize_scalar

    phi = (1 + 5**0.5) / 2
    lnphi = np.log(phi)
    out = []
    P = lambda *a: out.append(" ".join(str(x) for x in a))

    # ---------------------------------------------------------------- LYR data
    grav_obs = np.array([380., 700., 1000., 1322.])          # G_KK candidates (GeV)
    grav_tab = np.array([380, 700, 1000, 1322, 1640, 1945, 2260, 2590, 2905.])
    gluon = np.array([3600., 8600.])                          # g_KK
    quark = np.array([1040., 2150.])                          # q_KK
    zkk = 3000.

    # ------------------------------------------------ 1. gravitons: RS vs phi
    x = np.concatenate([[0.], jn_zeros(1, 12)])               # J1 zeros (incl. 0)
    P("== 1. Graviton tower ==")
    P("J1 zeros:", np.round(x[1:10], 2))
    # RS: m_i = M * x_i  (1 parameter).  Assignment: 380->x1, 700->x2, ...
    xi = x[1:5]
    M_rs = (grav_obs @ xi) / (xi @ xi)
    res_rs = grav_obs - M_rs * xi
    # Golden: m_k = m0 * phi^(k/2)  with k a free integer per point (1 parameter m0)
    def golden_fit(m, step):
        def cost(lm0):
            k = np.round((np.log(m) - lm0) / (step * lnphi))
            return np.sum((np.log(m) - lm0 - k * step * lnphi) ** 2)
        r = minimize_scalar(cost, bounds=(np.log(m.min()) - 1, np.log(m.min()) + 1),
                            method="bounded")
        lm0 = r.x
        k = np.round((np.log(m) - lm0) / (step * lnphi))
        return np.exp(lm0), k, np.exp(lm0 + k * step * lnphi)
    m0, k, pred_g = golden_fit(grav_obs, 1.0)
    rel_rs = res_rs / grav_obs
    rel_g = (grav_obs - pred_g) / grav_obs
    P(f"RS   M={M_rs:.1f} GeV  pred={np.round(M_rs*xi)}  rel err={np.round(rel_rs*100,1)}%")
    P(f"phi  m0={m0:.1f} GeV  k={k.astype(int)}  pred={np.round(pred_g)}  rel err={np.round(rel_g*100,1)}%")
    P(f"rms RS={np.sqrt(np.mean(rel_rs**2))*100:.1f}%   rms phi^k={np.sqrt(np.mean(rel_g**2))*100:.1f}%")
    P("successive observed ratios:", np.round(grav_obs[1:]/grav_obs[:-1], 3),
      "| RS:", np.round(xi[1:]/xi[:-1], 3), "| phi:", round(phi, 3))
    # the full LYR table (predictions) is exactly RS:
    P("LYR table / 100 :", np.round(grav_tab/100, 2), "vs zeros", np.round(x[1:10], 2))

    # --------------------------------------------- 2. KK gluons and quarks
    P("\n== 2. Gluones / quarks KK ==")
    rs_vec = np.array([2.45, 5.57, 8.70, 11.84])
    P(f"g: obs 8600/3600={8600/3600:.3f}  RS 5.57/2.45={5.57/2.45:.3f}  "
      f"phi^2={phi**2:.3f}  log_phi={np.log(8600/3600)/lnphi:.3f}")
    P(f"q: obs 2150/1040={2150/1040:.3f}  RS(Abe et al.)=2  phi^(3/2)={phi**1.5:.3f}  "
      f"log_phi={np.log(2150/1040)/lnphi:.3f}")
    hier = np.array([380., 1000., 3600.])
    P("hierarchy G:q:g =", hier/380, " log_phi ratios:",
      np.round(np.log(hier[1:]/hier[:-1])/lnphi, 3))
    P(f"q/G 1000/380={1000/380:.3f} vs phi^2={phi**2:.3f} (dif {100*(1000/380/phi**2-1):.1f}%)")
    P(f"gluon1/grav1 RS ingenuo 2.45/3.83={2.45/3.83:.3f}^-1  obs 380/3600={380/3600:.3f}")

    # --------------------------------- 3. look-elsewhere for 'phi coincidences'
    P("\n== 3. Look-elsewhere ==")
    rng = np.random.default_rng(1)
    r = np.exp(rng.uniform(np.log(1.3), np.log(4.5), 200000))
    grid = phi ** (np.arange(1, 9) / 2)          # phi^(k/2), k=1..8
    d = np.min(np.abs(r[:, None] / grid[None, :] - 1), axis=1)
    for tol in (0.01, 0.03, 0.05, 0.10):
        P(f"P(random ratio in [1.3,4.5] within {tol*100:.0f}% of some phi^(k/2)) = {np.mean(d<tol):.2f}")
    obs_ratios = {"q/G 1000/380": 1000/380, "g 8600/3600": 8600/3600,
                  "q 2150/1040": 2150/1040, "g/q 3600/1000": 3.6}
    for n_, v in obs_ratios.items():
        j = np.argmin(abs(v/grid-1)); P(f"  {n_}={v:.3f} -> phi^({j+1}/2)={grid[j]:.3f}  ({100*(v/grid[j]-1):+.1f}%)")

    # ------------------------------ 4. discrete KK operator of CW6 (app:kk)
    P("\n== 4. Discrete KK operator of CW6 (7 levels, sigma=0..6) ==")
    n = 7
    L = np.diag(np.full(n, -2.0))
    for s in range(1, n):
        L[s, s-1] = phi**2
        L[s-1, s] = phi**-2
    L /= lnphi**2
    ev = np.sort(np.linalg.eigvals(L).real)[::-1]
    P("eigenvalues L:", np.round(ev, 3))
    # L is non-symmetric tridiagonal; similar to a symmetric one with hopping sqrt(phi^2*phi^-2)=1
    P("hopping symmetrized sqrt(phi^2*phi^-2) =", 1.0, "-> spectrum = (-2+2cos(k pi/8))/ln^2 phi")
    ana = (-2 + 2*np.cos(np.arange(1, n+1)*np.pi/(n+1))) / lnphi**2
    P("analytic     :", np.round(np.sort(ana)[::-1], 3))
    m2 = -ev                                        # masses^2 >= 0
    m = np.sqrt(m2)
    P("m_k (units 1/ln phi):", np.round(m, 3))
    P("ratios m_k/m_1:", np.round(m/m[0], 3))
    P("RS (J1 zeros) x_k/x_1:", np.round(x[1:8]/x[1], 3))
    P("obs grav m/380 :", np.round(grav_obs/380, 3))

    # ------------------------------- 5. shared AdS5 invariants
    P("\n== 5. Background geometry (both use AdS5 with warp) ==")
    rows = [("warp A(z)", "RS: A=-k|y|", "CW6: A=-log z, z=phi^sigma"),
            ("Lambda_5", "RS: -6k^2", "CW6: -6 (l=1)"),
            ("R", "RS: -20k^2", "CW6: -20"),
            ("BF", "-4", "-4"),
            ("brane", "RS: IR/UV tension (Israel)", "CW6: Israel per level, lambda=N_modes/M_PCF"),
            ("abs. scale", "RS: k e^{-k pi r} ~ TeV", "CW6: not fixed (open scale translation)")]
    for a, b, c in rows:
        P(f"{a:12s} | {b:28s} | {c}")

    open("kk_vs_cw6_out.txt", "w").write("\n".join(out))
    print("\n".join(out))

SECCIONES.append((8, 'Look-elsewhere (§7, §10)', seccion_8))

_C = dict(hbar=HBAR, c=C_LIGHT, G=G_NEWTON, Mpc=MPC_M)   # single origin: kkgt.constants
_LamP = lam_planck   # single origin: kkgt.harness.lam_planck (same signature)

# ======================================================================
# 25. The cut and projection with the self-dual Gaussian, in both spaces
# ======================================================================
def seccion_25():
    import math
    phi = (1 + 5 ** 0.5) / 2; pb = (1 - 5 ** 0.5) / 2
    def best(x, rad=0.6):
        out = []
        for b in range(-50, 400):
            a0 = round(x - b * phi)
            for a in (a0 - 1, a0, a0 + 1):
                v = a + b * phi
                if abs(v - x) < rad:
                    c = a + b * pb; out.append((math.exp(-math.pi * c * c), a, b, v))
        return sorted(out, reverse=True)[:2]
    for x in (11.97, 583.88):
        print(f"sigma index, near {x}: " + "; ".join(f"{a}+{b}phi = {v:.2f} (weight {w:.2g})" for w, a, b, v in best(x)))
    print(f"  the integer 12 has conjugate 12: weight 10^{-math.pi*144/math.log(10):.0f}  -> the cut on sigma disappears")
    print("scale: units phi^n, conjugate (-1)^n phi^-n, weight e^(-pi phi^-2n):",
          ", ".join(f"n={n}: {math.exp(-math.pi*phi**(-2*n)):.2f}" for n in range(0, 7)))

SECCIONES.append((25, 'The cut and projection with the self-dual Gaussian, in both spaces', seccion_25))

# ======================================================================
# 26. The edge of the window and sigma_G
# ======================================================================
def seccion_26():
    import math
    phi = (1 + 5 ** 0.5) / 2; L = math.log(phi)
    print(f"weight 1/2 crossing: n = {0.5*math.log(math.pi/math.log(2))/L:.3f}; H l = 1 crossing: n = {math.log(2)/L:.3f}")
    print(f"thresholds that make n = 2 the first level: ({math.exp(-math.pi*phi**-2):.3f}, {math.exp(-math.pi*phi**-4):.3f})")
    for n in range(0, 4):
        print(f"  n = {n}: peso {math.exp(-math.pi*phi**(-2*n)):.3f}, H l = {math.sqrt(2*phi**(-n)):.3f}")
    print("first active integer level along both routes: 2 = sigma_G = n - 1 (CW6)")

SECCIONES.append((26, 'The edge of the window and sigma_G', seccion_26))

# ======================================================================
# 27. The window as a nome: the tower of tori and S as a mirror
# ======================================================================
def seccion_27():
    import math
    phi = (1 + 5 ** 0.5) / 2
    for n in range(0, 4):
        t = phi ** (-2 * n)
        print(f"  n={n}: tau_n = {t:.4f} i, nome q = e^(i pi tau) = {math.exp(-math.pi*t):.4f};  S: -1/tau_n = {1/t:.4f} i = tau_{-n}")
    nh = 0.5 * math.log(math.pi / math.log(2)) / math.log(phi)
    print(f"weight 1/2 crossing: n = {nh:.6f}; quarter turn pi/2 = {math.pi/2:.6f}; w(pi/2) = {math.exp(-math.pi*phi**(-math.pi)):.6f}")
    print(f"width that would make the crossing exact at pi/2: log2 * phi^pi = {math.log(2)*phi**math.pi:.6f} (self-dual: pi = {math.pi:.6f})")

SECCIONES.append((27, 'The window as a nome: the tower of tori and S as a mirror', seccion_27))

# ======================================================================
# 28. Poisson: the proper time and 1/N; theta_3 at tau = i
# ======================================================================
def seccion_28():
    import math
    for N in (2.618033988749895, 6.854101966249685):
        lhs = sum(math.exp(-math.pi * k * k * N) for k in range(-60, 61))
        rhs = N ** -0.5 * sum(math.exp(-math.pi * m * m / N) for m in range(-60, 61))
        print(f"  N = {N:.4f}: modes {lhs:.12f}, windings {rhs:.12f}; first winding e^(-pi/N) = {math.exp(-math.pi/N):.4f}")
    t3 = sum(math.exp(-math.pi * k * k) for k in range(-30, 31))
    print(f"theta_3(e^-pi) = {t3:.12f};  pi^(1/4)/Gamma(3/4) = {math.pi**0.25/math.gamma(0.75):.12f}")

SECCIONES.append((28, 'Poisson: the proper time and 1/N; theta_3 at tau = i', seccion_28))

# ======================================================================
# 29. What fixes the lattice point: Omega_Lambda h^2
# ======================================================================
def seccion_29():
    import math
    phi = (1 + 5 ** 0.5) / 2; L = math.log(phi)
    lP2 = _C['hbar'] * _C['G'] / _C['c'] ** 3; H100 = 100e3 / _C['Mpc']
    Lam = 3 * phi ** -584 / lP2
    OLh2 = Lam * _C['c'] ** 2 / (3 * H100 ** 2)
    h, dh, wm, dwm = 0.6736, 0.0054, 0.1430, 0.0011
    print(f"point 584: Lambda l_P^2 = 3 phi^-584 = {3*phi**-584:.4e};  Omega_L h^2 = {OLh2:.4f}")
    for r in (0.0, -1.0):        # Omega_m and H0 from Planck 2018, correlation between the two bounds
        Om, dOm = 0.3153, 0.0073
        a, b = -h * h * dOm, 2 * (1 - Om) * h * dh
        p, dp = (1 - Om) * h * h, math.sqrt(a * a + b * b + 2 * a * b * r)
        print(f"Planck 2018, r(Omega_m, H0) = {r:+.0f}: Omega_L h^2 = {p:.4f} +- {dp:.4f}: {(OLh2-p)/dp:+.1f} sigma")
    print(f"with omega_m = {wm} +- {dwm} and flatness: H0 = {100*math.sqrt(OLh2+wm):.2f} +- {100*0.5*dwm/math.sqrt(OLh2+wm):.2f}")
    # Planck only in the variable of the criterion (the level) and against DESI DR2 + CMB
    HD, dHD, OmD, dOmD, rD = 0.6817, 0.0028, 0.3027, 0.0036, -0.975
    aD, bD = -HD*HD*dOmD, 2*(1-OmD)*HD*dHD; pD = (1-OmD)*HD*HD; dpD = math.sqrt(aD*aD+bD*bD+2*aD*bD*rD)
    Om, dOm = 0.3153, 0.0073; a, b = -h*h*dOm, 2*(1-Om)*h*dh; p = (1-Om)*h*h
    lvl = lambda x: 584 + math.log(OLh2 / x) / L
    ten = []
    for r in (0.0, -1.0):
        dp = math.sqrt(a*a + b*b + 2*a*b*r); sl = dp / (p * L)
        ten.append((pD - p) / math.hypot(dpD, dp))
        print(f"Planck only, r = {r:+.0f}: level {lvl(p):.3f}, {(584-lvl(p))/sl:.2f} sigma from 584 in the level; DESI+CMB against Planck: {ten[-1]:.2f} sigma in Omega_L h^2")
    assert 1.3 < min(ten) < 1.5 and 1.7 < max(ten) < 1.9, ten
    print(f"DESI DR2 + CMB: Omega_L h^2 = {pD:.4f} +- {dpD:.4f}; Planck and the combination agree (1.4-1.8 sigma)")
    print(f"sensitivity: d sigma / d ln H0 = {-2/L:.3f}; 1 % in H0 = {0.02/L:.3f} levels")
    print(f"584 mod 24 = {584 % 24}; 584 = 2^3 * 73: not a distinguished level of the lattice")

SECCIONES.append((29, 'What fixes the lattice point: Omega_Lambda h^2', seccion_29))

# ======================================================================
# 30. The symmetric throat [-12, 12] and the UV scale
# ======================================================================
def seccion_30():
    import math
    phi = (1 + 5 ** 0.5) / 2; M = M_GEV
    print(f"depth 24 levels (the clock): k pi r = 24 log phi = {24*math.log(phi):.2f}  (top at Planck: 39.33)")
    print(f"IR scale = M phi^12 = {M*phi**12:.2f} GeV; UV scale = M phi^36 = {M*phi**36:.3e} GeV")
    print("vector ratio: 2.228 (symmetric) against 2.275 (Planck); current range 2.15-2.39")

SECCIONES.append((30, 'The symmetric throat [-12, 12] and the UV scale', seccion_30))

# ======================================================================
# 31. The moduli metric of the ring and the conjectures
# ======================================================================
def seccion_31():
    import math
    phi = (1 + 5 ** 0.5) / 2; L = math.log(phi)
    d = math.sqrt(2) * L
    print("K = -ln(2 Im tau), K_tt = 1/(4 Im^2); tau = i t: L_kin = (dt)^2/(4t^2), Phi = ln t / sqrt2")
    print(f"dPhi/dn = sqrt2 log phi = {d:.4f};  |dV/dPhi|/V = {L/d:.4f}")
    print(f"de Sitter (OOSV): c ~ O(1);  TCC (Bedroya-Vafa) in 4D: c >= sqrt(2/3) = {math.sqrt(2/3):.4f}")
    print(f"  slope {L/d:.4f} < bound {math.sqrt(2/3):.4f}: the comparison with the TCC fails under these assumptions")
    for n in (2, 12, 584):
        print(f"  canonical distance at the level {n}: Phi = sqrt2 n log phi = {math.sqrt(2)*n*L:.1f} M_Pl (no bound along the tower)")
    print("  with K = -k ln Im tau the slope is 1/sqrt(2k); the bound holds if and only if k <= 3/4")
    for s in (2, 12, 100):
        print(f"  norm of the two scales at sigma = {s}: (phi^s)(phi^-s) = {phi**s*phi**-s:.3f}")

SECCIONES.append((31, 'The moduli metric of the ring and the conjectures', seccion_31))

# ======================================================================
# 32. The level read off the observer against the lattice shape
# ======================================================================
def seccion_32():
    import math
    phi = (1 + 5 ** 0.5) / 2; L = math.log(phi)
    lP2 = _C['hbar'] * _C['G'] / _C['c'] ** 3; H100 = 100e3 / _C['Mpc']
    def req(n): return 3 * phi ** -n / lP2 * _C['c'] ** 2 / (3 * H100 ** 2)
    print("Omega_L h^2 required by points 583, 584, 585: " + ", ".join(f"{req(n):.4f}" for n in (583, 584, 585)))
    def det(Om, dOm, H0, dH0, r):
        h, dh = H0 / 100, dH0 / 100
        a, b = -h * h * dOm, 2 * (1 - Om) * h * dh
        return (1 - Om) * h * h, math.sqrt(a * a + b * b + 2 * a * b * r)
    def read_level(v, dv):
        n = 584 - math.log(v / req(584)) / L; dn = dv / v / L; k = round(n)
        return n, dn, k, abs(n - k) / dn
    cases = [("Planck 2018, LCDM, r = 0", 0.3153, 0.0073, 67.36, 0.54, 0.0),
             ("Planck 2018, LCDM, r = -1", 0.3153, 0.0073, 67.36, 0.54, -1.0),
             ("DESI DR2 + CMB, LCDM, r = -1 (worst case)", 0.3027, 0.0036, 68.17, 0.28, -1.0),
             ("DESI DR2 + CMB, LCDM, r = -0.975", 0.3027, 0.0036, 68.17, 0.28, -0.975),
             ("DESI DR2 + CMB, LCDM, r = 0", 0.3027, 0.0036, 68.17, 0.28, 0.0)]
    for nm, Om, dOm, H0, dH0, r in cases:
        v, dv = det(Om, dOm, H0, dH0, r); n, dn, k, z = read_level(v, dv)
        print(f"{nm:34s} Omega_L h^2 = {v:.4f} +- {dv:.4f}; level {n:.3f} +- {dn:.3f}; integer {k} at {z:.1f} sigma")
    v = 0.7304 ** 2 - 0.1430; dv = math.hypot(2 * 0.7304 * 0.0104, 0.0011); n, dn, k, z = read_level(v, dv)
    print(f"{'H0 local with omega_m from Planck':34s} Omega_L h^2 = {v:.4f} +- {dv:.4f}; level {n:.3f} +- {dn:.3f}; integer {k} at {z:.1f} sigma")
    print("criterion: a level read 3 sigma or more from every integer rules out the lattice shape")

SECCIONES.append((32, 'The level read off the observer against the lattice shape', seccion_32))

# ======================================================================
# 33. The colour hole: the welded tension, Higuchi and the Regge scale
# ======================================================================
def seccion_33():
    import math
    phi = (1 + 5 ** 0.5) / 2; L = math.log(phi)
    MPCF = 6 * 3 ** 0.5 * math.pi / L; eps0 = math.pi / MPCF
    M = M_GEV; u = M / MPCF; MPl = M_PLANCK_GEV; Ecurv = MPl / 2 ** 0.5
    for q2, nm in ((2 * math.pi, "q^2 = 2 pi"), (1.0, "q = 1")):
        qm2 = (2 * math.pi) ** 2 / q2
        vals = [qm2 * eps0 * phi ** -s * math.pi * phi ** s for s in (0, 5, 12)]
        print(f"{nm}: sigma_t * S en s = 0, 5, 12: " + ", ".join(f"{v:.4f}" for v in vals)
              + f"  (4 pi^4/(q^2 MPCF) = {4*math.pi**4/(q2*MPCF):.4f})")
        r = math.pi ** 3 / (q2 * MPCF)
        print(f"   Delta^2/(2 H^2) = pi^3/(q^2 MPCF) = {r:.4f}; spin two of mass kappa Delta: kappa >= {1/math.sqrt(r):.2f}")
    print(f"Higuchi for kappa = 1 if and only if q^2 <= pi^3/MPCF = {math.pi**3/MPCF:.4f}")
    m1 = 3.8317 * M * phi ** 12
    for nm, E in (("u (particulas)", u), ("sqrt2 l_P (curvatura)", Ecurv)):
        Ms = E / math.sqrt(MPCF)
        print(f"Regge, alpha' = MPCF in {nm}: M_1 = {Ms:.3e} GeV against m_KK,1 = {m1:.1f} GeV")
    print(f"conversion between the two units: {2*math.log(MPl/u)/L - math.log(2)/L:.2f} levels")
    from scipy.special import jn_zeros
    j = jn_zeros(1, 5000); mk = j * M * phi ** 12
    print(f"graviton modes below 1000 TeV: {int((mk < 1e6).sum())}; linear estimate 1e6/(pi M phi^12) = {1e6/(math.pi*M*phi**12):.1f}")

SECCIONES.append((33, 'The colour hole: the welded tension, Higuchi and the Regge scale', seccion_33))

# ======================================================================
# 34. The quintessence of the ring: lambda = 1/sqrt2 against the data
# ======================================================================
def seccion_34():
    import numpy as np
    from scipy.integrate import solve_ivp
    from scipy.optimize import brentq
    lam = 1 / np.sqrt(2)          # slope of the modulus (10.1), Phi in reduced Planck mass
    def run(y_i, N0=-8.0):
        def f(N, s):
            x, y = s; tot = 2 * x * x + (1 - x * x - y * y)
            return [-3 * x + lam * np.sqrt(6) / 2 * y * y + 1.5 * x * tot,
                    -lam * np.sqrt(6) / 2 * x * y + 1.5 * y * tot]
        return solve_ivp(f, [N0, 0.0], [0.0, y_i], dense_output=True, rtol=1e-10, atol=1e-13)
    for Om in (0.30, 0.31, 0.32):
        yi = brentq(lambda y: sum(v * v for v in run(y).y[:, -1]) - (1 - Om), 1e-8, 1e-1)
        sol = run(yi); z = np.linspace(0, 2, 400); N = -np.log(1 + z)
        x, y = sol.sol(N); w = (x * x - y * y) / (x * x + y * y); a = 1 / (1 + z); wt = x * x + y * y
        A = np.vstack([np.ones_like(a), 1 - a]).T * wt[:, None]
        w0, wa = np.linalg.lstsq(A, w * wt, rcond=None)[0]
        print(f"Omega_m = {Om}: w(0) = {w[0]:.3f}; CPL projection (z < 2): w0 = {w0:.3f}, wa = {wa:.3f}")
    c, up = 0.698, 0.173
    print(f"Akrami-Alestas-Nesseris (DESI DR2 + CMB + DESY5): lambda = 0.698 +0.173/-0.202")
    print(f"  1/sqrt2 at {(lam - c) / up:+.2f} sigma; sqrt(2/3) at {(np.sqrt(2/3) - c) / up:+.2f}; sqrt2 at {(np.sqrt(2) - c) / up:+.2f}")

SECCIONES.append((34, 'The quintessence of the ring: lambda = 1/sqrt2 against the data', seccion_34))

# ======================================================================
# 35. The 1/2 threshold: Fisher time, binary entropy, one bit per eigenvalue
# ======================================================================
def seccion_35():
    import math
    for f in (0.25, 0.5, 1.0):
        print(f"f = {f}: tau_F/tau_D = 1/sqrt(2f) = {1/math.sqrt(2*f):.4f};  H(f) = {-(f*math.log2(f)+(1-f)*math.log2(1-f)) if 0<f<1 else 0:.4f} bits")
    print("tau_F = tau_D if and only if f = 1/2; H(1/2) = 1 bit is the maximum; 4 mu^2 = 1 if and only if mu = 1/2")

SECCIONES.append((35, 'The 1/2 threshold: Fisher time, binary entropy, one bit per eigenvalue', seccion_35))

# ======================================================================
# 36. The black hole, touched where needed: the orbit of the tower, the horizon of S(12), the threshold
# ======================================================================
def seccion_36():
    import numpy as np
    from scipy.special import jn_zeros
    phi = (1 + 5 ** 0.5) / 2; L = np.log(phi)
    a = L / (2 * np.pi)
    f = lambda t: np.exp(np.cos(2 * np.pi * t)); g = lambda t: np.exp(2 * np.cos(2 * np.pi * t) + 0.5 * np.sin(4 * np.pi * t))
    th = np.arange(1 << 16) / (1 << 16); F, G = f(th), g(th); P = (F * G).mean(); C = P - F.mean() * G.mean()
    for name, al in (("tower phase, log(phi)/2pi", a), ("rational 13/8", 13 / 8)):
        for N in (100, 1000, 10000):
            t = (np.arange(N) * al) % 1; x, y = f(t), g(t); R = x * y - P
            print(f"{name}: N={N}: connected-part error {abs((x*y).mean()-x.mean()*y.mean()-C)/C:.1e}; mean of the rest/rms {abs(R.mean())/np.sqrt((R*R).mean()):.1e}")
    s = 12; H = np.sqrt(2) * phi ** (-s / 2)
    print(f"S(12) = {np.pi*phi**s:.2f}; Lambda(12) = {6*phi**(-s):.4f} > 0; Gibbons-Hawking pi/(G H^2) = {np.pi/(0.5*H*H):.2f}; "
          f"ring area/4G = {2*np.pi*phi**s/2:.2f}; Cardy c=3 = {2*np.pi*np.sqrt(3*phi**(2*s)/12):.2f}")
    x1 = jn_zeros(1, 1)[0]
    for k in (0.1, 0.05, 0.01):
        print(f"k/M_Pl = {k}: black-hole threshold / m1 = {1/(x1*k*k):.0f}")

SECCIONES.append((36, 'The black hole where needed: the orbit of the tower, the horizon of S(12), the threshold', seccion_36))

# ======================================================================
# 37. Consistency: entropy, modes and bits; vector ratio and depth; gluons; unit; 700/380
# ======================================================================
def seccion_37():
    import numpy as np
    from scipy.special import jn_zeros, j0, y0
    from scipy.optimize import brentq
    phi = (1 + 5 ** 0.5) / 2; L = np.log(phi); M = M_GEV
    S = np.pi * phi ** 12
    print(f"S(12) = {S:.2f} (nats, as in Gibbons-Hawking and Cardy); modes = {int(S)}; as Shannon bits: {int(S)*np.log(2):.1f} nats, log2 fraction = {np.log(2):.4f}")
    def ratio(depth):
        eps = phi ** (-depth); f = lambda x: j0(eps*x)*y0(x) - y0(eps*x)*j0(x)
        xs = np.linspace(0.5, 15, 6000); v = f(xs)
        r = [brentq(f, xs[i], xs[i+1]) for i in range(len(xs)-1) if v[i]*v[i+1] < 0]
        return r[1]/r[0], r[0]
    for lo, hi in ((-12, 12), (12, 36)):
        print(f"[{lo},{hi}]: m2/m1 = {ratio(hi-lo)[0]:.3f} (it depends only on the depth)")
    for d in (24, 81.74):
        r, x = ratio(d); print(f"background 12, depth {d}: first gluon {x*M*phi**12:.0f} GeV, graviton {jn_zeros(1,1)[0]*M*phi**12:.0f} GeV")
    for m in (3600, 4000):
        print(f"{m} GeV gluon: its background = {np.log(m/(jn_zeros(0,1)[0]*M))/L:.2f}")
    print(f"m_p/3 = 0.3128 GeV: sigma_IR = {np.log(99.6/0.3128)/L:.2f}")
    t = jn_zeros(1, 2); t = t[1]/t[0]; r = 700/380; e = r*np.hypot(20/700, 20/380)
    print(f"700/380 = {r:.4f} against {t:.4f}: {100*(r/t-1):.2f} %, {(r-t)/e:.2f} standard deviations")

    # the Hilbert space: the exact count grows as e^S (S in nats)
    import math
    Mx=3000; sg=[0]*(Mx+1)
    for d in range(1,Mx+1):
        for k in range(d,Mx+1,d): sg[k]+=d
    pp=[0]*(Mx+1); pp[0]=1
    for n in range(1,Mx+1): pp[n]=3*sum(sg[k]*pp[n-k] for k in range(1,n+1))//n
    X=[];Y=[]
    for s_ in range(3,10):
        L0=round(phi**(2*s_)/2); X.append(math.pi*math.sqrt(2*L0)); Y.append(math.log(pp[L0])+1.5*math.log(L0))
    print(f"ln W + (3/2) ln L0 = a S + b: a = {np.polyfit(X,Y,1)[0]:.4f} (S in nats: dim = e^S; in bits it would be a = 1/ln2 = 1.4427)")
    # W2: the integer dimension of the level, states with L0 <= N/2 (no rounding)
    cum=[0]
    for v in pp: cum.append(cum[-1]+v)
    Xs=[];Ys=[];Zs=[]; D={}
    for s_ in range(1,10):
        Lm=math.floor(phi**(2*s_)/2); D[s_]=cum[Lm+1]; Xs.append(math.pi*phi**s_); Ys.append(math.log(D[s_])); Zs.append(math.log(Lm))
    assert D[3]==1654 and D[4]==3436182 and D[5]==820599769985, D
    A_=np.vstack([Xs,Zs,np.ones(len(Xs))]).T[2:]; a_=np.linalg.lstsq(A_,np.array(Ys[2:]),rcond=None)[0][0]
    assert abs(a_-0.9972)<5e-4, a_
    print(f"W2: integer dimension (states with L0 <= N/2): sigma=3,4,5 -> {D[3]}, {D[4]}, {D[5]}; fit lnD = a S + b ln L + c (sigma=3..9): a = {a_:.4f}")
    from decimal import Decimal, getcontext; getcontext().prec=60
    PHd=(1+Decimal(5).sqrt())/2; PId=Decimal("3.14159265358979323846264338327950288419716939937510582097494459")
    vals=[(PId*PHd**s_/n_).exp() for s_ in range(0,13) for n_ in range(1,41)]
    vals=[x for x in vals if x<Decimal(10)**40]     # with 60 digits the fractional part is reliable below 10^40
    near=min(abs(x-x.to_integral_value()) for x in vals)
    assert near>Decimal("1e-9"), near
    print(f"e^(S/n) < 10^40 for sigma=0..12, n=1..40 ({len(vals)} cases): no integer (minimum distance {float(near):.2e}); Gelfond-Schneider: always transcendental")
    # the measure and the phase: with weight e^{2A}, the measure e^{4A} gives the zeros of J1; e^{6A}, a spacing with no offset
    from scipy.linalg import eigh
    def spec(pe, Q=32, lo=-6, hi=6, n=5):
        h=L/Q; w=np.arange(lo*Q,hi*Q+1)/Q*L; pm=np.exp(-pe*(w[:-1]+w[1:])/2); N=len(w); K=np.zeros((N,N))
        for i in range(N-1):
            c=pm[i]/h**2; K[i,i]+=c; K[i+1,i+1]+=c; K[i,i+1]-=c; K[i+1,i]-=c
        r=np.exp(-2*w); r[0]/=2; r[-1]/=2
        m=np.sqrt(np.clip(eigh(K,np.diag(r),eigvals_only=True),0,None)); return m[1:n+1]/m[1]
    z=jn_zeros(1,5); print("measure e^{4A}:", np.round(spec(4),4), " J1 zeros:", np.round(z/z[0],4))
    print("measure e^{6A}:", np.round(spec(6),4), " (integers: no offset)")

SECCIONES.append((37, 'Consistency: entropy, modes and bits; depth; gluons; unit; 700/380', seccion_37))

# ======================================================================
# 38. The 1/2 of (B1): area quantum, Fisher unit and Shannon bit
# ======================================================================
def seccion_38():
    import math
    G = 0.5; a = 1 / (4 * G)
    print(f"area law: {a} per ell^2 = {a/2} per ell_P^2 (Bekenstein-Hawking 1/4); Shannon bit ln2 = {math.log(2):.4f}")
    print(f"one Shannon bit per Planck area against the area law: ratio {math.log(2)/(a/2):.3f}; per ell^2: {math.log(2)/a:.3f}")
    print(f"area per unit of S (one mode): {1/a} ell^2 = {2/a} ell_P^2")

SECCIONES.append((38, 'The 1/2 of (B1): area quantum, Fisher unit and Shannon bit', seccion_38))

# ======================================================================
# 39. The throat with the Fibonacci tiling of its rings (Figure 4)
# ======================================================================
def seccion_39():
    """The section of the throat is the cusp; each ring is covered with long tiles (A) and short
    ones (B) by the substitution A->AB, B->A, with seed AAB at sigma=0. Before drawing it is
    checked: the boundaries of one ring continue into the next, and S = pi(A/phi^2 + B/phi^3) at
    every level. The tilt of the view, the distribution of the points and the scale of the loops
    are drawing conventions."""
    import numpy as np, math
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    phi=(1+5**.5)/2; L=math.log(phi); LEV=list(range(7))
    # ---- tiling: word of each ring (A long, B short), seed AAB at sigma=0
    words=["AAB"]
    for _ in range(6): words.append("".join({"A":"AB","B":"A"}[c] for c in words[-1]))
    def bounds(w):  # fronteras en fraccion de vuelta
        wid=[1 if c=="A" else 1/phi for c in w]; c=np.cumsum([0]+wid); return c/c[-1]
    for s in range(6):   # every boundary of a ring is a boundary of the next (they nest)
        b0,b1=bounds(words[s]),bounds(words[s+1]); assert all(np.min(abs(b1-x))<1e-12 for x in b0)
    rows=[]
    for s in LEV:
        A=words[s].count("A"); B=words[s].count("B"); S=math.pi*phi**s
        Sw=math.pi*(A/phi**2+B/phi**3); assert abs(Sw-S)<1e-9*S
        rows.append(dict(s=s,S=S,modes=int(S),N=phi**(2*s),A=A,B=B,w=words[s]))
    print("rings:",[(r['A'],r['B']) for r in rows],"; S = pi(A/phi^2+B/phi^3) exact; boundaries nested")
    # ---- throat (pseudosphere), as in Figure 4
    ys=np.linspace((LEV[0]-6.6)*L,0,2000); r=np.exp(ys)
    h=np.concatenate([[0],np.cumsum(np.sqrt(np.clip(1-r[1:]**2,0,None))*np.diff(ys))]); h=h-h[-1]
    H=lambda y: np.interp(y,ys,h); k=0.16
    def P3(rad,hh,th): return rad*np.cos(th), hh+k*rad*np.sin(th)
    fig=plt.figure(figsize=(11.0,11.69)); ax=fig.add_axes([0.02,0.02,0.96,0.96]); ax.set_aspect('equal'); ax.axis('off')
    ax.plot(np.exp(ys),h,'k',lw=1.2); ax.plot(-np.exp(ys),h,'k',lw=1.2)
    hb=H((LEV[0]-6)*L); ht=H(0.0); dl=(ht-hb)/6
    LAB={s:hb+(ht-hb)*s/6 for s in LEV}
    XL=1.33; XD=2.05; WD=0.95; HD=0.42*dl
    for row in rows:
        s=row['s']; y=(s-6)*L; rad=math.exp(y); hh=H(y)
        th=np.linspace(0,2*math.pi,400); x,yy=P3(rad,hh,th)
        ax.plot(np.where(np.sin(th)<0,x,np.nan),yy,'k',lw=1.0); ax.plot(np.where(np.sin(th)>=0,x,np.nan),yy,'k',lw=0.6,alpha=0.6)
        for j in range(row['modes']):                  # modes
            a=2*math.pi*j/row['modes']; x0,y0=P3(rad*1.07,hh,a); ax.plot(x0,y0,'ko',ms=1.5)
        # boundaries of the tiles: meridians of ring s to ring s+1 over the surface
        if s<6:
            yseg=np.linspace(y,y+L,30)
            for bnd in bounds(row['w'])[:-1]:
                a=2*math.pi*bnd-math.pi/2; xs,hs=np.exp(yseg)*np.cos(a),H(yseg)+k*np.exp(yseg)*np.sin(a)
                ax.plot(xs,hs,'k',lw=0.45 if math.sin(a)<0 else 0.3,ls='-' if math.sin(a)<0 else ':')
        ly=LAB[s]
        ax.text(-2.05,ly,f"σ = {s}\nS = {row['S']:.2f},  ⌊S⌋ = {row['modes']}\nN = {row['N']:.1f}\ntiles = {row['A']+row['B']} ({row['A']} long, {row['B']} short)",fontsize=6.2,va='center',family='serif')
        ax.plot([-1.32,-rad*1.08],[ly,hh],'k:',lw=0.4)
        # the ring unrolled at the same width: long tiles shaded, short ones white
        b=bounds(row['w'])
        for i,c in enumerate(row['w']):
            x0=XD+WD*b[i]; x1=XD+WD*b[i+1]
            ax.add_patch(plt.Rectangle((x0,ly-HD/2),x1-x0,HD,facecolor='0.75' if c=='A' else 'white',edgecolor='k',lw=0.3))
    # the string and the loops, as in Figure 4
    sg=np.linspace(LEV[0],LEV[-1],600); yy=(sg-6)*L; thh=-math.pi/2+sg*L
    xs=np.exp(yy)*np.cos(thh); hs=H(yy)+k*np.exp(yy)*np.sin(thh); front=np.sin(thh)<0
    ax.plot(np.where(front,xs,np.nan),hs,'k',lw=1.1); ax.plot(np.where(~front,xs,np.nan),hs,'k--',lw=0.8)
    for row in rows:
        s=row['s']; y=(s-6)*L; t=-math.pi/2+s*L; px=math.exp(y)*math.cos(t); py=H(y)+k*math.exp(y)*math.sin(t)
        rho=0.40*dl*phi**(-s); ly=LAB[s]; a=np.linspace(0,2*math.pi,100)
        ax.plot(XL+rho*np.cos(a),ly+rho*np.sin(a),'k',lw=0.6); ax.plot([px,XL-rho],[py,ly],'k:',lw=0.4); ax.plot([XL+rho,XD-0.03],[ly,ly],'k:',lw=0.3)
    xc=(-2.05+XD+WD)/2
    ax.text(xc,H(0)+0.38,"The throat with the tiling of its rings",ha='center',fontsize=11,family='serif')
    ax.text(XL,ht+0.62*dl,"half-turn loop",ha='center',fontsize=6.3,family='serif',style='italic')
    ax.text(XD+WD/2,ht+0.62*dl,"the ring, unrolled at equal width",ha='center',fontsize=6.3,family='serif',style='italic')
    ax.set_xlim(-2.1,XD+WD+0.05); ax.set_ylim(H((LEV[0]-6.6)*L)-0.05,H(0)+0.5)
    fig.savefig("fig_throat_tiling.pdf",bbox_inches="tight",pad_inches=0.05)


SECCIONES.append((39, 'The throat with the Fibonacci tiling of its rings (Figure 4)', seccion_39))

# ======================================================================
# 40. The dictionary on a regular tiling against the cusp
# ======================================================================
def seccion_40():
    """A lattice on a regular tiling {p,q} cut at the level sigma: open legs against S
    (Crofton), pairs (tiling, chi) that give S on average; the cusp: metric, two prototiles,
    uniqueness of the substitution, exact weighted sum, equivalent chi; the count of points of
    Z[i] from §11.1."""
    import numpy as np, math, itertools
    from decimal import Decimal, getcontext; getcontext().prec=60
    phi=(1+5**.5)/2
    def circ(a,b):
        A=np.array([[2*a.real,2*a.imag],[2*b.real,2*b.imag]]); c=complex(*np.linalg.solve(A,[abs(a)**2+1,abs(b)**2+1]))
        return c, math.sqrt(abs(c)**2-1)
    def refl(z,a,b):
        if abs((np.conj(a)*b).imag)<1e-12:
            u=(a if abs(a)>1e-12 else b); u=u/abs(u); return u*u*np.conj(z)
        c,r=circ(a,b); return c+r*r/np.conj(z-c)
    def hcenter(P):
        K=2*P/(1+abs(P)**2); k=K.mean(); return k/(1+math.sqrt(max(0,1-abs(k)**2)))
    def hd(z): return 2*math.atanh(min(abs(z),1-1e-15))
    def radii(p,q):
        R=math.acosh(1/(math.tan(math.pi/p)*math.tan(math.pi/q)))   # circumradius
        r=math.acosh(math.cos(math.pi/q)/math.sin(math.pi/p))         # inradius
        e=2*math.acosh(math.cos(math.pi/p)/math.sin(math.pi/q))       # edge
        return R,r,e
    def P0(p,q,center='tile'):
        R,_,_=radii(p,q); t=math.tanh(R/2)
        P=np.array([t*np.exp(2j*math.pi*(k+.5)/p) for k in range(p)]) if center=='tile' else np.array([t*np.exp(2j*math.pi*k/p) for k in range(p)])
        if center=='vertex':
            v=P[0]; P=(P-v)/(1-np.conj(v)*P); P[0]=0j
        return P
    def key(P): c=hcenter(P); return (round(c.real,6),round(c.imag,6))
    def tiles_within(p,q,Rmax,center='tile',with_centres=False):
        """all tiles whose centre is at distance <= Rmax+margin (BFS over edges with pruning).
        The centre of each tile is reflected together with its vertices, so it is exact."""
        Rc,_,_=radii(p,q); A=P0(p,q,center)
        c0=0j if center=='tile' else complex(-math.tanh(Rc/2),0)
        A=np.append(A,c0); kf=lambda P:(round(P[-1].real,8),round(P[-1].imag,8))
        seen={kf(A)}; fr=[A]; out=[A]; lim=Rmax+Rc+0.2
        while fr:
            new=[]
            for P in fr:
                for k in range(p):
                    Q=np.array([refl(z,P[k],P[(k+1)%p]) for z in P]); kk=kf(Q)
                    if kk in seen: continue
                    seen.add(kk)
                    if hd(Q[-1])<=lim: new.append(Q)
            out+=new; fr=new
        T=[P[:-1] for P in out]; C=np.array([P[-1] for P in out])
        return (T,C) if with_centres else T
    def edge_layers(p,q,depth=7,cap=6000):
        A=P0(p,q); seen={key(A)}; fr=[A]; L=[1]
        for _ in range(depth):
            new=[]
            for P in fr:
                for k in range(p):
                    Q=np.array([refl(z,P[k],P[(k+1)%p]) for z in P]); kk=key(Q)
                    if kk not in seen: seen.add(kk); new.append(Q)
            L.append(len(new)); fr=new
            if len(new)>cap: break
        return L

    def edges(T):
        E={}
        for P in T:
            for j in range(len(P)):
                a,b=P[j],P[(j+1)%len(P)]
                E[tuple(sorted([(round(a.real,7),round(a.imag,7)),(round(b.real,7),round(b.imag,7))]))]=(a,b)
        return list(E.values())
    def crossings(E,R):
        n=0
        for a,b in E:
            da,db=hd(a),hd(b)
            if (da<R)!=(db<R): n+=1; continue
            if da>R and db>R and abs((np.conj(a)*b).imag)>1e-12:
                c,rc=circ(a,b); ft=c/abs(c)*(abs(c)-rc); an=lambda z: np.angle((z-c)/(-c)); lo,hi=sorted([an(a),an(b)])
                if lo<=0<=hi and hd(ft)<R: n+=2
        return n
    SIG=list(range(13)); RL=[math.asinh(phi**s) for s in SIG]; S=[math.pi*phi**s for s in SIG]
    E=edges(tiles_within(7,3,RL[-1]+0.05)); n=[crossings(E,R) for R in RL]
    assert n==[7,14,28,35,56,84,133,217,350,567,938,1484,2443], n
    R_,r_,e_=radii(7,3); cro=4*(7*e_/2)/(math.pi/3)/math.pi
    print("  {7,3}: open legs",n); print("  legs/S",[round(a/b,3) for a,b in zip(n,S)],"; Crofton constant",round(cro,4))
    L=[]; best=(9,None)
    for p in range(3,61):
        for q in range(3,61):
            if (p-2)*(q-2)<=4: continue
            R_,r_,e_=radii(p,q); A=(p-2)*math.pi-p*2*math.pi/q; c=4*(p*e_/2)/A/math.pi
            for chi in range(2,17):
                d=abs(c*math.log(chi)-1); L.append(d)
                if d<best[0]: best=(d,(p,q,chi))
    tol=[sum(x<t for x in L) for t in (1e-2,1e-3,1e-4,1e-5,1e-6)]
    assert len(L)==50340 and tol==[172,22,2,1,0] and best[1]==(20,3,3), (len(L),tol,best)
    print("  pairs (tiling, chi<=16), p,q<=60:",len(L),"; closer than 1e-2..1e-6:",tol,"; best",best[1],f"at {best[0]:.2e}")
    for yy in (-3.0,0.0,1.7): assert abs(math.exp(-yy)**2*math.exp(2*yy)-1)<1e-12
    print("  cusp: t=e^-y gives (dth^2+dt^2)/t^2 = e^(2y)dth^2+dy^2; level s at t=phi^-s, length 2pi phi^s, distance log phi")
    a0=2*math.pi/phi**2
    for s in (0,3,7):
        t=phi**-s
        for top,area in ((a0,a0/phi),(a0/phi,a0/phi**2)):
            dx=top*t; assert abs(dx*(phi/t-1/t)-area)<1e-12 and abs(dx/(t/phi)-phi*top)<1e-12
    print("  two prototiles, equal at every level: areas",round(a0/phi,6),"and",round(a0/phi**2,6))
    subs=[m for m in itertools.product(range(10),repeat=4) if m[0]+m[3]==1 and m[0]*m[3]-m[1]*m[2]==-1]
    assert subs==[(0,1,1,1),(1,1,1,0)]; print("  two-tile substitutions with eigenvalue phi:",subs)
    PI=Decimal("3.14159265358979323846264338327950288419716939937510582097494459"); ph=(1+Decimal(5).sqrt())/2
    A,B=2,1
    for s in range(41):
        assert abs(PI/ph**2*A+PI/ph**3*B-PI*ph**s)<Decimal(10)**-45; A,B=A+B,A
    print("  S = pi(A/phi^2 + B/phi^3) exact (60 digits) for s = 0..40; tiles/S ->",round(phi**4/5**.5/math.pi,4))
    print("  equivalent chi: e^(pi/phi^2) =",round(math.exp(math.pi/phi**2),3),", e^(pi/phi^3) =",round(math.exp(math.pi/phi**3),3))
    # count with fixed weights: arcs between cuts on the level circles of {7,3} (the throat: two weights)
    def mob(z_,w): return (z_-w)/(1-np.conj(w)*z_)
    def imob(z_,w): return (z_+w)/(1+np.conj(w)*z_)
    E9=edges(tiles_within(7,3,RL[9]+0.05)); nw=[]; allw=set()
    for sg in range(10):
        R=RL[sg]; rho=math.tanh(R/2); ang=[]
        for a,b in E9:
            if min(hd(a),hd(b))>R+0.01 and abs((np.conj(a)*b).imag)>1e-12:
                c,rc=circ(a,b)
                if 2*math.atanh(min(abs(c)-rc,1-1e-15))>R+0.01: continue
            bb=mob(b,a); zz=np.linspace(0,1,300); g=imob(zz*bb,a); sgn=np.sign(abs(g)-rho)
            for kk in np.where(np.diff(sgn)!=0)[0]:
                t0,t1=zz[kk],zz[kk+1]
                for _ in range(50):
                    tm=(t0+t1)/2
                    if (abs(imob(t0*bb,a))-rho)*(abs(imob(tm*bb,a))-rho)<=0: t1=tm
                    else: t0=tm
                ang.append(np.angle(imob(t0*bb,a))%(2*math.pi))
        ang=sorted(set(round(x,9) for x in ang)); d=np.diff(ang+[ang[0]+2*math.pi])
        w=set(round(math.sinh(R)*x/2,6) for x in d); allw|=w; nw.append(len(w))
        assert abs(sum(math.sinh(R)*x/2 for x in d)-S[sg])<1e-6
    assert nw==[1,2,3,3,5,7,10,16,27,41] and len(allw)==115, (nw,len(allw))
    print("  {7,3}: distinct weights (arc between cuts x 1/2) per level",nw,", 115 in total; the throat: 2 at every level")
    # the 1/2 of each statement: the constant of the definition places it
    fstar={c_:[f for f in np.linspace(0.001,1,99901) if abs(1/math.sqrt(c_*f)-1)<1e-4] for c_ in (1.5,2,3)}
    assert all(abs(np.mean(v)-1/c_)<1e-3 for c_,v in fstar.items())
    mstar={k_:1/math.sqrt(k_) for k_ in (2,4,8)}; assert abs(mstar[4]-0.5)<1e-15
    ps=np.linspace(0.01,0.99,9801); Hb=-(ps*np.log2(ps)+(1-ps)*np.log2(1-ps)); assert abs(ps[np.argmax(Hb)]-0.5)<1e-9
    print("  tau_D/sqrt(c f)=tau_D gives f=1/c (c=2 in CW6: 1/2); k mu^2=1 gives mu=1/sqrt(k) (k=4, quantum Fisher: 1/2); binary entropy: 1/2 without the constant")
    def lattice(r2):
        R=int(math.isqrt(int(r2)))+1; return sum(1 for x in range(-R,R+1) for y in range(-R,R+1) if x*x+y*y<=r2)
    cnt=[lattice(phi**s) for s in range(7)]; assert cnt==[5,5,9,13,21,37,57], cnt
    c12=lattice(phi**12); assert c12==1005
    rat=[round(c/(math.pi*phi**s),2) for s,c in enumerate(cnt)]; r22=lattice(phi**22)/(math.pi*phi**22)
    print("  points of Z[i] (§11.1):",cnt,"; points/S",rat,"; sigma=12:",c12,"against floor S = 1011; sigma=22:",round(r22,4))

SECCIONES.append((40, 'The dictionary on a regular tiling against the cusp', seccion_40))

# ======================================================================
# 41. Five regular tilings against the levels (Figure 5)
# ======================================================================
def seccion_41():
    """Five {p,q} tilings of discs of radius arcsinh phi^sigma, exact centres (reflected with the
    vertices): tiles inside each disc, tangencies of one level's boundary with edges, and why a
    count does not follow phi: the Fibonacci ratios approach phi as 1/(sqrt5 q^2) and no further."""
    import math, numpy as np, matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    phi=(1+5**.5)/2
    def circ(a,b):
        A=np.array([[2*a.real,2*a.imag],[2*b.real,2*b.imag]]); c=complex(*np.linalg.solve(A,[abs(a)**2+1,abs(b)**2+1]))
        return c, math.sqrt(abs(c)**2-1)
    def refl(z,a,b):
        if abs((np.conj(a)*b).imag)<1e-12:
            u=(a if abs(a)>1e-12 else b); u=u/abs(u); return u*u*np.conj(z)
        c,r=circ(a,b); return c+r*r/np.conj(z-c)
    def hcenter(P):
        K=2*P/(1+abs(P)**2); k=K.mean(); return k/(1+math.sqrt(max(0,1-abs(k)**2)))
    def hd(z): return 2*math.atanh(min(abs(z),1-1e-15))
    def radii(p,q):
        R=math.acosh(1/(math.tan(math.pi/p)*math.tan(math.pi/q)))   # circumradius
        r=math.acosh(math.cos(math.pi/q)/math.sin(math.pi/p))         # inradius
        e=2*math.acosh(math.cos(math.pi/p)/math.sin(math.pi/q))       # edge
        return R,r,e
    def P0(p,q,center='tile'):
        R,_,_=radii(p,q); t=math.tanh(R/2)
        P=np.array([t*np.exp(2j*math.pi*(k+.5)/p) for k in range(p)]) if center=='tile' else np.array([t*np.exp(2j*math.pi*k/p) for k in range(p)])
        if center=='vertex':
            v=P[0]; P=(P-v)/(1-np.conj(v)*P); P[0]=0j
        return P
    def key(P): c=hcenter(P); return (round(c.real,6),round(c.imag,6))
    def tiles_within(p,q,Rmax,center='tile',with_centres=False):
        """all tiles whose centre is at distance <= Rmax+margin (BFS over edges with pruning).
        The centre of each tile is reflected together with its vertices, so it is exact."""
        Rc,_,_=radii(p,q); A=P0(p,q,center)
        c0=0j if center=='tile' else complex(-math.tanh(Rc/2),0)
        A=np.append(A,c0); kf=lambda P:(round(P[-1].real,8),round(P[-1].imag,8))
        seen={kf(A)}; fr=[A]; out=[A]; lim=Rmax+Rc+0.2
        while fr:
            new=[]
            for P in fr:
                for k in range(p):
                    Q=np.array([refl(z,P[k],P[(k+1)%p]) for z in P]); kk=kf(Q)
                    if kk in seen: continue
                    seen.add(kk)
                    if hd(Q[-1])<=lim: new.append(Q)
            out+=new; fr=new
        T=[P[:-1] for P in out]; C=np.array([P[-1] for P in out])
        return (T,C) if with_centres else T
    def edge_layers(p,q,depth=7,cap=6000):
        A=P0(p,q); seen={key(A)}; fr=[A]; L=[1]
        for _ in range(depth):
            new=[]
            for P in fr:
                for k in range(p):
                    Q=np.array([refl(z,P[k],P[(k+1)%p]) for z in P]); kk=key(Q)
                    if kk not in seen: seen.add(kk); new.append(Q)
            L.append(len(new)); fr=new
            if len(new)>cap: break
        return L

    REC={}
    def geod(a,b,n=30):
        m=lambda z,w:(z-w)/(1-np.conj(w)*z); mi=lambda z,w:(z+w)/(1+np.conj(w)*z)
        bb=m(b,a); t=np.linspace(0,1,n); return mi(t*bb,a)
    C=[(7,3,'{7,3}: heptagons'),(3,7,'{3,7}: triangles'),(5,4,'{5,4}: pentagons'),(12,5,'{12,5}: dodecagons'),(6,10,'{6,10}: hexagons')]
    fig,axs=plt.subplots(5,7,figsize=(14,10.5))
    for i,(p,q,nm) in enumerate(C):
        T,Cc=tiles_within(p,q,math.asinh(phi**6)+0.5,'tile',True); d=[hd(x) for x in Cc]
        for s in range(7):
            ax=axs[i,s]; Rh=math.asinh(phi**s); sc=1/math.tanh(Rh/2); n=0
            for P,dd in zip(T,d):
                if dd<=Rh: n+=1
                if dd>Rh+2.5: continue
                for j in range(p):
                    g=geod(P[j],P[(j+1)%p])*sc; g=np.where(abs(g)<=1,g,np.nan); ax.plot(g.real,g.imag,'k',lw=0.35)
            t=np.linspace(0,2*math.pi,300); ax.plot(np.cos(t),np.sin(t),'k',lw=1)
            S=math.pi*phi**s
            for j in range(int(S)): a=2*math.pi*j/int(S); ax.plot(1.12*math.cos(a),1.12*math.sin(a),'ko',ms=1.5)
            ax.set_aspect('equal'); ax.axis('off'); ax.set_xlim(-1.2,1.2); ax.set_ylim(-1.2,1.2)
            tg=0
            for P in T:
                for j in range(p):
                    a_,b_=P[j],P[(j+1)%p]
                    if abs((np.conj(a_)*b_).imag)<1e-12: continue
                    c_,rc_=circ(a_,b_); ft=c_/abs(c_)*(abs(c_)-rc_); an=lambda z: np.angle((z-c_)/(-c_)); lo,hi=sorted([an(a_),an(b_)])
                    if lo-1e-12<=0<=hi+1e-12 and abs(hd(ft)-Rh)<1e-9: tg+=1
            REC[(p,q,s)]=(n,tg//2)
            ax.set_title(f"σ={s}, tiles={n}"+(f"\nboundary tangent to {tg//2} edges" if tg else ""),fontsize=7,family='serif',color='k')
        axs[i,0].text(-1.5,0,nm,rotation=90,va='center',ha='right',fontsize=9,family='serif')
    fig.tight_layout(); fig.savefig('fig_tilings_strip.pdf',bbox_inches='tight',pad_inches=0.05)

    assert [REC[(7,3,s)][0] for s in range(7)]==[1,8,8,29,29,57,99]
    assert [REC[(12,5,s)][0] for s in range(7)]==[1]*7
    assert [REC[(6,10,s)][1] for s in range(7)]==[0,6,0,12,0,0,0], [REC[(6,10,s)][1] for s in range(7)]
    assert all(REC[(p,q,s)][1]==0 for (p,q,s) in REC if (p,q)!=(6,10))
    print("  tiles whose centre falls inside each disc:")
    for (p,q) in [(7,3),(3,7),(5,4),(12,5),(6,10)]: print(f"    {{{p},{q}}}:",[REC[(p,q,s)][0] for s in range(7)])
    print("  boundary of a level tangent to edges: only {6,10}, sigma=1 (6 edges) and sigma=3 (12 edges)")
    F=[1,1]
    for _ in range(40): F.append(F[-1]+F[-2])
    dev=[abs(phi-F[n+1]/F[n])*5**.5*F[n]**2 for n in range(5,30)]
    assert all(abs(x-1)<0.05 for x in dev[5:])
    print("  Fibonacci ratios: |phi - F(n+1)/F(n)| * sqrt5 * F(n)^2 ->",round(dev[-1],6),"(Hurwitz: phi is the worst approximant)")
    T37,C37=tiles_within(3,7,7.5,'tile',True); vk=lambda z:(round(z.real,7),round(z.imag,7)); VV={}
    for i_,P in enumerate(T37):
        for z in P: VV.setdefault(vk(z),[]).append(i_)
    lay=[{0}]; seen={0}
    for _ in range(6):
        nxt=set()
        for i_ in lay[-1]:
            for z in T37[i_]:
                for j_ in VV[vk(z)]:
                    if j_ not in seen: nxt.add(j_)
        seen|=nxt; lay.append(nxt)
    nl=[len(x) for x in lay]; assert nl==[1,15,45,120,315,825,2160], nl
    print("  {3,7} by shared vertices:",nl,"-> phi^2; by edges ~1.6")
    from decimal import Decimal, getcontext; getcontext().prec=80
    def hconst(X,N=60):
        h0,h1,k0,k1=0,1,1,0; y=X; out=[]
        for i_ in range(N):
            a_=int(y); h0,h1=h1,a_*h1+h0; k0,k1=k1,a_*k1+k0
            if i_>5: out.append(float(abs(X-Decimal(h1)/Decimal(k1))*k1*k1))
            y=1/(y-a_)
        return min(out[-10:])
    PH=(1+Decimal(5).sqrt())/2
    cls=[hconst(x) for x in (PH,1/PH,PH+1)]; assert all(abs(c-1/5**.5)<1e-4 for c in cls)
    assert hconst(Decimal(2).sqrt())<0.36
    print("  Hurwitz: phi, 1/phi, phi+1 ->",[round(c,5) for c in cls],"= 1/sqrt5; sqrt2 ->",round(hconst(Decimal(2).sqrt()),5))
    gr={}
    for (p_,q_) in [(7,3),(3,7),(5,4),(12,5),(6,10)]:
        Lq=edge_layers(p_,q_,depth=7,cap=3000); gr[(p_,q_)]=Lq[-1]/Lq[-2]
    assert abs(gr[(7,3)]-phi**2)<1e-3 and abs(gr[(5,4)]-phi**2)<1e-3 and abs(gr[(3,7)]-1.6)<0.05 and gr[(12,5)]>10 and abs(gr[(6,10)]-5)<0.05, gr
    R_,r_,e_=radii(5,4); assert abs(math.cosh(e_)-phi)<1e-12
    R_,r_,e_=radii(6,10); assert abs(math.sinh(r_)-phi)<1e-12
    R_,r_,e_=radii(5,4); c54=4*(5*e_/2)/(math.pi/2)/math.pi; assert abs(c54*math.log(2)-1.4907)<1e-3
    print("  growth per layer (edges):",{k:round(v,3) for k,v in gr.items()},"; {5,4}: cosh e = phi; {6,10}: sinh r = phi; {5,4} with qubits:",round(c54*math.log(2),4),"S")


SECCIONES.append((41, 'Five regular tilings against the levels (Figure 5)', seccion_41))

# ======================================================================
# 42. The two coordinates, the level step, the orthogonalization, the rational step and the imp:A1 operator
# ======================================================================
def seccion_42():
    import math
    phi = (1 + 5 ** 0.5) / 2; psi = -1 / phi; L = math.log(phi)
    M = 6 * math.sqrt(3) * math.pi / L
    F = [0, 1]
    for _ in range(40): F.append(F[-1] + F[-2])
    # I1: the time of the weld is the second Galois coordinate
    for s_ in (1, 2, 3, 6, 12):
        a, b = F[s_ - 1], F[s_]
        assert a * a + a * b - b * b == (-1) ** s_
        assert abs(M * abs(a + b * psi) - M * phi ** -s_) < 1e-9
    print(f"  I1: M|a + b phibar| = M phi^-s = tau(s) at s = 1, 2, 3, 6, 12; tau(12) = {M*phi**-12:.4f}, phi^12 = 89 + 144 phi, norm +1")
    # I2: the matrix of the substitution is the exchange followed by a shift
    ex = [[0, 1], [1, 0]]; sh = [[1, 0], [1, 1]]
    prod = [[sum(ex[i][k] * sh[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    assert prod == [[1, 1], [1, 0]]
    print("  I2: [[0,1],[1,0]] [[1,0],[1,1]] =", prod, "= matrix of A -> AB, B -> A")
    # I3: ring s is labelled by the unit phi^{s+3} and is a periodic approximant
    def sub(w): return "".join("AB" if c == "A" else "A" for c in w)
    w = "AAB"; ok = True
    for s_ in range(12):
        if (w.count("B"), w.count("A")) != (F[s_ + 2], F[s_ + 3]): ok = False
        ap = "A"
        for _ in range(s_ + 2): ap = sub(ap)
        if not (len(ap) == len(w) and ap in w + w): ok = False
        w = sub(w)
    assert ok
    print("  I3: ring s, s = 0..11: (B, A) = (F_{s+2}, F_{s+3}), coefficients of phi^{s+3}; word = rotation of s^{s+2}(A)")
    # I4: orthogonalization at the half turn
    for p_ in (0.3, 0.5, 0.7):
        ov = abs((1 - p_) + p_ * complex(math.cos(math.pi), math.sin(math.pi)))
        assert (ov < 1e-12) == (p_ == 0.5)
    e0 = L / (6 * math.sqrt(3))
    assert all(abs(e0 * phi ** s_ * M * phi ** -s_ - math.pi) < 1e-12 for s_ in range(20))
    print("  I4: eps(s) tau(s) = pi at every level; overlap at the half turn 1 - 2p: 0.4, 0, 0.4 at p = 0.3, 0.5, 0.7")
    # I5: the rational step against the comparison
    out = []
    for p_, q_ in [(21, 13), (34, 21), (55, 34), (89, 55), (144, 89), (233, 144)]:
        f = L / math.log(p_ / q_)
        out.append((p_, q_, abs(11.97 * f - 11.97) / 0.05, abs(583.789 * f - 583.789) / 0.028))
    assert out[0][3] > 70 and out[3][3] > 3 and out[4][3] < 3
    print("  I5: step p/q -> deviations (background, observer):", ", ".join(f"{a}/{b}: {x:.1f}, {y:.1f}" for a, b, x, y in out))
    # I6: the trace 3 and the shortest geodesic
    assert abs(phi ** 2 + phi ** -2 - 3) < 1e-12 and abs(2 * math.acosh(1.5) - 4 * L) < 1e-12
    print(f"  I6: tr [[2,1],[1,1]] = 3 = phi^2 + phi^-2; length 2 arccosh(3/2) = {2*math.acosh(1.5):.6f} = 4 log phi")
    # I7: the imp:A1 operator with n = 6
    n = 6; m = [2 * math.sin(k * math.pi / (4 * (n + 1))) / L for k in range(1, 2 * n + 2)]
    r = [m[k + 1] / m[k] for k in range(len(m) - 1)]
    assert all(abs(x - phi) > 0.05 for x in r)
    print("  I7: ratios of successive masses of imp:A1, n = 6:", [round(x, 2) for x in r], "; none is phi")

SECCIONES.append((42, 'The two coordinates, the level step, the orthogonalization, the rational step and the imp:A1 operator', seccion_42))

# ======================================================================
# 43. The three columns and why they did not fit: R11, the diagonal of the cube, the rational kernel, Bragg
# ======================================================================
def seccion_43():
    import math, itertools
    import numpy as np
    phi = (1 + 5 ** 0.5) / 2
    # R11: primitive two-letter substitutions with entries <= 3
    ok123 = set(); ok4 = set()
    for a, b, c, d in itertools.product(range(4), repeat=4):
        if b == 0 or c == 0: continue
        tr, de = a + d, a * d - b * c; disc = tr * tr - 4 * de
        if disc <= 0: continue
        r = math.sqrt(disc); lam = (tr + r) / 2; mu = (tr - r) / 2
        if int(round(r)) ** 2 != disc and abs(de) == 1 and abs(mu) < 1:
            ok123.add(round(lam, 4))
            if (tr, de) == (1, -1): ok4.add(round(lam, 4))
    assert round(1 + 2 ** 0.5, 4) in ok123 and ok4 == {round(phi, 4)}
    print("  C1-C3 (irrational, unimodular, Pisot):", sorted(ok123), "; with the additive law:", sorted(ok4))
    # the diagonal of the cube
    n = np.array([1, 1, 1]) / 3 ** 0.5; P = [e - (e @ n) * n for e in np.eye(3)]
    ang = {round(math.degrees(math.acos(P[i] @ P[j] / (np.linalg.norm(P[i]) * np.linalg.norm(P[j])))), 6) for i, j in [(0, 1), (1, 2), (0, 2)]}
    assert ang == {120.0} and np.allclose(sum(P), 0)
    print(f"  Z^3 along (1,1,1): three axes of length {np.linalg.norm(P[0]):.4f} at 120 degrees (hexagonal lattice, Z[omega] at scale sqrt(2/3)); the kernel is Z(1,1,1)")
    # kernel of the rational projection
    def coll(slope):
        seen = set(); c = 0
        for m in range(-60, 61):
            for k in range(-60, 61):
                v = round(m + k * slope, 9)
                if v in seen: c += 1
                seen.add(v)
        return c
    c32, cphi = coll(1.5), coll(phi)
    assert c32 == 14042 and cphi == 0
    print(f"  Z^2 -> line, pairs in [-60,60]^2: slope 3/2 -> {c32} collisions; slope phi -> {cphi}")
    # Bragg of the Fibonacci chain
    w = "A"
    for _ in range(22): w = "".join("AB" if ch == "A" else "A" for ch in w)
    x = np.concatenate([[0], np.cumsum([phi if ch == "A" else 1.0 for ch in w])])[:-1]
    amp = lambda k: abs(np.exp(2j * math.pi * k * x).sum()) / len(x)
    D = phi + 2
    pk = {(m_, n_): amp((m_ + n_ * phi) / D) for m_, n_ in [(2, 3), (1, 2), (1, 1)]}
    rng = np.random.default_rng(1); rnd = max(amp(k) for k in rng.uniform(0.05, 2.5, 200))
    assert pk[(2, 3)] > 0.9 and pk[(1, 2)] > 0.85 and pk[(1, 1)] > 0.65 and rnd < 0.02
    F = [0, 1]
    for _ in range(40): F.append(F[-1] + F[-2])
    for sg in range(0, 25):
        S = math.pi * phi ** sg; d_ = F[sg + 4] - phi ** 4 * S / (5 ** 0.5 * math.pi)
        assert abs(abs(d_) - phi ** -(sg + 4) / 5 ** 0.5) < 1e-6
    print("  tile count: F_{s+4} - 0.9757 S = +-phi^-(s+4)/sqrt5 exact (Binet, Pisot), s = 0..24")
    print(f"  Bragg (N = {len(x)}): (2,3) {pk[(2,3)]:.2f}, (1,2) {pk[(1,2)]:.2f}, (1,1) {pk[(1,1)]:.2f}; 200 random points: max {rnd:.3f}")

SECCIONES.append((43, 'The three columns and why they did not fit', seccion_43))


# ======================================================================
# 44. The Background figure: one structure seen at once (Figure 1)
# ======================================================================
def seccion_44():
    """Background figure (fig:background): the torus and the third direction; from the diagonal to
    the face; each dimension from the next one up; the rings of the throat tiled. Every statement
    drawn is checked."""
    import numpy as np, math, itertools, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    plt.rcParams.update({"font.family":"serif","mathtext.fontset":"cm","font.size":9})
    phi=(1+5**.5)/2; pb=(1-5**.5)/2; L=math.log(phi); M=6*3**.5*math.pi/L
    INK="#333333"; RED="#c0392b"; BLU="#2f6db3"; GOLD="#c99a2e"; GRN="#2e8b57"; TEAL="#5aa6a6"; VIO="#7b4fa0"
    t=np.linspace(0,2*np.pi,300); w=np.exp(2j*np.pi/3)
    fig=plt.figure(figsize=(17,21))
    def head(x,y,txt,sub,col=INK):
        fig.text(x,y,txt,ha="center",va="top",fontsize=12,color=col); fig.text(x,y-0.0105,sub,ha="center",va="top",fontsize=9,color="0.4")
    def band(y,txt): fig.text(0.5,y,txt,ha="center",va="top",fontsize=12.5,color=INK,style="italic")
    def sep(y): fig.add_artist(Line2D([0.04,0.96],[y,y],color="0.85",lw=.8))
    X3=(0.17,0.50,0.83)
    fig.suptitle("One structure, seen at once",fontsize=15,y=0.995)

    # ======== row 1: the third direction, on |z| = 1/2
    band(0.975,"The torus and the third direction")
    TRI=[("P",RED,0),("C",GRN,1),("F",BLU,2)]; R=0.5; V3=[R*w**k for k in range(3)]
    assert np.allclose([abs(v) for v in V3],0.5)
    def clean3d(ax,lim,zl):
        ax.set_xlim(-lim,lim); ax.set_ylim(-lim,lim); ax.set_zlim(-zl,zl); ax.set_axis_off(); ax.view_init(20,-120)
    axT=fig.add_axes([0.01,0.795,0.32,0.155],projection="3d")
    def cliff(a,b):
        Xc=np.stack([np.cos(a),np.sin(a),np.cos(b),np.sin(b)])/np.sqrt(2); return Xc[:3]/(1-Xc[3])
    aa,bb=np.meshgrid(np.linspace(0,2*np.pi,40),np.linspace(0,2*np.pi,40)); Pc=cliff(aa,bb)
    assert np.allclose((np.hypot(Pc[0],Pc[1])-np.sqrt(2))**2+Pc[2]**2,1,atol=1e-9)
    wv=np.linspace(0,2*np.pi,400); KK=dict(color="k",lw=0.35)
    for c_ in np.linspace(0,2*np.pi,24,endpoint=False):
        axT.plot(*cliff(wv,0*wv+c_),**KK); axT.plot(*cliff(0*wv+c_,wv),**KK)
    axT.plot(*cliff(wv,0*wv+np.pi),color="k",lw=1.6); axT.plot(*cliff(0*wv,wv),color="k",lw=1.6,ls="--")
    axT.set_xlim(-2.1,2.1); axT.set_ylim(-2.1,2.1); axT.set_zlim(-1.1,1.1); axT.set_box_aspect((1,1,2.2/4.2)); axT.set_axis_off(); axT.view_init(elev=28,azim=-58)
    head(X3[0],0.955,"(a)  the torus","$T^2=\\mathbb{C}/M_{\\rm PCF}\\mathbb{Z}[i]$, $\\tau=i$: two cycles of equal length, $M$ (solid) and $Mi$ (dashed) (§11.1)")
    ax=fig.add_axes([0.36,0.785,0.28,0.145],projection="3d")
    for a_ in np.linspace(0,2*np.pi,24,endpoint=False): ax.plot([R*np.cos(a_)]*2,[R*np.sin(a_)]*2,[-1.2,1.2],color="k",lw=.35)
    for g_ in np.linspace(-0.75,0.75,7):
        ax.plot([g_,g_],[-0.75,0.75],[-phi*.75,phi*.75],color="k",lw=.3,alpha=.7); ax.plot([-0.75,0.75],[g_,g_],[phi*g_]*2,color="k",lw=.3,alpha=.7)
    ax.plot(R*np.cos(t),R*np.sin(t),-1.2+0*t,"k",lw=1.0); ax.plot(R*np.cos(t),R*np.sin(t),phi*R*np.sin(t),"k",lw=1.6)
    for nm,col,k in TRI:
        v=V3[k]; ax.scatter([v.real],[v.imag],[-1.2],c=col,s=14,depthshade=False); ax.scatter([v.real],[v.imag],[phi*v.imag],c=col,s=40,depthshade=False)
        ax.plot([v.real]*2,[v.imag]*2,[-1.2,phi*v.imag],color=col,lw=.7,ls=":"); ax.text(v.real*1.5,v.imag*1.5,phi*v.imag,nm,color=col,fontsize=11,weight="bold")
    ax.view_init(elev=18,azim=-125); ax.set_box_aspect((1,1,1.4)); ax.set_axis_off()
    head(X3[1],0.955,"(b)  the third direction","the ring $|z|=\\frac{1}{2}$ (I12) and the plane $z=\\varphi y$:\nthe triad lifts without a kernel (I15, §11.1)")
    ax=fig.add_axes([0.70,0.80,0.26,0.15]); ax.set_aspect("equal"); ax.axis("off")
    sq=R/2**.5
    for i in range(-3,4): ax.plot([i*sq]*2,[-3*sq,3*sq],color="#9fd6d6",lw=.5); ax.plot([-3*sq,3*sq],[i*sq]*2,color="#9fd6d6",lw=.5)
    ax.plot(R*np.cos(t),R*np.sin(t),"--",color="0.5",lw=.9)
    ax.fill([v.real for v in V3],[v.imag for v in V3],color="#c9a0d6",alpha=.5); ax.plot([v.real for v in V3+[V3[0]]],[v.imag for v in V3+[V3[0]]],"k",lw=1.2)
    ax.add_patch(plt.Rectangle((0,0),sq,sq,fill=False,ec="#1a8f8f",lw=2))
    for nm,col,k in TRI:
        v=V3[k]; ax.plot(v.real,v.imag,"o",color=col,ms=9)
        ax.text(v.real+(.06 if k==0 else 0),v.imag+(.08 if k==1 else -.1 if k==2 else 0),f"{nm} ({120*k}°)",color=col,fontsize=9.5,weight="bold",ha="left" if k==0 else "center",va="center")
    ax.set_xlim(-3.1*sq,3.1*sq); ax.set_ylim(-3.1*sq,3.1*sq)
    head(X3[2],0.955,"(c)  from $120^\\circ$ to $90^\\circ$","the triangle of $\\mathbb{Z}[\\omega]$ and the square cell of $\\mathbb{Z}[i]$, $\\tau=i$ (I15, §11.1)")
    sep(0.78)

    # ======== row 2: from the diagonal to the face
    band(0.7720,"From the diagonal to the face")
    E=[(a,b) for a,b in itertools.combinations(list(itertools.product([0,1],repeat=3)),2) if sum(x!=y for x,y in zip(a,b))==1]
    def prj(d,up):
        d=np.array(d,float); d/=np.linalg.norm(d); up=np.array(up,float); a1=np.cross(up,d); a1/=np.linalg.norm(a1); a2=np.cross(d,a1)
        return lambda p: np.array([np.array(p,float)@a1,np.array(p,float)@a2])
    def slerp(a,b,u):
        a=np.array(a,float)/np.linalg.norm(a); b=np.array(b,float)/np.linalg.norm(b); o=math.acos(np.clip(a@b,-1,1)); return (math.sin((1-u)*o)*a+math.sin(u*o)*b)/math.sin(o)
    AX=[RED,GRN,BLU]
    def cubeview(ax,d,up,face=False):
        f=prj(d,up); c=f((.5,.5,.5))
        for a,b in E: A,Bq=f(a)-c,f(b)-c; ax.plot([A[0],Bq[0]],[A[1],Bq[1]],color="0.55",lw=1)
        for e,col in zip(np.eye(3),AX): ax.annotate("",xy=f(e)-c,xytext=f((0,0,0))-c,arrowprops=dict(arrowstyle="-|>",color=col,lw=1.8))
        if face:
            q=[f(p)-c for p in [(0,0,1),(1,0,1),(1,1,1),(0,1,1)]]; ax.fill([p[0] for p in q],[p[1] for p in q],color="#1a8f8f",alpha=.18)
        ax.set_xlim(-1.1,1.1); ax.set_ylim(-1.1,1.1)
    d0=(1,1,1); d1=(1e-3,1e-3,1); up=(0,1,0); f=prj(d0,(0,0,1)); Pr=[f(e)-f((0,0,0)) for e in np.eye(3)]
    assert np.allclose([math.degrees(math.acos(Pr[i]@Pr[j]/np.linalg.norm(Pr[i])/np.linalg.norm(Pr[j]))) for i,j in [(0,1),(1,2),(0,2)]],120)
    assert np.allclose([np.linalg.norm(p)**2 for p in Pr],2/3)
    TT=["along $(1,1,1)$: axes at $120^\\circ$, $|\\cdot|^2=\\frac{2}{3}$","turning, $\\frac{1}{3}$","turning, $\\frac{2}{3}$","an axis faces us: the square face [R]","the cells from one corner, sides $M\\varphi^{\\sigma}$"]
    W5=0.16; xs5=[0.035+i*0.19 for i in range(5)]
    sides=[M*phi**s for s in range(6)]
    for i in range(5):
        ax=fig.add_axes([xs5[i],0.635,W5,0.11]); ax.set_aspect("equal"); ax.axis("off")
        if i==0:
            for p in itertools.product(range(-2,3),repeat=3):
                q=f(p); ax.plot(*q,"o",color="0.3" if sum(p)%3 else RED,ms=2.4)
            for e,col in zip(np.eye(3),AX): ax.annotate("",xy=f(e)*1.8,xytext=(0,0),arrowprops=dict(arrowstyle="-|>",color=col,lw=1.8))
            ax.set_xlim(-2.4,2.4); ax.set_ylim(-2.4,2.4)
        elif i<4: cubeview(ax,slerp(d0,d1,i/3) if i<3 else d1,up,face=(i==3))
        else:
            for s in range(6):
                d=phi**s; ax.add_patch(plt.Rectangle((0,0),d,d,fill=False,ec="#1a8f8f",lw=1.1,alpha=0.35+0.11*s)); ax.text(d+.1,d,f"{sides[s]:.0f}",fontsize=7,color="0.35")
                assert abs((L/(6*3**.5))*phi**s*M*phi**-s-math.pi)<1e-12
            ax.set_xlim(-.4,12.5); ax.set_ylim(-.4,12.5)
        fig.text(xs5[i]+W5/2,0.6270,TT[i],ha="center",va="top",fontsize=8.8,color="0.35")
        if i<4: fig.text(xs5[i]+W5+0.015,0.6900,"→",fontsize=18,ha="center",va="center",color="0.45")
    fig.text(0.5,0.6090,"(d)  the turn from the diagonal to the face is a reading [R]; the passage the paper proves is (c). The cell of level $\\sigma$ has side $M\\varphi^{\\sigma}$ and carries the phase $\\varepsilon_0M\\varphi^{2\\sigma}$ (phase_on_cell, §11.1)",ha="center",va="top",fontsize=9,color="0.4")
    sep(0.5900)

    # ======== row 3: the cube that turns
    band(0.5820,"Each dimension from the next one up: one cut and projection per step")
    ax=fig.add_axes([0.05,0.3950,0.26,0.135])
    pts=[(a,b) for a in range(-12,13) for b in range(-9,10)]
    X1=np.array([a+b*phi for a,b in pts]); X2=np.array([a+b*pb for a,b in pts])
    k=(abs(X1)<12)&(abs(X2)<4); ax.plot(X1[k],X2[k],".",color="0.65",ms=3)
    xs=np.linspace(-12,12,2000)
    for s_ in (1,-1):
        with np.errstate(divide="ignore"): yv=s_/xs
        yv[abs(yv)>4]=np.nan; ax.plot(xs,yv,color=RED,lw=.9,ls="-" if s_==1 else "--")
    for n in range(-4,6):
        x,y=phi**n,(pb)**n; assert abs(x*y-(-1)**n)<1e-9
        if abs(x)<12 and abs(y)<4: ax.plot(x,y,"o",mfc="none",mec=RED,ms=6); ax.text(x+.2,y+.15,f"$\\varphi^{{{n}}}$",fontsize=7,color=RED)
    ax.axhspan(-1,phi-1,color=BLU,alpha=.12); win=k&(X2>=-1)&(X2<phi-1); ax.plot(X1[win],X2[win],"o",color=BLU,ms=3)
    ch=np.sort(X1[win]); ax.plot(ch,0*ch-3.6,"|",color=BLU,ms=9); ax.axhline(-3.6,color=BLU,lw=.6)
    gaps=set(np.round(np.diff(ch),6)); assert gaps<= {round(1.0,6),round(phi,6)} and len(gaps)==2
    ax.set_xlim(-12,12); ax.set_ylim(-4,4); ax.set_xlabel("$x=a+b\\varphi$",fontsize=8,color="0.35"); ax.set_ylabel("$\\bar x=a+b\\bar\\varphi$",fontsize=8,color="0.35")
    ax.tick_params(labelsize=7,colors="0.5")
    for s_ in ax.spines.values(): s_.set_color("0.75")
    head(X3[0],0.5580,"(e)  1D from 2D","$a+b\\varphi\\mapsto(x,\\bar x)$, units on $x\\bar x=\\pm1$;\nthe window $[-1,\\varphi-1)$ gives the Fibonacci chain, gaps $1$ and $\\varphi$ (§11.1)")
    ax=fig.add_axes([0.35,0.3800,0.30,0.17],projection="3d"); n3=np.ones(3)/3**.5
    LAY=[VIO,TEAL,GOLD]
    P3=np.array(list(itertools.product(range(3),repeat=3)),float); c0=np.array([-1.3]*3)
    e1=np.array([1,-1,0])/2**.5; e2=np.cross(n3,e1); uu,vv=np.meshgrid([-2.4,2.4],[-2.4,2.4])
    ax.plot_surface(*(c0[:,None,None]+uu*e1[:,None,None]+vv*e2[:,None,None]),color=TEAL,alpha=.12,lw=0)
    proj=P3-((P3-c0)@n3)[:,None]*n3; sh={}
    for p,q in zip(P3,proj):
        col=LAY[int(p.sum())%3]; ax.scatter(*p,c=col,s=14,depthshade=False); ax.plot(*np.c_[p,q],color=col,lw=.3,alpha=.4); sh.setdefault(tuple(np.round(q,9)),[]).append(p)
    for q,ps in sh.items(): ax.scatter(*q,c=LAY[int(ps[0].sum())%3],s=8+12*len(ps),edgecolor="k" if len(ps)>1 else "none",depthshade=False)
    assert len(sh)==19 and all(len({int(p.sum())%3 for p in ps})==1 for ps in sh.values())
    for Lc in (3,5,7):
        pp=np.array(list(itertools.product(range(Lc),repeat=3)),float); assert len({tuple(np.round([p@e1,p@e2],9)) for p in pp})==3*Lc*Lc-3*Lc+1
    ax.plot([-1.3,2.8],[-1.3,2.8],[-1.3,2.8],"k",lw=1.3); ax.text(2.9,2.9,2.9,"$(1,1,1)$",fontsize=8)
    ax.view_init(14,-20); ax.set_axis_off(); ax.set_box_aspect((1,1,1))
    head(X3[1],0.5580,"(f)  2D from 3D","$\\mathbb{Z}^3$ along its diagonal gives $\\mathbb{Z}[\\omega]$; layers $i+j+k$ mod 3;\noutlined: the kernel $\\mathbb{Z}(1,1,1)$")
    fig.text(X3[1],0.3770,"$\\{0,\\dots,L-1\\}^3$ casts $3L^2-3L+1$ shadows: $19, 61, 127$ for $L=3,5,7$ (cube_diagonal_kernel, §11.1)",ha="center",va="top",fontsize=9,color="0.4")
    ax=fig.add_axes([0.69,0.3800,0.28,0.17],projection="3d")
    V=[]
    for s1 in (1,-1):
        for s2 in (1,-1): p=(0,s1,s2*phi); V+=[p,(p[1],p[2],p[0]),(p[2],p[0],p[1])]
    V=np.array(V,float); assert np.allclose((V**2).sum(1),phi+2) and phi+2<4
    Ed=[(i,j) for i,j in itertools.combinations(range(12),2) if abs(((V[i]-V[j])**2).sum()-4)<1e-9]; assert len(Ed)==30
    for i,j in Ed: ax.plot(*np.c_[V[i],V[j]],color="#7a5c2e",lw=.8)
    ax.scatter(*V.T,c="#6a3d9a",s=28,depthshade=False)
    for ii in range(3):
        Rr=np.array([[0,1,phi],[0,-1,phi],[0,-1,-phi],[0,1,-phi]],float)[:,[(0-ii)%3,(1-ii)%3,(2-ii)%3]]
        s1_,s2_=np.linalg.norm(Rr[0]-Rr[1]),np.linalg.norm(Rr[1]-Rr[2]); assert abs(max(s1_,s2_)/min(s1_,s2_)-phi)<1e-12
        ax.add_collection3d(Poly3DCollection([Rr],facecolor=LAY[ii],alpha=.2,edgecolor=LAY[ii]))
    ax.view_init(18,30); ax.set_axis_off(); ax.set_box_aspect((1,1,1))
    head(X3[2],0.5580,"(g)  3D","the icosahedron $(0,\\pm1,\\pm\\varphi)$ and its cyclic permutations;\n$|v|^2=\\varphi+2<4$: kissing $12$ (§11.1)")
    sep(0.3550)

    # ======== row 4: the tiles and the throat from the side
    band(0.347,"The rings of the throat: each level one ring, tiled at its boundary")
    words=["AAB"]
    for _ in range(12): words.append("".join({"A":"AB","B":"A"}[c] for c in words[-1]))
    def bd(wd):
        wid=[1 if c=="A" else 1/phi for c in wd]; c=np.cumsum([0]+wid); return c/c[-1]
    F=[0,1]
    for _ in range(20): F.append(F[-1]+F[-2])
    for s_ in range(13):
        A_,B_=words[s_].count("A"),words[s_].count("B")
        assert len(words[s_])==F[s_+4] and A_==F[s_+3] and B_==F[s_+2]
        assert abs(math.pi*(A_/phi**2+B_/phi**3)-math.pi*phi**s_)<1e-9
        if s_<12: assert all(np.min(abs(bd(words[s_+1])-x))<1e-12 for x in bd(words[s_]))
    NL=7; LEV=list(range(NL))
    # (h) the tiles, sigma=6 at the top ... sigma=0 at the bottom
    axH=fig.add_axes([0.04,0.085,0.27,0.205]); axH.axis("off")
    yrow=lambda s_: s_*1.0
    for s_ in LEV:
        b_=bd(words[s_])
        for i,c in enumerate(words[s_]): axH.add_patch(plt.Rectangle((b_[i],yrow(s_)),b_[i+1]-b_[i],.55,fc="0.78" if c=="A" else "white",ec="k",lw=.45))
        if s_<NL-1:
            b1=bd(words[s_+1])
            for i in range(len(words[s_])):
                for j in range(len(words[s_+1])):
                    if b_[i]-1e-12<=b1[j] and b1[j+1]<=b_[i+1]+1e-12: axH.plot([(b_[i]+b_[i+1])/2,(b1[j]+b1[j+1])/2],[yrow(s_)+.55,yrow(s_+1)],color="0.6",lw=.35)
        A_,B_=words[s_].count("A"),words[s_].count("B")
        axH.text(-0.03,yrow(s_)+.27,f"$\\sigma={s_}$",ha="right",va="center",fontsize=9,color="0.25")
        axH.text(1.03,yrow(s_)+.27,f"{A_+B_} = {A_}+{B_}",ha="left",va="center",fontsize=8.5,color="0.3")
    axH.set_xlim(-0.16,1.3); axH.set_ylim(-0.2,NL-0.3)
    head(0.17,0.322,"(h)  the ring of each level, unrolled","$AAB$, then $A\\to AB$, $B\\to A$; tiles $=$ long $+$ short; lines join a tile to its daughters;\ndotted: each strip to its ring in (i)")
    # (i) the throat, levels 0..6, with the long tiles shaded on the front face
    axG=fig.add_axes([0.40,0.085,0.57,0.21]); axG.set_axis_off()
    def hgt(r): return np.arccosh(1/r)-np.sqrt(1-r*r)
    top=NL-1; rad=lambda s_: phi**(s_-top)
    Lh=hgt(rad(0)); xpos=lambda s_: Lh-hgt(rad(s_))
    r=np.geomspace(rad(0)*0.8,1,600); Xg=Lh-hgt(r)
    ee=0.16
    for s_ in LEV[:-1]:
        b_=bd(words[s_]); ss=np.linspace(s_,s_+1,25); rr=rad(ss); xx=np.array([xpos(q) for q in ss])
        for i,c in enumerate(words[s_]):
            th=np.linspace(2*np.pi*b_[i],2*np.pi*b_[i+1],30)
            if c=="A":
                fr=np.sin(th)>0
                if fr.sum()>1:
                    tf=th[fr]
                    X0=xpos(s_)+ee*rad(s_)*np.sin(tf); Y0=rad(s_)*np.cos(tf); X1=xpos(s_+1)+ee*rad(s_+1)*np.sin(tf[::-1]); Y1=rad(s_+1)*np.cos(tf[::-1])
                    axG.fill(np.r_[X0,X1],np.r_[Y0,Y1],color="0.82",lw=0,zorder=1)
            a0=2*np.pi*b_[i]
            if math.sin(a0)>0: axG.plot(xx+ee*rr*math.sin(a0),rr*math.cos(a0),color="k",lw=.4,zorder=2)
    axG.plot(Xg,r,"k",lw=1.0); axG.plot(Xg,-r,"k",lw=1.0)
    tb=np.linspace(0,np.pi,100)
    for s_ in LEV:
        rr=rad(s_); xs_=xpos(s_); assert s_==0 or abs(rr/rad(s_-1)-phi)<1e-12
        axG.plot(xs_+ee*rr*np.sin(tb),rr*np.cos(tb),c="k",lw=1.3,zorder=3); axG.plot(xs_-ee*rr*np.sin(tb),rr*np.cos(tb),c="k",lw=.6,ls="--",zorder=3)
        axG.text(xs_,-1.16,f"{s_}",ha="center",fontsize=10,color="0.25")
    axG.text(Lh/2,-1.36,"level $\\sigma$",ha="center",fontsize=10,color="0.4")
    axG.set_xlim(-0.05,Lh+0.3); axG.set_ylim(-1.42,1.12)
    head(0.685,0.322,"(i)  the throat, assembled","$e^{A}=\\varphi^{\\sigma}$, rings in the ratio $\\varphi$; each ring carries the tiles of (h), $S=\\pi(A/\\varphi^{2}+B/\\varphi^{3})=\\pi\\varphi^{\\sigma}$ exactly")
    fig.canvas.draw()
    FH=lambda xy: fig.transFigure.inverted().transform(axH.transData.transform(xy))
    FG=lambda xy: fig.transFigure.inverted().transform(axG.transData.transform(xy))
    for s_ in LEV:
        p=FH((1.27,yrow(s_)+.27)); q=FG((xpos(s_),rad(s_)))
        fig.add_artist(Line2D([p[0],q[0]],[p[1],q[1]],color="0.7",lw=.6,ls=":"))
    fig.text(0.5,0.072,"Drawn $\\sigma=0,\\dots,6$: $3,5,8,13,21,34,55$ tiles. The same substitution continues to the bottom $\\sigma_{\\rm IR}=12$, where the ring has $987=610+377$ tiles (§11.1).",ha="center",fontsize=9.5,color="0.35")
    fig.text(0.5,0.05,"Colours are conventions of the drawing: P, C, F and the axes $e_1,e_2,e_3$ in red, green, blue; the layers of (f) and the rectangles of (g) in violet, teal, gold.",ha="center",fontsize=9,color="0.4")
    fig.savefig("fig_background.pdf",bbox_inches="tight"); plt.close(fig)
    plt.rcParams.update(matplotlib.rcParamsDefault)
    print("background figure: ok")

SECCIONES.append((44, 'The Background figure: one structure seen at once (Figure 1)', seccion_44))

# ======================================================================
# 45. The observer level along LCDM, the story of (F10), the half, and the throat constant
# ======================================================================
def seccion_45():
    """(F10) and the texts of ssec:phys: every number is checked; what
    holds by construction is marked as such.
    Run:  python -m kkgt.sections 45"""
    import numpy as np
    from math import gamma, pi
    phi=(1+5**.5)/2; L=np.log(phi); lam=np.log(2)/L; G=0.5
    z=lambda s: phi**s; S=lambda s: np.pi*phi**s; Lam=lambda s: 6*phi**(-s); Hl=lambda s: np.sqrt(Lam(s)/3)
    # the horizon level in LCDM, with the Planck values
    tP=5.391247e-44; l=np.sqrt(2)*tP; Mpc=3.0856775814913673e22
    H0=67.36e3/Mpc; Om=0.3153; Or=9.0e-5; OL=1-Om-Or
    Hc=lambda a: H0*np.sqrt(Or/a**4+Om/a**3+OL); sig=lambda h: np.log(6/(3*(h*l)**2))/L
    a=np.logspace(-34,4,4000); s=sig(Hc(a))
    s_inf=sig(H0*np.sqrt(OL)); s_hoy=sig(H0)
    assert np.all(np.diff(s)>-1e-9) and abs(s[-1]-s_inf)<1e-2
    assert abs(s_inf-583.877)<5e-3 and abs(s_hoy-583.090)<5e-3
    print(f"Planck: asymptotic level {s_inf:.2f}; horizon of today {s_hoy:.2f}, below it, rising towards it")
    assert np.allclose(3*(Hc(a)*l)**2*np.pi*phi**s,6*np.pi)
    print("3H^2 = 6pi/S_H at every moment; what falls is 3H^2, Lambda is constant (w = -1)")
    print(f"N bound: 3pi/(Lambda G_N) with G_N=1/2 = 6pi/Lambda = S_obs = pi phi^{s_inf:.3f}")
    # the compression limit
    zz=np.linspace(0.01,3,30000); cruce=zz[np.argmin(abs(2*np.pi*zz**2-np.pi*zz))]
    assert abs(cruce-0.5)<1e-3 and np.isclose(z(-lam),0.5) and np.isclose(S(-lam),np.pi/2)
    assert np.all(2*np.pi*zz[zz<0.5]**2<np.pi*zz[zz<0.5])
    print(f"compression limit: 4pi z^2/(4G_N) = pi z only at z = 1/2, sigma = {-lam:.4f}, S = pi/2 (half a cell)")
    assert np.isclose(z(0)/z(-lam),2) and np.isclose(S(0),2*S(-lam))
    print("first expansion: the radius doubles, half a cell becomes a cell, S(0) = pi; a doubling is not a bit:",
          f"Delta S = {(S(0)-S(-lam))/np.log(2):.3f} bits")
    # the constant of the first patch and that of the throat
    assert np.isclose(3*np.pi/(G*S(0)),6) and np.isclose(4*3/2,6)
    Om_=lambda k: 2*pi**((k+1)/2)/gamma((k+1)/2)
    iguales=[d for d in range(3,30) if np.isclose((d-1)*(d-2)/2*(Om_(d-2)/(4*G*np.pi))**(2/(d-2)),d*(d-1)/2)]
    assert iguales==[4]
    print("Lambda(0) = 3/G_N = 6 (W4) and |Lambda_5| = d(d-1)/2 = 6 (W8): with patch and throat at the same d, only d = 4")
    sg=np.linspace(-5,600,200001); assert abs(sg[np.argmin(abs(Lam(sg)-6))])<1e-2
    print("[by construction] the level where they are equal is sigma = 0; H(0) l = %.4f, throat radius 1: equal constants, not radii"%Hl(0))
    w=lambda n: np.exp(-np.pi*phi**(-2.0*n)); assert w(1)<0.5<w(2) and Hl(1)>1>Hl(2)
    r=583.79*np.log10(phi); assert abs(r-122.0)<0.01 and np.isclose(Lam(583.79)*S(583.79),6*S(0))
    print(f"[by construction, Lambda S = 6pi] Lambda_obs = |Lambda_5| S(0)/S_obs: 3H^2(0)/Lambda_obs = phi^583.79 = 10^{r:.2f} pi cells")
    # the half
    rng=np.random.default_rng(45); N=200000; T=rng.uniform(-np.pi/2,np.pi/2,N)*0.999; chi=rng.uniform(0,np.pi,N)
    tau=np.arcsinh(np.tan(T)); X0=np.sinh(tau); X4=np.cosh(tau)*np.cos(chi)
    fut=chi<T+np.pi/2; past=chi<np.pi/2-T
    assert np.array_equal(X0+X4>0,fut) and np.array_equal(X4-X0>0,past) and np.array_equal(fut&past,chi<np.pi/2-abs(T))
    print("the flat chart X0+X4>0 is the causal future of the worldline; what it receives, X4-X0>0; they cross at the static patch, a quarter")
    for l_,t_,r_ in [(1,0.3,2),(2.5,-1,0.7),(0.4,3,5)]:
        assert np.isclose((l_*np.sinh(t_/l_)+r_**2/(2*l_)*np.exp(t_/l_))+(l_*np.cosh(t_/l_)-r_**2/(2*l_)*np.exp(t_/l_)),l_*np.exp(t_/l_))
    print("X0+X4 = l e^{t/l} > 0 (planar_patch_positive): ok")

SECCIONES.append((45, 'The observer level in LCDM, the story of (F10), the throat constant and the half', seccion_45))

# ======================================================================
# 46. The Hopf foliation and J
# ======================================================================
def seccion_46():
    """P7 (ssec:math) and P7b (conclusions): the tori of the window, the
    mirror, J, the axis.
    Run:  python -m kkgt.sections 46"""
    import numpy as np
    phi=(1+5**.5)/2; rng=np.random.default_rng(46)
    tor=lambda e,a,b: np.array([np.cos(e)*np.exp(1j*a),np.sin(e)*np.exp(1j*b)])
    ns=np.arange(-12,13); eta=np.arctan(phi**(-2.0*ns))
    assert np.allclose(np.tan(eta),phi**(-2.0*ns))
    e=0.4;a,b=1.1,2.3;h=1e-6; g=lambda u,v:np.real(np.vdot(u,v))
    da=(tor(e,a+h,b)-tor(e,a-h,b))/2/h; db=(tor(e,a,b+h)-tor(e,a,b-h))/2/h
    assert np.allclose([g(da,da),g(db,db),g(da,db)],[np.cos(e)**2,np.sin(e)**2,0],atol=1e-8)
    assert np.allclose(np.pi/2-eta,eta[::-1]) and np.isclose(eta[ns==0][0],np.pi/4)
    for n,et in zip(ns,eta):
        bb=np.linspace(0,2*np.pi,50); s=np.sin(et); rho=np.cos(et)/(1-s*np.sin(bb)); zz=s*np.cos(bb)/(1-s*np.sin(bb))
        assert np.allclose((rho-1/np.cos(et))**2+zz**2,np.tan(et)**2,rtol=1e-9) and np.isclose(1/np.sin(et),np.sqrt(1+phi**(4.0*n)))
    print("flat tori of modulus i tan eta, tan eta_n = phi^-2n; the exchange is the mirror; Clifford at 0; R/r = sqrt(1+phi^4n) from z1=0")
    z=rng.normal(size=2)+1j*rng.normal(size=2); z/=np.linalg.norm(z); hopf=lambda z: z[...,0]/z[...,1]
    J=lambda z: np.array([-np.conj(z[1]),np.conj(z[0])])
    assert np.allclose(-z,np.exp(1j*np.pi)*z) and np.isclose(hopf(-z),hopf(z))
    assert np.isclose(hopf(J(z)),-1/np.conj(hopf(z))) and np.allclose(J(J(z)),-z) and np.allclose(J(J(J(J(z)))),z)
    assert np.isclose(abs(J(tor(e,a,b))[0]),np.sin(e))
    print("J^2 = -1, J^4 = 1; on the base, the antipode of W10; on the tori, the mirror; the half turn is not seen on the base")
    # homogeneity, tori and axis
    for _ in range(100):
        p=rng.normal(size=2)+1j*rng.normal(size=2); p/=np.linalg.norm(p); q=rng.normal(size=2)+1j*rng.normal(size=2); q/=np.linalg.norm(q)
        A=np.array([[p[0],-p[1].conj()],[p[1],p[0].conj()]]); B=np.array([[q[0],-q[1].conj()],[q[1],q[0].conj()]]); U=B@np.linalg.inv(A)
        assert np.allclose(U@p,q) and np.allclose(U.conj().T@U,np.eye(2))
    e0=0.5; aa=rng.uniform(0,2*np.pi,500); bb=rng.uniform(0,2*np.pi,500)
    Tz=np.stack([np.cos(e0)*np.exp(1j*aa),np.sin(e0)*np.exp(1j*bb)],-1)
    assert np.allclose(abs(hopf(Tz)),1/np.tan(e0))
    R=np.array([[np.cos(.7),-np.sin(.7)*np.exp(-.3j)],[np.sin(.7)*np.exp(.3j),np.cos(.7)]]); Tr=Tz@R.T
    assert np.std(abs(Tr[:,0]))>1e-2 and np.allclose(abs(hopf(Tr@np.linalg.inv(R).T)),1/np.tan(e0))
    D=np.diag([np.exp(.4j),np.exp(-1.1j)]); assert np.allclose(abs((Tz@D.T)[:,0]),np.cos(e0))
    print("SU(2) takes any fibre to any other; a torus is the preimage of a parallel and asks for an axis; every axis goes to every other; U(1)xU(1) preserves each torus")
    w=lambda n: np.exp(-np.pi*phi**(-2.0*n)); n12=0.5*np.log(np.pi/np.log(2))/np.log(phi)
    assert np.allclose(w(ns),np.exp(-np.pi*np.tan(eta))) and abs(n12-1.5702)<1e-4
    print(f"the window weight is e^(-pi tan eta_n); it crosses 1/2 at n = {n12:.4f}")

SECCIONES.append((46, 'The Hopf foliation and J', seccion_46))

# ======================================================================
# 47. La tríada como código, la cuerda como corte, y el código pentagonal
# ======================================================================
def seccion_47():
    """imp:adscft (el código), «The dictionary without a choice» (la cuerda, el código pentagonal)."""
    import numpy as np, itertools
    from collections import deque
    phi=(1+5**.5)/2; w=np.exp(2j*np.pi/3)
    # la tríada
    v=0.5*w**np.arange(3); V=(v/np.linalg.norm(v)).reshape(3,1); P=V@V.conj().T
    assert np.allclose(V.conj().T@V,1) and np.linalg.matrix_rank(P)==1 and np.allclose(P@P,P)
    F3=np.array([[w**(j*k) for k in range(3)] for j in range(3)])/np.sqrt(3)
    assert np.allclose(V[:,0],F3[:,1]) and np.allclose(F3.conj().T@F3,np.eye(3)) and abs(v.sum())<1e-12
    print("la tríada V: una codificación con subespacio de código de dimensión 1; columna k=1 de la transformada de Fourier de Z/3")
    # la cuerda como corte
    for s in [0,3,6,12]: assert np.isclose(2*np.pi*phi**s/2,np.pi*phi**s)
    print("la cuerda como corte: longitud del anillo 2 pi phi^sigma por 1/2 = S en cada nivel")
    # el tensor perfecto de seis patas del código de cinco qubits
    I=np.eye(2); X=np.array([[0,1],[1,0]]); Z=np.diag([1,-1])
    def kron(*a):
        r=np.array([[1.0]])
        for m in a: r=np.kron(r,m)
        return r
    Pc=np.eye(32)
    for g in [kron(X,Z,Z,X,I),kron(I,X,Z,Z,X),kron(X,I,X,Z,Z),kron(Z,X,I,X,Z)]: Pc=Pc@(np.eye(32)+g)/2
    assert np.linalg.matrix_rank(Pc)==2
    ev,vec=np.linalg.eigh(Pc@kron(Z,Z,Z,Z,Z)@Pc); T6=np.stack([vec[:,np.argmax(ev)],vec[:,np.argmin(ev)]]).reshape([2]*6)
    for A in itertools.combinations(range(6),3):
        B=[i for i in range(6) if i not in A]; M=np.transpose(T6,list(A)+B).reshape(8,8)
        assert np.allclose(M@M.conj().T,np.eye(8)*np.trace(M@M.conj().T)/8)
    print("el tensor de seis patas del código [[5,1,3]] es perfecto: las 20 biparticiones 3|3 son isometrías")
    # el lado del pentágono de {5,4}
    a=2*np.arccosh(np.cos(np.pi/5)/np.sin(np.pi/4))
    assert np.isclose(np.cosh(a),phi) and np.isclose(np.sinh(a),phi**0.5) and np.isclose(a,np.arcsinh(phi**0.5))
    print(f"lado del pentágono: cosh a = phi, sinh a = phi^(1/2), a = {a:.6f} = arsinh(phi^(1/2)), el radio del disco del nivel 1/2")
    # los conteos, con capas por arista
    J=np.diag([-1.,1.,1.]); mink=lambda u,x:u@J@x
    R0=np.arccosh(1/(np.tan(np.pi/5)*np.tan(np.pi/4)))
    t0=[np.array([np.cosh(R0),np.sinh(R0)*np.cos(2*np.pi*k/5),np.sinh(R0)*np.sin(2*np.pi*k/5)]) for k in range(5)]
    assert np.isclose(np.arccosh(-mink(t0[0],t0[1])),a)
    def refl(p,q):
        n=J@np.cross(p,q); n=n/np.sqrt(mink(n,n)); return np.eye(3)-2*np.outer(n,J@n)
    key=lambda p:(round(p[1]/(1+p[0]),6)+0.0,round(p[2]/(1+p[0]),6)+0.0)
    tk=lambda vs: tuple(sorted(key(x) for x in vs))
    def counts(tiles):
        e={}
        for vs in tiles.values():
            for k in range(5):
                ed=tuple(sorted((key(vs[k]),key(vs[(k+1)%5])))); e[ed]=e.get(ed,0)+1
        return len(tiles),sum(1 for c in e.values() if c==1)
    tiles={tk(t0):t0}; last=[t0]; res=[counts(tiles)]
    for _ in range(6):
        nuevo=[]
        for vs in last:
            for k in range(5):
                nv=[refl(vs[k],vs[(k+1)%5])@x for x in vs]
                if tk(nv) not in tiles: tiles[tk(nv)]=nv; nuevo.append(nv)
        last=nuevo; res.append(counts(tiles))
    Fb=[0,1]; Lc=[2,1]
    for _ in range(20): Fb.append(Fb[-1]+Fb[-2]); Lc.append(Lc[-1]+Lc[-2])
    assert [r[0] for r in res]==[5*Fb[2*n+1]-4 for n in range(7)] and [r[1] for r in res]==[5*Lc[2*n+1] for n in range(7)]
    print("capas por arista: pentágonos", [r[0] for r in res], "= 5F(2n+1)-4; patas de frontera", [r[1] for r in res], "= 5L(2n+1)")
    print(f"tasa en la capa 6: {res[6][0]/res[6][1]:.4f}; límite F/L = 1/sqrt5 = {5**-.5:.4f}; cada capa multiplica por phi^2 = {phi**2:.4f}")
    assert abs(res[6][0]/res[6][1]-5**-.5)<2e-3
    # el corte
    cro=10*a/np.pi**2; assert np.isclose(cro,2/np.pi*(5*a/2)/(np.pi/2))
    print(f"Crofton: {cro:.4f} cruces por unidad de longitud; con chi=2, {cro*np.log(2):.3f} frente a 1/2: {cro*np.log(2)/0.5:.2f} S en promedio; chi que daría S: {np.exp(0.5/cro):.3f}")

SECCIONES.append((47, 'La tríada como código, la cuerda como corte, y el código pentagonal', seccion_47))

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
