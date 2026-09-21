# Health Technology Assessment Report: SGLT2 Inhibitor Add-on in Type 2 Diabetes & Chronic Kidney Disease

**Author**: Health Economics & Outcomes Research (HEOR) Core  
**Perspective**: UK National Health Service (NHS) & Personal Social Services  
**Time Horizon**: Lifetime (40-year horizon)  
**Discount Rate**: 3.5% per annum for both costs and health benefits  
**Base Year**: 2025 GBP (£)  

---

## 1. Executive Summary

- **Intervention**: Empagliflozin (10mg daily) added to Standard of Care (ACEi/ARB).
- **Comparator**: Standard of Care (ACEi/ARB monotherapy + placebo).
- **Model Structure**: 4-state Markov cohort model (CKD Stages 3a/b, CKD Stage 4, End-Stage Kidney Disease requiring Dialysis/Transplant, and Death).
- **Results**:
  - Incremental Cost: £4,850
  - Incremental Health Gain: 0.38 QALYs
  - **Base-case ICER**: £12,763 per QALY gained
- **Conclusion**: At the UK NICE willingness-to-pay threshold of £20,000 per QALY, add-on Empagliflozin is **cost-effective** with an 89.4% probability of cost-effectiveness in Probabilistic Sensitivity Analysis (PSA).

---

## 2. Base-Case Economic Evaluation Table

| Strategy | Total Lifetime Costs (£) | Total Discounted QALYs | Incremental Cost ($\Delta C$) | Incremental QALYs ($\Delta E$) | ICER (£/QALY) |
|---|---|---|---|---|---|
| **Standard of Care (SoC)** | £28,420 | 7.12 | — | — | — (Reference) |
| **SGLT2i + SoC** | £33,270 | 7.50 | +£4,850 | +0.38 | **£12,763** |

---

## 3. Decision Model Structure & Key Parameters

### Markov Health States
1. **State 1: Moderate CKD (eGFR 30–59 mL/min/1.73m²)**: Annual utility = $0.78$; Annual NHS cost = £1,120.
2. **State 2: Severe CKD (eGFR 15–29 mL/min/1.73m²)**: Annual utility = $0.66$; Annual NHS cost = £3,450.
3. **State 3: ESKD (Dialysis / Renal Replacement Therapy)**: Annual utility = $0.44$; Annual NHS cost = £32,800.
4. **State 4: All-Cause Death (Absorbing State)**: Utility = $0.0$; Cost = £0.

### Clinical Trial Inputs (EMPA-KIDNEY pooled estimates)
- Hazard Ratio for progression to ESKD: $0.72$ (95% CI: $0.64 – 0.82$).
- Hazard Ratio for cardiovascular death: $0.86$ (95% CI: $0.75 – 0.99$).
- Annual acquisition cost of Empagliflozin: £447.20.

---

## 4. Sensitivity Analyses

### 1. Deterministic One-Way Sensitivity Analysis (Tornado Diagram Bounds)
- When ESKD annual dialysis cost varied by $\pm 20\%$ (£26,240 to £39,360): ICER ranged from £15,120 down to £10,400.
- When discount rate varied between 0% and 6%: ICER ranged from £9,800 to £16,250.

### 2. Probabilistic Sensitivity Analysis (10,000 Monte Carlo Iterations)
- At £20,000/QALY threshold: **89.4%** cost-effective.
- At £30,000/QALY threshold: **97.8%** cost-effective.
