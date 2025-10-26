# Changelog - rust-analyzer

All notable changes to the Rust Safety & Performance Analyzer skill will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

## [1.0.0] - 2025-10-26

### Added
- Initial skill implementation with T1/T2/T3 tiers
- Memory safety analysis (ownership, borrowing, lifetimes)
- Concurrency pattern validation (Arc/Mutex, channels, async/await)
- Performance optimization detection (allocations, zero-copy, SIMD)
- Unsafe code soundness review
- Tokio runtime efficiency analysis
- Ecosystem tooling integration (clippy config, rustfmt)
- 5 evaluation scenarios covering safety, concurrency, performance
- Example: async service with Mutex-held-across-await issue
- Resource files: clippy-config.toml
- Citations from Rust Book, Tokio docs, Performance Book, Rustonomicon

### Documentation
- Complete SKILL.md with 8 required sections
- Token budgets: T1 ≤2k, T2 ≤6k, T3 ≤12k
- Comprehensive output schema (JSON)
- Decision rules for analysis routing
- Quality gates and accuracy requirements
