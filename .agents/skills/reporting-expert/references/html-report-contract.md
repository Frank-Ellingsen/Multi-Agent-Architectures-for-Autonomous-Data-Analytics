# HTML Reporting Contract

## Required semantic structure

```html
<header>Report identity, period, generated time, audience</header>
<nav>Keyboard-accessible section navigation</nav>
<main>
  <section id="executive-summary"></section>
  <section id="status"></section>
  <section id="descriptive-diagnostic"></section>
  <section id="predictive"></section>
  <section id="prescriptive"></section>
  <section id="actions"></section>
  <section id="assumptions-limitations"></section>
  <section id="data-quality-validation"></section>
  <section id="evidence"></section>
</main>
<footer>Report identifier and lineage</footer>
```

## Layout

- Responsive max-width content container.
- Executive message and required decision at the top.
- KPI/RAG cards directly below the executive message.
- One dominant analytical question per section.
- Use a clear grid with consistent alignment and spacing.
- Collapse gracefully to one column on narrow screens.
- Include print CSS that removes decorative controls and preserves tables and charts.

## RAG cards

Each card should expose:

```yaml
name: string
status: RED | AMBER | GREEN
actual: number|string
target: number|string
variance: number|string
trend: up|down|flat|unknown
forecast: number|string|null
rule_id: string
```

Color must be accompanied by status text and an icon or shape.

## Accessibility

- Use semantic headings in order.
- Ensure keyboard access for navigation, filters, disclosures, and tooltips.
- Add `aria-label` or visible labels to controls.
- Add concise chart alt text or an accessible textual summary.
- Do not rely on hover as the only method of showing values.
- Do not rely on color alone.
- Use sufficient text and object contrast.
- Respect reduced-motion preferences.
- Keep animation optional and nonessential.

## Interactivity

Include a filter or drill-down only when it supports the report's decision. Every filter must visibly display its current state and apply consistently across relevant content.

## Provenance

Each analytical section should retain references to:

- dataset/version;
- reporting period and filters;
- query or calculation identifier;
- model/scenario identifier where applicable;
- source/evidence reference;
- generated timestamp.
