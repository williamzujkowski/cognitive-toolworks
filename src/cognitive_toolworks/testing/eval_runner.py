"""Evaluation runner for cognitive-toolworks skills.

Executes YAML-based evaluation scenarios and validates skill outputs
against expected criteria.
"""

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml


@dataclass
class EvalScenario:
    """A single evaluation scenario from YAML.

    Attributes:
        id: Unique scenario identifier (e.g., "eval-001")
        name: Human-readable scenario name
        description: What this scenario tests
        inputs: Input parameters to pass to the skill
        expected_outputs: Expected output structure/values
        success_criteria: List of conditions that must be met
        tier: Token tier (T1/T2/T3) or None
    """

    id: str
    name: str
    description: str
    inputs: dict[str, Any]
    expected_outputs: dict[str, Any]
    success_criteria: list[str]
    tier: str | None = None


@dataclass
class EvalResult:
    """Result of running a single evaluation scenario.

    Attributes:
        scenario_id: ID of the scenario that was run
        passed: Whether all success criteria were met
        actual_output: The actual output from the skill (if any)
        errors: List of error messages (empty if passed)
        criteria_results: Per-criterion results [(criterion, passed), ...]
    """

    scenario_id: str
    passed: bool
    actual_output: dict[str, Any] | None = None
    errors: list[str] = field(default_factory=list)
    criteria_results: list[tuple[str, bool]] = field(default_factory=list)


class EvalRunner:
    """Runs evaluation scenarios from YAML files.

    This runner loads YAML scenario files and validates them against
    expected outputs and success criteria. It does NOT execute actual
    skills (which would require LLM calls), but instead validates the
    structure and format of evaluation files.
    """

    def load_scenarios(self, yaml_path: Path) -> list[EvalScenario]:
        """Load evaluation scenarios from a YAML file.

        Args:
            yaml_path: Path to the YAML file containing scenarios

        Returns:
            List of EvalScenario objects

        Raises:
            FileNotFoundError: If yaml_path does not exist
            yaml.YAMLError: If YAML is malformed
            ValueError: If required scenario fields are missing
        """
        if not yaml_path.exists():
            raise FileNotFoundError(f"Eval file not found: {yaml_path}")

        with yaml_path.open("r") as f:
            data = yaml.safe_load(f)

        if not data:
            raise ValueError(f"Empty YAML file: {yaml_path}")

        # Handle both old format (top-level scenarios) and new format (with skill key)
        scenarios_data = data.get("scenarios", data)
        if not isinstance(scenarios_data, list):
            raise ValueError(f"Expected 'scenarios' list in {yaml_path}")

        scenarios = []
        for idx, scenario in enumerate(scenarios_data):
            # Validate required fields
            required = ["name", "description"]
            missing = [f for f in required if f not in scenario]
            if missing:
                raise ValueError(
                    f"Scenario {idx} missing required fields: {missing} in {yaml_path}"
                )

            # Extract fields with fallbacks
            scenario_id = scenario.get("id", f"scenario-{idx + 1}")
            inputs = scenario.get("inputs", scenario.get("input", {}))
            expected_outputs = scenario.get("expected_outputs", {})
            success_criteria = scenario.get("success_criteria", [])
            tier = scenario.get("tier", scenario.get("token_tier"))

            scenarios.append(
                EvalScenario(
                    id=scenario_id,
                    name=scenario["name"],
                    description=scenario["description"],
                    inputs=inputs,
                    expected_outputs=expected_outputs,
                    success_criteria=success_criteria,
                    tier=tier,
                )
            )

        return scenarios

    def run_scenario(self, scenario: EvalScenario) -> EvalResult:
        """Run a single evaluation scenario.

        This is a structural validation only. It checks:
        - Inputs are well-formed dicts
        - Expected outputs are well-formed dicts
        - Success criteria are non-empty strings

        It does NOT execute actual skills (no LLM calls).

        Args:
            scenario: The scenario to run

        Returns:
            EvalResult with validation results
        """
        errors: list[str] = []
        criteria_results: list[tuple[str, bool]] = []

        # Validate inputs structure
        if not isinstance(scenario.inputs, dict):
            errors.append(f"Inputs must be dict, got {type(scenario.inputs).__name__}")

        # Validate expected_outputs structure
        if not isinstance(scenario.expected_outputs, dict):
            errors.append(
                f"Expected outputs must be dict, got {type(scenario.expected_outputs).__name__}"
            )

        # Validate success_criteria
        if not scenario.success_criteria:
            errors.append("Success criteria cannot be empty")
        else:
            for criterion in scenario.success_criteria:
                if not isinstance(criterion, str) or not criterion.strip():
                    errors.append(f"Invalid criterion: {criterion!r}")
                    criteria_results.append((criterion, False))
                else:
                    # Structural validation passes for valid string criteria
                    criteria_results.append((criterion, True))

        # Validate tier format if present
        if scenario.tier and not re.match(r"^T[123]$", scenario.tier):
            errors.append(f"Invalid tier format: {scenario.tier} (expected T1, T2, or T3)")

        passed = len(errors) == 0

        return EvalResult(
            scenario_id=scenario.id,
            passed=passed,
            actual_output={"inputs": scenario.inputs, "expected": scenario.expected_outputs},
            errors=errors,
            criteria_results=criteria_results,
        )

    def run_all(self, yaml_path: Path) -> list[EvalResult]:
        """Run all scenarios from a YAML file.

        Args:
            yaml_path: Path to the YAML file

        Returns:
            List of EvalResult objects (one per scenario)
        """
        scenarios = self.load_scenarios(yaml_path)
        return [self.run_scenario(scenario) for scenario in scenarios]

    def check_criteria(self, output: dict[str, Any], criteria: list[str]) -> list[tuple[str, bool]]:
        """Check success criteria against actual output.

        This is a helper for future integration with actual skill execution.
        Currently performs basic structural checks.

        Args:
            output: Actual output from a skill
            criteria: List of success criteria strings

        Returns:
            List of (criterion, passed) tuples
        """
        results: list[tuple[str, bool]] = []

        for criterion in criteria:
            # Basic validation: criterion is a non-empty string
            if not isinstance(criterion, str) or not criterion.strip():
                results.append((criterion, False))
                continue

            # For now, we just validate that output is a dict
            # Future: Parse criterion and check against output
            passed = isinstance(output, dict)
            results.append((criterion, passed))

        return results
