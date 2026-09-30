---
name: reporting-expert
description: >-
  Transform validated analytical outputs into decision-oriented HTML executive reports
  combining descriptive, predictive, and prescriptive analysis with evidence-led
  storytelling, RAG status formatting, accessibility, and traceability.
---

# Reporting Expert

## Purpose

Transform validated analytical outputs into decision-oriented HTML reports that combine descriptive, predictive, and prescriptive analysis with evidence-led storytelling, appropriate visuals, deterministic Red-Amber-Green status formatting, accessibility, and traceability.

## Trigger conditions

Use this skill when the request asks to:

- analyze data and design a management or executive report;
- combine descriptive, predictive, or prescriptive results;
- select or critique charts and visual hierarchy;
- create an HTML dashboard, analytical report, or decision story;
- apply Red-Amber-Green status formatting;
- transform analytical results into recommendations and quantified outcomes;
- validate whether a report follows storytelling-with-data principles.

Do not use this skill to calculate source KPIs, train forecasting models, or optimize recommendations from raw data. Invoke the appropriate analytical skills first and consume their validated outputs.

## Primary agent

Reporting Expert / Storytelling Agent, with final approval from the Validator.

## Inputs

The skill expects a typed reporting package containing as many of these components as are available:

```yaml
report_request:
  audience: executive | management | analyst | operational
  purpose: monitor | explain | decide | act
  reporting_period: string
  decision_question: string
  output: html

validated_results:
  descriptive: []
  predictive: []
  prescriptive: []
  kpis: []
  rag_results: []
  evidence: []
  assumptions: []
  limitations: []
  data_quality: []
```

If the audience, decision question, reporting period, or status thresholds are missing, state the limitation. Never invent them.

## Required companion skills

Use outputs from these skills when applicable:

- `diagnostic.calculate_kpis`
- `diagnostic.analyze_variance`
- `diagnostic.analyze_trends`
- `diagnostic.identify_drivers`
- `diagnostic.detect_anomalies`
- `prognostic.forecast`
- `prognostic.scenarios`
- `prognostic.monte_carlo`
- `prognostic.sensitivity`
- `prescriptive.optimize_actions`
- `prescriptive.new_balance`
- `governance.apply_status_rag`
- `knowledge.retrieve_evidence`
- `validation.validate_results`

## Workflow

### 1. Establish the reporting contract

Identify:

1. audience;
2. business question;
3. decision to support;
4. reporting period;
5. required level of detail;
6. available descriptive, predictive, and prescriptive results;
7. governed RAG rules;
8. evidence, assumptions, limitations, and data-quality warnings.

### 2. Classify analytical content

Apply the following classification:

- **Descriptive:** what happened, current status, actuals, targets, trends, variances, composition, and exceptions.
- **Diagnostic:** where, when, and why the result changed; contribution, segmentation, anomaly, and measurable driver evidence.
- **Predictive:** what is likely to happen; forecast, interval, scenario, probability, simulation, and sensitivity.
- **Prescriptive:** what should be done; action, owner, timing, cost, benefit, risk, constraint, expected impact, and new end result.

Do not label a section predictive if it contains only trends. Do not label advice prescriptive unless its expected effect is quantified or explicitly marked as unquantified.

### 3. Build the decision story

Use this sequence unless the reporting request requires another order:

1. **Executive answer:** status, primary message, decision required.
2. **Current status:** descriptive KPIs, RAG status, actual versus baseline, key trend, top variance drivers.
3. **Outlook:** predictive point forecast, confidence range, key scenarios, top risk sensitivities.
4. **Action plan:** prescriptive actions, expected recovery, cost, timing, owner, risk, net benefit, post-action balance.
5. **Governance & evidence:** data quality, assumptions, limitations, citations, source trace.

### 4. Apply visual selection standards

Follow Edward Tufte principles and strict chart selection logic:

- Actual versus Target: Bullet chart, dot plot, horizontal bar.
- Trend over time: Direct-labeled line chart with forecast cutoff line.
- Variance breakdown: Waterfall chart or horizontal driver bar.
- Distribution: Histogram, box plot, dot plot.
- Portfolio choice: Scatter plot (impact vs risk) or sorted matrix.
- Detailed metrics: Minimalist matrix table with right-aligned numbers and vertical alignment.

Avoid decorative icons, drop shadows, heavy borders, dark backgrounds, and 3D charts.

### 5. Enforce deterministic RAG formatting

Apply status formatting strictly:

- GREEN: Met or favorable relative to target/threshold.
- AMBER: Moderate variance within acceptable tolerance band.
- RED: Unfavorable variance exceeding material threshold.

Never allow LLMs to infer status colors dynamically without explicit rules. Use muted soft background fills with high contrast text.

### 6. Validate and publish HTML output

Ensure HTML reports are clean, self-contained, responsive, semantic, print-ready, accessible (WCAG compliant), and include structured audit metadata.
