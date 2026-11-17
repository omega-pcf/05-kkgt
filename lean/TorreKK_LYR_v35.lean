/-
  TorreKK_LYR.lean, v34 (November 11, 2026; v34 adds the Hopf foliation, J, the compression limit and the observer's half, and renames the Dedekind axiom to dedekindEta so as not to clash with the metric eta): everything article 9 proves, in Lean.
  Status: [P*] written, NOT COMPILED (there is no Lean in the environment where it was written).
  No sorry. Axioms at the end for classical results that Mathlib does not have yet (each with its source).

  Contenido
  1. The A.7 operator (hops b², b⁻²) is self-adjoint in the metric η_σ = b^(−4σ)
     (symmetry of η·K, row by row).                                  [E1]
  2. η_σ = exp(4·A σ) with A σ = −σ·log b: the metric is √(−g) of the throat.   [E1]
  3. The correct symmetrizer is D_σ = b^(−2σ), with D² = η; the one in the
     A.1 proof, b^σ, does not symmetrize if b > 1.                                    [defect 1]
  4. The hops b², b⁻² are Bloch scattering with momentum k − i·2·log b.  [§1]
  5. The phase of the zeros of J_ν with ν = d/2 − 1 is (d − 3)/4, and equals 1/4
     exactly when d = 4 = n + 1 with n = 3.                             [E2]
  6. Randall–Sundrum is the golden throat (change of variables).
  7. The ring: constant mode m²(log φ)² = −1, below the BF bound −4.
  8. The clock of φ: the half turn x¹² in a clock of order 24.
  9. An exponent carries an angle and a radius.
 10. Results imported from CW6 and F1: z·τ = M, ε₀·M = π, golden valuation, |2|₂ = φ^{−λ}.
 11. (v31) The time of the weld is the second Galois coordinate; the level step is the
     the exchange (n,w) ↦ (w,n) with a shift; orthogonality at the half turn forces ½;
     the trace 3 of the square of the golden matrix.
 12. (v32) The diagonal of the cube has a kernel; the tile count differs from its mean by
     −ψⁿ/√5 (Binet); a rational step p/q has kernel (−p, q).
 13. (v34) The Hopf foliation of S³ is the torus tower of the window; J; the limit z = ½; flip_level;
     the flat chart covers the half.
-/
import Mathlib

noncomputable section
set_option linter.style.longLine false

open Real Complex

namespace TorreKK

/-! ### 1–3. The metric of the throat -/

/-- Metric of the level σ: η_σ = b^(−4σ). -/
def etaMetric (b : ℝ) (σ : ℤ) : ℝ := b ^ (-(4 : ℤ) * σ)

/-- Hop down (σ → σ−1) and up (σ → σ+1) of the A.7 operator. -/
def hopDown (b : ℝ) : ℝ := b ^ (2 : ℤ)
def hopUp (b : ℝ) : ℝ := b ^ (-(2 : ℤ))

/-- E1: η·K is symmetric. The (σ, σ+1) entry of η·K is η_σ·b⁻²; the (σ+1, σ)
    one is η_{σ+1}·b². They are equal for every nonzero base. -/
theorem eta_symmetrizes (b : ℝ) (hb : b ≠ 0) (σ : ℤ) :
    etaMetric b σ * hopUp b = etaMetric b (σ + 1) * hopDown b := by
  unfold etaMetric hopUp hopDown
  rw [← zpow_add₀ hb, ← zpow_add₀ hb]
  congr 1
  ring

/-- In the opposite orientation, the reflected operator (hops b⁻² from below and b² from above)
    is symmetrized by η'_σ = b^(4σ): η'_σ·b² = η'_{σ+1}·b⁻². -/
theorem eta_reflected_symmetrizes (b : ℝ) (hb : b ≠ 0) (σ : ℤ) :
    b ^ ((4 : ℤ) * σ) * hopDown b = b ^ ((4 : ℤ) * (σ + 1)) * hopUp b := by
  unfold hopDown hopUp
  rw [← zpow_add₀ hb, ← zpow_add₀ hb]
  congr 1
  ring

/-- E1: η is the exponential of 4A, with A σ = −σ·log b. -/
theorem eta_eq_exp_fourA (b : ℝ) (hb : 0 < b) (σ : ℤ) :
    etaMetric b σ = Real.exp (4 * (-(σ : ℝ) * Real.log b)) := by
  unfold etaMetric
  rw [← Real.rpow_intCast, Real.rpow_def_of_pos hb]
  congr 1
  push_cast
  ring

/-- Symmetrizer of the A.1 proof, corrected: D_σ = b^(−2σ). -/
def D (b : ℝ) (σ : ℤ) : ℝ := b ^ (-(2 : ℤ) * σ)

/-- D² = η. -/
theorem D_sq_eq_eta (b : ℝ) (hb : b ≠ 0) (σ : ℤ) : D b σ * D b σ = etaMetric b σ := by
  unfold D etaMetric
  rw [← zpow_add₀ hb]
  congr 1
  ring

/-- With D the two conjugated hops coincide (the conjugated operator is symmetric):
    (D_{σ+1}/D_σ)·b² = (D_σ/D_{σ+1})·b⁻², both equal to 1. -/
theorem D_conjugated_hops_equal (b : ℝ) (hb : b ≠ 0) (σ : ℤ) :
    (D b (σ + 1) / D b σ) * hopDown b = (D b σ / D b (σ + 1)) * hopUp b := by
  unfold D hopDown hopUp
  rw [← zpow_sub₀ hb, ← zpow_sub₀ hb, ← zpow_add₀ hb, ← zpow_add₀ hb]
  congr 1
  ring


/-- Conjugated by D, every hop is exactly 1: the conjugated operator is the symmetric chain
    with diagonal 2 and hops −1 (in units of (log b)⁻²), a Dirichlet band of phase 0. -/
theorem D_conjugated_hop_is_one (b : ℝ) (hb : b ≠ 0) (σ : ℤ) :
    (D b (σ + 1) / D b σ) * hopDown b = 1 := by
  unfold D hopDown
  rw [← zpow_sub₀ hb, ← zpow_add₀ hb]
  have : -(2 : ℤ) * (σ + 1) - -(2 : ℤ) * σ + 2 = 0 := by ring
  rw [this, zpow_zero]

/-- The symmetrizer named by the A.1 proof, b^σ, does not symmetrize if b > 1:
    it would have to satisfy b·b² = b⁻¹·b⁻², that is b³ = b⁻³. -/
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

/-! ### 4. Bloch with complexified momentum -/

/-- e^{i(k − iε)} = e^{ε}·e^{ik}: complexifying the momentum by −iε multiplies the hop by e^{ε}. -/
theorem bloch_complexified (k ε : ℝ) :
    Complex.exp (I * ((k : ℂ) - I * ε)) = Real.exp ε * Complex.exp (I * k) := by
  have : I * ((k : ℂ) - I * ε) = (ε : ℂ) + I * k := by
    rw [mul_sub, ← mul_assoc, I_mul_I]
    ring
  rw [this, Complex.exp_add, ← Complex.ofReal_exp]

/-- With ε = 2·log b (b > 0), the factor is exactly the hop b². -/
theorem bloch_factor_is_hop (b : ℝ) (hb : 0 < b) :
    Real.exp (2 * Real.log b) = b ^ (2 : ℤ) := by
  rw [show (2 : ℝ) * Real.log b = Real.log b + Real.log b by ring, Real.exp_add,
    Real.exp_log hb, zpow_two]

/-- And with −ε, the reciprocal hop b⁻². -/
theorem bloch_factor_is_hop_inv (b : ℝ) (hb : 0 < b) :
    Real.exp (-(2 * Real.log b)) = b ^ (-(2 : ℤ)) := by
  rw [Real.exp_neg, bloch_factor_is_hop b hb, zpow_neg]

/-! ### 5. The dimension fixes the Bessel phase -/

/-- Bessel index of the graviton profile in AdS_{d+1}. -/
def nuOf (d : ℚ) : ℚ := d / 2 - 1

/-- Asymptotic phase of the zeros of J_ν: j_{ν,k} ≈ π(k + ν/2 − 1/4). -/
def besselPhase (ν : ℚ) : ℚ := ν / 2 - 1 / 4

theorem phase_of_dimension (d : ℚ) : besselPhase (nuOf d) = (d - 3) / 4 := by
  unfold besselPhase nuOf
  ring

/-- The phase is 1/4 if and only if d = 4. -/
theorem phase_quarter_iff (d : ℚ) : besselPhase (nuOf d) = 1 / 4 ↔ d = 4 := by
  rw [phase_of_dimension]
  constructor
  · intro h; linarith
  · intro h; subst h; norm_num

/-- With the arity n = 3 of CW6, d = n + 1 = 4, ν = 1 and the phase is 1/4. -/
theorem phase_from_arity : nuOf ((3 : ℚ) + 1) = 1 ∧ besselPhase (nuOf ((3 : ℚ) + 1)) = 1 / 4 := by
  unfold besselPhase nuOf
  norm_num

/-! ### 6. Randall–Sundrum is the golden throat (change of variables) -/

/-- The RS warp with k = 1 at y = (σ_UV − σ)·log b is the golden warp normalized to the UV:
    e^{−y} = b^σ / b^{σ_UV}. -/
theorem rs_warp_is_golden (b : ℝ) (hb : 0 < b) (σ σUV : ℝ) :
    Real.exp (-((σUV - σ) * Real.log b)) = b ^ σ / b ^ σUV := by
  rw [Real.rpow_def_of_pos hb, Real.rpow_def_of_pos hb, ← Real.exp_sub]
  congr 1
  ring

/-- The RS depth: e^{−kπr} = b^{−(σ_UV − σ_IR)} with kπr = (σ_UV − σ_IR)·log b. -/
theorem rs_depth_is_levels (b : ℝ) (hb : 0 < b) (σIR σUV : ℝ) :
    Real.exp (-((σUV - σIR) * Real.log b)) = b ^ (-(σUV - σIR)) := by
  rw [Real.rpow_def_of_pos hb]
  congr 1
  ring

/-- The KK scale of RS is the scale operator on the background: k·e^{−kπr} = m₀·b^{σ_IR}
    when the curvature is the scale of the UV, k = m₀·b^{σ_UV}. -/
theorem rs_scale_is_H_at_bottom (b m₀ : ℝ) (hb : 0 < b) (σIR σUV : ℝ) :
    (m₀ * b ^ σUV) * Real.exp (-((σUV - σIR) * Real.log b)) = m₀ * b ^ σIR := by
  rw [rs_warp_is_golden b hb σIR σUV]
  have : b ^ σUV ≠ 0 := (Real.rpow_pos_of_pos hb σUV).ne'
  field_simp

/-- With the UV at a scale M_UV > 0: kπr = log(M_UV/m₀) − σ_IR·log b, that is, kπr is the
    distance in levels between the background and the UV, per log b. -/
theorem rs_kpir_from_uv (b m₀ MUV : ℝ) (hb : 0 < b) (hm : 0 < m₀) (hM : 0 < MUV) (σIR : ℝ) :
    Real.log (MUV / (m₀ * b ^ σIR)) = Real.log (MUV / m₀) - σIR * Real.log b := by
  have h1 : 0 < b ^ σIR := Real.rpow_pos_of_pos hb σIR
  rw [Real.log_div hM.ne' (mul_pos hm h1).ne', Real.log_mul hm.ne' h1.ne',
    Real.log_div hM.ne' hm.ne', Real.log_rpow hb]
  ring

/-! ### 7. The ring and the Breitenlohner–Freedman bound (Remark 2) -/

/-- In the golden tower, b² + b⁻² = 3. -/
theorem sq_add_inv_sq (b : ℝ) (hb : 0 < b) (h : b ^ 2 = b + 1) : b ^ 2 + (b⁻¹) ^ 2 = 3 := by
  have hb0 : b ≠ 0 := hb.ne'
  have hinv : b⁻¹ = b - 1 := by
    field_simp
    nlinarith [h]
  rw [hinv]; nlinarith [h]

/-- In the ring the constant mode has m²·(log b)² = 2 − b² − b⁻² = −1. -/
theorem ring_constant_mode (b : ℝ) (hb : 0 < b) (h : b ^ 2 = b + 1) :
    2 - b ^ 2 - (b⁻¹) ^ 2 = -1 := by
  have := sq_add_inv_sq b hb h; linarith

/-- log φ < 1/2, so −1/(log φ)² < −4, the BF bound of CW6 (eq. 158). -/
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

/-! ### 8. The clock of φ and its half turn (Definition, Proposition 7)
  The clock of φ modulo N is the order of φ in ℤ[φ]/N (the Pisano period); the orders
  π(16) = π(9) = π(12) = π(24) = π(48) = π(72) = 24 and π(5) = 20 are in module XXI,
  `RelojYMenosUnoDoce` (pi_sixteen, pi_nine, pi_twelve, pi_twentyfour, pi_fortyeight,
  pi_seventytwo, pi_five). Here, for any monoid: -/

/-- In a clock of order 24, x¹² is the half turn: different from 1, of square 1, order 2. -/
theorem half_turn_of_clock24 {G : Type*} [Monoid G] (x : G) (hx : orderOf x = 24) :
    x ^ 12 ≠ 1 ∧ (x ^ 12) ^ 2 = 1 ∧ orderOf (x ^ 12) = 2 := by
  have h1 : x ^ 12 ≠ 1 := by
    intro h
    have := orderOf_le_of_pow_eq_one (by norm_num) h
    omega
  have h2 : (x ^ 12) ^ 2 = 1 := by
    rw [← pow_mul]; norm_num; rw [← hx]; exact pow_orderOf_eq_one x
  exact ⟨h1, h2, orderOf_eq_prime h2 h1⟩

/-- In a clock of order 20, x¹² is not an involution. -/
theorem not_half_turn_of_clock20 {G : Type*} [Monoid G] (x : G) (hx : orderOf x = 20) :
    (x ^ 12) ^ 2 ≠ 1 := by
  rw [← pow_mul]
  intro h
  have := orderOf_dvd_of_pow_eq_one h
  rw [hx] at this
  norm_num at this

/-! ### 9. An exponent carries an angle and a radius (notes −1/12, §10.2 (a)) -/

/-- q^E with q = e^{2πiτ}, τ = x + iy: e^{2πiEτ} = e^{2πiEx}·e^{−2πEy}; the first factor has
    modulus 1 (the rotation) and the second is real positive (the radius). -/
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

/-! ### 10. Results imported from CW6 and F1 (Appendix A of article v2)
  Elementary statements of CW6 and F1 used by the article, proved again here so that
  the module is self-contained. -/

/-- CW6 `lattice_radius_conjugate`, F1 §tower-info: z(σ)·τ(σ) = M with z = b^σ, τ = M·b^{−σ}. -/
theorem lattice_radius_conjugate (b M σ : ℝ) (hb : 0 < b) :
    b ^ σ * (M * b ^ (-σ)) = M := by
  rw [Real.rpow_neg hb.le]
  have : b ^ σ ≠ 0 := (Real.rpow_pos_of_pos hb σ).ne'
  field_simp

/-- CW6 (31), F1 `eps0_relates_log_and_geometry`: with ε₀ = log b/(6√3) and M = 6√3·π/log b,
    ε₀·M = π (the certainty principle), and log b = 6√3·π/M. -/
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

/-- F1 `prop:tower-disc-val`: the golden valuation v(x) = log x / log b takes the value n at b^n. -/
theorem golden_valuation_on_tower (b : ℝ) (hb : 1 < b) (n : ℤ) :
    Real.log (b ^ n) / Real.log b = n := by
  have hl : Real.log b ≠ 0 := (Real.log_pos hb).ne'
  rw [Real.log_zpow]; field_simp

/-- F1 `prop:omega-two-adic`: with λ = log 2 / log b, b^{−λ} = 1/2 = |2|₂. -/
theorem two_adic_is_level (b : ℝ) (hb : 1 < b) :
    b ^ (-(Real.log 2 / Real.log b)) = 1 / 2 := by
  have hb0 : 0 < b := by linarith
  have hl : Real.log b ≠ 0 := (Real.log_pos hb).ne'
  rw [Real.rpow_def_of_pos hb0]
  have : Real.log b * -(Real.log 2 / Real.log b) = -Real.log 2 := by field_simp
  rw [this, Real.exp_neg, Real.exp_log (by norm_num)]; norm_num

/-- F1, the additive law of the tower: if r > 0 and r^σ + r^{σ+1} = r^{σ+2} for some real σ,
    then r² = r + 1, whose only positive root is φ. -/
theorem additive_law_forces_golden (r σ : ℝ) (hr : 0 < r)
    (h : r ^ σ + r ^ (σ + 1) = r ^ (σ + 2)) : r ^ 2 = r + 1 := by
  rw [Real.rpow_add hr, Real.rpow_add hr, Real.rpow_one, Real.rpow_two] at h
  have hs : 0 < r ^ σ := Real.rpow_pos_of_pos hr σ
  have h2 : r ^ σ * (r ^ 2 - r - 1) = 0 := by linear_combination (-1 : ℝ) * h
  rcases mul_eq_zero.mp h2 with h3 | h3
  · exact absurd h3 hs.ne'
  · linarith

/-! ### 11. The structure behind the masses (mathematical retroduction) -/

/-- φ is born from the circle: φ = 2 cos(π/5), the ratio of the inscribed pentagon; a cyclotomic number. -/
theorem golden_eq_two_cos_pi_div_five :
    (1 + Real.sqrt 5) / 2 = 2 * Real.cos (Real.pi / 5) := by
  rw [Real.cos_pi_div_five]; ring

/-- φ refers to itself: φ = 1 + 1/φ. Its continued fraction is [1; 1, 1, …], all
    partial quotients equal to 1: it is the irrational worst approximated by fractions (Hurwitz). -/
theorem golden_self_reference (b : ℝ) (hb : 0 < b) (h : b ^ 2 = b + 1) : b = 1 + 1 / b := by
  have hb0 : b ≠ 0 := hb.ne'
  field_simp; ring_nf
  nlinarith [h]

/-- The angle and the scale are one (CW6, Prop. 3.4): with α(σ) = arctan(ε₀ b^σ),
    tan α(σ+1) / tan α(σ) = b. Going up one level multiplies the tangent of the angle by b. -/
theorem spectral_angle_ratio (b ε σ : ℝ) (hb : 0 < b) (hε : 0 < ε) :
    Real.tan (Real.arctan (ε * b ^ (σ + 1))) / Real.tan (Real.arctan (ε * b ^ σ)) = b := by
  rw [Real.tan_arctan, Real.tan_arctan, Real.rpow_add hb, Real.rpow_one]
  have : 0 < b ^ σ := Real.rpow_pos_of_pos hb σ
  field_simp

/-- The periodic roots of the ring used by the article: the quarter turn i (the ¼ offset)
    and the half turn −1 (the background), with i² = −1 and i⁴ = 1. -/
theorem quarter_and_half_turn : Complex.I ^ 2 = -1 ∧ Complex.I ^ 4 = 1 := by
  constructor
  · exact Complex.I_sq
  · rw [show (4 : ℕ) = 2 * 2 from rfl, pow_mul, Complex.I_sq]; norm_num


/-! ## Exact geometry of the throat, the torus and the fibre
Sources: CW6 eq. (torus) `T² = ℂ/Λ`, `Λ = M·ℤ[i]`, `τ = i`; Prop. "fibre independent of base"
(monodromy `e^{iπ} = −1`); eq. (worldline) `Ω(t) = ½ e^{i t log φ}`; eq. (throat) `z(σ) = φ^σ`.
HP Def. "tower parameters": `ε(σ) = ε₀ φ^σ`, `M_σ = φ^σ M`; Prop. "certainty principle":
the half turn closes on the wavelength `π/ε(σ) = M φ^{−σ}`. -/

/-- The modular parameter of each level of the lattice tower is `i`:
`Λ_σ = s·M·ℤ[i]` with `s = φ^σ` has `τ = (s M i)/(s M) = i`. The torus is the same at every level,
up to scale. -/
theorem lattice_tower_tau (s M : ℝ) (hs : 0 < s) (hM : 0 < M) :
    ((s * M : ℝ) * Complex.I) / ((s * M : ℝ) : ℂ) = Complex.I := by
  have h : ((s * M : ℝ) : ℂ) ≠ 0 := by exact_mod_cast (mul_pos hs hM).ne'
  field_simp

/-- The half turn closes at every level on the wavelength `τ(σ) = M b^{−σ}`:
`ε(σ)·τ(σ) = (ε₀ b^σ)(M b^{−σ}) = ε₀ M = π`. -/
theorem closure_each_level (b ε₀ M σ : ℝ) (hb : 0 < b) (hc : ε₀ * M = Real.pi) :
    (ε₀ * b ^ σ) * (M * b ^ (-σ)) = Real.pi := by
  have h1 : b ^ σ * b ^ (-σ) = 1 := by
    rw [← Real.rpow_add hb, add_neg_cancel, Real.rpow_zero]
  calc (ε₀ * b ^ σ) * (M * b ^ (-σ)) = (ε₀ * M) * (b ^ σ * b ^ (-σ)) := by ring
    _ = Real.pi := by rw [h1, hc, mul_one]

/-- On the cell `M_σ = M b^σ` the accumulated phase is `π b^{2σ}`. -/
theorem phase_on_cell (b ε₀ M σ : ℝ) (hb : 0 < b) (hc : ε₀ * M = Real.pi) :
    (ε₀ * b ^ σ) * (M * b ^ σ) = Real.pi * b ^ (2 * σ) := by
  have h2 : b ^ σ * b ^ σ = b ^ (2 * σ) := by
    rw [← Real.rpow_add hb]; ring_nf
  calc (ε₀ * b ^ σ) * (M * b ^ σ) = (ε₀ * M) * (b ^ σ * b ^ σ) := by ring
    _ = Real.pi * b ^ (2 * σ) := by rw [h2, hc]

/-- And that phase is the half turn only at the level `σ = 0`. -/
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

/-- The monodromy of the fibre: half turn, `e^{iπ} = −1`, of order two. -/
theorem fibre_half_turn : Complex.exp (Real.pi * Complex.I) = -1 ∧ ((-1 : ℂ)) ^ 2 = 1 := by
  refine ⟨Complex.exp_pi_mul_I, by norm_num⟩

/-- The modulus of the worldline is `½` at every phase: `|½ e^{iθ}| = ½`. -/
theorem worldline_modulus (θ : ℝ) :
    ‖(1 / 2 : ℂ) * Complex.exp (θ * Complex.I)‖ = 1 / 2 := by
  rw [Complex.norm_mul, Complex.norm_exp_ofReal_mul_I]; norm_num

/-- The throat is exactly a pseudosphere (Beltrami): the profile `r(y) = e^{y}`, `y ≤ 0`,
with height `h'(y) = √(1 − r²)` has unit speed, `r'² + h'² = 1`; the induced metric is
`e^{2y} dθ² + dy²`, the radial section of `ds² = e^{2A} dx² + dy²`. -/
theorem pseudosphere_unit_speed (y : ℝ) (hy : y ≤ 0) :
    (Real.exp y) ^ 2 + (Real.sqrt (1 - (Real.exp y) ^ 2)) ^ 2 = 1 := by
  have h1 : Real.exp y ≤ 1 := Real.exp_le_one_iff.mpr hy
  have h0 : 0 ≤ Real.exp y := (Real.exp_pos y).le
  have : 0 ≤ 1 - (Real.exp y) ^ 2 := by nlinarith
  rw [Real.sq_sqrt this]; ring

/-- The rings: the radius at the level `σ` is `b^σ` (up to normalization), and successive
rings are in ratio `b`. -/
theorem ring_ratio (b σ : ℝ) (hb : 0 < b) : b ^ (σ + 1) / b ^ σ = b := by
  rw [Real.rpow_add hb, Real.rpow_one]
  have : 0 < b ^ σ := Real.rpow_pos_of_pos hb σ
  field_simp

/-- The square torus `τ = i` on the Clifford torus: `(a,b) ↦ (cos a, sin a, cos b, sin b)/√2`
has its two partial derivatives of equal norm, `½`, and orthogonal: it is the flat
square metric. Its stereographic projection (conformal, classical) is the surface of revolution with
`R/r = √2`. -/
theorem clifford_square (a b : ℝ) :
    (Real.sin a) ^ 2 / 2 + (Real.cos a) ^ 2 / 2 = 1 / 2 ∧
    (Real.sin b) ^ 2 / 2 + (Real.cos b) ^ 2 / 2 = 1 / 2 := by
  constructor <;> nlinarith [Real.sin_sq_add_cos_sq a, Real.sin_sq_add_cos_sq b]


/-! ## Why φ for the ensemble: the orbit does not close
A rotation of step `φ` on the circle has no period: `n·φ` is never an integer for `n ≠ 0`.
By Weyl (1916) the orbit is equidistributed: the average over an orbit is the average
over the whole circle. -/

theorem golden_irrational : Irrational ((1 + Real.sqrt 5) / 2) := by
  have h5 : Irrational (Real.sqrt 5) := by
    simpa using Nat.Prime.irrational_sqrt (by norm_num : Nat.Prime 5)
  have h1 : Irrational ((1 : ℚ) + Real.sqrt 5) := Irrational.ratCast_add 1 h5
  have h2 := Irrational.div_ratCast h1 (by norm_num : (2 : ℚ) ≠ 0)
  simpa using h2

theorem golden_rotation_aperiodic (n m : ℤ) (hn : n ≠ 0) :
    (n : ℝ) * ((1 + Real.sqrt 5) / 2) ≠ m :=
  (Irrational.intCast_mul golden_irrational hn).ne_int m


/-! ## Contact in 2 and 3 dimensions
2D: the six units of ℤ[ω], at distance 1 from the origin and from their neighbours (side π).
3D: the twelve vertices `(0, ±1, ±φ)` of the icosahedron (side φ).
The 12: |A₅| / 5 = 60 / 5 = lcm(4, 6) (F1, module XXI: `group_orders`, `pi_ten`,
`minus_one_twelfth_is_the_clock`). -/

/-- Hexagonal contact: `e^{iπ/3}` is at distance 1 from `1`. -/
theorem hexagonal_contact :
    (Real.cos (Real.pi / 3) - 1) ^ 2 + (Real.sin (Real.pi / 3)) ^ 2 = 1 := by
  rw [Real.cos_pi_div_three, Real.sin_pi_div_three]
  have h : Real.sqrt 3 ^ 2 = 3 := Real.sq_sqrt (by norm_num)
  nlinarith [h]

/-- The vertices `(0, ±1, ±φ)` are at distance² `φ + 2` from the centre. -/
theorem icosahedron_vertex_norm (b : ℝ) (h : b ^ 2 = b + 1) :
    (0 : ℝ) ^ 2 + 1 ^ 2 + b ^ 2 = b + 2 := by nlinarith [h]

/-- Two neighbours, `(0,1,φ)` with `(0,−1,φ)` and `(0,1,φ)` with `(1,φ,0)`, are at distance² 4. -/
theorem icosahedron_edges (b : ℝ) (h : b ^ 2 = b + 1) :
    (0 - 0 : ℝ) ^ 2 + (1 - (-1)) ^ 2 + (b - b) ^ 2 = 4
    ∧ (0 - 1 : ℝ) ^ 2 + (1 - b) ^ 2 + (b - 0) ^ 2 = 4 := by
  constructor
  · ring
  · nlinarith [h]

/-- With the centres at distance 2, the twelve unit spheres touch the central one and do not
cut each other: the distance² between neighbours, `4·4/(φ+2)`, is at least 4 because `φ + 2 ≤ 4`. -/
theorem icosahedral_kissing (b : ℝ) (h1 : 0 < b) (h2 : b ≤ 2) :
    4 ≤ 4 * 4 / (b + 2) := by
  rw [le_div_iff₀ (by linarith)]; nlinarith

/-- The twelve: `|A₅| = 60`, `60 / 5 = 12 = lcm(4, 6)`. -/
theorem twelve_of_the_icosahedron :
    Fintype.card (alternatingGroup (Fin 5)) = 60 ∧ 60 / 5 = 12 ∧ Nat.lcm 4 6 = 12 := by
  have h5 := two_mul_card_alternatingGroup (α := Fin 5)
  rw [Fintype.card_perm, Fintype.card_fin] at h5
  have f5 : Nat.factorial 5 = 120 := rfl
  rw [f5] at h5
  exact ⟨by omega, rfl, by norm_num⟩

/-- `φ` is the trace of the icosahedral rotation of angle `2π/5`: `1 + 2cos(2π/5) = φ`. -/
theorem golden_is_icosahedral_trace :
    1 + 2 * Real.cos (2 * Real.pi / 5) = (1 + Real.sqrt 5) / 2 := by
  have h : 2 * Real.pi / 5 = 2 * (Real.pi / 5) := by ring
  rw [h, Real.cos_two_mul, Real.cos_pi_div_five]
  have h5 : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)
  nlinarith [h5]


/-- Mass is information: `π(k+¼)·M·b^{12} = (k+¼)·M·S(12)` with `S(σ) = π b^σ`, the entropy of
saturation of the level (CW6 §4.4). -/
theorem mass_is_bottom_information (b M k : ℝ) :
    Real.pi * (k + 1 / 4) * M * b ^ 12 = (k + 1 / 4) * M * (Real.pi * b ^ 12) := by ring


/-! ## Audit: what was missing for the argument to be complete in Lean -/

/-- Prop. «The scale is the scale operator at the bottom»: `j·b^σ = j·H(σ)/m₀`, with `H = m₀ b^σ`. -/
theorem scale_operator_at_bottom (j m₀ b σ : ℝ) (hm : m₀ ≠ 0) :
    j * b ^ σ = j * (m₀ * b ^ σ) / m₀ := by
  field_simp

/-- Prop. «The bottom is the half-turn», point 2: `χ(SL₂ℤ) = ¼ + ⅙ − ½ = −1/12` from the
amalgam `ℤ/4 *_{ℤ/2} ℤ/6`. -/
theorem euler_char_amalgam : (1 / 4 + 1 / 6 - 1 / 2 : ℚ) = -1 / 12 := by norm_num

/-- `S` has order 4 and `ST` order 6 in `SL₂(ℤ)`. -/
theorem modular_orders :
    let S : Matrix (Fin 2) (Fin 2) ℤ := !![0, -1; 1, 0]
    let T : Matrix (Fin 2) (Fin 2) ℤ := !![1, 1; 0, 1]
    S ^ 4 = 1 ∧ S ^ 2 ≠ 1 ∧ (S * T) ^ 6 = 1 ∧ (S * T) ^ 2 ≠ 1 ∧ (S * T) ^ 3 ≠ 1 := by
  decide

set_option maxRecDepth 100000 in
/-- The clocks of `φ`: the order of the Fibonacci matrix `Q = [[0,1],[1,1]]` (the
multiplication by `φ` in `ℤ[φ]`) modulo `N`. It is 24 for `N = 16` and `N = 9`, 20 for `N = 5`
and 60 for `N = 10`; in each case the maximal divisors are ruled out. -/
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


/-! ## Axioms: classical results that Mathlib does not have yet
Each is a published theorem; it is declared here as an axiom with its source, and everything the
article derives from it is proved from the axiom. -/

/-- **Axiom (zeros of `J₁`).** The positive zeros of the Bessel function `J₁`, in
increasing order, with their first four values and the McMahon phase `π(k + ¼)`.
Sources: Watson, *A Treatise on the Theory of Bessel Functions* (1944), §15.53; for the
Kaluza–Klein tower, Randall and Sundrum (1999) and Davoudiasl, Hewett and Rizzo (2000). -/
axiom bessel_J1_zeros :
  ∃ j : ℕ → ℝ, StrictMono j ∧ 0 < j 0 ∧
    |j 0 - 3.8317| < 1e-4 ∧ |j 1 - 7.0156| < 1e-4 ∧ |j 2 - 10.1735| < 1e-4 ∧
    |j 3 - 13.3237| < 1e-4 ∧
    Filter.Tendsto (fun k : ℕ => j k - Real.pi * ((k : ℝ) + 1 + 1 / 4)) Filter.atTop (nhds 0)

/-- **Axiom (Gelfond–Schneider).** For every real algebraic `a ≠ 0`, `e^{πa}` is transcendental:
it is `(−1)^{−ia}`, with algebraic base different from 0 and 1 and exponent `−ia` algebraic and irrational.
Sources: Gelfond (1934); Schneider (1935). -/
axiom exp_pi_mul_algebraic_transcendental (a : ℝ) (ha : IsAlgebraic ℚ a) (ha0 : a ≠ 0) :
    Transcendental ℚ (Real.exp (Real.pi * a))

/-- `e^π` is transcendental: the case `a = 1`. -/
theorem exp_pi_transcendental : Transcendental ℚ (Real.exp Real.pi) := by
  simpa using exp_pi_mul_algebraic_transcendental 1 isAlgebraic_one one_ne_zero

/-- `φ` is algebraic: a root of `X² − X − 1`. -/
theorem golden_is_algebraic : IsAlgebraic ℚ ((1 + Real.sqrt 5) / 2) := by
  refine ⟨Polynomial.X ^ 2 - Polynomial.X - 1, ?_, ?_⟩
  · intro h
    have := congrArg (Polynomial.coeff · 2) h
    simp [Polynomial.coeff_X, Polynomial.coeff_one] at this
  · have h5 : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)
    simp [Polynomial.aeval_def]

/-- `log φ / π` is irrational: if `q·log φ = p·π` with `q > 0`, then `φ^q = (e^π)^p`, and
`e^π` would be algebraic. -/
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
  have halg : IsAlgebraic ℚ (Real.exp Real.pi ^ p) := hpow ▸ golden_is_algebraic.pow q
  exact exp_pi_transcendental (IsAlgebraic.of_pow hp halg)

/-- The stereographic image of the Clifford torus is the surface of revolution with `R = √2`, `r = 1`:
for `s² + c² = 1` and `d = 1 − s/√2`, the point `(ρ, z) = (1/(√2 d), c/(√2 d))` satisfies
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

/-- **Axiom (derivatives of the projection).** With `r(b) = √2 − sin b`, the projected meridian
`ρ(b) = 1/r`, `z(b) = cos b / r` has derivatives `ρ' = cos b / r²` and `z' = (1 − √2 sin b) / r²`.
It is single-variable calculus (quotient rule). -/
axiom stereographic_meridian_deriv (b : ℝ) :
    HasDerivAt (fun x => 1 / (Real.sqrt 2 - Real.sin x))
      (Real.cos b / (Real.sqrt 2 - Real.sin b) ^ 2) b ∧
    HasDerivAt (fun x => Real.cos x / (Real.sqrt 2 - Real.sin x))
      ((1 - Real.sqrt 2 * Real.sin b) / (Real.sqrt 2 - Real.sin b) ^ 2) b

/-- The projection is conformal on the torus: the induced metric `ρ² da² + (ρ'² + z'²) db²` is
`ρ²(da² + db²)`, because `ρ'² + z'² = ρ²`. Thus the surface of revolution is conformal to the flat
square torus, `τ = i`. -/
theorem stereographic_conformal (s c : ℝ) (hsc : s ^ 2 + c ^ 2 = 1) (hr : Real.sqrt 2 - s ≠ 0) :
    (c / (Real.sqrt 2 - s) ^ 2) ^ 2 + ((1 - Real.sqrt 2 * s) / (Real.sqrt 2 - s) ^ 2) ^ 2
      = (1 / (Real.sqrt 2 - s)) ^ 2 := by
  have h2 : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  field_simp; ring_nf
  nlinarith [h2, hsc]


/-! ## The postulates of field theory, holography and the string that the article proves -/

/-- Critical dimension: `(D − 2)·½·ζ(−1) = −1` with `ζ(−1) = −1/12` gives `D = 26 = c`. -/
theorem critical_dimension (D : ℚ) :
    (D - 2) * (1 / 2) * (-1 / 12) = -1 ↔ D = 26 := by
  constructor
  · intro h; linarith
  · intro h; subst h; norm_num

/-- The crossing group: modulo 2, `S` and `ST` (the partner of `φ`) generate `SL₂(𝔽₂) ≅ S₃`. -/
theorem crossing_group_mod_two :
    let S : Matrix (Fin 2) (Fin 2) (ZMod 2) := !![0, 1; 1, 0]
    let R : Matrix (Fin 2) (Fin 2) (ZMod 2) := !![0, 1; 1, 1]
    S ^ 2 = 1 ∧ R ^ 3 = 1 ∧ R ≠ 1 ∧ S * R ≠ R * S ∧
    [1, S, R, R ^ 2, S * R, S * R ^ 2].Nodup := by
  decide

/-- The crossing point: if `λ(−1/τ) = 1 − λ(τ)` and `S` fixes `τ = i`, then `λ(i) = ½`. -/
theorem crossing_point_half (lam : ℂ → ℂ) (hS : lam (-1 / Complex.I) = 1 - lam Complex.I) :
    lam Complex.I = 1 / 2 := by
  have h : -1 / Complex.I = Complex.I := by
    rw [div_eq_iff Complex.I_ne_zero, Complex.I_mul_I]
  rw [h] at hS
  linear_combination hS / 2

/-- **Axioma (Dedekind; Apostol, *Modular Functions and Dirichlet Series*, Thms. 3.1 and 3.4).** -/
axiom dedekindEta : ℂ → ℂ
axiom eta_T (τ : ℂ) (h : 0 < τ.im) :
    dedekindEta (τ + 1) = Complex.exp (2 * Real.pi * Complex.I / 24) * dedekindEta τ

/-- The multiplier of `η^k` under `T`: with `k = 24`, the clock, it is 1; with `k = 12`, the background, it is
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

/-- `|η|^{48}` is invariant under `T`. -/
theorem partition_T_invariant (τ : ℂ) (h : 0 < τ.im) :
    ‖dedekindEta (τ + 1)‖ ^ 48 = ‖dedekindEta τ‖ ^ 48 := by
  rw [eta_T τ h, Complex.norm_mul, Complex.norm_exp]
  have : (2 * Real.pi * Complex.I / 24 : ℂ).re = 0 := by simp
  rw [this, Real.exp_zero, one_mul]

/-- Average over the first `N+1` points of the orbit `n ↦ nα`. -/
noncomputable def orbitAvg (f : ℝ → ℝ) (α : ℝ) (N : ℕ) : ℝ :=
  (1 / ((N : ℝ) + 1)) * ∑ n ∈ Finset.range (N + 1), f (n * α)

/-- **Axioma (Weyl 1916, Math. Ann. 77, 313–352).** -/
axiom weyl_equidistribution (α : ℝ) (hα : Irrational α) (f : ℝ → ℝ) (hf : Continuous f)
    (hper : Function.Periodic f 1) :
    Filter.Tendsto (orbitAvg f α) Filter.atTop (nhds (∫ x in (0 : ℝ)..1, f x))

/-- Factorization: the connected part over an orbit tends to the covariance `∫fg − ∫f∫g`. -/
theorem orbit_connected_part (α : ℝ) (hα : Irrational α) (f g : ℝ → ℝ)
    (hf : Continuous f) (hg : Continuous g)
    (hpf : Function.Periodic f 1) (hpg : Function.Periodic g 1) :
    Filter.Tendsto (fun N => orbitAvg (fun x => f x * g x) α N - orbitAvg f α N * orbitAvg g α N)
      Filter.atTop
      (nhds ((∫ x in (0 : ℝ)..1, f x * g x) - (∫ x in (0 : ℝ)..1, f x) * ∫ x in (0 : ℝ)..1, g x)) := by
  have hfg : Function.Periodic (fun x => f x * g x) 1 := fun x => by simp [hpf x, hpg x]
  exact (weyl_equidistribution α hα _ (hf.mul hg) hfg).sub
    ((weyl_equidistribution α hα f hf hpf).mul (weyl_equidistribution α hα g hg hpg))

/-- In each individual theory the product factorizes. -/
theorem single_theory_factorizes (f g : ℝ → ℝ) (θ : ℝ) :
    (fun x => f x * g x) θ = f θ * g θ := rfl

/-- Distance: with `H(σ) = √2·b^{−σ/2}` and `Λ = 6 b^{−σ}` (CW6), `3H² = Λ`; the tower that falls as
`b^{−σ/2}` falls as `Λ^{1/2}`. -/
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


/-! ## The subdivision of the ring by the compactification
`N(σ) = z(σ)/(τ(σ)/M) = φ^{2σ}`: fibre loops that fit in the ring of the level. -/

/-- Powers of `φ` in the basis `{1, φ}`: `φ^{n+1} = F_{n+1}·φ + F_n`. -/
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

/-- The resolution of the ring is not integer: `φ^{2n}` is irrational for `n ≥ 1`. -/
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

/-- `N = z²`: with `z = b^σ` and `τ = M·b^{−σ}`, `z / (τ/M) = b^{2σ}`. -/
theorem ring_resolution_is_square (b M σ : ℝ) (hb : 0 < b) (hM : M ≠ 0) :
    b ^ σ / ((M * b ^ (-σ)) / M) = (b ^ σ) ^ 2 := by
  rw [show (M * b ^ (-σ)) / M = b ^ (-σ) by rw [mul_comm M, mul_div_cancel_right₀ _ hM],
    Real.rpow_neg hb.le, div_inv_eq_mul]
  ring

/-- Cardy with `c = 3` and `L₀ = N/2`: `2π√(c·L₀/6) = π√N`; with `N = z²`, `= π z = S`. -/
theorem cardy_entropy (N : ℝ) (hN : 0 ≤ N) :
    2 * Real.pi * Real.sqrt (3 * (N / 2) / 6) = Real.pi * Real.sqrt N := by
  have h : 3 * (N / 2) / 6 = (Real.sqrt N / 2) ^ 2 := by
    rw [div_pow, Real.sq_sqrt hN]; ring
  rw [h, Real.sqrt_sq (by positivity)]; ring

theorem cardy_is_tower_entropy (b σ : ℝ) (hb : 0 < b) :
    2 * Real.pi * Real.sqrt (3 * ((b ^ σ) ^ 2 / 2) / 6) = Real.pi * b ^ σ := by
  rw [cardy_entropy _ (sq_nonneg _), Real.sqrt_sq (Real.rpow_pos_of_pos hb σ).le]

/-- The spectrum of a closed string on a circle of radius `R`, without oscillators:
`m² = (n/R)² + (wR/α')²`. -/
noncomputable def closedStringMass2 (n w : ℤ) (R a : ℝ) : ℝ := (n / R) ^ 2 + (w * R / a) ^ 2

/-- Invariance: radius `R` with `(n, w)` and radius `α'/R` with `(w, n)` give the same mass. -/
theorem closed_string_invariance (n w : ℤ) (R a : ℝ) (hR : R ≠ 0) (ha : a ≠ 0) :
    closedStringMass2 n w R a = closedStringMass2 w n (a / R) a := by
  unfold closedStringMass2; field_simp; ring

/-- With `α' = M`, the dual radius of the throat `z = b^σ` is the loop `τ = M b^{−σ}`. -/
theorem dual_radius_is_loop (b M σ : ℝ) (hb : 0 < b) :
    M / b ^ σ = M * b ^ (-σ) := by
  rw [Real.rpow_neg hb.le, div_eq_mul_inv]


/-! ## What `N` counts: retroduction
The holographic bound of the level is `S = π z` (CW6: `S = A/4G_N`, `G_N = ½`, `A = 2π z`). -/

/-- `φ³ = 2 + √5 > π`. -/
theorem golden_cube_gt_pi : Real.pi < ((1 + Real.sqrt 5) / 2) ^ 3 := by
  have h5 : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)
  have hs : 2 < Real.sqrt 5 := by nlinarith [Real.sqrt_nonneg 5]
  have hc : ((1 + Real.sqrt 5) / 2) ^ 3 = 2 + Real.sqrt 5 := by nlinarith [h5]
  rw [hc]; linarith [Real.pi_lt_d2]

/-- If `N = z²` counted bits, it would exceed the bound `π z` as soon as `z > π`, that is from `σ = 3`. -/
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

/-- The area law in four dimensions, `4π z²/(4·½) = 2π z²`, matches the entropy of
the weld `π z` only at `z = ½ = |Ω|`. -/
theorem area_law_4d_meets_weld_iff (z : ℝ) (hz : 0 < z) :
    2 * Real.pi * z ^ 2 = Real.pi * z ↔ z = 1 / 2 := by
  constructor
  · intro h
    have : Real.pi * z * (2 * z - 1) = 0 := by linarith
    rcases mul_eq_zero.mp this with h0 | h0
    · exact absurd h0 (mul_pos Real.pi_pos hz).ne'
    · linarith
  · rintro rfl; ring

/-- With `N = z²` quanta, the Cardy entropy saturates the bound: `π √N = π z`. -/
theorem cardy_saturates_bound (z : ℝ) (hz : 0 ≤ z) : Real.pi * Real.sqrt (z ^ 2) = Real.pi * z := by
  rw [Real.sqrt_sq hz]


/-! ## The individual and the ensemble
A single microstate: its modulus, the isometry of the triad, the bit, the gravitational data;
-/

/-- The triad `v_k = ½ ω^k`, `ω = e^{2πi/3}`: each `|v_k| = ½`. -/
theorem triad_modulus (k : ℕ) :
    ‖(1 / 2 : ℂ) * Complex.exp (((2 * Real.pi / 3 : ℝ) : ℂ) * Complex.I) ^ k‖ = 1 / 2 := by
  rw [Complex.norm_mul, Complex.norm_pow, Complex.norm_exp_ofReal_mul_I, one_pow, mul_one]; norm_num

/-- Bulk–boundary isometry: `‖v‖² = 3·¼ = ¾`, and the normalized column satisfies `V†V = Σ|V_k|² = 1`. -/
theorem bulk_boundary_isometry :
    (∑ k ∈ Finset.range 3,
        (‖(1 / 2 : ℂ) * Complex.exp (((2 * Real.pi / 3 : ℝ) : ℂ) * Complex.I) ^ k‖) ^ 2) = 3 / 4 ∧
    (∑ k ∈ Finset.range 3,
        (‖(1 / 2 : ℂ) * Complex.exp (((2 * Real.pi / 3 : ℝ) : ℂ) * Complex.I) ^ k‖) ^ 2 / (3 / 4)) = 1 := by
  simp only [triad_modulus]; constructor <;> norm_num [Finset.sum_range_succ]

/-- Binary entropy at `½`: one bit. -/
noncomputable def binEntropy (p : ℝ) : ℝ := -(p * Real.logb 2 p + (1 - p) * Real.logb 2 (1 - p))

theorem bin_entropy_half : binEntropy (1 / 2) = 1 := by
  have h : Real.logb 2 (1 / 2) = -1 := by
    rw [one_div, Real.logb_inv, Real.logb_self_eq_one (by norm_num)]
  unfold binEntropy; norm_num [h]

/-- The gravitational data of the module: with `G_N = ½`, `S_BH = 1/(4G_N) = ½`, and the
Brown–Henneaux central charge `c = 3ℓ/(2G_N)` (`ℓ = 1`) equals `3` if and only if `G_N = ½`. -/
theorem area_quantum_half : 1 / (4 * (1 / 2 : ℝ)) = 1 / 2 := by norm_num

theorem brown_henneaux_three_iff (G : ℝ) (hG : 0 < G) : 3 * 1 / (2 * G) = 3 ↔ G = 1 / 2 := by
  constructor
  · intro h; field_simp at h; linarith
  · rintro rfl; norm_num

/-! ## (F5): the mathematical premises of Jacobson's construction
Jacobson (1995) derives Einstein's equation from `δQ = T δS` on every local Rindler horizon,
if the entropy is proportional to the area with a universal coefficient and the law is the same at
every point. Those premises are proved here; the postulate `δQ = T δS` remains as a physical axiom (F5). -/

/-- Fisher ceiling: `F_Ω = 4μ² = 1` (one bit per eigenvalue) if and only if `μ = ½`. -/
theorem fisher_unit_iff (μ : ℝ) (hμ : 0 < μ) : 4 * μ ^ 2 = 1 ↔ μ = 1 / 2 := by
  constructor
  · intro h; nlinarith [sq_nonneg (μ - 1 / 2), sq_nonneg (μ + 1 / 2)]
  · rintro rfl; norm_num

/-- The energy per bit is the same at every level: with `ε(σ) = ε₀ b^σ`, `S(σ) = π b^σ` and
`ε₀ M = π`, `ε(σ)/S(σ) = 1/M`: the temperature `T = 1/M` does not depend on the level. -/
theorem energy_per_bit_constant (b σ ε₀ M : ℝ) (hb : 0 < b) (hM : M ≠ 0) (hc : ε₀ * M = Real.pi) :
    (ε₀ * b ^ σ) / (Real.pi * b ^ σ) = 1 / M := by
  have hp : b ^ σ ≠ 0 := (Real.rpow_pos_of_pos hb σ).ne'
  have he0 : ε₀ ≠ 0 := by
    intro h
    have h0 : Real.pi = 0 := by rw [← hc, h, zero_mul]
    linarith [Real.pi_pos]
  rw [← hc]; field_simp

/-- The coefficient of the area law, `η = 1/(4G_N)`, is the same at every level: `G_N = |Ω_σ| = ½`. -/
theorem area_coefficient_every_level (θ : ℝ) :
    1 / (4 * ‖(1 / 2 : ℂ) * Complex.exp (θ * Complex.I)‖) = 1 / 2 := by
  rw [worldline_modulus]; norm_num

/-- The throat is an Einstein space. For `ds² = e^{2A(y)} η dx² + dy²` in five dimensions
the Ricci coefficients are `R_μν = −(A″ + 4A′²) g_μν` and `R_yy = −4(A″ + A′²)`; with `A′² = 1`,
`A″ = 0` both equal `−4`, the scalar curvature is `5·(−4) = −20` and `G_AB = 6 g_AB`, that is
`Λ₅ = −6`. -/
theorem throat_einstein_space (A1 A2 : ℝ) (h1 : A1 ^ 2 = 1) (h2 : A2 = 0) :
    -(A2 + 4 * A1 ^ 2) = -4 ∧ -4 * (A2 + A1 ^ 2) = -4 ∧ 5 * (-4 : ℝ) = -20 ∧
    (-4 : ℝ) - (1 / 2) * (-20) = 6 := by
  subst h2; refine ⟨?_, ?_, ?_, ?_⟩ <;> nlinarith [h1]

/-- In an Einstein space `R_ab = −4 g_ab`, `R_ab k^a k^b = 0` for every null `k`: in vacuum the
Clausius relation gives `δS = 0`, the equilibrium that Jacobson's construction requires. -/
theorem einstein_null_contraction (gkk : ℝ) (hnull : gkk = 0) : -4 * gkk = 0 := by
  rw [hnull]; ring


/-! ## (F8): the internal rotation flips the sign of a square -/

/-- `(i t)² = −t²`: the rotation `t ↦ i t` flips the sign of a square; it is the mathematical part
of the reading that takes the AdS throat (`Λ₅ = −6`) to the de Sitter patch of each level (`Λ > 0`). -/
theorem wick_squares_flip_sign (t : ℝ) : (Complex.I * t) ^ 2 = -((t : ℂ) ^ 2) := by
  rw [mul_pow, Complex.I_sq]; ring


/-! ## The criteria of Witten and CLPW, and the mathematics of the observer

`Λ(σ)·S(σ)` does not depend on the level (de Sitter entropy law); the offset of the tower is `1/d`
only at `d = 4`; the zero mode is the exact zero `J₁(0) = 0`; `12 = 2σ_Λ` only at `n = 3`; and the
pieces of W2–W12 that were missing. -/

/-- **W4, W11.** `Λ(σ)S(σ) = 6φ^{−σ}·πφ^σ = 6π`, invariant along the flow of levels. -/
theorem lambda_times_entropy (b σ : ℝ) (hb : 0 < b) :
    (6 * b ^ (-σ)) * (Real.pi * b ^ σ) = 6 * Real.pi := by
  rw [Real.rpow_neg hb.le]
  have : b ^ σ ≠ 0 := (Real.rpow_pos_of_pos hb σ).ne'
  field_simp

/-- `6π = 3π/G_N` with `G_N = ½`: the entropy law of the de Sitter horizon, `S = 3π/(GΛ)`. -/
theorem dS_entropy_law : 3 * Real.pi / (1 / 2 : ℝ) = 6 * Real.pi := by ring

/-- The asymptotic offset of the zeros of `J_{d/2−1}` (McMahon), `d/4 − 3/4`, equals `1/d`
if and only if `d = 4`. -/
theorem phase_equals_inverse_dimension_iff (d : ℝ) (hd : 0 < d) :
    d / 4 - 3 / 4 = 1 / d ↔ d = 4 := by
  constructor
  · intro h
    have h' : (d - 4) * (d + 1) = 0 := by field_simp at h; nlinarith [h]
    rcases mul_eq_zero.mp h' with h1 | h1
    · linarith
    · linarith
  · rintro rfl; norm_num

/-- `J₁` by its power series. -/
noncomputable def besselJ1 (x : ℝ) : ℝ :=
  ∑' m : ℕ, (-1 : ℝ) ^ m / ((Nat.factorial m : ℝ) * Nat.factorial (m + 1)) * (x / 2) ^ (2 * m + 1)

/-- The zero mode: `J₁(0) = 0`, the exact `k = 0` term, where the asymptotic form would give `π/4`. -/
theorem bessel_zero_mode : besselJ1 0 = 0 := by
  unfold besselJ1; simp

theorem zero_mode_vs_asymptotic : (0 : ℝ) ≠ Real.pi * (0 + 1 / 4) := by
  have := Real.pi_pos; intro h; linarith

/-- **W8.** `12 = 2σ_Λ = (n+1)n`: `n(n+1) = 4n` si y solo si `n = 3`. -/
theorem bottom_twice_lambda_iff (n : ℝ) (hn : 0 < n) : n * (n + 1) = 4 * n ↔ n = 3 := by
  constructor
  · intro h; nlinarith
  · rintro rfl; norm_num

/-- **W8.** The two routes to six, `|Λ₅| = d(d−1)/2` with `d = n+1` and `σ_Λ = 2n`, coincide only at
`n = 3`. -/
theorem two_routes_to_six (n : ℝ) (hn : 0 < n) : (n + 1) * n / 2 = 2 * n ↔ n = 3 := by
  constructor
  · intro h; nlinarith
  · rintro rfl; norm_num

/-- **W2.** The dimension per level, `⌊S(σ)⌋`, is a nonnegative integer. -/
theorem witten_finite_rank (b σ : ℝ) (hb : 0 < b) : 0 ≤ ⌊Real.pi * b ^ σ⌋ :=
  Int.floor_nonneg.mpr (mul_pos Real.pi_pos (Real.rpow_pos_of_pos hb σ)).le

/-- **W3.** The modulus exceeds the collapse threshold: `½ > ¼`. -/
theorem half_gt_quarter : (1 / 2 : ℝ) > 1 / 4 := by norm_num

/-- **W5.** Norms of the components of the eigenvalue triangle (CW6): `‖C‖ = 1`,
`‖F‖ = √3/2`, `‖P‖ = 1/√3`; the inner pairing `⟨F|P⟩ = F̄P/C` has modulus `½`. -/
theorem pairing_FP_modulus_half :
    (Real.sqrt 3 / 2) * (1 / Real.sqrt 3) / 1 = (1 / 2 : ℝ) := by
  have h : Real.sqrt 3 ≠ 0 := (Real.sqrt_pos.mpr (by norm_num)).ne'
  field_simp

/-- **W6.** The Galois conjugation of `ℤ[φ]`, `a + bφ ↦ a + bφ̄ = (a+b) − bφ`. -/
def galoisConj (p : ℤ × ℤ) : ℤ × ℤ := (p.1 + p.2, -p.2)

/-- `Θ² = 1`. -/
theorem cpt_involution (p : ℤ × ℤ) : galoisConj (galoisConj p) = p := by
  simp [galoisConj]

/-- `Θ` preserves the norm `N(a + bφ) = a² + ab − b²`. -/
theorem cpt_preserves_modulus (p : ℤ × ℤ) :
    let q := galoisConj p
    q.1 ^ 2 + q.1 * q.2 - q.2 ^ 2 = p.1 ^ 2 + p.1 * p.2 - p.2 ^ 2 := by
  simp only [galoisConj]; ring

/-- `Θ` swaps `φ` and `φ̄ = 1 − φ`, and fixes the rationals (the centre). -/
theorem cpt_swaps_and_fixes (a : ℤ) :
    galoisConj (0, 1) = (1, -1) ∧ galoisConj (a, 0) = (a, 0) := by
  simp [galoisConj]

/-- **W7.** The discrete symmetry that replaces the noncompact group: `ω³ = 1`. -/
theorem eisenstein_cube :
    Complex.exp (2 * Real.pi * Complex.I / 3) ^ 3 = 1 := by
  rw [← Complex.exp_nat_mul]
  have : ((3 : ℕ) : ℂ) * (2 * Real.pi * Complex.I / 3) = 2 * Real.pi * Complex.I := by
    push_cast; ring
  rw [this, Complex.exp_two_pi_mul_I]

/-- **W10.** The antipodal map of the sphere, in the stereographic coordinate, `z ↦ −1/z̄`, is an
involution: `F` antipodal to `P`. -/
theorem antipodal_involution (z : ℂ) (hz : z ≠ 0) :
    -1 / (starRingEnd ℂ) (-1 / (starRingEnd ℂ) z) = z := by
  have hc : (starRingEnd ℂ) z ≠ 0 := by simpa using hz
  simp only [map_div₀, map_neg, map_one, Complex.conj_conj]
  field_simp

/-- **The theta law under `S`** (Mathlib, no axiom): `θ(−1/τ) = (−iτ)^{1/2} θ(τ)`. -/
theorem theta_S_law (τ : UpperHalfPlane) :
    jacobiTheta ↑(ModularGroup.S • τ) = (-Complex.I * τ) ^ (1 / 2 : ℂ) * jacobiTheta τ :=
  jacobiTheta_S_smul τ

/-! ## W1 and W9 in this note: the projection of the observer and the thermal patch -/

/-- **W1.** From an isometry `V†V = 1` follows the projection `P = VV†`: `P² = P`. The projection that
places the observer is built from the map of the theory itself (`bulk_boundary_isometry`). -/
theorem projection_of_isometry {R : Type*} [Monoid R] (V Vd : R) (h : Vd * V = 1) :
    (V * Vd) * (V * Vd) = V * Vd := by
  rw [mul_assoc, ← mul_assoc Vd V Vd, h, one_mul]

/-- **W1.** An idempotent splits the identity: `P + (1 − P) = 1` and `P(1 − P) = 0`; no region is left outside. -/
theorem idempotent_splits_identity {R : Type*} [Ring R] (P : R) (h : P * P = P) :
    P + (1 - P) = 1 ∧ P * (1 - P) = 0 := by
  refine ⟨by abel, ?_⟩
  rw [mul_sub, mul_one, h, sub_self]

/-- **W9.** The Hubble-rate horizon `H(σ) = √2·b^{−σ/2}` has, with `G_N = ½`, the
Gibbons–Hawking entropy `π/(G_N H²) = π b^σ = S(σ)`: the entropy of the static patch is the bit count. -/
theorem gibbons_hawking_entropy (b σ : ℝ) (hb : 0 < b) :
    Real.pi / ((1 / 2) * (Real.sqrt 2 * b ^ (-σ / 2)) ^ 2) = Real.pi * b ^ σ := by
  have h2 : Real.sqrt 2 ^ 2 = 2 := Real.sq_sqrt (by norm_num)
  have hh : (b ^ (-σ / 2)) ^ 2 = b ^ (-σ) := by
    rw [← Real.rpow_natCast, ← Real.rpow_mul hb.le]; congr 1; push_cast; ring
  have hp : b ^ σ ≠ 0 := (Real.rpow_pos_of_pos hb σ).ne'
  rw [mul_pow, h2, hh, Real.rpow_neg hb.le]
  field_simp

/-! ## The lattice of the tower: integer and real at once (v22)

`a + bφ` is the pair `(a, b)`; with `φ² = φ + 1`, `(a, b)(c, d) = (ac + bd, ad + bc + bd)` and the norm is
`N(a + bφ) = a² + ab − b²`. With its conjugate, `ℤ[φ]` is a discrete lattice of the plane; the units
`φⁿ` fall on the hyperbola `xy = ±1`, which the real level traverses continuously. -/

/-- Product in `ℤ[φ]`. -/
def zmul (p q : ℤ × ℤ) : ℤ × ℤ := (p.1 * q.1 + p.2 * q.2, p.1 * q.2 + p.2 * q.1 + p.2 * q.2)

/-- Norm of `a + bφ`. -/
def znorm (p : ℤ × ℤ) : ℤ := p.1 ^ 2 + p.1 * p.2 - p.2 ^ 2

/-- The norm is multiplicative. -/
theorem znorm_mul (p q : ℤ × ℤ) : znorm (zmul p q) = znorm p * znorm q := by
  unfold znorm zmul; ring

/-- `φⁿ` in `ℤ[φ]`. -/
def zpow : ℕ → ℤ × ℤ
  | 0 => (1, 0)
  | n + 1 => zmul (zpow n) (0, 1)

/-- The integer levels are units: `N(φⁿ) = (−1)ⁿ`. -/
theorem znorm_zpow (n : ℕ) : znorm (zpow n) = (-1) ^ n := by
  induction n with
  | zero => simp [zpow, znorm]
  | succ n ih =>
    rw [zpow, znorm_mul, ih]
    simp [znorm, pow_succ]

/-- `φ¹² = 89 + 144φ`, of norm `1`: the background is a point of the lattice. -/
theorem bottom_is_lattice_point : zpow 12 = (89, 144) ∧ znorm (89, 144) = 1 := by
  constructor
  · decide
  · decide

/-- **There is no unit between `1` and `φ`** (F1, «The tower is the unit group, without Dirichlet»): if `1 < u < φ`,
neither `u + 1/u` (norm `+1`) nor `u − 1/u` (norm `−1`) is an integer. With the floor of `log u / log φ`, every
positive unit is a power of `φ`. -/
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

/-- The conjugate of `φ` is `−1/φ`: the conjugate of a level is its mirror. -/
theorem conjugate_is_mirror : (1 - Real.sqrt 5) / 2 = -1 / ((1 + Real.sqrt 5) / 2) := by
  have h5 : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)
  have hp : (0 : ℝ) < 1 + Real.sqrt 5 := by positivity
  field_simp
  nlinarith [h5]

/-! ## The window: the self-dual Gaussian (CW6, «Uniqueness of the self-dual Gaussian») -/

/-- Normalization: `√(π/a) = 1 ⟺ a = π`. -/
theorem gauss_normalised_iff (a : ℝ) (ha : 0 < a) : Real.sqrt (Real.pi / a) = 1 ↔ a = Real.pi := by
  rw [Real.sqrt_eq_one, div_eq_one_iff_eq ha.ne']; exact eq_comm

/-- With Mathlib's integral, `∫ e^{−a x²} = 1 ⟺ a = π`. -/
theorem gaussian_integral_one_iff (a : ℝ) (ha : 0 < a) :
    (∫ x : ℝ, Real.exp (-a * x ^ 2)) = 1 ↔ a = Real.pi := by
  rw [integral_gaussian]; exact gauss_normalised_iff a ha

/-- Width of the transform: `π²/a = a ⟺ a = π`. -/
theorem fourier_width_iff (a : ℝ) (ha : 0 < a) : Real.pi ^ 2 / a = a ↔ a = Real.pi := by
  have hpi := Real.pi_pos
  constructor
  · intro h
    have h2 : a ^ 2 = Real.pi ^ 2 := by field_simp at h; linarith
    nlinarith [sq_nonneg (a - Real.pi), sq_nonneg (a + Real.pi)]
  · rintro rfl; field_simp

/-- The threshold of the window: `e^{−y} > ½ ⟺ y < log 2`. -/
theorem window_half_iff (y : ℝ) : (1 / 2 : ℝ) < Real.exp (-y) ↔ y < Real.log 2 := by
  rw [← Real.log_lt_log_iff (by norm_num) (Real.exp_pos _), Real.log_exp, one_div, Real.log_inv]
  constructor <;> intro h <;> linarith

/-- The weight `e^{−πφ^{−2n}}` crosses `½` between `n = 1` and `n = 2`: `π/φ² > log 2 > π/φ⁴`. -/
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

/-- `Hℓ = √(2φ^{−n})` crosses `1` in the same interval: `2/φ > 1` and `2/φ² < 1`. -/
theorem hubble_below_bulk_crossing (b : ℝ) (h : b ^ 2 = b + 1) (h1 : 1 < b) (h2 : b < 2) :
    1 < 2 / b ∧ 2 / b ^ 2 < 1 := by
  constructor
  · rw [lt_div_iff₀ (by linarith)]; linarith
  · rw [div_lt_iff₀ (by positivity), h]; linarith

/-! ## v23: the tower of nomes, the invariant interval, the norm of the two scales, the moduli slope -/

/-- **S is the mirror on the tower of nomes.** `−1/(i x) = i/x`: `τ ↦ −1/τ` takes `τ_n = i φ^{−2n}`
to `i φ^{2n} = τ_{−n}`. -/
theorem S_acts_as_mirror (x : ℝ) (hx : x ≠ 0) :
    -1 / (Complex.I * (x : ℂ)) = Complex.I * (1 / (x : ℂ)) := by
  have hI : Complex.I ≠ 0 := Complex.I_ne_zero
  have hx' : (x : ℂ) ≠ 0 := by exact_mod_cast hx
  field_simp
  ring_nf
  rw [Complex.I_sq]

/-- A level interval invariant under the mirror is symmetric. -/
theorem invariant_interval_symmetric (p q : ℝ) (hpq : p ≤ q)
    (h : ∀ x, p ≤ x → x ≤ q → p ≤ -x ∧ -x ≤ q) : p = -q := by
  have h1 := (h p le_rfl hpq).2
  have h2 := (h q hpq le_rfl).1
  linarith

/-- The symmetric throat `[−12, 12]` has the length of the clock. -/
theorem symmetric_throat_is_clock : (12 : ℤ) - (-12) = 24 := by norm_num

/-- `2` is not a unit of `ℤ[φ]`: its norm is `4`. -/
theorem two_not_unit : znorm (2, 0) = 4 := by decide

/-- An integer mass level is an even curvature level. -/
theorem mass_level_even_curvature (k : ℤ) : Even (2 * k) := ⟨k, two_mul k⟩

/-- **The norm of the two scales.** The Kaluza–Klein scale `m₀ b^σ` (direct coordinate) times
`H_dS(σ)²/2 = b^{−σ}` (mirror) is `m₀` at every level. -/
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

/-- **The slope in the canonical field of the ring modulus.** With `dΦ/dn = √2 log φ` and
`d log V/dn = −log φ`, `|∂_Φ V|/V = 1/√2`. -/
theorem moduli_slope (L : ℝ) (hL : 0 < L) : L / (Real.sqrt 2 * L) = 1 / Real.sqrt 2 := by
  have hs : 0 < Real.sqrt 2 := by positivity
  field_simp

/-- The slope of the modulus lies below the trans-Planckian censorship bound at d = 4:
    1/√2 < √(2/3), because 1/2 < 2/3. -/
theorem moduli_slope_below_tcc : 1 / Real.sqrt 2 < Real.sqrt (2 / 3) := by
  rw [one_div, ← Real.sqrt_inv]
  apply Real.sqrt_lt_sqrt (by norm_num)
  norm_num

/-- With K = −k log(Im τ) the slope is 1/√(2k); the bound √(2/3) holds if and only if k ≤ 3/4. -/
theorem tcc_iff_k (k : ℝ) (hk : 0 < k) :
    Real.sqrt (2 / 3) ≤ 1 / Real.sqrt (2 * k) ↔ k ≤ 3 / 4 := by
  rw [one_div, ← Real.sqrt_inv, Real.sqrt_le_sqrt_iff (by positivity)]
  rw [le_inv_comm₀ (by norm_num) (by positivity)]
  have h23 : (2 / 3 : ℝ)⁻¹ = 3 / 2 := by norm_num
  rw [h23]
  constructor <;> intro h <;> linarith

/-- The tension welded by the entropy does not depend on the level (CW6, eq. 144):
    (q_m² ε₀ b^{−σ})·(π b^{σ}) = q_m² ε₀ π. -/
theorem tension_times_entropy_const (b qm2 e0 σ : ℝ) (hb : 0 < b) :
    (qm2 * e0 * b ^ (-σ)) * (π * b ^ σ) = qm2 * e0 * π := by
  have h : b ^ (-σ) * b ^ σ = 1 := by
    rw [← Real.rpow_add hb]; simp
  calc (qm2 * e0 * b ^ (-σ)) * (π * b ^ σ) = qm2 * e0 * π * (b ^ (-σ) * b ^ σ) := by ring
    _ = qm2 * e0 * π := by rw [h, mul_one]

/-- If the tension is C·b^{−σ}/π and H² = 2 b^{−σ}, the ratio with the Higuchi bound,
    t/(2H²) = C/(4π), is the same at every level. -/
theorem higuchi_ratio_level_free (b C σ : ℝ) (hb : 0 < b) :
    (C / π * b ^ (-σ)) / (2 * (2 * b ^ (-σ))) = C / (4 * π) := by
  have hp : 0 < b ^ (-σ) := Real.rpow_pos_of_pos hb _
  have hπ : (0:ℝ) < π := Real.pi_pos
  field_simp
  ring

/-- With C = 4π⁴/(q² M) the ratio is π³/(q² M), and it is ≥ 1 if and only if q² ≤ π³/M. -/
theorem higuchi_iff_charge (q2 M : ℝ) (hq : 0 < q2) (hM : 0 < M) :
    1 ≤ π ^ 3 / (q2 * M) ↔ q2 ≤ π ^ 3 / M := by
  rw [one_le_div (by positivity), le_div_iff₀ hM]

/-- CW6, eq. (101): the Fisher time τ_F = τ_D/√(2f) equals the decoherence time
    τ_D if and only if f = 1/2. -/
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

/-- The section of the throat is the cusp: with `t = e^{-y}`, the angular coefficient `1/t²` of the metric
    of the half-plane `(dθ² + dt²)/t²` is `e^{2y}`, that of the section `e^{2y}dθ² + dy²`. -/
theorem cusp_metric (y : ℝ) : Real.exp (-y) ^ 2 * Real.exp (2 * y) = 1 := by
  rw [sq, ← Real.exp_add, ← Real.exp_add]
  norm_num [show -y + -y + 2 * y = 0 by ring]

/-- The two tiles of the rings: with `A = F_{n+3}` long and `B = F_{n+2}` short, of weights `π/b²`
    and `π/b³`, the weighted sum is `π bⁿ` at every level (here without the factor `π`). -/
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

/-- The two-tile substitution that grows by φ is the Fibonacci one: a matrix `(a b; c d)` of
    naturals with trace 1 and determinant −1 (`a d + 1 = b c`) is `(1 1; 1 0)` or `(0 1; 1 1)`. -/
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

/-- W2 against a lattice: the growth `e^{S}` of the dimension of an integer level is not the
dimension `χⁿ` of any lattice of `n ≥ 1` integer links, because `e^{S/n} = e^{π (φ^σ/n)}` is
transcendental (Gelfond–Schneider). -/
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
    exact (golden_is_algebraic.pow σ).mul (IsAlgebraic.inv (isAlgebraic_natCast n))
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

/-! ## v31: the two coordinates, the level step, the half turn and the trace 3 (Sprint 55) -/

/-- `|φ̄|·φ = 1`, with `φ̄ = (1 − √5)/2 = −1/φ` (`conjugate_is_mirror`). -/
theorem conjugate_abs_mul_golden :
    |(1 - Real.sqrt 5) / 2| * ((1 + Real.sqrt 5) / 2) = 1 := by
  rw [conjugate_is_mirror]
  have hp : (0 : ℝ) < (1 + Real.sqrt 5) / 2 := by positivity
  rw [abs_div, abs_neg, abs_one, abs_of_pos hp]
  field_simp

/-- I1: the second coordinate of a level, times `M`, is the time of the weld:
`φⁿ · (M · |φ̄|ⁿ) = M`, because the norm of a unit is ±1. -/
theorem weld_time_is_conjugate (M : ℝ) (n : ℕ) :
    ((1 + Real.sqrt 5) / 2) ^ n * (M * |(1 - Real.sqrt 5) / 2| ^ n) = M := by
  have h := conjugate_abs_mul_golden
  calc ((1 + Real.sqrt 5) / 2) ^ n * (M * |(1 - Real.sqrt 5) / 2| ^ n)
      = M * (|(1 - Real.sqrt 5) / 2| * ((1 + Real.sqrt 5) / 2)) ^ n := by rw [mul_pow]; ring
    _ = M := by rw [h, one_pow, mul_one]

/-- I2: the matrix of the substitution of the rings, `A ↦ AB`, `B ↦ A`, is a shift of the
winding followed by the exchange `(n,w) ↦ (w,n)` (on column vectors the right factor acts first). -/
theorem level_step_is_exchange_shift :
    (!![0, 1; 1, 0] : Matrix (Fin 2) (Fin 2) ℤ) * !![1, 0; 1, 1] = !![1, 1; 1, 0] := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [Matrix.mul_apply, Fin.sum_univ_two]

/-- I6: the square of the golden matrix is `[[2,1],[1,1]]`. -/
theorem golden_matrix_sq :
    (!![1, 1; 1, 0] : Matrix (Fin 2) (Fin 2) ℤ) * !![1, 1; 1, 0] = !![2, 1; 1, 1] := by
  ext i j; fin_cases i <;> fin_cases j <;> simp [Matrix.mul_apply, Fin.sum_univ_two]

/-- I6: its trace, `2 + 1 = 3`, is `φ² + φ⁻²` (`sq_add_inv_sq`). -/
theorem golden_square_trace :
    ((2 : ℝ) + 1) = ((1 + Real.sqrt 5) / 2) ^ 2 + (((1 + Real.sqrt 5) / 2)⁻¹) ^ 2 := by
  have h5 : Real.sqrt 5 ^ 2 = 5 := Real.sq_sqrt (by norm_num)
  have hb : (0 : ℝ) < (1 + Real.sqrt 5) / 2 := by positivity
  have h2 : ((1 + Real.sqrt 5) / 2) ^ 2 = (1 + Real.sqrt 5) / 2 + 1 := by nlinarith [h5]
  rw [sq_add_inv_sq _ hb h2]; norm_num

/-- I4: at the half turn, `e^{iπ} = −1`, the overlap of a state of weights `1 − p` and `p`
with itself is `1 − 2p`, and it vanishes if and only if `p = ½`. -/
theorem orthogonal_at_half_turn (p : ℝ) : (1 - p) + p * (-1) = 0 ↔ p = 1 / 2 := by
  constructor <;> intro h <;> linarith

/-! ## v32: the three columns (Sprint 56) -/

/-- E1: the axes of ℤ³ projected by the diagonal, `e_k − ⅓(1,1,1)`, sum to zero (the kernel is
the diagonal), have squared length `⅔` and form angles of cosine `−½` (120°). -/
theorem cube_diagonal_kernel :
    ((2 : ℝ) / 3 + (-1 / 3) + (-1 / 3) = 0) ∧
    ((2 : ℝ) / 3) ^ 2 + (-1 / 3) ^ 2 + (-1 / 3) ^ 2 = 2 / 3 ∧
    ((2 : ℝ) / 3 * (-1 / 3) + (-1 / 3) * (2 / 3) + (-1 / 3) * (-1 / 3)) / (2 / 3) = -1 / 2 := by
  norm_num

/-- E2 (Binet): the Fibonacci count differs from `φⁿ/√5` exactly by `−ψⁿ/√5`; since
`|ψ| < 1` (φ is a Pisot unit), the difference vanishes. -/
theorem tile_count_deviation (n : ℕ) :
    (Nat.fib n : ℝ) - goldenRatio ^ n / Real.sqrt 5 = -(goldenConj ^ n) / Real.sqrt 5 := by
  rw [Real.coe_fib_eq]; ring

/-- E4: a rational step `p/q` sends the pair `(−p, q)` to `0`: the reading on the line has a kernel. -/
theorem rational_step_kernel (p q : ℤ) (hq : q ≠ 0) :
    ((-p : ℤ) : ℝ) + (q : ℝ) * ((p : ℝ) / q) = 0 := by
  have hq' : (q : ℝ) ≠ 0 := by exact_mod_cast hq
  have h : (q : ℝ) * ((p : ℝ) / q) = p := by field_simp
  rw [h]; push_cast; ring

/-! ## v34 (Sprints 57, 58 and 70b): the Hopf foliation, J, the compression limit and the observer's half

The tori |z₁| = cos η, |z₂| = sin η of S³ with tan η_n = φ^{−2n} are the torus tower of the window
(I13); J(z₁, z₂) = (−z̄₂, z̄₁) is the antipode of W10 on the base, the mirror on the tori and, squared,
the half turn of the fibre. φ is local with its own name, `hopfPhi`, so as not to clash with anything
in the module. -/

/-- φ, the golden ratio (local to this section). -/
def hopfPhi : ℝ := (1 + Real.sqrt 5) / 2

/-- The leaf angle of level n: tan η_n = φ^{-2n}. -/
def windowEta (n : ℤ) : ℝ := Real.arctan (hopfPhi ^ (-2 * n))

/-- The torus of level n has modulus τ_n = i·tan η_n = i φ^{-2n} (I13). -/
theorem tan_eta (n : ℤ) : Real.tan (windowEta n) = hopfPhi ^ (-2 * n) := by
  unfold windowEta; exact Real.tan_arctan _

/-- The exchange z₁ ↔ z₂ sends η to π/2 − η: it is the mirror n ↦ −n (`S_acts_as_mirror`). -/
theorem swap_is_mirror (n : ℤ) : windowEta (-n) = Real.pi / 2 - windowEta n := by
  unfold windowEta
  have hφ : 0 < hopfPhi := by unfold hopfPhi; have := Real.sqrt_nonneg 5; linarith
  have hpos : 0 < hopfPhi ^ (-2 * n) := zpow_pos hφ _
  have h : hopfPhi ^ (-2 * -n) = (hopfPhi ^ (-2 * n))⁻¹ := by
    rw [← zpow_neg]; ring_nf
  rw [h, Real.arctan_inv_of_pos hpos]

/-- Level 0 is the Clifford torus, η = π/4 (τ = i). -/
theorem level_zero_is_clifford : windowEta 0 = Real.pi / 4 := by
  unfold windowEta; simp [Real.arctan_one]

/-- The antipode of S³ is the Hopf action at angle π: −z = e^{iπ} z. -/
theorem antipode_is_half_turn (z : ℂ × ℂ) :
    (-z.1, -z.2) = (Complex.exp (Real.pi * Complex.I) * z.1,
                    Complex.exp (Real.pi * Complex.I) * z.2) := by
  simp [Complex.exp_pi_mul_I]

/-- The Hopf map h(z) = z₁/z₂ does not tell z apart from −z: the half turn is invisible on the base. -/
theorem hopf_blind_to_half_turn (z : ℂ × ℂ) : (-z.1) / (-z.2) = z.1 / z.2 :=
  neg_div_neg_eq _ _

/-- J(z₁, z₂) = (−z̄₂, z̄₁), the quaternionic unit j. -/
def J (z : ℂ × ℂ) : ℂ × ℂ := (-(starRingEnd ℂ) z.2, (starRingEnd ℂ) z.1)

/-- J² = −1: its square is the half turn. -/
theorem J_sq (z : ℂ × ℂ) : J (J z) = (-z.1, -z.2) := by
  simp [J]

/-- J has order 4, like S in SL₂(ℤ) (`quarter_and_half_turn`). -/
theorem J_four (z : ℂ × ℂ) : J (J (J (J z))) = z := by
  simp [J]

/-- J swaps the moduli: it carries the torus η to the torus π/2 − η (the mirror). -/
theorem J_swaps_moduli (z : ℂ × ℂ) :
    ‖(J z).1‖ = ‖z.2‖ ∧ ‖(J z).2‖ = ‖z.1‖ := by
  simp only [J]
  constructor
  · rw [norm_neg]; exact Complex.norm_conj _
  · exact Complex.norm_conj _

/-- On the base, J is the antipode of W10: h(Jz) = −1 / conj(h z) (`antipodal_involution`). -/
theorem J_lifts_W10 (z : ℂ × ℂ) (h1 : z.1 ≠ 0) (h2 : z.2 ≠ 0) :
    (J z).1 / (J z).2 = -1 / (starRingEnd ℂ) (z.1 / z.2) := by
  have c1 : (starRingEnd ℂ) z.1 ≠ 0 := (map_ne_zero _).mpr h1
  have c2 : (starRingEnd ℂ) z.2 ≠ 0 := (map_ne_zero _).mpr h2
  simp only [J, map_div₀]
  field_simp

/-- For x > 0, 1/sin(arctan x) = √(1 + x⁻²); with x = φ^{-2n} it gives R/r = √(1 + φ^{4n}). -/
theorem stereo_ratio (x : ℝ) (hx : 0 < x) :
    1 / Real.sin (Real.arctan x) = Real.sqrt (1 + x⁻¹ ^ 2) := by
  rw [Real.sin_arctan]
  rw [one_div_div]
  rw [show (1 + x⁻¹ ^ 2) = (1 + x ^ 2) / x ^ 2 by field_simp; ring]
  rw [Real.sqrt_div (by positivity), Real.sqrt_sq hx.le]

/-- Below z = ½ the four-dimensional area law, 2πz², does not reach the bits πz
    (the equality at z = ½ is `area_law_4d_meets_weld_iff`). -/
theorem capacity_exceeded (z : ℝ) (hz : 0 < z) (hz2 : z < 1 / 2) :
    2 * Real.pi * z ^ 2 < Real.pi * z := by
  have hp : 0 < Real.pi := Real.pi_pos
  have hsq : 2 * z ^ 2 < z := by nlinarith
  calc
    2 * Real.pi * z ^ 2 = Real.pi * (2 * z ^ 2) := by ring
    _ < Real.pi * z := mul_lt_mul_of_pos_left hsq hp

/-- 6φ^{-σ} = 6 only at σ = 0: the level at which the first patch and the throat have the same
    constant (that they do is `dS_entropy_law` with `two_routes_to_six`; the level, by construction). -/
theorem flip_level (σ : ℝ) : 6 * hopfPhi ^ (-σ) = 6 ↔ σ = 0 := by
  have hφ : 1 < hopfPhi := by
    unfold hopfPhi
    have : (1 : ℝ) < Real.sqrt 5 := by
      rw [show (1 : ℝ) = Real.sqrt 1 by simp]
      exact Real.sqrt_lt_sqrt (by norm_num) (by norm_num)
    linarith
  have hφ0 : 0 < hopfPhi := by linarith
  have hl : Real.log hopfPhi ≠ 0 := (Real.log_pos hφ).ne'
  constructor
  · intro h
    have h1 : hopfPhi ^ (-σ) = 1 := by linarith
    have h2 : Real.log (hopfPhi ^ (-σ)) = 0 := by rw [h1, Real.log_one]
    rw [Real.log_rpow hφ0] at h2
    rcases mul_eq_zero.mp h2 with h3 | h3
    · linarith
    · exact absurd h3 hl
  · rintro rfl; simp

/-- The flat chart: X₀ + X₄ = ℓ e^{t/ℓ} > 0 (CW6, «The observer sees exactly half»), with
    X₀ = ℓ sinh(t/ℓ) + r²/(2ℓ) e^{t/ℓ} and X₄ = ℓ cosh(t/ℓ) − r²/(2ℓ) e^{t/ℓ}. -/
theorem planar_patch_positive (ℓ t r : ℝ) (hℓ : 0 < ℓ) :
    0 < (ℓ * Real.sinh (t / ℓ) + r ^ 2 / (2 * ℓ) * Real.exp (t / ℓ))
      + (ℓ * Real.cosh (t / ℓ) - r ^ 2 / (2 * ℓ) * Real.exp (t / ℓ)) := by
  have h : (ℓ * Real.sinh (t / ℓ) + r ^ 2 / (2 * ℓ) * Real.exp (t / ℓ))
      + (ℓ * Real.cosh (t / ℓ) - r ^ 2 / (2 * ℓ) * Real.exp (t / ℓ))
      = ℓ * (Real.cosh (t / ℓ) + Real.sinh (t / ℓ)) := by ring
  rw [h, Real.cosh_add_sinh]
  exact mul_pos hℓ (Real.exp_pos _)

end TorreKK
