---
name: powerbi-dashboard-guide
description: >-
  Power BI canvas & styling setup (16:9 ratio, Segoe UI, light slate palette), top KPI card visual setup,
  DAX measures for VAC/CPI/SPI/FTEs, middle section trends, and bottom matrix visual layout.
---

# Power BI Dashboard Canvas & Styling Setup (powerbi-dashboard-guide)

## Overview
A comprehensive guide for building 16:9 executive Power BI dashboards with Segoe UI typography, curated color palettes, DAX metrics, and 3-30-300 layout mapping.

## Canvas Ratio & Palette
- **Canvas Ratio:** 16:9 (1920 × 1080 px or 1280 × 720 px)
- **Background:** Light Muted Gray (`#F8FAFC`)
- **Card Containers:** White (`#FFFFFF`) with 8px border radius, 1px subtle gray border (`#E2E8F0`), and light drop shadow (Blur: 8, Distance: 2, Transparency: 92%).
- **Color Palette:**
  - Primary Navy: `#1E293B` (Titles, Headers, Primary Bars)
  - Secondary Slate: `#64748B` (Subtitles, Axis Labels, Secondary Series)
  - Success Green: `#10B981` (Favorable variances / Under budget / Target met)
  - Warning Amber: `#F59E0B` (Moderate variance 2–5%)
  - Alert Crimson: `#EF4444` (Unfavorable variances > 5% / Net Deficit)

## Header & Slicers (Top Right Header)
Minimal slicer bar containing:
- `Regnskapsår` (Single Select: 2026)
- `Rapporteringsperiode` (Dropdown: M09 / September YTD)
- `Enhet / Fakultet` (Dropdown: Alle Fakulteter with Multi-select enabled)

## Top Section: KPI Cards (3-Second Snapshot)
Place 5 New Card Visuals across the top row ($Y = 20\,\text{px}$, Height $= 120\,\text{px}$).

### Card 1: Total Revenue (Samlet Inntekt)
- **Data Field:** `[Forecast LE (EAC)]` (Filtered to Income Class 3) -> 1 433,0 MNOK
- **Reference Metric / Subtitle:** `[Revenue Variance Indicator]`
- **DAX Indicator Measure:**
```dax
Revenue Variance Indicator =
VAR Budget = [Årsbudsjett (BAC)]
VAR Forecast = [Forecast LE (EAC)]
VAR Diff = Forecast - Budget
VAR Pct = DIVIDE(Diff, Budget, 0)
RETURN
"Budsjett: " & FORMAT(Budget, "#,##0.0") & " MNOK | " &
IF(Diff >= 0, "▲ +" & FORMAT(Pct, "0.0%"), "▼ " & FORMAT(Pct, "0.0%"))
```
- **Conditional Accent Color:** `#10B981` (Green) if $\ge 0$, `#EF4444` if $< 0$.

### Card 2: Net Operating Result (Helårsavvik / VAC)
- **Data Field:** `[Sluttavvik (VAC)]` -> -11,0 MNOK
- **Subtitle:** "Dekkes av formålskapital (F-05-20)"
- **Card Accent / Value Color:** `#EF4444` (Crimson Red)
- **DAX Subtitle Indicator:**
```dax
Net Result Status Text =
VAR YTDResult = [Actual YTD] // Net YTD
RETURN
"YTD per Sept: " & FORMAT(YTDResult, "#,##0.0") & " MNOK (Budsjettavvik)"
```

### Card 3: Work Years & Staffing (Årsverk & Lønnsandel)
- **Data Field:** `[Totale Årsverk]` -> 1 240 ÅV
- **Subtitle Field:** `[Staffing Card Subtitle]`
- **DAX Measure:**
```dax
Staffing Card Subtitle =
VAR UF = [Faglige Årsverk (UF)]
VAR TA = [Teknisk-Admin Årsverk (TA)]
VAR LonnPct = [Lønnsandel %]
RETURN
FORMAT(UF, "#0") & " UF / " & FORMAT(TA, "#0") & " TA | Lønnsandel: " & FORMAT(LonnPct, "0.0%")
```

### Card 4: EVM Efficiency (CPI & SPI)
- **Data Field:** `[CPI]` -> 0,95
- **Subtitle Field:** `[EVM Status Subtitle]`
- **DAX Measure:**
```dax
EVM Status Subtitle =
VAR SPIVal = [SPI]
RETURN
"SPI (Tidsfremdrift): " & FORMAT(SPIVal, "0.00") & " | 5% Kostnadsoverskridelse"
```
- **Conditional Formatting:** Amber (`#F59E0B`) for $0.90 \le \text{CPI} < 1.00$.

### Card 5: Student Density & Production (Studenter & SPE60)
- **Data Field:** `[Registrerte Studenter]` -> 14 000
- **Subtitle Field:** `[Student KPI Subtitle]`
- **DAX Measure:**
```dax
Student KPI Subtitle =
VAR SPE = [Avlagte SPE60]
VAR Ratio = [Studenter pr UF-Årsverk]
RETURN
FORMAT(SPE, "#,##0") & " SPE60 | " & FORMAT(Ratio, "0.0") & " Studenter/UF-ÅV"
```

## Middle Section: Core Trends & Segmental Analysis (30-Second Insight)
- **Visual 1 (Middle Left - Width: 60%):** Monthly Revenue & Cost Performance vs. Budget
  - Visual Type: Clustered Column + Line Chart (Line and Clustered Column Chart).
  - X-Axis: `DimDate[MånedNavnKort]` (Jan, Feb, ..., Des).
  - Column Series: `[Faktiske & Prognostiserte Driftskostnader]` (Bar Color: Primary Navy `#1E293B` for Actuals M01–M09, Muted Blue `#64748B` for Q4 Forecast M10–M12).
  - Line Series: `[Månedlig Budsjett]` (Line Style: Dashed `#94A3B8`, Stroke Width: 2px).
  - Reference Line: Add a vertical dotted line between Sep (M09) and Okt (M10) labeled "T3 Cutoff / Actuals vs Forecast".

- **Visual 2 (Middle Right - Width: 40%):** Faculty Net Result & Budget Variance
  - Visual Type: Diverging Horizontal Bar Chart (Clustered Bar Chart).
  - Y-Axis: `DimOrganization[Fakultetsnavn]`.
  - X-Axis: `[Sluttavvik (VAC)]` (MNOK).
  - Conditional Data Colors: Positive Net Result -> Emerald Green (`#10B981`), Negative Net Result -> Soft Crimson (`#EF4444`).

## Bottom Section: Detailed Summary & Risk Table (300-Second Deep Dive)
Place a clean, highly structured Matrix Visual spanning the bottom panel ($Y = 620\,\text{px}$, Height $= 400\,\text{px}$).
- **Rows:** `DimOrganization[Fakultetsnavn]` -> `DimOrganization[Instituttnavn]`.
- **Columns (Measures):** Total Inntekt, Lønnskostnad, Driftskostnad, Capex, Netto Resultat, UF-Årsverk, Studenter/UF-ÅV, RAG Status.
- **Matrix Styling:** Style Preset: None (Minimalist). Row Headers: Segoe UI Semi-bold, 10 pt. Horizontal Gridlines only (`#E2E8F0`). Right-aligned numbers.
