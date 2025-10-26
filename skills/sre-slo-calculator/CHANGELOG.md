# Changelog

All notable changes to the sre-slo-calculator skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-25

### Added
- Initial implementation of SRE SLO/SLI Calculator skill
- T1 tier: Fast path SLI/SLO definition for standard services
- T2 tier: Extended SLO design with error budget policies and multi-window tracking
- SLI definition based on service golden signals (latency, error rate, throughput)
- Error budget calculation with burn rate thresholds (1h, 6h, 3d windows)
- Multi-platform monitoring query generation (Prometheus, Datadog, CloudWatch, New Relic)
- Alerting policy design with severity mapping
- SLA derivation from SLO targets
- Error budget policy framework (freeze conditions, escalation paths)
- Comprehensive examples and resource links
- Integration with Google SRE Book and SRE Workbook methodologies
- Support for availability, latency, freshness, correctness, and throughput SLIs
- Rolling and calendar window SLO tracking

### Sources
- Google SRE Book Chapter 4 (Service Level Objectives)
- Google SRE Workbook Chapter 2 (Implementing SLOs)
- Google SRE Workbook Chapter 5 (Alerting on SLOs)
- Prometheus Best Practices (Alerting)
- All sources accessed 2025-10-25T21:30:36-04:00
