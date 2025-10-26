---
name: "Go Project Scaffolder"
slug: go-project-scaffolder
description: "Generate Go project structure with modules, testing (testify), mocking (gomock), linting (golangci-lint), and build tooling (Makefiles, goreleaser)."
capabilities:
  - generate_project_structure
  - configure_testing_frameworks
  - setup_build_automation
  - create_ci_templates
inputs:
  project_type:
    type: string
    description: "Project type: cli, microservice, library, grpc-service"
    required: true
  project_name:
    type: string
    description: "Module name (e.g., github.com/org/project)"
    required: true
  features:
    type: array
    description: "Enabled features: testing, mocking, linting, build-automation, ci, wire, otel"
    required: true
outputs:
  project_layout:
    type: object
    description: "Directory structure with files and purposes"
  go_mod:
    type: code
    description: "go.mod module definition"
  makefile:
    type: code
    description: "Makefile with build/test/lint targets"
  ci_template:
    type: code
    description: "GitHub Actions workflow (optional)"
keywords:
  - golang
  - project-scaffolding
  - testify
  - gomock
  - golangci-lint
  - goreleaser
  - makefile
  - grpc
  - wire
  - opentelemetry
version: 1.0.0
owner: william@cognitive-toolworks
license: MIT
security:
  pii: false
  secrets: false
  sandbox: required
links:
  - https://go.dev/doc/modules/layout
  - https://github.com/golang-standards/project-layout
  - https://golangci-lint.run/docs/configuration/
  - https://goreleaser.com/
---

## Purpose & When-To-Use

**Trigger conditions:**

- Starting a new Go project from scratch
- Migrating from unstructured Go code to standard layout
- Adding testing, linting, or build automation to existing Go project
- Setting up CI/CD for Go applications
- Creating gRPC services with dependency injection and observability
- Scaffolding Go libraries for public or internal distribution

**Use this skill when** you need a production-ready Go project structure with modern tooling, testing frameworks, linters, and build automation configured correctly from the start.

---

## Pre-Checks

**Before execution, verify:**

1. **Time normalization**: `NOW_ET = 2025-10-26T02:31:24-05:00` (NIST/time.gov semantics, America/New_York)
2. **Input schema validation**:
   - `project_type` is one of: `cli`, `microservice`, `library`, `grpc-service`
   - `project_name` follows Go module naming convention (e.g., domain/org/repo)
   - `features` contains valid identifiers: `testing`, `mocking`, `linting`, `build-automation`, `ci`, `wire`, `otel`
3. **Source freshness**: All cited sources accessed on `NOW_ET`; verify documentation links current
4. **Tooling availability**: Go 1.21+, golangci-lint, goreleaser (if build-automation enabled)

**Abort conditions:**

- Invalid project_name (does not match Go module path format)
- Conflicting features (e.g., `library` + `grpc-service`)
- Features reference unavailable tools (e.g., wire/otel without microservice/grpc-service types)

---

## Procedure

### Tier 1 (Fast Path, ≤2k tokens)

**Token budget**: ≤2k tokens

**Scope**: Generate basic Go project with go.mod, standard directory layout, and minimal Makefile.

**Steps:**

1. **Determine project structure** (400 tokens):
   - **CLI**: `/cmd/<app-name>/main.go`, `/internal/<pkg>`, optional `/pkg`
   - **Library**: Root package files, `/internal` for private code
   - **Microservice/gRPC**: `/cmd/server/main.go`, `/internal/{handler,service,repository}`, `/api` for protobuf
   - Follow official Go layout guidance (accessed 2025-10-26T02:31:24-05:00): [go.dev/doc/modules/layout](https://go.dev/doc/modules/layout)

2. **Generate core files** (1200 tokens):
   - **go.mod**: Module name, Go version 1.21+
   - **main.go** or entry point in `/cmd`
   - **internal/** packages with basic structure
   - **README.md** with project description and build instructions
   - **.gitignore** for Go artifacts (binaries, vendor/, etc.)

3. **Create basic Makefile** (400 tokens):
   - Targets: `build`, `test`, `clean`
   - Build command: `go build -o bin/<app-name> ./cmd/<app-name>`
   - Test command: `go test -v ./...`

**Output:** Project directory structure, go.mod, Makefile, .gitignore

---

### Tier 2 (Extended, ≤6k tokens)

**Token budget**: ≤6k tokens

**Scope**: Add testing (testify), linting (golangci-lint), and enhanced Makefile with coverage reports.

**Steps:**

1. **Configure testing framework** (1500 tokens):
   - Add testify dependency: `go get github.com/stretchr/testify`
   - Create example test file: `internal/<pkg>/<pkg>_test.go`
   - Use testify assertions and suites
   - Configure test coverage: `go test -coverprofile=coverage.out ./...`
   - Add coverage HTML report: `go tool cover -html=coverage.out -o coverage.html`

2. **Setup mocking (if enabled)** (1000 tokens):
   - Install gomock: `go install github.com/golang/mock/mockgen@latest`
   - Add mockgen command to generate mocks from interfaces
   - Create `/mocks` directory for generated mocks
   - Example: `mockgen -source=internal/service/user.go -destination=mocks/user_mock.go`

3. **Configure golangci-lint** (2000 tokens):
   - Create `.golangci.yml` with v2 configuration (accessed 2025-10-26T02:31:24-05:00): [golangci-lint.run/docs/configuration](https://golangci-lint.run/docs/configuration/)
   - Set `version: "2"` at top of config
   - Use `linters.default: standard` for baseline linters
   - Enable recommended linters: `errcheck`, `gosimple`, `govet`, `ineffassign`, `staticcheck`, `unused`
   - Add exclusion presets: `common-false-positives`
   - Configure path handling with `${base-path}` placeholder

4. **Enhance Makefile** (1500 tokens):
   - Add `lint` target: `golangci-lint run ./...`
   - Add `test-coverage` target with coverage thresholds
   - Add `fmt` target: `go fmt ./...`
   - Add `vet` target: `go vet ./...`
   - Add `install-tools` target for gomock, golangci-lint

**Output:** Enhanced project with testify tests, gomock setup, .golangci.yml, comprehensive Makefile

---

### Tier 3 (Deep Dive, ≤12k tokens)

**Token budget**: ≤12k tokens

**Scope**: Full production setup with CI/CD, goreleaser, Wire dependency injection, and OpenTelemetry instrumentation.

**Steps:**

1. **Setup goreleaser** (2500 tokens):
   - Create `.goreleaser.yml` config (accessed 2025-10-26T02:31:24-05:00): [goreleaser.com](https://goreleaser.com/)
   - Configure build targets for multiple platforms (linux, darwin, windows)
   - Setup GitHub release creation with changelog
   - Configure archives (tar.gz, zip) and checksums
   - Optional: Docker image builds and Homebrew tap publishing
   - Add `release` target to Makefile: `goreleaser release --clean`

2. **Generate GitHub Actions CI** (2000 tokens):
   - Create `.github/workflows/ci.yml`
   - Jobs: `test`, `lint`, `build`, optional `release`
   - Test job: Run tests on multiple Go versions (1.21, 1.22)
   - Lint job: Run golangci-lint with uploaded results
   - Build job: Compile for linux/amd64
   - Release job: Trigger goreleaser on tag push
   - Add status badges to README.md

3. **Wire dependency injection (microservice/grpc-service)** (3000 tokens):
   - Install Wire: `go install github.com/google/wire/cmd/wire@latest`
   - Create `/internal/di/wire.go` with provider sets
   - Define providers for services, repositories, handlers
   - Generate `/internal/di/wire_gen.go` via `wire`
   - Add `wire` target to Makefile
   - Example: `func InitializeServer(cfg Config) (*Server, error)` with auto-generated deps

4. **OpenTelemetry instrumentation (grpc-service)** (3000 tokens):
   - Add OTel dependencies: `go.opentelemetry.io/otel`, `go.opentelemetry.io/contrib/instrumentation/google.golang.org/grpc/otelgrpc`
   - Create `/internal/telemetry/tracer.go` with OTel setup
   - Configure trace exporter (OTLP, Jaeger, or stdout)
   - Add middleware to gRPC server for automatic tracing
   - Include context propagation across service boundaries
   - Add metrics and logging with structured fields

5. **gRPC-specific setup** (1500 tokens):
   - Create `/api/proto/<service>.proto` with service definitions
   - Add `buf.yaml` for protobuf linting and breaking change detection
   - Generate Go code: `protoc --go_out=. --go-grpc_out=. api/proto/*.proto`
   - Create `/internal/server/grpc.go` with gRPC server setup
   - Add reflection for grpcurl/grpcui compatibility
   - Create Makefile target: `proto-gen` for code generation

**Output:** Production-ready project with CI/CD, multi-platform releases, dependency injection, and observability instrumentation.

---

## Decision Rules

**Project type selection:**

- **CLI**: Single-purpose command-line tool with flags/subcommands → use `/cmd/<app-name>`, no server logic
- **Library**: Reusable package for import by other projects → root package files, minimal `/cmd`, focus on `/pkg` or root
- **Microservice**: HTTP/REST API service → `/cmd/server`, `/internal/{handler,service,repository}`, optional `/api`
- **gRPC-service**: gRPC API service → same as microservice + `/api/proto`, protobuf tooling, reflection

**Feature escalation thresholds:**

- **Testing**: Always recommended; skip only for throwaway prototypes
- **Mocking**: Enable for projects with >3 interfaces/dependencies; skip for simple libraries
- **Linting**: Always enable for team projects; optional for personal experiments
- **Build-automation (goreleaser)**: Enable for public releases or multi-platform distributions
- **CI**: Enable for team projects, public repos, or any project with >1 contributor
- **Wire**: Enable for microservices/gRPC with >5 dependencies; adds complexity, use only when needed
- **OTel**: Enable for production microservices/gRPC; essential for distributed tracing

**Abort/ask conditions:**

- User provides incompatible feature combinations → ask for clarification
- Project type unclear from description → prompt with examples
- Missing critical context (e.g., gRPC service without protobuf schemas) → request schemas or generate placeholder

---

## Output Contract

**Schema:**

```yaml
project_layout:
  type: object
  properties:
    directories:
      type: array
      items:
        path: string          # e.g., "/cmd/server"
        purpose: string       # e.g., "gRPC server entry point"
    files:
      type: array
      items:
        path: string          # e.g., "go.mod"
        content: string       # full file content
        description: string   # e.g., "Go module definition"

go_mod:
  type: string
  format: go.mod
  required_fields:
    - module
    - go

makefile:
  type: string
  format: makefile
  required_targets:
    - build
    - test
    - clean

ci_template:
  type: string
  format: yaml
  conditions: if "ci" in features
```

**Required fields:**

- `project_layout.directories`: At minimum `/cmd` or root package
- `project_layout.files`: Must include `go.mod`, entry point (`main.go`), `.gitignore`
- `go_mod`: Valid Go module with semantic version (e.g., `go 1.21`)
- `makefile`: Functional build, test, clean targets

---

## Examples

**Example 1: CLI Project with Testing**

```yaml
# Input
project_type: cli
project_name: github.com/example/mytool
features: [testing, linting]

# Output (project_layout excerpt)
directories:
  - path: /cmd/mytool
    purpose: CLI entry point
  - path: /internal/commands
    purpose: CLI command implementations
  - path: /internal/commands
    purpose: Unit tests for commands

files:
  - path: go.mod
    content: |
      module github.com/example/mytool
      go 1.21
  - path: Makefile
    content: |
      .PHONY: build test lint clean
      build:
        go build -o bin/mytool ./cmd/mytool
      test:
        go test -v -cover ./...
      lint:
        golangci-lint run ./...
      clean:
        rm -rf bin/
```

---

## Quality Gates

**Token budgets (enforced):**

- **T1**: ≤2k tokens for basic project setup
- **T2**: ≤6k tokens for testing + linting
- **T3**: ≤12k tokens for full production setup

**Safety checks:**

- No hardcoded secrets in generated files (API keys, passwords)
- .gitignore includes all Go build artifacts and OS-specific files
- go.mod uses semantic versioning and current stable Go version

**Auditability:**

- All generated files include comments explaining purpose
- Makefile targets documented with inline comments
- CI workflows include descriptive job/step names

**Determinism:**

- Same inputs always produce same project structure
- Generated code follows gofmt and golangci-lint standards
- Dependency versions pinned where possible (e.g., Go version in go.mod, golangci-lint in CI)

**Source requirements:**

- Cite official Go docs, golangci-lint docs, goreleaser docs
- Include access date for all external references
- Verify links resolve before output

---

## Resources

**Official Documentation:**

- [Go Module Layout](https://go.dev/doc/modules/layout) - Official Go team guidance on organizing Go modules (accessed 2025-10-26T02:31:24-05:00)
- [golang-standards/project-layout](https://github.com/golang-standards/project-layout) - Community-driven Go project structure patterns (accessed 2025-10-26T02:31:24-05:00)
- [golangci-lint Configuration](https://golangci-lint.run/docs/configuration/) - Official configuration docs for golangci-lint v2 (accessed 2025-10-26T02:31:24-05:00)
- [GoReleaser Documentation](https://goreleaser.com/) - Release automation tool for Go projects (accessed 2025-10-26T02:31:24-05:00)

**Testing & Mocking:**

- [testify](https://github.com/stretchr/testify) - Popular assertion and mocking toolkit
- [gomock](https://github.com/golang/mock) - Official Go mocking framework

**Dependency Injection & Observability:**

- [Wire](https://github.com/google/wire) - Compile-time dependency injection
- [OpenTelemetry Go](https://opentelemetry.io/docs/instrumentation/go/) - Observability instrumentation

**CI/CD:**

- [GitHub Actions for Go](https://docs.github.com/en/actions/automating-builds-and-tests/building-and-testing-go) - Official GitHub Actions guide for Go projects
