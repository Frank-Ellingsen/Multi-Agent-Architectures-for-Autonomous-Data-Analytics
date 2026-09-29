Dashboard Canvas & Styling SetupCanvas Ratio: 16:9 (1920 × 1080 px or 1280 × 720 px)Background: Light Muted Gray (#F8FAFC)Card Containers: White (#FFFFFF) with 8px border radius, 1px subtle gray border (#E2E8F0), and light drop shadow (Blur: 8, Distance: 2, Transparency: 92%).Color Palette:Primary Navy: #1E293B (Titles, Headers, Primary Bars)Secondary Slate: #64748B (Subtitles, Axis Labels, Secondary Series)Success Green: #10B981 (Favorable variances / Under budget / Target met)Warning Amber: #F59E0B (Moderate variance 2–5%)Alert Crimson: #EF4444 (Unfavorable variances > 5% / Net Deficit)Slicers (Top Right Header): Minimal slicer bar containing:Regnskapsår (Single Select: 2026)Rapporteringsperiode (Dropdown: M09 / September YTD)Enhet / Fakultet (Dropdown: Alle Fakulteter with Multi-select enabled)Top Section: KPI Cards (3-Second Snapshot)Place 5 New Card Visuals (Power BI Core Card Visual) across the top row ($Y = 20\,\text{px}$, Height $= 120\,\text{px}$).Card 1: Total Revenue (Samlet Inntekt)Data Field: [Forecast LE (EAC)] (Filtered to Income Class 3) $\rightarrow$ 1 433,0 MNOKReference Metric / Subtitle: [Revenue Variance Indicator]DAX Indicator Measure:Revenue Variance Indicator =
VAR Budget = [Årsbudsjett (BAC)]
VAR Forecast = [Forecast LE (EAC)]
VAR Diff = Forecast - Budget
VAR Pct = DIVIDE(Diff, Budget, 0)
RETURN
"Budsjett: " & FORMAT(Budget, "#,##0.0") & " MNOK | " &
IF(Diff >= 0, "▲ +" & FORMAT(Pct, "0.0%"), "▼ " & FORMAT(Pct, "0.0%"))
Conditional Accent Color: #10B981 (Green) if $\ge 0$, #EF4444 if $< 0$.Card 2: Net Operating Result (Helårsavvik / VAC)Data Field: [Sluttavvik (VAC)] $\rightarrow$ -11,0 MNOKSubtitle: "Dekkes av formålskapital (F-05-20)"Card Accent / Value Color: #EF4444 (Crimson Red)DAX Subtitle Indicator:Net Result Status Text =
VAR YTDResult = [Actual YTD] // Net YTD
RETURN
"YTD per Sept: " & FORMAT(YTDResult, "#,##0.0") & " MNOK (Budsjettavvik)"
Card 3: Work Years & Staffing (Årsverk & Lønnsandel)Data Field: [Totale Årsverk] $\rightarrow$ 1 240 ÅVSubtitle Field: [Staffing Card Subtitle]DAX Measure:Staffing Card Subtitle =
VAR UF = [Faglige Årsverk (UF)]
VAR TA = [Teknisk-Admin Årsverk (TA)]
VAR LonnPct = [Lønnsandel %]
RETURN
FORMAT(UF, "#0") & " UF / " & FORMAT(TA, "#0") & " TA | Lønnsandel: " & FORMAT(LonnPct, "0.0%")
Card 4: EVM Efficiency (CPI & SPI)Data Field: [CPI] $\rightarrow$ 0,95Subtitle Field: [EVM Status Subtitle]DAX Measure:EVM Status Subtitle =
VAR SPIVal = [SPI]
RETURN
"SPI (Tidsfremdrift): " & FORMAT(SPIVal, "0.00") & " | 5% Kostnadsoverskridelse"
Conditional Formatting: Amber (#F59E0B) for $0.90 \le \text{CPI} < 1.00$.Card 5: Student Density & Production (Studenter & SPE60)Data Field: [Registrerte Studenter] $\rightarrow$ 14 000Subtitle Field: [Student KPI Subtitle]DAX Measure:Student KPI Subtitle =
VAR SPE = [Avlagte SPE60]
VAR Ratio = [Studenter pr UF-Årsverk]
RETURN
FORMAT(SPE, "#,##0") & " SPE60 | " & FORMAT(Ratio, "0.0") & " Studenter/UF-ÅV"
Middle Section: Core Trends & Segmental Analysis (30-Second Insight)Visual 1 (Middle Left - Width: 60%): Monthly Revenue & Cost Performance vs. BudgetVisual Type: Clustered Column + Line Chart (Line and Clustered Column Chart).X-Axis: DimDate[MånedNavnKort] (Jan, Feb, ..., Des).Column Series:[Faktiske & Prognostiserte Driftskostnader] (Bar Color: Primary Navy #1E293B for Actuals M01–M09, Muted Blue #64748B for Q4 Forecast M10–M12).Line Series:[Månedlig Budsjett] (Line Style: Dashed #94A3B8, Stroke Width: 2px).Reference Line: Add a vertical dotted line between Sep (M09) and Okt (M10) labeled "T3 Cutoff / Actuals vs Forecast".Visual 2 (Middle Right - Width: 40%): Faculty Net Result & Budget VarianceVisual Type: Diverging Horizontal Bar Chart (Clustered Bar Chart).Y-Axis: DimOrganization[Fakultetsnavn].X-Axis: [Sluttavvik (VAC)] (MNOK).Conditional Data Colors:Positive Net Result (HHU +2,2M, SAM +3,0M) $\rightarrow$ Emerald Green (#10B981)Negative Net Result (TEK -1,9M, HEL -5,3M, ADM -8,7M) $\rightarrow$ Soft Crimson (#EF4444)// DAX Measure for Bar Color Conditional Formatting
Faculty Bar Color =
IF([Sluttavvik (VAC)] >= 0, "#10b981", "#ef4444")
Bottom Section: Detailed Summary & Risk Table (300-Second Deep Dive)Place a clean, highly structured Matrix Visual spanning the bottom panel ($Y = 620\,\text{px}$, Height $= 400\,\text{px}$).Layout & Hierarchy:Rows: DimOrganization[Fakultetsnavn] $\rightarrow$ DimOrganization[Instituttnavn].Columns (Measures):Total Inntekt (MNOK): [Forecast LE (EAC)] (Income)Lønnskostnad (MNOK): [Actual/FC Lønn]Driftskostnad (MNOK): [Actual/FC Drift]Investeringer (Capex): [Actual/FC Capex]Netto Resultat (MNOK): [Sluttavvik (VAC)]UF-Årsverk: [Faglige Årsverk (UF)]Studenter / UF-ÅV: [Studenter pr UF-Årsverk]RAG Status: [Forecast RAG Status]Matrix Styling Rules:Style Preset: None (Minimalist).Row Headers: Font: Segoe UI Semi-bold, Size: 10 pt, Background: #F1F5F9.Gridlines: Horizontal Gridlines only (Color: #E2E8F0, Width: 1px). Vertical Gridlines off.Values Formatting: Right-aligned numbers, 1 decimal place.Conditional Background on Net Result Column: Subtle background fill based on [RAG Hex Color] with 85% transparency so text remains dark and legible.Key DAX Measures for Chart & Table Formatting// Cumulative Actuals + Q4 Forecast Line for M01-M12
Cumulative Actual & Forecast =
VAR MaxDate = MAX('DimDate'[Dato])
RETURN
CALCULATE(
[Forecast LE (EAC)],
'DimDate'[Dato] <= MaxDate,
ALLSELECTED('DimDate')
)

// Cumulative Budget Line
Cumulative Budget =
VAR MaxDate = MAX('DimDate'[Dato])
RETURN
CALCULATE(
[Årsbudsjett (BAC)],
'DimDate'[Dato] <= MaxDate,
ALLSELECTED('DimDate')
)

// Dynamic Card Border Color for Executive Highlighting
KPI Card Border Color =
SWITCH(
TRUE(),
[VAC %] < -0.05, "#EF4444", // Red highlight
[VAC %] < 0.00, "#F59E0B", // Yellow highlight
"#10B981" // Green
)
Summary Layout Grid Mapping+---------------------------------------------------------------------------------------------------+
| University Board Executive Dashboard 2026 | Cutoff: 30. Sept 2026 | Slicers: [Year: 2026] [Faculty: All] |
+---------------------------------------------------------------------------------------------------+
| [ CARD 1 ] | [ CARD 2 ] | [ CARD 3 ] | [ CARD 4 ] | [ CARD 5 ] |
| Total Revenue | Net Result (VAC) | Total FTEs / Staff | CPI / SPI | Students |
| 1 433,0 MNOK | -11,0 MNOK | 1 240 ÅV (65.4% L) | 0.95 CPI / 0.92 | 14 000 |
+---------------------------------------------------------------------------------------------------+
| | |
| MIDDLE LEFT (60%): | MIDDLE RIGHT (40%): |
| Monthly Revenue & Cost Performance vs. Budget | Faculty Net Result & Variance Breakdown |
| (Clustered Column + Line Chart, M01-M12) | (Diverging Horizontal Bar Chart) |
| | |
+---------------------------------------------------------------------------------------------------+
| |
| BOTTOM SECTION (100%): |
| Detailed Faculty & Department Summary Matrix |
| (Inntekt | Lønn | Drift | Capex | Netto Resultat | UF-ÅV | Studenter/UF | RAG Status) |
| |
+---------------------------------------------------------------------------------------------------+
This layout enforces the 3-30-300 rule: board members get an instant status check in 3 seconds, spot key trends and faculty drivers in 30 seconds, and can drill down into granular faculty matrix data for up to 300 seconds during meetings.
