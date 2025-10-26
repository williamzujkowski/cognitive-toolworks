---
name: "Java Tooling Specialist"
slug: "tooling-java-generator"
description: "Generate Java project scaffolding with Maven/Gradle, JUnit 5, Mockito, Checkstyle/SpotBugs, and packaging (JAR/WAR/native-image)."
capabilities:
  - Project structure generation (library, application, Spring Boot, microservice)
  - Build tool setup (Maven, Gradle, multi-module)
  - Testing framework configuration (JUnit 5, Mockito, TestContainers)
  - Code quality tools (Checkstyle, SpotBugs, PMD, Error Prone)
  - Packaging and distribution (JAR, WAR, Docker, GraalVM native-image)
  - CI/CD integration (GitHub Actions, Jenkins)
inputs:
  - project_type: "library | application | spring-boot | microservice (string)"
  - build_tool: "maven | gradle (string)"
  - java_version: "11 | 17 | 21 (string)"
  - project_name: "Name of the project (string)"
outputs:
  - project_structure: "Directory layout with all config files (JSON)"
  - build_config: "Complete pom.xml or build.gradle configuration"
  - ci_config: "GitHub Actions or Jenkins pipeline (YAML)"
  - dockerfile: "Multi-stage Dockerfile (optional)"
keywords:
  - java
  - tooling
  - maven
  - gradle
  - junit
  - spring-boot
  - mockito
  - checkstyle
  - packaging
version: "1.0.0"
owner: "cognitive-toolworks"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://maven.apache.org/guides/
  - https://docs.gradle.org/current/userguide/userguide.html
  - https://junit.org/junit5/docs/current/user-guide/
  - https://spring.io/projects/spring-boot
  - https://www.graalvm.org/latest/reference-manual/native-image/
---

## Purpose & When-To-Use

**Trigger conditions:**
- Starting a new Java project requiring modern tooling
- Migrating legacy Java projects to contemporary best practices (Java 11+)
- Standardizing build configuration across multiple Java projects
- Setting up Spring Boot microservices with testing infrastructure
- Creating multi-module Maven/Gradle projects

**Not for:**
- Android projects (use `tooling-kotlin-generator` instead)
- Legacy Java 8 projects (use framework-specific generators)
- Simple scripts without dependencies

---

## Pre-Checks

**Time normalization:**
- Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601)
- Use `NOW_ET` for all citation access dates

**Input validation:**
- `project_type` must be one of: library, application, spring-boot, microservice
- `build_tool` must be one of: maven, gradle
- `java_version` must be one of: 11, 17, 21 (LTS versions)
- `project_name` must be valid Java package name (lowercase, dots/hyphens allowed)

**Source freshness:**
- Maven docs must be accessible [accessed 2025-10-26](https://maven.apache.org/guides/)
- Gradle docs must be accessible [accessed 2025-10-26](https://docs.gradle.org/)
- JUnit 5 docs must be accessible [accessed 2025-10-26](https://junit.org/junit5/)
- Spring Boot docs must be accessible [accessed 2025-10-26](https://spring.io/projects/spring-boot)

---

## Procedure

### T1: Basic Project Structure (≤2k tokens)

**Fast path for common cases:**

1. **Directory Layout Generation**
   - Maven standard directory structure:
     ```
     project-name/
       src/
         main/
           java/com/example/project/
           resources/
         test/
           java/com/example/project/
           resources/
       pom.xml (Maven) or build.gradle (Gradle)
       README.md
       .gitignore
     ```

2. **Core Build Configuration**
   - **Maven (pom.xml)** [accessed 2025-10-26](https://maven.apache.org/pom.html)
     - Project metadata (groupId, artifactId, version)
     - Java version configuration (maven.compiler.source/target)
     - Basic dependencies (JUnit 5, logging)
   - **Gradle (build.gradle)** [accessed 2025-10-26](https://docs.gradle.org/current/samples/sample_building_java_libraries.html)
     - Plugins: java-library, application
     - Java toolchain configuration
     - Dependency management

3. **Basic .gitignore**
   - Build outputs (target/, build/, *.class)
   - IDE files (.idea/, *.iml, .vscode/)
   - OS files (.DS_Store)

**Decision:** If only basic scaffolding needed → STOP at T1; otherwise proceed to T2.

---

### T2: Full Tooling Setup (≤6k tokens)

**Extended configuration with testing and quality tools:**

1. **Testing Framework Configuration**

   **JUnit 5 + Mockito** [accessed 2025-10-26](https://junit.org/junit5/docs/current/user-guide/)

   Maven dependencies:
   ```xml
   <dependency>
     <groupId>org.junit.jupiter</groupId>
     <artifactId>junit-jupiter</artifactId>
     <version>5.10.1</version>
     <scope>test</scope>
   </dependency>
   <dependency>
     <groupId>org.mockito</groupId>
     <artifactId>mockito-core</artifactId>
     <version>5.8.0</version>
     <scope>test</scope>
   </dependency>
   <dependency>
     <groupId>org.mockito</groupId>
     <artifactId>mockito-junit-jupiter</artifactId>
     <version>5.8.0</version>
     <scope>test</scope>
   </dependency>
   ```

   Gradle (build.gradle):
   ```gradle
   dependencies {
       testImplementation 'org.junit.jupiter:junit-jupiter:5.10.1'
       testImplementation 'org.mockito:mockito-core:5.8.0'
       testImplementation 'org.mockito:mockito-junit-jupiter:5.8.0'
   }

   test {
       useJUnitPlatform()
   }
   ```

2. **Code Quality Tools**

   **Checkstyle** [accessed 2025-10-26](https://checkstyle.sourceforge.io/)
   - Maven plugin configuration
   - Google Java Style or Sun checks

   **SpotBugs** [accessed 2025-10-26](https://spotbugs.github.io/)
   - Static analysis for bug patterns
   - Integration with Maven/Gradle

   **PMD** (optional)
   - Code quality rules
   - Copy-paste detection (CPD)

3. **Build Plugins**
   - maven-surefire-plugin (test execution)
   - maven-failsafe-plugin (integration tests)
   - jacoco-maven-plugin (code coverage)
   - maven-enforcer-plugin (dependency convergence)

4. **Spring Boot Configuration** (if `project_type == spring-boot`)
   ```xml
   <parent>
     <groupId>org.springframework.boot</groupId>
     <artifactId>spring-boot-starter-parent</artifactId>
     <version>3.2.0</version>
   </parent>
   ```

---

### T3: Packaging and Distribution (≤12k tokens)

**Deep configuration for production deployment:**

1. **JAR/WAR Packaging** [accessed 2025-10-26](https://maven.apache.org/plugins/maven-jar-plugin/)
   - Executable JAR with manifest (Main-Class, Class-Path)
   - Fat JAR with maven-shade-plugin or gradle shadow plugin
   - WAR for servlet containers

2. **Multi-Module Project Structure**
   - Parent POM with dependency management
   - Module structure (api, core, service, integration-tests)
   - Build reactor configuration

3. **GraalVM Native Image** [accessed 2025-10-26](https://www.graalvm.org/latest/reference-manual/native-image/)
   - native-maven-plugin configuration
   - Reflection configuration (reflect-config.json)
   - Resource configuration
   - Build optimizations

4. **Docker Packaging**
   - Multi-stage Dockerfile:
     ```dockerfile
     FROM maven:3.9-eclipse-temurin-21 AS build
     WORKDIR /app
     COPY pom.xml .
     RUN mvn dependency:go-offline
     COPY src src
     RUN mvn package -DskipTests

     FROM eclipse-temurin:21-jre-alpine
     COPY --from=build /app/target/*.jar app.jar
     ENTRYPOINT ["java", "-jar", "/app.jar"]
     ```

5. **CI/CD Pipeline**
   - GitHub Actions workflow (build, test, package, deploy)
   - Jenkins declarative pipeline
   - SonarQube integration
   - Artifact publishing (Maven Central, GitHub Packages)

6. **TestContainers Integration** (for integration tests)
   ```java
   @Testcontainers
   class IntegrationTest {
       @Container
       static PostgreSQLContainer<?> postgres =
           new PostgreSQLContainer<>("postgres:16-alpine");
   }
   ```

---

## Decision Rules

**Build Tool Selection:**
- **Maven:** Enterprise projects, strict dependency management, plugin ecosystem
- **Gradle:** Modern build performance, Kotlin DSL, flexible configuration

**Project Type Structure:**
- **library:** JAR packaging, no main class, extensive testing
- **application:** Executable JAR, main class, CLI or batch processing
- **spring-boot:** Spring Boot parent POM, auto-configuration, embedded server
- **microservice:** Spring Boot + Docker + health checks + observability

**Abort Conditions:**
- Invalid `project_name` (contains spaces, uppercase, invalid chars) → error
- Unsupported `java_version` (<11) → error "Minimum Java 11 required"
- Conflicting configuration (WAR + GraalVM) → error with alternatives

**Tool Version Selection:**
- Use latest stable LTS Java version (11, 17, 21)
- Pin test dependencies, use version ranges for compile deps (Maven)
- Use Gradle version catalog for multi-module projects

---

## Output Contract

**Schema (JSON):**

```json
{
  "project_name": "string",
  "project_type": "library | application | spring-boot | microservice",
  "java_version": "string",
  "build_tool": "maven | gradle",
  "structure": {
    "directories": ["string"],
    "files": {
      "path/to/file": "file content (string)"
    }
  },
  "commands": {
    "build": "string",
    "test": "string",
    "package": "string",
    "run": "string (optional)"
  },
  "next_steps": ["string"],
  "timestamp": "ISO-8601 string (NOW_ET)"
}
```

**Required Fields:**
- `project_name`, `project_type`, `java_version`, `build_tool`, `structure`, `commands`, `next_steps`, `timestamp`

**File Contents:**
- All generated files must be syntactically valid (XML, Gradle, Java)
- Include inline comments explaining non-obvious configuration
- Reference official documentation in comments

---

## Examples

**Example 1: Spring Boot Microservice with Maven**

```
INPUT: {
  project_type: "spring-boot",
  build_tool: "maven",
  java_version: "21",
  project_name: "user-service"
}

OUTPUT:
structure:
  - src/main/java/com/example/userservice/
    - UserServiceApplication.java
    - controller/UserController.java
    - service/UserService.java
    - repository/UserRepository.java
  - src/main/resources/
    - application.yml
  - src/test/java/com/example/userservice/
    - UserServiceApplicationTests.java
  - pom.xml
  - Dockerfile

pom.xml excerpt:
<parent>
  <groupId>org.springframework.boot</groupId>
  <artifactId>spring-boot-starter-parent</artifactId>
  <version>3.2.0</version>
</parent>

commands:
  build: "mvn clean install"
  test: "mvn test"
  package: "mvn package"
  run: "mvn spring-boot:run"
```

_(Full output truncated for ≤30 line limit)_

---

## Quality Gates

**Token Budgets:**
- **T1:** ≤2k tokens (basic structure + core build config)
- **T2:** ≤6k tokens (full tooling: testing, quality, Spring Boot)
- **T3:** ≤12k tokens (packaging, multi-module, native-image, CI/CD)

**Safety:**
- No hardcoded credentials or API keys
- .gitignore always includes sensitive file patterns
- Docker images use non-root users

**Auditability:**
- All tool configurations cite official documentation
- Version constraints are explicit (no floating versions)
- Generated files include generation timestamp and tool versions

**Determinism:**
- Same inputs → identical file structure and configuration
- Tool versions pinned to specific releases
- No randomness in file generation

**Performance:**
- T1 generation: <1 second
- T2 generation: <3 seconds (includes all configs)
- T3 generation: <5 seconds (includes Docker, CI/CD)

---

## Resources

**Official Documentation (accessed 2025-10-26):**
1. [Maven Documentation](https://maven.apache.org/guides/) - Build tool and POM reference
2. [Gradle User Guide](https://docs.gradle.org/current/userguide/userguide.html) - Build automation
3. [JUnit 5 User Guide](https://junit.org/junit5/docs/current/user-guide/) - Testing framework
4. [Spring Boot Documentation](https://spring.io/projects/spring-boot) - Framework reference
5. [GraalVM Native Image](https://www.graalvm.org/latest/reference-manual/native-image/) - Native compilation
6. [Checkstyle](https://checkstyle.sourceforge.io/) - Code style checking
7. [SpotBugs](https://spotbugs.github.io/) - Static analysis
8. [Testcontainers](https://testcontainers.com/) - Integration testing

**Build Tools:**
- [Maven Central Repository](https://search.maven.org/) - Dependency search
- [Gradle Plugin Portal](https://plugins.gradle.org/) - Gradle plugins
- [Maven Wrapper](https://maven.apache.org/wrapper/) - Portable builds
- [Gradle Wrapper](https://docs.gradle.org/current/userguide/gradle_wrapper.html) - Version management

**Best Practices:**
- [Google Java Style Guide](https://google.github.io/styleguide/javaguide.html) - Code formatting
- [Effective Java (3rd Edition)](https://www.oreilly.com/library/view/effective-java/9780134686097/) - Best practices
- [Spring Boot Best Practices](https://spring.io/guides/tutorials/rest/) - Framework patterns
