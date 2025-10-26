---
name: "Content & Documentation Generator"
slug: "documentation-content-generator"
description: "Generate technical documentation, API docs, and content with accessibility and SEO optimization."
capabilities:
  - Generate Markdown/MDX documentation from templates
  - Create API documentation from OpenAPI specifications
  - Apply technical writing best practices (clarity, structure, readability)
  - Optimize for accessibility (WCAG 2.2 compliance)
  - Generate documentation site structures
inputs:
  - content_type: "technical-doc | api-doc | user-guide | tutorial (string)"
  - source: "code path, OpenAPI spec, or content brief (string)"
  - output_format: "markdown | mdx | html (string, default: markdown)"
  - style_guide: "microsoft | google | write-the-docs (string, default: write-the-docs)"
outputs:
  - documentation: "Generated documentation in specified format (string)"
  - metadata: "SEO metadata and frontmatter (object)"
  - accessibility_score: "WCAG compliance rating 0-100 (integer)"
keywords:
  - documentation
  - technical-writing
  - api-docs
  - markdown
  - accessibility
  - content-generation
version: "1.0.0"
owner: "cognitive-toolworks"
license: "MIT"
security: "Public; no secrets or PII; safe for open repositories"
links:
  - https://www.writethedocs.org/guide/
  - https://docusaurus.io/docs
  - https://www.mkdocs.org/
  - https://developers.google.com/tech-writing
  - https://www.w3.org/WAI/WCAG22/quickref/
---

## Purpose & When-To-Use

**Trigger conditions:**
- New feature requires documentation
- API endpoint needs OpenAPI-driven documentation
- User guide or tutorial creation needed
- Documentation refresh for clarity and accessibility
- Knowledge base article generation
- Migration from wiki/docs to structured documentation site

**Not for:**
- Marketing copy or sales materials
- Legal documents or contracts
- Research papers or academic writing
- Long-form narrative content

---

## Pre-Checks

**Time normalization:**
- Compute `NOW_ET` using NIST/time.gov semantics (America/New_York, ISO-8601)
- Use `NOW_ET` for all citation access dates

**Input validation:**
- `content_type` must be one of: technical-doc, api-doc, user-guide, tutorial
- `source` must be valid (file exists, spec parseable, or non-empty string)
- `output_format` must be: markdown, mdx, or html
- `style_guide` must be: microsoft, google, or write-the-docs

**Source freshness:**
- For API docs: verify OpenAPI spec version (3.0.x or 3.1.x supported)
- Style guide references accessible and current

---

## Procedure

### T1: Standard Documentation Generation (≤2k tokens)

**Fast path for 80% of documentation needs:**

1. **Content Analysis**
   - Detect content type from source or use provided `content_type`
   - Identify key sections needed (overview, quickstart, reference, examples)

2. **Template Selection** ([Write the Docs Structure Guide](https://www.writethedocs.org/guide/writing/beginners-guide-to-docs/), accessed 2025-10-25T21:30:36-04:00)
   - **Technical Doc:** Title, Purpose, Prerequisites, Steps, Troubleshooting, Next Steps
   - **API Doc:** Endpoint description, Request/Response schemas, Examples, Error codes
   - **User Guide:** Introduction, Task-based sections, Screenshots/diagrams, FAQs
   - **Tutorial:** Learning objectives, Step-by-step instructions, Code samples, Validation

3. **Content Generation Principles** ([Google Technical Writing Guide](https://developers.google.com/tech-writing/overview), accessed 2025-10-25T21:30:36-04:00)
   - Use active voice and present tense
   - Keep sentences ≤25 words
   - Use concrete examples over abstract concepts
   - Front-load important information
   - Use bulleted lists for 3+ items
   - Add code blocks with language identifiers

4. **Accessibility Checks** ([WCAG 2.2 Level AA](https://www.w3.org/WAI/WCAG22/quickref/), accessed 2025-10-25T21:30:36-04:00)
   - Headings in logical hierarchy (H1 → H2 → H3)
   - Descriptive link text (no "click here")
   - Alt text for images
   - Color contrast sufficient (4.5:1 for text)
   - No flashing content

5. **Metadata Generation**
   - Generate frontmatter: title, description (≤160 chars), keywords, date
   - Create navigation breadcrumbs if part of doc site

**Output:** Markdown/MDX document with frontmatter and accessibility-compliant structure.

**Decision:** If `content_type == "api-doc"` and OpenAPI spec provided → proceed to T2 for enhanced API documentation. Otherwise STOP at T1.

---

### T2: API Documentation Enhancement (≤6k tokens)

**Extended API documentation from OpenAPI specifications:**

1. **OpenAPI Parsing**
   - Parse OpenAPI 3.0.x or 3.1.x specification
   - Extract endpoints, schemas, security schemes
   - Validate spec completeness (descriptions, examples present)

2. **Enhanced Documentation Sections** ([Docusaurus OpenAPI Docs](https://docusaurus.io/docs/api/plugins/@docusaurus/plugin-content-docs), accessed 2025-10-25T21:30:36-04:00)
   - **Overview:** API purpose, base URL, authentication methods
   - **Authentication:** Security scheme details with examples
   - **Endpoints by Resource:** Group by tags, show HTTP methods
   - **Request Details:** Parameters (path/query/header/body), schemas, constraints
   - **Response Details:** Status codes, response schemas, examples
   - **Error Handling:** Common error codes and resolution steps
   - **Rate Limiting:** If defined in spec

3. **Code Sample Generation**
   - Generate request examples in 2-3 languages (curl, JavaScript, Python)
   - Include authentication headers
   - Use realistic sample data from OpenAPI examples

4. **Interactive Features** (for MDX output)
   - Try-it-out component metadata
   - Collapsible schema sections
   - Tabbed code examples

**Output:** Comprehensive API documentation with code samples and interactive elements.

---

### T3: Documentation Site Generation (not implemented in v1.0.0)

Reserved for:
- Full documentation site scaffolding (Docusaurus/MkDocs)
- Multi-version documentation management
- Search indexing and algolia integration
- Documentation analytics and feedback collection

---

## Decision Rules

**Content Type Detection:**
- If source contains `openapi` or `swagger` key → api-doc
- If source is directory with code files → technical-doc
- If source is plain text brief → user-guide or tutorial (ask user if ambiguous)

**Abort Conditions:**
- OpenAPI spec invalid or unparseable → error "Invalid OpenAPI specification"
- Source file not found → error "Source file not accessible"
- Unsupported OpenAPI version → error "Only OpenAPI 3.0.x and 3.1.x supported"

**Accessibility Threshold:**
- Score ≥90 → "Excellent accessibility"
- Score 70-89 → "Good accessibility, minor improvements suggested"
- Score <70 → Include remediation recommendations in output

**Style Guide Conflicts:**
- When style guides conflict, prefer: write-the-docs > google > microsoft
- Document style guide choice in frontmatter

---

## Output Contract

**Required fields:**

```yaml
documentation:
  type: string
  description: "Generated documentation content in requested format"
  format: "markdown | mdx | html"

metadata:
  type: object
  required: [title, description, keywords, generated_at]
  properties:
    title:
      type: string
      maxLength: 60
    description:
      type: string
      maxLength: 160
    keywords:
      type: array
      items: {type: string}
      maxItems: 10
    generated_at:
      type: string
      format: date-time
    style_guide:
      type: string
      enum: [microsoft, google, write-the-docs]

accessibility_score:
  type: integer
  minimum: 0
  maximum: 100
  description: "WCAG 2.2 Level AA compliance rating"

issues:
  type: array
  description: "Accessibility or style issues found (optional)"
  items:
    type: object
    properties:
      severity: {type: string, enum: [error, warning, info]}
      message: {type: string}
      line: {type: integer}
```

---

## Examples

**Input:**
```yaml
content_type: "api-doc"
source: "openapi-spec.yaml"
output_format: "markdown"
style_guide: "write-the-docs"
```

**Output (abbreviated):**
```markdown
---
title: "User Management API"
description: "REST API for user authentication and profile management"
keywords: [api, users, authentication, rest]
generated_at: "2025-10-25T21:30:36-04:00"
style_guide: "write-the-docs"
---

# User Management API

Manage user accounts and authentication.

## Authentication
Bearer token required. Include in `Authorization` header.

## Endpoints

### POST /users/register
Create new user account.

**Request:**
```json
{"email": "user@example.com", "password": "***"}
```

**Response (201):**
```json
{"id": "usr_123", "email": "user@example.com"}
```
```

---

## Quality Gates

**Token budgets (mandatory):**
- **T1 ≤ 2k tokens** — Standard doc generation (technical-doc, user-guide, tutorial)
- **T2 ≤ 6k tokens** — API documentation with OpenAPI parsing and code samples
- **T3 ≤ 12k tokens** — (Not implemented) Full site generation

**Safety:**
- No secrets in documentation examples
- Sanitize user-provided content
- No executable code in examples (documentation only)

**Auditability:**
- All style guide references cite specific sections with access dates
- Template choices logged in metadata
- Accessibility issues enumerated with severity

**Determinism:**
- Same input + style guide → same output structure
- Variation acceptable in generated examples (realistic data)

---

## Resources

**Style Guides:**
- [Write the Docs Guide](https://www.writethedocs.org/guide/) — Community best practices
- [Google Technical Writing Courses](https://developers.google.com/tech-writing) — Free courses on clarity
- [Microsoft Writing Style Guide](https://learn.microsoft.com/en-us/style-guide/welcome/) — Enterprise style guide

**Documentation Tools:**
- [Docusaurus](https://docusaurus.io/docs) — React-based doc site generator
- [MkDocs](https://www.mkdocs.org/) — Python-based static site generator
- [MkDocs Material](https://squidfunk.github.io/mkdocs-material/) — Material Design theme for MkDocs

**Accessibility:**
- [WCAG 2.2 Quick Reference](https://www.w3.org/WAI/WCAG22/quickref/) — Official guidelines
- [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) — Color contrast validation

**OpenAPI:**
- [OpenAPI Specification](https://spec.openapis.org/oas/latest.html) — Official spec
- [Swagger Editor](https://editor.swagger.io/) — Online OpenAPI editor

**Templates:**
- See `resources/templates/` for reusable Markdown templates
- See `resources/schemas/` for JSON schemas
