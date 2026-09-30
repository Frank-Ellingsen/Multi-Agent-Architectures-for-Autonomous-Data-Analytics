---
name: storytelling-with-data-pbi
description: >-
  Transform complex ERP, accounting, staffing, and operational data into clear executive stories in Power BI
  grounded in Edward Tufte principles, YoY/MoM temporal context, RAG threshold rules, 3-30-300 visual hierarchy,
  and dynamic DAX narrative formatting.
---

# Storytelling with Data in Power BI (storytelling-with-data-pbi)

## Purpose
A production-grade framework and operational skill guide for transforming complex ERP, accounting, staffing, and operational data into clear, persuasive, and actionable executive stories in Power BI. Grounded in Edward Tufte's Data-Ink principles, temporal context (YoY and MoM comparisons), strict RAG (Red-Amber-Green) conditional formatting standards, the 3-30-300 visual hierarchy, and dynamic DAX narrative formatting.

## Core Philosophy: The "So What?" Framework
In executive and board reporting, data without context is noise. Move beyond passive record-keeping (*"what happened"*) to proactive decision support (*"why it happened and what leadership must do"*).

```
   [ DATA / ACTUALS ]          Bokført regnskap og operative tall (FactGL, FactFTE)
           │
           ▼
   [ TEMPORAL & PLAN CONTEXT ] Hvor står vi mot Budsjett (BAC), Fjorår (YoY) og Siste Måned (MoM)?
           │
           ▼
   [ RAG STATUS SIGNAL ]      Tydelig RAG-klassifisering (🟢 Grønn / 🟡 Gul / 🔴 Rød) basert på vesentlighet
           │
           ▼
   [ VARIANCE / DRIVERS ]     Hvorfor avviker vi fra plan og historikk? (Volum, Pris, Timing, Struktur)
           │
           ▼
   [ FORECAST / EAC ]         Hvor ender vi ved årets slutt dersom kursen holdes? (Latest Estimate)
           │
           ▼
   [ ACTION & IMPACT ]        Hvilke konkrete omstillingstiltak lukker gapet? (FactAction)
           │
           ▼
   [ DECISION SUPPORT ]       Hvilke 2–3 valg har ledelsen NÅ, og hva er konsekvensene?
```

### The 4 Golden Rules of Data Storytelling
1. **Lead with the Conclusion:** State the bottom line (Net Deficit/Surplus, Forecast EAC, CPI) before explaining details.
2. **Contextualize Every Metric (Plan, YoY & MoM):** Never show an isolated number. Pair actuals with baseline budget targets (BAC), Year-over-Year (YoY) trends, and Month-over-Month (MoM) momentum.
3. **Apply Strict RAG Formatting:** Highlight material variances using Tufte-compliant RAG standards. Mute normal performance; let critical exceptions (>5% variance or negative YoY momentum) draw immediate focus.
4. **Action-Oriented Annotations:** Use dynamic labels and tooltips to explain *why* an anomaly occurred.

## RAG Formatting Standards & Threshold Rules

### RAG Threshold Matrix

| Category | Indicator / Metric | 🟢 Green (Favorable) | 🟡 Amber (Warning) | 🔴 Red (Alert / Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Budget Variance (VAC %)** | `[Sluttavvik %]` | `VAC % >= 0.0%` (In/Under budget) | `-5.0% <= VAC % < 0.0%` (2–5% overskridelse) | `VAC % < -5.0%` (>5% overskridelse) |
| **YoY Revenue Growth** | `[Actual YoY %]` | `YoY % >= +3.0%` (Solid vekst) | `-2.0% <= YoY % < +3.0%` (Flat trend) | `YoY % < -2.0%` (Betydelig nedgang) |
| **MoM Momentum** | `[Actual MoM %]` | `MoM % >= +0.0%` (Positiv driv) | `-2.0% <= MoM % < 0.0%` (Mild avdemping) | `MoM % < -2.0%` (Skarp nedgang) |
| **EVM Cost Index (CPI)** | `[CPI]` | `CPI >= 1.00` (I/Under budsjett) | `0.90 <= CPI < 1.00` (Moderat overskridelse) | `CPI < 0.90` (Kritisk overskridelse) |
| **EVM Schedule Index (SPI)**| `[SPI]` | `SPI >= 1.00` (I/Foran rute) | `0.90 <= SPI < 1.00` (Moderat forsinkelse) | `SPI < 0.90` (Kritisk forsinkelse) |
| **Labor Share %** | `[Lønnsandel %]` | `Lønnsandel <= 65.0%` (Sektornorm) | `65.0% < Lønnsandel <= 67.0%` (Påkrevd obs) | `Lønnsandel > 67.0%` (Høy risiko) |
| **Student Density** | `[Studenter/UF-ÅV]` | `Ratio >= 18.0` (Høy produksjon)| `14.0 <= Ratio < 18.0` (Normal) | `Ratio < 14.0` (Lav lærerkapasitet) |

### Edward Tufte Data-Ink Rules for RAG
- **Never Use Solid Neon Fills:** Avoid saturated solid fills across large table cells or bar backgrounds.
- **Use Soft Fills (85% Transparency) or Indicator Circles:** Apply background fills with low opacity (`#FEF2F2` for soft red, `#ECFDF5` for soft green) or Unicode icons (`🟢`, `🟡`, `🔴`).
- **Semantic Color Palette:**
  - Emerald Green: `#10B981` (Foreground) | `#ECFDF5` (Soft Background)
  - Amber Yellow: `#F59E0B` (Foreground) | `#FFFBEB` (Soft Background)
  - Crimson Red: `#EF4444` (Foreground) | `#FEF2F2` (Soft Background)
  - Muted Neutral Gray: `#94A3B8` (Baseline)

## Visual Hierarchy: The 3-30-300 Rule
Structure every Power BI dashboard canvas into three visual layers:
- **3 SECONDS (Top Row):** 5 KPI Card visuals providing immediate executive summary status.
- **30 SECONDS (Middle Section):** Trend line chart (60% width) + Diverging horizontal bar chart (40% width) showing unit variance breakdown.
- **300 SECONDS (Bottom Section):** Comprehensive Faculty/Department Matrix with RAG badges and metric drill-down.
