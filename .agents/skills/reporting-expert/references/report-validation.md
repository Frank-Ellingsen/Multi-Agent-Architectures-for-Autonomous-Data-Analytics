# Reporting Validation Checklist

## Analytical integrity

- [ ] Narrative values reconcile with validated result objects.
- [ ] Chart values reconcile with tables and narrative.
- [ ] Units, currencies, dates, filters, and dimensional grain are consistent.
- [ ] Actual, target, budget, forecast, and scenario values are not conflated.
- [ ] Causal wording is not used for unsupported associations.

## Descriptive and diagnostic reporting

- [ ] Current status and comparison basis are explicit.
- [ ] Largest contributors and exceptions are prioritized.
- [ ] Variance percentages have valid denominators.
- [ ] Trend comparisons use compatible periods.

## Predictive reporting

- [ ] Forecast horizon and cutoff are shown.
- [ ] Model or method reference is retained.
- [ ] Uncertainty interval or limitation is visible.
- [ ] Scenario assumptions are explicit.
- [ ] Simulations retain random seed and iteration metadata where applicable.

## Prescriptive reporting

- [ ] Recommended actions are feasible under recorded constraints.
- [ ] Expected benefit, cost, risk, and timing are shown when available.
- [ ] Unquantified actions are clearly marked.
- [ ] Before/after results reconcile.
- [ ] Residual gap and residual risk remain visible.

## RAG governance

- [ ] Every status comes from a governed rule result.
- [ ] Actual, target, variance, and rule/threshold are accessible.
- [ ] Color is not the only status indicator.
- [ ] Status colors are used consistently.

## Storytelling

- [ ] Audience, purpose, and decision question are explicit.
- [ ] Executive answer appears first.
- [ ] Every section answers a question.
- [ ] Every visual supports a decision-relevant statement.
- [ ] The recommendation follows from the analysis.
- [ ] Assumptions and limitations are not hidden.

## HTML and accessibility

- [ ] Semantic heading structure is valid.
- [ ] Navigation and controls work by keyboard.
- [ ] Charts include alt text or accessible summaries.
- [ ] Labels and contrast are sufficient.
- [ ] Interactive values do not depend only on hover.
- [ ] Layout is responsive and print friendly.

## Publication decision

Return `fail` with blocking issues if any analytical reconciliation, RAG governance, unsupported-claim, or accessibility-critical check fails. Return `pass` only when all blocking checks are resolved.
