"""Tests for eval_runner module."""

from pathlib import Path

import pytest
import yaml

from cognitive_toolworks.testing import EvalResult, EvalRunner, EvalScenario


class TestEvalScenario:
    """Tests for EvalScenario dataclass."""

    def test_create_scenario(self) -> None:
        """Test creating a basic scenario."""
        scenario = EvalScenario(
            id="test-001",
            name="Test Scenario",
            description="A test scenario",
            inputs={"param1": "value1"},
            expected_outputs={"result": "expected"},
            success_criteria=["Criterion 1", "Criterion 2"],
            tier="T1",
        )

        assert scenario.id == "test-001"
        assert scenario.name == "Test Scenario"
        assert scenario.description == "A test scenario"
        assert scenario.inputs == {"param1": "value1"}
        assert scenario.expected_outputs == {"result": "expected"}
        assert scenario.success_criteria == ["Criterion 1", "Criterion 2"]
        assert scenario.tier == "T1"

    def test_scenario_without_tier(self) -> None:
        """Test scenario with no tier specified."""
        scenario = EvalScenario(
            id="test-002",
            name="No Tier",
            description="Test without tier",
            inputs={},
            expected_outputs={},
            success_criteria=["Check something"],
        )

        assert scenario.tier is None


class TestEvalResult:
    """Tests for EvalResult dataclass."""

    def test_create_result_passed(self) -> None:
        """Test creating a passing result."""
        result = EvalResult(
            scenario_id="test-001",
            passed=True,
            actual_output={"status": "success"},
            errors=[],
            criteria_results=[("Criterion 1", True), ("Criterion 2", True)],
        )

        assert result.scenario_id == "test-001"
        assert result.passed is True
        assert result.actual_output == {"status": "success"}
        assert result.errors == []
        assert len(result.criteria_results) == 2

    def test_create_result_failed(self) -> None:
        """Test creating a failing result."""
        result = EvalResult(
            scenario_id="test-002",
            passed=False,
            actual_output=None,
            errors=["Error 1", "Error 2"],
            criteria_results=[("Criterion 1", False)],
        )

        assert result.scenario_id == "test-002"
        assert result.passed is False
        assert result.actual_output is None
        assert result.errors == ["Error 1", "Error 2"]


class TestEvalRunner:
    """Tests for EvalRunner class."""

    @pytest.fixture
    def runner(self) -> EvalRunner:
        """Create an EvalRunner instance."""
        return EvalRunner()

    @pytest.fixture
    def valid_yaml_file(self, tmp_path: Path) -> Path:
        """Create a valid eval YAML file."""
        yaml_content = {
            "skill": "test-skill",
            "version": "1.0.0",
            "scenarios": [
                {
                    "id": "eval-001",
                    "name": "Test Scenario 1",
                    "description": "First test scenario",
                    "inputs": {"param1": "value1", "param2": 42},
                    "expected_outputs": {"status": "success", "result": "expected"},
                    "success_criteria": ["Criterion 1", "Criterion 2"],
                    "tier": "T1",
                },
                {
                    "id": "eval-002",
                    "name": "Test Scenario 2",
                    "description": "Second test scenario",
                    "inputs": {"different": "input"},
                    "expected_outputs": {"output": "value"},
                    "success_criteria": ["Single criterion"],
                    "tier": "T2",
                },
            ],
        }

        yaml_file = tmp_path / "test_evals.yaml"
        with yaml_file.open("w") as f:
            yaml.dump(yaml_content, f)

        return yaml_file

    @pytest.fixture
    def old_format_yaml_file(self, tmp_path: Path) -> Path:
        """Create an old format eval YAML file (scenarios at top level)."""
        yaml_content = {
            "scenarios": [
                {
                    "name": "Old Format Scenario",
                    "description": "Test old format",
                    "input": {"old": "format"},
                    "expected_outputs": {},
                    "success_criteria": ["Works"],
                    "token_tier": "T1",
                }
            ]
        }

        yaml_file = tmp_path / "old_format.yaml"
        with yaml_file.open("w") as f:
            yaml.dump(yaml_content, f)

        return yaml_file

    def test_load_scenarios_valid_file(self, runner: EvalRunner, valid_yaml_file: Path) -> None:
        """Test loading scenarios from a valid YAML file."""
        scenarios = runner.load_scenarios(valid_yaml_file)

        assert len(scenarios) == 2

        # Check first scenario
        assert scenarios[0].id == "eval-001"
        assert scenarios[0].name == "Test Scenario 1"
        assert scenarios[0].description == "First test scenario"
        assert scenarios[0].inputs == {"param1": "value1", "param2": 42}
        assert scenarios[0].expected_outputs == {"status": "success", "result": "expected"}
        assert scenarios[0].success_criteria == ["Criterion 1", "Criterion 2"]
        assert scenarios[0].tier == "T1"

        # Check second scenario
        assert scenarios[1].id == "eval-002"
        assert scenarios[1].tier == "T2"

    def test_load_scenarios_old_format(
        self, runner: EvalRunner, old_format_yaml_file: Path
    ) -> None:
        """Test loading scenarios from old format YAML."""
        scenarios = runner.load_scenarios(old_format_yaml_file)

        assert len(scenarios) == 1
        assert scenarios[0].name == "Old Format Scenario"
        assert scenarios[0].inputs == {"old": "format"}  # 'input' mapped to 'inputs'
        assert scenarios[0].tier == "T1"  # 'token_tier' mapped to 'tier'

    def test_load_scenarios_missing_file(self, runner: EvalRunner, tmp_path: Path) -> None:
        """Test loading from non-existent file."""
        missing_file = tmp_path / "missing.yaml"

        with pytest.raises(FileNotFoundError, match="Eval file not found"):
            runner.load_scenarios(missing_file)

    def test_load_scenarios_empty_file(self, runner: EvalRunner, tmp_path: Path) -> None:
        """Test loading from empty YAML file."""
        empty_file = tmp_path / "empty.yaml"
        empty_file.write_text("")

        with pytest.raises(ValueError, match="Empty YAML file"):
            runner.load_scenarios(empty_file)

    def test_load_scenarios_malformed_yaml(self, runner: EvalRunner, tmp_path: Path) -> None:
        """Test loading from malformed YAML file."""
        bad_yaml = tmp_path / "bad.yaml"
        bad_yaml.write_text("{ invalid yaml content: [}")

        with pytest.raises(yaml.YAMLError):
            runner.load_scenarios(bad_yaml)

    def test_load_scenarios_missing_required_fields(
        self, runner: EvalRunner, tmp_path: Path
    ) -> None:
        """Test loading scenarios missing required fields."""
        yaml_content = {
            "scenarios": [
                {
                    "id": "bad-001",
                    # Missing 'name' and 'description'
                    "inputs": {},
                }
            ]
        }

        yaml_file = tmp_path / "missing_fields.yaml"
        with yaml_file.open("w") as f:
            yaml.dump(yaml_content, f)

        with pytest.raises(ValueError, match="missing required fields"):
            runner.load_scenarios(yaml_file)

    def test_load_scenarios_auto_generated_ids(self, runner: EvalRunner, tmp_path: Path) -> None:
        """Test scenarios without explicit IDs get auto-generated IDs."""
        yaml_content = {
            "scenarios": [
                {"name": "Scenario 1", "description": "Test 1"},
                {"name": "Scenario 2", "description": "Test 2"},
            ]
        }

        yaml_file = tmp_path / "no_ids.yaml"
        with yaml_file.open("w") as f:
            yaml.dump(yaml_content, f)

        scenarios = runner.load_scenarios(yaml_file)

        assert scenarios[0].id == "scenario-1"
        assert scenarios[1].id == "scenario-2"

    def test_run_scenario_valid(self, runner: EvalRunner) -> None:
        """Test running a valid scenario."""
        scenario = EvalScenario(
            id="test-001",
            name="Valid Test",
            description="A valid test scenario",
            inputs={"key": "value"},
            expected_outputs={"result": "expected"},
            success_criteria=["Check 1", "Check 2"],
            tier="T1",
        )

        result = runner.run_scenario(scenario)

        assert result.scenario_id == "test-001"
        assert result.passed is True
        assert result.errors == []
        assert len(result.criteria_results) == 2
        assert all(passed for _, passed in result.criteria_results)

    def test_run_scenario_invalid_inputs(self, runner: EvalRunner) -> None:
        """Test running scenario with invalid inputs type."""
        scenario = EvalScenario(
            id="test-002",
            name="Bad Inputs",
            description="Scenario with invalid inputs",
            inputs="not a dict",  # type: ignore
            expected_outputs={},
            success_criteria=["Check"],
        )

        result = runner.run_scenario(scenario)

        assert result.scenario_id == "test-002"
        assert result.passed is False
        assert any("Inputs must be dict" in err for err in result.errors)

    def test_run_scenario_invalid_expected_outputs(self, runner: EvalRunner) -> None:
        """Test running scenario with invalid expected_outputs type."""
        scenario = EvalScenario(
            id="test-003",
            name="Bad Outputs",
            description="Scenario with invalid outputs",
            inputs={},
            expected_outputs="not a dict",  # type: ignore
            success_criteria=["Check"],
        )

        result = runner.run_scenario(scenario)

        assert result.passed is False
        assert any("Expected outputs must be dict" in err for err in result.errors)

    def test_run_scenario_empty_criteria(self, runner: EvalRunner) -> None:
        """Test running scenario with empty success criteria."""
        scenario = EvalScenario(
            id="test-004",
            name="No Criteria",
            description="Scenario with no criteria",
            inputs={},
            expected_outputs={},
            success_criteria=[],
        )

        result = runner.run_scenario(scenario)

        assert result.passed is False
        assert any("Success criteria cannot be empty" in err for err in result.errors)

    def test_run_scenario_invalid_criteria(self, runner: EvalRunner) -> None:
        """Test running scenario with invalid criteria."""
        scenario = EvalScenario(
            id="test-005",
            name="Bad Criteria",
            description="Scenario with invalid criteria",
            inputs={},
            expected_outputs={},
            success_criteria=["Valid", "", "   ", 123],  # type: ignore
        )

        result = runner.run_scenario(scenario)

        assert result.passed is False
        assert len([c for c, p in result.criteria_results if not p]) > 0

    def test_run_scenario_invalid_tier(self, runner: EvalRunner) -> None:
        """Test running scenario with invalid tier format."""
        scenario = EvalScenario(
            id="test-006",
            name="Bad Tier",
            description="Scenario with invalid tier",
            inputs={},
            expected_outputs={},
            success_criteria=["Check"],
            tier="T4",  # Invalid: should be T1, T2, or T3
        )

        result = runner.run_scenario(scenario)

        assert result.passed is False
        assert any("Invalid tier format" in err for err in result.errors)

    def test_run_all_scenarios(self, runner: EvalRunner, valid_yaml_file: Path) -> None:
        """Test running all scenarios from a file."""
        results = runner.run_all(valid_yaml_file)

        assert len(results) == 2
        assert all(r.passed for r in results)
        assert results[0].scenario_id == "eval-001"
        assert results[1].scenario_id == "eval-002"

    def test_check_criteria_valid_output(self, runner: EvalRunner) -> None:
        """Test checking criteria against valid output."""
        output = {"status": "success", "value": 42}
        criteria = ["Check 1", "Check 2"]

        results = runner.check_criteria(output, criteria)

        assert len(results) == 2
        assert all(passed for _, passed in results)

    def test_check_criteria_invalid_output(self, runner: EvalRunner) -> None:
        """Test checking criteria against non-dict output."""
        output = "not a dict"
        criteria = ["Check 1"]

        results = runner.check_criteria(output, criteria)  # type: ignore[arg-type]

        assert len(results) == 1
        assert not results[0][1]  # Should fail

    def test_check_criteria_empty_criterion(self, runner: EvalRunner) -> None:
        """Test checking empty/invalid criteria."""
        output = {"valid": "output"}
        criteria = ["Valid", "", "   "]

        results = runner.check_criteria(output, criteria)

        assert len(results) == 3
        assert results[0][1] is True  # Valid criterion
        assert results[1][1] is False  # Empty string
        assert results[2][1] is False  # Whitespace only

    def test_integration_real_eval_file(self, runner: EvalRunner) -> None:
        """Test with an actual eval file from the project (if it exists)."""
        project_root = Path(__file__).parent.parent.parent
        eval_file = project_root / "tests" / "evals_cloud-edge-architect.yaml"

        if not eval_file.exists():
            pytest.skip("Actual eval file not found")

        scenarios = runner.load_scenarios(eval_file)
        assert len(scenarios) > 0

        # Run scenarios and check structure
        results = runner.run_all(eval_file)
        assert len(results) == len(scenarios)

        # All should pass structural validation
        for result in results:
            if not result.passed:
                print(f"Failed: {result.scenario_id}")
                print(f"Errors: {result.errors}")

        assert all(r.passed for r in results), "Some scenarios failed structural validation"
