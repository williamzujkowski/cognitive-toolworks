---
name: OSCAL SSP Validator
slug: oscal-ssp-validate
description: Validates OSCAL System Security Plan documents against schemas, profiles, and cross-reference requirements with tiered validation depth.
capabilities:
  - Schema validation (JSON/XML/YAML)
  - Profile alignment verification
  - Cross-reference integrity checks
  - Constraint validation
  - Multi-format support
inputs:
  - ssp_path: file path or URL to OSCAL SSP document
  - profile: optional profile identifier for alignment checks
  - strict: boolean flag for strict validation mode (default false)
outputs:
  - report: structured JSON validation report
  - summary: markdown-formatted validation summary
keywords:
  - oscal
  - ssp
  - validation
  - schema
  - profile
  - compliance
  - security
version: 1.0.0
owner: cognitive-toolworks
license: CC0-1.0
security: public; no secrets or PII
links:
  - https://pages.nist.gov/OSCAL/learn/concepts/layer/implementation/ssp/
  - https://pages.nist.gov/OSCAL/learn/concepts/validation/
  - https://github.com/usnistgov/OSCAL
---

## Purpose & When-To-Use

**Trigger conditions:**

* You have an OSCAL System Security Plan (SSP) document in JSON, XML, or YAML format
* You need to verify schema compliance and structural validity
* You want to check profile alignment for control implementation
* You require cross-reference integrity validation for components and controls
* You need varying depth of validation (quick schema check vs. comprehensive audit)

**Use this skill when:**

* Integrating SSP documents into automated compliance pipelines
* Preparing SSP submissions for FedRAMP or other compliance frameworks
* Debugging SSP authoring or generation tools
* Conducting quality assurance on SSP documents before review

## Pre-Checks

**Time normalization:**
```
NOW_ET = <NIST time.gov semantics, America/New_York, ISO-8601>
Example: 2025-10-25T21:04:34-04:00
```

**Input validation:**

* `ssp_path` must resolve to accessible file or reachable URL
* If file: check read permissions and non-zero size
* If URL: verify HTTPS and reachability (HEAD request)
* Document format must be detectable (`.json`, `.xml`, `.yaml`/`.yml` extension or MIME type)
* If `profile` specified: must be valid OSCAL profile identifier or resolvable path/URL
* `strict` must be boolean (default: `false`)

**Schema freshness check:**

* Verify OSCAL schema version in document metadata
* Current reference version: v1.1.2 (accessed 2025-10-25T21:04:34-04:00)
* Warn if schema version > 1.1.2 or < 1.0.0
* Schemas available at: https://github.com/usnistgov/OSCAL/tree/main/json/schema

## Procedure

### Tier 1: Fast Schema Validation (≤2k tokens)

**Goal:** Confirm well-formedness and basic schema compliance

**Steps:**

1. **Load document**
   * Parse based on detected format (JSON/XML/YAML)
   * Catch syntax errors; abort if malformed

2. **Extract metadata**
   * Read `metadata/version` and `metadata/oscal-version`
   * Identify document as SSP model type

3. **Schema validation**
   * Fetch appropriate schema for OSCAL version + format
   * Apply schema validator (JSON Schema for JSON/YAML, XSD for XML)
   * Collect validation errors/warnings

4. **Output quick report**
   * Status: `valid`, `invalid`, or `error`
   * Error count and first 3 errors
   * Schema version used

**Stop condition:** If document is malformed or has >10 schema errors, abort and report.

### Tier 2: Profile Alignment + Citations (≤6k tokens)

**Goal:** Verify profile compliance and control implementation integrity

**Steps (extends T1):**

5. **Profile resolution** (if `profile` provided)
   * Load or resolve profile document
   * Extract required controls and parameters
   * Compare against SSP `control-implementation` section

6. **Control coverage check**
   * List all controls referenced in profile
   * Verify each control has implementation statement in SSP
   * Flag missing or incomplete implementations

7. **Parameter validation**
   * Check parameter values against profile constraints
   * Verify required parameters are set
   * Validate data types and allowed values

8. **Citation and source references**
   * NIST OSCAL SSP Model v1.1.2 (accessed 2025-10-25T21:04:34-04:00): https://pages.nist.gov/OSCAL-Reference/models/v1.1.2/system-security-plan/xml-reference/
   * OSCAL Validation Concepts (accessed 2025-10-25T21:04:34-04:00): https://pages.nist.gov/OSCAL/learn/concepts/validation/
   * OSCAL Layers of Validation - FedRAMP (accessed 2025-10-25T21:04:34-04:00): https://automate.fedramp.gov/documentation/general-concepts/oscal-layers-of-validation/
   * NIST OSCAL GitHub Repository (accessed 2025-10-25T21:04:34-04:00): https://github.com/usnistgov/OSCAL

**Output enhanced report:**
* Profile alignment score (% controls implemented)
* Parameter validation results
* Control gap list

### Tier 3: Deep Cross-Reference & Rationale (≤12k tokens)

**Goal:** Comprehensive integrity validation with detailed rationale

**Steps (extends T2):**

9. **Component cross-reference validation**
   * Extract all `component-definition` UUIDs
   * Verify all referenced components exist
   * Check for orphaned components (defined but not used)
   * Validate component-to-control mappings

10. **Link integrity**
    * Validate all `link/@href` references
    * Check internal UUID references (back-matter, responsible-parties)
    * Verify external URLs are reachable (if strict mode)

11. **Metadata consistency**
    * Check `last-modified` vs. `published` dates
    * Verify party/role/location UUID references
    * Validate responsible-party assignments

12. **Generate rationale**
    * For each validation failure: explain constraint and fix suggestion
    * Cite relevant OSCAL specification sections
    * Provide example corrections

## Decision Rules

* **Abort threshold:** >50 schema errors in T1 → stop, document is fundamentally broken
* **Profile mismatch severity:**
  * `strict=false`: warn on missing controls
  * `strict=true`: fail on any control gap
* **Cross-reference tolerance:**
  * Missing internal UUIDs: always fail
  * Unreachable external URLs: warn unless `strict=true`
* **Tier escalation:**
  * T1 sufficient for schema-only validation
  * T2 required if profile specified or control implementation needed
  * T3 required for comprehensive audit or strict mode

## Output Contract

**JSON Report Schema:**

```json
{
  "validation_timestamp": "ISO-8601 timestamp",
  "ssp_path": "string",
  "oscal_version": "string",
  "tier": "1|2|3",
  "status": "valid|invalid|error",
  "summary": {
    "total_errors": "integer",
    "total_warnings": "integer",
    "schema_valid": "boolean",
    "profile_aligned": "boolean|null",
    "cross_refs_valid": "boolean|null"
  },
  "errors": [
    {
      "type": "schema|profile|cross-ref|metadata",
      "severity": "error|warning",
      "location": "JSONPath or XPath",
      "message": "string",
      "suggestion": "string|null"
    }
  ],
  "profile_report": {
    "controls_required": "integer",
    "controls_implemented": "integer",
    "coverage_percent": "float",
    "missing_controls": ["string"]
  },
  "sources": ["array of citation URLs with access dates"]
}
```

**Markdown Summary Format:**

```markdown
# OSCAL SSP Validation Report

**Document:** `{ssp_path}`
**Timestamp:** {validation_timestamp}
**OSCAL Version:** {oscal_version}
**Status:** {status}

## Summary
- Errors: {total_errors}
- Warnings: {total_warnings}
- Schema Valid: {schema_valid}
- Profile Aligned: {profile_aligned}

## Details
{top 5 errors with suggestions}

## Sources
{clickable links with access dates}
```

## Examples

**Example 1: T1 validation of valid SSP**

```bash
# Input
ssp_path: "./my-ssp.json"
profile: null
strict: false

# Execution
1. Parse my-ssp.json → success
2. Extract metadata/oscal-version → "1.1.2"
3. Fetch JSON schema v1.1.2
4. Validate → 0 errors

# Output (JSON)
{
  "validation_timestamp": "2025-10-25T21:04:34-04:00",
  "ssp_path": "./my-ssp.json",
  "oscal_version": "1.1.2",
  "tier": "1",
  "status": "valid",
  "summary": {
    "total_errors": 0,
    "total_warnings": 0,
    "schema_valid": true
  },
  "errors": []
}
```

## Quality Gates

**Token budgets (mandatory):**

* T1: ≤2,000 tokens (schema validation only)
* T2: ≤6,000 tokens (+ profile checks + 2-4 cited sources)
* T3: ≤12,000 tokens (+ cross-refs + rationale + examples)

**Safety:**

* No credential exposure in validation reports
* Sanitize file paths in error messages (remove sensitive directory names)
* Do not persist validation reports with PII/secrets

**Auditability:**

* All validation runs must log: timestamp, tier, status, error count
* Citation access dates must equal NOW_ET
* Schema version must be recorded in output

**Determinism:**

* Same SSP + profile + tier → identical validation result
* Schema fetch must use version-pinned URLs
* No random sampling or probabilistic checks

## Resources

**Official NIST OSCAL Documentation:**

* System Security Plan Model Reference: https://pages.nist.gov/OSCAL/learn/concepts/layer/implementation/ssp/
* OSCAL Validation Concepts: https://pages.nist.gov/OSCAL/learn/concepts/validation/
* OSCAL v1.1.2 SSP XML Reference: https://pages.nist.gov/OSCAL-Reference/models/v1.1.2/system-security-plan/xml-reference/
* OSCAL GitHub Repository: https://github.com/usnistgov/OSCAL

**Schemas:**

* JSON Schema: https://github.com/usnistgov/OSCAL/tree/main/json/schema
* XML Schema: https://github.com/usnistgov/OSCAL/tree/main/xml/schema

**Tools:**

* OSCAL CLI (NIST): https://pages.nist.gov/OSCAL/resources/tools/
* FedRAMP OSCAL Layers of Validation: https://automate.fedramp.gov/documentation/general-concepts/oscal-layers-of-validation/

**Profile Resolution Specification:**

* https://pages.nist.gov/OSCAL/concepts/processing/profile-resolution/
