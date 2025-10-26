---
name: "Rust Safety & Performance Analyzer"
slug: "rust-analyzer"
description: "Review Rust code for memory safety, concurrency patterns, performance optimization, and ecosystem tooling (cargo, clippy, rustfmt)."
capabilities:
  - Memory safety analysis (ownership, borrowing, lifetimes)
  - Concurrency pattern validation (Arc/Mutex, channels, async/await)
  - Performance optimization detection (zero-copy, SIMD, allocations)
  - Unsafe code review and soundness verification
  - Ecosystem tooling integration (cargo, clippy, rustfmt)
  - Tokio runtime efficiency analysis
inputs:
  - code_path: "file or directory path (string)"
  - analysis_focus: "safety | concurrency | performance | all (string, default: all)"
  - rust_edition: "2018 | 2021 (string, default: 2021)"
  - check_unsafe: "boolean (default: true)"
outputs:
  - safety_report: "JSON with ownership/borrowing issues, lifetime problems"
  - concurrency_analysis: "Race conditions, deadlocks, async patterns"
  - performance_recommendations: "Optimization opportunities with impact estimates"
  - ecosystem_suggestions: "Crate recommendations and tooling config"
keywords:
  - rust
  - memory-safety
  - concurrency
  - performance
  - async
  - tokio
  - ownership
  - borrowing
  - zero-copy
version: "1.0.0"
owner: "cognitive-toolworks"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://doc.rust-lang.org/book/
  - https://docs.rs/tokio/latest/tokio/
  - https://nnethercote.github.io/perf-book/
  - https://rust-lang.github.io/api-guidelines/
  - https://doc.rust-lang.org/nomicon/
---

## Purpose & When-To-Use

**Trigger conditions:**
- Pre-merge code review for Rust projects requiring safety/performance validation
- Auditing async services using tokio for runtime efficiency and concurrency bugs
- Performance optimization of hot paths in production Rust code
- Unsafe code review requiring soundness verification
- Evaluating third-party Rust dependencies for quality and safety

**Not for:**
- Basic syntax errors (use `cargo check` or rust-analyzer LSP)
- Build configuration issues (use `cargo` diagnostics)
- API design patterns (use api-design-validator skill)
- Security vulnerability scanning (use cargo-audit, cargo-deny)

---

## Pre-Checks

**Time normalization:**
- Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601)
- Use `NOW_ET` for all citation access dates

**Input validation:**
- `code_path` must exist and contain valid Rust code (.rs files)
- `analysis_focus` must be one of: "safety", "concurrency", "performance", "all"
- `rust_edition` must be "2018" or "2021" (affects borrow checker and async behavior)
- `check_unsafe` must be boolean (controls unsafe block analysis depth)

**Source freshness:**
- Verify Rust Book, Tokio docs, Performance Book links return HTTP 200
- If analyzing against specific Rust version, verify tooling matches (rustc --version)
- Check clippy version compatibility with edition (clippy --version)

**Prerequisites:**
- Rust toolchain installed (rustc, cargo, clippy, rustfmt)
- For async analysis: tokio crate version noted (affects runtime behavior)
- For SIMD: target architecture specified (x86_64, aarch64, etc.)

---

## Procedure

### T1: Basic Safety Review (≤2k tokens)

**Fast path for ownership/borrowing issues:**

1. **Ownership Analysis**
   - Check move semantics: variables used after move
   - Validate clone usage: unnecessary clones on Copy types
   - Detect double-free potential in manual Drop implementations

2. **Borrowing Rules**
   - Mutable borrow conflicts: &mut T alongside &T or other &mut T
   - Lifetime elision issues: implicit lifetimes causing unexpected behavior
   - Self-referential structs without Pin<Box<T>>

3. **Quick Safety Score**
   - Calculate: `100 - (borrow_errors×15 + move_errors×10 + lifetime_warnings×5)`
   - Flag critical issues requiring immediate attention

**Decision:** If `analysis_focus == "safety"` AND score >90 → STOP at T1; otherwise proceed to T2.

**References:**
- [The Rust Programming Language - Ownership](https://doc.rust-lang.org/book/ch04-00-understanding-ownership.html) (accessed 2025-10-26T03:52:00-04:00)
- [Rust Reference - Lifetime Elision](https://doc.rust-lang.org/reference/lifetime-elision.html) (accessed 2025-10-26T03:52:00-04:00)

---

### T2: Concurrency Patterns (≤6k tokens)

**Extended validation for async/await and synchronization:**

1. **Tokio Runtime Patterns**
   - Blocking calls in async context: detect `std::fs`, `std::thread::sleep` in async fns
   - Task spawning efficiency: analyze spawn vs spawn_blocking usage
   - Runtime selection: multi-threaded vs current-thread appropriateness
   - Resource leaks: uncancelled tasks, unbounded channels

   **Reference:** [Tokio Tutorial](https://tokio.rs/tokio/tutorial) (accessed 2025-10-26T03:52:00-04:00)

2. **Synchronization Primitives**
   - Arc/Mutex vs Arc/RwLock: read-heavy workloads using Mutex
   - Deadlock detection: lock acquisition order analysis
   - Channel selection: mpsc vs broadcast vs watch appropriateness
   - Atomic operations: relaxed ordering correctness

   **Reference:** [Rust Atomics and Locks](https://marabos.nl/atomics/) (accessed 2025-10-26T03:52:00-04:00)

3. **Async Patterns**
   - Future combinators: inefficient sequential await chains (use join!/try_join!)
   - Select bias: fairness in tokio::select! branches
   - Cancellation safety: .await points losing data on task cancellation
   - Send bounds: non-Send types crossing .await boundaries

   **Reference:** [Tokio: Async in Depth](https://tokio.rs/tokio/tutorial/async) (accessed 2025-10-26T03:52:00-04:00)

4. **Concurrency Score Adjustment**
   - Apply weights: `deadlock_risk×20 + race_condition×15 + resource_leak×10`
   - Recommend fixes with async/sync trade-off analysis

---

### T3: Performance Optimization (≤12k tokens)

**Deep dive into zero-copy, allocations, and SIMD:**

1. **Allocation Analysis**
   - Unnecessary heap allocations: detect Box/Vec/String where stack works
   - Collection pre-sizing: Vec::with_capacity, HashMap::with_capacity
   - Copy-on-write: evaluate Cow usage opportunities
   - String concatenation: += vs format! vs join() efficiency

   **Reference:** [Rust Performance Book - Heap Allocations](https://nnethercote.github.io/perf-book/heap-allocations.html) (accessed 2025-10-26T03:52:00-04:00)

2. **Zero-Copy Patterns**
   - Slice usage: &[T] vs Vec<T> in function signatures
   - AsRef/Borrow traits: generic borrowing for API flexibility
   - MaybeUninit: safe uninitialized memory for hot paths
   - Bytes crate: efficient buffer management in network code

   **Reference:** [Rust Performance Book - Type Sizes](https://nnethercote.github.io/perf-book/type-sizes.html) (accessed 2025-10-26T03:52:00-04:00)

3. **SIMD Opportunities**
   - Auto-vectorization blockers: iterator chains preventing SIMD
   - Explicit SIMD: std::simd usage for data-parallel operations
   - Alignment requirements: repr(align) for cache-line optimization
   - Target features: conditional compilation for platform-specific SIMD

   **Reference:** [Portable SIMD Project](https://doc.rust-lang.org/stable/std/simd/index.html) (accessed 2025-10-26T03:52:00-04:00)

4. **Profiling Recommendations**
   - Suggest profiling tools: cargo-flamegraph, perf, Instruments
   - Benchmarking setup: criterion.rs integration
   - Hotspot identification: functions to prioritize for optimization

   **Reference:** [Criterion.rs](https://bheisler.github.io/criterion.rs/book/) (accessed 2025-10-26T03:52:00-04:00)

5. **Unsafe Code Review** (if `check_unsafe == true`)
   - Soundness verification: invariants documented and upheld
   - Undefined behavior patterns: dangling pointers, data races
   - Safe abstraction boundaries: public API cannot trigger UB
   - Alternative safe approaches: when unsafe is unnecessary

   **Reference:** [The Rustonomicon - Unsafe Rust](https://doc.rust-lang.org/nomicon/) (accessed 2025-10-26T03:52:00-04:00)

---

## Decision Rules

**Analysis Focus Routing:**
- `safety` → T1 only, skip concurrency/performance
- `concurrency` → T1 + T2 (ownership matters for Send/Sync)
- `performance` → T1 + T3 (safety issues affect optimization validity)
- `all` → T1 + T2 + T3 (comprehensive analysis)

**Abort Conditions:**
- `code_path` not readable → error "File/directory not accessible"
- No .rs files found → error "No Rust source files detected"
- Rust toolchain missing → error "Install rustc/cargo (rustup.rs)"
- Parse failure → return partial results with "syntax errors present" warning

**Severity Thresholds:**
- **Critical:** Undefined behavior, data races, memory unsafety
- **High:** Deadlock potential, resource leaks, significant perf issues
- **Medium:** Suboptimal patterns, unnecessary allocations
- **Low:** Style preferences, micro-optimizations

**Ambiguity Handling:**
- Lifetime inference failures: suggest explicit annotations
- Async vs sync unclear: recommend profiling before conversion
- Unsafe necessity unclear: propose safe alternative with caveats

---

## Output Contract

**Schema (JSON):**

```json
{
  "code_path": "string",
  "rust_edition": "2018 | 2021",
  "analysis_focus": "safety | concurrency | performance | all",
  "overall_score": "integer (0-100)",
  "safety_report": {
    "ownership_issues": [
      {
        "file": "string",
        "line": "integer",
        "severity": "critical | high | medium | low",
        "category": "move-after-use | borrow-conflict | lifetime",
        "message": "string",
        "fix": "string (optional)"
      }
    ],
    "unsafe_blocks": [
      {
        "file": "string",
        "line": "integer",
        "soundness_concern": "boolean",
        "rationale": "string",
        "safe_alternative": "string (optional)"
      }
    ]
  },
  "concurrency_analysis": {
    "deadlock_risks": ["array of objects with file/line/description"],
    "race_conditions": ["array of objects"],
    "async_issues": ["array of objects with tokio-specific patterns"],
    "sync_primitive_recommendations": ["array of strings"]
  },
  "performance_recommendations": {
    "allocations": ["array of hotspots with impact estimates"],
    "zero_copy_opportunities": ["array with refactoring suggestions"],
    "simd_candidates": ["array with vectorization potential"],
    "profiling_setup": "string (command to run)"
  },
  "ecosystem_suggestions": {
    "recommended_crates": ["array of crate names with use cases"],
    "clippy_config": "string (TOML snippet)",
    "rustfmt_config": "string (TOML snippet)"
  },
  "metrics": {
    "total_lines": "integer",
    "unsafe_line_count": "integer",
    "async_fn_count": "integer",
    "critical_issues": "integer",
    "high_issues": "integer",
    "medium_issues": "integer",
    "low_issues": "integer"
  },
  "timestamp": "ISO-8601 string (NOW_ET)"
}
```

**Required Fields:**
- `code_path`, `rust_edition`, `analysis_focus`, `overall_score`, `metrics`, `timestamp`
- At least one of: `safety_report`, `concurrency_analysis`, `performance_recommendations` (based on focus)

**Fix Suggestions:**
- Grouped by severity (critical first)
- Include code diff or refactoring instructions
- Reference Rust Book/docs.rs for learning resources
- Maximum 10 suggestions per category (prioritize highest impact)

---

## Examples

**Example: Async Rust Service with Concurrency Issues**

```rust
// INPUT: async service with tokio runtime inefficiencies
use tokio::sync::Mutex;
use std::sync::Arc;

async fn process_requests(db: Arc<Mutex<Database>>) {
    loop {
        let req = receive_request().await;

        // Issue 1: Holding lock across .await (blocking other tasks)
        let mut db = db.lock().await;
        db.update(req).await; // .await while holding Mutex

        // Issue 2: Blocking I/O in async context
        std::fs::read_to_string("config.txt").unwrap();

        // Issue 3: Spawning without bound (memory leak potential)
        tokio::spawn(async move {
            slow_operation().await;
        });
    }
}

// T2 ANALYSIS OUTPUT:
// Critical: Mutex held across .await (line 9-10)
//   Fix: Minimize critical section, release before async call
// High: Blocking std::fs in async fn (line 13)
//   Fix: Use tokio::fs::read_to_string
// High: Unbounded task spawning (line 16)
//   Fix: Use semaphore or bounded channel
```

---

## Quality Gates

**Token Budgets:**
- **T1:** ≤2k tokens (ownership/borrowing basics)
- **T2:** ≤6k tokens (async patterns + sync primitives)
- **T3:** ≤12k tokens (perf analysis + unsafe review + profiling)

**Safety:**
- No code execution beyond `cargo check --message-format=json`
- Sandbox filesystem access (read-only)
- Redact any secrets found in source comments

**Auditability:**
- Cite Rust edition for borrow checker behavior differences
- Log clippy version and lints enabled
- Include rustc version in output metadata
- Deterministic results (same code + edition → same findings)

**Performance:**
- T1 response: <3 seconds for single file ≤500 lines
- T2 response: <8 seconds for moderate async project
- T3 response: <20 seconds with full unsafe review
- Recommend splitting analysis for projects >50k LOC

**Accuracy:**
- All lifetime/borrow errors verified against `cargo check`
- Async issues tested against tokio documentation examples
- Performance claims backed by Rust Performance Book or benchmarks
- SIMD recommendations conditional on target architecture

---

## Resources

**Official Rust Documentation (accessed 2025-10-26T03:52:00-04:00):**
1. [The Rust Programming Language (Book)](https://doc.rust-lang.org/book/)
2. [The Rustonomicon (Unsafe Rust)](https://doc.rust-lang.org/nomicon/)
3. [Rust Reference](https://doc.rust-lang.org/reference/)
4. [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/)

**Async/Concurrency (accessed 2025-10-26T03:52:00-04:00):**
5. [Tokio Documentation](https://docs.rs/tokio/latest/tokio/)
6. [Tokio Tutorial](https://tokio.rs/tokio/tutorial)
7. [Async Book](https://rust-lang.github.io/async-book/)
8. [Rust Atomics and Locks](https://marabos.nl/atomics/)

**Performance (accessed 2025-10-26T03:52:00-04:00):**
9. [Rust Performance Book](https://nnethercote.github.io/perf-book/)
10. [Criterion.rs Benchmarking](https://bheisler.github.io/criterion.rs/book/)
11. [Portable SIMD](https://doc.rust-lang.org/stable/std/simd/)

**Tooling Integration:**
- `resources/clippy-config.toml` - Recommended clippy lints for each focus area
- `resources/rustfmt.toml` - Standard formatting configuration
- `resources/cargo-deny.toml` - Dependency security/license checking

**Crate Recommendations by Use Case:**
- Async runtime: tokio, async-std, smol
- Channels: flume, crossbeam-channel
- Serialization: serde, bincode, postcard (zero-copy)
- Profiling: pprof, tracing-subscriber, console
- SIMD: simdeez, packed_simd
