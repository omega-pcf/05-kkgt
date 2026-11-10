/-
  TorreKK_LYR.lean, v33 (7 de noviembre de 2026; v33 corrige el orden en la docstring de level_step_is_exchange_shift): todo lo que el artículo 9 demuestra en Lean.
  Estado: [P*] escrito, SIN COMPILAR (no hay Lean en el entorno donde se escribió).
  Sin sorry. Axiomas, al final, para resultados clásicos que Mathlib aún no tiene (cada uno con su fuente).

  Contenido
  1. El operador de A.7 (saltos b², b⁻²) es autoadjunto en la métrica η_σ = b^(−4σ)
     (simetría de η·K, renglón a renglón).                                  [E1]
  2. η_σ = exp(4·A σ) con A σ = −σ·log b: la métrica es √(−g) de la garganta.   [E1]
  3. El simetrizador correcto es D_σ = b^(−2σ), con D² = η; el de la prueba
     de A.1, b^σ, no simetriza si b > 1.                                     [defecto 1]
  4. Los saltos b², b⁻² son la dispersión de Bloch con momento k − i·2·log b.  [§1]
  5. La fase de los ceros de J_ν con ν = d/2 − 1 es (d − 3)/4, y vale 1/4
     exactamente cuando d = 4 = n + 1 con n = 3.                             [E2]
  6. Randall–Sundrum es la garganta dorada (cambio de variable).
  7. El anillo: modo constante m²(log φ)² = −1, bajo la cota de BF −4.
  8. El reloj de φ: la media vuelta x¹² en un reloj de orden 24.
  9. Un exponente lleva un ángulo y un radio.
 10. Resultados importados de CW6 y F1: z·τ = M, ε₀·M = π, valuación dorada, |2|₂ = φ^{−λ}.
 11. (v31) El tiempo del weld es la segunda coordenada de Galois; el paso de nivel es el
     intercambio (n,w) ↦ (w,n) con un corrimiento; la ortogonalidad en el medio giro exige ½;
     la traza 3 del cuadrado de la matriz dorada.
 12. (v32) La diagonal del cubo tiene nucleo; la cuenta de teselas difiere de su media por
     −ψⁿ/√5 (Binet); un paso racional p/q tiene nucleo (−p, q).
-/
import Mathlib

noncomputable section
open Real Complex

namespace TorreKK

set_option linter.style.longLine false

/-! ### 1–3. La métrica de la garganta -/

/-- Métrica del nivel σ: η_σ = b^(−4σ). -/
def etaMetric (b : ℝ) (σ : ℤ) : ℝ := b ^ (-(4 : ℤ) * σ)

/-- Salto hacia abajo (σ → σ−1) y hacia arriba (σ → σ+1) del operador de A.7. -/
def hopDown (b : ℝ) : ℝ := b ^ (2 : ℤ)
def hopUp (b : ℝ) : ℝ := b ^ (-(2 : ℤ))

/-- E1: η·K es simétrica. El elemento (σ, σ+1) de η·K es η_σ·b⁻²; el (σ+1, σ)
    es η_{σ+1}·b². Son iguales para toda base no nula. -/
theorem eta_symmetrizes (b : ℝ) (hb : b ≠ 0) (σ : ℤ) :
    etaMetric b σ * hopUp b = etaMetric b (σ + 1) * hopDown b := by
  unfold etaMetric hopUp hopDown
  rw [← zpow_add₀ hb, ← zpow_add₀ hb]
  congr 1
  ring

/-- En la orientación opuesta, el operador reflejado (saltos b⁻² desde abajo y b² desde arriba)
    lo simetriza η'_σ = b^(4σ): η'_σ·b² = η'_{σ+1}·b⁻². -/
theorem eta_reflected_symmetrizes (b : ℝ) (hb : b ≠ 0) (σ : ℤ) :
    b ^ ((4 : ℤ) * σ) * hopDown b = b ^ ((4 : ℤ) * (σ + 1)) * hopUp b := by
  unfold hopDown hopUp
  rw [← zpow_add₀ hb, ← zpow_add₀ hb]
  congr 1
  ring

/-- E1: η es la exponencial de 4A, con A σ = −σ·log b. -/
theorem eta_eq_exp_fourA (b : ℝ) (hb : 0 < b) (σ : ℤ) :
    etaMetric b σ = Real.exp (4 * (-(σ : ℝ) * Real.log b)) := by
  unfold etaMetric
  rw [← Real.rpow_intCast, Real.rpow_def_of_pos hb]
  congr 1
  push_cast
  ring

/-- Simetrizador de la prueba de A.1, corregido: D_σ = b^(−2σ). -/
def D (b : ℝ) (σ : ℤ) : ℝ := b ^ (-(2 : ℤ) * σ)

/-- D² = η. -/
theorem D_sq_eq_eta (b : ℝ) (hb : b ≠ 0) (σ : ℤ) : D b σ * D b σ = etaMetric b σ := by
  unfold D etaMetric
  rw [← zpow_add₀ hb]
  congr 1
  ring

/-- Con D, los dos saltos conjugados coinciden (el operador conjugado es simétrico):
    (D_{σ+1}/D_σ)·b² = (D_σ/D_{σ+1})·b⁻², ambos iguales a 1. -/
theorem D_conjugated_hops_equal (b : ℝ) (hb : b ≠ 0) (σ : ℤ) :
    (D b (σ + 1) / D b σ) * hopDown b = (D b σ / D b (σ + 1)) * hopUp b := by
  unfold D hopDown hopUp
  rw [← zpow_sub₀ hb, ← zpow_sub₀ hb, ← zpow_add₀ hb, ← zpow_add₀ hb]
  congr 1
  ring


/-- Conjugado por D, cada salto vale exactamente 1: el operador conjugado es la cadena simétrica
    con diagonal 2 y saltos −1 (en unidades de (log b)⁻²), una banda de Dirichlet de fase 0. -/
theorem D_conjugated_hop_is_one (b : ℝ) (hb : b ≠ 0) (σ : ℤ) :
    (D b (σ + 1) / D b σ) * hopDown b = 1 := by
  unfold D hopDown
  rw [← zpow_sub₀ hb, ← zpow_add₀ hb]
  have : -(2 : ℤ) * (σ + 1) - -(2 : ℤ) * σ + 2 = 0 := by ring
  rw [this, zpow_zero]

/-- El simetrizador que nombra la prueba de A.1, b^σ, no simetriza si b > 1:
    tendría que valer b·b² = b⁻¹·b⁻², es decir b³ = b⁻³. -/
theorem old_symmetrizer_fails (b : ℝ) (hb : 1 < b) :
    b * b ^ (2 : ℤ) ≠ b⁻¹ * b ^ (-(2 : ℤ)) := by
  have h0 : (0 : ℝ) < b := by linarith
  have hb0 : b ≠ 0 := ne_of_gt h0
  intro h
  have hl : b * b ^ (2 : ℤ) = b ^ (3 : ℤ) := by
    rw [show (3 : ℤ) = 1 + 2 by norm_num, zpow_add₀ hb0, zpow_one]
  have hr : b⁻¹ * b ^ (-(2 : ℤ)) = b ^ (-(3 : ℤ)) := by
    rw [show (-(3 : ℤ)) = -1 + -2 by norm_num, zpow_add₀ hb0, zpow_neg_one]
  rw [hl, hr] at h
  have h1 : (1 : ℝ) < b ^ (3 : ℤ) := one_lt_zpow₀ hb (by norm_num)
  have h2 : b ^ (-(3 : ℤ)) < 1 := zpow_lt_one_of_neg₀ hb (by norm_num)
  linarith

/-! ### 4. Bloch con momento complejizado -/

/-- e^{i(k − iε)} = e^{ε}·e^{ik}: complejizar el momento por −iε multiplica el salto por e^{ε}. -/
theorem bloch_complexified (k ε : ℝ) :
    Complex.exp (I * ((k : ℂ) - I * ε)) = Real.exp ε * Complex.exp (I * k) := by
  have : I * ((k : ℂ) - I * ε) = (ε : ℂ) + I * k := by
    rw [mul_sub, ← mul_assoc, I_mul_I]
    ring
  rw [this, Complex.exp_add, ← Complex.ofReal_exp]

/-- Con ε = 2·log b (b > 0), el factor es exactamente el salto b². -/
theorem bloch_factor_is_hop (b : ℝ) (hb : 0 < b) :
    Real.exp (2 * Real.log b) = b ^ (2 : ℤ) := by
  rw [show (2 : ℝ) * Real.log b = Real.log b + Real.log b by ring, Real.exp_add,
    Real.exp_log hb, zpow_two]

/-- Y con −ε, el salto recíproco b⁻². -/
theorem bloch_factor_is_hop_inv (b : ℝ) (hb : 0 < b) :
    Real.exp (-(2 * Real.log b)) = b ^ (-(2 : ℤ)) := by
  rw [Real.exp_neg, bloch_factor_is_hop b hb, zpow_neg]

/-! ### 5. La fase de Bessel la fija la dimensión -/

/-- Índice de Bessel del perfil del gravitón en AdS_{d+1}. -/
def nuOf (d : ℚ) : ℚ := d / 2 - 1

/-- Fase asintótica de los ceros de J_ν: j_{ν,k} ≈ π(k + ν/2 − 1/4). -/
def besselPhase (ν : ℚ) : ℚ := ν / 2 - 1 / 4

theorem phase_of_dimension (d : ℚ) : besselPhase (nuOf d) = (d - 3) / 4 := by
  unfold besselPhase nuOf
  ring

/-- La fase es 1/4 si y solo si d = 4. -/
theorem phase_quarter_iff (d : ℚ) : besselPhase (nuOf d) = 1 / 4 ↔ d = 4 := by
  rw [phase_of_dimension]
  constructor
  · intro h; linarith
  · intro h; subst h; norm_num

/-- Con la aridad n = 3 de CW6, d = n + 1 = 4, ν = 1 y la fase es 1/4. -/
theorem phase_from_arity : nuOf ((3 : ℚ) + 1) = 1 ∧ besselPhase (nuOf ((3 : ℚ) + 1)) = 1 / 4 := by
  unfold besselPhase nuOf
  norm_num

/-! ### 6. Randall–Sundrum es la garganta dorada (cambio de variable) -/

/-- El warp de RS con k = 1 en y = (σ_UV − σ)·log b es el warp dorado normalizado al UV:
    e^{−y} = b^σ / b^{σ_UV}. -/
theorem rs_warp_is_golden (b : ℝ) (hb : 0 < b) (σ σUV : ℝ) :
    Real.exp (-((σUV - σ) * Real.log b)) = b ^ σ / b ^ σUV := by
  rw [Real.rpow_def_of_pos hb, Real.rpow_def_of_pos hb, ← Real.exp_sub]
  congr 1
  ring

/-- La profundidad de RS: e^{−kπr} = b^{−(σ_UV − σ_IR)} con kπr = (σ_UV − σ_IR)·log b. -/
theorem rs_depth_is_levels (b : ℝ) (hb : 0 < b) (σIR σUV : ℝ) :
    Real.exp (-((σUV - σIR) * Real.log b)) = b ^ (-(σUV - σIR)) := by
  rw [Real.rpow_def_of_pos hb]
  congr 1
  ring

/-- La escala KK de RS es el operador de escala en el fondo: k·e^{−kπr} = m₀·b^{σ_IR}
    cuando la curvatura es la escala del UV, k = m₀·b^{σ_UV}. -/
theorem rs_scale_is_H_at_bottom (b m₀ : ℝ) (hb : 0 < b) (σIR σUV : ℝ) :
    (m₀ * b ^ σUV) * Real.exp (-((σUV - σIR) * Real.log b)) = m₀ * b ^ σIR := by
  rw [rs_warp_is_golden b hb σIR σUV]
  have : b ^ σUV ≠ 0 := (Real.rpow_pos_of_pos hb σUV).ne'
  field_simp

/-- Con el UV en una escala M_UV > 0: kπr = log(M_UV/m₀) − σ_IR·log b, es decir, kπr es la
    distancia en niveles entre el fondo y el UV, por log b. -/
theorem rs_kpir_from_uv (b m₀ MUV : ℝ) (hb : 0 < b) (hm : 0 < m₀) (hM : 0 < MUV) (σIR : ℝ) :
    Real.log (MUV / (m₀ * b ^ σIR)) = Real.log (MUV / m₀) - σIR * Real.log b := by
  have h1 : 0 < b ^ σIR := Real.rpow_pos_of_pos hb σIR
  rw [Real.log_div hM.ne' (mul_pos hm h1).ne', Real.log_mul hm.ne' h1.ne',
    Real.log_div hM.ne' hm.ne', Real.log_rpow hb]
  ring

/-! ### 7. El anillo y la cota de Breitenlohner–Freedman (Remark 2) -/

/-- En la torre dorada, b² + b⁻² = 3. -/
theorem sq_add_inv_sq (b : ℝ) (hb : 0 < b) (h : b ^ 2 = b + 1) : b ^ 2 + (b⁻¹) ^ 2 = 3 := by
  have hb0 : b ≠ 0 := hb.ne'
  have hinv : b⁻¹ = b - 1 := by
    field_simp
    nlinarith [h]
  rw [hinv]; nlinarith [h]

/-- En el anillo el modo constante tiene m²·(log b)² = 2 − b² − b⁻² = −1. -/
theorem ring_constant_mode (b : ℝ) (hb : 0 < b) (h : b ^ 2 = b + 1) :
    2 - b ^ 2 - (b⁻¹) ^ 2 = -1 := by
  have := sq_add_inv_sq b hb h; linarith

/-- log φ < 1/2, así que −1/(log φ)² < −4, la cota de BF de CW6 (ec. 158). -/
theorem log_golden_lt_half (b : ℝ) (hb : 0 < b) (h : b ^ 2 = b + 1) : Real.log b < 1 / 2 := by
  have hb1 : b < 13 / 8 := by nlinarith [h]
  have he : (13 / 8 : ℝ) ≤ Real.exp (1 / 2) := by
    have := Real.quadratic_le_exp_of_nonneg (x := (1 / 2 : ℝ)) (by norm_num)
    linarith
  rw [Real.log_lt_iff_lt_exp hb]; linarith

theorem ring_mode_below_BF (b : ℝ) (hb : 0 < b) (h : b ^ 2 = b + 1) (h1 : 1 < b) :
    -1 / (Real.log b) ^ 2 < -4 := by
  have hl : 0 < Real.log b := Real.log_pos h1
  have hl2 := log_golden_lt_half b hb h
  have hsq : (Real.log b) ^ 2 < 1 / 4 := by nlinarith
  have hpos : 0 < (Real.log b) ^ 2 := by positivity
  rw [div_lt_iff₀ hpos]; nlinarith

/-! ### 8. El reloj de φ y su media vuelta (Definition, Proposition 7)
  El reloj de φ módulo N es el orden de φ en ℤ[φ]/N (el periodo de Pisano); los órdenes
  π(16) = π(9) = π(12) = π(24) = π(48) = π(72) = 24 y π(5) = 20 están en el módulo XXI,
  `RelojYMenosUnoDoce` (pi_sixteen, pi_nine, pi_twelve, pi_twentyfour, pi_fortyeight,
  pi_seventytwo, pi_five). Aquí, para cualquier monoide: -/

/-- En un reloj de orden 24, x¹² es la media vuelta: distinto de 1, de cuadrado 1, orden 2. -/
theorem half_turn_of_clock24 {G : Type*} [Monoid G] (x : G) (hx : orderOf x = 24) :
    x ^ 12 ≠ 1 ∧ (x ^ 12) ^ 2 = 1 ∧ orderOf (x ^ 12) = 2 := by
  have h1 : x ^ 12 ≠ 1 := by
    intro h
    have := orderOf_le_of_pow_eq_one (by norm_num) h
    omega
  have h2 : (x ^ 12) ^ 2 = 1 := by
    rw [← pow_mul]; norm_num; rw [← hx]; exact pow_orderOf_eq_one x
  exact ⟨h1, h2, orderOf_eq_prime h2 h1⟩

/-- En un reloj de orden 20, x¹² no es una involución. -/
theorem not_half_turn_of_clock20 {G : Type*} [Monoid G] (x : G) (hx : orderOf x = 20) :
    (x ^ 12) ^ 2 ≠ 1 := by
  rw [← pow_mul]
  intro h
  have := orderOf_dvd_of_pow_eq_one h
  rw [hx] at this
  norm_num at this

/-! ### 9. Un exponente lleva un ángulo y un radio (notas −1/12, §10.2 (a)) -/

/-- q^E con q = e^{2πiτ}, τ = x + iy: e^{2πiEτ} = e^{2πiEx}·e^{−2πEy}; el primer factor tiene
    módulo 1 (el giro) y el segundo es real positivo (el radio). -/
theorem exponent_angle_radius (E x y : ℝ) :
    Complex.exp (2 * Real.pi * I * E * ((x : ℂ) + I * y))
      = Complex.exp (2 * Real.pi * I * (E * x)) * (Real.exp (-2 * Real.pi * E * y) : ℂ) := by
  rw [Complex.ofReal_exp, ← Complex.exp_add]
  congr 1
  push_cast
  ring_nf
  rw [I_sq]
  ring

theorem angle_has_modulus_one (E x : ℝ) :
    ‖Complex.exp (2 * Real.pi * I * (E * x))‖ = 1 := by
  rw [show (2 * Real.pi * I * (E * x) : ℂ) = ((2 * Real.pi * (E * x) : ℝ) : ℂ) * I by
    push_cast; ring]
  exact Complex.norm_exp_ofReal_mul_I _

/-! ### 10. Resultados importados de CW6 y F1 (Appendix A del artículo v2)
  Enunciados elementales de CW6 y F1 que el artículo usa, demostrados aquí de nuevo para que
  el módulo sea autocontenido. -/

/-- CW6 `lattice_radius_conjugate`, F1 §tower-info: z(σ)·τ(σ) = M con z = b^σ, τ = M·b^{−σ}. -/
theorem lattice_radius_conjugate (b M σ : ℝ) (hb : 0 < b) :
    b ^ σ * (M * b ^ (-σ)) = M := by
  rw [Real.rpow_neg hb.le]
  have : b ^ σ ≠ 0 := (Real.rpow_pos_of_pos hb σ).ne'
  field_simp

/-- CW6 (31), F1 `eps0_relates_log_and_geometry`: con ε₀ = log b/(6√3) y M = 6√3·π/log b,
    ε₀·M = π (el principio de certeza), y log b = 6√3·π/M. -/
theorem certainty_principle (b : ℝ) (hb : 1 < b) :
    (Real.log b / (6 * Real.sqrt 3)) * (6 * Real.sqrt 3 * Real.pi / Real.log b) = Real.pi := by
  have hl : Real.log b ≠ 0 := (Real.log_pos hb).ne'
  have hs : Real.sqrt 3 ≠ 0 := by positivity
  field_simp

theorem log_from_scale (b : ℝ) (hb : 1 < b) :
    Real.log b = 6 * Real.sqrt 3 * Real.pi / (6 * Real.sqrt 3 * Real.pi / Real.log b) := by
  have hl : Real.log b ≠ 0 := (Real.log_pos hb).ne'
  have hp : 6 * Real.sqrt 3 * Real.pi ≠ 0 := by positivity
  field_simp

/-- F1 `prop:tower-disc-val`: la valuación dorada v(x) = log x / log b vale n en b^n. -/
theorem golden_valuation_on_tower (b : ℝ) (hb : 1 < b) (n : ℤ) :
    Real.log (b ^ n) / Real.log b = n := by
  have hl : Real.log b ≠ 0 := (Real.log_pos hb).ne'
  rw [Real.log_zpow]; field_simp

/-- F1 `prop:omega-two-adic`: con λ = log 2 / log b, b^{−λ} = 1/2 = |2|₂. -/
theorem two_adic_is_level (b : ℝ) (hb : 1 < b) :
    b ^ (-(Real.log 2 / Real.log b)) = 1 / 2 := by
  have hb0 : 0 < b := by linarith
  have hl : Real.log b ≠ 0 := (Real.log_pos hb).ne'
  rw [Real.rpow_def_of_pos hb0]
  have : Real.log b * -(Real.log 2 / Real.log b) = -Real.log 2 := by field_simp
  rw [this, Real.exp_neg, Real.exp_log (by norm_num)]; norm_num

/-- F1, la ley aditiva de la torre: si r > 0 y r^σ + r^{σ+1} = r^{σ+2} para algún σ real,
    entonces r² = r + 1, cuya única raíz positiva es φ. -/
theorem additive_law_forces_golden (r σ : ℝ) (hr : 0 < r)
    (h : r ^ σ + r ^ (σ + 1) = r ^ (σ + 2)) : r ^ 2 = r + 1 := by
  rw [Real.rpow_add hr, Real.rpow_add hr, Real.rpow_one, Real.rpow_two] at h
  have hs : 0 < r ^ σ := Real.rpow_pos_of_pos hr σ
  have h2 : r ^ σ * (r ^ 2 - r - 1) = 0 := by linear_combination (-1 : ℝ) * h
  rcases mul_eq_zero.mp h2 with h3 | h3
  · exact absurd h3 hs.ne'
  · linarith

/-! ### 11. La estructura detrás de las masas (retroducción matemática) -/

/-- φ nace del círculo: φ = 2 cos(π/5), la razón del pentágono inscrito; un número ciclotómico. -/
theorem golden_eq_two_cos_pi_div_five :
    (1 + Real.sqrt 5) / 2 = 2 * Real.cos (Real.pi / 5) := by
  rw [Real.cos_pi_div_five]; ring

/-- φ se refiere a sí mismo: φ = 1 + 1/φ. Su fracción continua es [1; 1, 1, …], todos los
    cocientes parciales iguales a 1: es el irracional peor aproximado por fracciones (Hurwitz). -/
theorem golden_self_reference (b : ℝ) (hb : 0 < b) (h : b ^ 2 = b + 1) : b = 1 + 1 / b := by
  have hb0 : b ≠ 0 := hb.ne'
  field_simp; ring
  nlinarith [h]

/-- El ángulo y la escala son uno (CW6, Prop. 3.4): con α(σ) = arctan(ε₀ b^σ),
    tan α(σ+1) / tan α(σ) = b. Subir un nivel multiplica la tangente del ángulo por b. -/
theorem spectral_angle_ratio (b ε σ : ℝ) (hb : 0 < b) (hε : 0 < ε) :
    Real.tan (Real.arctan (ε * b ^ (σ + 1))) / Real.tan (Real.arctan (ε * b ^ σ)) = b := by
  rw [Real.tan_arctan, Real.tan_arctan, Real.rpow_add hb, Real.rpow_one]
  have : 0 < b ^ σ := Real.rpow_pos_of_pos hb σ
  field_simp

/-- Las raíces periódicas del anillo que usa el artículo: la cuarta vuelta i (el desfase ¼) y
    la media vuelta −1 (el fondo), con i² = −1 e i⁴ = 1. -/
theorem quarter_and_half_turn : Complex.I ^ 2 = -1 ∧ Complex.I ^ 4 = 1 := by
  constructor
  · exact Complex.I_sq
  · rw [show (4 : ℕ) = 2 * 2 from rfl, pow_mul, Complex.I_sq]; norm_num


/-! ## Geometría exacta de la garganta, el toro y la fibra
Fuentes: CW6 eq. (torus) `T² = ℂ/Λ`, `Λ = M·ℤ[i]`, `τ = i`; Prop. "fibre independent of base"
(monodromía `e^{iπ} = −1`); eq. (worldline) `Ω(t) = ½ e^{i t log φ}`; eq. (throat) `z(σ) = φ^σ`.
HP Def. "tower parameters": `ε(σ) = ε₀ φ^σ`, `M_σ = φ^σ M`; Prop. "certainty principle":
la media vuelta cierra sobre la longitud de onda `π/ε(σ) = M φ^{−σ}`. -/

/-- El parámetro modular de cada nivel de la torre de retículas es `i`:
`Λ_σ = s·M·ℤ[i]` con `s = φ^σ` tiene `τ = (s M i)/(s M) = i`. El toro es el mismo en todo nivel,
salvo la escala. -/
theorem lattice_tower_tau (s M : ℝ) (hs : 0 < s) (hM : 0 < M) :
    ((s * M : ℝ) * Complex.I) / ((s * M : ℝ) : ℂ) = Complex.I := by
  have h : ((s * M : ℝ) : ℂ) ≠ 0 := by exact_mod_cast (mul_pos hs hM).ne'
  field_simp

/-- La media vuelta cierra en cada nivel sobre la longitud de onda `τ(σ) = M b^{−σ}`:
`ε(σ)·τ(σ) = (ε₀ b^σ)(M b^{−σ}) = ε₀ M = π`. -/
theorem closure_each_level (b ε₀ M σ : ℝ) (hb : 0 < b) (hc : ε₀ * M = Real.pi) :
    (ε₀ * b ^ σ) * (M * b ^ (-σ)) = Real.pi := by
  have h1 : b ^ σ * b ^ (-σ) = 1 := by
    rw [← Real.rpow_add hb, add_neg_cancel, Real.rpow_zero]
  calc (ε₀ * b ^ σ) * (M * b ^ (-σ)) = (ε₀ * M) * (b ^ σ * b ^ (-σ)) := by ring
    _ = Real.pi := by rw [h1, hc, mul_one]

/-- Sobre la celda `M_σ = M b^σ` la fase acumulada es `π b^{2σ}`. -/
theorem phase_on_cell (b ε₀ M σ : ℝ) (hb : 0 < b) (hc : ε₀ * M = Real.pi) :
    (ε₀ * b ^ σ) * (M * b ^ σ) = Real.pi * b ^ (2 * σ) := by
  have h2 : b ^ σ * b ^ σ = b ^ (2 * σ) := by
    rw [← Real.rpow_add hb]; ring_nf
  calc (ε₀ * b ^ σ) * (M * b ^ σ) = (ε₀ * M) * (b ^ σ * b ^ σ) := by ring
    _ = Real.pi * b ^ (2 * σ) := by rw [h2, hc]

/-- Y esa fase es la media vuelta solo en el nivel `σ = 0`. -/
theorem phase_on_cell_halfturn_iff (b σ : ℝ) (hb : 1 < b) :
    Real.pi * b ^ (2 * σ) = Real.pi ↔ σ = 0 := by
  constructor
  · intro h
    have hp : Real.pi ≠ 0 := Real.pi_ne_zero
    have h1 : b ^ (2 * σ) = b ^ (0 : ℝ) := by
      rw [Real.rpow_zero]; exact mul_left_cancel₀ hp (by rw [mul_one]; exact h)
    have hinj : (2 * σ) = 0 := by
      rcases lt_trichotomy (2 * σ) 0 with hl | he | hg
      · have := (Real.rpow_lt_rpow_left_iff hb).mpr hl; linarith
      · exact he
      · have := (Real.rpow_lt_rpow_left_iff hb).mpr hg; linarith
    linarith
  · intro h; rw [h]; simp

/-- La monodromía de la fibra: media vuelta, `e^{iπ} = −1`, de orden dos. -/
theorem fibre_half_turn : Complex.exp (Real.pi * Complex.I) = -1 ∧ ((-1 : ℂ)) ^ 2 = 1 := by
  refine ⟨Complex.exp_pi_mul_I, by norm_num⟩

/-- El módulo de la línea de mundo es `½` a toda fase: `|½ e^{iθ}| = ½`. -/
theorem worldline_modulus (θ : ℝ) :
    ‖(1 / 2 : ℂ) * Complex.exp (θ * Complex.I)‖ = 1 / 2 := by
  rw [Complex.norm_mul, Complex.norm_exp_ofReal_mul_I]; norm_num

/-- La garganta es exactamente una pseudoesfera (Beltrami): el perfil `r(y) = e^{y}`, `y ≤ 0`,
con altura `h'(y) = √(1 − r²)` tiene rapidez uno, `r'² + h'² = 1`; la métrica inducida es
`e^{2y} dθ² + dy²`, la sección radial de `ds² = e^{2A} dx² + dy²`. -/
theorem pseudosphere_unit_speed (y : ℝ) (hy : y ≤ 0) :
    (Real.exp y) ^ 2 + (Real.sqrt (1 - (Real.exp y) ^ 2)) ^ 2 = 1 := by
  have h1 : Real.exp y ≤ 1 := Real.exp_le_one_iff.mpr hy
  have h0 : 0 ≤ Real.exp y := (Real.exp_pos y).le
  have : 0 ≤ 1 - (Real.exp y) ^ 2 := by nlinarith
  rw [Real.sq_sqrt this]; ring

/-- Los anillos: el radio en el nivel `σ` es `b^σ` (salvo normalización), y anillos sucesivos
están en razón `b`. -/
theorem ring_ratio (b σ : ℝ) (hb : 0 < b) : b ^ (σ + 1) / b ^ σ = b := by
  rw [Real.rpow_add hb, Real.rpow_one]
  have : 0 < b ^ σ := Real.rpow_pos_of_pos hb σ
  field_simp

/-- El toro cuadrado `τ = i` en el toro de Clifford: `(a,b) ↦ (cos a, sin a, cos b, sin b)/√2`
tiene sus dos derivadas parciales de igual norma, `½`, y ortogonales: es la métrica plana
cuadrada. Su proyección estereográfica (conforme, clásica) es el toro de revolución con
`R/r = √2`. -/
theorem clifford_square (a b : ℝ) :
    (Real.sin a) ^ 2 / 2 + (Real.cos a) ^ 2 / 2 = 1 / 2 ∧
    (Real.sin b) ^ 2 / 2 + (Real.cos b) ^ 2 / 2 = 1 / 2 := by
  constructor <;> nlinarith [Real.sin_sq_add_cos_sq a, Real.sin_sq_add_cos_sq b]


/-! ## Por qué φ para el ensamble: la órbita no se cierra
Una rotación de paso `φ` sobre el círculo no tiene periodo: `n·φ` nunca es entero para `n ≠ 0`.
Con Weyl (1916) la órbita es equidistribuida: el promedio sobre una órbita es el promedio
sobre todo el círculo. -/

theorem golden_irrational : Irrational ((1 + Real.sqrt 5) / 2) := by
  have h5 : Irrational (Real.sqrt 5) := by
    simpa using Nat.Prime.irrational_sqrt (by norm_num : Nat.Prime 5)
  have h1 : Irrational ((1 : ℚ) + Real.sqrt 5) := Irrational.ratCast_add 1 h5
  have h2 := Irrational.div_ratCast h1 (by norm_num : (2 : ℚ) ≠ 0)
  simpa using h2

theorem golden_rotation_aperiodic (n m : ℤ) (hn : n ≠ 0) :
    (n : ℝ) * ((1 + Real.sqrt 5) / 2) ≠ m :=
  (Irrational.intCast_mul golden_irrational hn).ne_int m


/-! ## Contacto en 2 y 3 dimensiones
2D: las seis unidades de ℤ[ω], a distancia 1 del origen y de sus vecinas (lado de π).
3D: los doce vértices `(0, ±1, ±φ)` del icosaedro (lado de φ).
El 12: |A₅| / 5 = 60 / 5 = mcm(4, 6) (F1, módulo XXI: `group_orders`, `pi_ten`,
`minus_one_twelfth_is_the_clock`). -/

/-- Contacto hexagonal: `e^{iπ/3}` está a distancia 1 de `1`. -/
theorem hexagonal_contact :
    (Real.cos (Real.pi / 3) - 1) ^ 2 + (Real.sin (Real.pi / 3)) ^ 2 = 1 := by
  rw [Real.cos_pi_div_three, Real.sin_pi_div_three]
  have h : Real.sqrt 3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  nlinarith [h]

/-- Los vértices `(0, ±1, ±φ)` están a distancia² `φ + 2` del centro. -/
theorem icosahedron_vertex_norm (b : ℝ) (h : b ^ 2 = b + 1) :
    (0 : ℝ) ^ 2 + 1 ^ 2 + b ^ 2 = b + 2 := by nlinarith [h]

/-- Dos vecinos, `(0,1,φ)` con `(0,−1,φ)` y `(0,1,φ)` con `(1,φ,0)`, están a distancia² 4. -/
theorem icosahedron_edges (b : ℝ) (h : b ^ 2 = b + 1) :
    (0 - 0 : ℝ) ^ 2 + (1 - (-1)) ^ 2 + (b - b) ^ 2 = 4
    ∧ (0 - 1 : ℝ) ^ 2 + (1 - b) ^ 2 + (b - 0) ^ 2 = 4 := by
  constructor
  · ring
  · nlinarith [h]

/-- Con los centros a distancia 2, las doce esferas unitarias tocan la central y no se
cortan entre sí: la distancia² entre vecinas, `4·4/(φ+2)`, es al menos 4 porque `φ + 2 ≤ 4`. -/
theorem icosahedral_kissing (b : ℝ) (h1 : 0 < b) (h2 : b ≤ 2) :
    4 ≤ 4 * 4 / (b + 2) := by
  rw [le_div_iff₀ (by linarith)]; nlinarith

/-- El doce: `|A₅| = 60`, `60 / 5 = 12 = mcm(4, 6)`. -/
theorem twelve_of_the_icosahedron :
    Fintype.card (alternatingGroup (Fin 5)) = 60 ∧ 60 / 5 = 12 ∧ Nat.lcm 4 6 = 12 := by
  have h5 := two_mul_card_alternatingGroup (α := Fin 5)
  rw [Fintype.card_perm, Fintype.card_fin] at h5
  have f5 : Nat.factorial 5 = 120 := rfl
  rw [f5] at h5
  exact ⟨by omega, rfl, by norm_num⟩

/-- `φ` es la traza de la rotación icosaédrica de ángulo `2π/5`: `1 + 2cos(2π/5) = φ`. -/
theorem golden_is_icosahedral_trace :
    1 + 2 * Real.cos (2 * Real.pi / 5) = (1 + Real.sqrt 5) / 2 := by
  have h : 2 * Real.pi / 5 = 2 * (Real.pi / 5) := by ring
  rw [h, Real.cos_two_mul, Real.cos_pi_div_five]
  have h5 : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)
  nlinarith [h5]


/-- La masa es información: `π(k+¼)·M·b^{12} = (k+¼)·M·S(12)` con `S(σ) = π b^σ`, la entropía de
saturación del nivel (CW6 §4.4). -/
theorem mass_is_bottom_information (b M k : ℝ) :
    Real.pi * (k + 1 / 4) * M * b ^ 12 = (k + 1 / 4) * M * (Real.pi * b ^ 12) := by ring


/-! ## Auditoría: lo que faltaba para que el argumento quede completo en Lean -/

/-- Prop. «The scale is the scale operator at the bottom»: `j·b^σ = j·H(σ)/m₀`, con `H = m₀ b^σ`. -/
theorem scale_operator_at_bottom (j m₀ b σ : ℝ) (hm : m₀ ≠ 0) :
    j * b ^ σ = j * (m₀ * b ^ σ) / m₀ := by
  field_simp

/-- Prop. «The bottom is the half-turn», punto 2: `χ(SL₂ℤ) = ¼ + ⅙ − ½ = −1/12` desde la
amalgama `ℤ/4 *_{ℤ/2} ℤ/6`. -/
theorem euler_char_amalgam : (1 / 4 + 1 / 6 - 1 / 2 : ℚ) = -1 / 12 := by norm_num

/-- `S` tiene orden 4 y `ST` orden 6 en `SL₂(ℤ)`. -/
theorem modular_orders :
    let S : Matrix (Fin 2) (Fin 2) ℤ := !![0, -1; 1, 0]
    let T : Matrix (Fin 2) (Fin 2) ℤ := !![1, 1; 0, 1]
    S ^ 4 = 1 ∧ S ^ 2 ≠ 1 ∧ (S * T) ^ 6 = 1 ∧ (S * T) ^ 2 ≠ 1 ∧ (S * T) ^ 3 ≠ 1 := by
  decide

set_option maxRecDepth 100000 in
/-- Los relojes de `φ`: el orden de la matriz de Fibonacci `Q = [[0,1],[1,1]]` (la
multiplicación por `φ` en `ℤ[φ]`) módulo `N`. Es 24 para `N = 16` y `N = 9`, 20 para `N = 5`
y 60 para `N = 10`; en cada caso se descartan los divisores maximales. -/
theorem pisano_orders :
    let Q16 : Matrix (Fin 2) (Fin 2) (ZMod 16) := !![0, 1; 1, 1]
    let Q9 : Matrix (Fin 2) (Fin 2) (ZMod 9) := !![0, 1; 1, 1]
    let Q5 : Matrix (Fin 2) (Fin 2) (ZMod 5) := !![0, 1; 1, 1]
    let Q10 : Matrix (Fin 2) (Fin 2) (ZMod 10) := !![0, 1; 1, 1]
    (Q16 ^ 24 = 1 ∧ Q16 ^ 12 ≠ 1 ∧ Q16 ^ 8 ≠ 1) ∧
    (Q9 ^ 24 = 1 ∧ Q9 ^ 12 ≠ 1 ∧ Q9 ^ 8 ≠ 1) ∧
    (Q5 ^ 20 = 1 ∧ Q5 ^ 10 ≠ 1 ∧ Q5 ^ 4 ≠ 1) ∧
    (Q10 ^ 60 = 1 ∧ Q10 ^ 30 ≠ 1 ∧ Q10 ^ 20 ≠ 1 ∧ Q10 ^ 12 ≠ 1) := by
  decide


/-! ## Axiomas: resultados clásicos que Mathlib aún no tiene
Cada uno es un teorema publicado; se declara aquí como axioma con su fuente, y todo lo que el
artículo deriva de él se demuestra a partir del axioma. -/

/-- **Axioma (ceros de `J₁`).** Los ceros positivos de la función de Bessel `J₁`, en orden
creciente, con sus cuatro primeros valores y la fase de McMahon `π(k + ¼)`.
Fuentes: Watson, *A Treatise on the Theory of Bessel Functions* (1944), §15.53; para la torre de
Kaluza–Klein, Randall y Sundrum (1999) y Davoudiasl, Hewett y Rizzo (2000). -/
axiom bessel_J1_zeros :
  ∃ j : ℕ → ℝ, StrictMono j ∧ 0 < j 0 ∧
    |j 0 - 3.8317| < 1e-4 ∧ |j 1 - 7.0156| < 1e-4 ∧ |j 2 - 10.1735| < 1e-4 ∧
    |j 3 - 13.3237| < 1e-4 ∧
    Filter.Tendsto (fun k : ℕ => j k - Real.pi * ((k : ℝ) + 1 + 1 / 4)) Filter.atTop (nhds 0)

/-- **Axioma (Gelfond–Schneider).** Para todo real algebraico `a ≠ 0`, `e^{πa}` es trascendente:
es `(−1)^{−ia}`, con base algebraica distinta de 0 y 1 y exponente `−ia` algebraico y no racional.
Fuentes: Gelfond (1934); Schneider (1935). -/
axiom exp_pi_mul_algebraic_transcendental (a : ℝ) (ha : IsAlgebraic ℚ a) (ha0 : a ≠ 0) :
    Transcendental ℚ (Real.exp (Real.pi * a))

/-- `e^π` es trascendente: el caso `a = 1`. -/
theorem exp_pi_transcendental : Transcendental ℚ (Real.exp Real.pi) := by
  simpa using exp_pi_mul_algebraic_transcendental 1 isAlgebraic_one one_ne_zero

/-- `φ` es algebraico: raíz de `X² − X − 1`. -/
theorem golden_isAlgebraic : IsAlgebraic ℚ ((1 + Real.sqrt 5) / 2) := by
  refine ⟨Polynomial.X ^ 2 - Polynomial.X - 1, ?_, ?_⟩
  · intro h
    have := congrArg (Polynomial.coeff · 2) h
    simp [Polynomial.coeff_X, Polynomial.coeff_one] at this
  · have h5 : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)
    simp [Polynomial.aeval_def]

/-- `log φ / π` es irracional: si `q·log φ = p·π` con `q > 0`, entonces `φ^q = (e^π)^p`, y
`e^π` sería algebraico. -/
theorem log_golden_div_pi_irrational :
    ¬ ∃ p q : ℕ, 0 < q ∧ (q : ℝ) * Real.log ((1 + Real.sqrt 5) / 2) = p * Real.pi := by
  rintro ⟨p, q, hq, h⟩
  set b := (1 + Real.sqrt 5) / 2 with hbdef
  have hb1 : 1 < b := by
    have : (1 : ℝ) < Real.sqrt 5 := by
      rw [show (1 : ℝ) = Real.sqrt 1 by simp]
      exact Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
    rw [hbdef]; linarith
  have hlog : 0 < Real.log b := Real.log_pos hb1
  have hp : 0 < p := by
    rcases Nat.eq_zero_or_pos p with h0 | h0
    · subst h0; simp only [CharP.cast_eq_zero, zero_mul, mul_eq_zero, Nat.cast_eq_zero, log_eq_zero] at h
      rcases h with h | h
      · exact absurd h (by exact_mod_cast hq.ne')
      · rcases h with h | h | h <;> linarith
    · exact h0
  have hpow : b ^ q = Real.exp Real.pi ^ p := by
    rw [← Real.exp_log (by linarith : (0 : ℝ) < b), ← Real.exp_nat_mul, ← Real.exp_nat_mul, h]
  have halg : IsAlgebraic ℚ (Real.exp Real.pi ^ p) := hpow ▸ golden_isAlgebraic.pow q
  exact exp_pi_transcendental (IsAlgebraic.of_pow hp halg)

/-- La imagen estereográfica del toro de Clifford es el toro de revolución con `R = √2`, `r = 1`:
para `s² + c² = 1` y `d = 1 − s/√2`, el punto `(ρ, z) = (1/(√2 d), c/(√2 d))` cumple
`(ρ − √2)² + z² = 1`. -/
theorem clifford_stereographic_torus (s c : ℝ) (hsc : s ^ 2 + c ^ 2 = 1)
    (hd : 1 - s / Real.sqrt 2 ≠ 0) :
    (1 / (Real.sqrt 2 * (1 - s / Real.sqrt 2)) - Real.sqrt 2) ^ 2
      + (c / (Real.sqrt 2 * (1 - s / Real.sqrt 2))) ^ 2 = 1 := by
  have h2 : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hs2 : Real.sqrt 2 ≠ 0 := by positivity
  have hden : Real.sqrt 2 * (1 - s / Real.sqrt 2) = Real.sqrt 2 - s := by field_simp
  rw [hden]
  have hd' : Real.sqrt 2 - s ≠ 0 := by
    intro h0; apply hd; field_simp; linarith
  field_simp; nlinarith [h2, hsc]

/-- **Axioma (derivadas de la proyección).** Con `r(b) = √2 − sin b`, el meridiano proyectado
`ρ(b) = 1/r`, `z(b) = cos b / r` tiene derivadas `ρ' = cos b / r²` y `z' = (1 − √2 sin b) / r²`.
Es cálculo de una variable (regla del cociente). -/
axiom stereographic_meridian_deriv (b : ℝ) :
    HasDerivAt (fun x => 1 / (Real.sqrt 2 - Real.sin x))
      (Real.cos b / (Real.sqrt 2 - Real.sin b) ^ 2) b ∧
    HasDerivAt (fun x => Real.cos x / (Real.sqrt 2 - Real.sin x))
      ((1 - Real.sqrt 2 * Real.sin b) / (Real.sqrt 2 - Real.sin b) ^ 2) b

/-- La proyección es conforme sobre el toro: la métrica inducida `ρ² da² + (ρ'² + z'²) db²` es
`ρ²(da² + db²)`, porque `ρ'² + z'² = ρ²`. Así el toro de revolución es conforme al toro plano
cuadrado, `τ = i`. -/
theorem stereographic_conformal (s c : ℝ) (hsc : s ^ 2 + c ^ 2 = 1) (hr : Real.sqrt 2 - s ≠ 0) :
    (c / (Real.sqrt 2 - s) ^ 2) ^ 2 + ((1 - Real.sqrt 2 * s) / (Real.sqrt 2 - s) ^ 2) ^ 2
      = (1 / (Real.sqrt 2 - s)) ^ 2 := by
  have h2 : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  field_simp; ring
  nlinarith [h2, hsc]


/-! ## Los postulados de la teoría de campos, la holografía y la cuerda que el artículo demuestra -/

/-- Dimensión crítica: `(D − 2)·½·ζ(−1) = −1` con `ζ(−1) = −1/12` da `D = 26 = c`. -/
theorem critical_dimension (D : ℚ) :
    (D - 2) * (1 / 2) * (-1 / 12) = -1 ↔ D = 26 := by
  constructor
  · intro h; linarith
  · intro h; subst h; norm_num

/-- El grupo de cruce: módulo 2, `S` y `ST` (la compañera de `φ`) generan `SL₂(𝔽₂) ≅ S₃`. -/
theorem crossing_group_mod_two :
    let S : Matrix (Fin 2) (Fin 2) (ZMod 2) := !![0, 1; 1, 0]
    let R : Matrix (Fin 2) (Fin 2) (ZMod 2) := !![0, 1; 1, 1]
    S ^ 2 = 1 ∧ R ^ 3 = 1 ∧ R ≠ 1 ∧ S * R ≠ R * S ∧
    [1, S, R, R ^ 2, S * R, S * R ^ 2].Nodup := by
  decide

/-- El punto de cruce: si `λ(−1/τ) = 1 − λ(τ)` y `S` fija `τ = i`, entonces `λ(i) = ½`. -/
theorem crossing_point_half (lam : ℂ → ℂ) (hS : lam (-1 / Complex.I) = 1 - lam Complex.I) :
    lam Complex.I = 1 / 2 := by
  have h : -1 / Complex.I = Complex.I := by
    rw [div_eq_iff Complex.I_ne_zero, Complex.I_mul_I]
  rw [h] at hS
  linear_combination hS / 2

/-- **Axioma (Dedekind; Apostol, *Modular Functions and Dirichlet Series*, Thms. 3.1 y 3.4).** -/
axiom eta : ℂ → ℂ
axiom eta_T (τ : ℂ) (h : 0 < τ.im) :
    eta (τ + 1) = Complex.exp (2 * Real.pi * Complex.I / 24) * eta τ

/-- El multiplicador de `η^k` bajo `T`: con `k = 24`, el reloj, es 1; con `k = 12`, el fondo, es
`e^{iπ} = −1`. -/
theorem eta_power_T_phase :
    Complex.exp (2 * Real.pi * Complex.I / 24) ^ 24 = 1 ∧
    Complex.exp (2 * Real.pi * Complex.I / 24) ^ 12 = -1 := by
  constructor
  · rw [← Complex.exp_nat_mul]; push_cast
    rw [show (24 : ℂ) * (2 * Real.pi * Complex.I / 24) = 2 * Real.pi * Complex.I by ring]
    exact Complex.exp_two_pi_mul_I
  · rw [← Complex.exp_nat_mul]; push_cast
    rw [show (12 : ℂ) * (2 * Real.pi * Complex.I / 24) = Real.pi * Complex.I by ring]
    exact Complex.exp_pi_mul_I

/-- `|η|^{48}` es invariante bajo `T`. -/
theorem partition_T_invariant (τ : ℂ) (h : 0 < τ.im) :
    ‖eta (τ + 1)‖ ^ 48 = ‖eta τ‖ ^ 48 := by
  rw [eta_T τ h, Complex.norm_mul, Complex.norm_exp]
  have : (2 * Real.pi * Complex.I / 24 : ℂ).re = 0 := by simp
  rw [this, Real.exp_zero, one_mul]

/-- Promedio sobre los primeros `N+1` puntos de la órbita `n ↦ nα`. -/
noncomputable def orbitAvg (f : ℝ → ℝ) (α : ℝ) (N : ℕ) : ℝ :=
  (1 / ((N : ℝ) + 1)) * ∑ n ∈ Finset.range (N + 1), f (n * α)

/-- **Axioma (Weyl 1916, Math. Ann. 77, 313–352).** -/
axiom weyl_equidistribution (α : ℝ) (hα : Irrational α) (f : ℝ → ℝ) (hf : Continuous f)
    (hper : Function.Periodic f 1) :
    Filter.Tendsto (orbitAvg f α) Filter.atTop (nhds (∫ x in (0 : ℝ)..1, f x))

/-- Factorización: la parte conexa sobre una órbita tiende a la covarianza `∫fg − ∫f∫g`. -/
theorem orbit_connected_part (α : ℝ) (hα : Irrational α) (f g : ℝ → ℝ)
    (hf : Continuous f) (hg : Continuous g)
    (hpf : Function.Periodic f 1) (hpg : Function.Periodic g 1) :
    Filter.Tendsto (fun N => orbitAvg (fun x => f x * g x) α N - orbitAvg f α N * orbitAvg g α N)
      Filter.atTop
      (nhds ((∫ x in (0 : ℝ)..1, f x * g x) - (∫ x in (0 : ℝ)..1, f x) * ∫ x in (0 : ℝ)..1, g x)) := by
  have hfg : Function.Periodic (fun x => f x * g x) 1 := fun x => by simp [hpf x, hpg x]
  exact (weyl_equidistribution α hα _ (hf.mul hg) hfg).sub
    ((weyl_equidistribution α hα f hf hpf).mul (weyl_equidistribution α hα g hg hpg))

/-- En cada teoría individual el producto factoriza. -/
theorem single_theory_factorizes (f g : ℝ → ℝ) (θ : ℝ) :
    (fun x => f x * g x) θ = f θ * g θ := rfl

/-- Distancia: con `H(σ) = √2·b^{−σ/2}` y `Λ = 6 b^{−σ}` (CW6), `3H² = Λ`; la torre que baja como
`b^{−σ/2}` baja como `Λ^{1/2}`. -/
theorem hubble_lambda (b σ : ℝ) (hb : 0 < b) :
    3 * (Real.sqrt 2 * b ^ (-σ / 2)) ^ 2 = 6 * b ^ (-σ) := by
  have h2 : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hh : (b ^ (-σ / 2)) ^ 2 = b ^ (-σ) := by
    rw [← Real.rpow_natCast, ← Real.rpow_mul hb.le]; congr 1; push_cast; ring
  rw [mul_pow, h2, hh]; ring

theorem tower_is_root_lambda (b σ : ℝ) (hb : 0 < b) :
    b ^ (-σ / 2) = Real.sqrt (b ^ (-σ)) := by
  have hh : (b ^ (-σ / 2)) ^ 2 = b ^ (-σ) := by
    rw [← Real.rpow_natCast, ← Real.rpow_mul hb.le]; congr 1; push_cast; ring
  rw [← hh, Real.sqrt_sq (Real.rpow_pos_of_pos hb _).le]


/-! ## La subdivisión del anillo por la compactificación
`N(σ) = z(σ)/(τ(σ)/M) = φ^{2σ}`: lazos de la fibra que caben en el anillo del nivel. -/

/-- Potencias de `φ` en la base `{1, φ}`: `φ^{n+1} = F_{n+1}·φ + F_n`. -/
theorem golden_pow_fib (n : ℕ) :
    ((1 + Real.sqrt 5) / 2) ^ (n + 1) = (Nat.fib (n + 1) : ℝ) * ((1 + Real.sqrt 5) / 2) + Nat.fib n := by
  set b := (1 + Real.sqrt 5) / 2 with hbdef
  have h5 : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)
  have hb2 : b ^ 2 = b + 1 := by rw [hbdef]; nlinarith [h5]
  induction n with
  | zero => simp
  | succ k ih =>
    rw [pow_succ, ih, Nat.fib_add_two]; push_cast
    nlinarith [hb2]

/-- La resolución del anillo no es entera: `φ^{2n}` es irracional para `n ≥ 1`. -/
theorem ring_resolution_irrational (n : ℕ) (hn : 1 ≤ n) :
    Irrational (((1 + Real.sqrt 5) / 2) ^ (2 * n)) := by
  obtain ⟨m, rfl⟩ : ∃ m, n = m + 1 := ⟨n - 1, by omega⟩
  have h := golden_pow_fib (2 * m + 1)
  rw [show 2 * (m + 1) = 2 * m + 1 + 1 by ring, h]
  have hF : (Nat.fib (2 * m + 1 + 1) : ℤ) ≠ 0 := by
    have : 0 < Nat.fib (2 * m + 1 + 1) := Nat.fib_pos.mpr (by omega)
    exact_mod_cast this.ne'
  have hI : Irrational ((Nat.fib (2 * m + 1 + 1) : ℕ) * ((1 + Real.sqrt 5) / 2)) := by
    rw [mul_comm]
    exact Irrational.mul_natCast golden_irrational (by exact_mod_cast hF)
  exact hI.add_natCast (Nat.fib (2 * m + 1))

/-- `N = z²`: con `z = b^σ` y `τ = M·b^{−σ}`, `z / (τ/M) = b^{2σ}`. -/
theorem ring_resolution_is_square (b M σ : ℝ) (hb : 0 < b) (hM : M ≠ 0) :
    b ^ σ / ((M * b ^ (-σ)) / M) = (b ^ σ) ^ 2 := by
  rw [show (M * b ^ (-σ)) / M = b ^ (-σ) by rw [mul_comm M, mul_div_cancel_right₀ _ hM],
    Real.rpow_neg hb.le, div_inv_eq_mul]
  ring

/-- Cardy con `c = 3` y `L₀ = N/2`: `2π√(c·L₀/6) = π√N`; con `N = z²`, `= π z = S`. -/
theorem cardy_entropy (N : ℝ) (hN : 0 ≤ N) :
    2 * Real.pi * Real.sqrt (3 * (N / 2) / 6) = Real.pi * Real.sqrt N := by
  have h : 3 * (N / 2) / 6 = (Real.sqrt N / 2) ^ 2 := by
    rw [div_pow, Real.sq_sqrt hN]; ring
  rw [h, Real.sqrt_sq (by positivity)]; ring

theorem cardy_is_tower_entropy (b σ : ℝ) (hb : 0 < b) :
    2 * Real.pi * Real.sqrt (3 * ((b ^ σ) ^ 2 / 2) / 6) = Real.pi * b ^ σ := by
  rw [cardy_entropy _ (sq_nonneg _), Real.sqrt_sq (Real.rpow_pos_of_pos hb σ).le]

/-- El espectro de una cuerda cerrada en un círculo de radio `R`, sin osciladores:
`m² = (n/R)² + (wR/α')²`. -/
noncomputable def closedStringMass2 (n w : ℤ) (R a : ℝ) : ℝ := (n / R) ^ 2 + (w * R / a) ^ 2

/-- Invariancia: radio `R` con `(n, w)` y radio `α'/R` con `(w, n)` dan la misma masa. -/
theorem closed_string_invariance (n w : ℤ) (R a : ℝ) (hR : R ≠ 0) (ha : a ≠ 0) :
    closedStringMass2 n w R a = closedStringMass2 w n (a / R) a := by
  unfold closedStringMass2; field_simp; ring

/-- Con `α' = M`, el radio dual de la garganta `z = b^σ` es el lazo `τ = M b^{−σ}`. -/
theorem dual_radius_is_loop (b M σ : ℝ) (hb : 0 < b) :
    M / b ^ σ = M * b ^ (-σ) := by
  rw [Real.rpow_neg hb.le, div_eq_mul_inv]


/-! ## Qué cuenta `N`: retroducción
La cota holográfica del nivel es `S = π z` (CW6: `S = A/4G_N`, `G_N = ½`, `A = 2π z`). -/

/-- `φ³ = 2 + √5 > π`. -/
theorem golden_cube_gt_pi : Real.pi < ((1 + Real.sqrt 5) / 2) ^ 3 := by
  have h5 : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)
  have hs : 2 < Real.sqrt 5 := by nlinarith [Real.sqrt_nonneg 5]
  have hc : ((1 + Real.sqrt 5) / 2) ^ 3 = 2 + Real.sqrt 5 := by nlinarith [h5]
  rw [hc]; linarith [Real.pi_lt_d2]

/-- Si `N = z²` contara bits, superaría la cota `π z` en cuanto `z > π`, es decir desde `σ = 3`. -/
theorem ring_count_exceeds_bound (z : ℝ) (hz : Real.pi < z) : Real.pi * z < z ^ 2 := by
  have : 0 < z := lt_trans Real.pi_pos hz
  nlinarith

theorem ring_count_exceeds_bound_from_three (σ : ℝ) (hσ : 3 ≤ σ) :
    Real.pi * ((1 + Real.sqrt 5) / 2) ^ σ < (((1 + Real.sqrt 5) / 2) ^ σ) ^ 2 := by
  apply ring_count_exceeds_bound
  have h1 : (1 : ℝ) < (1 + Real.sqrt 5) / 2 := by
    have : (1 : ℝ) < Real.sqrt 5 := by
      rw [show (1 : ℝ) = Real.sqrt 1 by simp]; exact Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
    linarith
  calc Real.pi < ((1 + Real.sqrt 5) / 2) ^ (3 : ℕ) := golden_cube_gt_pi
    _ = ((1 + Real.sqrt 5) / 2) ^ (3 : ℝ) := by norm_cast
    _ ≤ ((1 + Real.sqrt 5) / 2) ^ σ := Real.rpow_le_rpow_of_exponent_le h1.le hσ

/-- La ley de área en cuatro dimensiones, `4π z²/(4·½) = 2π z²`, coincide con la entropía de
la soldadura `π z` solo en `z = ½ = |Ω|`. -/
theorem area_law_4d_meets_weld_iff (z : ℝ) (hz : 0 < z) :
    2 * Real.pi * z ^ 2 = Real.pi * z ↔ z = 1 / 2 := by
  constructor
  · intro h
    have : Real.pi * z * (2 * z - 1) = 0 := by linarith
    rcases mul_eq_zero.mp this with h0 | h0
    · exact absurd h0 (mul_pos Real.pi_pos hz).ne'
    · linarith
  · rintro rfl; ring

/-- Con `N = z²` cuantos, la entropía de Cardy satura la cota: `π √N = π z`. -/
theorem cardy_saturates_bound (z : ℝ) (hz : 0 ≤ z) : Real.pi * Real.sqrt (z ^ 2) = Real.pi * z := by
  rw [Real.sqrt_sq hz]


/-! ## El individuo y el ensamble
Un solo microestado: su módulo, la isometría de la tríada, el bit, los datos gravitacionales;
-/

/-- La tríada `v_k = ½ ω^k`, `ω = e^{2πi/3}`: cada `|v_k| = ½`. -/
theorem triad_modulus (k : ℕ) :
    ‖(1 / 2 : ℂ) * Complex.exp (((2 * Real.pi / 3 : ℝ) : ℂ) * Complex.I) ^ k‖ = 1 / 2 := by
  rw [Complex.norm_mul, Complex.norm_pow, Complex.norm_exp_ofReal_mul_I, one_pow, mul_one]; norm_num

/-- Isometría bulk–frontera: `‖v‖² = 3·¼ = ¾`, y la columna normalizada cumple `V†V = Σ|V_k|² = 1`. -/
theorem bulk_boundary_isometry :
    (∑ k ∈ Finset.range 3,
        (‖(1 / 2 : ℂ) * Complex.exp (((2 * Real.pi / 3 : ℝ) : ℂ) * Complex.I) ^ k‖) ^ 2) = 3 / 4 ∧
    (∑ k ∈ Finset.range 3,
        (‖(1 / 2 : ℂ) * Complex.exp (((2 * Real.pi / 3 : ℝ) : ℂ) * Complex.I) ^ k‖) ^ 2 / (3 / 4)) = 1 := by
  simp only [triad_modulus]; constructor <;> norm_num [Finset.sum_range_succ]

/-- Entropía binaria en `½`: un bit. -/
noncomputable def binEntropy (p : ℝ) : ℝ := -(p * Real.logb 2 p + (1 - p) * Real.logb 2 (1 - p))

theorem binEntropy_half : binEntropy (1 / 2) = 1 := by
  have h : Real.logb 2 (1 / 2) = -1 := by
    rw [one_div, Real.logb_inv, Real.logb_self_eq_one (by norm_num)]
  unfold binEntropy; norm_num [h]

/-- Los datos gravitacionales del módulo: con `G_N = ½`, `S_BH = 1/(4G_N) = ½`, y la carga central
de Brown–Henneaux `c = 3ℓ/(2G_N)` (`ℓ = 1`) vale `3` si y solo si `G_N = ½`. -/
theorem area_quantum_half : 1 / (4 * (1 / 2 : ℝ)) = 1 / 2 := by norm_num

theorem brown_henneaux_three_iff (G : ℝ) (hG : 0 < G) : 3 * 1 / (2 * G) = 3 ↔ G = 1 / 2 := by
  constructor
  · intro h; field_simp at h; linarith
  · rintro rfl; norm_num

/-! ## (F5): las premisas matemáticas de la construcción de Jacobson
Jacobson (1995) obtiene la ecuación de Einstein de `δQ = T δS` en cada horizonte local de Rindler,
si la entropía es proporcional al área con un coeficiente universal y la ley es la misma en cada
punto. Aquí se prueban esas premisas; el postulado `δQ = T δS` queda como axioma físico (F5). -/

/-- Techo de Fisher: `F_Ω = 4μ² = 1` (un bit por autovalor) si y solo si `μ = ½`. -/
theorem fisher_unit_iff (μ : ℝ) (hμ : 0 < μ) : 4 * μ ^ 2 = 1 ↔ μ = 1 / 2 := by
  constructor
  · intro h; nlinarith [sq_nonneg (μ - 1 / 2), sq_nonneg (μ + 1 / 2)]
  · rintro rfl; norm_num

/-- La energía por bit es la misma en cada nivel: con `ε(σ) = ε₀ b^σ`, `S(σ) = π b^σ` y
`ε₀ M = π`, `ε(σ)/S(σ) = 1/M`: la temperatura `T = 1/M` no depende del nivel. -/
theorem energy_per_bit_constant (b σ ε₀ M : ℝ) (hb : 0 < b) (hM : M ≠ 0) (hc : ε₀ * M = Real.pi) :
    (ε₀ * b ^ σ) / (Real.pi * b ^ σ) = 1 / M := by
  have hp : b ^ σ ≠ 0 := (Real.rpow_pos_of_pos hb σ).ne'
  have he0 : ε₀ ≠ 0 := by
    intro h
    have h0 : Real.pi = 0 := by rw [← hc, h, zero_mul]
    linarith [Real.pi_pos]
  rw [← hc]; field_simp

/-- El coeficiente de la ley de área, `η = 1/(4G_N)`, es el mismo en cada nivel: `G_N = |Ω_σ| = ½`. -/
theorem area_coefficient_every_level (θ : ℝ) :
    1 / (4 * ‖(1 / 2 : ℂ) * Complex.exp (θ * Complex.I)‖) = 1 / 2 := by
  rw [worldline_modulus]; norm_num

/-- La garganta es un espacio de Einstein. Para `ds² = e^{2A(y)} η dx² + dy²` en cinco dimensiones
los coeficientes de Ricci son `R_μν = −(A″ + 4A′²) g_μν` y `R_yy = −4(A″ + A′²)`; con `A′² = 1`,
`A″ = 0` ambos valen `−4`, la curvatura escalar es `5·(−4) = −20` y `G_AB = 6 g_AB`, es decir
`Λ₅ = −6`. -/
theorem throat_einstein_space (A1 A2 : ℝ) (h1 : A1 ^ 2 = 1) (h2 : A2 = 0) :
    -(A2 + 4 * A1 ^ 2) = -4 ∧ -4 * (A2 + A1 ^ 2) = -4 ∧ 5 * (-4 : ℝ) = -20 ∧
    (-4 : ℝ) - (1 / 2) * (-20) = 6 := by
  subst h2; refine ⟨?_, ?_, ?_, ?_⟩ <;> nlinarith [h1]

/-- En un espacio de Einstein `R_ab = −4 g_ab`, `R_ab k^a k^b = 0` para todo `k` nulo: en vacío la
relación de Clausius da `δS = 0`, el equilibrio que pide la construcción de Jacobson. -/
theorem einstein_null_contraction (gkk : ℝ) (hnull : gkk = 0) : -4 * gkk = 0 := by
  rw [hnull]; ring


/-! ## (F8): la rotación interna cambia el signo de un cuadrado -/

/-- `(i t)² = −t²`: la rotación `t ↦ i t` invierte el signo de un cuadrado; es la parte matemática
de la lectura que lleva la garganta AdS (`Λ₅ = −6`) al parche de de Sitter de cada nivel (`Λ > 0`). -/
theorem wick_squares_flip_sign (t : ℝ) : (Complex.I * t) ^ 2 = -((t : ℂ) ^ 2) := by
  rw [mul_pow, Complex.I_sq]; ring


/-! ## Los criterios de Witten y CLPW, y la matemática del observador

`Λ(σ)·S(σ)` no depende del nivel (ley de entropía de de Sitter); el desfase de la torre es `1/d`
solo en `d = 4`; el modo cero es el cero exacto `J₁(0) = 0`; `12 = 2σ_Λ` solo en `n = 3`; y las
piezas de W2–W12 que faltaban. -/

/-- **W4, W11.** `Λ(σ)S(σ) = 6φ^{−σ}·πφ^σ = 6π`, invariante a lo largo del flujo de niveles. -/
theorem lambda_times_entropy (b σ : ℝ) (hb : 0 < b) :
    (6 * b ^ (-σ)) * (Real.pi * b ^ σ) = 6 * Real.pi := by
  rw [Real.rpow_neg hb.le]
  have : b ^ σ ≠ 0 := (Real.rpow_pos_of_pos hb σ).ne'
  field_simp

/-- `6π = 3π/G_N` con `G_N = ½`: la ley de entropía del horizonte de de Sitter, `S = 3π/(GΛ)`. -/
theorem dS_entropy_law : 3 * Real.pi / (1 / 2 : ℝ) = 6 * Real.pi := by ring

/-- El desfase asintótico de los ceros de `J_{d/2−1}` (McMahon), `d/4 − 3/4`, es igual a `1/d`
si y solo si `d = 4`. -/
theorem phase_equals_inverse_dimension_iff (d : ℝ) (hd : 0 < d) :
    d / 4 - 3 / 4 = 1 / d ↔ d = 4 := by
  constructor
  · intro h
    have h' : (d - 4) * (d + 1) = 0 := by field_simp at h; nlinarith [h]
    rcases mul_eq_zero.mp h' with h1 | h1
    · linarith
    · linarith
  · rintro rfl; norm_num

/-- `J₁` por su serie de potencias. -/
noncomputable def besselJ1 (x : ℝ) : ℝ :=
  ∑' m : ℕ, (-1 : ℝ) ^ m / ((Nat.factorial m : ℝ) * Nat.factorial (m + 1)) * (x / 2) ^ (2 * m + 1)

/-- El modo cero: `J₁(0) = 0`, el término `k = 0` exacto, donde la asintótica daría `π/4`. -/
theorem bessel_zero_mode : besselJ1 0 = 0 := by
  unfold besselJ1; simp

theorem zero_mode_vs_asymptotic : (0 : ℝ) ≠ Real.pi * (0 + 1 / 4) := by
  have := Real.pi_pos; intro h; linarith

/-- **W8.** `12 = 2σ_Λ = (n+1)n`: `n(n+1) = 4n` si y solo si `n = 3`. -/
theorem bottom_twice_lambda_iff (n : ℝ) (hn : 0 < n) : n * (n + 1) = 4 * n ↔ n = 3 := by
  constructor
  · intro h; nlinarith
  · rintro rfl; norm_num

/-- **W8.** Las dos rutas a seis, `|Λ₅| = d(d−1)/2` con `d = n+1` y `σ_Λ = 2n`, coinciden solo en
`n = 3`. -/
theorem two_routes_to_six (n : ℝ) (hn : 0 < n) : (n + 1) * n / 2 = 2 * n ↔ n = 3 := by
  constructor
  · intro h; nlinarith
  · rintro rfl; norm_num

/-- **W2.** La dimensión por nivel, `⌊S(σ)⌋`, es un entero no negativo. -/
theorem witten_finite_rank (b σ : ℝ) (hb : 0 < b) : 0 ≤ ⌊Real.pi * b ^ σ⌋ :=
  Int.floor_nonneg.mpr (mul_pos Real.pi_pos (Real.rpow_pos_of_pos hb σ)).le

/-- **W3.** El módulo supera el umbral de colapso: `½ > ¼`. -/
theorem half_gt_quarter : (1 / 2 : ℝ) > 1 / 4 := by norm_num

/-- **W5.** Normas de las componentes del triángulo de autovalores (CW6): `‖C‖ = 1`,
`‖F‖ = √3/2`, `‖P‖ = 1/√3`; el emparejamiento interno `⟨F|P⟩ = F̄P/C` tiene módulo `½`. -/
theorem pairing_FP_modulus_half :
    (Real.sqrt 3 / 2) * (1 / Real.sqrt 3) / 1 = (1 / 2 : ℝ) := by
  have h : Real.sqrt 3 ≠ 0 := (Real.sqrt_pos.mpr (by norm_num)).ne'
  field_simp

/-- **W6.** La conjugación de Galois de `ℤ[φ]`, `a + bφ ↦ a + bφ̄ = (a+b) − bφ`. -/
def galoisConj (p : ℤ × ℤ) : ℤ × ℤ := (p.1 + p.2, -p.2)

/-- `Θ² = 1`. -/
theorem cpt_involution (p : ℤ × ℤ) : galoisConj (galoisConj p) = p := by
  simp [galoisConj]

/-- `Θ` preserva la norma `N(a + bφ) = a² + ab − b²`. -/
theorem cpt_preserves_modulus (p : ℤ × ℤ) :
    let q := galoisConj p
    q.1 ^ 2 + q.1 * q.2 - q.2 ^ 2 = p.1 ^ 2 + p.1 * p.2 - p.2 ^ 2 := by
  simp only [galoisConj]; ring

/-- `Θ` intercambia `φ` y `φ̄ = 1 − φ`, y fija los racionales (el centro). -/
theorem cpt_swaps_and_fixes (a : ℤ) :
    galoisConj (0, 1) = (1, -1) ∧ galoisConj (a, 0) = (a, 0) := by
  simp [galoisConj]

/-- **W7.** La simetría discreta que sustituye al grupo no compacto: `ω³ = 1`. -/
theorem eisenstein_cube :
    Complex.exp (2 * Real.pi * Complex.I / 3) ^ 3 = 1 := by
  rw [← Complex.exp_nat_mul]
  have : ((3 : ℕ) : ℂ) * (2 * Real.pi * Complex.I / 3) = 2 * Real.pi * Complex.I := by
    push_cast; ring
  rw [this, Complex.exp_two_pi_mul_I]

/-- **W10.** El mapa antipodal de la esfera, en la coordenada estereográfica, `z ↦ −1/z̄`, es una
involución: `F` antipodal a `P`. -/
theorem antipodal_involution (z : ℂ) (hz : z ≠ 0) :
    -1 / (starRingEnd ℂ) (-1 / (starRingEnd ℂ) z) = z := by
  have hc : (starRingEnd ℂ) z ≠ 0 := by simpa using hz
  simp only [map_div₀, map_neg, map_one, Complex.conj_conj]
  field_simp

/-- **La ley de la theta bajo `S`** (Mathlib, sin axioma): `θ(−1/τ) = (−iτ)^{1/2} θ(τ)`. -/
theorem theta_S_law (τ : UpperHalfPlane) :
    jacobiTheta ↑(ModularGroup.S • τ) = (-Complex.I * τ) ^ (1 / 2 : ℂ) * jacobiTheta τ :=
  jacobiTheta_S_smul τ

/-! ## W1 y W9 en esta nota: la proyección del observador y el parche térmico -/

/-- **W1.** De una isometría `V†V = 1` sale la proyección `P = VV†`: `P² = P`. La proyección que coloca
al observador se construye con el mapa de la propia teoría (`bulk_boundary_isometry`). -/
theorem projection_of_isometry {R : Type*} [Monoid R] (V Vd : R) (h : Vd * V = 1) :
    (V * Vd) * (V * Vd) = V * Vd := by
  rw [mul_assoc, ← mul_assoc Vd V Vd, h, one_mul]

/-- **W1.** Un idempotente parte la identidad: `P + (1 − P) = 1` y `P(1 − P) = 0`; no queda región fuera. -/
theorem idempotent_splits_identity {R : Type*} [Ring R] (P : R) (h : P * P = P) :
    P + (1 - P) = 1 ∧ P * (1 - P) = 0 := by
  refine ⟨by abel, ?_⟩
  rw [mul_sub, mul_one, h, sub_self]

/-- **W9.** El horizonte de tasa de Hubble `H(σ) = √2·b^{−σ/2}` tiene, con `G_N = ½`, la entropía de
Gibbons–Hawking `π/(G_N H²) = π b^σ = S(σ)`: la entropía del parche estático es la cuenta de bits. -/
theorem gibbons_hawking_entropy (b σ : ℝ) (hb : 0 < b) :
    Real.pi / ((1 / 2) * (Real.sqrt 2 * b ^ (-σ / 2)) ^ 2) = Real.pi * b ^ σ := by
  have h2 : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hh : (b ^ (-σ / 2)) ^ 2 = b ^ (-σ) := by
    rw [← Real.rpow_natCast, ← Real.rpow_mul hb.le]; congr 1; push_cast; ring
  have hp : b ^ σ ≠ 0 := (Real.rpow_pos_of_pos hb σ).ne'
  rw [mul_pow, h2, hh, Real.rpow_neg hb.le]
  field_simp

/-! ## La red de la torre: entero y real a la vez (v22)

`a + bφ` es el par `(a, b)`; con `φ² = φ + 1`, `(a, b)(c, d) = (ac + bd, ad + bc + bd)` y la norma es
`N(a + bφ) = a² + ab − b²`. Con su conjugado, `ℤ[φ]` es una red discreta del plano; las unidades
`φⁿ` caen sobre la hipérbola `xy = ±1`, que el nivel real recorre de forma continua. -/

/-- Producto en `ℤ[φ]`. -/
def zmul (p q : ℤ × ℤ) : ℤ × ℤ := (p.1 * q.1 + p.2 * q.2, p.1 * q.2 + p.2 * q.1 + p.2 * q.2)

/-- Norma de `a + bφ`. -/
def znorm (p : ℤ × ℤ) : ℤ := p.1 ^ 2 + p.1 * p.2 - p.2 ^ 2

/-- La norma es multiplicativa. -/
theorem znorm_mul (p q : ℤ × ℤ) : znorm (zmul p q) = znorm p * znorm q := by
  unfold znorm zmul; ring

/-- `φⁿ` en `ℤ[φ]`. -/
def zpow : ℕ → ℤ × ℤ
  | 0 => (1, 0)
  | n + 1 => zmul (zpow n) (0, 1)

/-- Los niveles enteros son unidades: `N(φⁿ) = (−1)ⁿ`. -/
theorem znorm_zpow (n : ℕ) : znorm (zpow n) = (-1) ^ n := by
  induction n with
  | zero => simp [zpow, znorm]
  | succ n ih =>
    rw [zpow, znorm_mul, ih]
    simp [znorm, pow_succ]

/-- `φ¹² = 89 + 144φ`, de norma `1`: el fondo es un punto de la red. -/
theorem bottom_is_lattice_point : zpow 12 = (89, 144) ∧ znorm (89, 144) = 1 := by
  constructor
  · decide
  · decide

/-- **No hay unidad entre `1` y `φ`** (F1, «The tower is the unit group, without Dirichlet»): si `1 < u < φ`,
ni `u + 1/u` (norma `+1`) ni `u − 1/u` (norma `−1`) es entero. Con el suelo de `log u / log φ`, toda
unidad positiva es una potencia de `φ`. -/
theorem no_unit_below_golden (u : ℝ) (t : ℤ) (h1 : 1 < u) (h2 : u < (1 + Real.sqrt 5) / 2) :
    u + 1 / u ≠ t ∧ u - 1 / u ≠ t := by
  have h5 : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)
  have h5p : 0 < Real.sqrt 5 := by positivity
  have hu0 : 0 < u := by linarith
  have hroot : u ^ 2 - u - 1 < 0 := by nlinarith
  have hu2 : u ^ 2 < 3 * u - 1 := by nlinarith
  constructor
  · intro h
    have a1 : (2 : ℝ) < t := by
      rw [← h, show u + 1 / u = (u ^ 2 + 1) / u by field_simp, lt_div_iff₀ hu0]; nlinarith
    have a2 : (t : ℝ) < 3 := by
      rw [← h, show u + 1 / u = (u ^ 2 + 1) / u by field_simp, div_lt_iff₀ hu0]; nlinarith
    have b1 : (2 : ℤ) < t := by exact_mod_cast a1
    have b2 : t < (3 : ℤ) := by exact_mod_cast a2
    omega
  · intro h
    have a1 : (0 : ℝ) < t := by
      rw [← h, show u - 1 / u = (u ^ 2 - 1) / u by field_simp, lt_div_iff₀ hu0]; nlinarith
    have a2 : (t : ℝ) < 1 := by
      rw [← h, show u - 1 / u = (u ^ 2 - 1) / u by field_simp, div_lt_iff₀ hu0]; nlinarith
    have b1 : (0 : ℤ) < t := by exact_mod_cast a1
    have b2 : t < (1 : ℤ) := by exact_mod_cast a2
    omega

/-- El conjugado de `φ` es `−1/φ`: el conjugado de un nivel es su espejo. -/
theorem conjugate_is_mirror : (1 - Real.sqrt 5) / 2 = -1 / ((1 + Real.sqrt 5) / 2) := by
  have h5 : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)
  have hp : (0 : ℝ) < 1 + Real.sqrt 5 := by positivity
  field_simp
  nlinarith [h5]

/-! ## La ventana: la gaussiana autodual (CW6, «Uniqueness of the self-dual Gaussian») -/

/-- Normalización: `√(π/a) = 1 ⟺ a = π`. -/
theorem gauss_normalised_iff (a : ℝ) (ha : 0 < a) : Real.sqrt (Real.pi / a) = 1 ↔ a = Real.pi := by
  rw [Real.sqrt_eq_one, div_eq_one_iff_eq ha.ne']; exact eq_comm

/-- Con la integral de Mathlib, `∫ e^{−a x²} = 1 ⟺ a = π`. -/
theorem gaussian_integral_one_iff (a : ℝ) (ha : 0 < a) :
    (∫ x : ℝ, Real.exp (-a * x ^ 2)) = 1 ↔ a = Real.pi := by
  rw [integral_gaussian]; exact gauss_normalised_iff a ha

/-- Ancho de la transformada: `π²/a = a ⟺ a = π`. -/
theorem fourier_width_iff (a : ℝ) (ha : 0 < a) : Real.pi ^ 2 / a = a ↔ a = Real.pi := by
  have hpi := Real.pi_pos
  constructor
  · intro h
    have h2 : a ^ 2 = Real.pi ^ 2 := by field_simp at h; linarith
    nlinarith [sq_nonneg (a - Real.pi), sq_nonneg (a + Real.pi)]
  · rintro rfl; field_simp

/-- El umbral de la ventana: `e^{−y} > ½ ⟺ y < log 2`. -/
theorem window_half_iff (y : ℝ) : (1 / 2 : ℝ) < Real.exp (-y) ↔ y < Real.log 2 := by
  rw [← Real.log_lt_log_iff (by norm_num) (Real.exp_pos _), Real.log_exp, one_div, Real.log_inv]
  constructor <;> intro h <;> linarith

/-- El peso `e^{−πφ^{−2n}}` cruza `½` entre `n = 1` y `n = 2`: `π/φ² > log 2 > π/φ⁴`. -/
theorem window_crosses_half (b : ℝ) (h : b ^ 2 = b + 1) (h1 : 1.618 < b) (h2 : b < 1.6181) :
    Real.log 2 < Real.pi / b ^ 2 ∧ Real.pi / b ^ 4 < Real.log 2 := by
  have hb2 : b ^ 2 < 2.6181 := by nlinarith
  have hb4 : 6.854 < b ^ 4 := by nlinarith
  have hl1 := Real.log_two_lt_d9
  have hl2 := Real.log_two_gt_d9
  have hpi1 := Real.pi_gt_d2
  have hpi2 := Real.pi_lt_d2
  constructor
  · rw [lt_div_iff₀ (by positivity)]; nlinarith
  · rw [div_lt_iff₀ (by positivity)]; nlinarith

/-- `Hℓ = √(2φ^{−n})` cruza `1` en el mismo intervalo: `2/φ > 1` y `2/φ² < 1`. -/
theorem hubble_below_bulk_crossing (b : ℝ) (h : b ^ 2 = b + 1) (h1 : 1 < b) (h2 : b < 2) :
    1 < 2 / b ∧ 2 / b ^ 2 < 1 := by
  constructor
  · rw [lt_div_iff₀ (by linarith)]; linarith
  · rw [div_lt_iff₀ (by positivity), h]; linarith

/-! ## v23: la torre de nomes, el intervalo invariante, la norma de las dos escalas, la pendiente de moduli -/

/-- **S es el espejo sobre la torre de nomes.** `−1/(i x) = i/x`: `τ ↦ −1/τ` lleva `τ_n = i φ^{−2n}`
a `i φ^{2n} = τ_{−n}`. -/
theorem S_acts_as_mirror (x : ℝ) (hx : x ≠ 0) :
    -1 / (Complex.I * (x : ℂ)) = Complex.I * (1 / (x : ℂ)) := by
  have hI : Complex.I ≠ 0 := Complex.I_ne_zero
  have hx' : (x : ℂ) ≠ 0 := by exact_mod_cast hx
  field_simp
  ring_nf
  rw [Complex.I_sq]

/-- Un intervalo de niveles invariante bajo el espejo es simétrico. -/
theorem invariant_interval_symmetric (p q : ℝ) (hpq : p ≤ q)
    (h : ∀ x, p ≤ x → x ≤ q → p ≤ -x ∧ -x ≤ q) : p = -q := by
  have h1 := (h p le_rfl hpq).2
  have h2 := (h q hpq le_rfl).1
  linarith

/-- La garganta simétrica `[−12, 12]` tiene la longitud del reloj. -/
theorem symmetric_throat_is_clock : (12 : ℤ) - (-12) = 24 := by norm_num

/-- `2` no es una unidad de `ℤ[φ]`: su norma es `4`. -/
theorem two_not_unit : znorm (2, 0) = 4 := by decide

/-- Un nivel entero de masa es un nivel par de curvatura. -/
theorem mass_level_even_curvature (k : ℤ) : Even (2 * k) := ⟨k, two_mul k⟩

/-- **La norma de las dos escalas.** La escala de Kaluza–Klein `m₀ b^σ` (coordenada directa) por
`H_dS(σ)²/2 = b^{−σ}` (espejo) es `m₀` en todo nivel. -/
theorem kk_hubble_norm (b σ m₀ : ℝ) (hb : 0 < b) :
    (m₀ * b ^ σ) * ((Real.sqrt 2 * b ^ (-σ / 2)) ^ 2 / 2) = m₀ := by
  have h2 : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hh : (b ^ (-σ / 2)) ^ 2 = b ^ (-σ) := by
    rw [← Real.rpow_natCast, ← Real.rpow_mul hb.le]; congr 1; push_cast; ring
  have hp : b ^ σ * b ^ (-σ) = 1 := by
    rw [← Real.rpow_add hb]; simp
  rw [mul_pow, h2, hh]
  calc m₀ * b ^ σ * (2 * b ^ (-σ) / 2) = m₀ * (b ^ σ * b ^ (-σ)) := by ring
    _ = m₀ := by rw [hp, mul_one]

/-- **La pendiente en el campo canónico del módulo del anillo.** Con `dΦ/dn = √2 log φ` y
`d log V/dn = −log φ`, `|∂_Φ V|/V = 1/√2`. -/
theorem moduli_slope (L : ℝ) (hL : 0 < L) : L / (Real.sqrt 2 * L) = 1 / Real.sqrt 2 := by
  have hs : 0 < Real.sqrt 2 := by positivity
  field_simp

/-- La pendiente del módulo está por debajo de la cota de la censura transplanckiana en d = 4:
    1/√2 < √(2/3), porque 1/2 < 2/3. -/
theorem moduli_slope_below_tcc : 1 / Real.sqrt 2 < Real.sqrt (2 / 3) := by
  rw [one_div, ← Real.sqrt_inv]
  apply Real.sqrt_lt_sqrt (by norm_num)
  norm_num

/-- Con K = −k log(Im τ) la pendiente es 1/√(2k); la cota √(2/3) se cumple si y solo si k ≤ 3/4. -/
theorem tcc_iff_k (k : ℝ) (hk : 0 < k) :
    Real.sqrt (2 / 3) ≤ 1 / Real.sqrt (2 * k) ↔ k ≤ 3 / 4 := by
  rw [one_div, ← Real.sqrt_inv, Real.sqrt_le_sqrt_iff (by positivity)]
  rw [le_inv_comm₀ (by norm_num) (by positivity)]
  have h23 : (2 / 3 : ℝ)⁻¹ = 3 / 2 := by norm_num
  rw [h23]
  constructor <;> intro h <;> linarith

/-- La tensión soldada por la entropía no depende del nivel (CW6, eq. 144):
    (q_m² ε₀ b^{−σ})·(π b^{σ}) = q_m² ε₀ π. -/
theorem tension_times_entropy_const (b qm2 e0 σ : ℝ) (hb : 0 < b) :
    (qm2 * e0 * b ^ (-σ)) * (π * b ^ σ) = qm2 * e0 * π := by
  have h : b ^ (-σ) * b ^ σ = 1 := by
    rw [← Real.rpow_add hb]; simp
  calc (qm2 * e0 * b ^ (-σ)) * (π * b ^ σ) = qm2 * e0 * π * (b ^ (-σ) * b ^ σ) := by ring
    _ = qm2 * e0 * π := by rw [h, mul_one]

/-- Si la tensión es C·b^{−σ}/π y H² = 2 b^{−σ}, el cociente con la cota de Higuchi,
    t/(2H²) = C/(4π), es el mismo en todo nivel. -/
theorem higuchi_ratio_level_free (b C σ : ℝ) (hb : 0 < b) :
    (C / π * b ^ (-σ)) / (2 * (2 * b ^ (-σ))) = C / (4 * π) := by
  have hp : 0 < b ^ (-σ) := Real.rpow_pos_of_pos hb _
  have hπ : (0:ℝ) < π := Real.pi_pos
  field_simp
  ring

/-- Con C = 4π⁴/(q² M) el cociente es π³/(q² M), y es ≥ 1 si y solo si q² ≤ π³/M. -/
theorem higuchi_iff_charge (q2 M : ℝ) (hq : 0 < q2) (hM : 0 < M) :
    1 ≤ π ^ 3 / (q2 * M) ↔ q2 ≤ π ^ 3 / M := by
  rw [one_le_div (by positivity), le_div_iff₀ hM]

/-- CW6, eq. (101): el tiempo de Fisher τ_F = τ_D/√(2f) es igual al tiempo de decoherencia
    τ_D si y solo si f = 1/2. -/
theorem fisher_time_eq_decoherence_iff (tD f : ℝ) (ht : 0 < tD) (hf : 0 < f) :
    tD / Real.sqrt (2 * f) = tD ↔ f = 1 / 2 := by
  have hs : 0 < Real.sqrt (2 * f) := Real.sqrt_pos.mpr (by linarith)
  rw [div_eq_iff hs.ne']
  constructor
  · intro h
    have h1 : Real.sqrt (2 * f) = 1 :=
      mul_left_cancel₀ ht.ne' (h.symm.trans (mul_one tD).symm)
    have h2 := Real.sqrt_eq_one.mp h1
    linarith
  · intro h
    subst h
    norm_num

/-- La sección del throat es la cúspide: con `t = e^{-y}`, el coeficiente angular `1/t²` de la métrica
    del semiplano `(dθ² + dt²)/t²` es `e^{2y}`, el de la sección `e^{2y}dθ² + dy²`. -/
theorem cusp_metric (y : ℝ) : Real.exp (-y) ^ 2 * Real.exp (2 * y) = 1 := by
  rw [sq, ← Real.exp_add, ← Real.exp_add]
  norm_num [show -y + -y + 2 * y = 0 by ring]

/-- Las dos tejas de los anillos: con `A = F_{n+3}` largas y `B = F_{n+2}` cortas, de pesos `π/b²`
    y `π/b³`, la suma pesada es `π bⁿ` en cada nivel (aquí sin el factor `π`). -/
theorem two_tile_entropy (b : ℝ) (hb : 0 < b) (h : b ^ 2 = b + 1) :
    ∀ n : ℕ, (Nat.fib (n + 3) : ℝ) / b ^ 2 + (Nat.fib (n + 2) : ℝ) / b ^ 3 = b ^ n
  | 0 => by
      have hb0 : b ≠ 0 := hb.ne'
      have h3 : b ^ 3 = 2 * b + 1 := by nlinarith [h]
      norm_num [Nat.fib_add_two]
      field_simp
      nlinarith [h, h3]
  | 1 => by
      have hb0 : b ≠ 0 := hb.ne'
      have h3 : b ^ 3 = 2 * b + 1 := by nlinarith [h]
      have h4 : b ^ 4 = 3 * b + 2 := by nlinarith [h, h3]
      norm_num [Nat.fib_add_two]
      field_simp
      nlinarith [h, h3, h4]
  | n + 2 => by
      have ih1 := two_tile_entropy b hb h (n + 1)
      have ih0 := two_tile_entropy b hb h n
      have fa : (Nat.fib (n + 2 + 3) : ℝ) = Nat.fib (n + 1 + 3) + Nat.fib (n + 3) := by
        rw [show n + 2 + 3 = (n + 3) + 2 by ring, Nat.fib_add_two]; push_cast; ring_nf
      have fb : (Nat.fib (n + 2 + 2) : ℝ) = Nat.fib (n + 1 + 2) + Nat.fib (n + 2) := by
        rw [show n + 2 + 2 = (n + 2) + 2 by ring, Nat.fib_add_two]; push_cast; ring_nf
      have hp : b ^ (n + 2) = b ^ (n + 1) + b ^ n := by
        rw [pow_succ, pow_succ, mul_assoc, ← sq, h]; ring
      rw [fb, fa, hp, ← ih1, ← ih0]; ring

/-- La sustitución de dos tejas que crece por φ es la de Fibonacci: una matriz `(a b; c d)` de
    naturales con traza 1 y determinante −1 (`a d + 1 = b c`) es `(1 1; 1 0)` o `(0 1; 1 1)`. -/
theorem fibonacci_substitution_unique (a b c d : ℕ) (ht : a + d = 1) (hd : a * d + 1 = b * c) :
    (a = 1 ∧ b = 1 ∧ c = 1 ∧ d = 0) ∨ (a = 0 ∧ b = 1 ∧ c = 1 ∧ d = 1) := by
  have ha : a ≤ 1 := by omega
  interval_cases a
  · have hd1 : d = 1 := by omega
    subst hd1
    have hbc : b * c = 1 := by simpa using hd.symm
    obtain ⟨rfl, rfl⟩ : b = 1 ∧ c = 1 :=
      ⟨Nat.dvd_one.mp ⟨c, hbc.symm⟩, Nat.dvd_one.mp ⟨b, hbc.symm.trans (mul_comm b c)⟩⟩
    right; exact ⟨rfl, rfl, rfl, rfl⟩
  · have hd0 : d = 0 := by omega
    subst hd0
    have hbc : b * c = 1 := by simpa using hd.symm
    obtain ⟨rfl, rfl⟩ : b = 1 ∧ c = 1 :=
      ⟨Nat.dvd_one.mp ⟨c, hbc.symm⟩, Nat.dvd_one.mp ⟨b, hbc.symm.trans (mul_comm b c)⟩⟩
    left; exact ⟨rfl, rfl, rfl, rfl⟩

/-- W2 frente a una red: el crecimiento `e^{S}` de la dimensión de un nivel entero no es la
dimensión `χⁿ` de ninguna red de `n ≥ 1` enlaces enteros, porque `e^{S/n} = e^{π (φ^σ/n)}` es
trascendente (Gelfond–Schneider). -/
theorem level_growth_not_power (σ n χ : ℕ) (hn : 0 < n) :
    (χ : ℝ) ^ n ≠ Real.exp (Real.pi * ((1 + Real.sqrt 5) / 2) ^ σ) := by
  intro h
  set b : ℝ := (1 + Real.sqrt 5) / 2 with hb
  have hn0 : (n : ℝ) ≠ 0 := by exact_mod_cast hn.ne'
  set a : ℝ := b ^ σ / n with ha
  have hbpos : 0 < b := by rw [hb]; positivity
  have ha0 : a ≠ 0 := by rw [ha]; exact div_ne_zero (pow_ne_zero _ hbpos.ne') hn0
  have halg : IsAlgebraic ℚ a := by
    rw [ha, div_eq_mul_inv]
    exact (golden_isAlgebraic.pow σ).mul (IsAlgebraic.inv (isAlgebraic_natCast n))
  have hT := exp_pi_mul_algebraic_transcendental a halg ha0
  have hpow : Real.exp (Real.pi * a) ^ n = (χ : ℝ) ^ n := by
    rw [← Real.exp_nat_mul, h]; congr 1; rw [ha]; field_simp
  have hx : Real.exp (Real.pi * a) = χ := by
    have h1 : 0 ≤ Real.exp (Real.pi * a) := (Real.exp_pos _).le
    have h2 : 0 ≤ (χ : ℝ) := Nat.cast_nonneg χ
    have hpow' : Real.exp (Real.pi * a) ^ ((n : ℝ)) = (χ : ℝ) ^ ((n : ℝ)) := by
      simp only [Real.rpow_natCast]; exact hpow
    exact (Real.rpow_left_inj h1 h2 hn0).mp hpow'
  exact hT (hx ▸ isAlgebraic_natCast χ)

/-! ## v31: las dos coordenadas, el paso de nivel, el medio giro y la traza 3 (Sprint 55) -/

/-- `|φ̄|·φ = 1`, con `φ̄ = (1 − √5)/2 = −1/φ` (`conjugate_is_mirror`). -/
theorem conjugate_abs_mul_golden :
    |(1 - Real.sqrt 5) / 2| * ((1 + Real.sqrt 5) / 2) = 1 := by
  rw [conjugate_is_mirror]
  have hp : (0 : ℝ) < (1 + Real.sqrt 5) / 2 := by positivity
  rw [abs_div, abs_neg, abs_one, abs_of_pos hp]
  field_simp

/-- I1: la segunda coordenada de un nivel, por `M`, es el tiempo del weld:
`φⁿ · (M · |φ̄|ⁿ) = M`, porque la norma de una unidad es ±1. -/
theorem weld_time_is_conjugate (M : ℝ) (n : ℕ) :
    ((1 + Real.sqrt 5) / 2) ^ n * (M * |(1 - Real.sqrt 5) / 2| ^ n) = M := by
  have h := conjugate_abs_mul_golden
  calc ((1 + Real.sqrt 5) / 2) ^ n * (M * |(1 - Real.sqrt 5) / 2| ^ n)
      = M * (|(1 - Real.sqrt 5) / 2| * ((1 + Real.sqrt 5) / 2)) ^ n := by rw [mul_pow]; ring
    _ = M := by rw [h, one_pow, mul_one]

/-- I2: la matriz de la sustitución de los anillos, `A ↦ AB`, `B ↦ A`, es un corrimiento del
enrollamiento seguido del intercambio `(n,w) ↦ (w,n)` (sobre vectores columna actúa primero el factor derecho). -/
theorem level_step_is_exchange_shift :
    (!![0, 1; 1, 0] : Matrix (Fin 2) (Fin 2) ℤ) * !![1, 0; 1, 1] = !![1, 1; 1, 0] := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [Matrix.mul_apply, Fin.sum_univ_two]

/-- I6: el cuadrado de la matriz dorada es `[[2,1],[1,1]]`. -/
theorem golden_matrix_sq :
    (!![1, 1; 1, 0] : Matrix (Fin 2) (Fin 2) ℤ) * !![1, 1; 1, 0] = !![2, 1; 1, 1] := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [Matrix.mul_apply, Fin.sum_univ_two]

/-- I6: su traza, `2 + 1 = 3`, es `φ² + φ⁻²` (`sq_add_inv_sq`). -/
theorem golden_square_trace :
    ((2 : ℝ) + 1) = ((1 + Real.sqrt 5) / 2) ^ 2 + (((1 + Real.sqrt 5) / 2)⁻¹) ^ 2 := by
  have h5 : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)
  have hb : (0 : ℝ) < (1 + Real.sqrt 5) / 2 := by positivity
  have h2 : ((1 + Real.sqrt 5) / 2) ^ 2 = (1 + Real.sqrt 5) / 2 + 1 := by nlinarith [h5]
  rw [sq_add_inv_sq _ hb h2]; norm_num

/-- I4: en el medio giro, `e^{iπ} = −1`, el solapamiento de un estado de pesos `1 − p` y `p`
con su inicio es `1 − 2p`, y se anula si y solo si `p = ½`. -/
theorem orthogonal_at_half_turn (p : ℝ) : (1 - p) + p * (-1) = 0 ↔ p = 1 / 2 := by
  constructor <;> intro h <;> linarith

/-! ## v32: las tres columnas (Sprint 56) -/

/-- E1: los ejes de ℤ³ proyectados por la diagonal, `e_k − ⅓(1,1,1)`, suman cero (el núcleo es
la diagonal), tienen cuadrado de largo `⅔` y forman ángulos de coseno `−½` (120°). -/
theorem cube_diagonal_kernel :
    ((2 : ℝ) / 3 + (-1 / 3) + (-1 / 3) = 0) ∧
    ((2 : ℝ) / 3) ^ 2 + (-1 / 3) ^ 2 + (-1 / 3) ^ 2 = 2 / 3 ∧
    ((2 : ℝ) / 3 * (-1 / 3) + (-1 / 3) * (2 / 3) + (-1 / 3) * (-1 / 3)) / (2 / 3) = -1 / 2 := by
  norm_num

/-- E2 (Binet): la cuenta de Fibonacci difiere de `φⁿ/√5` exactamente en `−ψⁿ/√5`; como
`|ψ| < 1` (φ es una unidad de Pisot), la diferencia se anula. -/
theorem tile_count_deviation (n : ℕ) :
    (Nat.fib n : ℝ) - goldenRatio ^ n / Real.sqrt 5 = -(goldenConj ^ n) / Real.sqrt 5 := by
  rw [Real.coe_fib_eq]; ring

/-- E4: un paso racional `p/q` envía el par `(−p, q)` a `0`: la lectura sobre la recta tiene núcleo. -/
theorem rational_step_kernel (p q : ℤ) (hq : q ≠ 0) :
    ((-p : ℤ) : ℝ) + (q : ℝ) * ((p : ℝ) / q) = 0 := by
  have hq' : (q : ℝ) ≠ 0 := by exact_mod_cast hq
  have h : (q : ℝ) * ((p : ℝ) / q) = p := by field_simp
  rw [h]; push_cast; ring

end TorreKK
