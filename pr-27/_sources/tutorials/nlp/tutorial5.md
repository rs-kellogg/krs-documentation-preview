# Validation and Rigor

Text analysis results submitted to academic peer review must meet a high standard of rigor. This tutorial covers the key approaches for validating automated text analysis — whether you use rule-based methods, paid LLMs, or open-source models.

## The Core Trade-off

Choosing a method involves balancing transparency, reproducibility, performance, and cost:

| Feature | Rule-Based & Dictionary | Paid LLMs (API) | Open-Source LLMs |
|---|---|---|---|
| **Logic Transparency** | Fully transparent; exact rules auditable | Opaque; weights and updates not visible | More transparent; weights inspectable |
| **Reproducibility** | High; deterministic outputs | Medium–Low; models may update | High; version-controlled models can be frozen |
| **Performance (Nuance)** | Limited; struggles with sarcasm, negation | High; strong contextual reasoning | Medium–High; improving rapidly |
| **Cost** | Free on KLC or laptop | Usage-based; scales quickly | Free on KLC |
| **Scalability** | Extremely scalable and fast | Scalable but cost-constrained | Scalable depending on infrastructure |
| **Best For** | Baseline trends in stable datasets | High-stakes qualitative synthesis | Privacy-sensitive research; reproducible pipelines |

## Validation Framework

The goal of validation is to establish a **Gold Standard** — ground truth against which all automated outputs are evaluated.

### Step 1: Hand-Code a Representative Sample

Manually label a random, representative sample of 50–200 documents. This is your **Gold Standard**. It should:
- Be drawn randomly from your full corpus (not cherry-picked)
- Be labeled independently by at least two raters
- Cover edge cases you've observed in the data

### Step 2: Measure Inter-Rater Reliability

Before using your Gold Standard, verify that human raters agree with each other. **Cohen's Kappa** adjusts for agreement that could occur by chance:

```python
from sklearn.metrics import cohen_kappa_score

rater1 = ["Positive", "Negative", "Neutral", "Positive", "Negative"]
rater2 = ["Positive", "Neutral",  "Neutral", "Positive", "Negative"]

kappa = cohen_kappa_score(rater1, rater2)
print(f"Cohen's Kappa: {kappa:.3f}")
# Kappa > 0.8 → strong agreement
# Kappa 0.6–0.8 → moderate agreement
# Kappa < 0.6 → consider revising coding guidelines
```

### Step 3: Evaluate Your Automated Method

Compare your automated labels to the Gold Standard:

```python
from sklearn.metrics import classification_report, cohen_kappa_score

gold_standard    = ["Positive", "Negative", "Neutral", "Positive", "Negative"]
automated_labels = ["Positive", "Negative", "Positive", "Positive", "Negative"]

# Accuracy, precision, recall, F1
print(classification_report(gold_standard, automated_labels))

# Agreement vs. chance
kappa = cohen_kappa_score(gold_standard, automated_labels)
print(f"Kappa (human vs. model): {kappa:.3f}")
```

A common threshold for publishable text analysis: **Kappa ≥ 0.7** between your automated method and the Gold Standard.

### Step 4: Cross-Validation

For ML-based approaches, use cross-validation to ensure performance is stable across different subsets of the data:

```python
from sklearn.model_selection import cross_val_score
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

texts  = [...]   # list of document strings
labels = [...]   # list of labels

pipeline = make_pipeline(TfidfVectorizer(), LogisticRegression())
scores   = cross_val_score(pipeline, texts, labels, cv=5, scoring="f1_macro")
print(f"Mean F1: {scores.mean():.3f} ± {scores.std():.3f}")
```

## Documenting for Reproducibility

For every text analysis project:

1. **Record the method** — which model, which dictionary, which parameters
2. **Log all outputs** — save raw results before post-processing; never modify them
3. **Version control everything** — code, prompts, and word lists in git
4. **Freeze model versions** — for LLMs, pin the exact model tag (`gpt-4o-2024-08-06`, `llama3.2:3b`)
5. **Archive your Gold Standard** — store labeled samples alongside your data

## The Research Reproducibility Triad

From a research methods perspective, text analysis pipelines should be:

1. **Automated** — transition from interactive notebooks to Python scripts designed for command-line execution and batch processing
2. **Tested** — embed sanity checks and unit tests at every step to validate data integrity and extraction accuracy
3. **Abstract** — separate core logic (your functions) from specific parameters (model versions, file paths, thresholds)

## Related Pages

- [Tutorial 1: Deterministic Extraction](tutorial1) — rule-based methods (highest reproducibility)
- [Tutorial 2: Quantifying Features](tutorial2) — dictionary methods and TF-IDF
- [Tutorial 3: Paid LLMs for Text Analysis](tutorial3) — API-based LLMs
- [Tutorial 4: Open-Source LLMs](tutorial4) — local models on KLC
