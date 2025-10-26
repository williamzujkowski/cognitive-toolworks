# Analytics Dashboard Wireframe (T2 Example)

## User Story
As a business analyst, I want to view key metrics and charts on a dashboard so that I can monitor business performance at a glance.

## Screen: Main Dashboard

### Desktop Layout (1280px+)
```
+------------------------------------------------------------------+
| [Logo] Analytics Dashboard              [Profile ▼] [Settings]  |
+------------------------------------------------------------------+
| Sidebar (240px)      | Main Content Area (1040px)                |
|                      |                                           |
| • Overview           | +-------+ +-------+ +-------+ +-------+  |
| • Reports            | | Users | | Sales | |Growth | |Churn  |  |
| • Analytics          | | 1,234 | |$52K   | | +12% | | -2%   |  |
| • Settings           | +-------+ +-------+ +-------+ +-------+  |
|                      |                                           |
| [+ New Report]       | Revenue Trend (Last 30 Days)             |
|                      | +-----------------------------------+    |
|                      | |                              📈  |    |
|                      | |  [Line Chart Placeholder]        |    |
|                      | +-----------------------------------+    |
|                      |                                           |
|                      | Recent Activity                          |
|                      | +-----------------------------------+    |
|                      | | • User signup: john@example.com   |    |
|                      | | • Payment received: $299          |    |
|                      | | • Report generated: Q4 Summary    |    |
|                      | +-----------------------------------+    |
+------------------------------------------------------------------+
```

### Mobile Layout (375px)
```
+---------------------+
| ☰  Dashboard   [👤] |
+---------------------+
| +-------+ +-------+ |
| | Users | | Sales | |
| | 1,234 | |$52K   | |
| +-------+ +-------+ |
| +-------+ +-------+ |
| |Growth | |Churn  | |
| | +12% | | -2%   | |
| +-------+ +-------+ |
|                     |
| Revenue (30d)       |
| +-----------------+ |
| |   [Chart]      | |
| +-----------------+ |
|                     |
| Recent Activity     |
| • User signup       |
| • Payment $299      |
+---------------------+
```

## Component Specifications

### Metric Card
- **States**: default, loading (skeleton), error
- **Interaction**: Click to drill down to detailed view
- **Accessibility**: aria-label="Total users: 1234"

### Sidebar Navigation
- **States**: collapsed (mobile), expanded (desktop)
- **Keyboard**: Arrow keys navigate, Enter selects
- **Responsive**: Hamburger menu on mobile (<768px)

### Chart Widget
- **Loading**: Show skeleton placeholder (200ms delay before showing)
- **Error**: Display "Unable to load data" with retry button
- **Interaction**: Hover shows data point tooltip

## Accessibility Notes
- ✅ Color contrast: 4.7:1 (text), 3.2:1 (UI elements)
- ✅ Keyboard navigation: Tab order follows visual layout
- ✅ Screen reader: All charts have data table alternative
- ✅ Focus indicators: 2px blue outline on all interactive elements
