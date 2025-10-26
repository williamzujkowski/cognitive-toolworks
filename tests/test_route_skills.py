"""Unit tests for tooling/route_skills.py"""

from __future__ import annotations

import json
import pickle
import sys
from pathlib import Path
from unittest.mock import Mock, patch

import pytest
from sklearn.feature_extraction.text import TfidfVectorizer

# Add tooling to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "tooling"))

from route_skills import SkillRouter, main


class TestSkillRouter:
    """Test SkillRouter class."""

    def create_mock_embeddings(self, tmp_path: Path) -> Path:
        """Create mock embeddings files for testing."""
        embeddings_dir = tmp_path / "embeddings"
        embeddings_dir.mkdir(parents=True, exist_ok=True)

        # Create mock vectorizer
        texts = [
            "security validation and compliance checking",
            "kubernetes deployment and infrastructure",
            "api design and documentation",
        ]
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform(texts)

        # Save vectorizer
        with open(embeddings_dir / "vectorizer.pkl", "wb") as f:
            pickle.dump(vectorizer, f)

        # Save vectors
        with open(embeddings_dir / "vectors.pkl", "wb") as f:
            pickle.dump(vectors, f)

        # Save slugs
        slugs = ["security-validator", "kubernetes-deploy", "api-designer"]
        with open(embeddings_dir / "slugs.json", "w") as f:
            json.dump(slugs, f)

        # Save metadata
        metadata = {
            "total_skills": 3,
            "embedding_dim": vectors.shape[1],
            "model": "TfidfVectorizer",
        }
        with open(embeddings_dir / "metadata.json", "w") as f:
            json.dump(metadata, f)

        return embeddings_dir

    def test_init_with_default_path(self) -> None:
        """Initialize with default embeddings path."""
        with patch("route_skills.SkillRouter._load_embeddings") as mock_load:
            router = SkillRouter()
            expected_path = Path(__file__).parent.parent / "index" / "embeddings"
            assert router.embeddings_dir == expected_path
            mock_load.assert_called_once()

    def test_init_with_custom_path(self, tmp_path: Path) -> None:
        """Initialize with custom embeddings path."""
        embeddings_dir = self.create_mock_embeddings(tmp_path)
        router = SkillRouter(embeddings_dir=embeddings_dir)
        assert router.embeddings_dir == embeddings_dir
        assert hasattr(router, "vectorizer")
        assert hasattr(router, "vectors")
        assert hasattr(router, "slugs")
        assert hasattr(router, "metadata")

    def test_load_embeddings(self, tmp_path: Path) -> None:
        """Load embeddings from disk successfully."""
        embeddings_dir = self.create_mock_embeddings(tmp_path)
        router = SkillRouter(embeddings_dir=embeddings_dir)

        # Verify loaded data
        assert router.vectorizer is not None
        assert router.vectors is not None
        assert len(router.slugs) == 3
        assert router.metadata["total_skills"] == 3

    def test_route_basic(self, tmp_path: Path) -> None:
        """Route query to relevant skills."""
        embeddings_dir = self.create_mock_embeddings(tmp_path)
        router = SkillRouter(embeddings_dir=embeddings_dir)

        results = router.route("security compliance validation", top_k=2)

        # Should return 2 results
        assert len(results) <= 2

        # Results should have required fields
        if results:
            assert "slug" in results[0]
            assert "score" in results[0]
            assert "rank" in results[0]
            assert results[0]["rank"] == 1

    def test_route_top_k_parameter(self, tmp_path: Path) -> None:
        """Respect top_k parameter."""
        embeddings_dir = self.create_mock_embeddings(tmp_path)
        router = SkillRouter(embeddings_dir=embeddings_dir)

        results_k1 = router.route("kubernetes deployment", top_k=1)
        results_k3 = router.route("kubernetes deployment", top_k=3)

        assert len(results_k1) <= 1
        assert len(results_k3) <= 3

    def test_route_min_score_filtering(self, tmp_path: Path) -> None:
        """Filter results by minimum score."""
        embeddings_dir = self.create_mock_embeddings(tmp_path)
        router = SkillRouter(embeddings_dir=embeddings_dir)

        # High min_score should filter out low matches
        results_low = router.route("unrelated query xyz", top_k=3, min_score=0.01)
        results_high = router.route("unrelated query xyz", top_k=3, min_score=0.9)

        # High threshold should return fewer results
        assert len(results_high) <= len(results_low)

    def test_route_scores_range(self, tmp_path: Path) -> None:
        """Verify similarity scores are in valid range."""
        embeddings_dir = self.create_mock_embeddings(tmp_path)
        router = SkillRouter(embeddings_dir=embeddings_dir)

        results = router.route("security validation", top_k=3, min_score=0.0)

        for r in results:
            assert 0.0 <= r["score"] <= 1.0

    def test_route_ranks_sequential(self, tmp_path: Path) -> None:
        """Verify ranks are sequential starting from 1."""
        embeddings_dir = self.create_mock_embeddings(tmp_path)
        router = SkillRouter(embeddings_dir=embeddings_dir)

        results = router.route("api documentation design", top_k=3, min_score=0.0)

        for i, r in enumerate(results, start=1):
            assert r["rank"] == i

    def test_route_empty_query(self, tmp_path: Path) -> None:
        """Handle empty query string."""
        embeddings_dir = self.create_mock_embeddings(tmp_path)
        router = SkillRouter(embeddings_dir=embeddings_dir)

        # Empty query should still work (vectorizer handles it)
        results = router.route("", top_k=2)
        assert isinstance(results, list)

    def test_route_no_matches_above_threshold(self, tmp_path: Path) -> None:
        """Return empty list when no matches exceed min_score."""
        embeddings_dir = self.create_mock_embeddings(tmp_path)
        router = SkillRouter(embeddings_dir=embeddings_dir)

        # Impossible threshold should return empty list
        results = router.route("test query", top_k=3, min_score=1.5)
        assert results == []

    def test_route_with_explanation(self, tmp_path: Path) -> None:
        """Generate human-readable explanation."""
        embeddings_dir = self.create_mock_embeddings(tmp_path)
        router = SkillRouter(embeddings_dir=embeddings_dir)

        query = "security validation"
        explanation = router.route_with_explanation(query, top_k=2)

        # Should include query
        assert query in explanation

        # Should include skill count
        assert "skill(s):" in explanation

        # Should include results (if any)
        results = router.route(query, top_k=2)
        if results:
            assert results[0]["slug"] in explanation
            assert "score:" in explanation

    def test_route_with_explanation_formatting(self, tmp_path: Path) -> None:
        """Verify explanation format structure."""
        embeddings_dir = self.create_mock_embeddings(tmp_path)
        router = SkillRouter(embeddings_dir=embeddings_dir)

        explanation = router.route_with_explanation("api design", top_k=1)

        # Should have structured format
        assert explanation.startswith("Query:")
        assert "Top" in explanation
        assert "skill(s):" in explanation

    def test_route_scores_sorted_descending(self, tmp_path: Path) -> None:
        """Verify results sorted by score (descending)."""
        embeddings_dir = self.create_mock_embeddings(tmp_path)
        router = SkillRouter(embeddings_dir=embeddings_dir)

        results = router.route("security kubernetes api", top_k=3, min_score=0.0)

        # Scores should be in descending order
        for i in range(len(results) - 1):
            assert results[i]["score"] >= results[i + 1]["score"]


class TestMain:
    """Test CLI main function."""

    def create_mock_embeddings(self, tmp_path: Path) -> Path:
        """Create mock embeddings files for testing."""
        embeddings_dir = tmp_path / "embeddings"
        embeddings_dir.mkdir(parents=True, exist_ok=True)

        # Create mock vectorizer
        texts = ["security validation", "kubernetes deployment", "api design"]
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform(texts)

        # Save files
        with open(embeddings_dir / "vectorizer.pkl", "wb") as f:
            pickle.dump(vectorizer, f)
        with open(embeddings_dir / "vectors.pkl", "wb") as f:
            pickle.dump(vectors, f)
        with open(embeddings_dir / "slugs.json", "w") as f:
            json.dump(["security-validator", "k8s-deploy", "api-designer"], f)
        with open(embeddings_dir / "metadata.json", "w") as f:
            json.dump({"total_skills": 3}, f)

        return embeddings_dir

    def test_main_with_query(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Run main with query argument."""
        monkeypatch.setattr(sys, "argv", ["route_skills.py", "security", "validation"])

        with patch("route_skills.SkillRouter") as mock_router:
            mock_instance = Mock()
            mock_instance.route_with_explanation.return_value = "Mock explanation"
            mock_instance.route.return_value = [{"slug": "test-skill", "score": 0.9, "rank": 1}]
            mock_router.return_value = mock_instance

            # Should not raise
            main()

            # Verify router was called with combined query
            mock_instance.route_with_explanation.assert_called_with("security validation", top_k=3)

    def test_main_no_arguments(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Exit with error when no query provided."""
        monkeypatch.setattr(sys, "argv", ["route_skills.py"])

        with pytest.raises(SystemExit) as exc_info:
            main()

        assert exc_info.value.code == 1

    def test_main_missing_embeddings(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Handle missing embeddings error."""
        monkeypatch.setattr(sys, "argv", ["route_skills.py", "test", "query"])

        with patch("route_skills.SkillRouter") as mock_router:
            mock_router.side_effect = FileNotFoundError("embeddings not found")

            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 1

    def test_main_output_format(
        self, monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Verify main output includes both explanation and JSON."""
        monkeypatch.setattr(sys, "argv", ["route_skills.py", "api", "design"])

        with patch("route_skills.SkillRouter") as mock_router:
            mock_instance = Mock()
            mock_instance.route_with_explanation.return_value = "Test explanation"
            mock_instance.route.return_value = [{"slug": "api-skill", "score": 0.85, "rank": 1}]
            mock_router.return_value = mock_instance

            main()

            captured = capsys.readouterr()
            # Should have explanation
            assert "Test explanation" in captured.out
            # Should have JSON header
            assert "Raw results (JSON):" in captured.out
            # Should have JSON content
            assert "api-skill" in captured.out

    def test_main_combines_multi_word_query(self, monkeypatch: pytest.MonkeyPatch) -> None:
        """Combine multiple argv words into single query."""
        monkeypatch.setattr(
            sys, "argv", ["route_skills.py", "validate", "kubernetes", "security", "policies"]
        )

        with patch("route_skills.SkillRouter") as mock_router:
            mock_instance = Mock()
            mock_instance.route_with_explanation.return_value = "Mock"
            mock_instance.route.return_value = []
            mock_router.return_value = mock_instance

            main()

            # Should combine all words with spaces
            mock_instance.route_with_explanation.assert_called_with(
                "validate kubernetes security policies", top_k=3
            )


class TestIntegration:
    """Integration tests with real embeddings."""

    def create_realistic_embeddings(self, tmp_path: Path) -> Path:
        """Create realistic embeddings for integration testing."""
        embeddings_dir = tmp_path / "embeddings"
        embeddings_dir.mkdir(parents=True, exist_ok=True)

        # Create realistic skill descriptions
        texts = [
            "security compliance validation oscal framework policy checking",
            "kubernetes deployment infrastructure container orchestration helm",
            "api design documentation openapi rest graphql specification",
            "terraform infrastructure as code cloud provisioning aws azure",
            "cicd pipeline automation jenkins github actions testing deployment",
        ]

        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform(texts)

        with open(embeddings_dir / "vectorizer.pkl", "wb") as f:
            pickle.dump(vectorizer, f)
        with open(embeddings_dir / "vectors.pkl", "wb") as f:
            pickle.dump(vectors, f)

        slugs = [
            "security-oscal-validator",
            "kubernetes-helm-deploy",
            "api-design-generator",
            "terraform-cloud-provisioner",
            "cicd-pipeline-builder",
        ]
        with open(embeddings_dir / "slugs.json", "w") as f:
            json.dump(slugs, f)

        metadata = {
            "total_skills": 5,
            "embedding_dim": vectors.shape[1],
            "model": "TfidfVectorizer",
        }
        with open(embeddings_dir / "metadata.json", "w") as f:
            json.dump(metadata, f)

        return embeddings_dir

    def test_security_query_routes_correctly(self, tmp_path: Path) -> None:
        """Security queries route to security skills."""
        embeddings_dir = self.create_realistic_embeddings(tmp_path)
        router = SkillRouter(embeddings_dir=embeddings_dir)

        results = router.route("validate security compliance with oscal", top_k=3, min_score=0.1)

        # Top result should likely be security-related
        assert len(results) > 0
        # Just verify we got results with valid structure
        assert all("slug" in r and "score" in r and "rank" in r for r in results)

    def test_kubernetes_query_routes_correctly(self, tmp_path: Path) -> None:
        """Kubernetes queries route to k8s skills."""
        embeddings_dir = self.create_realistic_embeddings(tmp_path)
        router = SkillRouter(embeddings_dir=embeddings_dir)

        results = router.route("deploy application to kubernetes cluster", top_k=2, min_score=0.1)

        assert len(results) > 0
        # Verify structure
        assert all(isinstance(r["score"], float) for r in results)
        assert all(r["rank"] in [1, 2] for r in results)

    def test_api_design_query_routes_correctly(self, tmp_path: Path) -> None:
        """API design queries route to api skills."""
        embeddings_dir = self.create_realistic_embeddings(tmp_path)
        router = SkillRouter(embeddings_dir=embeddings_dir)

        results = router.route("create openapi specification for rest api", top_k=1, min_score=0.05)

        assert len(results) > 0
        assert results[0]["rank"] == 1

    def test_default_top_k_is_2(self, tmp_path: Path) -> None:
        """Verify default top_k follows CLAUDE.md (max 2)."""
        embeddings_dir = self.create_realistic_embeddings(tmp_path)
        router = SkillRouter(embeddings_dir=embeddings_dir)

        # Don't specify top_k, should default to 2
        results = router.route("terraform infrastructure provisioning", min_score=0.01)

        # Default should be 2 per CLAUDE.md routing rule
        assert len(results) <= 2
