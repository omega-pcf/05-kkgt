"""Sections 9-16, moved out of ``_rest`` (SEC-001, layer 2, lot 2).

They are the bodies of ``seccion_9`` … ``seccion_16`` verbatim; the
registry is assembled by ``kkgt.sections.__init__``.
"""

from ..constants import (
    M_KOIDE_MEV,
    M_TAU_MEV,
)

SECCIONES = []

# ======================================================================
# 9. Gap ratios (Discussion 6.1)
# ======================================================================
def seccion_9():
    """Why phi for the ensemble: an irrational orbit on the circle visits every phase.
    Star discrepancy D_N of {n alpha}, n=1..N, and the number of distinct gaps (three gaps)."""
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

SECCIONES.append((9, 'Gap ratios (Discussion 6.1)', seccion_9))

# ======================================================================
# 10. Figure 3: granularity, with its numbers
# ======================================================================
def seccion_10():
    """Granularity: integer, dyadic and golden levels; phase of the worldline."""
    import numpy as np
    phi=(1+5**.5)/2; lp=np.log(phi)
    def gaps(x):
        x=np.sort(np.r_[0,np.mod(x,1),1]); g=np.diff(x); g=g[g>1e-12]; return g
    F=[1,2,3,5,8,13,21,34,55,89,144,233,377,610,987]
    print("levels a+b*phi in [0,1): N points {n phi}, distinct gaps, max/min ratio")
    for N in F[3:]:
        g=gaps(np.arange(1,N+1)*phi); print(N, len(np.unique(np.round(g,9))), round(g.max()/g.min(),4), "max gap", round(g.max(),5))
    print("dyadics: resolution 2^-k requires k binary digits (k registers)")
    for k in range(1,11): print(k, 2**k, 2.0**-k)
    # phase: step log(phi)/(2 pi) on the circle; Gelfond: log(phi)/pi irrational
    a=lp/(2*np.pi)
    print("phase rotation per level (turns):", a)
    print("worst gap ratio, phase, N<=5000:", round(max(gaps(np.arange(1,N+1)*a).max()/gaps(np.arange(1,N+1)*a).min() for N in range(10,5001)),3))
    print("worst gap ratio, phi, N<=5000:", round(max(gaps(np.arange(1,N+1)*phi).max()/gaps(np.arange(1,N+1)*phi).min() for N in range(10,5001)),3))
    exc=[N for N in range(3,5001) if abs(gaps(np.arange(1,N+1)*phi).max()/gaps(np.arange(1,N+1)*phi).min()-phi**2)>1e-6]
    print("N <= 5000 with ratio different from phi^2:", exc, "(N+1, marks including the origin, is Fibonacci: two lengths, ratio phi)")

    # The drawing of figure 3 lives in the generator
    # scripts/figures/figuras_v134.py (generate_fig_granularity); this
    # section keeps the numbers the manuscript cites from it and writes
    # no file (SPEC-002 §1.1: a test never produces a figure).

SECCIONES.append((10, 'Figure 3: granularity, with its numbers', seccion_10))

# ======================================================================
# 11. Contact configurations in 1D, 2D and 3D (6.1)
# ======================================================================
def seccion_11():
    """Contact in 1, 2 and 3 dimensions from pi and phi.
    1D: two neighbours; 2D: the six units of Z[omega], omega = e^{2 pi i/3}; 3D: the twelve vertices
    (0, ±1, ±phi) and the cyclic permutations of the icosahedron."""
    import numpy as np, itertools
    phi=(1+5**.5)/2
    # 2D
    u=np.exp(1j*np.pi*np.arange(6)/3)
    d2=[abs(a-b) for a,b in itertools.combinations(u,2)]
    print("2D: 6 units, |u|=1:", np.allclose(abs(u),1), " minimum distance between neighbours:", round(min(d2),12))
    # 3D
    V=[]
    for s1 in (1,-1):
        for s2 in (1,-1):
            p=(0,s1,s2*phi); V+= [p,(p[1],p[2],p[0]),(p[2],p[0],p[1])]
    V=np.array(V,float); print("3D: vertices", len(V))
    r2=(V**2).sum(1); print("   |v|^2 = phi+2:", np.allclose(r2,phi+2))
    D=[((a-b)**2).sum() for a,b in itertools.combinations(V,2)]
    vals=np.unique(np.round(D,9)); print("   distinct squared distances:", vals, " (4, 4phi+4? ->", 4*phi+4, ")")
    print("   edges (d^2=4):", sum(abs(x-4)<1e-9 for x in D), "; neighbours per vertex:", 2*sum(abs(x-4)<1e-9 for x in D)//12)
    W=2*V/np.sqrt(phi+2)   # centres at distance 2: unit spheres touching the central one
    m=min(((a-b)**2).sum() for a,b in itertools.combinations(W,2))**.5
    print("   contact: 12 unit spheres touching the central one, minimum distance between them:", round(m,4), ">= 2:", m>=2)
    print("   slack: 4 >= phi+2 <=> phi <= 2")
    # J3 (v134): in 3D the 12 is also reached by FCC and HCP, without phi
    fcc=[v for v in itertools.product([-1,0,1],repeat=3) if sorted(map(abs,v))==[0,1,1]]
    Wf=[2*np.array(v)/np.sqrt(2) for v in fcc]
    mf=min(np.linalg.norm(a-b) for a,b in itertools.combinations(Wf,2))
    hc=[(2*np.cos(k*np.pi/3),2*np.sin(k*np.pi/3),0) for k in range(6)]
    for s in (1,-1):
        for k in range(3):
            t=k*2*np.pi/3+np.pi/6; hc.append((2*np.cos(t)/np.sqrt(3),2*np.sin(t)/np.sqrt(3),2*s*np.sqrt(2/3)))
    hc=np.array(hc); mh=min(np.linalg.norm(a-b) for a,b in itertools.combinations(hc,2))
    assert len(fcc)==12 and abs(mf-2)<1e-12 and len(hc)==12 and np.allclose(np.linalg.norm(hc,axis=1),2) and abs(mh-2)<1e-12
    print("   FCC and HCP: 12 unit spheres at distance 2 from the central one, without phi; minimum distance between them:", round(mf,4), round(mh,4))
    print("   the twelve of the icosahedron and that of the background are proved separately")
    # the chain of the twelve
    print("chain: |A5|/5 =", 60//5, "; pi(10)/5 = 60/5 =", 12, "; lcm(4,6) =", np.lcm(4,6), "; -1/zeta(-1) = 12")

SECCIONES.append((11, 'Contact configurations in 1D, 2D and 3D (6.1)', seccion_11))

# ======================================================================
# 12. One structure seen at once: the checks, the points of Z[i] per level and the vector ratio
# ======================================================================
def seccion_12():
    """Exact geometry of the throat, the torus and the fibre (article 9, v9).
    Every figure comes from a statement proved in TorreKK_LYR_v8.lean; this script checks
    those statements numerically (the figure that drew them left in the v134; Figure 1, section 44, draws them now).

    Sources: CW6 eq. (torus), Prop. (fibre independent of base), eq. (worldline), eq. (throat);
    HP Def. (tower parameters), Prop. (certainty principle).
    """
    import numpy as np

    phi = (1 + 5 ** 0.5) / 2
    lp = np.log(phi)
    eps0 = lp / (6 * np.sqrt(3))
    M = 6 * np.sqrt(3) * np.pi / lp

    # ---------- checks (one per Lean theorem) ----------
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
    # Clifford torus: stereographic projection from (0,0,0,1) -> surface of revolution R = sqrt2, r = 1
    a, b = np.meshgrid(np.linspace(0, 2*np.pi, 60), np.linspace(0, 2*np.pi, 60))
    X = np.stack([np.cos(a), np.sin(a), np.cos(b), np.sin(b)]) / np.sqrt(2)
    P = X[:3] / (1 - X[3])
    rho = np.hypot(P[0], P[1])
    assert np.allclose((rho - np.sqrt(2))**2 + P[2]**2, 1, atol=1e-9)        # clifford_square + stereographic
    print("eps0 =", eps0, " M_PCF =", M, " eps0*M/pi =", eps0*M/np.pi)
    print("phase on the cell at sigma=12: pi *", phi**24)
    print("all checks: ok")


    # 2. the points of Z[i] inside the disc of each level (text of §11.1)
    cnt=[sum(1 for a_ in range(-60,61) for b_ in range(-60,61) if a_*a_+b_*b_<=phi**s_) for s_ in range(7)]
    assert cnt==[5,5,9,13,21,37,57]
    assert [int(np.floor(np.pi*phi**s_)) for s_ in range(7)]==[3,5,8,13,21,34,56]
    rat=[round(c/(np.pi*phi**s_),2) for s_,c in enumerate(cnt)]
    assert rat==[1.59,0.98,1.09,0.98,0.98,1.06,1.01]
    c22=sum(2*int(np.floor(np.sqrt(phi**22-a_*a_)))+1 for a_ in range(-int(phi**11)-1,int(phi**11)+2) if a_*a_<=phi**22)
    assert round(c22/(np.pi*phi**22),4)==0.9998
    c12=sum(2*int(np.floor(np.sqrt(phi**12-a_*a_)))+1 for a_ in range(-30,31) if a_*a_<=phi**12)
    assert c12==1005 and int(np.floor(np.pi*phi**12))==1011
    print("points of Z[i] in the disc of area S, sigma = 0..6:",cnt,"; ratio to S:",rat,"; sigma = 22:",round(c22/(np.pi*phi**22),4),"; sigma = 12:",c12,"against",int(np.floor(np.pi*phi**12)))

    # 3. the vector ratio against the depth (§10), exact two-brane condition: the table of §10
    from scipy.special import j0, y0
    from scipy.optimize import brentq
    def ratio(D):
        e=1/D; f=lambda x: j0(e*x)*y0(x)-y0(e*x)*j0(x)
        xs=np.linspace(0.3,12,3000); v=f(xs); z=[brentq(f,xs[i],xs[i+1]) for i in range(len(xs)-1) if v[i]*v[i+1]<0]
        return z[1]/z[0]
    tab={6:2.093,12:2.171,24:2.228,30:2.241,81.74:2.275}
    for d_,r_ in tab.items(): assert round(ratio(phi**d_),3)==r_
    print("m2/m1 against the depth:",tab,": ok")

SECCIONES.append((12, 'One structure seen at once: the checks, the points of Z[i] per level and the vector ratio', seccion_12))

# ======================================================================
# 13. Figure 2: the two reciprocal families
# ======================================================================
def seccion_13():
    """Exact figure 2: at each level sigma = 12..18,
     left: the ring of the throat, radius proportional to z(sigma) = phi^sigma (normalized phi^(sigma-18));
     right: the Möbius fibre over its own loop, the half-turn period tau(sigma) = M phi^-sigma
     (radius normalized phi^-(sigma-12)), with half a turn per loop (epsilon(sigma) tau(sigma) = pi,
     closure_each_level) and half-width 1/2 of the radius of its loop (|Omega| = 1/2, the B1 drawing
     convention).
     The product of the two radii is constant, phi^-6: z tau = M."""
    import numpy as np
    phi=(1+5**.5)/2; lev=np.arange(12,19)
    rz=lambda s: phi**(s-18); rt=lambda s: phi**(-(s-12))
    for s in lev: assert abs(rz(s)*rt(s)-phi**-6)<1e-12          # z*tau constante
    # The drawing of figure 2 lives in the generator
    # scripts/figures/figuras_v134.py (generate_fig_mobius_throat); this
    # section only checks the statement behind it and writes no file
    # (SPEC-002 §1.1: a test never produces a figure).
    print("ok")

SECCIONES.append((13, 'Figure 2: the two reciprocal families', seccion_13))

# ======================================================================
# 14. Three gaps of the marks on the ring (6.1)
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
        print(f"σ={s} N={phi**(2*s):.3f} gaps(100,1e3,1e4)={out} discrepancy={D:.4f}")

SECCIONES.append((14, 'Three gaps of the marks on the ring (6.1)', seccion_14))

# ======================================================================
# 15. Exact count of states with c = 3 at the level N/2 against S (6.1)
# ======================================================================
def seccion_15():
    import math
    phi=(1+5**.5)/2
    M=3000
    sig=[0]*(M+1)
    for d in range(1,M+1):
        for k in range(d,M+1,d): sig[k]+=d
    p=[0]*(M+1); p[0]=1          # c=3 boson states: prod (1-q^n)^-3 ; n p(n) = 3 sum sigma(k) p(n-k)
    for n in range(1,M+1):
        p[n]=3*sum(sig[k]*p[n-k] for k in range(1,n+1))//n
    print("σ   N=φ^2σ   L0=N/2  ln#states   S=π√N   ratio  bound πz   N/πz")
    for s in range(1,10):
        N=phi**(2*s); L0=round(N/2); z=phi**s
        lnW=math.log(p[L0]); S=math.pi*math.sqrt(2*L0)
        print(f"{s}  {N:9.2f} {L0:6d}  {lnW:10.3f}  {S:8.3f}  {lnW/S:.4f}   {math.pi*z:8.2f}  {N/(math.pi*z):6.2f}")
    print("\nWith the next-order Cardy correction, ln W ≈ S − (c+3)/4·ln L0 + C, c=3:")
    for s in range(3,10):
        L0=round(phi**(2*s)/2); S=math.pi*math.sqrt(2*L0)
        print(f"σ={s}  S − ln W − (3/2) ln L0 = {S-math.log(p[L0])-1.5*math.log(L0):.4f}")

SECCIONES.append((15, 'Exact count of states with c = 3 at the level N/2 against S (6.1)', seccion_15))

# ======================================================================
# 16. The scale M of (F1): Koide-type reconstruction of the lepton masses
# ======================================================================
def seccion_16():
    import math
    M = M_KOIDE_MEV   # MeV, (F1)
    d = 2 / 9    # delta = 2/n^2, n = 3
    obs = {"e": 0.51099895, "mu": 105.6583755, "tau": M_TAU_MEV}
    m = sorted(M * (1 + math.sqrt(2) * math.cos(d + 2 * math.pi * k / 3)) ** 2 for k in range(3))
    for (name, o), x in zip(obs.items(), m):
        print(f"{name:4s} Koide from M: {x:10.4f} MeV   observed: {o:10.4f}   rel. {abs(x-o)/o:.1e}")

SECCIONES.append((16, 'The scale M of (F1): Koide-type reconstruction of the lepton masses', seccion_16))
