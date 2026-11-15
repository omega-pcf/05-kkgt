"""figuras_v134.py: el código de generación de las cinco figuras de
«One object instead of a choice of vacuum to put the observer in de Sitter space» (kk_golden_throat_v134.tex),
extraído de reproduce_v134.py; lo dibujado y lo comprobado no cambia.

  Figura 1  fig_background.pdf       sección 44  (§2, Background)
  Figura 2  fig_mobius_throat.pdf    sección 13  (§11.1, las dos familias recíprocas)
  Figura 3  fig_granularity.pdf      sección 10  (§11.1, granularidad)
  Figura 4  fig_throat_tiling.pdf    sección 39  (el throat con el teselado de Fibonacci)
  Figura 5  fig_tilings_strip.pdf    sección 41  (cinco teselados regulares frente a los niveles)

Uso:  python3 figuras_v134.py          las cinco
      python3 figuras_v134.py 1 4      solo esas figuras (numeración del artículo)
Cada sección comprueba numéricamente lo que dibuja (assert) antes de guardar el PDF.
Python 3.13, NumPy, SciPy, Matplotlib.
"""
import sys


# ======================================================================
# Figura 3 (sección 10): granularidad
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


# ======================================================================
# Figura 2 (sección 13): las dos familias recíprocas
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


# ======================================================================
# Figura 4 (sección 39): el throat con el teselado de Fibonacci
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


# ======================================================================
# Figura 5 (sección 41): cinco teselados regulares frente a los niveles
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


def seccion_44():
    """Figura del Background (fig:background): el toro y la tercera dirección; de la diagonal a la cara;
    cada dimensión desde la siguiente; los anillos del throat teselados. Cada enunciado dibujado se comprueba."""
    import numpy as np, math, itertools, matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    from matplotlib.lines import Line2D
    from mpl_toolkits.mplot3d.art3d import Poly3DCollection
    plt.rcParams.update({"font.family":"serif","mathtext.fontset":"cm","font.size":12})
    phi=(1+5**.5)/2; pb=(1-5**.5)/2; L=math.log(phi); M=6*3**.5*math.pi/L
    INK="#333333"; RED="#c0392b"; BLU="#2f6db3"; GOLD="#c99a2e"; GRN="#2e8b57"; TEAL="#5aa6a6"; VIO="#7b4fa0"
    t=np.linspace(0,2*np.pi,300); w=np.exp(2j*np.pi/3)
    fig=plt.figure(figsize=(17,21))
    def head(x,y,txt,col=INK):
        # la prosa de cada panel vive en el caption; aqui solo la letra
        fig.text(x,y,txt,ha="center",va="top",fontsize=26,color=col)
    def sep(y): fig.add_artist(Line2D([0.04,0.96],[y,y],color="0.85",lw=.8))
    X3=(0.17,0.50,0.83)

    # ======== fila 1: la tercera dirección, en |z| = 1/2
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
    head(X3[0],0.955,"(a)")
    ax=fig.add_axes([0.36,0.785,0.28,0.145],projection="3d")
    for a_ in np.linspace(0,2*np.pi,24,endpoint=False): ax.plot([R*np.cos(a_)]*2,[R*np.sin(a_)]*2,[-1.2,1.2],color="k",lw=.35)
    for g_ in np.linspace(-0.75,0.75,7):
        ax.plot([g_,g_],[-0.75,0.75],[-phi*.75,phi*.75],color="k",lw=.3,alpha=.7); ax.plot([-0.75,0.75],[g_,g_],[phi*g_]*2,color="k",lw=.3,alpha=.7)
    ax.plot(R*np.cos(t),R*np.sin(t),-1.2+0*t,"k",lw=1.0); ax.plot(R*np.cos(t),R*np.sin(t),phi*R*np.sin(t),"k",lw=1.6)
    for nm,col,k in TRI:
        v=V3[k]; ax.scatter([v.real],[v.imag],[-1.2],c=col,s=14,depthshade=False); ax.scatter([v.real],[v.imag],[phi*v.imag],c=col,s=40,depthshade=False)
        ax.plot([v.real]*2,[v.imag]*2,[-1.2,phi*v.imag],color=col,lw=.7,ls=":"); ax.text(v.real*1.5,v.imag*1.5,phi*v.imag,nm,color=col,fontsize=24,weight="bold")
    ax.view_init(elev=18,azim=-125); ax.set_box_aspect((1,1,1.4)); ax.set_axis_off()
    head(X3[1],0.955,"(b)")
    ax=fig.add_axes([0.70,0.80,0.26,0.15]); ax.set_aspect("equal"); ax.axis("off")
    sq=R/2**.5
    for i in range(-3,4): ax.plot([i*sq]*2,[-3*sq,3*sq],color="#9fd6d6",lw=.5); ax.plot([-3*sq,3*sq],[i*sq]*2,color="#9fd6d6",lw=.5)
    ax.plot(R*np.cos(t),R*np.sin(t),"--",color="0.5",lw=.9)
    ax.fill([v.real for v in V3],[v.imag for v in V3],color="#c9a0d6",alpha=.5); ax.plot([v.real for v in V3+[V3[0]]],[v.imag for v in V3+[V3[0]]],"k",lw=1.2)
    ax.add_patch(plt.Rectangle((0,0),sq,sq,fill=False,ec="#1a8f8f",lw=2))
    for nm,col,k in TRI:
        v=V3[k]; ax.plot(v.real,v.imag,"o",color=col,ms=9)
        ax.text(v.real+(.06 if k==0 else 0),v.imag+(.08 if k==1 else -.1 if k==2 else 0),f"{nm} ({120*k}°)",color=col,fontsize=20,weight="bold",ha="left" if k==0 else "center",va="center")
    ax.set_xlim(-3.1*sq,3.1*sq); ax.set_ylim(-3.1*sq,3.1*sq)
    head(X3[2],0.955,"(c)")
    sep(0.78)

    # ======== fila 2: de 1D a 3D
    head(0.5,0.7720,"(d)")
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
                d=phi**s; ax.add_patch(plt.Rectangle((0,0),d,d,fill=False,ec="#1a8f8f",lw=1.1,alpha=0.35+0.11*s)); ax.text(d+.1,d,f"{sides[s]:.0f}",fontsize=18,color="0.35")
                assert abs((L/(6*3**.5))*phi**s*M*phi**-s-math.pi)<1e-12
            ax.set_xlim(-.4,12.5); ax.set_ylim(-.4,12.5)
        if i<4: fig.text(xs5[i]+W5+0.015,0.6900,"→",fontsize=24,ha="center",va="center",color="0.45")
    sep(0.5900)

    # ======== fila 3: el cubo que gira
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
        if abs(x)<12 and abs(y)<4: ax.plot(x,y,"o",mfc="none",mec=RED,ms=6); ax.text(x+.2,y+.15,f"$\\varphi^{{{n}}}$",fontsize=18,color=RED)
    ax.axhspan(-1,phi-1,color=BLU,alpha=.12); win=k&(X2>=-1)&(X2<phi-1); ax.plot(X1[win],X2[win],"o",color=BLU,ms=3)
    ch=np.sort(X1[win]); ax.plot(ch,0*ch-3.6,"|",color=BLU,ms=9); ax.axhline(-3.6,color=BLU,lw=.6)
    gaps=set(np.round(np.diff(ch),6)); assert gaps<= {round(1.0,6),round(phi,6)} and len(gaps)==2
    ax.set_xlim(-12,12); ax.set_ylim(-4,4); ax.set_xlabel("$x=a+b\\varphi$",fontsize=20,color="0.35"); ax.set_ylabel("$\\bar x=a+b\\bar\\varphi$",fontsize=20,color="0.35")
    ax.tick_params(labelsize=15,colors="0.5")
    for s_ in ax.spines.values(): s_.set_color("0.75")
    head(X3[0],0.5580,"(e)")
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
    ax.plot([-1.3,2.8],[-1.3,2.8],[-1.3,2.8],"k",lw=1.3); ax.text(2.9,2.9,2.9,"$(1,1,1)$",fontsize=20)
    ax.view_init(14,-20); ax.set_axis_off(); ax.set_box_aspect((1,1,1))
    head(X3[1],0.5580,"(f)")
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
    head(X3[2],0.5580,"(g)")
    sep(0.3550)

    # ======== fila 4: las tejas y el throat de lado
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
    # (h) las tejas, sigma=6 arriba ... sigma=0 abajo
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
        axH.text(-0.03,yrow(s_)+.27,f"$\\sigma={s_}$",ha="right",va="center",fontsize=20,color="0.25")
        axH.text(1.03,yrow(s_)+.27,f"{A_+B_} = {A_}+{B_}",ha="left",va="center",fontsize=18,color="0.3")
    axH.set_xlim(-0.16,1.3); axH.set_ylim(-0.2,NL-0.3)
    head(0.17,0.322,"(h)")
    # (i) el throat, niveles 0..6, con las tejas largas sombreadas en la cara frontal
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
        axG.text(xs_,-1.16,f"{s_}",ha="center",fontsize=22,color="0.25")
    axG.text(Lh/2,-1.36,"level $\\sigma$",ha="center",fontsize=22,color="0.4")
    axG.set_xlim(-0.05,Lh+0.3); axG.set_ylim(-1.42,1.12)
    head(0.685,0.322,"(i)")
    fig.canvas.draw()
    FH=lambda xy: fig.transFigure.inverted().transform(axH.transData.transform(xy))
    FG=lambda xy: fig.transFigure.inverted().transform(axG.transData.transform(xy))
    for s_ in LEV:
        p=FH((1.27,yrow(s_)+.27)); q=FG((xpos(s_),rad(s_)))
        fig.add_artist(Line2D([p[0],q[0]],[p[1],q[1]],color="0.7",lw=.6,ls=":"))
    fig.savefig("fig_background.pdf",bbox_inches="tight"); plt.close(fig)
    plt.rcParams.update(matplotlib.rcParamsDefault)
    print("figura del Background: ok")


# número de figura del artículo -> (sección de reproduce_v134.py, función, nombre)
FIGURAS = {1: (44, seccion_44, "fig_background.pdf"),
           2: (13, seccion_13, "fig_mobius_throat.pdf"),
           3: (10, seccion_10, "fig_granularity.pdf"),
           4: (39, seccion_39, "fig_throat_tiling.pdf"),
           5: (41, seccion_41, "fig_tilings_strip.pdf")}

if __name__ == "__main__":
    pedir = {int(a) for a in sys.argv[1:]} or set(FIGURAS)
    for n in sorted(pedir):
        sec, f, nombre = FIGURAS[n]
        print(f"\n{'#'*72}\n# Figura {n} (sección {sec}) -> {nombre}\n{'#'*72}")
        f()
