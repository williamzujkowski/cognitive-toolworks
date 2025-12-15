"""
AGENTS.md Generator.

Generates AGENTS.md files for repositories by analyzing:
- Package configuration (package.json, pyproject.toml, Cargo.toml)
- CI/CD configuration (GitHub Actions, etc.)
- Existing documentation (README, CONTRIBUTING, CLAUDE.md)
- Directory structure
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from cognitive_toolworks.llm.client import LLMClient
from cognitive_toolworks.llm.prompts import get_prompt

if TYPE_CHECKING:
    from pathlib import Path


@dataclass
class RepoAnalysis:
    """Analysis of a repository structure."""

    name: str
    path: Path
    language: str
    package_manager: str
    test_framework: str
    has_readme: bool
    has_agents_md: bool
    has_claude_md: bool
    has_contributing: bool
    readme_content: str = ""
    existing_guidance: str = ""
    ci_config: str = ""
    directories: dict[str, str] = field(default_factory=dict)


class AgentsGenerator:
    """
    Generates AGENTS.md files for repositories.

    Analyzes repository structure and uses LLM to generate
    comprehensive agent instructions following the AAIF spec.
    """

    def __init__(self, llm_client: LLMClient | None = None) -> None:
        self.llm = llm_client or LLMClient()

    async def generate(
        self,
        repo_path: Path,
        include_llms_txt: bool = False,
    ) -> tuple[str, str | None]:
        """
        Generate AGENTS.md (and optionally llms.txt) for a repository.

        Args:
            repo_path: Path to the repository.
            include_llms_txt: Whether to also generate llms.txt.

        Returns:
            Tuple of (agents_md_content, llms_txt_content or None).
        """
        # Analyze repository
        analysis = self._analyze_repo(repo_path)

        # Generate AGENTS.md
        agents_content = await self._generate_agents_md(analysis)

        # Generate llms.txt if requested
        llms_content = None
        if include_llms_txt:
            llms_content = await self._generate_llms_txt(analysis)

        return agents_content, llms_content

    def _analyze_repo(self, repo_path: Path) -> RepoAnalysis:
        """Analyze repository structure and configuration."""
        repo_path = repo_path.resolve()

        # Detect language and package manager
        language, package_manager = self._detect_language(repo_path)

        # Detect test framework
        test_framework = self._detect_test_framework(repo_path, language)

        # Check for documentation files
        readme_path = self._find_readme(repo_path)
        readme_content = readme_path.read_text() if readme_path else ""

        # Check for existing guidance
        existing_guidance = ""
        claude_md = repo_path / "CLAUDE.md"
        contributing = repo_path / "CONTRIBUTING.md"

        if claude_md.exists():
            existing_guidance += f"## CLAUDE.md\n{claude_md.read_text()}\n\n"
        if contributing.exists():
            existing_guidance += f"## CONTRIBUTING.md\n{contributing.read_text()}\n\n"

        # Find CI config
        ci_config = self._find_ci_config(repo_path)

        # Analyze directory structure
        directories = self._analyze_directories(repo_path)

        return RepoAnalysis(
            name=repo_path.name,
            path=repo_path,
            language=language,
            package_manager=package_manager,
            test_framework=test_framework,
            has_readme=readme_path is not None,
            has_agents_md=(repo_path / "AGENTS.md").exists(),
            has_claude_md=claude_md.exists(),
            has_contributing=contributing.exists(),
            readme_content=readme_content[:5000],  # Limit size
            existing_guidance=existing_guidance[:3000],
            ci_config=ci_config,
            directories=directories,
        )

    def _detect_language(self, repo_path: Path) -> tuple[str, str]:
        """Detect primary language and package manager."""
        # Check for common package files
        if (repo_path / "package.json").exists():
            # Check for specific package managers
            if (repo_path / "pnpm-lock.yaml").exists():
                return "JavaScript/TypeScript", "pnpm"
            elif (repo_path / "yarn.lock").exists():
                return "JavaScript/TypeScript", "yarn"
            elif (repo_path / "bun.lockb").exists():
                return "JavaScript/TypeScript", "bun"
            return "JavaScript/TypeScript", "npm"

        if (repo_path / "pyproject.toml").exists():
            # Check for specific Python package managers
            if (repo_path / "uv.lock").exists():
                return "Python", "uv"
            elif (repo_path / "poetry.lock").exists():
                return "Python", "poetry"
            return "Python", "pip"

        if (repo_path / "requirements.txt").exists():
            return "Python", "pip"

        if (repo_path / "Cargo.toml").exists():
            return "Rust", "cargo"

        if (repo_path / "go.mod").exists():
            return "Go", "go"

        if (repo_path / "Gemfile").exists():
            return "Ruby", "bundler"

        if (repo_path / "pom.xml").exists():
            return "Java", "maven"

        if (repo_path / "build.gradle").exists() or (
            repo_path / "build.gradle.kts"
        ).exists():
            return "Java/Kotlin", "gradle"

        return "Unknown", "unknown"

    def _detect_test_framework(self, repo_path: Path, language: str) -> str:
        """Detect the test framework used."""
        if "Python" in language:
            if (repo_path / "pytest.ini").exists() or (
                repo_path / "pyproject.toml"
            ).exists():
                pyproject = repo_path / "pyproject.toml"
                if pyproject.exists() and "pytest" in pyproject.read_text():
                    return "pytest"
            if (repo_path / "setup.cfg").exists():
                if "pytest" in (repo_path / "setup.cfg").read_text():
                    return "pytest"
            return "pytest"  # Default for Python

        if "JavaScript" in language or "TypeScript" in language:
            package_json = repo_path / "package.json"
            if package_json.exists():
                content = package_json.read_text()
                if "vitest" in content:
                    return "vitest"
                if "jest" in content:
                    return "jest"
                if "mocha" in content:
                    return "mocha"
            return "jest"  # Default

        if "Rust" in language:
            return "cargo test"

        if "Go" in language:
            return "go test"

        return "unknown"

    def _find_readme(self, repo_path: Path) -> Path | None:
        """Find README file in repository."""
        for name in ["README.md", "README.rst", "README.txt", "README"]:
            path = repo_path / name
            if path.exists():
                return path
        return None

    def _find_ci_config(self, repo_path: Path) -> str:
        """Find and extract CI/CD configuration."""
        ci_content = ""

        # GitHub Actions
        gh_workflows = repo_path / ".github" / "workflows"
        if gh_workflows.exists():
            for workflow in gh_workflows.glob("*.yml"):
                ci_content += f"## {workflow.name}\n{workflow.read_text()[:1000]}\n\n"
            for workflow in gh_workflows.glob("*.yaml"):
                ci_content += f"## {workflow.name}\n{workflow.read_text()[:1000]}\n\n"

        # GitLab CI
        gitlab_ci = repo_path / ".gitlab-ci.yml"
        if gitlab_ci.exists():
            ci_content += f"## .gitlab-ci.yml\n{gitlab_ci.read_text()[:1000]}\n\n"

        # CircleCI
        circleci = repo_path / ".circleci" / "config.yml"
        if circleci.exists():
            ci_content += f"## CircleCI\n{circleci.read_text()[:1000]}\n\n"

        return ci_content[:3000]  # Limit total size

    def _analyze_directories(self, repo_path: Path) -> dict[str, str]:
        """Analyze key directories in the repository."""
        directories: dict[str, str] = {}

        common_dirs = {
            "src": "Source code",
            "lib": "Library code",
            "app": "Application code",
            "tests": "Test files",
            "test": "Test files",
            "spec": "Test specifications",
            "docs": "Documentation",
            "scripts": "Utility scripts",
            "bin": "Executable scripts",
            "config": "Configuration files",
            "public": "Public assets",
            "static": "Static files",
            "assets": "Asset files",
            "components": "UI components",
            "pages": "Page components",
            "api": "API handlers",
            "utils": "Utility functions",
            "helpers": "Helper functions",
            "models": "Data models",
            "services": "Service layer",
            "controllers": "Controllers",
            "middleware": "Middleware",
        }

        for dir_name, description in common_dirs.items():
            if (repo_path / dir_name).is_dir():
                directories[dir_name] = description

        return directories

    async def _generate_agents_md(self, analysis: RepoAnalysis) -> str:
        """Generate AGENTS.md content using LLM."""
        prompt = get_prompt("agents_md").format(
            repo_name=analysis.name,
            language=analysis.language,
            package_manager=analysis.package_manager,
            test_framework=analysis.test_framework,
            readme_content=analysis.readme_content[:2000],
            existing_guidance=analysis.existing_guidance[:1500],
            ci_config=analysis.ci_config[:1000],
        )
        system = get_prompt("agents_md_system")

        async with self.llm:
            response = await self.llm.generate(prompt, system=system)

        return response.content

    async def _generate_llms_txt(self, analysis: RepoAnalysis) -> str:
        """Generate llms.txt content."""
        # Build a simple llms.txt
        lines = [
            f"# {analysis.name}",
            "",
            f"Language: {analysis.language}",
            f"Package Manager: {analysis.package_manager}",
            "",
            "## Key Directories",
        ]

        for dir_name, description in analysis.directories.items():
            lines.append(f"- {dir_name}/: {description}")

        lines.extend(
            [
                "",
                "## Testing",
                f"Framework: {analysis.test_framework}",
                "",
                "## Documentation",
            ]
        )

        if analysis.has_readme:
            lines.append("- README.md: Project documentation")
        if analysis.has_agents_md:
            lines.append("- AGENTS.md: Agent instructions")
        if analysis.has_claude_md:
            lines.append("- CLAUDE.md: Claude-specific instructions")
        if analysis.has_contributing:
            lines.append("- CONTRIBUTING.md: Contribution guidelines")

        return "\n".join(lines)

    def generate_sync(
        self,
        repo_path: Path,
        include_llms_txt: bool = False,
    ) -> tuple[str, str | None]:
        """Synchronous wrapper for generate."""
        import asyncio

        return asyncio.run(self.generate(repo_path, include_llms_txt))
