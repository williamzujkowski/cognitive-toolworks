# Analytics Dashboard Wireframe

**User Story**: Business analyst wants to view key metrics and charts to monitor performance at a glance.

## Desktop Layout (1280px+)
```
+------------------------------------------------------------------+
| [Logo] Analytics Dashboard              [Profile ▼] [Settings]  |
+------------------------------------------------------------------+
| Sidebar (240px)      | Main Content Area (1040px)                |
| • Overview           | +-------+ +-------+ +-------+ +-------+  |
| • Reports            | | Users | | Sales | |Growth | |Churn  |  |
| • Analytics          | | 1,234 | |$52K   | | +12% | | -2%   |  |
| • Settings           | +-------+ +-------+ +-------+ +-------+  |
| [+ New Report]       | Revenue Trend (Last 30 Days)             |
|                      | +-----------------------------------+    |
|                      | |  [Line Chart: Revenue over time] |    |
|                      | +-----------------------------------+    |
|                      | Recent Activity                          |
|                      | • User signup: john@example.com          |
|                      | • Payment received: $299                 |
|                      | • Report generated: Q4 Summary           |
+------------------------------------------------------------------+
```

## Mobile Layout (375px)
```
+---------------------+
| ☰  Dashboard   [👤] |
+---------------------+
| +-------+ +-------+ |
| | Users | | Sales | |
| | 1,234 | |$52K   | |
| +-------+ +-------+ |
| Revenue (30d) 📈    |
| +-----------------+ |
| |  [Line Chart]  | |
| +-----------------+ |
| Recent Activity     |
| • User signup       |
+---------------------+
```

## Component Specs

**Metric Cards**: States (default, loading, error), click to drill down, aria-label with values
**Sidebar**: Collapsed (mobile), expanded (desktop), keyboard navigation (arrows + Enter)
**Chart Widget**: Skeleton loading, error retry button, hover tooltips with data points

## Accessibility
- Color contrast: 4.7:1 (text), 3.2:1 (UI)
- Keyboard: Tab order follows layout, 2px blue focus outline
- Screen reader: Charts have data table alternative
