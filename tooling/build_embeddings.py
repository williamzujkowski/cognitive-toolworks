#!/usr/bin/env python3
"""
Build lightweight embeddings for skill routing
Uses TF-IDF vectorization for simplicity (no external ML dependencies)
"""

import json
import pickle
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer


def load_skills_index():
    """Load skills index"""
    index_path = Path(__file__).parent.parent / "index" / "skills-index.json"
    with open(index_path) as f:
        return json.load(f)


def build_skill_documents(skills):
    """Build text documents for each skill combining name, summary, keywords"""
    documents = []
    slugs = []

    for skill in skills:
        # Combine all text fields with weight
        doc_parts = []

        # Name gets repeated 3x for higher weight
        doc_parts.extend([skill["name"]] * 3)

        # Summary gets repeated 2x
        doc_parts.extend([skill["summary"]] * 2)

        # Keywords get repeated 1x
        doc_parts.extend(skill.get("keywords", []))

        # Join all parts
        document = " ".join(doc_parts)

        documents.append(document)
        slugs.append(skill["slug"])

    return slugs, documents


def build_embeddings(skills):
    """Build TF-IDF embeddings for all skills"""
    slugs, documents = build_skill_documents(skills)

    # Create TF-IDF vectorizer
    # Use bigrams for better phrase matching
    vectorizer = TfidfVectorizer(
        max_features=500,  # Keep it compact
        ngram_range=(1, 2),  # Unigrams and bigrams
        stop_words="english",
        lowercase=True,
        min_df=1,  # Include rare terms (small corpus)
        max_df=0.8,  # Exclude very common terms
    )

    # Fit and transform
    tfidf_matrix = vectorizer.fit_transform(documents)

    return {
        "slugs": slugs,
        "vectorizer": vectorizer,
        "vectors": tfidf_matrix,
        "metadata": {
            "total_skills": len(slugs),
            "vocab_size": len(vectorizer.vocabulary_),
            "feature_count": tfidf_matrix.shape[1],
        },
    }


def save_embeddings(embeddings, output_dir):
    """Save embeddings to disk in compact format"""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    # Save vectorizer (needed for query embedding)
    with open(output_dir / "vectorizer.pkl", "wb") as f:
        pickle.dump(embeddings["vectorizer"], f)

    # Save vectors as sparse matrix (more compact)
    with open(output_dir / "vectors.pkl", "wb") as f:
        pickle.dump(embeddings["vectors"], f)

    # Save slug mapping as JSON (human-readable)
    with open(output_dir / "slugs.json", "w") as f:
        json.dump(embeddings["slugs"], f, indent=2)

    # Save metadata
    with open(output_dir / "metadata.json", "w") as f:
        json.dump(embeddings["metadata"], f, indent=2)


def main():
    print("Building skill embeddings...")

    skills = load_skills_index()
    print(f"Loaded {len(skills)} skills")

    embeddings = build_embeddings(skills)
    print(f"Built embeddings: {embeddings['metadata']}")

    output_dir = Path(__file__).parent.parent / "index" / "embeddings"
    save_embeddings(embeddings, output_dir)

    print(f"Saved embeddings to: {output_dir}")
    print(f"  - vectorizer.pkl ({output_dir / 'vectorizer.pkl'})")
    print(f"  - vectors.pkl ({output_dir / 'vectors.pkl'})")
    print(f"  - slugs.json ({output_dir / 'slugs.json'})")
    print(f"  - metadata.json ({output_dir / 'metadata.json'})")


if __name__ == "__main__":
    main()
