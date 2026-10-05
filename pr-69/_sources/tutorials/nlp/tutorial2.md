# Quantifying Features

This tutorial covers methods for transforming unstructured text into numerical variables that can be used in econometric regressions or machine learning models. The goal: turn messy language into a clean `X` matrix for analysis (`Y = βX + ε`).

Two common approaches:

1. **Dictionary methods** — count occurrences of words from a curated word list
2. **TF-IDF** — weight word importance by frequency and rarity across documents

## Dictionary Methods

Dictionary (or lexicon) methods are among the most interpretable approaches in quantitative textual analysis. They:

- Count occurrences of pre-specified words or phrases from a curated dictionary
- Define thematic constructs through domain-specific word lists
- Generate features (e.g., an "uncertainty score") that serve as explanatory variables

**Advantages:**
- Fully interpretable — trace statistical results back to exact terms
- Computationally lightweight
- Well-established in finance and economics research

**Limitations:**
- No context sensitivity — ignores negation, sentence structure
- Cannot handle polysemy or domain-specific nuance
- Require careful dictionary construction

### Loughran-McDonald Dictionary

A widely used resource in finance research. The [Loughran-McDonald (2011) Master Dictionary](https://sraf.nd.edu/loughranmcdonald-master-dictionary/) provides sentiment categories tailored to SEC filings: *Negative, Positive, Uncertainty, Litigious, Strong Modal, Weak Modal, Constraining*.

A copy is available on KLC at:
```
/kellogg/data/workshop_examples/mda_text/Loughran-McDonald_MasterDictionary_1993-2024_uncertainty.csv
```

### Example: Uncertainty Score

```python
import re
import pandas as pd

# Load dictionary
df = pd.read_csv(
    "/kellogg/data/workshop_examples/mda_text/"
    "Loughran-McDonald_MasterDictionary_1993-2024_uncertainty.csv"
)
uncertainty_words = set(df[df["Uncertainty"] > 0]["Word"].str.lower())

def calculate_uncertainty_score(text: str, word_set: set) -> tuple:
    """Return (score, hits, total_words) for a document."""
    words = re.findall(r"\b\w+\b", text.lower())
    hits  = [w for w in words if w in word_set]
    score = len(hits) / len(words) if words else 0
    return score, hits, len(words)

# Test
text = "The future is uncertain and full of risk and doubt."
score, hits, total = calculate_uncertainty_score(text, {"uncertain", "risk", "doubt"})
print(f"Score: {score:.3f}, Hits: {hits}, Total: {total}")
# → Score: 0.333, Hits: ['uncertain', 'risk', 'doubt'], Total: 9
```

### Regression Example

Once you have scores per document, use them as explanatory variables:

```python
from sklearn.linear_model import LinearRegression
import numpy as np

# uncertainty_scores and volatility_values are arrays of floats
X = np.array(uncertainty_scores).reshape(-1, 1)
y = np.array(volatility_values)

model = LinearRegression().fit(X, y)
print(f"β (uncertainty → volatility): {model.coef_[0]:.4f}")
```

## TF-IDF (Term Frequency–Inverse Document Frequency)

TF-IDF weights word importance by how frequently a word appears in a document, offset by how common it is across all documents. Rare words that appear often in a document get high scores.

- **TF (Term Frequency)** — how often a word appears in this document
- **IDF (Inverse Document Frequency)** — log of (total documents / documents containing the word); penalizes common words

```python
from sklearn.feature_extraction.text import TfidfVectorizer

corpus = [
    "The firm disclosed uncertain earnings guidance for next quarter.",
    "Management expressed strong confidence in the merger outcome.",
    "Regulatory risk and uncertainty weighed on quarterly results.",
]

vectorizer = TfidfVectorizer(max_features=20, stop_words="english")
X = vectorizer.fit_transform(corpus)

# Show top terms
feature_names = vectorizer.get_feature_names_out()
print(feature_names)
```

TF-IDF vectors can be used directly as features in classifiers (e.g., random forest, logistic regression) or clustered to identify topics.

## Choosing Between Methods

| | Dictionary Methods | TF-IDF |
|---|---|---|
| **Interpretability** | Very high — map results to specific terms | Moderate — feature weights are interpretable |
| **Requires labeled data** | No | No (unsupervised) |
| **Context sensitivity** | None | None |
| **Best for** | Measuring a known construct (e.g., uncertainty) | Finding discriminating features across a corpus |

## Next Steps

- [Tutorial 3: Paid LLMs for Text Analysis](tutorial3) — when LLMs outperform rule-based methods
- [Tutorial 4: Open-Source LLMs](tutorial4) — running local models on KLC
