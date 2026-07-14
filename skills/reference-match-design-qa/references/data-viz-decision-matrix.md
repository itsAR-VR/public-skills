# Data Visualization Decision Matrix

Research date: 2026-05-18

Purpose: make charts, dashboards, reports, and maps answer a real decision
question instead of decorating the screen.

Primary sources:

- Carbon chart types: https://carbondesignsystem.com/data-visualization/chart-types/
- Carbon legends: https://carbondesignsystem.com/data-visualization/legends/
- Carbon dashboards: https://carbondesignsystem.com/data-visualization/dashboards/
- Observable Plot: https://observablehq.com/plot/
- Apache ECharts: https://echarts.apache.org/
- deck.gl: https://deck.gl/
- kepler.gl: https://kepler.gl/

## Choose Chart By Task

| User task | Prefer | Avoid |
| --- | --- | --- |
| Compare categories | bar, dot plot, table | pie with many slices |
| Show trend over time | line, area, small multiples | isolated KPI without context |
| Show part-to-whole | stacked bar, 100% bar, treemap when many parts | donut/pie for precise comparison |
| Show distribution | histogram, box plot, violin where appropriate | averages alone |
| Show correlation | scatter, bubble with caution | dual axes without explanation |
| Show ranking | sorted bar/table | unsorted category chart |
| Show geography/spatial | map/table split, choropleth, route/layer map | map-only UI with no list fallback |
| Show operational status | status table, timeline, exception queue | decorative dashboard cards |

## Rules

- Name the decision question before choosing the chart.
- Prefer direct labels when legends create extra work.
- Keep color meanings consistent across the dashboard.
- Do not use fake metrics or unsupported precision.
- Include empty, loading, error, filtered-empty, no-data-yet, and huge-data
  states where relevant.
- Provide table/list fallback for dense charts, maps, and spatial dashboards.
- Annotate thresholds, targets, anomalies, or risk bands when they drive action.
- Check chart contrast, keyboard access where interactive, and text alternatives
  for key insights.

## Packet Fields

- decision_question:
- chart_task:
- selected_chart_type:
- comparison_baseline:
- color_mapping:
- legend_strategy:
- annotation_strategy:
- table_or_text_fallback:
- accessibility_summary:
- data_truth_risk:
- map_or_chart_state_proof:
