# Natural Language Processing

These tutorials provide a hands-on introduction to analyzing text data for research, covering the full spectrum from deterministic rule-based methods to modern LLMs.

## The Research Reproducibility Triad

Before diving in, keep these principles in mind for all text analysis work:

1. **Automate** — transition from interactive notebooks to scripts designed for batch processing
2. **Test** — embed sanity checks and unit tests at every step to validate extraction accuracy
3. **Abstract** — separate core logic (your functions) from specific parameters (model versions, file paths)

## Tutorial Overview

| Tutorial | Methods Covered | When to Use |
|---|---|---|
| [1. Deterministic Extraction](tutorial1) | Regex, tokenization, stemming, POS tagging | Pattern-based extraction; maximum reproducibility |
| [2. Quantifying Features](tutorial2) | Dictionary methods, TF-IDF | Measuring known constructs; regression inputs |
| [3. Paid LLMs](tutorial3) | OpenAI, Anthropic, Google APIs | Nuanced classification; when context matters |
| [4. Open-Source LLMs](tutorial4) | Ollama on KLC | Sensitive data; cost at scale; reproducibility |
| [5. Validation and Rigor](tutorial5) | Cohen's Kappa, cross-validation, Gold Standard | Validating results for academic publication |

```{toctree}
:maxdepth: 2
:hidden:

Deterministic Extraction <tutorial1>
Quantifying Features <tutorial2>
Paid LLMs for Text Analysis <tutorial3>
Open-Source LLMs for Text Analysis <tutorial4>
Validation and Rigor <tutorial5>
```
