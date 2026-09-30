# Visual Selection Rules

## Principle

Choose the simplest visual that answers the decision question. Start with the message, not the available chart library.

## Selection matrix

| Analytical question | Preferred visual | Required explanation |
|---|---|---|
| How does actual compare with target? | bar, bullet chart, dot plot | actual, target, variance, unit, period |
| How has performance changed over time? | line chart | period, target/baseline, relevant annotation |
| What created the variance? | waterfall or sorted contribution bar | starting value, contributors, ending value |
| Which categories contribute most? | sorted horizontal bar or Pareto | contribution and cumulative context |
| Where are the exceptions? | highlight table, dot plot, small multiples | exception rule and affected entity |
| What is the distribution? | histogram, box plot, density | sample size, unit, notable tails/outliers |
| What is the relationship? | scatter plot | variables, scale, association caveat |
| What is the forecast? | line plus interval/fan | cutoff, horizon, forecast distinction, interval |
| What is the scenario range? | interval plot, clustered bar, scenario table | scenario assumptions and baseline |
| What drives uncertainty? | tornado/sensitivity chart | changed inputs, range, outcome effect |
| What is the risk probability? | percentile curve, probability bar, distribution | probability definition and threshold |
| Which action should be selected? | ranked table or impact-effort matrix | cost, benefit, risk, feasibility |
| How does the action change the result? | before/after bar or waterfall | baseline, action effect, residual gap |

## Formatting rules

- Write chart titles as conclusions when supported.
- Label important values directly.
- Use consistent units, scales, filters, and date ranges.
- Reserve strong color for emphasis and status.
- Keep contextual series neutral.
- Avoid legends when direct labels are practical.
- Avoid 3D and decorative chart effects.
- Do not truncate axes when doing so creates a misleading comparison.
- Distinguish actual, forecast, and scenario visually.
- Provide concise alt text containing chart type, data context, and takeaway.
- Provide an accessible table or data summary for complex interactive charts.
