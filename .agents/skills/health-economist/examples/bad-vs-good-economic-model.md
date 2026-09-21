# Comparative Analysis: Common Flaws vs Rigorous Practice in Health Economic Models

## Summary Table of Critical Differences

| Evaluation Dimension | ❌ Flawed / Anti-Pattern Approach | ✅ Rigorous / Methodological Standard |
|---|---|---|
| **Perspective** | Unstated or mixed (e.g. counting patient travel expenses in an NHS payer model without societal framework). | Explicitly declared as Healthcare Payer, Provider, or Societal with all costs strictly mapped to that perspective. |
| **Time Horizon** | Truncated to 1-year trial follow-up for chronic illnesses, omitting delayed downstream dialysis/death costs. | Lifetime horizon extrapolated using parametric survival distributions (Weibull, Gompertz) with clinical validation. |
| **Discounting** | Omitted ($r=0\%$) or applied only to costs while leaving health benefits undiscounted. | Consistent 3.0% - 3.5% discount applied annually to both monetary costs and QALY gains with half-cycle correction. |
| **Utility Values** | Arbitrarily guessed ("feels like 80% health = 0.80") without validated instrument source. | Elicited using validated Multi-Attribute Utility Instruments (e.g. EQ-5D-5L) mapped to published country tariffs. |
| **Comparator** | Compared to "no treatment" or an outdated off-patent agent no longer used in standard practice. | Compared to contemporary clinical Standard of Care (SoC) recommended by relevant national clinical guidelines. |
| **Sensitivity Analysis** | Only base-case point estimate reported; zero variance or confidence intervals reported. | Comprehensive: Deterministic Tornado diagrams for parameter drivers + Probabilistic Sensitivity Analysis (PSA, 5k-10k runs). |
| **Dominance Testing** | Calculated an ICER with negative denominator without checking dominance quadrant. | Explicitly tested for strict and extended dominance before calculating pairwise incremental ratios. |
