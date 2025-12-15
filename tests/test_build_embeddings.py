"""Unit tests for tooling/build_embeddings.py"""

from __future__ import annotations

import json
import pickle
import sys
from pathlib import Path
from typing import TYPE_CHECKING, Any

# Add tooling to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent / "tooling"))

from build_embeddings import (
    build_embeddings,
    build_skill_documents,
    load_skills_index,
    main,
    save_embeddings,
)

if TYPE_CHECKING:
    import pytest


class TestLoadSkillsIndex:
    """Test loading skills index."""

    def test_load_skills_index(self, tmp_path: Path) -> None:
        """Load skills index successfully."""
        # Create mock index
        skills = [
            {"slug": "skill-1", "name": "Skill One", "summary": "First", "keywords": ["test"]},
            {"slug": "skill-2", "name": "Skill Two", "summary": "Second", "keywords": ["demo"]},
        ]

        index_path = tmp_path / "index" / "skills-index.json"
        index_path.parent.mkdir(parents=True, exist_ok=True)
        index_path.write_text(json.dumps(skills), encoding="utf-8")

        # Mock the path resolution by patching __file__ attribute
        import build_embeddings

        original_file = build_embeddings.__file__
        try:
            build_embeddings.__file__ = str(tmp_path / "tooling" / "build_embeddings.py")
            loaded_skills = load_skills_index()
            assert len(loaded_skills) == 2
            assert loaded_skills[0]["slug"] == "skill-1"
        finally:
            build_embeddings.__file__ = original_file


class TestBuildSkillDocuments:
    """Test skill document building."""

    def test_basic_document_building(self) -> None:
        """Build documents from skill data."""
        skills = [
            {
                "slug": "test-skill",
                "name": "Test Skill",
                "summary": "A test skill",
                "keywords": ["testing", "validation"],
            }
        ]

        slugs, documents = build_skill_documents(skills)

        assert len(slugs) == 1
        assert slugs[0] == "test-skill"
        assert len(documents) == 1

        # Document should contain weighted repetitions
        doc = documents[0]
        # Name appears 3 times
        assert doc.count("Test Skill") == 3
        # Summary appears 2 times
        assert doc.count("A test skill") == 2
        # Keywords appear once each
        assert "testing" in doc
        assert "validation" in doc

    def test_multiple_skills(self) -> None:
        """Build documents for multiple skills."""
        skills = [
            {"slug": "skill-1", "name": "Skill One", "summary": "First", "keywords": ["a"]},
            {"slug": "skill-2", "name": "Skill Two", "summary": "Second", "keywords": ["b"]},
            {"slug": "skill-3", "name": "Skill Three", "summary": "Third", "keywords": ["c"]},
        ]

        slugs, documents = build_skill_documents(skills)

        assert len(slugs) == 3
        assert len(documents) == 3
        assert slugs == ["skill-1", "skill-2", "skill-3"]

    def test_empty_keywords(self) -> None:
        """Handle skills with no keywords."""
        skills = [{"slug": "test", "name": "Test", "summary": "Summary"}]

        slugs, documents = build_skill_documents(skills)

        assert len(slugs) == 1
        assert len(documents) == 1
        # Should still have name and summary
        assert "Test" in documents[0]
        assert "Summary" in documents[0]

    def test_document_ordering(self) -> None:
        """Verify slugs and documents are in same order."""
        skills = [
            {"slug": "zebra", "name": "Zebra", "summary": "Last", "keywords": []},
            {"slug": "alpha", "name": "Alpha", "summary": "First", "keywords": []},
        ]

        slugs, documents = build_skill_documents(skills)

        # Order should match input (not alphabetical)
        assert slugs[0] == "zebra"
        assert slugs[1] == "alpha"
        assert "Zebra" in documents[0]
        assert "Alpha" in documents[1]


class TestBuildEmbeddings:
    """Test embedding generation."""

    def test_build_embeddings_structure(self) -> None:
        """Build embeddings with expected structure."""
        skills = [
            {
                "slug": "security-validator",
                "name": "Security Validator",
                "summary": "Validate security compliance",
                "keywords": ["security", "compliance", "validation"],
            },
            {
                "slug": "api-designer",
                "name": "API Designer",
                "summary": "Design REST APIs",
                "keywords": ["api", "design", "rest"],
            },
        ]

        embeddings = build_embeddings(skills)

        # Verify structure
        assert "slugs" in embeddings
        assert "vectorizer" in embeddings
        assert "vectors" in embeddings
        assert "metadata" in embeddings

        # Verify slugs
        assert embeddings["slugs"] == ["security-validator", "api-designer"]

        # Verify metadata
        assert embeddings["metadata"]["total_skills"] == 2
        assert "vocab_size" in embeddings["metadata"]
        assert "feature_count" in embeddings["metadata"]

    def test_vectorizer_configuration(self) -> None:
        """Verify vectorizer is configured correctly."""
        # Need at least 2 skills to avoid max_df/min_df conflict
        skills = [
            {"slug": "test1", "name": "Test One", "summary": "Testing one", "keywords": ["test"]},
            {"slug": "test2", "name": "Test Two", "summary": "Testing two", "keywords": ["demo"]},
        ]

        embeddings = build_embeddings(skills)
        vectorizer = embeddings["vectorizer"]

        # Check vectorizer settings
        assert vectorizer.max_features == 500
        assert vectorizer.ngram_range == (1, 2)
        assert vectorizer.stop_words == "english"
        assert vectorizer.lowercase is True
        assert vectorizer.min_df == 1
        assert vectorizer.max_df == 0.8

    def test_tfidf_matrix_shape(self) -> None:
        """Verify TF-IDF matrix has correct shape."""
        skills = [
            {"slug": "s1", "name": "Skill One", "summary": "First skill", "keywords": ["one"]},
            {"slug": "s2", "name": "Skill Two", "summary": "Second skill", "keywords": ["two"]},
            {"slug": "s3", "name": "Skill Three", "summary": "Third skill", "keywords": ["three"]},
        ]

        embeddings = build_embeddings(skills)
        vectors = embeddings["vectors"]

        # Matrix should have 3 rows (one per skill)
        assert vectors.shape[0] == 3

        # Matrix should have columns equal to feature count
        assert vectors.shape[1] == embeddings["metadata"]["feature_count"]

    def test_small_corpus(self) -> None:
        """Handle small corpus (2 skills minimum for TF-IDF params)."""
        # TF-IDF with max_df=0.8, min_df=1 requires at least 2 documents
        skills = [
            {"slug": "skill-1", "name": "Skill One", "summary": "First", "keywords": ["one"]},
            {"slug": "skill-2", "name": "Skill Two", "summary": "Second", "keywords": ["two"]},
        ]

        embeddings = build_embeddings(skills)

        assert embeddings["metadata"]["total_skills"] == 2
        assert embeddings["vectors"].shape[0] == 2


class TestSaveEmbeddings:
    """Test embedding persistence."""

    def create_mock_embeddings(self) -> dict[str, Any]:
        """Create mock embeddings for testing."""
        from sklearn.feature_extraction.text import TfidfVectorizer

        texts = ["security validation", "api design"]
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform(texts)

        return {
            "slugs": ["security-validator", "api-designer"],
            "vectorizer": vectorizer,
            "vectors": vectors,
            "metadata": {
                "total_skills": 2,
                "vocab_size": len(vectorizer.vocabulary_),
                "feature_count": vectors.shape[1],
            },
        }

    def test_save_embeddings_creates_files(self, tmp_path: Path) -> None:
        """Save embeddings creates all required files."""
        embeddings = self.create_mock_embeddings()
        output_dir = tmp_path / "embeddings"

        save_embeddings(embeddings, output_dir)

        # Verify all files created
        assert (output_dir / "vectorizer.pkl").exists()
        assert (output_dir / "vectors.pkl").exists()
        assert (output_dir / "slugs.json").exists()
        assert (output_dir / "metadata.json").exists()

    def test_save_embeddings_creates_directory(self, tmp_path: Path) -> None:
        """Save embeddings creates output directory if missing."""
        embeddings = self.create_mock_embeddings()
        output_dir = tmp_path / "nested" / "output" / "dir"

        # Directory doesn't exist yet
        assert not output_dir.exists()

        save_embeddings(embeddings, output_dir)

        # Directory should be created
        assert output_dir.exists()
        assert (output_dir / "slugs.json").exists()

    def test_saved_vectorizer_loadable(self, tmp_path: Path) -> None:
        """Saved vectorizer can be loaded and used."""
        embeddings = self.create_mock_embeddings()
        output_dir = tmp_path / "embeddings"

        save_embeddings(embeddings, output_dir)

        # Load vectorizer
        # S301: Pickle files are from trusted test data (not user input)
        with (output_dir / "vectorizer.pkl").open("rb") as f:
            loaded_vectorizer = pickle.load(f)

        # Should be able to transform text
        test_vec = loaded_vectorizer.transform(["security"])
        assert test_vec is not None

    def test_saved_vectors_loadable(self, tmp_path: Path) -> None:
        """Saved vectors can be loaded."""
        embeddings = self.create_mock_embeddings()
        output_dir = tmp_path / "embeddings"

        save_embeddings(embeddings, output_dir)

        # Load vectors
        # S301: Pickle files are from trusted test data (not user input)
        with (output_dir / "vectors.pkl").open("rb") as f:
            loaded_vectors = pickle.load(f)

        # Should have same shape
        assert loaded_vectors.shape == embeddings["vectors"].shape

    def test_saved_slugs_format(self, tmp_path: Path) -> None:
        """Saved slugs are in correct JSON format."""
        embeddings = self.create_mock_embeddings()
        output_dir = tmp_path / "embeddings"

        save_embeddings(embeddings, output_dir)

        # Load and verify slugs
        with (output_dir / "slugs.json").open() as f:
            slugs = json.load(f)

        assert isinstance(slugs, list)
        assert len(slugs) == 2
        assert slugs == ["security-validator", "api-designer"]

    def test_saved_metadata_format(self, tmp_path: Path) -> None:
        """Saved metadata is in correct JSON format."""
        embeddings = self.create_mock_embeddings()
        output_dir = tmp_path / "embeddings"

        save_embeddings(embeddings, output_dir)

        # Load and verify metadata
        with (output_dir / "metadata.json").open() as f:
            metadata = json.load(f)

        assert isinstance(metadata, dict)
        assert metadata["total_skills"] == 2
        assert "vocab_size" in metadata
        assert "feature_count" in metadata

    def test_save_with_string_path(self, tmp_path: Path) -> None:
        """Save embeddings accepts string path."""
        embeddings = self.create_mock_embeddings()
        output_dir = tmp_path / "embeddings"

        # Pass as string instead of Path
        save_embeddings(embeddings, str(output_dir))

        assert (output_dir / "vectorizer.pkl").exists()


class TestMain:
    """Test CLI main function."""

    def create_mock_index(self, tmp_path: Path) -> Path:
        """Create mock skills index."""
        skills = [
            {
                "slug": "test-skill-1",
                "name": "Test Skill One",
                "summary": "First test skill",
                "keywords": ["test", "one"],
            },
            {
                "slug": "test-skill-2",
                "name": "Test Skill Two",
                "summary": "Second test skill",
                "keywords": ["test", "two"],
            },
        ]

        index_path = tmp_path / "index" / "skills-index.json"
        index_path.parent.mkdir(parents=True, exist_ok=True)
        index_path.write_text(json.dumps(skills), encoding="utf-8")

        return index_path.parent

    def test_main_creates_embeddings(
        self, tmp_path: Path, capsys: pytest.CaptureFixture[str]
    ) -> None:
        """Main function creates embeddings successfully."""
        self.create_mock_index(tmp_path)
        embeddings_dir = tmp_path / "index" / "embeddings"

        # Mock Path(__file__) resolution
        import build_embeddings

        original_file = build_embeddings.__file__
        try:
            build_embeddings.__file__ = str(tmp_path / "tooling" / "build_embeddings.py")
            main()

            # Verify output messages
            captured = capsys.readouterr()
            assert "Building skill embeddings" in captured.out
            assert "Loaded 2 skills" in captured.out
            assert "Built embeddings" in captured.out
            assert "Saved embeddings to" in captured.out

            # Verify files created
            assert embeddings_dir.exists()
            assert (embeddings_dir / "vectorizer.pkl").exists()
            assert (embeddings_dir / "vectors.pkl").exists()
            assert (embeddings_dir / "slugs.json").exists()
            assert (embeddings_dir / "metadata.json").exists()

        finally:
            build_embeddings.__file__ = original_file

    def test_main_output_format(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """Main function outputs all expected information."""
        self.create_mock_index(tmp_path)

        import build_embeddings

        original_file = build_embeddings.__file__
        try:
            build_embeddings.__file__ = str(tmp_path / "tooling" / "build_embeddings.py")
            main()

            captured = capsys.readouterr()

            # Verify all output sections
            assert "Building skill embeddings" in captured.out
            assert "Loaded" in captured.out
            assert "skills" in captured.out
            assert "Built embeddings" in captured.out
            assert "total_skills" in captured.out
            assert "Saved embeddings to" in captured.out
            assert "vectorizer.pkl" in captured.out
            assert "vectors.pkl" in captured.out
            assert "slugs.json" in captured.out
            assert "metadata.json" in captured.out

        finally:
            build_embeddings.__file__ = original_file


class TestIntegration:
    """Integration tests for complete workflow."""

    def test_complete_workflow(self, tmp_path: Path) -> None:
        """Test complete embedding generation workflow."""
        # Create realistic skills
        skills = [
            {
                "slug": "security-oscal-validator",
                "name": "Security OSCAL Validator",
                "summary": "Validate security compliance using OSCAL framework",
                "keywords": ["security", "compliance", "oscal", "validation"],
            },
            {
                "slug": "kubernetes-helm-deploy",
                "name": "Kubernetes Helm Deployer",
                "summary": "Deploy applications to Kubernetes using Helm charts",
                "keywords": ["kubernetes", "helm", "deployment", "infrastructure"],
            },
            {
                "slug": "api-design-generator",
                "name": "API Design Generator",
                "summary": "Generate OpenAPI specifications for REST APIs",
                "keywords": ["api", "design", "openapi", "rest"],
            },
        ]

        # Build embeddings
        embeddings = build_embeddings(skills)

        # Save to disk
        output_dir = tmp_path / "embeddings"
        save_embeddings(embeddings, output_dir)

        # Verify we can load and use them
        # S301: Pickle files are from trusted test data (not user input)
        with (output_dir / "vectorizer.pkl").open("rb") as f:
            vectorizer = pickle.load(f)

        with (output_dir / "vectors.pkl").open("rb") as f:
            vectors = pickle.load(f)

        with (output_dir / "slugs.json").open() as f:
            slugs = json.load(f)

        # Test query transformation
        query = "validate security compliance"
        query_vec = vectorizer.transform([query])

        assert query_vec is not None
        assert vectors.shape[0] == 3
        assert len(slugs) == 3
