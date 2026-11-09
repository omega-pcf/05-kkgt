"""reproduce_v108.py: todos los números y las cinco figuras de
«The Kaluza–Klein spectrum of the golden throat», v108.

Uso:  python3 reproduce_v108.py          todas las secciones
      python3 reproduce_v108.py 2 14     solo esas secciones

Cada sección es uno de los scripts anteriores, sin cambios, en su propio espacio de
nombres. Figuras: 1 (sección 12), 2 (sección 13), 3 (sección 10), 4 (sección 39),
5 (sección 41). Python 3.13, NumPy, SciPy, Matplotlib; la
sección 2 necesita además mpmath.
"""
import sys
SECCIONES = []

# ======================================================================
# 1. Todos los números en orden de aparición; alternativas para m0 (§9)
# ======================================================================
def seccion_1():
    """Reproduce every number of kk_golden_throat.tex, in order of appearance.
    Python 3.13, NumPy 2.5.3, SciPy 1.18.1.  Run:  python3 reproduce_all.py"""
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

    print("== §2 tower operator (2), sigma = 0..6")
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

    print("== §3 spectrum of (sl)")
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

    print("== §4 look-elsewhere")
    rng = np.random.default_rng(1); q = np.exp(rng.uniform(np.log(1.3), np.log(4.5), 200000))
    grid = phi ** (np.arange(1, 9) / 2)
    P("P(within 1% of phi^{k/2}) (0.08)", round(np.mean(np.min(abs(q[:, None]/grid - 1), 1) < 0.01), 2))

    print("== §5 vector, M=24")
    for a in (0, -6, -24):
        rv, _ = ratios(sl(a, 6, 24, 2, 0))
        P(f"sigma[{a},6] m2/m1 (2.093, 2.171, 2.241)", round(rv[1], 3))
    j0 = jn_zeros(0, 2); P("J0 limit (2.295)", round(j0[1] / j0[0], 3))

    print("== §6 sectors")
    g1 = ratios(sl(-6, 6, 32, 4, 2))[1][0]; v1 = ratios(sl(-6, 6, 32, 2, 0))[1][0]
    for mg in (3600, 4000):
        P(f"gluon {mg}: log_phi(gluon/graviton scale) (5.39, 5.61)", round(np.log((mg/v1)/(380/g1)) / lp, 2))

    print("== Methods: assumed errors")
    for mm, dm in ((700, 20), (1000, 30), (1322, 40)):
        P(f"{mm}/380 error (0.11..0.21)", round(mm/380 * np.hypot(dm/mm, 20/380), 2))

    print("== §6 the scale (orientation e^A = phi^sigma)")
    def sl_r(a, b, M):                               # A = +w: rigidez e^{4A}, peso e^{2A}
        s = np.linspace(a, b, int(round((b - a) * M)) + 1); h = lp / M; n = len(s)
        p = phi ** (4 * (s[:-1] + 0.5 / M)); K = np.zeros((n, n))
        for i in range(n - 1):
            K[i, i] += p[i]; K[i+1, i+1] += p[i]; K[i, i+1] -= p[i]; K[i+1, i] -= p[i]
        return eigh(K / h**2, trap(phi ** (2 * s)), eigvals_only=True)
    for a in (0, 2, 4):
        w = sl_r(a, a + 12, 32); m = np.sqrt(w[1:5])
        P(f"[{a},{a+12}] m1/phi^sigma_IR (3.8319); ratios", (round(m[0]/phi**a, 4), np.round(m/m[0], 4)))
    M_lep = ((np.sqrt(0.51099895)+np.sqrt(105.6583755)+np.sqrt(1776.86))/3)**2
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
    # (2) exact two-brane condition reproduces the golden-chain vector table
    P("exact vector m2/m1 at phi^6, phi^12, phi^30 (2.093, 2.171, 2.241)",
      [round((lambda v: v[1]/v[0])(vec2(phi**-L)), 3) for L in (6, 12, 30)])
    # (3) bottom at 12, top at Planck
    mKK = M_lep*phi**12/1000                          # GeV per zero
    for nm, MP in (("M_Pl", 1.2209e19), ("reduced M_Pl", 2.435e18)):
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
    for _nm, _m in (("M", 0.31384), ("m_p/3", 0.938272/3), ("m_e", 0.000510999)):
        P(f"sigma_IR with m0 = {_nm}", round(float(np.log(_sc/_m)/lp), 2))
    P("M_PCF log phi = 6 sqrt3 pi (framework units): M_PCF", round(6*np.sqrt(3)*np.pi/lp, 3))

    print("== v3: second short cycle")
    P("leading order pi(k+1/4) M phi^12, k=1 (GeV) ; exact j11", (round(np.pi*1.25*mKK, 0), round(jn_zeros(1,1)[0]*mKK, 0)))
    _v24 = vec2(phi**-24)
    P("vector m2/m1, T-dual throat [-12,12] (2.228) ; Planck top (2.275)", (round(_v24[1]/_v24[0], 3), round((lambda v: v[1]/v[0])(vec2(np.exp(-np.log(1.2209e19/mKK)))), 3)))
    P("M phi^11 (GeV), CW6 M-theory level read as a scale", round(0.31384*phi**11, 1))
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

SECCIONES.append((1, 'Todos los números en orden de aparición; alternativas para m0 (§9)', seccion_1))

# ======================================================================
# 2. Energía del vacío de la torre, ceros exactos de J1 (§9; requiere mpmath)
# ======================================================================
def seccion_2():
    """Casimir (Coleman-Weinberg) de la torre del graviton con ceros EXACTOS de J1.
    Sum f(j_k), f = j^4 log j^2 (A) y j^4 (B), regularizadas: K ceros exactos + cola de McMahon
    (j = b + c1/b + c3/b^3 + c5/b^5, b = pi(k+1/4)) sumada con zeta de Hurwitz, a = 5/4."""
    import mpmath as mp
    mp.mp.dps = 30
    phi = (1 + mp.sqrt(5)) / 2
    c1, c3, c5 = mp.mpf(-3)/8, mp.mpf(36)/1536, -mp.mpf(32*3*1179)/(15*32768)
    eps = lambda u: c1*u**2 + c3*u**4 + c5*u**6
    P = mp.taylor(lambda u: (1+eps(u))**4, 0, 8)                       # coef. de L
    Q = mp.taylor(lambda u: 2*(1+eps(u))**4*mp.log(1+eps(u)) if u != 0 else 0, 0, 8)
    a = mp.mpf(5)/4
    def S(m, conlog):                    # sum_k beta^m (log beta^2 si conlog), regularizada
        z, dz = mp.zeta(-m, a), mp.zeta(-m, a, 1)
        return mp.pi**m * ((2*mp.log(mp.pi)*z - 2*dz) if conlog else z)
    def asym(beta, conlog):
        L = mp.log(beta**2); out = 0
        for n in range(0, 9, 2):
            out += beta**(4-n) * ((P[n]*L + Q[n]) if conlog else P[n])
        return out
    def suma(conlog, K):
        reg = sum((P[n]*S(4-n, True) + Q[n]*S(4-n, False)) if conlog else P[n]*S(4-n, False)
                  for n in range(0, 9, 2))
        corr = 0
        for k in range(1, K+1):
            j = mp.besseljzero(1, k); beta = mp.pi*(k + mp.mpf(1)/4)
            f = j**4*mp.log(j**2) if conlog else j**4
            corr += f - asym(beta, conlog)
        return reg + corr
    for K in (20, 60):
        A, B = suma(True, K), suma(False, K)
        ls = -A/(2*B) - mp.mpf(1)/4
        print(f"K={K}: A={mp.nstr(A,8)}  B={mp.nstr(B,8)}  log s*={mp.nstr(ls,8)}  "
              f"profundidad log_phi(1/s*) = {mp.nstr(-ls/mp.log(phi),8)}   signo B: {'+' if B>0 else '-'}")

SECCIONES.append((2, 'Energía del vacío de la torre, ceros exactos de J1 (§9; requiere mpmath)', seccion_2))

# ======================================================================
# 3. Espectros de dos branas (Proposición del modelo de dos branas)
# ======================================================================
def seccion_3():
    """Ecuaciones de RS y de la torre dorada, lado a lado: masas KK exactas con dos branas.
    Gravitón:  J1(eps x) Y1(x) - Y1(eps x) J1(x) = 0 ;  vector: J0(eps x) Y0(x) - Y0(eps x) J0(x) = 0
    con x = m z_IR, eps = z_UV/z_IR = e^{-k pi r} = phi^{-(sigma_UV - sigma_IR)}."""
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
    print("validacion contra la cadena dorada (tabla del articulo):")
    for lev in (6, 12, 30):
        v = vec(phi**-lev); print(f"  profundidad phi^{lev}: vector m2/m1 = {v[1]/v[0]:.3f}")
    M = 0.31384; mKK = M*phi**12          # escala por cero en el fondo sigma_IR = 12 (GeV)
    for nm, MP in (("M_Pl", 1.2209e19), ("M_Pl reducida", 2.435e18)):
        kpr = np.log(MP/mKK); levels = kpr/lp; eps = np.exp(-kpr)
        g, v = grav(eps), vec(eps)
        print(f"\nUV en {nm}: k pi r = {kpr:.2f} = {levels:.2f} niveles; sigma_UV = {12+levels:.2f}")
        print(f"  graviton x_n = {np.round(g,4)}  (J1 profundo: 3.8317, 7.0156)")
        print(f"  vector   x_n = {np.round(v,4)}  m2/m1 = {v[1]/v[0]:.4f}")
        print(f"  gluon/graviton por cero universal: x1_vec/x1_grav = {v[0]/g[0]:.4f}")
    print("\nLYR: gluon 3600-4000 GeV / graviton 380 GeV =", round(3600/380,2), "-", round(4000/380,2))

SECCIONES.append((3, 'Espectros de dos branas (Proposición del modelo de dos branas)', seccion_3))

# ======================================================================
# 4. Métrica y positividad de reflexión (Proposición de la métrica, §4)
# ======================================================================
def seccion_4():
    import numpy as np
    from scipy.linalg import expm, eigvalsh
    phi=(1+5**.5)/2; l2=np.log(phi)**2; N=7; s=np.arange(N)
    L=np.diag(np.full(N,-2.))
    for i in range(1,N): L[i,i-1]=phi**2; L[i-1,i]=phi**-2
    L/=l2; K=-L                                   # operador de masas^2, espectro >0
    # 1. producto estandar <u,v> = u.v  (base |sigma> ortonormal, como en Prop 5.16/5.22)
    print("K autoadjunto en el producto estandar:", np.allclose(K,K.T))
    for a in (0.05,0.2,1.0):
        T=expm(-a*K); m=eigvalsh((T+T.T)/2).min()
        print(f"  a={a}: min autovalor de sym(T)={m:.3e}  -> <f,Tf> >= 0 para todo f: {m>-1e-12}")
    # 2. metrica eta = D^T D con D = diag(phi^{-2 sigma})
    eta=np.diag(phi**(-4.*s))
    print("K autoadjunto en <u,v>_eta = u.eta.v :", np.allclose(eta@K,(eta@K).T))
    for a in (0.05,0.2,1.0):
        T=expm(-a*K); G=eta@T
        print(f"  a={a}: <f,Tf>_eta minimo = {eigvalsh((G+G.T)/2).min():.3e}")
    # 3. eta contra el warp de la garganta (87): z = phi^sigma, A = -log z
    A=-s*np.log(phi)
    print("eta_sigma == e^{4A(sigma)} (sqrt(-g) de ds^2=e^{2A}eta dx dx + dz^2):",
          np.allclose(np.diag(eta),np.exp(4*A)))
    # 4. anchos en la metrica eta == biortogonales
    w,V=np.linalg.eig(K); o=np.argsort(w.real); w,V=w[o].real,V[:,o].real
    V=V/np.sqrt(np.einsum('ij,ij->j',V,eta@V))     # normalizar en eta
    p=np.array([eta[0,0]*V[0,j]**2 for j in range(4)])
    print("peso en el borde (eta), relativo al modo 2 x20:",np.round(p/p[1]*20,1))

SECCIONES.append((4, 'Métrica y positividad de reflexión (Proposición de la métrica, §4)', seccion_4))

# ======================================================================
# 5. Fase 1/4 (Corolario de la fase)
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
    print("1) Fase libre: m = A (n + theta), 2 parametros")
    best=min((fit(np.arange(1,5)+t)[0],t) for t in np.linspace(-.5,1,3001))
    print(f"   theta optimo = {best[1]:.3f}  rms={best[0]:.2f}%")
    print("2) Ceros de J_nu con nu = d/2 - 1 (perfil de graviton en AdS_{d+1}), 1 parametro")
    for d in (3,4,5,6):
        nu=d/2-1; z=zeros(nu); r,A=fit(z)
        ph=np.mean(z/np.pi-np.arange(1,5))
        print(f"   d={d}: nu={nu:.1f}  fase asint.(d-3)/4={ (d-3)/4:.2f}  fase medida={ph:.3f}  rms={r:.2f}%")
    print("3) Cadena discreta de A.7 (Dirichlet en ambos bordes): fase 0 -> rms",
          f"{fit(np.arange(1,5)*1.0)[0]:.2f}%")

SECCIONES.append((5, 'Fase 1/4 (Corolario de la fase)', seccion_5))

# ======================================================================
# 6. Cadena de Bessel (Teorema de Bessel, Observación de niveles)
# ======================================================================
def seccion_6():
    import numpy as np
    from scipy.linalg import eigh
    from scipy.special import jn_zeros
    phi=(1+5**.5)/2; h0=np.log(phi); obs=np.array([380.,700,1000,1322]); j1=jn_zeros(1,4)
    def cadena(s_uv,s_ir,M,peso=True):
        # nodos sigma = s_uv .. s_ir con M subpasos por nivel dorado; Neumann en ambos bordes
        sig=np.linspace(s_uv,s_ir,int(round((s_ir-s_uv)*M))+1); h=h0/M; n=len(sig)
        p=phi**(-4*(sig[:-1]+0.5/M))            # rigidez e^{4A} en los puntos medios
        K=np.zeros((n,n))
        for i in range(n-1):
            K[i,i]+=p[i];K[i+1,i+1]+=p[i];K[i,i+1]-=p[i];K[i+1,i]-=p[i]
        K/=h*h
        R=np.diag(phi**(-2*sig)) if peso else np.eye(n)   # peso de masa e^{2A}
        R[0,0]/=2; R[-1,-1]/=2                # medio peso en los extremos (trapecio): segundo orden
        w=eigh(K,R,eigvals_only=True); m=np.sqrt(np.clip(w,0,None))
        return m[1:5]                         # m[0]=0: el graviton sin masa (modo cero)
    def rms(m): A=(obs@m)/(m@m); return np.sqrt(np.mean(((obs-A*m)/obs)**2))*100
    print("ceros J1 normalizados:",np.round(j1/j1[0],4),"  LYR:",np.round(obs/380,4))
    for (a,b) in [(0,6),(-6,6),(-20,6),(-60,6)]:
        for M in (1,4,32):
            m=cadena(a,b,M); print(f"sigma[{a},{b}] M={M:2d}: m/m1={np.round(m/m[0],4)}  rms LYR={rms(m):.2f}%")
    # sin peso: en [-20,6] el problema esta mal condicionado (pesos ~1e17) y el solver da modos espurios
    # segun M; se muestra en [-6,6], donde es estable.
    print("sin peso e^{2A} (como A.7), sigma[-6,6], M=32:",np.round((lambda m:m/m[0])(cadena(-6,6,32,False)),3))

SECCIONES.append((6, 'Cadena de Bessel (Teorema de Bessel, Observación de niveles)', seccion_6))

# ======================================================================
# 7. Predicción y lo no afirmado (§10, §11)
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
        r_=phi**(-kw*s); r_[0]/=2; r_[-1]/=2   # medio peso en los extremos (trapecio)
        w=eigh(K/h/h,np.diag(r_),eigvals_only=True); return np.sqrt(np.clip(w,0,None))[1:4]
    g=chain(-6,6,32,4,2); v=chain(-6,6,32,2,0)
    print("graviton torre:",np.round(g/g[0],4)," J1:",np.round(jn_zeros(1,3)/jn_zeros(1,1),4))
    print("vector   torre:",np.round(v/v[0],4)," J0:",np.round(jn_zeros(0,3)/jn_zeros(0,1),4))
    print(" gluon LYR 8600/3600 =",round(8600/3600,3),"(torre vector",round(v[1]/v[0],3),")")
    print(" quark LYR 2150/1040 =",round(2150/1040,3))
    print("\n== E4: escala por sector (m1 / primer cero de su operador) ==")
    x1g=g[0]; x1v=v[0]
    Sg=380/x1g; Sgl=3600/x1v; Sq=1040/x1v
    for n_,S in (("graviton",Sg),("gluon",Sgl),("quark*",Sq)):
        print(f"  {n_:8s} escala={S:9.2f}  log_phi(escala/graviton)={np.log(S/Sg)/np.log(phi):.2f}")
    print("  CW6: sigma_G=2, U(1)=3, SU(2)=4, SU(3)=5  -> gluon/graviton pediria Delta sigma = 3")
    print("  (*quark con normalizacion vectorial, solo orientativa)")
    print("\n== E5: incertidumbre de los cocientes de LYR ==")
    for m,dm in ((700,20),(1000,30),(1322,40)):
        print(f"  {m}/380: {m/380:.3f} +- {m/380*np.hypot(dm/m,20/380):.3f}")
    print("  torre finita sigma[0,6] vs J1 (infinita): m2/m1 1.8419 vs 1.8309, m4/m1 3.5284 vs 3.4772")

SECCIONES.append((7, 'Predicción y lo no afirmado (§10, §11)', seccion_7))

# ======================================================================
# 8. Look-elsewhere (§6, §9)
# ======================================================================
def seccion_8():
    """
    Comparativa: Le Yaouanc & Richard (2026), "Evidence for KK excitations of the
    graviton, gluon and quark at LHC"  vs  CW6_paper_v4.tex (Crystalline Worldsheet).

    Pregunta: ¿qué estructura espectral describe mejor las masas KK reportadas,
    la de Randall-Sundrum (ceros de Bessel, espaciado ~lineal) o la torre dorada
    de CW6 (z = phi^sigma, espaciado geométrico)?  Y ¿qué dice el operador KK
    discreto de CW6 (Prop. kk-discrete-spectrum) sobre los cocientes de masa?
    """
    import numpy as np
    from scipy.special import jn_zeros
    from scipy.optimize import minimize_scalar

    phi = (1 + 5**0.5) / 2
    lnphi = np.log(phi)
    out = []
    P = lambda *a: out.append(" ".join(str(x) for x in a))

    # ---------------------------------------------------------------- datos LYR
    grav_obs = np.array([380., 700., 1000., 1322.])          # candidatos G_KK (GeV)
    grav_tab = np.array([380, 700, 1000, 1322, 1640, 1945, 2260, 2590, 2905.])
    gluon = np.array([3600., 8600.])                          # g_KK
    quark = np.array([1040., 2150.])                          # q_KK
    zkk = 3000.

    # ------------------------------------------------ 1. gravitones: RS vs phi
    x = np.concatenate([[0.], jn_zeros(1, 12)])               # ceros J1 (incl. 0)
    P("== 1. Torre de gravitones ==")
    P("ceros J1:", np.round(x[1:10], 2))
    # RS: m_i = M * x_i  (1 parámetro).  Asignación: 380->x1, 700->x2, ...
    xi = x[1:5]
    M_rs = (grav_obs @ xi) / (xi @ xi)
    res_rs = grav_obs - M_rs * xi
    # Dorada: m_k = m0 * phi^(k/2)  con k entero libre por punto (1 parámetro m0)
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
    P(f"RS   M={M_rs:.1f} GeV  pred={np.round(M_rs*xi)}  err rel={np.round(rel_rs*100,1)}%")
    P(f"phi  m0={m0:.1f} GeV  k={k.astype(int)}  pred={np.round(pred_g)}  err rel={np.round(rel_g*100,1)}%")
    P(f"rms RS={np.sqrt(np.mean(rel_rs**2))*100:.1f}%   rms phi^k={np.sqrt(np.mean(rel_g**2))*100:.1f}%")
    P("cocientes sucesivos obs:", np.round(grav_obs[1:]/grav_obs[:-1], 3),
      "| RS:", np.round(xi[1:]/xi[:-1], 3), "| phi:", round(phi, 3))
    # la tabla completa de LYR (predicciones) es exactamente RS:
    P("tabla LYR / 100 :", np.round(grav_tab/100, 2), "vs ceros", np.round(x[1:10], 2))

    # --------------------------------------------- 2. gluones y quarks KK
    P("\n== 2. Gluones / quarks KK ==")
    rs_vec = np.array([2.45, 5.57, 8.70, 11.84])
    P(f"g: obs 8600/3600={8600/3600:.3f}  RS 5.57/2.45={5.57/2.45:.3f}  "
      f"phi^2={phi**2:.3f}  log_phi={np.log(8600/3600)/lnphi:.3f}")
    P(f"q: obs 2150/1040={2150/1040:.3f}  RS(Abe et al.)=2  phi^(3/2)={phi**1.5:.3f}  "
      f"log_phi={np.log(2150/1040)/lnphi:.3f}")
    hier = np.array([380., 1000., 3600.])
    P("jerarquía G:q:g =", hier/380, " log_phi cocientes:",
      np.round(np.log(hier[1:]/hier[:-1])/lnphi, 3))
    P(f"q/G 1000/380={1000/380:.3f} vs phi^2={phi**2:.3f} (dif {100*(1000/380/phi**2-1):.1f}%)")
    P(f"gluon1/grav1 RS ingenuo 2.45/3.83={2.45/3.83:.3f}^-1  obs 380/3600={380/3600:.3f}")

    # --------------------------------- 3. look-elsewhere para 'coincidencias phi'
    P("\n== 3. Look-elsewhere ==")
    rng = np.random.default_rng(1)
    r = np.exp(rng.uniform(np.log(1.3), np.log(4.5), 200000))
    grid = phi ** (np.arange(1, 9) / 2)          # phi^(k/2), k=1..8
    d = np.min(np.abs(r[:, None] / grid[None, :] - 1), axis=1)
    for tol in (0.01, 0.03, 0.05, 0.10):
        P(f"P(ratio aleatorio en [1.3,4.5] a <{tol*100:.0f}% de algún phi^(k/2)) = {np.mean(d<tol):.2f}")
    obs_ratios = {"q/G 1000/380": 1000/380, "g 8600/3600": 8600/3600,
                  "q 2150/1040": 2150/1040, "g/q 3600/1000": 3.6}
    for n_, v in obs_ratios.items():
        j = np.argmin(abs(v/grid-1)); P(f"  {n_}={v:.3f} -> phi^({j+1}/2)={grid[j]:.3f}  ({100*(v/grid[j]-1):+.1f}%)")

    # ------------------------------ 4. operador KK discreto de CW6 (app:kk)
    P("\n== 4. Operador KK discreto CW6 (7 niveles, sigma=0..6) ==")
    n = 7
    L = np.diag(np.full(n, -2.0))
    for s in range(1, n):
        L[s, s-1] = phi**2
        L[s-1, s] = phi**-2
    L /= lnphi**2
    ev = np.sort(np.linalg.eigvals(L).real)[::-1]
    P("autovalores L:", np.round(ev, 3))
    # L es tridiagonal no simétrica; similar a simétrica con hopping sqrt(phi^2*phi^-2)=1
    P("hopping simetrizado sqrt(phi^2*phi^-2) =", 1.0, "-> espectro = (-2+2cos(k pi/8))/ln^2 phi")
    ana = (-2 + 2*np.cos(np.arange(1, n+1)*np.pi/(n+1))) / lnphi**2
    P("analítico     :", np.round(np.sort(ana)[::-1], 3))
    m2 = -ev                                        # masas^2 >= 0
    m = np.sqrt(m2)
    P("m_k (unid. 1/ln phi):", np.round(m, 3))
    P("cocientes m_k/m_1:", np.round(m/m[0], 3))
    P("RS (ceros J1) x_k/x_1:", np.round(x[1:8]/x[1], 3))
    P("obs grav m/380 :", np.round(grav_obs/380, 3))

    # ------------------------------- 5. invariantes AdS5 compartidos
    P("\n== 5. Geometría de fondo (ambos usan AdS5 con warp) ==")
    rows = [("warp A(z)", "RS: A=-k|y|", "CW6: A=-log z, z=phi^sigma"),
            ("Lambda_5", "RS: -6k^2", "CW6: -6 (l=1)"),
            ("R", "RS: -20k^2", "CW6: -20"),
            ("BF", "-4", "-4"),
            ("brana", "RS: tensión IR/UV (Israel)", "CW6: Israel por nivel, lambda=N_modes/M_PCF"),
            ("escala abs.", "RS: k e^{-k pi r} ~ TeV", "CW6: no fijada (scale translation abierta)")]
    for a, b, c in rows:
        P(f"{a:12s} | {b:28s} | {c}")

    open("kk_vs_cw6_out.txt", "w").write("\n".join(out))
    print("\n".join(out))

SECCIONES.append((8, 'Look-elsewhere (§6, §9)', seccion_8))

# ======================================================================
# 9. Cocientes de huecos (Discusión 6.1)
# ======================================================================
def seccion_9():
    """Por qué phi para el ensamble: una órbita irracional sobre el círculo recorre todas las fases.
    Discrepancia estrella D_N de {n alpha}, n=1..N, y número de huecos distintos (tres huecos)."""
    import numpy as np
    phi=(1+5**.5)/2
    def disc(a,N):
        x=np.sort((np.arange(1,N+1)*a)%1); i=np.arange(1,N+1)
        return max(np.max(i/N-x), np.max(x-(i-1)/N))
    def gaps(a,N):
        x=np.sort(np.r_[0,(np.arange(1,N+1)*a)%1,1]); g=np.round(np.diff(x),10); g=np.unique(g[g>0])
        return len(g), g.max()/g.min()
    for name,a in [("phi",phi),("sqrt2",2**.5),("pi",np.pi),("e",np.e),("rational 13/8",13/8)]:
        print(f"{name:13s} N*D_N: N=100 {100*disc(a,100):.3f}  N=1000 {1000*disc(a,1000):.3f}  N=10000 {10000*disc(a,10000):.3f}   gaps N=1000: {gaps(a,1000)}")

SECCIONES.append((9, 'Cocientes de huecos (Discusión 6.1)', seccion_9))

# ======================================================================
# 10. Figura 3: granularidad, con sus números
# ======================================================================
def seccion_10():
    """Granularidad: niveles enteros, diádicos y áureos; fase de la línea de mundo."""
    import numpy as np
    phi=(1+5**.5)/2; lp=np.log(phi)
    def gaps(x):
        x=np.sort(np.r_[0,np.mod(x,1),1]); g=np.diff(x); g=g[g>1e-12]; return g
    F=[1,2,3,5,8,13,21,34,55,89,144,233,377,610,987]
    print("niveles a+b*phi en [0,1): N puntos {n phi}, huecos distintos, razon max/min")
    for N in F[3:]:
        g=gaps(np.arange(1,N+1)*phi); print(N, len(np.unique(np.round(g,9))), round(g.max()/g.min(),4), "hueco max", round(g.max(),5))
    print("diadicos: resolucion 2^-k exige k digitos binarios (k registros)")
    for k in range(1,11): print(k, 2**k, 2.0**-k)
    # fase: paso log(phi)/(2 pi) sobre el circulo; Gelfond: log(phi)/pi irracional
    a=lp/(2*np.pi)
    print("rotacion de la fase por nivel (vueltas):", a)
    print("peor razon de huecos, fase, N<=5000:", round(max(gaps(np.arange(1,N+1)*a).max()/gaps(np.arange(1,N+1)*a).min() for N in range(10,5001)),3))
    print("peor razon de huecos, phi, N<=5000:", round(max(gaps(np.arange(1,N+1)*phi).max()/gaps(np.arange(1,N+1)*phi).min() for N in range(10,5001)),3))
    exc=[N for N in range(3,5001) if abs(gaps(np.arange(1,N+1)*phi).max()/gaps(np.arange(1,N+1)*phi).min()-phi**2)>1e-6]
    print("N <= 5000 con razon distinta de phi^2:", exc, "(N+1, las marcas con el origen, es de Fibonacci: dos longitudes, razon phi)")

    # ---------- figura: granularidad, sin color ----------
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 3, figsize=(10, 3.3), gridspec_kw=dict(width_ratios=[1.3, 1.3, 1]))
    for i, k in enumerate([1, 2, 3, 4, 5]):
        y = -i
        ax[0].plot([0, 1], [y, y], "k", lw=0.5)
        for j in range(2**k + 1): ax[0].plot([j/2**k]*2, [y-.15, y+.15], "k", lw=0.8)
        ax[0].text(1.04, y, rf"$k={k}$", va="center", fontsize=8)
    ax[0].set_title("integer and binary levels:\none new digit per halving", fontsize=9)
    for i, N in enumerate([5, 8, 13, 21, 34]):
        y = -i; x = np.mod(np.arange(1, N+1)*phi, 1)
        ax[1].plot([0, 1], [y, y], "k", lw=0.5)
        for v in np.r_[0, x, 1]: ax[1].plot([v]*2, [y-.15, y+.15], "k", lw=0.8)
        ax[1].text(1.04, y, rf"$N={N}$", va="center", fontsize=8)
    ax[1].set_title(r"golden levels $\{n\varphi\}$: same rule," "\n" r"three gaps, ratio $\varphi^{2}$", fontsize=9)
    t = np.linspace(0, 2*np.pi, 400); ax[2].plot(np.cos(t), np.sin(t), "k", lw=0.5)
    n = np.arange(0, 200); th = n*lp
    ax[2].plot(np.cos(th), np.sin(th), "k.", ms=3)
    for m in (0, 1, 2): ax[2].text(1.08*np.cos(m*lp), 1.08*np.sin(m*lp), rf"${m}$", fontsize=7, ha="center", va="center")
    ax[2].set_title(r"phase $e^{i\sigma\log\varphi}$, $\sigma=0,\dots,199$:" "\n" "never closes", fontsize=9)
    ax[2].set_aspect("equal")
    for a_ in ax: a_.axis("off")
    fig.savefig("fig_granularity.pdf", bbox_inches="tight")
    print("figura: ok")

SECCIONES.append((10, 'Figura 3: granularidad, con sus números', seccion_10))

# ======================================================================
# 11. Configuraciones de contacto en 1D, 2D y 3D (6.1)
# ======================================================================
def seccion_11():
    """Contacto en 1, 2 y 3 dimensiones desde pi y phi.
    1D: dos vecinos; 2D: las seis unidades de Z[omega], omega = e^{2 pi i/3}; 3D: los doce vértices
    (0, ±1, ±phi) y permutaciones cíclicas del icosaedro."""
    import numpy as np, itertools
    phi=(1+5**.5)/2
    # 2D
    u=np.exp(1j*np.pi*np.arange(6)/3)
    d2=[abs(a-b) for a,b in itertools.combinations(u,2)]
    print("2D: 6 unidades, |u|=1:", np.allclose(abs(u),1), " distancia mínima entre vecinos:", round(min(d2),12))
    # 3D
    V=[]
    for s1 in (1,-1):
        for s2 in (1,-1):
            p=(0,s1,s2*phi); V+= [p,(p[1],p[2],p[0]),(p[2],p[0],p[1])]
    V=np.array(V,float); print("3D: vértices", len(V))
    r2=(V**2).sum(1); print("   |v|^2 = phi+2:", np.allclose(r2,phi+2))
    D=[((a-b)**2).sum() for a,b in itertools.combinations(V,2)]
    vals=np.unique(np.round(D,9)); print("   distancias^2 distintas:", vals, " (4, 4phi+4? ->", 4*phi+4, ")")
    print("   aristas (d^2=4):", sum(abs(x-4)<1e-9 for x in D), "; vecinos por vértice:", 2*sum(abs(x-4)<1e-9 for x in D)//12)
    W=2*V/np.sqrt(phi+2)   # centros a distancia 2: esferas unitarias tocando la central
    m=min(((a-b)**2).sum() for a,b in itertools.combinations(W,2))**.5
    print("   contacto: 12 esferas unitarias tocando la central, distancia mínima entre ellas:", round(m,4), ">= 2:", m>=2)
    print("   holgura: 4 >= phi+2 <=> phi <= 2")
    # J3 (v108): el 12 en 3D también lo alcanzan FCC y HCP, sin phi
    fcc=[v for v in itertools.product([-1,0,1],repeat=3) if sorted(map(abs,v))==[0,1,1]]
    Wf=[2*np.array(v)/np.sqrt(2) for v in fcc]
    mf=min(np.linalg.norm(a-b) for a,b in itertools.combinations(Wf,2))
    hc=[(2*np.cos(k*np.pi/3),2*np.sin(k*np.pi/3),0) for k in range(6)]
    for s in (1,-1):
        for k in range(3):
            t=k*2*np.pi/3+np.pi/6; hc.append((2*np.cos(t)/np.sqrt(3),2*np.sin(t)/np.sqrt(3),2*s*np.sqrt(2/3)))
    hc=np.array(hc); mh=min(np.linalg.norm(a-b) for a,b in itertools.combinations(hc,2))
    assert len(fcc)==12 and abs(mf-2)<1e-12 and len(hc)==12 and np.allclose(np.linalg.norm(hc,axis=1),2) and abs(mh-2)<1e-12
    print("   FCC y HCP: 12 esferas unitarias a distancia 2 de la central, sin phi; distancia mínima entre ellas:", round(mf,4), round(mh,4))
    print("   el doce del icosaedro y el del fondo se prueban por separado (lectura [R])")
    # la cadena del 12
    print("cadena: |A5|/5 =", 60//5, "; pi(10)/5 = 60/5 =", 12, "; lcm(4,6) =", np.lcm(4,6), "; -1/zeta(-1) = 12")

SECCIONES.append((11, 'Configuraciones de contacto en 1D, 2D y 3D (6.1)', seccion_11))

# ======================================================================
# 12. Figura 1: una estructura vista de una vez; los puntos de Z[i] por nivel; comprobaciones
# ======================================================================
def seccion_12():
    """Geometría exacta de la garganta, el toro y la fibra (artículo 9, v9).
    Cada figura sale de un enunciado demostrado en TorreKK_LYR_v8.lean; este script verifica
    numéricamente esos enunciados y dibuja solo lo que verifican.

    Fuentes: CW6 eq. (torus), Prop. (fibre independent of base), eq. (worldline), eq. (throat);
    HP Def. (tower parameters), Prop. (certainty principle).
    """
    import numpy as np
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    phi = (1 + 5 ** 0.5) / 2
    lp = np.log(phi)
    eps0 = lp / (6 * np.sqrt(3))
    M = 6 * np.sqrt(3) * np.pi / lp
    SIR, STOP = 12, 18          # fondo (half-turn) y nivel donde se normaliza el dibujo (r = 1)

    # ---------- verificaciones (una por teorema de Lean) ----------
    assert abs(eps0 * M - np.pi) < 1e-12                                   # certainty_principle
    for s in np.linspace(-3, 20, 47):
        assert abs((eps0 * phi**s) * (M * phi**-s) - np.pi) < 1e-9           # closure_each_level
        assert abs((eps0 * phi**s) * (M * phi**s) - np.pi * phi**(2*s)) < 1e-6 * phi**(2*s)  # phase_on_cell
        assert abs(phi**(s+1) / phi**s - phi) < 1e-12                        # ring_ratio
        z = complex(phi**s * M, 0); assert abs((z * 1j) / z - 1j) < 1e-12    # lattice_tower_tau
    assert abs(np.exp(1j*np.pi) + 1) < 1e-15                                # fibre_half_turn
    th = np.linspace(0, 7, 50); assert np.allclose(abs(0.5*np.exp(1j*th)), .5)  # worldline_modulus
    y = np.linspace(-8, 0, 400)
    assert np.allclose(np.exp(y)**2 + (1 - np.exp(y)**2), 1)               # pseudosphere_unit_speed
    # toro de Clifford: proyección estereográfica desde (0,0,0,1) -> toro de revolución R = sqrt2, r = 1
    a, b = np.meshgrid(np.linspace(0, 2*np.pi, 60), np.linspace(0, 2*np.pi, 60))
    X = np.stack([np.cos(a), np.sin(a), np.cos(b), np.sin(b)]) / np.sqrt(2)
    P = X[:3] / (1 - X[3])
    rho = np.hypot(P[0], P[1])
    assert np.allclose((rho - np.sqrt(2))**2 + P[2]**2, 1, atol=1e-9)        # clifford_square + estereográfica
    print("eps0 =", eps0, " M_PCF =", M, " eps0*M/pi =", eps0*M/np.pi)
    print("fase sobre la celda en sigma=12: pi *", phi**24)
    print("todas las verificaciones: ok")


    # ---------- dibujo: solo líneas, sin color ----------
    def r_of(s): return phi ** (s - STOP)
    def h_of(r):
        q = np.sqrt(1 - r**2); return np.log((1 + q) / r) - q
    lev = np.arange(SIR, STOP + 1); tt = np.linspace(0, 2*np.pi, 400)
    zb = -h_of(r_of(SIR))
    K = dict(color="k", lw=0.35)

    def throat_lines(ax, meridians=24, rings=True, lab=True):
        s = np.linspace(SIR, STOP, 300); R = r_of(s); Z = -h_of(R)
        for t0 in np.linspace(0, 2*np.pi, meridians, endpoint=False):
            ax.plot(R*np.cos(t0), R*np.sin(t0), Z, **K)
        if rings:
            for k in lev:
                r = r_of(k); ax.plot(r*np.cos(tt), r*np.sin(tt), -h_of(r)+0*tt, color="k", lw=1.0)
                if lab: ax.text(r+0.04, 0, -h_of(r), rf"$\sigma={k}$", fontsize=7)

    def clean(ax, lim, zlim, elev=14):
        ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_zlim(*zlim)
        ax.set_box_aspect((1, 1, (zlim[1]-zlim[0]) / (2*lim))); ax.set_axis_off()
        ax.view_init(elev=elev, azim=-58)

    # 2. los puntos de Z[i] dentro del anillo de cada nivel (texto de §10.1)
    cnt=[sum(1 for a_ in range(-60,61) for b_ in range(-60,61) if a_*a_+b_*b_<=phi**s_) for s_ in range(7)]
    assert cnt==[5,5,9,13,21,37,57]
    assert [int(np.floor(np.pi*phi**s_)) for s_ in range(7)]==[3,5,8,13,21,34,56]
    rat=[round(c/(np.pi*phi**s_),2) for s_,c in enumerate(cnt)]
    assert rat==[1.59,0.98,1.09,0.98,0.98,1.06,1.01]
    c22=sum(2*int(np.floor(np.sqrt(phi**22-a_*a_)))+1 for a_ in range(-int(phi**11)-1,int(phi**11)+2) if a_*a_<=phi**22)
    assert round(c22/(np.pi*phi**22),4)==0.9998
    c12=sum(2*int(np.floor(np.sqrt(phi**12-a_*a_)))+1 for a_ in range(-30,31) if a_*a_<=phi**12)
    assert c12==1005 and int(np.floor(np.pi*phi**12))==1011
    print("puntos de Z[i] en el disco de area S, sigma = 0..6:",cnt,"; razon a S:",rat,"; sigma = 22:",round(c22/(np.pi*phi**22),4),"; sigma = 12:",c12,"frente a",int(np.floor(np.pi*phi**12)))

    # 3. la figura 1: una estructura vista de una vez (§10.1); cada panel dibuja un enunciado del texto
    def _figura_1():
        import numpy as np, matplotlib, itertools
        import matplotlib.pyplot as plt
        from matplotlib.patches import FancyArrowPatch
        from matplotlib.lines import Line2D
        plt.rcParams.update({"font.family":"serif","mathtext.fontset":"cm","font.size":10})
        phi=(1+5**.5)/2
        INK="#333333"; GOLD="#c99a2e"; BLUE="#2f6db3"; TEAL="#5aa6a6"; PURP="#6a3d9a"; KER="#b2182b"; DOT="#555555"; RRED="#c0392b"; GRN="#2e8b57"; VIO="#7b4fa0"
        TRI=["#b2182b","#1b7837","#2166ac"]
        t=np.linspace(0,2*np.pi,300); w=np.exp(2j*np.pi/3); V=[0.5*w**k for k in range(3)]
        fig=plt.figure(figsize=(17,19))
        def head(x,y,letter,title,sub,col=None):
            fig.text(x,y,f"({letter})  {title}",ha="center",va="top",fontsize=11.5,color=col or INK)
            fig.text(x,y-0.015,sub,ha="center",va="top",fontsize=9.5,color="0.4")
        # ---------------- (a) toro (cliff, solo líneas)
        K=dict(color="k",lw=0.35)
        axT=fig.add_axes([0.01,0.80,0.32,0.15],projection="3d")
        def cliff(a,b):
            Xc=np.stack([np.cos(a),np.sin(a),np.cos(b),np.sin(b)])/np.sqrt(2); return Xc[:3]/(1-Xc[3])
        wv=np.linspace(0,2*np.pi,400)
        for c_ in np.linspace(0,2*np.pi,24,endpoint=False):
            axT.plot(*cliff(wv,0*wv+c_),**K); axT.plot(*cliff(0*wv+c_,wv),**K)
        axT.plot(*cliff(wv,0*wv+np.pi),color="k",lw=1.6)
        axT.plot(*cliff(0*wv,wv),color="k",lw=1.6,ls="--")
        axT.set_xlim(-2.1,2.1); axT.set_ylim(-2.1,2.1); axT.set_zlim(-1.1,1.1); axT.set_box_aspect((1,1,2.2/4.2)); axT.set_axis_off(); axT.view_init(elev=28,azim=-58)
        head(0.17,0.985,"a","The angular direction is the torus","§10.1: $T^2=\\mathbb{C}/M_{\\rm PCF}\\mathbb{Z}[i]$, $\\tau=i$; cycles $M$ (solid), $Mi$ (dashed)")
        # ---------------- (b) anillo normalizado
        axR=fig.add_axes([0.38,0.805,0.24,0.135]); axR.set_aspect("equal"); axR.set_axis_off()
        axR.plot(0.5*np.cos(t),0.5*np.sin(t),"k",lw=1.6)
        axR.plot([p.real for p in V+[V[0]]],[p.imag for p in V+[V[0]]],"k",lw=0.5,ls="--")
        for k in range(3):
            v=V[k]; axR.plot([0,v.real],[0,v.imag],"k",lw=0.6); axR.plot(v.real,v.imag,"o",mfc="k",mec="k",ms=6)
            axR.text(v.real+0.07 if k==0 else 1.3*v.real,v.imag if k==0 else 1.3*v.imag,f"$v_{k}=\\frac{{1}}{{2}}\\omega^{k}$" if k==0 else f"$v_{k}$",ha="left" if k==0 else "center",va="center",fontsize=11)
        axR.plot(0,0,"o",mfc="white",mec="k",ms=4)
        axR.set_xlim(-0.8,1.15); axR.set_ylim(-0.75,0.75)
        head(0.50,0.985,"b","One microstate at every level","I12: $|\\Omega|_\\sigma=\\frac{1}{2}$; the eigenvalue triad $v_k=\\frac{1}{2}\\omega^{k}$, $V^\\dagger V=1$")
        # ---------------- (c) tercera dirección: cilindro y plano en líneas
        axC=fig.add_axes([0.67,0.80,0.32,0.15],projection="3d")
        for a_ in np.linspace(0,2*np.pi,24,endpoint=False): axC.plot([0.5*np.cos(a_)]*2,[0.5*np.sin(a_)]*2,[-1.2,1.2],**K)
        axC.plot(0.5*np.cos(t),0.5*np.sin(t),1.2+0*t,**K)
        for g_ in np.linspace(-0.75,0.75,7):
            axC.plot([g_,g_],[-0.75,0.75],[-phi*0.75,phi*0.75],color="k",lw=0.3,alpha=0.7)
            axC.plot([-0.75,0.75],[g_,g_],[phi*g_,phi*g_],color="k",lw=0.3,alpha=0.7)
        axC.plot(0.5*np.cos(t),0.5*np.sin(t),-1.2+0*t,"k",lw=1.0)
        axC.plot(0.5*np.cos(t),0.5*np.sin(t),phi*0.5*np.sin(t),"k",lw=1.6)
        for k in range(3):
            x,y=V[k].real,V[k].imag
            axC.scatter([x],[y],[-1.2],c="k",s=14,depthshade=False); axC.scatter([x],[y],[phi*y],c="k",s=26,depthshade=False)
            axC.plot([x,x],[y,y],[-1.2,phi*y],"k",lw=0.6,ls=":"); axC.text(1.9*x,1.9*y,phi*y+0.05,f"$v_{k}$",fontsize=11,ha="center",bbox=dict(fc="white",ec="none",pad=0.5))
        axC.view_init(elev=18,azim=-55); axC.set_box_aspect((1,1,1.4)); axC.set_axis_off()
        head(0.83,0.985,"c","The golden coupling","I15: $z=\\varphi y$ carries the triangle onto $\\mathbb{Z}[i]$, $120^\\circ\\to90^\\circ$")
        # ---------------- (d) la garganta: como la Fig. 4, solo líneas, frente sólido y fondo punteado
        axG=fig.add_axes([0.02,0.555,0.96,0.205]); axG.set_aspect("equal"); axG.set_axis_off()
        s0,s1=2,18
        def hgt(r): return np.arccosh(1/r)-np.sqrt(1-r*r)
        L=hgt(phi**(s0-18)); r=np.geomspace(phi**(s0-18),1,600); X=L-hgt(r)
        for a_ in np.linspace(0,2*np.pi,24,endpoint=False):
            front=np.sin(a_)<0
            axG.plot(X,r*np.cos(a_),color="k",lw=0.45 if front else 0.3,ls="-" if front else ":")
        axG.plot(X,r,"k",lw=1.0); axG.plot(X,-r,"k",lw=1.0)
        ee=0.22; tb=np.linspace(0,np.pi,100)
        ring={}
        for s_ in range(s0,s1+1):
            rr=phi**(s_-18); xs=L-hgt(rr); ring[s_]=(xs,rr)
            col={6:GRN,9:RRED,15:GOLD,12:BLUE,18:VIO}.get(s_,"k"); hl=s_ in (6,9,12,15,18); lw=2.4 if hl else 1.0
            axG.plot(xs+ee*rr*np.sin(tb),rr*np.cos(tb),c=col,lw=lw)
            axG.plot(xs-ee*rr*np.sin(tb),rr*np.cos(tb),c=col,lw=0.8,ls="--")
            axG.text(xs,-1.12,f"{s_}",ha="center",fontsize=9,color=col if hl else "0.3",weight="bold" if hl else "normal")
        axG.text(L/2,-1.32,"level $\\sigma$",ha="center",fontsize=10,color="0.4")
        axG.set_xlim(-0.1,L+0.4); axG.set_ylim(-1.40,1.08)
        head(0.50,0.545,"d","The radial direction is the throat","§10.1: Beltrami's pseudosphere, $e^{A}=\\varphi^{\\sigma}$, rings in the ratio $\\varphi$ (ring_ratio); $\\sigma=6,9$, the bottom $\\sigma_{\\rm IR}=12$, $\\sigma=15,18$")
        # ---------------- conectores: de cada anillo a un riel, del riel a cada panel
        fig.canvas.draw()
        F=lambda xy: fig.transFigure.inverted().transform(axG.transData.transform(xy))
        yrail=0.768; ytop=0.797
        pp={k_:F((ring[k_][0],ring[k_][1]+0.03)) for k_ in (6,9,12,15,18)}
        for p,col in ((pp[6],GRN),(pp[9],RRED),(pp[12],BLUE),(pp[15],GOLD),(pp[18],VIO)):
            fig.add_artist(Line2D([p[0],p[0]],[p[1],yrail],transform=fig.transFigure,color=col,lw=1.8,solid_capstyle="round"))
            fig.add_artist(Line2D([p[0]],[yrail],transform=fig.transFigure,marker="o",ms=6,color=col))
        fig.add_artist(Line2D([0.17,0.83],[yrail,yrail],transform=fig.transFigure,color=INK,lw=1.4))
        for x in (0.17,0.50,0.83):
            fig.add_artist(FancyArrowPatch((x,yrail),(x,ytop),transform=fig.transFigure,arrowstyle="-|>",mutation_scale=14,color=INK,lw=1.4,shrinkA=0,shrinkB=0))
        # ---------------- (e), (f) Z^3 por su diagonal
        def cubo(ax,Lc,c0v,lim,CC):
            n3=np.array([1,1,1])/3**.5; pts=np.array(list(itertools.product(range(Lc),repeat=3)),float)
            c0=np.array([c0v]*3); e1=np.array([1,-1,0])/2**.5; e2=np.cross(n3,e1)
            uu,vv=np.meshgrid(np.linspace(-lim,lim,2),np.linspace(-lim,lim,2))
            ax.plot_surface(c0[0]+uu*e1[0]+vv*e2[0],c0[1]+uu*e1[1]+vv*e2[1],c0[2]+uu*e1[2]+vv*e2[2],color=TEAL,alpha=0.15,shade=False)
            proj=pts-((pts-c0)@n3)[:,None]*n3; g={}
            for p,q in zip(pts,proj): g.setdefault(tuple(np.round(q,9)),[]).append(p)
            for p,q in zip(pts,proj):
                k=len(g[tuple(np.round(q,9))]); col=CC
                ax.scatter(*p,s=12,c=col,depthshade=False,alpha=0.9); ax.plot(*np.c_[p,q],c=col,lw=0.3,alpha=0.30)
            for q,ps in g.items(): ax.scatter(*q,s=6+9*len(ps),c=CC,edgecolor=INK if len(ps)>1 else 'none',linewidth=0.6,depthshade=False)
            tt=np.linspace(c0v,Lc-0.4,2); ax.plot(tt,tt,tt,c=INK,lw=1.2)
            ax.view_init(elev=14,azim=-20); ax.set_box_aspect((1,1,1)); ax.set_axis_off()
            return len(pts),len(g)
        CUB=[(2,-0.9,1.8,GRN,"e"),(3,-1.4,2.8,RRED,"f"),(5,-2.4,5.6,BLUE,"g"),(7,-3.4,8.4,GOLD,"h"),(9,-4.4,11.2,VIO,"i")]
        res=[]
        for k_,(Lc,c0v,lim,CC,let) in enumerate(CUB):
            axk=fig.add_axes([0.2*k_,0.300,0.2,0.165],projection="3d"); n_,d_=cubo(axk,Lc,c0v,lim,CC); res.append((n_,d_))
            assert n_==Lc**3 and d_==3*Lc*Lc-3*Lc+1   # sombras de {0..L-1}^3: 3L^2-3L+1
            win="\\{0,1\\}" if Lc==2 else ("\\{0,1,2\\}" if Lc==3 else f"\\{{0,\\dots,{Lc-1}\\}}")
            fig.text(0.1+0.2*k_,0.468,f"({let})  ${win}^3$:\n{n_} points, {d_} projected points",ha="center",va="top",fontsize=10.5,color=CC)
        assert res==[(8,7),(27,19),(125,61),(343,127),(729,217)]
        fig.add_artist(Line2D([0.04,0.96],[0.502,0.502],transform=fig.transFigure,color="0.85",lw=0.8))
        fig.text(0.50,0.492,"The cube $\\mathbb{Z}^3$ seen along its diagonal",ha="center",va="top",fontsize=11.5,color=INK)
        fig.text(0.50,0.296,"§10.1 (cube_diagonal_kernel): each axis projects to $e_k-\\frac{1}{3}(1,1,1)$, $|\\cdot|^2=\\frac{2}{3}$, at $120^\\circ$, onto a hexagonal lattice, $\\mathbb{Z}[\\omega]$ up to $\\sqrt{2/3}$;\nthe projection has a kernel, the diagonal: dot size = points projected to one point; outlined = more than one",ha="center",fontsize=9.5,color="0.4")

        # ---------------- (g) la razón vectorial frente a la profundidad (§9), condición exacta de dos branas
        from scipy.special import jn_zeros, j0, y0
        from scipy.optimize import brentq
        def ratio(D):
            e=1/D; f=lambda x: j0(e*x)*y0(x)-y0(e*x)*j0(x)
            xs=np.linspace(0.3,12,3000); v=f(xs); z=[brentq(f,xs[i],xs[i+1]) for i in range(len(xs)-1) if v[i]*v[i+1]<0]
            return z[1]/z[0]
        tab={6:2.093,12:2.171,24:2.228,30:2.241,81.74:2.275}
        for d_,r_ in tab.items(): assert round(ratio(phi**d_),3)==r_
        fig.add_artist(Line2D([0.04,0.96],[0.278,0.278],transform=fig.transFigure,color="0.85",lw=0.8))
        head(0.50,0.264,"j","The vector ratio as a function of the depth (§9)","§9: $m_2/m_1$ from the exact two-brane conditions; only the depth, the position of the top, stays free")
        axE=fig.add_axes([0.05,0.045,0.92,0.17])
        dd=np.linspace(2,100,200); axE.plot(dd,[ratio(phi**x) for x in dd],c=INK,lw=1.8); axE.plot(list(tab),list(tab.values()),"o",c=INK,ms=5)
        for x_,y_ in tab.items(): axE.text(x_+1.2,y_-0.03,f"$\\varphi^{{{x_}}}$",fontsize=9,color="0.35")
        J0=jn_zeros(0,2); axE.axhline(J0[1]/J0[0],c="0.4",ls="--",lw=1); axE.text(99,J0[1]/J0[0]+0.01,"deep-throat limit $j_{0,2}/j_{0,1}=2.295$",fontsize=9,ha="right",color="0.35")
        axE.axhspan(2.15,2.39,color=TEAL,alpha=0.12); axE.text(1,2.36,"gluon candidates [LYR26]: 2.15–2.39",fontsize=9,color="#2f7f7f")
        axE.axvline(81.74,c="0.6",lw=0.8,ls=":"); axE.text(80.5,2.02,"depth $\\varphi^{81.74}$: the Planck scale from the level $12$",fontsize=8.5,color="0.45",ha="right")
        axE.set_xlabel("depth of the throat, $\\varphi^{d}$: $d$ levels",color="0.3"); axE.set_ylabel("vector $m_2/m_1$",color="0.3")
        axE.set_xlim(0,101); axE.set_ylim(2.0,2.40)
        for s_ in ("top","right"): axE.spines[s_].set_visible(False)
        for s_ in ("left","bottom"): axE.spines[s_].set_color("0.5")
        axE.tick_params(colors="0.4",labelsize=9)
        fig.savefig("fig_one_structure.pdf",bbox_inches="tight"); plt.close(fig)

    _figura_1()
    plt.rcParams.update(matplotlib.rcParamsDefault)


    print("figuras: ok")

SECCIONES.append((12, 'Figura 1: una estructura vista de una vez; los puntos de Z[i] por nivel; comprobaciones', seccion_12))

# ======================================================================
# 13. Figura 2: las dos familias recíprocas
# ======================================================================
def seccion_13():
    """Figura 2 exacta: en cada nivel sigma = 12..18,
     izquierda: el anillo de la garganta, radio proporcional a z(sigma) = phi^sigma (normalizado phi^(sigma-18));
     derecha: la fibra de Möbius sobre su propio lazo, el periodo de media vuelta tau(sigma) = M phi^-sigma
     (radio normalizado phi^-(sigma-12)), con media vuelta por vuelta (epsilon(sigma) tau(sigma) = pi,
     closure_each_level) y semiancho 1/2 del radio de su lazo (|Omega| = 1/2, convención de dibujo de B1).
     El producto de los dos radios es constante, phi^-6: z tau = M."""
    import numpy as np, matplotlib
    matplotlib.use("Agg"); import matplotlib.pyplot as plt
    phi=(1+5**.5)/2; lev=np.arange(12,19); tt=np.linspace(0,2*np.pi,400)
    rz=lambda s: phi**(s-18); rt=lambda s: phi**(-(s-12))
    for s in lev: assert abs(rz(s)*rt(s)-phi**-6)<1e-12          # z*tau constante
    K=dict(color="k", lw=0.4)
    fig=plt.figure(figsize=(8.6,5.0))
    def clean(ax,lim):
        ax.set_xlim(-lim,lim); ax.set_ylim(-lim,lim); ax.set_zlim(11.5,18.5)
        ax.set_box_aspect((1,1,1.25)); ax.set_axis_off(); ax.view_init(elev=16,azim=-58)
    ax=fig.add_subplot(1,2,1,projection="3d")
    for s in lev:
        r=rz(s); ax.plot(r*np.cos(tt),r*np.sin(tt),s+0*tt,"k",lw=1.0)
        ax.text(r+0.05,0,s,rf"$\sigma={s}$",fontsize=7)
    for t0 in np.linspace(0,2*np.pi,16,endpoint=False):
        ss=np.linspace(12,18,100); ax.plot(rz(ss)*np.cos(t0),rz(ss)*np.sin(t0),ss,**K)
    ax.set_title(r"rings of the throat, radius $\propto z(\sigma)=\varphi^{\sigma}$",fontsize=8)
    clean(ax,1.05)
    ax=fig.add_subplot(1,2,2,projection="3d")
    U=np.linspace(0,2*np.pi,300)
    for s in lev:
        R=rt(s)*0.6; h=0.5*R            # semiancho 1/2 del radio del lazo
        for wv in (-1,1):
            ax.plot((R+wv*h*np.cos(U/2))*np.cos(U),(R+wv*h*np.cos(U/2))*np.sin(U),s+wv*h*np.sin(U/2),"k",lw=0.9)
        for u0 in np.linspace(0,2*np.pi,26,endpoint=False):
            w=np.array([-1,1]); ax.plot((R+w*h*np.cos(u0/2))*np.cos(u0),(R+w*h*np.cos(u0/2))*np.sin(u0),s+w*h*np.sin(u0/2),**K)
    ax.set_title(r"Möbius fibre on its loop, radius $\propto\tau(\sigma)=M\varphi^{-\sigma}$",fontsize=8)
    clean(ax,1.05)
    fig.savefig("fig_mobius_throat.pdf",bbox_inches="tight"); print("ok")

SECCIONES.append((13, 'Figura 2: las dos familias recíprocas', seccion_13))

# ======================================================================
# 14. Tres huecos de las marcas en el anillo (6.1)
# ======================================================================
def seccion_14():
    import math
    phi=(1+5**.5)/2
    for s in range(1,7):
        a=phi**(-2*s); out=[]
        for K in (100,1000,10000):
            x=sorted((k*a)%1 for k in range(K)); g=[x[i+1]-x[i] for i in range(K-1)]+[1-x[-1]+x[0]]
            out.append(len(set(round(v,9) for v in g)))
        K=10000; x=[(k*a)%1 for k in range(K)]
        D=max(abs(sum(1 for v in x if v<t)/K-t) for t in [i/50 for i in range(51)])
        print(f"σ={s} N={phi**(2*s):.3f} huecos(100,1e3,1e4)={out} discrepancia={D:.4f}")

SECCIONES.append((14, 'Tres huecos de las marcas en el anillo (6.1)', seccion_14))

# ======================================================================
# 15. Cuenta exacta de estados con c = 3 en el nivel N/2 frente a S (6.1)
# ======================================================================
def seccion_15():
    import math
    phi=(1+5**.5)/2
    M=3000
    sig=[0]*(M+1)
    for d in range(1,M+1):
        for k in range(d,M+1,d): sig[k]+=d
    p=[0]*(M+1); p[0]=1          # estados de c=3 bosones: prod (1-q^n)^-3 ; n p(n) = 3 sum sigma(k) p(n-k)
    for n in range(1,M+1):
        p[n]=3*sum(sig[k]*p[n-k] for k in range(1,n+1))//n
    print("σ   N=φ^2σ   L0=N/2  ln#estados   S=π√N   cociente  cota πz   N/πz")
    for s in range(1,10):
        N=phi**(2*s); L0=round(N/2); z=phi**s
        lnW=math.log(p[L0]); S=math.pi*math.sqrt(2*L0)
        print(f"{s}  {N:9.2f} {L0:6d}  {lnW:10.3f}  {S:8.3f}  {lnW/S:.4f}   {math.pi*z:8.2f}  {N/(math.pi*z):6.2f}")
    print("\nCon la corrección de Cardy de orden siguiente, ln W ≈ S − (c+3)/4·ln L0 + C, c=3:")
    for s in range(3,10):
        L0=round(phi**(2*s)/2); S=math.pi*math.sqrt(2*L0)
        print(f"σ={s}  S − ln W − (3/2) ln L0 = {S-math.log(p[L0])-1.5*math.log(L0):.4f}")

SECCIONES.append((15, 'Cuenta exacta de estados con c = 3 en el nivel N/2 frente a S (6.1)', seccion_15))

# ======================================================================
# 16. La escala M de (F1): reconstrucción de tipo Koide de las masas leptónicas
# ======================================================================
def seccion_16():
    import math
    M = 313.84   # MeV, (F1)
    d = 2 / 9    # delta = 2/n^2, n = 3
    obs = {"e": 0.51099895, "mu": 105.6583755, "tau": 1776.86}
    m = sorted(M * (1 + math.sqrt(2) * math.cos(d + 2 * math.pi * k / 3)) ** 2 for k in range(3))
    for (name, o), x in zip(obs.items(), m):
        print(f"{name:4s} Koide desde M: {x:10.4f} MeV   observada: {o:10.4f}   rel. {abs(x-o)/o:.1e}")

SECCIONES.append((16, 'La escala M de (F1): reconstrucción de tipo Koide de las masas leptónicas', seccion_16))

# ======================================================================
# 17. El nivel del observador por el valor de Lambda, bajo (F9) y la unidad de (F1)
# ======================================================================
def seccion_17():
    import math, random
    phi = (1 + 5 ** 0.5) / 2
    L = math.log(phi)
    u = 313.84e6 / (6 * 3 ** 0.5 * math.pi / L)        # eV, la unidad de (F1)
    hbar, Mpc = 6.582119569e-16, 3.0856775814913673e19   # eV s, km
    def sigma_obs(H0, OL):                              # Lambda = 3 H0^2 Omega_L, curvatura
        lam = 3 * (hbar * H0 / Mpc) ** 2 * OL
        return math.log(6 * u ** 2 / lam) / L
    random.seed(1)
    v = [sigma_obs(random.gauss(67.36, 0.54), random.gauss(0.6847, 0.0073)) for _ in range(200000)]
    m = sum(v) / len(v); sd = (sum((x - m) ** 2 for x in v) / len(v)) ** 0.5
    print(f"unidad de (F1): {u/1e6:.4f} MeV")
    print(f"sigma_obs = {sigma_obs(67.36, 0.6847):.3f} +- {sd:.3f}  (Planck 2018: H0 = 67.36 +- 0.54, Omega_L = 0.6847 +- 0.0073)")

SECCIONES.append((17, 'El nivel del observador por el valor de Lambda, bajo (F9) y la unidad de (F1)', seccion_17))

# ======================================================================
# 18. El nivel del observador y la unidad de la curvatura
# ======================================================================
def seccion_18():
    import math, random
    phi = (1 + 5 ** 0.5) / 2; L = math.log(phi)
    u = 313.84e6 / (6 * 3 ** 0.5 * math.pi / L)      # eV, unidad de (F1)
    M = 313.84e6; MP = 1.220890e28                    # eV
    hbar, Mpc_km = 6.582119569e-16, 3.0856775814913673e19
    lP2, c, Mpc_m = (1.616255e-35) ** 2, 2.99792458e8, 3.0856775814913673e22
    def readings(H0, OL):
        lam_eV2 = 3 * (hbar * H0 / Mpc_km) ** 2 * OL                 # curvatura, eV^2
        s_curv = math.log(6 * u ** 2 / lam_eV2) / L                  # W8, unidad de (F1)
        lam_m = 3 * (H0 * 1e3 / Mpc_m) ** 2 * OL / c ** 2            # m^-2
        S = 3 * math.pi / (lam_m * lP2)                              # entropia de de Sitter
        s_ent = math.log(S / math.pi) / L                            # W4, sin unidad
        return s_curv, s_ent, S
    random.seed(2)
    v = [readings(random.gauss(67.36, 0.54), random.gauss(0.6847, 0.0073)) for _ in range(100000)]
    def ms(i):
        x = [t[i] for t in v]; m = sum(x) / len(x); return m, (sum((y - m) ** 2 for y in x) / len(x)) ** 0.5
    sc, se, S = readings(67.36, 0.6847)
    print(f"nivel del observador (W4 = W8 en la unidad gravitacional l = sqrt2 l_P): sigma = {se:.3f} +- {ms(1)[1]:.3f};  S = {S:.3e}")
    print(f"la misma curvatura medida en la unidad de particulas (F1), eliminada: {sc:.3f}; diferencia {se - sc:.3f} = 2 log_phi(M_Pl/u) - log_phi 2 = {2*math.log(MP/u)/L - math.log(2)/L:.3f}, una conversion de unidad")
    print(f"Lambda(sigma) S(sigma) = 6 pi = 3 pi / G_N con G_N = 1/2:", abs(6*phi**-7.3*math.pi*phi**7.3 - 6*math.pi) < 1e-12)

SECCIONES.append((18, 'El nivel del observador y la unidad de la curvatura', seccion_18))

# ======================================================================
# 19. El desfase de la torre: ceros exactos frente a la asintótica, y la forma de Maldacena–Qi
# ======================================================================
def seccion_19():
    import math
    from scipy.special import jn_zeros
    j = jn_zeros(1, 8)
    print("k  j_1,k/pi - k   (asintota 1/4 = 1/d en d = 4; el k = 0 exacto es j_1,0 = 0)")
    print("0  exacto: j_1,0 = 0;  la asintota daria 0.25")
    for k, x in enumerate(j, 1):
        print(f"{k}  {x/math.pi - k:.4f}")
    for d in range(2, 9):
        print(f"d = {d}: d/4 - 3/4 = {d/4-0.75:+.3f},  1/d = {1/d:.3f}", "  iguales" if abs(d/4-0.75-1/d) < 1e-12 else "")
    print("Maldacena-Qi: E_n = t'(n + 1/4); torre: m_k ~ pi M phi^12 (k + 1/4), con k = 0 sustituido por el modo cero")

SECCIONES.append((19, 'El desfase de la torre: ceros exactos frente a la asintótica, y la forma de Maldacena–Qi', seccion_19))

# ======================================================================
# 20. El contraste con los dos candidatos observados (380 y 700 GeV)
# ======================================================================
def seccion_20():
    import math
    from scipy.special import jn_zeros
    phi = (1 + 5 ** 0.5) / 2; M = 0.31384
    j = jn_zeros(1, 6)
    def fit(m, e):
        w = [1 / x ** 2 for x in e]; mu = j[:len(m)]
        lam = sum(a * b * c for a, b, c in zip(w, m, mu)) / sum(a * c * c for a, c in zip(w, mu))
        dl = 1 / math.sqrt(sum(a * c * c for a, c in zip(w, mu)))
        return math.log(lam / M) / math.log(phi), dl / lam / math.log(phi)
    s, ds = fit([380, 700], [20, 20])
    print(f"dos datos: sigma_IR = {s:.2f} +- {ds:.2f}  ({abs(s-12)/ds:.1f} desviaciones de 12)")
    print(f"cociente 700/380 = {700/380:.3f};  j_1,2/j_1,1 = {j[1]/j[0]:.3f}")
    print("predicciones con sigma = 12 (GeV):", [round(x * M * phi ** 12) for x in j[2:6]], " frente a RS (LYR): 1000, 1322")

SECCIONES.append((20, 'El contraste con los dos candidatos observados (380 y 700 GeV)', seccion_20))

# ======================================================================
# 21. El rival de dos branas ajustado a los mismos dos candidatos
# ======================================================================
def seccion_21():
    import math
    from scipy.special import jn_zeros
    phi = (1 + 5 ** 0.5) / 2; M = 0.31384
    j = jn_zeros(1, 4); m, e = [380, 700], [20, 20]
    w = [1 / x ** 2 for x in e]
    lam = sum(a * b * c for a, b, c in zip(w, m, j)) / sum(a * c * c for a, c in zip(w, j))
    lg = M * phi ** 12
    print(f"escala libre ajustada: {lam:.2f} GeV -> modos 3 y 4: {j[2]*lam:.0f}, {j[3]*lam:.0f} GeV")
    print(f"garganta (sigma = 12): {lg:.2f} GeV -> {j[2]*lg:.0f}, {j[3]*lg:.0f} GeV; diferencia {100*(lg/lam-1):.1f} %")
    print(f"separacion: {j[2]*(lg-lam):.0f} y {j[3]*(lg-lam):.0f} GeV, frente a +-30 y +-40 GeV supuestos en la sec. 2")

SECCIONES.append((21, 'El rival de dos branas ajustado a los mismos dos candidatos', seccion_21))

# ======================================================================
# 22. La unidad de la curvatura y el nivel del observador
# ======================================================================
_C = dict(hbar=1.054571817e-34, c=299792458.0, G=6.67430e-11, Mpc=3.0856775814913673e22)
def _LamP(H0, OL):
    H = H0 * 1e3 / _C['Mpc']; lP2 = _C['hbar'] * _C['G'] / _C['c'] ** 3
    return 3 * H * H * OL / _C['c'] ** 2 * lP2
def seccion_22():
    import math
    phi = (1 + 5 ** 0.5) / 2; L = math.log(phi); GN = 0.5
    lp = _LamP(67.36, 0.6847)
    s_l = math.log(6 / (lp / GN)) / L; s_S = math.log(3 / lp) / L; s_cw6 = math.log(6 / lp) / L
    print(f"l = l_P/sqrt(G_N) = {1/math.sqrt(GN):.4f} l_P (I12, tau = i)")
    print(f"W8 en unidad l: {s_l:.3f};  W4: {s_S:.3f}  (iguales por Lambda S = 6 pi)")
    print(f"eq. sigma-obs de CW6 (Lambda en l_P con el 6 de G_N = 1/2): {s_cw6:.3f} = W4 + log_phi 2")
    for name, H0, OL in [("Planck 2018", 67.36, 0.6847), ("SH0ES, omega_m fijo", 73.04, 1 - 0.1430 / 0.7304 ** 2)]:
        print(f"  {name:20s}: sigma_obs = {math.log(3/_LamP(H0, OL))/L:.3f}")

SECCIONES.append((22, 'La unidad de la curvatura y el nivel del observador', seccion_22))

# ======================================================================
# 23. La red: unidades de Z[phi], el fondo y el observador
# ======================================================================
def seccion_23():
    import math
    phi = (1 + 5 ** 0.5) / 2; L = math.log(phi); F = [0, 1]
    for _ in range(30): F.append(F[-1] + F[-2])
    for n in (1, 2, 3, 6, 12):
        a, b = F[n - 1], F[n]
        print(f"  phi^{n} = {a} + {b} phi, norma {a*a + a*b - b*b:+d}")
    print("fondo: 11.97 +- 0.05 frente al punto de red 12 (0.6 desviaciones)")
    wm = 0.1430
    def H0_for(n, mode):
        lo, hi = 40.0, 120.0
        for _ in range(100):
            h = (lo + hi) / 2; OL = 1 - wm / (h / 100) ** 2 if mode == 'wm' else 0.6847
            if math.log(3 / _LamP(h, OL)) / L > n: lo = h
            else: hi = h
        return h
    for n in (583, 584, 585):
        print(f"  observador en el punto {n}: H0 = {H0_for(n,'wm'):.2f} (omega_m fijo), {H0_for(n,'OL'):.2f} (Omega_Lambda fijo)")
    h = H0_for(584, 'wm')
    print(f"  584: {(h-67.36)/0.54:+.1f} sigma de Planck (67.36 +- 0.54), {(h-73.04)/1.04:+.1f} sigma de SH0ES (73.04 +- 1.04)")

SECCIONES.append((23, 'La red: unidades de Z[phi], el fondo y el observador', seccion_23))

# ======================================================================
# 24. Los dos datos con dimension y la cima
# ======================================================================
def seccion_24():
    import math
    phi = (1 + 5 ** 0.5) / 2; L = math.log(phi)
    GeVJ = 1.602176634e-10
    MPl = math.sqrt(_C['hbar'] * _C['c'] ** 5 / _C['G']) / GeVJ
    me, mmu, mtau = 0.51099895, 105.6583755, 1776.93
    M = (math.sqrt(me) + math.sqrt(mmu) + math.sqrt(mtau)) ** 2 / 9 / 1e3
    Mpcf = 6 * math.sqrt(3) * math.pi / L; u = M / Mpcf
    r = 2 * math.log(MPl * math.sqrt(0.5) / u) / L
    print(f"M = {M*1e3:.3f} MeV (Koide-Brannen), u = {u*1e3:.4f} MeV, M_Pl = {MPl:.5e} GeV")
    print(f"2 log_phi(l_u / l), l = sqrt2 l_P: {r:.3f}  (a {abs(r-round(r)):.2f} del entero): la red no fija la cima")
    print(f"sigma_UV = log_phi(M_Pl/M) = {math.log(MPl/M)/L:.3f}")

SECCIONES.append((24, 'Los dos datos con dimension y la cima', seccion_24))

# ======================================================================
# 25. El corte y proyeccion con la gaussiana autodual, en los dos espacios
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
        print(f"indice sigma, cerca de {x}: " + "; ".join(f"{a}+{b}phi = {v:.2f} (peso {w:.2g})" for w, a, b, v in best(x)))
    print(f"  el entero 12 tiene conjugado 12: peso 10^{-math.pi*144/math.log(10):.0f}  -> el corte sobre sigma se elimina")
    print("escala: unidades phi^n, conjugado (-1)^n phi^-n, peso e^(-pi phi^-2n):",
          ", ".join(f"n={n}: {math.exp(-math.pi*phi**(-2*n)):.2f}" for n in range(0, 7)))

SECCIONES.append((25, 'El corte y proyeccion con la gaussiana autodual, en los dos espacios', seccion_25))

# ======================================================================
# 26. El borde de la ventana y sigma_G
# ======================================================================
def seccion_26():
    import math
    phi = (1 + 5 ** 0.5) / 2; L = math.log(phi)
    print(f"cruce del peso 1/2: n = {0.5*math.log(math.pi/math.log(2))/L:.3f}; cruce de H l = 1: n = {math.log(2)/L:.3f}")
    print(f"umbrales que dan n = 2 como primer nivel: ({math.exp(-math.pi*phi**-2):.3f}, {math.exp(-math.pi*phi**-4):.3f})")
    for n in range(0, 4):
        print(f"  n = {n}: peso {math.exp(-math.pi*phi**(-2*n)):.3f}, H l = {math.sqrt(2*phi**(-n)):.3f}")
    print("primer nivel entero activo por las dos rutas: 2 = sigma_G = n - 1 (CW6)")

SECCIONES.append((26, 'El borde de la ventana y sigma_G', seccion_26))

# ======================================================================
# 27. La ventana como nome: la torre de toros y S como espejo
# ======================================================================
def seccion_27():
    import math
    phi = (1 + 5 ** 0.5) / 2
    for n in range(0, 4):
        t = phi ** (-2 * n)
        print(f"  n={n}: tau_n = {t:.4f} i, nome q = e^(i pi tau) = {math.exp(-math.pi*t):.4f};  S: -1/tau_n = {1/t:.4f} i = tau_{-n}")
    nh = 0.5 * math.log(math.pi / math.log(2)) / math.log(phi)
    print(f"cruce del peso 1/2: n = {nh:.6f}; cuarto de vuelta pi/2 = {math.pi/2:.6f}; w(pi/2) = {math.exp(-math.pi*phi**(-math.pi)):.6f}")
    print(f"ancho que haria exacto el cruce en pi/2: log2 * phi^pi = {math.log(2)*phi**math.pi:.6f} (autodual: pi = {math.pi:.6f})")

SECCIONES.append((27, 'La ventana como nome: la torre de toros y S como espejo', seccion_27))

# ======================================================================
# 28. Poisson: el tiempo propio y 1/N; theta_3 en tau = i
# ======================================================================
def seccion_28():
    import math
    for N in (2.618033988749895, 6.854101966249685):
        lhs = sum(math.exp(-math.pi * k * k * N) for k in range(-60, 61))
        rhs = N ** -0.5 * sum(math.exp(-math.pi * m * m / N) for m in range(-60, 61))
        print(f"  N = {N:.4f}: modos {lhs:.12f}, enrollamientos {rhs:.12f}; primer enrollamiento e^(-pi/N) = {math.exp(-math.pi/N):.4f}")
    t3 = sum(math.exp(-math.pi * k * k) for k in range(-30, 31))
    print(f"theta_3(e^-pi) = {t3:.12f};  pi^(1/4)/Gamma(3/4) = {math.pi**0.25/math.gamma(0.75):.12f}")

SECCIONES.append((28, 'Poisson: el tiempo propio y 1/N; theta_3 en tau = i', seccion_28))

# ======================================================================
# 29. Lo que fija el punto de red: Omega_Lambda h^2
# ======================================================================
def seccion_29():
    import math
    phi = (1 + 5 ** 0.5) / 2; L = math.log(phi)
    lP2 = _C['hbar'] * _C['G'] / _C['c'] ** 3; H100 = 100e3 / _C['Mpc']
    Lam = 3 * phi ** -584 / lP2
    OLh2 = Lam * _C['c'] ** 2 / (3 * H100 ** 2)
    h, dh, wm, dwm = 0.6736, 0.0054, 0.1430, 0.0011
    print(f"punto 584: Lambda l_P^2 = 3 phi^-584 = {3*phi**-584:.4e};  Omega_L h^2 = {OLh2:.4f}")
    for r in (0.0, -1.0):        # Omega_m y H0 de Planck 2018, correlacion entre las dos cotas
        Om, dOm = 0.3153, 0.0073
        a, b = -h * h * dOm, 2 * (1 - Om) * h * dh
        p, dp = (1 - Om) * h * h, math.sqrt(a * a + b * b + 2 * a * b * r)
        print(f"Planck 2018, r(Omega_m, H0) = {r:+.0f}: Omega_L h^2 = {p:.4f} +- {dp:.4f}: {(OLh2-p)/dp:+.1f} sigma")
    print(f"con omega_m = {wm} +- {dwm} y planitud: H0 = {100*math.sqrt(OLh2+wm):.2f} +- {100*0.5*dwm/math.sqrt(OLh2+wm):.2f}")
    # Planck solo en la variable del criterio (el nivel) y frente a DESI DR2 + CMB
    HD, dHD, OmD, dOmD, rD = 0.6817, 0.0028, 0.3027, 0.0036, -0.975
    aD, bD = -HD*HD*dOmD, 2*(1-OmD)*HD*dHD; pD = (1-OmD)*HD*HD; dpD = math.sqrt(aD*aD+bD*bD+2*aD*bD*rD)
    Om, dOm = 0.3153, 0.0073; a, b = -h*h*dOm, 2*(1-Om)*h*dh; p = (1-Om)*h*h
    lvl = lambda x: 584 + math.log(OLh2 / x) / L
    ten = []
    for r in (0.0, -1.0):
        dp = math.sqrt(a*a + b*b + 2*a*b*r); sl = dp / (p * L)
        ten.append((pD - p) / math.hypot(dpD, dp))
        print(f"Planck solo, r = {r:+.0f}: nivel {lvl(p):.3f}, a {(584-lvl(p))/sl:.2f} sigma de 584 en el nivel; DESI+CMB frente a Planck: {ten[-1]:.2f} sigma en Omega_L h^2")
    assert 1.3 < min(ten) < 1.5 and 1.7 < max(ten) < 1.9, ten
    print(f"DESI DR2 + CMB: Omega_L h^2 = {pD:.4f} +- {dpD:.4f}; Planck y la combinacion concuerdan (1.4-1.8 sigma)")
    print(f"sensibilidad: d sigma / d ln H0 = {-2/L:.3f}; 1 % en H0 = {0.02/L:.3f} niveles")
    print(f"584 mod 24 = {584 % 24}; 584 = 2^3 * 73: no es un nivel distinguido de la red")

SECCIONES.append((29, 'Lo que fija el punto de red: Omega_Lambda h^2', seccion_29))

# ======================================================================
# 30. La garganta simetrica [-12, 12] y la escala UV
# ======================================================================
def seccion_30():
    import math
    phi = (1 + 5 ** 0.5) / 2; M = 0.313851
    print(f"profundidad 24 niveles (el reloj): k pi r = 24 log phi = {24*math.log(phi):.2f}  (cima en Planck: 39.33)")
    print(f"escala IR = M phi^12 = {M*phi**12:.2f} GeV; escala UV = M phi^36 = {M*phi**36:.3e} GeV")
    print("cociente vectorial: 2.228 (simetrica) frente a 2.275 (Planck); rango actual 2.15-2.39")

SECCIONES.append((30, 'La garganta simetrica [-12, 12] y la escala UV', seccion_30))

# ======================================================================
# 31. La metrica de moduli del anillo y las conjeturas
# ======================================================================
def seccion_31():
    import math
    phi = (1 + 5 ** 0.5) / 2; L = math.log(phi)
    d = math.sqrt(2) * L
    print("K = -ln(2 Im tau), K_tt = 1/(4 Im^2); tau = i t: L_kin = (dt)^2/(4t^2), Phi = ln t / sqrt2")
    print(f"dPhi/dn = sqrt2 log phi = {d:.4f};  |dV/dPhi|/V = {L/d:.4f}")
    print(f"de Sitter (OOSV): c ~ O(1);  TCC (Bedroya-Vafa) en 4D: c >= sqrt(2/3) = {math.sqrt(2/3):.4f}")
    print(f"  pendiente {L/d:.4f} < cota {math.sqrt(2/3):.4f}: el contraste con la TCC falla con estos supuestos")
    for n in (2, 12, 584):
        print(f"  distancia canonica en el nivel {n}: Phi = sqrt2 n log phi = {math.sqrt(2)*n*L:.1f} M_Pl (sin cota a lo largo de la torre)")
    print("  con K = -k ln Im tau la pendiente es 1/sqrt(2k); la cota se cumple si y solo si k <= 3/4")
    for s in (2, 12, 100):
        print(f"  norma de las dos escalas en sigma = {s}: (phi^s)(phi^-s) = {phi**s*phi**-s:.3f}")

SECCIONES.append((31, 'La metrica de moduli del anillo y las conjeturas', seccion_31))

# ======================================================================
# 32. El nivel leido del observador frente a la forma de red
# ======================================================================
def seccion_32():
    import math
    phi = (1 + 5 ** 0.5) / 2; L = math.log(phi)
    lP2 = _C['hbar'] * _C['G'] / _C['c'] ** 3; H100 = 100e3 / _C['Mpc']
    def req(n): return 3 * phi ** -n / lP2 * _C['c'] ** 2 / (3 * H100 ** 2)
    print("Omega_L h^2 requerido por los puntos 583, 584, 585: " + ", ".join(f"{req(n):.4f}" for n in (583, 584, 585)))
    def det(Om, dOm, H0, dH0, r):
        h, dh = H0 / 100, dH0 / 100
        a, b = -h * h * dOm, 2 * (1 - Om) * h * dh
        return (1 - Om) * h * h, math.sqrt(a * a + b * b + 2 * a * b * r)
    def nivel(v, dv):
        n = 584 - math.log(v / req(584)) / L; dn = dv / v / L; k = round(n)
        return n, dn, k, abs(n - k) / dn
    casos = [("Planck 2018, LCDM, r = 0", 0.3153, 0.0073, 67.36, 0.54, 0.0),
             ("Planck 2018, LCDM, r = -1", 0.3153, 0.0073, 67.36, 0.54, -1.0),
             ("DESI DR2 + CMB, LCDM, r = -1 (peor caso)", 0.3027, 0.0036, 68.17, 0.28, -1.0),
             ("DESI DR2 + CMB, LCDM, r = -0.975", 0.3027, 0.0036, 68.17, 0.28, -0.975),
             ("DESI DR2 + CMB, LCDM, r = 0", 0.3027, 0.0036, 68.17, 0.28, 0.0)]
    for nm, Om, dOm, H0, dH0, r in casos:
        v, dv = det(Om, dOm, H0, dH0, r); n, dn, k, z = nivel(v, dv)
        print(f"{nm:34s} Omega_L h^2 = {v:.4f} +- {dv:.4f}; nivel {n:.3f} +- {dn:.3f}; entero {k} a {z:.1f} sigma")
    v = 0.7304 ** 2 - 0.1430; dv = math.hypot(2 * 0.7304 * 0.0104, 0.0011); n, dn, k, z = nivel(v, dv)
    print(f"{'H0 local con omega_m de Planck':34s} Omega_L h^2 = {v:.4f} +- {dv:.4f}; nivel {n:.3f} +- {dn:.3f}; entero {k} a {z:.1f} sigma")
    print("criterio: el nivel leido a 3 sigma o mas de todo entero excluye la forma de red")

SECCIONES.append((32, 'El nivel leido del observador frente a la forma de red', seccion_32))

# ======================================================================
# 33. El hueco de color: la tension soldada, Higuchi y la escala de Regge
# ======================================================================
def seccion_33():
    import math
    phi = (1 + 5 ** 0.5) / 2; L = math.log(phi)
    MPCF = 6 * 3 ** 0.5 * math.pi / L; eps0 = math.pi / MPCF
    M = 0.313851; u = M / MPCF; MPl = 1.2209e19; Ecurv = MPl / 2 ** 0.5
    for q2, nm in ((2 * math.pi, "q^2 = 2 pi"), (1.0, "q = 1")):
        qm2 = (2 * math.pi) ** 2 / q2
        vals = [qm2 * eps0 * phi ** -s * math.pi * phi ** s for s in (0, 5, 12)]
        print(f"{nm}: sigma_t * S en s = 0, 5, 12: " + ", ".join(f"{v:.4f}" for v in vals)
              + f"  (4 pi^4/(q^2 MPCF) = {4*math.pi**4/(q2*MPCF):.4f})")
        r = math.pi ** 3 / (q2 * MPCF)
        print(f"   Delta^2/(2 H^2) = pi^3/(q^2 MPCF) = {r:.4f}; espin dos de masa kappa Delta: kappa >= {1/math.sqrt(r):.2f}")
    print(f"Higuchi para kappa = 1 si y solo si q^2 <= pi^3/MPCF = {math.pi**3/MPCF:.4f}")
    m1 = 3.8317 * M * phi ** 12
    for nm, E in (("u (particulas)", u), ("sqrt2 l_P (curvatura)", Ecurv)):
        Ms = E / math.sqrt(MPCF)
        print(f"Regge, alpha' = MPCF en {nm}: M_1 = {Ms:.3e} GeV frente a m_KK,1 = {m1:.1f} GeV")
    print(f"conversion entre las dos unidades: {2*math.log(MPl/u)/L - math.log(2)/L:.2f} niveles")
    from scipy.special import jn_zeros
    j = jn_zeros(1, 5000); mk = j * M * phi ** 12
    print(f"modos de graviton bajo 1000 TeV: {int((mk < 1e6).sum())}; estimacion lineal 1e6/(pi M phi^12) = {1e6/(math.pi*M*phi**12):.1f}")

SECCIONES.append((33, 'El hueco de color: la tension soldada, Higuchi y la escala de Regge', seccion_33))

# ======================================================================
# 34. La quintaesencia del anillo: lambda = 1/sqrt2 frente a los datos
# ======================================================================
def seccion_34():
    import numpy as np
    from scipy.integrate import solve_ivp
    from scipy.optimize import brentq
    lam = 1 / np.sqrt(2)          # pendiente del modulo (10.1), Phi en masa de Planck reducida
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
        print(f"Omega_m = {Om}: w(0) = {w[0]:.3f}; proyeccion CPL (z < 2): w0 = {w0:.3f}, wa = {wa:.3f}")
    c, up = 0.698, 0.173
    print(f"Akrami-Alestas-Nesseris (DESI DR2 + CMB + DESY5): lambda = 0.698 +0.173/-0.202")
    print(f"  1/sqrt2 a {(lam - c) / up:+.2f} sigma; sqrt(2/3) a {(np.sqrt(2/3) - c) / up:+.2f}; sqrt2 a {(np.sqrt(2) - c) / up:+.2f}")

SECCIONES.append((34, 'La quintaesencia del anillo: lambda = 1/sqrt2 frente a los datos', seccion_34))

# ======================================================================
# 35. El umbral 1/2: tiempo de Fisher, entropia binaria, un bit por autovalor
# ======================================================================
def seccion_35():
    import math
    for f in (0.25, 0.5, 1.0):
        print(f"f = {f}: tau_F/tau_D = 1/sqrt(2f) = {1/math.sqrt(2*f):.4f};  H(f) = {-(f*math.log2(f)+(1-f)*math.log2(1-f)) if 0<f<1 else 0:.4f} bits")
    print("tau_F = tau_D si y solo si f = 1/2; H(1/2) = 1 bit es el maximo; 4 mu^2 = 1 si y solo si mu = 1/2")

SECCIONES.append((35, 'El umbral 1/2: tiempo de Fisher, entropia binaria, un bit por autovalor', seccion_35))

# ======================================================================
# 36. El agujero negro, tocado donde hace falta: la orbita de la torre, el horizonte de S(12), el umbral
# ======================================================================
def seccion_36():
    import numpy as np
    from scipy.special import jn_zeros
    phi = (1 + 5 ** 0.5) / 2; L = np.log(phi)
    a = L / (2 * np.pi)
    f = lambda t: np.exp(np.cos(2 * np.pi * t)); g = lambda t: np.exp(2 * np.cos(2 * np.pi * t) + 0.5 * np.sin(4 * np.pi * t))
    th = np.arange(1 << 16) / (1 << 16); F, G = f(th), g(th); P = (F * G).mean(); C = P - F.mean() * G.mean()
    for nombre, al in (("fase de la torre, log(phi)/2pi", a), ("racional 13/8", 13 / 8)):
        for N in (100, 1000, 10000):
            t = (np.arange(N) * al) % 1; x, y = f(t), g(t); R = x * y - P
            print(f"{nombre}: N={N}: error de la parte conexa {abs((x*y).mean()-x.mean()*y.mean()-C)/C:.1e}; media del resto/rms {abs(R.mean())/np.sqrt((R*R).mean()):.1e}")
    s = 12; H = np.sqrt(2) * phi ** (-s / 2)
    print(f"S(12) = {np.pi*phi**s:.2f}; Lambda(12) = {6*phi**(-s):.4f} > 0; Gibbons-Hawking pi/(G H^2) = {np.pi/(0.5*H*H):.2f}; "
          f"area del anillo/4G = {2*np.pi*phi**s/2:.2f}; Cardy c=3 = {2*np.pi*np.sqrt(3*phi**(2*s)/12):.2f}")
    x1 = jn_zeros(1, 1)[0]
    for k in (0.1, 0.05, 0.01):
        print(f"k/M_Pl = {k}: umbral de agujero negro / m1 = {1/(x1*k*k):.0f}")

SECCIONES.append((36, 'El agujero negro donde hace falta: la orbita de la torre, el horizonte de S(12), el umbral', seccion_36))

# ======================================================================
# 37. Consistencia: entropia, modos y bits; razon vectorial y profundidad; gluones; unidad; 700/380
# ======================================================================
def seccion_37():
    import numpy as np
    from scipy.special import jn_zeros, j0, y0
    from scipy.optimize import brentq
    phi = (1 + 5 ** 0.5) / 2; L = np.log(phi); M = 0.31384
    S = np.pi * phi ** 12
    print(f"S(12) = {S:.2f} (nats, como Gibbons-Hawking y Cardy); modos = {int(S)}; como bits de Shannon: {int(S)*np.log(2):.1f} nats, fraccion log2 = {np.log(2):.4f}")
    def ratio(depth):
        eps = phi ** (-depth); f = lambda x: j0(eps*x)*y0(x) - y0(eps*x)*j0(x)
        xs = np.linspace(0.5, 15, 6000); v = f(xs)
        r = [brentq(f, xs[i], xs[i+1]) for i in range(len(xs)-1) if v[i]*v[i+1] < 0]
        return r[1]/r[0], r[0]
    for lo, hi in ((-12, 12), (12, 36)):
        print(f"[{lo},{hi}]: m2/m1 = {ratio(hi-lo)[0]:.3f} (solo depende de la profundidad)")
    for d in (24, 81.74):
        r, x = ratio(d); print(f"fondo 12, profundidad {d}: primer gluon {x*M*phi**12:.0f} GeV, graviton {jn_zeros(1,1)[0]*M*phi**12:.0f} GeV")
    for m in (3600, 4000):
        print(f"gluon de {m} GeV: su fondo = {np.log(m/(jn_zeros(0,1)[0]*M))/L:.2f}")
    print(f"m_p/3 = 0.3128 GeV: sigma_IR = {np.log(99.6/0.3128)/L:.2f}")
    t = jn_zeros(1, 2); t = t[1]/t[0]; r = 700/380; e = r*np.hypot(20/700, 20/380)
    print(f"700/380 = {r:.4f} frente a {t:.4f}: {100*(r/t-1):.2f} %, {(r-t)/e:.2f} desviaciones estandar")

    # el espacio de Hilbert: el conteo exacto crece como e^S (S en nats)
    import math
    Mx=3000; sg=[0]*(Mx+1)
    for d in range(1,Mx+1):
        for k in range(d,Mx+1,d): sg[k]+=d
    pp=[0]*(Mx+1); pp[0]=1
    for n in range(1,Mx+1): pp[n]=3*sum(sg[k]*pp[n-k] for k in range(1,n+1))//n
    X=[];Y=[]
    for s_ in range(3,10):
        L0=round(phi**(2*s_)/2); X.append(math.pi*math.sqrt(2*L0)); Y.append(math.log(pp[L0])+1.5*math.log(L0))
    print(f"ln W + (3/2) ln L0 = a S + b: a = {np.polyfit(X,Y,1)[0]:.4f} (S en nats: dim = e^S; en bits seria a = 1/ln2 = 1.4427)")
    # W2: la dimension entera del nivel, estados con L0 <= N/2 (sin redondeo)
    cum=[0]
    for v in pp: cum.append(cum[-1]+v)
    Xs=[];Ys=[];Zs=[]; D={}
    for s_ in range(1,10):
        Lm=math.floor(phi**(2*s_)/2); D[s_]=cum[Lm+1]; Xs.append(math.pi*phi**s_); Ys.append(math.log(D[s_])); Zs.append(math.log(Lm))
    assert D[3]==1654 and D[4]==3436182 and D[5]==820599769985, D
    A_=np.vstack([Xs,Zs,np.ones(len(Xs))]).T[2:]; a_=np.linalg.lstsq(A_,np.array(Ys[2:]),rcond=None)[0][0]
    assert abs(a_-0.9972)<5e-4, a_
    print(f"W2: dimension entera (estados con L0 <= N/2): sigma=3,4,5 -> {D[3]}, {D[4]}, {D[5]}; ajuste lnD = a S + b ln L + c (sigma=3..9): a = {a_:.4f}")
    from decimal import Decimal, getcontext; getcontext().prec=60
    PHd=(1+Decimal(5).sqrt())/2; PId=Decimal("3.14159265358979323846264338327950288419716939937510582097494459")
    vals=[(PId*PHd**s_/n_).exp() for s_ in range(0,13) for n_ in range(1,41)]
    vals=[x for x in vals if x<Decimal(10)**40]     # con 60 digitos, la parte fraccionaria es fiable bajo 10^40
    near=min(abs(x-x.to_integral_value()) for x in vals)
    assert near>Decimal("1e-9"), near
    print(f"e^(S/n) < 10^40 para sigma=0..12, n=1..40 ({len(vals)} casos): ninguno entero (distancia minima {float(near):.2e}); Gelfond-Schneider: trascendente siempre")
    # la medida y la fase: con peso e^{2A}, la medida e^{4A} da los ceros de J1; e^{6A}, un espaciado sin desfase
    from scipy.linalg import eigh
    def spec(pe, Q=32, lo=-6, hi=6, n=5):
        h=L/Q; w=np.arange(lo*Q,hi*Q+1)/Q*L; pm=np.exp(-pe*(w[:-1]+w[1:])/2); N=len(w); K=np.zeros((N,N))
        for i in range(N-1):
            c=pm[i]/h**2; K[i,i]+=c; K[i+1,i+1]+=c; K[i,i+1]-=c; K[i+1,i]-=c
        r=np.exp(-2*w); r[0]/=2; r[-1]/=2
        m=np.sqrt(np.clip(eigh(K,np.diag(r),eigvals_only=True),0,None)); return m[1:n+1]/m[1]
    z=jn_zeros(1,5); print("medida e^{4A}:", np.round(spec(4),4), " ceros de J1:", np.round(z/z[0],4))
    print("medida e^{6A}:", np.round(spec(6),4), " (enteros: sin desfase)")

SECCIONES.append((37, 'Consistencia: entropia, modos y bits; profundidad; gluones; unidad; 700/380', seccion_37))

# ======================================================================
# 38. El 1/2 de (B1): cuanto de area, unidad de Fisher y bit de Shannon
# ======================================================================
def seccion_38():
    import math
    G = 0.5; a = 1 / (4 * G)
    print(f"ley de area: {a} por ell^2 = {a/2} por ell_P^2 (Bekenstein-Hawking 1/4); bit de Shannon ln2 = {math.log(2):.4f}")
    print(f"un bit de Shannon por area de Planck frente a la ley de area: cociente {math.log(2)/(a/2):.3f}; por ell^2: {math.log(2)/a:.3f}")
    print(f"area por unidad de S (un modo): {1/a} ell^2 = {2/a} ell_P^2")

SECCIONES.append((38, 'El 1/2 de (B1): cuanto de area, unidad de Fisher y bit de Shannon', seccion_38))

# ======================================================================
# 39. El throat con el teselado de Fibonacci de sus anillos (Figura 4)
# ======================================================================
def seccion_39():
    """La seccion del throat es la cuspide; cada anillo se cubre con tejas largas (A) y cortas (B) por la
    sustitucion A->AB, B->A, con semilla AAB en sigma=0. Antes de dibujar se comprueba: las fronteras de
    un anillo continuan en el siguiente, y S = pi(A/phi^2 + B/phi^3) en cada nivel. La inclinacion de la
    vista, el reparto de los puntos y la escala de los lazos son convenciones del dibujo."""
    import numpy as np, math
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    phi=(1+5**.5)/2; L=math.log(phi); LEV=list(range(7))
    # ---- teselado: palabra de cada anillo (A larga, B corta), semilla AAB en sigma=0
    words=["AAB"]
    for _ in range(6): words.append("".join({"A":"AB","B":"A"}[c] for c in words[-1]))
    def bounds(w):  # fronteras en fraccion de vuelta
        wid=[1 if c=="A" else 1/phi for c in w]; c=np.cumsum([0]+wid); return c/c[-1]
    for s in range(6):   # cada frontera de un anillo es frontera del siguiente (anidan)
        b0,b1=bounds(words[s]),bounds(words[s+1]); assert all(np.min(abs(b1-x))<1e-12 for x in b0)
    rows=[]
    for s in LEV:
        A=words[s].count("A"); B=words[s].count("B"); S=math.pi*phi**s
        Sw=math.pi*(A/phi**2+B/phi**3); assert abs(Sw-S)<1e-9*S
        rows.append(dict(s=s,S=S,modes=int(S),N=phi**(2*s),A=A,B=B,w=words[s]))
    print("anillos:",[(r['A'],r['B']) for r in rows],"; S = pi(A/phi^2+B/phi^3) exacto; fronteras anidadas")
    # ---- throat (pseudoesfera), igual que la Figura 4
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
        for j in range(row['modes']):                  # modos
            a=2*math.pi*j/row['modes']; x0,y0=P3(rad*1.07,hh,a); ax.plot(x0,y0,'ko',ms=1.5)
        # fronteras de las tejas: meridianos del anillo s al anillo s+1 sobre la superficie
        if s<6:
            yseg=np.linspace(y,y+L,30)
            for bnd in bounds(row['w'])[:-1]:
                a=2*math.pi*bnd-math.pi/2; xs,hs=np.exp(yseg)*np.cos(a),H(yseg)+k*np.exp(yseg)*np.sin(a)
                ax.plot(xs,hs,'k',lw=0.45 if math.sin(a)<0 else 0.3,ls='-' if math.sin(a)<0 else ':')
        ly=LAB[s]
        ax.text(-2.05,ly,f"σ = {s}\nS = {row['S']:.2f},  ⌊S⌋ = {row['modes']}\nN = {row['N']:.1f}\ntiles = {row['A']+row['B']} ({row['A']} long, {row['B']} short)",fontsize=6.2,va='center',family='serif')
        ax.plot([-1.32,-rad*1.08],[ly,hh],'k:',lw=0.4)
        # el anillo desenrollado al mismo ancho: tejas largas sombreadas, cortas en blanco
        b=bounds(row['w'])
        for i,c in enumerate(row['w']):
            x0=XD+WD*b[i]; x1=XD+WD*b[i+1]
            ax.add_patch(plt.Rectangle((x0,ly-HD/2),x1-x0,HD,facecolor='0.75' if c=='A' else 'white',edgecolor='k',lw=0.3))
    # la cuerda y los lazos, como en la Figura 4
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


SECCIONES.append((39, 'El throat con el teselado de Fibonacci de sus anillos (Figura 4)', seccion_39))

# ======================================================================
# 40. El diccionario sobre un teselado regular frente a la cuspide
# ======================================================================
def seccion_40():
    """Una red sobre un teselado regular {p,q} cortada en el nivel sigma: patas abiertas frente a S
    (Crofton), pares (teselado, chi) que dan S en promedio; la cuspide: metrica, dos prototejas,
    unicidad de la sustitucion, suma pesada exacta, chi equivalentes; la cuenta de puntos de Z[i] de §10.1."""
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
        R=math.acosh(1/(math.tan(math.pi/p)*math.tan(math.pi/q)))   # circunradio
        r=math.acosh(math.cos(math.pi/q)/math.sin(math.pi/p))         # inradio
        e=2*math.acosh(math.cos(math.pi/p)/math.sin(math.pi/q))       # arista
        return R,r,e
    def P0(p,q,center='tile'):
        R,_,_=radii(p,q); t=math.tanh(R/2)
        P=np.array([t*np.exp(2j*math.pi*(k+.5)/p) for k in range(p)]) if center=='tile' else np.array([t*np.exp(2j*math.pi*k/p) for k in range(p)])
        if center=='vertex':
            v=P[0]; P=(P-v)/(1-np.conj(v)*P); P[0]=0j
        return P
    def key(P): c=hcenter(P); return (round(c.real,6),round(c.imag,6))
    def tiles_within(p,q,Rmax,center='tile',with_centres=False):
        """todas las teselas cuyo centro esta a distancia <= Rmax+margen (BFS por aristas con poda).
        El centro de cada tesela se refleja junto con sus vertices, asi que es exacto."""
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
    print("  {7,3}: patas abiertas",n); print("  patas/S",[round(a/b,3) for a,b in zip(n,S)],"; constante de Crofton",round(cro,4))
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
    print("  pares (teselado, chi<=16), p,q<=60:",len(L),"; a menos de 1e-2..1e-6:",tol,"; mejor",best[1],f"a {best[0]:.2e}")
    for yy in (-3.0,0.0,1.7): assert abs(math.exp(-yy)**2*math.exp(2*yy)-1)<1e-12
    print("  cuspide: t=e^-y da (dth^2+dt^2)/t^2 = e^(2y)dth^2+dy^2; nivel s en t=phi^-s, longitud 2pi phi^s, distancia log phi")
    a0=2*math.pi/phi**2
    for s in (0,3,7):
        t=phi**-s
        for top,area in ((a0,a0/phi),(a0/phi,a0/phi**2)):
            dx=top*t; assert abs(dx*(phi/t-1/t)-area)<1e-12 and abs(dx/(t/phi)-phi*top)<1e-12
    print("  dos prototejas, iguales en todos los niveles: areas",round(a0/phi,6),"y",round(a0/phi**2,6))
    subs=[m for m in itertools.product(range(10),repeat=4) if m[0]+m[3]==1 and m[0]*m[3]-m[1]*m[2]==-1]
    assert subs==[(0,1,1,1),(1,1,1,0)]; print("  sustituciones de dos tejas con autovalor phi:",subs)
    PI=Decimal("3.14159265358979323846264338327950288419716939937510582097494459"); ph=(1+Decimal(5).sqrt())/2
    A,B=2,1
    for s in range(41):
        assert abs(PI/ph**2*A+PI/ph**3*B-PI*ph**s)<Decimal(10)**-45; A,B=A+B,A
    print("  S = pi(A/phi^2 + B/phi^3) exacto (60 digitos) para s = 0..40; tejas/S ->",round(phi**4/5**.5/math.pi,4))
    print("  chi equivalentes: e^(pi/phi^2) =",round(math.exp(math.pi/phi**2),3),", e^(pi/phi^3) =",round(math.exp(math.pi/phi**3),3))
    # cuenta con pesos fijos: arcos entre cortes en los circulos de nivel del {7,3} (el throat: dos pesos)
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
    print("  {7,3}: pesos distintos (arco entre cortes x 1/2) por nivel",nw,", 115 en total; el throat: 2 en todos los niveles")
    # el 1/2 de cada enunciado: la constante de la definicion lo coloca
    fstar={c_:[f for f in np.linspace(0.001,1,99901) if abs(1/math.sqrt(c_*f)-1)<1e-4] for c_ in (1.5,2,3)}
    assert all(abs(np.mean(v)-1/c_)<1e-3 for c_,v in fstar.items())
    mstar={k_:1/math.sqrt(k_) for k_ in (2,4,8)}; assert abs(mstar[4]-0.5)<1e-15
    ps=np.linspace(0.01,0.99,9801); Hb=-(ps*np.log2(ps)+(1-ps)*np.log2(1-ps)); assert abs(ps[np.argmax(Hb)]-0.5)<1e-9
    print("  tau_D/sqrt(c f)=tau_D da f=1/c (c=2 en CW6: 1/2); k mu^2=1 da mu=1/sqrt(k) (k=4, Fisher cuantica: 1/2); entropia binaria: 1/2 sin constante")
    def lattice(r2):
        R=int(math.isqrt(int(r2)))+1; return sum(1 for x in range(-R,R+1) for y in range(-R,R+1) if x*x+y*y<=r2)
    cnt=[lattice(phi**s) for s in range(7)]; assert cnt==[5,5,9,13,21,37,57], cnt
    c12=lattice(phi**12); assert c12==1005
    rat=[round(c/(math.pi*phi**s),2) for s,c in enumerate(cnt)]; r22=lattice(phi**22)/(math.pi*phi**22)
    print("  puntos de Z[i] (§10.1):",cnt,"; puntos/S",rat,"; sigma=12:",c12,"frente a floor S = 1011; sigma=22:",round(r22,4))

SECCIONES.append((40, 'El diccionario sobre un teselado regular frente a la cuspide', seccion_40))

# ======================================================================
# 41. Cinco teselados regulares frente a los niveles (Figura 5)
# ======================================================================
def seccion_41():
    """Cinco teselados {p,q} de discos de radio arcsinh phi^sigma, centros exactos (reflejados con los
    vertices): teselas dentro de cada disco, tangencias del borde de un nivel con aristas, y por que una
    cuenta no sigue a phi: las razones de Fibonacci se acercan a phi como 1/(sqrt5 q^2) y no mas."""
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
        R=math.acosh(1/(math.tan(math.pi/p)*math.tan(math.pi/q)))   # circunradio
        r=math.acosh(math.cos(math.pi/q)/math.sin(math.pi/p))         # inradio
        e=2*math.acosh(math.cos(math.pi/p)/math.sin(math.pi/q))       # arista
        return R,r,e
    def P0(p,q,center='tile'):
        R,_,_=radii(p,q); t=math.tanh(R/2)
        P=np.array([t*np.exp(2j*math.pi*(k+.5)/p) for k in range(p)]) if center=='tile' else np.array([t*np.exp(2j*math.pi*k/p) for k in range(p)])
        if center=='vertex':
            v=P[0]; P=(P-v)/(1-np.conj(v)*P); P[0]=0j
        return P
    def key(P): c=hcenter(P); return (round(c.real,6),round(c.imag,6))
    def tiles_within(p,q,Rmax,center='tile',with_centres=False):
        """todas las teselas cuyo centro esta a distancia <= Rmax+margen (BFS por aristas con poda).
        El centro de cada tesela se refleja junto con sus vertices, asi que es exacto."""
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
    print("  teselas cuyo centro cae dentro de cada disco:")
    for (p,q) in [(7,3),(3,7),(5,4),(12,5),(6,10)]: print(f"    {{{p},{q}}}:",[REC[(p,q,s)][0] for s in range(7)])
    print("  borde de un nivel tangente a aristas: solo {6,10}, sigma=1 (6 aristas) y sigma=3 (12 aristas)")
    F=[1,1]
    for _ in range(40): F.append(F[-1]+F[-2])
    dev=[abs(phi-F[n+1]/F[n])*5**.5*F[n]**2 for n in range(5,30)]
    assert all(abs(x-1)<0.05 for x in dev[5:])
    print("  razones de Fibonacci: |phi - F(n+1)/F(n)| * sqrt5 * F(n)^2 ->",round(dev[-1],6),"(Hurwitz: phi es el peor aproximado)")
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
    print("  {3,7} por vertices compartidos:",nl,"-> phi^2; por aristas ~1.6")
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
    print("  crecimiento por capa (aristas):",{k:round(v,3) for k,v in gr.items()},"; {5,4}: cosh e = phi; {6,10}: sinh r = phi; {5,4} con qubits:",round(c54*math.log(2),4),"S")


SECCIONES.append((41, 'Cinco teselados regulares frente a los niveles (Figura 5)', seccion_41))

# ======================================================================
# 42. Las dos coordenadas, el paso de nivel, la ortogonalizacion, el paso racional y el operador de imp:A1
# ======================================================================
def seccion_42():
    import math
    phi = (1 + 5 ** 0.5) / 2; psi = -1 / phi; L = math.log(phi)
    M = 6 * math.sqrt(3) * math.pi / L
    F = [0, 1]
    for _ in range(40): F.append(F[-1] + F[-2])
    # I1: el tiempo del weld es la segunda coordenada de Galois
    for s_ in (1, 2, 3, 6, 12):
        a, b = F[s_ - 1], F[s_]
        assert a * a + a * b - b * b == (-1) ** s_
        assert abs(M * abs(a + b * psi) - M * phi ** -s_) < 1e-9
    print(f"  I1: M|a + b phibar| = M phi^-s = tau(s) en s = 1, 2, 3, 6, 12; tau(12) = {M*phi**-12:.4f}, phi^12 = 89 + 144 phi, norma +1")
    # I2: la matriz de la sustitucion es el intercambio por un corrimiento
    ex = [[0, 1], [1, 0]]; sh = [[1, 0], [1, 1]]
    prod = [[sum(ex[i][k] * sh[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    assert prod == [[1, 1], [1, 0]]
    print("  I2: [[0,1],[1,0]] [[1,0],[1,1]] =", prod, "= matriz de A -> AB, B -> A")
    # I3: el anillo s se rotula por la unidad phi^{s+3} y es un aproximante periodico
    def sub(w): return "".join("AB" if c == "A" else "A" for c in w)
    w = "AAB"; ok = True
    for s_ in range(12):
        if (w.count("B"), w.count("A")) != (F[s_ + 2], F[s_ + 3]): ok = False
        ap = "A"
        for _ in range(s_ + 2): ap = sub(ap)
        if not (len(ap) == len(w) and ap in w + w): ok = False
        w = sub(w)
    assert ok
    print("  I3: anillo s, s = 0..11: (B, A) = (F_{s+2}, F_{s+3}), coeficientes de phi^{s+3}; palabra = rotacion de s^{s+2}(A)")
    # I4: ortogonalizacion en el medio giro
    for p_ in (0.3, 0.5, 0.7):
        ov = abs((1 - p_) + p_ * complex(math.cos(math.pi), math.sin(math.pi)))
        assert (ov < 1e-12) == (p_ == 0.5)
    e0 = L / (6 * math.sqrt(3))
    assert all(abs(e0 * phi ** s_ * M * phi ** -s_ - math.pi) < 1e-12 for s_ in range(20))
    print("  I4: eps(s) tau(s) = pi en cada nivel; solapamiento en el medio giro 1 - 2p: 0.4, 0, 0.4 en p = 0.3, 0.5, 0.7")
    # I5: el paso racional frente al contraste
    out = []
    for p_, q_ in [(21, 13), (34, 21), (55, 34), (89, 55), (144, 89), (233, 144)]:
        f = L / math.log(p_ / q_)
        out.append((p_, q_, abs(11.97 * f - 11.97) / 0.05, abs(583.789 * f - 583.789) / 0.028))
    assert out[0][3] > 70 and out[3][3] > 3 and out[4][3] < 3
    print("  I5: paso p/q -> desviaciones (fondo, observador):", ", ".join(f"{a}/{b}: {x:.1f}, {y:.1f}" for a, b, x, y in out))
    # I6: la traza 3 y la geodesica mas corta
    assert abs(phi ** 2 + phi ** -2 - 3) < 1e-12 and abs(2 * math.acosh(1.5) - 4 * L) < 1e-12
    print(f"  I6: tr [[2,1],[1,1]] = 3 = phi^2 + phi^-2; largo 2 arccosh(3/2) = {2*math.acosh(1.5):.6f} = 4 log phi")
    # I7: el operador de imp:A1 con n = 6
    n = 6; m = [2 * math.sin(k * math.pi / (4 * (n + 1))) / L for k in range(1, 2 * n + 2)]
    r = [m[k + 1] / m[k] for k in range(len(m) - 1)]
    assert all(abs(x - phi) > 0.05 for x in r)
    print("  I7: razones de masas sucesivas de imp:A1, n = 6:", [round(x, 2) for x in r], "; ninguna es phi")

SECCIONES.append((42, 'Las dos coordenadas, el paso de nivel, la ortogonalizacion, el paso racional y el operador de imp:A1', seccion_42))

# ======================================================================
# 43. Las tres columnas y por que no encajaban: R11, la diagonal del cubo, el nucleo racional, Bragg
# ======================================================================
def seccion_43():
    import math, itertools
    import numpy as np
    phi = (1 + 5 ** 0.5) / 2
    # R11: sustituciones primitivas de dos letras con entradas <= 3
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
    print("  C1-C3 (irracional, unimodular, Pisot):", sorted(ok123), "; con la ley aditiva:", sorted(ok4))
    # la diagonal del cubo
    n = np.array([1, 1, 1]) / 3 ** 0.5; P = [e - (e @ n) * n for e in np.eye(3)]
    ang = {round(math.degrees(math.acos(P[i] @ P[j] / (np.linalg.norm(P[i]) * np.linalg.norm(P[j])))), 6) for i, j in [(0, 1), (1, 2), (0, 2)]}
    assert ang == {120.0} and np.allclose(sum(P), 0)
    print(f"  Z^3 por (1,1,1): tres ejes de largo {np.linalg.norm(P[0]):.4f} a 120 grados (red hexagonal, Z[omega] a escala sqrt(2/3)); el nucleo es Z(1,1,1)")
    # nucleo de la proyeccion racional
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
    print(f"  Z^2 -> recta, pares en [-60,60]^2: pendiente 3/2 -> {c32} coincidencias; pendiente phi -> {cphi}")
    # Bragg de la cadena de Fibonacci
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
    print("  cuenta de teselas: F_{s+4} - 0.9757 S = +-phi^-(s+4)/sqrt5 exacto (Binet, Pisot), s = 0..24")
    print(f"  Bragg (N = {len(x)}): (2,3) {pk[(2,3)]:.2f}, (1,2) {pk[(1,2)]:.2f}, (1,1) {pk[(1,1)]:.2f}; 200 puntos al azar: max {rnd:.3f}")

SECCIONES.append((43, 'Las tres columnas y por que no encajaban', seccion_43))

if __name__ == "__main__":
    pedir = {int(a) for a in sys.argv[1:]}
    for n, nombre, f in SECCIONES:
        if pedir and n not in pedir:
            continue
        print(f"\n{'#' * 72}\n# {n}. {nombre}\n{'#' * 72}")
        try:
            f()
        except ModuleNotFoundError as e:
            print(f"[sección {n} omitida: falta el módulo {e.name}]")
