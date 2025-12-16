# Integration Tests

End-to-end integration tests for complete workflows in cognitive-toolworks.

## Overview

Integration tests verify complete workflows across multiple modules:

1. **MCP Workflow** (`test_mcp_workflow.py`): Tests MCP introspection → analysis → generation
2. **Validation Workflow** (`test_validation_workflow.py`): Tests validation → auto-fix → re-validation

## Running Integration Tests

```bash
# Run all integration tests
pytest tests/integration/ -v -m integration

# Run specific workflow tests
pytest tests/integration/test_mcp_workflow.py -v -m integration
pytest tests/integration/test_validation_workflow.py -v -m integration

# Exclude integration tests from regular test runs
pytest tests/ -m "not integration"
```

## Test Structure

### MCP Workflow Tests (6 tests)

- `test_mcp_config_loading`: Load MCP configuration from JSON
- `test_mcp_introspection_mock`: Mock MCP server introspection
- `test_token_analysis_of_mcp_tools`: Analyze token usage of MCP tools
- `test_skill_generation_from_mcp_mock`: Test skill generator configuration
- `test_complete_mcp_to_validated_skill_workflow`: **Complete pipeline test**
- `test_token_budget_compliance`: Verify token budgets are met

### Validation Workflow Tests (12 tests)

- `test_detect_invalid_skill_issues`: Detect issues in invalid skills
- `test_validate_valid_skill`: Validate properly formatted skills
- `test_auto_fix_suggestions`: Verify fix suggestions are provided
- `test_validation_roundtrip_with_fixes`: **Complete roundtrip test**
- `test_aaif_validation_workflow`: Test AAIF validator
- `test_multiple_validator_workflow`: Run multiple validators
- `test_validation_metadata_extraction`: Extract and validate metadata
- `test_severity_levels`: Verify severity classification
- `test_real_skill_validation`: Validate real skills from repository
- `test_validation_performance`: Ensure validation completes quickly
- `test_validation_error_messages_quality`: Verify error message quality
- `test_batch_validation`: Test validating multiple skills

## Test Fixtures

Located in `fixtures/`:

- `sample_mcp_config.json`: Sample MCP server configuration
- `invalid_skill.md`: Intentionally invalid skill for validation testing

## Key Integration Points

### MCP Workflow
```
MCPIntrospector → MCPAnalysis → TokenAnalyzer → SkillGenerator → AnthropicValidator
```

### Validation Workflow
```
Load SKILL.md → Validator.validate_file() → Get issues → Apply fixes → Re-validate
```

## CI/CD Integration

Integration tests are marked with `@pytest.mark.integration` and can be:

- Included in CI: `pytest -m integration`
- Excluded from fast CI: `pytest -m "not integration"`

## Notes

- Integration tests use mocking where possible to avoid external dependencies
- Some tests verify structure without requiring actual LLM API calls
- All tests should complete in < 2 seconds total
- 18 total integration tests covering complete workflows
