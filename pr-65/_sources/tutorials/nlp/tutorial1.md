# Deterministic Extraction

Raw text is "unstructured" — a long string of characters that a computer doesn't naturally understand. Before reaching for an LLM, consider whether rule-based methods can solve your problem. When they can, they produce **reproducible, auditable, and computationally lightweight** results.

This tutorial covers two categories of deterministic extraction:

1. **Regular expressions** — pattern-based string matching
2. **Classic NLP pipeline** — tokenization, stemming/lemmatizing, and POS tagging

## When to Use Deterministic Methods

Using LLMs introduces uncertainty into your workflow. Whenever possible, rule-based logic is preferred because it is fully reproducible and auditable. Consider regex and NLP pipelines for:

- Extracting structured fields with known patterns (dates, identifiers, codes)
- Cleaning and normalizing text before analysis
- Tasks where you need to trace each result back to an exact rule

## Regular Expressions

A **regular expression** (regex) is syntax for representing patterns of characters in a text string. Use regex to search for matches, replace patterns, or split strings.

Good references: [Regex 101](https://regex101.com/) (interactive) and [Tao of Regular Expressions](https://www.scootersoftware.com/RegEx.html) (reference).

### Literal Characters

| Pattern | Meaning |
|---|---|
| `stock option` | the literal phrase "stock option" |
| `[a\|b\|c\|d]` | a or b or c or d |
| `[a-d]` | a or b or c or d |
| `[A-D]` | A or B or C or D |

```python
import re

# Standardize spelling
target  = "We observed unusual behaviours at high temperatures"
pattern = "behaviour"
repl    = "behavior"
result  = re.sub(pattern, repl, target)
print(result)
# → We observed unusual behaviors at high temperatures
```

### Metacharacter Classes

| Pattern | Meaning |
|---|---|
| `\d` | any digit (`[0-9]`) |
| `\D` | anything that is not a digit |
| `\w` | a "word" character (`[A-Za-z0-9]`) |
| `\s` | any whitespace (space, tab, newline) |
| `.` | any character except newline |

```python
import re

# Extract years from messy raw data
target = """
1993
2 15 17.8 30.2 49 9.39 35 4.0 0.6
1992
4.0 17 19.3 36.6 55 13.6 30 4.0 0.7
1991
5.0 27 32.3 62.8 94 21.2 33 4.0 1
"""
pattern = r"\d{4}"
matches = re.findall(pattern, target)
print(matches)
# → ['1993', '1992', '1991']
```

### Quantifiers, Anchors, and Groups

| Modifier | Meaning |
|---|---|
| `*` | 0 or more times |
| `+` | 1 or more times |
| `{n}` | exactly n times |
| `{i,j}` | at least i, fewer than j times |
| `^` | beginning of string |
| `$` | end of string |
| `(grp1)(grp2)` | capture groups; reference as `\1`, `\2` |

```python
import re

# Convert messy data to CSV by splitting on years
target = """
1993
2 15 17.8 30.2 49
1992
4.0 17 19.3 36.6 55
1991
5.0 27 32.3 62.8 94
"""
mid = re.sub(r"\s+", ",", target.strip())
result = re.sub(r",((\d{4}))", r"\n\1", mid)
print(result)
```

## Classic NLP Pipeline

Natural Language Processing follows a series of deterministic steps to transform raw text into structured data a model can parse. Install [spaCy](https://spacy.io/) to follow along:

```bash
pip install spacy
python -m spacy download en_core_web_sm
```

### Tokenization

Tokenization breaks a sentence into its most basic units — words and punctuation.

```python
import spacy

nlp  = spacy.load("en_core_web_sm")
text = "Hostile takeovers can get messy. But before you criticize a corporate raider, you should walk a mile in their shoes."

doc    = nlp(text)
tokens = [t.text for t in doc if not t.is_space]
print(tokens)
# → ['Hostile', 'takeovers', 'can', 'get', 'messy', '.', ...]
```

### Bigrams (N-grams)

Bigrams capture context that single words lose. They ensure "corporate raider" is treated as a single concept.

```python
bigrams = [tuple(tokens[i:i+2]) for i in range(len(tokens) - 1)]
print(bigrams[10:15])
# → [('a', 'corporate'), ('corporate', 'raider'), ('raider', ','), ...]
```

### Stemming

Stemming normalizes words to a root form by chopping suffixes — fast but crude.

```python
from nltk.stem import PorterStemmer

stemmer = PorterStemmer()
stems = [stemmer.stem(t.text) for t in doc if not t.is_punct]
print(stems[7:11])
# → ['you', 'critic', 'a', 'corpor']
```

### Lemmatizing

Lemmatization uses a dictionary to return the true base form (*lemma*) — more accurate than stemming.

```python
lemmas = [t.lemma_ for t in doc if not t.is_punct]
print(lemmas[15:25])
# → ['walk', 'a', 'mile', 'in', 'their', 'shoe', 'that', 'way', ...]
```

### Part-of-Speech Tagging

POS tagging labels each token with its grammatical role (noun, verb, adjective, etc.).

```python
pos_tags = [(t.text, t.pos_, t.tag_) for t in doc if not t.is_space]
for token, pos, tag in pos_tags[:8]:
    print(f"{token:15} {pos:10} {tag}")
# → Hostile         ADJ        JJ
#    takeovers       NOUN       NNS
#    can             AUX        MD
#    get             VERB       VB
#    messy           ADJ        JJ
```

## Next Steps

- [Tutorial 2: Quantifying Features](tutorial2) — dictionary methods and TF-IDF
- [Tutorial 3: Paid LLMs for Text Analysis](tutorial3) — when to use LLMs instead of rules
