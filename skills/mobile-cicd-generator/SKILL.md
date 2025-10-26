---
name: Mobile CI/CD Pipeline Generator
slug: mobile-cicd-generator
description: Generate mobile CI/CD pipelines for iOS (Fastlane, TestFlight) and Android (Gradle, Play Store) with code signing, beta distribution, and crash reporting
version: 1.0.0
owner: cognitive-toolworks
license: MIT
security: public
keywords:
  - mobile
  - ci-cd
  - ios
  - android
  - fastlane
  - testflight
  - play-store
  - react-native
  - flutter
  - github-actions
  - gitlab-ci
  - code-signing
  - beta-distribution
  - crash-reporting

capabilities:
  - Generate GitHub Actions/GitLab CI workflows for mobile builds
  - Configure iOS code signing (Fastlane Match, manual certificates)
  - Set up Android signing configurations (keystore management)
  - Automate TestFlight beta distribution
  - Configure Play Store internal testing and releases
  - Integrate crash reporting (Sentry, Firebase Crashlytics)
  - Support React Native and Flutter dual-platform builds
  - Configure CodePush/over-the-air updates

inputs:
  platform:
    type: enum
    required: true
    values: [ios, android, react-native, flutter]
    description: Target mobile platform
  ci_platform:
    type: enum
    required: true
    values: [github-actions, gitlab-ci, bitrise, app-center]
    description: CI/CD platform for automation
  distribution:
    type: enum
    required: false
    values: [testflight, firebase, appcenter, play-internal]
    description: Beta distribution channel
  signing_method:
    type: enum
    required: false
    values: [manual, fastlane-match, app-center]
    description: Code signing approach
  crash_reporting:
    type: enum
    required: false
    values: [sentry, firebase-crashlytics, none]
    description: Crash reporting integration
  enable_codepush:
    type: boolean
    required: false
    description: Enable CodePush for React Native

outputs:
  ci_pipeline:
    type: file
    format: yaml
    description: GitHub Actions or GitLab CI configuration
  fastlane_config:
    type: file
    format: ruby
    description: Fastfile for iOS automation (if platform=ios)
  gradle_config:
    type: snippet
    format: groovy
    description: Android build.gradle signing config (if platform=android)
  distribution_setup:
    type: document
    format: markdown
    description: TestFlight/Play Store configuration instructions
  secrets_checklist:
    type: document
    format: markdown
    description: Required CI secrets and environment variables

links:
  - title: Fastlane Documentation
    url: https://docs.fastlane.tools/
    accessed: 2025-10-26T03:51:56-04:00
  - title: Android Gradle Plugin User Guide
    url: https://developer.android.com/build
    accessed: 2025-10-26T03:51:56-04:00
  - title: GitHub Actions for Mobile
    url: https://docs.github.com/en/actions/deployment/deploying-xcode-applications
    accessed: 2025-10-26T03:51:56-04:00
  - title: Firebase App Distribution
    url: https://firebase.google.com/docs/app-distribution
    accessed: 2025-10-26T03:51:56-04:00
---

# Mobile CI/CD Pipeline Generator

## Purpose & When-To-Use

Use this skill when you need to:

- **Bootstrap CI/CD** for a new iOS or Android mobile application
- **Automate builds** for React Native or Flutter projects on GitHub Actions or GitLab CI
- **Set up beta distribution** to TestFlight, Firebase App Distribution, or Play Store internal testing
- **Configure code signing** using Fastlane Match or manual certificate management
- **Integrate crash reporting** (Sentry, Firebase Crashlytics) into build pipelines
- **Standardize mobile DevOps** across teams with repeatable pipeline templates

**Trigger conditions:**

- Project lacks automated mobile builds or manual build processes are error-prone
- Need to distribute beta builds to testers or stakeholders regularly
- Require consistent code signing across team members or CI environments
- Want to automate app store submissions and release management

---

## Pre-Checks

Before generating pipelines, verify:

1. **Compute NOW_ET** using NIST/time.gov semantics (America/New_York, ISO-8601) for all access dates
2. **Platform validity:**
   - `platform` ∈ {ios, android, react-native, flutter}
   - `ci_platform` ∈ {github-actions, gitlab-ci, bitrise, app-center}
3. **Input schema sanity:**
   - If `platform=ios`, `signing_method` should be specified (default: fastlane-match)
   - If `platform=android`, ensure keystore details are available or documented
   - If `distribution=testflight`, confirm Apple Developer account and App Store Connect API key access
   - If `distribution=play-internal`, confirm Google Play Console service account JSON
4. **Source freshness:**
   - Fastlane version compatibility (accessed 2025-10-26T03:51:56-04:00): v2.220+
   - Android Gradle Plugin (accessed 2025-10-26T03:51:56-04:00): AGP 8.0+ recommended
   - GitHub Actions runner images (macos-latest for iOS, ubuntu-latest for Android)
5. **Abort if:**
   - Required platform-specific tools are unavailable (Xcode for iOS, Java/Gradle for Android)
   - Code signing credentials or API keys are not provisioned
   - Distribution channel access is not confirmed

---

## Procedure

### T1: Basic Build Pipeline (≤2k tokens)

**Common 80% case:** Compile and test mobile app on CI without distribution.

**Steps:**

1. **Detect platform and CI system** from inputs
2. **Generate base CI workflow:**
   - **iOS:** macOS runner, Xcode build, unit tests
   - **Android:** Ubuntu runner, Gradle assemble, unit tests
   - **React Native/Flutter:** Detect native platforms, run dual iOS+Android jobs
3. **Configure caching:**
   - iOS: `~/Library/Caches/CocoaPods`, `vendor/bundle`
   - Android: `~/.gradle/caches`, `~/.gradle/wrapper`
4. **Run linting and tests:**
   - iOS: `xcodebuild test`
   - Android: `./gradlew test`
   - React Native: `npm test` or `yarn test`
5. **Output:** Basic CI YAML (GitHub Actions or GitLab CI) for build verification

**Example snippet (GitHub Actions, iOS):**

```yaml
name: iOS CI
on: [push, pull_request]
jobs:
  build:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4
      - name: Install dependencies
        run: bundle install
      - name: Build
        run: xcodebuild -workspace App.xcworkspace -scheme App build-for-testing
      - name: Test
        run: xcodebuild test -workspace App.xcworkspace -scheme App -destination 'platform=iOS Simulator,name=iPhone 15'
```

**Token budget:** ~1.5k tokens

---

### T2: Code Signing & Beta Distribution (≤6k tokens)

**Extended case:** Add code signing and automated beta uploads.

**Additional steps:**

1. **iOS code signing setup:**
   - **Fastlane Match:** Configure `Matchfile`, store certificates in encrypted git repo or cloud storage
   - **Manual:** Document certificate/provisioning profile upload to CI secrets
   - Reference: [Fastlane Match documentation](https://docs.fastlane.tools/actions/match/) (accessed 2025-10-26T03:51:56-04:00)
2. **Android code signing:**
   - Generate or use existing keystore file
   - Store keystore password, key alias, key password in CI secrets
   - Add signing config to `build.gradle`:
     ```groovy
     android {
       signingConfigs {
         release {
           storeFile file(System.getenv("KEYSTORE_FILE"))
           storePassword System.getenv("KEYSTORE_PASSWORD")
           keyAlias System.getenv("KEY_ALIAS")
           keyPassword System.getenv("KEY_PASSWORD")
         }
       }
     }
     ```
   - Reference: [Android signing documentation](https://developer.android.com/studio/publish/app-signing) (accessed 2025-10-26T03:51:56-04:00)
3. **Beta distribution:**
   - **TestFlight (iOS):** Use `fastlane pilot upload` or `altool`/Transporter API
     - Requires App Store Connect API key (stored as CI secret)
   - **Firebase App Distribution:** Use `firebase appdistribution:distribute` CLI
     - Reference: [Firebase App Distribution CLI](https://firebase.google.com/docs/app-distribution/android/distribute-cli) (accessed 2025-10-26T03:51:56-04:00)
   - **Play Store Internal Testing (Android):** Use `fastlane supply` or Google Play Developer API
4. **Generate Fastfile (iOS):**
   ```ruby
   lane :beta do
     match(type: "appstore")
     build_app(scheme: "App", export_method: "app-store")
     upload_to_testflight(skip_waiting_for_build_processing: true)
   end
   ```
5. **Output:** CI pipeline with signing and distribution steps, Fastfile, secrets checklist

**Token budget:** ~5k tokens

---

### T3: Release Automation & Crash Reporting (≤12k tokens)

**Deep dive:** Full release pipeline with crash reporting and advanced features.

**Additional steps:**

1. **Production release automation:**
   - **iOS:** Automate App Store submission with screenshots, metadata, phased rollout
   - **Android:** Automate Play Store production track deployment with staged rollout percentages
   - Use `fastlane deliver` (iOS) or `fastlane supply` (Android) with metadata management
2. **Crash reporting integration:**
   - **Sentry:** Add Sentry CLI upload of debug symbols/source maps
     - iOS: Upload dSYMs with `sentry-cli upload-dif`
     - Android: Upload ProGuard/R8 mapping files
     - Reference: [Sentry Mobile Setup](https://docs.sentry.io/platforms/react-native/) (accessed 2025-10-26T03:51:56-04:00)
   - **Firebase Crashlytics:** Integrate Crashlytics SDK, upload symbols automatically
3. **CodePush setup (React Native):**
   - Install `appcenter-cli`, configure CodePush release command
   - Deploy JS bundle updates without app store review
4. **Version bumping and changelog:**
   - Automate version increments (`agvtool`, `gradle version bump`)
   - Generate release notes from git commits or PR descriptions
5. **Notification and reporting:**
   - Slack/Discord notifications on build success/failure
   - Upload build artifacts (IPA, APK, AAB) to GitHub Releases or artifact storage
6. **Evals and quality gates:**
   - Run automated UI tests (Detox, Appium)
   - Performance profiling and bundle size checks
   - Security scanning (dependency audit, SAST)

**Token budget:** ~10k tokens

---

## Decision Rules

**Ambiguity thresholds:**

- If `platform=react-native` or `flutter`, **default to dual iOS+Android builds** unless explicitly single-platform
- If `signing_method` unspecified:
  - iOS: default to `fastlane-match` (team environments)
  - Android: default to `manual` (requires keystore upload)
- If `distribution` unspecified, **stop at T1** (build-only, no beta distribution)
- If `crash_reporting=none`, omit symbol upload steps

**Abort/stop conditions:**

- Missing required CI secrets (certificates, API keys) → output secrets checklist and halt
- Unsupported CI platform (e.g., Jenkins, Travis) → suggest GitHub Actions or GitLab CI migration
- Platform mismatch (e.g., `platform=ios` with `distribution=play-internal`) → reject and clarify

**Escalation:**

- If user needs custom build steps (e.g., native module compilation, custom signing flows), provide hook points in CI YAML and document extension pattern

---

## Output Contract

```typescript
interface MobileCICDOutput {
  ci_pipeline: {
    file_path: string;           // e.g., ".github/workflows/mobile-ci.yml"
    format: "yaml";
    platform: "github-actions" | "gitlab-ci";
    jobs: Array<{
      name: string;               // e.g., "ios-build", "android-release"
      runner: string;             // e.g., "macos-latest", "ubuntu-latest"
      steps: number;              // count of CI steps
    }>;
  };
  fastlane_config?: {             // optional, iOS-only
    file_path: string;            // "fastlane/Fastfile"
    lanes: string[];              // e.g., ["beta", "release"]
  };
  gradle_config?: {               // optional, Android-only
    snippet: string;              // signing config block for build.gradle
  };
  distribution_setup: {
    platform: string;             // "testflight" | "firebase" | "play-internal"
    instructions: string;         // markdown setup guide
    required_credentials: string[]; // e.g., ["APP_STORE_CONNECT_API_KEY"]
  };
  secrets_checklist: {
    secrets: Array<{
      name: string;               // e.g., "MATCH_PASSWORD"
      description: string;
      required_for: string[];     // e.g., ["ios-beta", "ios-release"]
    }>;
  };
  token_usage: number;            // actual tokens consumed
  tier: "T1" | "T2" | "T3";
}
```

**Required fields:**

- `ci_pipeline.file_path` and `ci_pipeline.jobs` (always)
- `secrets_checklist.secrets` (if signing or distribution enabled)
- `distribution_setup` (if T2+)

**Validation:**

- CI YAML must parse without syntax errors
- Fastfile must use valid Fastlane actions
- Gradle snippet must be syntactically valid Groovy

---

## Examples

**Example 1: React Native app with iOS/Android builds and TestFlight beta**

**Input:**
```json
{
  "platform": "react-native",
  "ci_platform": "github-actions",
  "distribution": "testflight",
  "signing_method": "fastlane-match",
  "crash_reporting": "sentry"
}
```

**Output (GitHub Actions excerpt, ≤30 lines):**

```yaml
name: React Native CI/CD
on: [push, pull_request]
jobs:
  ios-beta:
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: npm install
      - name: Install pods
        run: cd ios && pod install
      - name: Fastlane beta
        env:
          MATCH_PASSWORD: ${{ secrets.MATCH_PASSWORD }}
          FASTLANE_USER: ${{ secrets.FASTLANE_USER }}
          FASTLANE_APPLE_APPLICATION_SPECIFIC_PASSWORD: ${{ secrets.APP_SPECIFIC_PASSWORD }}
        run: cd ios && bundle exec fastlane beta
      - name: Upload dSYMs to Sentry
        run: npx sentry-cli upload-dif --org my-org --project my-project ios/build

  android-beta:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-java@v4
        with: { java-version: '17' }
      - run: npm install
      - name: Build release APK
        env:
          KEYSTORE_PASSWORD: ${{ secrets.KEYSTORE_PASSWORD }}
        run: cd android && ./gradlew assembleRelease
      - name: Upload to Firebase
        run: firebase appdistribution:distribute app/build/outputs/apk/release/app-release.apk --app ${{ secrets.FIREBASE_APP_ID }}
```

---

## Quality Gates

**Token budgets (enforced):**

- T1 ≤ 2k tokens (build-only)
- T2 ≤ 6k tokens (signing + beta distribution)
- T3 ≤ 12k tokens (release automation + crash reporting)

**Safety:**

- Never emit secrets directly in YAML; always use `${{ secrets.SECRET_NAME }}` placeholders
- Validate CI secrets exist before pipeline runs (check CI provider docs)
- Warn if keystore or certificates are stored in version control (security risk)

**Auditability:**

- All CI jobs must log build numbers, commit SHAs, and artifact URLs
- Crash reporting symbol uploads must confirm success/failure
- Beta distribution must report uploaded build version and tester group

**Determinism:**

- Pin Fastlane versions in Gemfile
- Pin Gradle plugin versions in build.gradle
- Use locked dependency versions (package-lock.json, Gemfile.lock)

**Performance:**

- Cache dependencies aggressively (CocoaPods, Gradle, npm)
- Parallelize iOS and Android builds when possible
- Avoid redundant builds (skip CI on docs-only changes)

---

## Resources

**Official Documentation (accessed 2025-10-26T03:51:56-04:00):**

- [Fastlane Documentation](https://docs.fastlane.tools/) — iOS/Android automation
- [Fastlane Match](https://docs.fastlane.tools/actions/match/) — Code signing sync
- [Android Gradle Plugin](https://developer.android.com/build) — Build configuration
- [GitHub Actions for Xcode](https://docs.github.com/en/actions/deployment/deploying-xcode-applications) — iOS CI setup
- [Firebase App Distribution](https://firebase.google.com/docs/app-distribution) — Beta distribution
- [Sentry Mobile Platforms](https://docs.sentry.io/platforms/react-native/) — Crash reporting
- [Google Play Publishing API](https://developers.google.com/android-publisher) — Android release automation

**Templates and Tools:**

- [fastlane/examples](https://github.com/fastlane/examples) — Sample Fastfiles
- [react-native-community/releases](https://github.com/react-native-community/releases) — React Native release tooling
- [CodePush CLI](https://github.com/microsoft/code-push) — Over-the-air updates

**Best Practices:**

- Use Fastlane Match for team-based iOS development to avoid certificate conflicts
- Store Android keystores in CI secrets, never commit to version control
- Enable incremental builds and caching to reduce CI duration
- Test beta distributions on real devices before production release
- Monitor crash-free user rates in Sentry/Crashlytics dashboards

---

**END OF SKILL**
