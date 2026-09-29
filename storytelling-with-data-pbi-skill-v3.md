# SKILL: Storytelling with Data in Power BI (Executive Reporting, RAG Formatting & Decision Support)

> **Purpose:** A production-grade framework and operational skill guide for transforming complex ERP, accounting, staffing, and operational data into clear, persuasive, and actionable executive stories in Power BI. Grounded in Edward Tufte's Data-Ink principles, temporal context (YoY and MoM comparisons), strict RAG (Red-Amber-Green) conditional formatting standards, the 3-30-300 visual hierarchy, and dynamic DAX narrative formatting.

---

## 1. Core Philosophy: The "So What?" Framework

In executive and board reporting, data without context is noise. A financial or operational controller must move beyond passive record-keeping (*"what happened"*) to proactive decision support (*"why it happened and what leadership must do"*).

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
1. **Lead with the Conclusion:** State the bottom line (Net Deficit/Surplus, Forecast EAC, CPI) before explaining the details.
2. **Contextualize Every Metric (Plan, YoY & MoM):** Never show an isolated number. Always pair actuals with baseline budget targets (BAC), Year-over-Year (YoY) historical trends, and Month-over-Month (MoM) short-term momentum.
3. **Apply Strict RAG Formatting:** Highlight material variances instantly using Tufte-compliant RAG standards. Mute normal performance; let critical exceptions (>5% variance or negative YoY momentum) draw immediate executive focus.
4. **Action-Oriented Annotations:** Use dynamic labels and tooltips to explain *why* an anomaly occurred rather than leaving executives to guess.

---

## 2. RAG Formatting Standards & Threshold Rules

Red-Amber-Green (RAG) conditional formatting provides immediate evaluative context. However, poorly implemented RAG creates visual clutter ("chartjunk"). Follow these strict rules:

### A. RAG Threshold Matrix

| Category | Indicator / Metric | 🟢 Green (Favorable) | 🟡 Amber (Warning) | 🔴 Red (Alert / Critical) |
| :--- | :--- | :--- | :--- | :--- |
| **Budget Variance (VAC %)** | `[Sluttavvik %]` | `VAC % >= 0.0%` (In/Under budget) | `-5.0% <= VAC % < 0.0%` (2–5% overskridelse) | `VAC % < -5.0%` (>5% overskridelse) |
| **YoY Revenue Growth** | `[Actual YoY %]` | `YoY % >= +3.0%` (Solid vekst) | `-2.0% <= YoY % < +3.0%` (Flat trend) | `YoY % < -2.0%` (Betydelig nedgang) |
| **MoM Momentum** | `[Actual MoM %]` | `MoM % >= +0.0%` (Positiv driv) | `-2.0% <= MoM % < 0.0%` (Mild avdemping) | `MoM % < -2.0%` (Skarp nedgang) |
| **EVM Cost Index (CPI)** | `[CPI]` | `CPI >= 1.00` (I/Under budsjett) | `0.90 <= CPI < 1.00` (Moderat overskridelse) | `CPI < 0.90` (Kritisk overskridelse) |
| **EVM Schedule Index (SPI)**| `[SPI]` | `SPI >= 1.00` (I/Foran rute) | `0.90 <= SPI < 1.00` (Moderat forsinkelse) | `SPI < 0.90` (Kritisk forsinkelse) |
| **Labor Share %** | `[Lønnsandel %]` | `Lønnsandel <= 65.0%` (Sektornorm) | `65.0% < Lønnsandel <= 67.0%` (Påkrevd obs) | `Lønnsandel > 67.0%` (Høy risiko) |
| **Student Density** | `[Studenter/UF-ÅV]` | `Ratio >= 18.0` (Høy produksjon)| `14.0 <= Ratio < 18.0` (Normal) | `Ratio < 14.0` (Lav lærerkapasitet) |

### B. Edward Tufte Data-Ink Rules for RAG
* **Never Use Solid Neon Fills:** Avoid saturated solid fills across large table cells or bar backgrounds. They create heavy visual noise and fatigue.
* **Use Soft Fills (85% Transparency) or Indicator Circles:** Apply background fills with low opacity (`#FEF2F2` for soft red, `#ECFDF5` for soft green) or use explicit Unicode icons (`🟢`, `🟡`, `🔴`) next to the text label.
* **Semantic Color Palette:**
  * **Emerald Green:** `#10B981` (Foreground Icon / Bar Fill) | `#ECFDF5` (Soft Background Fill)
  * **Amber Yellow:** `#F59E0B` (Foreground Icon / Bar Fill) | `#FFFBEB` (Soft Background Fill)
  * **Crimson Red:** `#EF4444` (Foreground Icon / Bar Fill) | `#FEF2F2` (Soft Background Fill)
  * **Muted Neutral Gray:** `#94A3B8` (In-active / Planned / Baseline)

---

## 3. Visual Hierarchy: The 3-30-300 Rule

Structure every Power BI dashboard canvas (16:9 ratio) into three distinct visual layers based on reader attention span:

```
+---------------------------------------------------------------------------------------------------+
| HEADER & MINIMAL SLICERS: [ Year ] [ Period / Cutoff ] [ Organizational Unit ]                    |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  3 SECONDS — TOP SECTION (Y: 20px, Height: 120px)                                                 |
|  [ Card 1: Revenue ]   [ Card 2: Net Result ]   [ Card 3: FTEs/Labor ]   [ Card 4: EVM CPI/SPI ]    |
|  🟢 1 433,0 MNOK       🔴 -11,0 MNOK            🟡 1 240 ÅV              🟡 0.95 CPI (Amber)       |
|  (Budsj: 0.0%|YoY +3.2%)(Deficit | MoM -1.5M)    (65.4% L | YoY +12 ÅV)   (SPI 0.92 | 5% over)       |
|                                                                                                   |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  30 SECONDS — MIDDLE SECTION (Y: 160px, Height: 440px)                                            |
|  MIDDLE LEFT (60% Width)                          | MIDDLE RIGHT (40% Width)                       |
|  Clustered Column + Line Chart                    | Diverging Horizontal Bar Chart                 |
|  Monthly Actuals vs Forecast vs Budget Line       | Net Variance / Sluttavvik (VAC) by Unit        |
|  Includes YoY Prior Year Reference Overlay        | RAG Color-Coded Bars (Green/Red)               |
|                                                   |                                               |
+---------------------------------------------------------------------------------------------------+
|                                                                                                   |
|  300 SECONDS — BOTTOM SECTION (Y: 620px, Height: 400px)                                           |
|  Minimalist Matrix / Deep Dive Table with RAG Formatting                                          |
|  Hierarchical Drill-down (Faculty -> Department -> Account / Project)                             |
|  Metrics: Revenue | Labor | Opex | Capex | Net Result | YoY % | MoM % | FTEs | RAG Status Badge   |
|                                                                                                   |
+---------------------------------------------------------------------------------------------------+
```

### Layer Breakdown
* **3 Seconds (Top Row):** KPI Cards delivering an immediate health check combining Target (Budget), YoY Growth, MoM Direction, and RAG Status Badges.
* **30 Seconds (Middle Band):** Analytical charts showing trends, seasonality, YoY comparison lines, and RAG color-coded unit performance.
* **300 Seconds (Bottom Grid):** Dense, structured matrix for granular inspection with RAG background fills and YoY/MoM deltas.

---

## 4. Comprehensive DAX Patterns for RAG Formatting

### Pattern A: Budget Variance RAG Status Text with Unicode Icons

```dax
Budget Variance RAG Status = 
VAR Budget = [Årsbudsjett (BAC)]
VAR Forecast = [Forecast LE (EAC)]
VAR Vac = Forecast - Budget
VAR VacPct = DIVIDE(Vac, Budget, 0)

RETURN
SWITCH(
    TRUE(),
    Vac >= 0, "🟢 Under/I budsjett",
    VacPct >= -0.05, "🟡 Moderat overskridelse (2-5%)",
    "🔴 Kritisk overskridelse (>5%)"
)
```

### Pattern B: YoY Growth RAG Status Text

```dax
YoY Growth RAG Status = 
VAR YoYPct = [Actual YoY %]

RETURN
SWITCH(
    TRUE(),
    YoYPct >= 0.03, "🟢 Sterk vekst (>= +3%)",
    YoYPct >= -0.02, "🟡 Stabil / Flat (-2% til +3%)",
    "🔴 Svekket inntekt (< -2%)"
)
```

### Pattern C: Primary RAG Hex Color (For Bars, Icons & Text)
Pass into Power BI **Conditional Formatting > Field Value**.

```dax
RAG Hex Color = 
VAR Vac = [Sluttavvik (VAC)]
VAR VacPct = [VAC %]
RETURN
IF(
    Vac >= 0, 
    "#10b981", // Emerald Green
    IF(
        VacPct >= -0.05, 
        "#f59e0b", // Amber Yellow
        "#ef4444"  // Crimson Red
    )
)
```

### Pattern D: Soft RAG Background Fill Hex (Tufte-Compliant 85% Opacity Tint)
Pass into Power BI **Matrix Cell Conditional Formatting > Background Color > Field Value**.

```dax
RAG Soft Background Hex = 
VAR Vac = [Sluttavvik (VAC)]
VAR VacPct = [VAC %]
RETURN
IF(
    Vac >= 0, 
    "#ecfdf5", // Soft Mint Green
    IF(
        VacPct >= -0.05, 
        "#fffbeb", // Soft Warm Amber
        "#fef2f2"  // Soft Crimson Red
    )
)
```

### Pattern E: EVM CPI/SPI RAG Status & Hex Color

```dax
EVM RAG Status = 
VAR CPIVal = [CPI]
RETURN
SWITCH(
    TRUE(),
    CPIVal >= 1.00, "🟢 God effektivitet (CPI >= 1.0)",
    CPIVal >= 0.90, "🟡 Moderat avvik (CPI 0.90-0.99)",
    "🔴 Kritisk overskridelse (CPI < 0.90)"
)

EVM CPI RAG Hex = 
VAR CPIVal = [CPI]
RETURN
IF(CPIVal >= 1.00, "#10b981", IF(CPIVal >= 0.90, "#f59e0b", "#ef4444"))
```

### Pattern F: Multi-Context Subtitle with RAG Icons (New Card Visual)

```dax
Multi-Context Revenue Subtitle = 
VAR Budget = [Årsbudsjett (BAC)]
VAR Forecast = [Forecast LE (EAC)]
VAR PlanDiffPct = DIVIDE(Forecast - Budget, Budget, 0)
VAR YoYPct = [Actual YoY %]
VAR MoMPct = [Actual MoM %]

VAR PlanIcon = IF(PlanDiffPct >= 0, "🟢", IF(PlanDiffPct >= -0.05, "🟡", "🔴"))
VAR YoYIcon = IF(YoYPct >= 0, "🟢", "🔴")

VAR PlanText = PlanIcon & " Budsj: " & IF(PlanDiffPct >= 0, "▲ +", "▼ ") & FORMAT(PlanDiffPct, "0.0%")
VAR YoYText = YoYIcon & " YoY: " & IF(YoYPct >= 0, "▲ +", "▼ ") & FORMAT(YoYPct, "0.0%")
VAR MoMText = "MoM: " & IF(MoMPct >= 0, "▲ +", "▼ ") & FORMAT(MoMPct, "0.0%")

RETURN
PlanText & " | " & YoYText & " | " & MoMText
```

---

## 5. Temporal DAX Baseline Measures (YoY & MoM)

### Year-over-Year (YoY)
```dax
// Prior Year Actuals
Actual PY = CALCULATE([Actual YTD], SAMEPERIODLASTYEAR('DimDate'[Dato]))

// Absolute YoY Difference
Actual YoY = [Actual YTD] - [Actual PY]

// Percentage YoY Growth
Actual YoY % = DIVIDE([Actual YoY], [Actual PY], 0)
```

### Month-over-Month (MoM)
```dax
// Prior Month Actuals
Actual PM = CALCULATE(SUM('FactGL'[Belop_signert]), PREVIOUSMONTH('DimDate'[Dato]), 'FactGL'[Bokforingstype] = "Actual")

// Current Month Actuals
Actual CM = CALCULATE(SUM('FactGL'[Belop_signert]), 'DimDate'[DatoNokkel] = MAX('FactGL'[DatoNokkel]), 'FactGL'[Bokforingstype] = "Actual")

// MoM Difference & Growth
Actual MoM = [Actual CM] - [Actual PM]
Actual MoM % = DIVIDE([Actual MoM], [Actual PM], 0)
```

---

## 6. Power BI Implementation Guide for RAG Formatting

### Setting up RAG on KPI Cards (New Card Visual)
1. Add the main metric (`[Forecast LE (EAC)]`) to the Card Visual data field.
2. In **Visual Formatting > Callout Value**, set font color to Primary Navy (`#1E293B`).
3. Enable **Subtitle**, and pass the DAX measure `[Multi-Context Revenue Subtitle]`.
4. Enable **Accent Bar** (Left border on Card): Select **Color > Conditional Formatting (fx)**, set Format Style to **Field Value**, and pick `[RAG Hex Color]`.

### Setting up RAG on Diverging Bar Charts
1. Select the Clustered Bar Chart (X-Axis: `[Sluttavvik (VAC)]`, Y-Axis: `DimOrganization[Fakultetsnavn]`).
2. Go to **Format Visual > Bars > Color**.
3. Click **fx (Conditional Formatting)** $ightarrow$ **Format Style: Field Value**.
4. Select measure: `[RAG Hex Color]`. Units with positive outcomes automatically turn Green (`#10B981`) and deficits turn Red (`#EF4444`).

### Setting up RAG on Matrix Tables
1. Select Matrix Visual.
2. Go to **Format Visual > Cell Elements**.
3. Select the `[Net Result]` or `[RAG Status]` column.
4. Turn on **Background color (fx)** $ightarrow$ **Format Style: Field Value** $ightarrow$ Pick `[RAG Soft Background Hex]`.
5. Turn on **Font color (fx)** $ightarrow$ **Format Style: Field Value** $ightarrow$ Pick `[RAG Hex Color]`.

---

## 7. Pre-Flight Storytelling & RAG Compliance Checklist

Before publishing any dashboard to Power BI Service, verify against this checklist:

- [ ] **3-30-300 Visual Structure:** Top row has 4–5 core KPI cards, middle section has trend/bar charts, bottom section has detailed matrix.
- [ ] **Multi-Context KPIs:** Each primary KPI card includes Budget, YoY (Year-over-Year), and MoM (Month-over-Month) context indicators.
- [ ] **RAG Formatting Compliance:** RAG rules applied using Tufte standards (soft fills `#FEF2F2`/`#ECFDF5`, accent borders, or Unicode icons `🟢`/`🟡`/`🔴`).
- [ ] **No Neon Glare:** Table background fills use 85%+ transparency tints rather than saturated solid fills.
- [ ] **DAX Formatting:** Every numeric measure uses explicit formatting (`#,##0.0 MNOK`, `0.0%`, `0.00`).
- [ ] **Accessibility:** High-contrast text colors on light backgrounds; font sizes legible on standard 1080p executive displays.
- [ ] **Performance & RLS:** Star schema verified (1:* single-direction relationships); Row-Level Security (RLS) configured for unit heads.
