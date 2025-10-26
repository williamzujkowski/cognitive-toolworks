---
name: "Container Image Optimizer"
slug: "container-image-optimizer"
description: "Create optimized Dockerfiles with multi-stage builds, security hardening, and vulnerability scanning for minimal, secure container images."
capabilities:
  - Multi-stage Dockerfile generation for size optimization
  - Language-specific build optimization (Node.js, Python, Go, Java)
  - Security hardening (non-root user, minimal base images)
  - Container vulnerability scanning integration
  - Layer caching optimization for faster builds
  - .dockerignore configuration
inputs:
  - application_language: "nodejs, python, go, java, rust (string)"
  - build_type: "development, production (string)"
  - base_image: "alpine, distroless, scratch, ubuntu (string, optional)"
  - package_manager: "npm, pip, cargo, maven, gradle (string, optional)"
  - exposed_port: "application port (integer, optional)"
  - security_scan: "enable vulnerability scanning (boolean, default: true)"
outputs:
  - dockerfile: "optimized multi-stage Dockerfile"
  - dockerignore: ".dockerignore file content"
  - security_report: "vulnerability scan results and recommendations"
  - build_instructions: "docker build command with optimization flags"
keywords:
  - docker
  - dockerfile
  - container
  - multi-stage-build
  - image-optimization
  - container-security
  - vulnerability-scanning
  - distroless
  - alpine
version: "1.0.0"
owner: "cognitive-toolworks"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://docs.docker.com/build/building/multi-stage/
  - https://docs.docker.com/develop/dev-best-practices/
  - https://docs.docker.com/build/building/best-practices/
  - https://github.com/GoogleContainerTools/distroless
---

## Purpose & When-To-Use

**Trigger conditions:**
- Need to containerize an application with optimal image size
- Converting existing Dockerfile to multi-stage build
- Implementing container security best practices
- Reducing build times through layer caching optimization
- Scanning images for vulnerabilities before deployment

**Not for:**
- Kubernetes manifest generation (use kubernetes-manifest-generator skill)
- Complete deployment orchestration (use cloud-native-orchestrator agent)
- Runtime container orchestration (use Kubernetes or Docker Swarm)
- Container registry management

---

## Pre-Checks

**Time normalization:**
- Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601): 2025-10-26T01:33:54-04:00
- Use `NOW_ET` for all citation access dates

**Input validation:**
- `application_language` must be one of: nodejs, python, go, java, rust
- `build_type` must be: development or production
- `base_image` if specified must be recognized (alpine, distroless, scratch, ubuntu, debian)
- `exposed_port` must be valid port number (1-65535)

**Source freshness:**
- Docker Multi-Stage Builds (accessed 2025-10-26T01:33:54-04:00): https://docs.docker.com/build/building/multi-stage/
- Docker Best Practices (accessed 2025-10-26T01:33:54-04:00): https://docs.docker.com/develop/dev-best-practices/
- Distroless Images (accessed 2025-10-26T01:33:54-04:00): https://github.com/GoogleContainerTools/distroless
- Trivy Scanner (accessed 2025-10-26T01:33:54-04:00): https://github.com/aquasecurity/trivy

**Decision thresholds:**
- T1 for basic multi-stage Dockerfile generation
- T2 for production optimization with security scanning and hardening

---

## Procedure

### T1: Basic Multi-Stage Dockerfile (≤2k tokens)

**Step 1: Generate multi-stage Dockerfile**
- Create build stage with language-specific toolchain
- Create runtime stage with minimal base image
- Copy only built artifacts (no source code or build tools)
- Set appropriate working directory and user

**Step 2: Create .dockerignore**
- Exclude common development files (.git, node_modules, __pycache__)
- Exclude CI/CD and documentation files
- Include only necessary application files

**Output:**
- Basic multi-stage Dockerfile
- .dockerignore file
- docker build command

**Abort conditions:**
- Unsupported language or framework
- Missing critical build information

---

### T2: Production-Optimized Container (≤6k tokens)

**All T1 steps plus:**

**Step 1: Advanced image optimization**
- Select minimal base image (distroless for production, alpine for tools)
- Optimize layer ordering (least-frequently-changed first)
- Combine RUN commands to reduce layers
- Use BuildKit cache mounts for package managers
- Implement build argument for versioning

**Step 2: Security hardening**
- Run as non-root user (create dedicated app user)
- Set read-only root filesystem where possible
- Drop unnecessary capabilities
- Scan image with Trivy or Grype
- Sign image layers (reference Sigstore/Cosign)

**Step 3: Build optimization**
- Configure BuildKit features (cache, secrets)
- Add health check instruction
- Set proper signal handling (STOPSIGNAL)
- Minimize final image size (target <100MB for simple apps)

**Step 4: Generate security report**
- Run vulnerability scanner
- Report CVEs by severity (Critical, High, Medium, Low)
- Provide remediation recommendations
- Check for exposed secrets in layers

**Output:**
- Production-optimized Dockerfile
- Security scan report with CVE details
- Build and scan commands
- Image size comparison (before/after optimization)

**Abort conditions:**
- Critical vulnerabilities found without patches available
- Base image not maintained or deprecated

---

### T3: Advanced Container Engineering (≤12k tokens)

**All T1 + T2 steps plus:**

**Step 1: Multi-architecture builds**
- Configure buildx for ARM64 and AMD64
- Platform-specific optimizations
- Cross-compilation setup

**Step 2: Advanced security**
- SBOM generation with Syft
- Image signing workflow
- Runtime security recommendations (Falco rules)

**Step 3: CI/CD integration**
- GitHub Actions / GitLab CI Dockerfile build pipeline
- Automated vulnerability scanning in CI
- Image promotion workflow

**Output:**
- Multi-arch Dockerfile
- CI/CD pipeline configuration
- SBOM and signed image artifacts
- Comprehensive security compliance report

---

## Decision Rules

**Base image selection:**
- **Distroless** (production): Minimal attack surface, no shell, smallest size
- **Alpine** (tooling needed): Small size, package manager available, shell for debugging
- **Scratch** (static binaries): Go/Rust compiled binaries, absolute minimal
- **Ubuntu/Debian** (compatibility): Legacy dependencies, broader package availability

**Language-specific optimizations:**
- **Node.js**: Use NODE_ENV=production, npm ci --only=production, multi-stage with build dependencies
- **Python**: Use pip install --no-cache-dir, requirements.txt pinning, compiled .pyc files
- **Go**: Static compilation (CGO_ENABLED=0), scratch base, single binary
- **Java**: JRE instead of JDK in runtime, jlink for minimal JRE, GraalVM native image
- **Rust**: Multi-stage with cargo build --release, strip binaries, musl for static linking

**Security scan thresholds:**
- **Critical CVEs**: Block build, require patching
- **High CVEs**: Warn, require review and exception approval
- **Medium/Low CVEs**: Report, track for future updates

**Ambiguity handling:**
- If base_image not specified → select distroless for production, alpine for development
- If package_manager unclear → infer from language (npm for nodejs, pip for python)
- If build process complex → request build script or package.json/requirements.txt

---

## Output Contract

**Required fields (all tiers):**
```dockerfile
# Dockerfile structure
FROM <build-base> AS builder
WORKDIR /build
COPY <dependencies-file> .
RUN <install-dependencies>
COPY . .
RUN <build-command>

FROM <runtime-base>
WORKDIR /app
COPY --from=builder /build/<artifacts> .
USER <non-root-user>
EXPOSE <port>
CMD [<entrypoint>]
```

```yaml
build_instructions:
  command: "docker build -t app:version ."
  buildkit_features: ["cache-mounts", "secrets"]
  estimated_build_time: "2-5 minutes"

image_metrics:
  final_size_mb: integer
  layer_count: integer
  optimization_ratio: "percentage reduction vs single-stage"
```

**Additional T2 fields:**
```yaml
security_report:
  scanner: "trivy | grype"
  scan_timestamp: "ISO-8601"
  vulnerabilities:
    critical: integer
    high: integer
    medium: integer
    low: integer
  recommendations: ["array of remediation steps"]

dockerfile_best_practices:
  non_root_user: boolean
  minimal_base: boolean
  layer_optimization: boolean
  healthcheck_present: boolean
```

**Additional T3 fields:**
```yaml
multi_arch_support:
  platforms: ["linux/amd64", "linux/arm64"]
  buildx_config: "buildx command"

supply_chain_security:
  sbom_file: "syft SBOM JSON"
  signature_verification: "cosign verification command"

ci_cd_integration:
  github_actions: "workflow YAML"
  automated_scanning: boolean
```

---

## Examples

```dockerfile
# T1 Example: Node.js Multi-Stage Dockerfile
FROM node:18-alpine AS builder
WORKDIR /build
COPY package*.json ./
RUN npm ci --only=production
COPY . .
RUN npm run build

FROM node:18-alpine
WORKDIR /app
RUN addgroup -g 1001 -S nodejs && \
    adduser -S nodejs -u 1001
COPY --from=builder /build/dist ./dist
COPY --from=builder /build/node_modules ./node_modules
USER nodejs
EXPOSE 3000
CMD ["node", "dist/index.js"]
```

```
# .dockerignore
node_modules
.git
.env
*.md
.github
tests
coverage
```

---

## Quality Gates

**Token budgets (enforced):**
- **T1**: ≤2,000 tokens - basic multi-stage Dockerfile generation
- **T2**: ≤6,000 tokens - production optimization with security scanning
- **T3**: ≤12,000 tokens - multi-arch, SBOM, CI/CD integration

**Safety checks:**
- No hardcoded secrets in Dockerfile or layers
- Non-root user configured for runtime
- Base images from trusted registries only
- Security scan shows no unpatched Critical CVEs (T2+)

**Auditability:**
- Base image tags are pinned (not :latest)
- Build stages are named and documented
- Security scan results include timestamp and scanner version
- Layer count and size metrics provided

**Determinism:**
- Same inputs produce identical Dockerfile structure
- Package versions pinned in dependency files
- Build process reproducible

**Validation requirements:**
- Dockerfile must pass `docker build` without errors
- T2+ images must pass Trivy scan with acceptable CVE thresholds
- Final image size meets optimization targets (<100MB for simple apps)

---

## Resources

**Official Documentation (accessed 2025-10-26T01:33:54-04:00):**
- Docker Multi-Stage Builds: https://docs.docker.com/build/building/multi-stage/
- Dockerfile Best Practices: https://docs.docker.com/build/building/best-practices/
- Docker BuildKit: https://docs.docker.com/build/buildkit/
- Docker Security: https://docs.docker.com/engine/security/

**Base Images:**
- Distroless Images: https://github.com/GoogleContainerTools/distroless
- Alpine Linux: https://alpinelinux.org/
- Official Docker Images: https://hub.docker.com/_/alpine

**Security Tools:**
- Trivy Scanner: https://github.com/aquasecurity/trivy
- Grype Scanner: https://github.com/anchore/grype
- Syft SBOM Generator: https://github.com/anchore/syft
- Cosign Image Signing: https://github.com/sigstore/cosign

**Optimization Guides:**
- Node.js Docker Best Practices: https://github.com/nodejs/docker-node/blob/main/docs/BestPractices.md
- Python Docker Best Practices: https://docs.python.org/3/using/unix.html#on-linux
- Go Docker Best Practices: https://docs.docker.com/language/golang/build-images/
