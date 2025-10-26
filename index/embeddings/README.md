# Skill Embeddings

Lightweight TF-IDF embeddings for intelligent skill routing.

## Files

- `vectorizer.pkl`: Fitted TF-IDF vectorizer (21KB)
- `vectors.pkl`: Sparse skill vectors (15KB)
- `slugs.json`: Skill slug mapping (2KB)
- `metadata.json`: Embedding metadata (<1KB)

**Total size**: ~48KB

## Usage

### Build Embeddings

```bash
python3 tooling/build_embeddings.py
```

### Route Skills

```bash
# Find top skills for a task
python3 tooling/route_skills.py "validate kubernetes security"

# Output:
# Query: validate kubernetes security
#
# Top 2 skill(s):
#   1. kubernetes-manifest-generator (score: 0.512)
#   2. security-container-validator (score: 0.389)
```

### Programmatic Usage

```python
from tooling.route_skills import SkillRouter

router = SkillRouter()
results = router.route("generate unit tests for Python", top_k=2)

# [
#   {'slug': 'testing-unit-generator', 'score': 0.325, 'rank': 1},
#   {'slug': 'tooling-python-generator', 'score': 0.327, 'rank': 2}
# ]
```

## Methodology

- **Embedding Model**: TF-IDF with unigrams + bigrams
- **Input**: Skill name (3x weight) + summary (2x) + keywords (1x)
- **Features**: 500 dimensions (compact)
- **Similarity**: Cosine similarity
- **Routing Rule**: Return ≤2 skills per query (CLAUDE.md §6)

## Regeneration

Rebuild embeddings after:
- Adding/removing skills
- Updating skill summaries or keywords
- Changing skill index

```bash
python3 tooling/build_embeddings.py
```

## Performance

- **Build time**: <1 second (61 skills)
- **Query time**: <10ms per query
- **Memory**: ~100KB loaded

---

**Last Updated**: 2025-10-26
**Skills Indexed**: 61
