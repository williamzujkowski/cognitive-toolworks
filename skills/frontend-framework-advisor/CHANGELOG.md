# Changelog - Frontend Framework Advisor

All notable changes to this skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-10-25

### Added
- Initial implementation of frontend-framework-advisor skill
- Support for 5 frontend platforms: React, Vue, iOS (SwiftUI), Android (Jetpack Compose), React Native
- T1 tier: Quick guidance for component architecture and state management (≤2k tokens)
- T2 tier: Detailed architecture with performance optimization and accessibility (≤6k tokens)
- State management recommendations across all platforms (local state → context → global stores)
- Performance optimization patterns for each platform
- Accessibility implementation guidance (WCAG-AA/AAA compliance)
- Integration with testing-strategy-composer for test planning
- Component hierarchy and file structure recommendations
- Framework/platform selection decision support
- Migration guidance for framework transitions
- Resource templates for platform-specific scaffolding

### Documentation
- Comprehensive SKILL.md with all required sections per CLAUDE.md §3
- Official documentation sources cited with access dates (2025-10-25T21:30:36-04:00)
- Example input/output for React component architecture
- Decision rules for framework selection and state management escalation
- Quality gates with token budgets and safety criteria

### Resources
- Component templates directory structure created
- State management pattern examples prepared
- Performance optimization code snippets ready

### Testing
- Eval scenarios covering all 5 platforms
- T1/T2 tier validation cases
- State complexity edge cases (simple, moderate, complex)
- Migration scenarios (React → Vue, Native → React Native)
- Accessibility requirement tests (WCAG-AA/AAA)

### Dependencies
- Leverages testing-strategy-composer for test strategy integration
- No hard dependencies; operates independently

### Compliance
- All sources from official documentation (React.dev, Vue.js, Apple, Android, React Native)
- WCAG 2.2 accessibility guidelines referenced
- No secrets, PII, or proprietary information
- MIT licensed, safe for public repositories
