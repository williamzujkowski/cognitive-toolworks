# Changelog - slo-validator

All notable changes to the Service Level Objective Validator skill.

## [1.0.0] - 2025-10-26

### Added
- Initial release of SLO Validator skill
- T1: Basic SLO validation against metrics with simple alerting
- T2: Multi-window validation with burn rate alerts and dashboard generation
- T3: Trend analysis, remediation recommendations, and advanced reporting
- Support for Prometheus, CloudWatch, Datadog, and New Relic metrics sources
- Multi-window burn rate alerting (1h, 6h, 3d windows)
- Error budget policy enforcement (strict, moderate, flexible)
- Dashboard configuration generation for Grafana and CloudWatch
- Compliance audit reporting with breach timeline
- Example: API service SLO validation with Prometheus
- Evaluation scenarios: 5 test cases covering availability, latency, burn rates

### Sources
- Google SRE Workbook - Implementing SLOs (accessed 2025-10-26T03:51:54-04:00)
- Google SRE Workbook - Alerting on SLOs (accessed 2025-10-26T03:51:54-04:00)
- Prometheus Alerting Rules documentation (accessed 2025-10-26T03:51:54-04:00)
- Sloth SLO Generator (accessed 2025-10-26T03:51:54-04:00)
