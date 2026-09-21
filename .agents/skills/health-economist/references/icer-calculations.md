# Incremental Cost-Effectiveness Ratio (ICER) Reference Guide

## 1. Mathematical Definition

The Incremental Cost-Effectiveness Ratio (ICER) summarizes the economic value of an intervention compared to an alternative:

$$\text{ICER} = \frac{C_A - C_B}{E_A - E_B} = \frac{\Delta C}{\Delta E}$$

Where:
- $C_A, C_B$: Mean total expected costs of Strategy A (new intervention) and Strategy B (comparator/standard of care).
- $E_A, E_B$: Mean total expected health outcomes (typically QALYs or life years gained).
- $\Delta C$: Incremental cost.
- $\Delta E$: Incremental effectiveness.

---

## 2. The Cost-Effectiveness Plane

```text
               Incremental Cost (+ΔC)
                         │
        Quadrant II      │       Quadrant I
   INTERVENTION DOMINATED│   TRADE-OFF ZONE
    (Higher cost,        │    (Higher cost,
     lower effect)       │     higher effect)
                         │      ICER < λ: Cost-effective
                         │      ICER > λ: Not cost-effective
─────────────────────────┼─────────────────────────► Incremental Effect (+ΔE)
                         │
        Quadrant III     │       Quadrant IV
      TRADE-OFF ZONE     │  INTERVENTION DOMINANT
    (Lower cost,         │   (Lower cost,
     lower effect)       │    higher effect)
                         │
               Incremental Cost (-ΔC)
```

### Decision Rules by Quadrant:
- **Quadrant IV ($\Delta C < 0, \Delta E > 0$)**: **Dominant**. Intervention is cost-saving and more effective. Unambiguously adopt.
- **Quadrant II ($\Delta C > 0, \Delta E < 0$)**: **Dominated**. Intervention is more expensive and less effective. Unambiguously reject.
- **Quadrant I ($\Delta C > 0, \Delta E > 0$)**: **Trade-off**. Adopt if $\text{ICER} \le \lambda$ (willingness-to-pay threshold).
- **Quadrant III ($\Delta C < 0, \Delta E < 0$)**: **Trade-off**. Adopt if acceptable cost savings outweigh health reduction ($\text{ICER} \ge \lambda$).

---

## 3. Standard Willingness-to-Pay (WTP, $\lambda$) Thresholds

| Jurisdiction / Agency | Standard Threshold ($\lambda$) | End-of-Life / Highly Innovative |
|-----------------------|--------------------------------|---------------------------------|
| **UK (NICE)** | £20,000 – £30,000 / QALY | £50,000 / QALY |
| **United States (ICER / ACC/AHA)** | $50,000 – $100,000 / QALY | $150,000 / QALY |
| **Canada (CADTH)** | $50,000 CAD / QALY | Evaluated case-by-case |
| **Australia (PBAC)** | $45,000 – $75,000 AUD / QALY | Special access provisions |
| **WHO (Low/Middle Income)** | $1 \times \text{GDP per capita}$ (very cost-effective) | $3 \times \text{GDP per capita}$ (cost-effective) |

---

## 4. Annual Discounting Formula

For outcomes occurring over a time horizon $t = 0, \dots, T$:

$$PV = \sum_{t=0}^{T} \frac{X_t}{(1 + r)^t}$$

Where:
- $X_t$: Cost or effect occurring in year $t$.
- $r$: Annual real discount rate (UK NICE: 3.5%; US Panel: 3.0%).
- Half-cycle corrections should be applied when state transitions occur continuously over discrete cycles.
