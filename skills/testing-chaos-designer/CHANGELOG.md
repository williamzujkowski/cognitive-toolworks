# Changelog

All notable changes to the chaos-engineering-designer skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-25

### Added
- Initial release of chaos-engineering-designer skill
- T1 tier: Quick experiment design with minimal configuration (≤2k tokens)
- T2 tier: Production-ready experiments with tool-specific configs (≤6k tokens)
- T3 tier: Advanced experiment suites with automation (≤12k tokens)
- Support for Chaos Mesh, LitmusChaos, and Chaos Monkey tooling
- Steady-state hypothesis formulation with measurable metrics
- Blast radius controls and progressive escalation strategies
- Safety controls including abort conditions and rollback procedures
- Example experiment for pod termination testing
- Resource templates for experiment specifications and blast radius configs
- Integration with cloud-native-deployment-orchestrator and devops-pipeline-architect
- Citation of authoritative sources (accessed 2025-10-25T21:30:36-04:00):
  - Principles of Chaos Engineering: https://principlesofchaos.org/
  - Chaos Mesh: https://chaos-mesh.org/
  - LitmusChaos: https://litmuschaos.io/
  - Netflix Chaos Monkey: https://netflix.github.io/chaosmonkey/

### Documentation
- Complete SKILL.md with all required sections per CLAUDE.md §3
- 5 evaluation scenarios in tests/evals_chaos-engineering-designer.yaml
- Example chaos experiment configuration (≤30 lines)
- Experiment template and blast radius configuration resources

### Quality Gates
- Token budgets enforced: T1 ≤2k, T2 ≤6k, T3 ≤12k
- Safety requirements: abort conditions, blast radius bounds, pre-validation
- Auditability: experiment logging, version control, metrics export
- Determinism: reproducible experiments with seeded randomization
