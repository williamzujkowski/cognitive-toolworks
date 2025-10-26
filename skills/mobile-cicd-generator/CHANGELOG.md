# Changelog

All notable changes to the Mobile CI/CD Pipeline Generator skill will be documented in this file.

## [1.0.0] - 2025-10-26

### Added
- Initial release of mobile-cicd-generator skill
- Support for iOS (Fastlane, TestFlight) and Android (Gradle, Play Store) pipelines
- GitHub Actions and GitLab CI workflow generation
- T1: Basic build pipeline with compile and test (≤2k tokens)
- T2: Code signing and beta distribution setup (≤6k tokens)
- T3: Release automation with crash reporting integration (≤12k tokens)
- Fastlane Match integration for iOS code signing
- Android keystore management and signing configuration
- TestFlight, Firebase App Distribution, and Play Store internal testing support
- Sentry and Firebase Crashlytics crash reporting integration
- React Native and Flutter dual-platform build support
- CodePush over-the-air update configuration
- Comprehensive secrets checklist for CI/CD setup
- Example GitHub Actions workflow for React Native dual-platform
- 5 evaluation scenarios covering iOS, Android, React Native, Flutter, and production releases

### Documentation
- Detailed procedure with three progressive tiers (T1/T2/T3)
- Decision rules for platform detection and configuration defaults
- TypeScript output contract specification
- Quality gates for security, auditability, and determinism
- Resource links to Fastlane, Android Gradle Plugin, Firebase, and Sentry documentation
- All source links accessed and verified on 2025-10-26T03:51:56-04:00
