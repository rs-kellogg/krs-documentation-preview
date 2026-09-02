(qualitative-coding-with-llms)=
# Qualitative Coding with LLMs: A Worked Example

## Prerequisites

- Python 3 with `openai` and `pandas` installed (`pip install openai pandas`)
- An OpenAI API key saved in `~/keys/openai-key.txt` in your home directory — see [OpenAI API](/guides/openai/openai-api)
- Familiarity with reading Python scripts; no prior qualitative-coding experience required

## Materials

Download the tutorial files, unzip, and run the scripts from the `code/` folder (they load paragraphs from the sibling `data/groups/` folder):

- {download}`Tutorial files (zip) <qual-coding-materials.zip>` — five Python scripts and six sample paragraphs

The sample paragraphs are synthetic examples written for this tutorial.

## Executive Summary

**Qualitative coding** is an iterative, interpretive process of indexing textual or non-numerical data to uncover deeper meanings, conceptual connections, and overarching themes. While other coding tasks rely on deterministic, unambiguous steps to automate the translation of text or images into structured data, qualitative coding is not as cut and dry. Its core nuance is that it requires continuous contextual judgment to interpret ambiguity, subtext, and conflicting evidence within the data.

Qualitative coding can show up across a wide range of research settings: from lab experiments asking subjects to explain their decisions, to observational data like news coverage, field notes, or historical administrative records.

For instance:

- **Lab experiments.** A study asks participants to explain in writing why they chose to share or keep money in a decision-making game.
  - *Target variable:* Primary motivation (Altruism, Self-interest, or Social pressure).
  - *Hard case:* A participant writes, "I wanted to be kind and give half because everyone was watching."
  - *Human judgment:* The action (giving half) looks like generosity, but the text reveals the true motive is avoiding embarrassment. A human coder reads the social context and codes it as Social pressure rather than Altruism.

- **Observational data.** A researcher collects news coverage of a proposed law to see how journalists frame the policy.
  - *Target variable:* Article framing (Economic impact or National security).
  - *Hard case:* A headline reads, "New Port Restrictions Aim to Cut Smuggling and Protect Local Shipping Jobs."
  - *Human judgment:* The headline explicitly mentions both security (smuggling) and the economy (jobs). A human coder reads the full article to judge which angle dominates the story, rather than letting a keyword count force a coin-flip choice.

Classifying cases against a rubric like these is precisely what this walkthrough is built around. Using an LLM for this work is promising, but the tricky part is managing the exact judgment calls that a rubric alone cannot make for you.

We'll cover:

- Why a rubric can never fully anticipate the data it's applied to (Section 1)
- The anatomy of an LLM API call (Section 2)
- Coding the rubric you are given (Section 3)
- Giving the model an explicit "out" for hard cases (Section 4)
- Anchoring the model's judgment with examples (Section 5)
- Scaling the pipeline across multiple inputs (Section 6)
- Why rerunning the same prompt doesn't always give the same answer (Section 7)
- Checking agreement between coders (Section 8)
- What to do when coders disagree (Section 9)

---

## 0. The Toy Example

Before any code, here is the toy example this whole walkthrough is built around.

**The research question.** Scholars of civil-military relations often want to know how consistently a state's security forces are actually integrated into its formal chain of command, since the answer bears on questions like coup risk, civilian control, and accountability for abuses those forces commit. A natural first step in a project like that is descriptive: across a set of security forces, which ones are cleanly state-integrated, which operate more like parallel or non-state structures (think mercenary groups), and how much variation is there even within a single country's security apparatus? Classifying dozens or hundreds of forces this way by hand is slow, which makes it a natural candidate for an LLM-assisted coding pipeline, provided that pipeline can be trusted to handle the hard cases responsibly.

**The task.** A professor working on a project like this has handed you a rubric and a set of paragraphs describing specific security forces, and asked you to use an LLM to code each one against it.

**The rubric.**

| Dimension | State-integrated | Non-state-parallel |
|---|---|---|
| Formal integration | Constitutionally part of the regular military | Parallel or parastatal structure |
| Command and control | Standard hierarchy under civilian or military authority | Personalized or opaque chain of command |
| Compensation and loyalty basis | Standard state salary or service law | Patronage, business ventures, or informal arrangements |

**The data.** Here are some groups to start with. Each paragraph is saved as its own file in `data/groups/`; the scripts load from that folder starting in Section 3.

Section 1 uses this same rubric and these same paragraphs to work through why classifying these groups is harder than the rubric alone suggests.

---

## 1. Why the Rubric Can't Be Complete

Qualitative coding starts with a **rubric** (or codebook): a structured set of categories meant to capture the dimensions of interest in some body of text, image, or observational data. The rubric is a starting point, not a finish line. No matter how carefully it is built, it cannot fully anticipate every case it will eventually be applied to.

This is a familiar problem to anyone who has hand-coded real data. A rubric built from theory or from a first pass through the data will inevitably meet cases that don't sit cleanly in any one category. When that happens, a human coder relies on **judgment**, informed by domain expertise, context, and the accumulated sense of "what the rubric-writer probably meant," to make a call anyway.

Apply this rubric to all six groups, and the picture splits into two very different kinds of cases.

Two of them are genuinely easy: every dimension points the same direction, so the rubric alone is enough.

- **AFP (Philippines):** Constitutionally established, funded through congressional appropriations, and run through a centralized chain of command to the Chief of Staff and the President, with no independent business ventures. State-integrated on all three dimensions.
- **Wagner Group (Russia):** Privately funded, privately commanded, and structured explicitly outside the Ministry of Defense's chain of command, with personnel under private contract rather than military oath. Non-state-parallel on all three dimensions.

The other four are harder, and harder in two different ways. Three of them split within a single dimension, the way you'd expect a hard case to:

- **ABRI (Indonesia):** Formally the national armed forces, paid through the state defense budget, with standard rank and chain of command: clear on dimensions 1 and 2. But under the *dwifungsi* doctrine, officers also ran a sprawling network of military-owned businesses, blurring salary-based compensation with off-budget business income. That third dimension does not fit cleanly into either column.
- **ISI (Pakistan):** A formally constituted state intelligence agency, staffed by seconded military officers: clear on dimensions 1 and 3. But its actual command relationships have often bypassed civilian oversight in practice, reporting informally to military leadership rather than elected government. That second dimension resists a clean label too.
- **IRGC (Iran):** Constitutionally established, but explicitly as a *parallel* force alongside the regular military (Artesh), answering directly to the Supreme Leader: already unusual on dimension 1. Personnel are nominally salaried, but the IRGC also controls major business conglomerates and runs the Quds Force through informal proxy militias abroad, so dimensions 2 and 3 both resist a clean call.

The fourth, Sudan's Janjaweed, is harder in a different way:

- **Janjaweed (Sudan):** Every dimension actually points toward non-state-parallel: no constitutional status, an opaque chieftain-based command hierarchy, and compensation through patronage and looted resources rather than salary. But the paragraph also says the militia was covertly mobilized, armed, and coordinated by the Sudanese government as an instrument of regime survival, meaning the state built this "non-state" structure on purpose for the deniability it provides. Clean on every dimension, but a rubric with no dimension for engineered deniability still misses what matters most about this case.

In each of these four cases, the evidence splits, or the rubric's categories themselves fall short of what's actually going on. Forcing every dimension into one of the two labels the rubric offers loses information a careful coder would want to preserve. That gap is exactly what a third category, "ambiguous," is for, and Section 4 builds it directly into the coding pipeline.

No single sentence in the rubric resolves these cases. A human coder has to weigh partial evidence and make a defensible call, and document why. The rest of this walkthrough is about how to get an LLM to do the same thing: apply a rubric the way a trained research assistant would, including knowing when to hedge.

---

## 2. Anatomy of an LLM API Call

Before getting into the specifics of this coding task, it helps to have the basic shape of an LLM API call in view, since most of what follows is really just decisions about how to fill in a few pieces of that shape. For API key setup and authentication, see [OpenAI API](/guides/openai/openai-api).

At the most basic level, an API call to an LLM is simple: you send a **prompt**, and you get back a **response**.

```
   PROMPT          --->          LLM          --->          RESPONSE
  (input text)                (the model)                  (output text)
```

That's the whole mechanism. What makes it useful is what you put in the prompt, and most APIs, including the one used in this walkthrough, actually split "the prompt" into two separate input fields rather than one block of text: a **system prompt** and a **user prompt**.

```
PROMPT
 |-- system prompt   (set once, reused every call: role, rules, format)
 |-- user prompt     (changes every call: this call's specific input)
```

**What these two fields are typically used for.** In most applications, the system prompt is written once and sets the model's role, its instructions, and any rules it should follow for the whole task. The user prompt is the specific input for that one call, and it's the piece that changes every time even though the system prompt usually stays fixed. A generic, non-coding example:

- **System prompt:** "You are a die-hard Cardinals fan who believes in heated team rivalries. You are taking a survey."
- **User prompt:** "What's your honest opinion of the Cubs?"

Here's that exact exchange as the simplest possible piece of running code, saved as `code/api_call_ex.py`:

```{literalinclude} code/api_call_ex.py
:language: python
```

Actual output from `code/api_call_ex.py`:

```text
Honest? I can't stand the Cubs. Classic bandwagon city, overhyped ballpark, and way
too many smug fans who act like 2016 erased a century of being annoying. On the
field they're loud and flashy sometimes, but they don't hold a candle to St. Louis'
history and consistency — Cardinals have 11 World Series rings to their three. Love
the rivalry though; nothing fires me up more than trouncing Chicago.
```

**How this maps onto qualitative coding.** The same two-field split applies here, just with a rubric standing in for a rivalry:

- **System prompt:** the rubric, the persona the model should adopt, the output format, and the rules for handling ambiguity, everything that should stay constant across every group you code.
- **User prompt:** the single paragraph about the one group being coded right now, the only thing that changes from call to call.

Section 3 puts that division into actual code.

---

## 3. System Prompt vs. User Prompt for Qualitative Coding

Section 2 laid out the general shape: rubric and persona in the system prompt, the one paragraph being coded in the user prompt. This mirrors how a human coding team actually works: everyone gets the same codebook and training (the system prompt), and then each coder independently looks at one case at a time (the user prompt).

**Code: coding a single file from `data/groups/`**, saved as `code/indonesia_basic_instruct.py`:

```{literalinclude} code/indonesia_basic_instruct.py
:language: python
```

Actual output from `python indonesia_basic_instruct.py`:

```text
Formal integration: state-integrated
Command & control: state-integrated
Compensation/loyalty basis: non-state-parallel
```

Notice what's *not* in this version yet: no explicit rule telling the model to hedge when evidence is genuinely conflicting, no required rationale field, and no structured output format to make each call auditable. In this run, the model landed on "non-state-parallel" for compensation.  Whereas, something is off for this case because of the off-budget business income Section 1 flagged. Without an explicit rule and a required rationale, there's nothing stopping the model from confidently forcing a label as seen in this case. Section 4 enables the model to acknowledge that a case is unclear and provide its reasoning so it can be audited later.

---

## 4. Giving the Model an "Out": Preventing False-Confidence Hallucination

If a rubric label is forced on every dimension, the model will produce one, even for a case, like ABRI's compensation dimension, where a human coder would visibly hesitate. That's a quiet but serious problem: the resulting dataset looks complete and confident, but some fraction of the labels are effectively guesses dressed up as findings. This is the LLM analogue of a human coder writing "unclear, flag for discussion" in the margin instead of forcing a call.

The fix is to build the "out" directly into the rubric and require a justification alongside every label, in structured output so it can be parsed reliably. Saved as `code/indonesia_give_an_out.py`:

```{literalinclude} code/indonesia_give_an_out.py
:language: python
```

Actual output from `python indonesia_give_an_out.py`:

```json
{
  "formal_integration": {
    "label": "state-integrated",
    "rationale": "The paragraph states ABRI/TNI was the 'formally recognized national armed forces, fully embedded in the constitutional chain of command under the Minister of Defense and the President' and describes national garrisons and a central officer academy, indicating formal state integration."
  },
  "command_control": {
    "label": "state-integrated",
    "rationale": "The text explicitly notes ABRI was 'fully embedded in the constitutional chain of command under the Minister of Defense and the President,' which indicates command and control were integrated with state institutions despite the organization's extra-political roles."
  },
  "compensation_basis": {
    "label": "ambiguous",
    "rationale": "The paragraph states officers 'were paid through the state defense budget' but also describes dwifungsi and a 'sprawling network of military-owned businesses and foundations' that produced off-budget income, so the basis of compensation/loyalty is unclear."
  }
}
```

The rationale field matters as much as the label itself, since it's what lets a human reviewer later spot-check why the model called something ambiguous, the same way you'd want a research assistant to show their reasoning rather than hand you a bare checkbox.

### 4.1 The "Out" Is a Routing Decision, Not a Resolution

Adding an "ambiguous" label doesn't make the hard cases go away, it relocates them. Instead of the model quietly guessing on ABRI's compensation dimension, the pipeline now *flags* it. That flag is only useful if something downstream actually reads it: Section 9 is where that flag turns into action (a human looks at exactly the cells marked "ambiguous," not the whole dataset). Giving the model an out and routing ambiguous cases to a human are the same design, described from two ends: the out is what makes routing possible in the first place.

**Walking through the ABRI case end to end.** Feed the model the ABRI paragraph from Section 0. On dimensions 1 and 2 it should land confidently on "state-integrated," since the text gives it clean evidence. On dimension 3 (compensation), a well-calibrated response looks something like:

```json
{"label": "ambiguous", "rationale": "The paragraph states officers 'were paid through the state defense budget' but also describes dwifungsi and a 'sprawling network of military-owned businesses and foundations' that produced off-budget income, so the basis of compensation/loyalty is unclear."}
```

That's the target behavior: a hedge with a *reason attached to specific text*, not a generic "insufficient information." A human adjudicator reading that rationale doesn't have to re-derive the ambiguity from scratch: the model has already done the first pass of the analysis, and the human is checking and finishing it, not starting over.

**Two failure modes worth watching for, in either direction:**

- **Under-hedging:** the model picks a confident label anyway, because "ambiguous" is a less common answer in its training data than a decisive one. This is the failure the whole section exists to prevent, and it's why the rule has to say explicitly *not* to force a label.
- **Over-hedging:** the model reaches for "ambiguous" as a safe default even when the paragraph is actually fairly clear, because hedging feels lower-risk. Watch for this especially once few-shot calibration (Section 5) is added: if the worked example is itself ambiguous, the model can overgeneralize *from* it and start seeing ambiguity everywhere.

Neither failure is visible from the label alone, it only shows up if you (or a human adjudicator) actually read the rationale against the source text. That's the practical argument for requiring rationales at all, beyond just interpretability: without them, over-hedging and under-hedging both look identical to "the pipeline ran successfully."

---

## 5. Calibration by Example: Anchoring the Model on Your Judgment Calls

A rubric alone tells the model *what the categories are*; it doesn't tell the model *how you personally draw the line* on a borderline case. Few-shot calibration closes that gap: you hand-code one example yourself, ideally a genuinely borderline one, and include it in the system prompt, so the model anchors on your standard rather than inventing its own.

This is exactly what a human coding team does in a training session: before independent coding begins, everyone reviews a few worked examples together and discusses *why* the case was coded the way it was.

**Code: adding a worked example to the system prompt**

```python
# <<< FOR A NEW STUDY, EDIT THIS BLOCK: replace the paragraph and "Correct
# coding" below with one hand-coded, genuinely borderline example from your
# own data. This is where your personal judgment calls enter the prompt,
# since the rubric text alone can't convey where you draw the line.
CALIBRATION_EXAMPLE = """
Worked example (for calibration only, not part of the dataset):

Paragraph: "The Republican Guard in Iraq was formally a branch of the national army, \
funded through the defense ministry's budget and holding standard military \
rank. In practice, however, unit commanders were personally appointed by the \
head of state based on kinship and loyalty ties rather than through the \
normal officer promotion system, and several units received supplementary \
payments through informal channels tied directly to the ruling family."

Correct coding:
{
  "formal_integration": {"label": "state-integrated", "rationale": "Formally a branch of the national army, funded through the standard defense budget."},
  "command_control": {"label": "non-state-parallel", "rationale": "Commanders appointed on personal/kinship loyalty rather than through the normal promotion hierarchy."},
  "compensation_basis": {"label": "ambiguous", "rationale": "Base pay follows standard channels, but supplementary informal payments are also described, so neither label fully fits."}
}
"""

SYSTEM_PROMPT_CALIBRATED = SYSTEM_PROMPT + "\n" + CALIBRATION_EXAMPLE
```

Notice the worked example itself has an "ambiguous" call on purpose: calibrating the model on *when* to hedge is just as important as calibrating it on the confident labels. Swap `SYSTEM_PROMPT` for `SYSTEM_PROMPT_CALIBRATED` in the `code_one_file` call from Section 4 to use it. Saved as `code/indonesia_few_shot.py`, running it on `data/groups/indonesia.txt` again gives:

Actual output from `python indonesia_few_shot.py`:

```json
{
  "formal_integration": {
    "label": "state-integrated",
    "rationale": "The paragraph states ABRI/TNI was the formally recognized national armed forces, embedded in the constitutional chain of command under the Minister of Defense and the President and organized as army, navy, and air force branches."
  },
  "command_control": {
    "label": "state-integrated",
    "rationale": "On paper command and control are explicitly under the Minister of Defense and the President and officers held standard military rank, even though the dwifungsi doctrine gave officers concurrent civilian administrative roles."
  },
  "compensation_basis": {
    "label": "ambiguous",
    "rationale": "Officers are described as paid through the state defense budget but the organization also controlled military-owned businesses and off-budget incomes that 'blur' the line between state salary and business-derived income, yielding mixed evidence."
  }
}
```

Same three labels as the uncalibrated run in Section 4. That's a fair result to sit with rather than explain away: calibration didn't change ABRI's coding here, because the uncalibrated model had already landed on the right hedge for this particular paragraph. Calibration's job isn't to change every output, it's to anchor the model on *your* specific line-drawing standard so it doesn't have to guess. Its value shows up most clearly on the cases where the model's default behavior would otherwise diverge from yours, not necessarily on the ones it was already getting right.

### 5.1 Adapting this template to your own study

Everything in Sections 3 through 6 (the client setup, the folder loop, the JSON parsing) is infrastructure that doesn't change from one coding project to the next. Only two things do, and they're marked `<<< FOR A NEW STUDY` in the code above:

1. **`RUBRIC_DIMENSIONS` (Section 4).** Your dimensions and labels replace ABRI/ISI/IRGC's three. This is where the *what* of your codebook lives.
2. **`CALIBRATION_EXAMPLE` (Section 5, here).** One hand-coded, genuinely borderline case from your own data replaces the Republican Guard example. This is where the *how you draw the line* lives, and it should stay a live decision each time you start a new coding project, not get copy-pasted forward from this one.

Everything downstream, Sections 6 through 9, runs unchanged once those two pieces are swapped in.

---

## 6. Scaling Beyond One Input: Looping Over the `data/groups/` Folder

Once the prompt logic is settled, applying it to many items is just a loop. Here, each group produces one row, with the three dimensions as columns: wide format, easy to eyeball, and a natural fit for a small toy dataset like this one. Saved as `code/mercenary_army_project.py`:

```{literalinclude} code/mercenary_army_project.py
:language: python
:lines: 99-162
```

Actual output from `python mercenary_army_project.py`, saved to `coded_groups.csv` (rationale columns omitted here to fit the page, but they're in the actual CSV):

| group | formal_integration_label | command_control_label | compensation_basis_label |
|---|---|---|---|
| indonesia | state-integrated | state-integrated | ambiguous |
| iran | non-state-parallel | non-state-parallel | ambiguous |
| pakistan | state-integrated | non-state-parallel | ambiguous |
| philippines | state-integrated | state-integrated | state-integrated |
| russia | non-state-parallel | non-state-parallel | non-state-parallel |
| sudan | non-state-parallel | non-state-parallel | non-state-parallel |

Worth pausing on two cells here rather than glossing over them: compare this table to the human judgment call in Section 1. For Pakistan, Section 1 flags command and control as the hard dimension; gpt-5-mini instead called it a confident `non-state-parallel`. For Iran, Section 1 flags both command and control and compensation as hard; gpt-5-mini only hedged on compensation, and again called command and control a confident `non-state-parallel`. Indonesia, Philippines, Russia, and Sudan all match the human read. Those two mismatches aren't a rubric problem or a prompt problem, the same calibrated prompt got the other four cases right. They're a model-capability problem, and they're exactly the kind of thing a single coding pass won't catch on its own. Section 8 picks this back up.

The run also wrote a second file, `api_call_log.csv`, with one row of call metadata per API call:

| group | call_timestamp | model_returned | total_tokens |
|---|---|---|---|
| indonesia | 2026-08-31T17:51:36-05:00 | gpt-5-mini-2025-08-07 | 1487 |
| iran | 2026-08-31T17:51:46-05:00 | gpt-5-mini-2025-08-07 | 1635 |
| pakistan | 2026-08-31T17:51:57-05:00 | gpt-5-mini-2025-08-07 | 1868 |
| philippines | 2026-08-31T17:52:11-05:00 | gpt-5-mini-2025-08-07 | 1107 |
| russia | 2026-08-31T17:52:18-05:00 | gpt-5-mini-2025-08-07 | 1452 |
| sudan | 2026-08-31T17:52:29-05:00 | gpt-5-mini-2025-08-07 | 1360 |

`model_returned` is worth calling out on its own: it's the exact dated snapshot that actually served each call (`gpt-5-mini-2025-08-07`), not just the alias (`gpt-5-mini`) requested in the code. That distinction matters for reproducibility, since an alias can point to a different underlying snapshot later even if the code never changes. The log also keeps each call's `response_id` and the API's own server-side timestamp, in case the two ever need to be reconciled.

Running this over the six files in `data/groups/` from Section 0 should produce a six-row CSV, one row per group, three label/rationale column-pairs each, that mirrors the rubric table from Section 0, but now filled in by the model instead of by hand.

---

## 7. Non-Determinism: Why Rerunning Isn't Free

A human coder, asked to code the same paragraph twice, will (mostly) give the same answer both times. An LLM won't necessarily. Even with an identical prompt, sending the exact same paragraph through the model twice can produce different labels or different rationale wording. This isn't a bug, it's a property of how the model samples its output.

This matters for two practical reasons: it means a single coding pass shouldn't be treated as ground truth, and it means "just rerun it" isn't a free diagnostic the way it would be for a deterministic script. For logging prompts and responses at scale, see [Paid LLMs for Text Analysis](/tutorials/nlp/tutorial3).

```python
groups_dir = os.path.join(os.path.dirname(__file__), "../data/groups")
result_1 = code_one_file(os.path.join(groups_dir, "indonesia.txt"))
result_2 = code_one_file(os.path.join(groups_dir, "indonesia.txt"))

for dim in ["formal_integration", "command_control", "compensation_basis"]:
    same = result_1[dim]["label"] == result_2[dim]["label"]
    print(f"{dim}: run1={result_1[dim]['label']!r}, run2={result_2[dim]['label']!r}, match={same}")
```

Example output:

```text
formal_integration: run1='state-integrated', run2='state-integrated', match=True
command_control: run1='state-integrated', run2='state-integrated', match=True
compensation_basis: run1='ambiguous', run2='state-integrated', match=False
```

Notice where the disagreement lands: not on the two dimensions that were clean to begin with, but on compensation, the one dimension that was genuinely hard in Section 1. That's not a coincidence. Non-determinism tends to surface exactly where the underlying call was already borderline.

Setting `temperature=0` and `seed=42` in the API call reduces variation but does not fully eliminate it: it's a partial fix, not a guarantee of identical output. See [OpenAI API](/guides/openai/openai-api) for reproducibility settings. The more robust approach is the one this walkthrough is building toward: treat any single pass as one "coder," and check it against other passes or other models, rather than trusting it in isolation.

---

## 8. Intercoder Reliability: LLM vs. LLM, and LLM vs. Human

The standard way to check whether a coding scheme is being applied consistently is to have more than one coder, human or otherwise, code the same items independently, then measure how often they agree. Here, we use a second, larger model (`gpt-5`) as a second coder, applying the exact same calibrated system prompt to the exact same paragraphs, to see whether a more capable model catches anything the faster `gpt-5-mini` run from Section 6 missed.

```python
def code_one_file_with_model(filepath, model_name, system_prompt):
    with open(filepath, "r") as f:
        paragraph = f.read().strip()

    response = client.chat.completions.create(
        model=model_name,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": paragraph},
        ],
    )
    return json.loads(response.choices[0].message.content)

def code_folder_with_model(folder_path, model_name, system_prompt):
    rows = []
    for filename in sorted(os.listdir(folder_path)):
        if not filename.endswith(".txt"):
            continue
        group_name = filename.replace(".txt", "")
        filepath = os.path.join(folder_path, filename)
        result = code_one_file_with_model(filepath, model_name, system_prompt)
        rows.append({
            "group": group_name,
            "formal_integration_label": result["formal_integration"]["label"],
            "command_control_label": result["command_control"]["label"],
            "compensation_basis_label": result["compensation_basis"]["label"],
        })
    return pd.DataFrame(rows)

# Coder A: gpt-5-mini (from Section 6)
df_a = code_folder_with_model(groups_dir, "gpt-5-mini", SYSTEM_PROMPT_CALIBRATED)

# Coder B: a larger model in the same family
df_b = code_folder_with_model(groups_dir, "gpt-5", SYSTEM_PROMPT_CALIBRATED)

# Merge on group and compare label-by-label
comparison = df_a.merge(df_b, on="group", suffixes=("_a", "_b"))

dimensions = ["formal_integration_label", "command_control_label", "compensation_basis_label"]
for dim in dimensions:
    comparison[f"{dim}_match"] = comparison[f"{dim}_a"] == comparison[f"{dim}_b"]

percent_agreement = comparison[[f"{d}_match" for d in dimensions]].mean()
print(percent_agreement)
```

Example output:

```text
formal_integration_label_match      1.000000
command_control_label_match         0.666667
compensation_basis_label_match      1.000000
dtype: float64
```

The two coders disagree on exactly two cases, and both land on the command and control dimension: `gpt-5` called Pakistan's and Iran's command and control "ambiguous," where `gpt-5-mini` had called both a confident "non-state-parallel." Look back at Section 6: those are the exact two cells flagged as diverging from the human judgment call in Section 1. The larger model isn't just disagreeing for its own sake here, it's landing on the same read a careful human coder made. That's the real case for cross-checking across models, or between a model and a human, instead of trusting a single pass: it's not a formality, it's the mechanism that actually catches cases like these two.

Percent agreement is the simplest diagnostic: the share of items where both coders picked the same label, per dimension. It's worth pairing with Cohen's kappa if you want a measure that accounts for agreement expected by chance (especially relevant here, since "ambiguous" is one of only three possible labels, so raw percent agreement can look artificially high). See [Validation and Rigor](/tutorials/nlp/tutorial5) for Cohen's kappa and a full validation framework; `sklearn.metrics.cohen_kappa_score` computes it directly once you have two aligned label columns.

This same structure (two independent coders, same items, same rubric, compare labels) is exactly how you'd check agreement between an LLM and a human coder instead: just swap `df_b` for a DataFrame of your own hand-coded labels.

---

## 9. What to Do When Coders Disagree: Adjudication, Not Just Diagnosis

Reliability statistics tell you *whether* two coders agree; they don't tell you what to do when they don't. That's a separate, necessary step: without it, "check intercoder reliability" becomes a box-checking exercise rather than something that actually improves the dataset.

This is the other half of the "out" from Section 4.1. There, giving the model permission to say "ambiguous" turned silent guessing into a visible flag. Here, that flag, and any case where two coders land on different labels, is what a human actually spends their time on. The point of both moves together is to make the human's effort go exactly where the model's judgment ran out, instead of asking a person to either re-check everything or trust everything.

A few standard options, in roughly ascending order of effort:

- **Human adjudicates ties.** Wherever the two model coders disagree, a human reviewer looks at the paragraph and the two rationales, and makes the final call. This is usually the right default for a small dataset like this one.
- **Majority vote across three or more coders.** If you're running more than two coders (e.g., two LLMs plus a human, or three LLM passes), take the majority label per dimension, and flag true three-way splits for manual review.
- **Disagreement as a signal to revise the codebook.** If the same dimension keeps producing disagreement across many items, not just one or two idiosyncratic cases, that's evidence the rubric itself may be under-specified for this dimension, not just that the coders are being sloppy. That sends you back to Section 1: refine the category definitions, then re-code.

That's the core loop this walkthrough has traced: a rubric is a starting point, judgment (human or model) fills the gaps the rubric can't anticipate, and disagreement between coders, properly adjudicated, tells you whether the rubric needs to grow to meet the data, or whether the data was just genuinely hard to call. That's the toy-example version of the process; seeing it run on a real research pipeline is a natural next step.

## Next Steps

- **Adapt the template** — swap in your own `RUBRIC_DIMENSIONS` and `CALIBRATION_EXAMPLE` (Sections 4–5), then loop over your corpus (Section 6)
- **Validate before scaling** — build a hand-coded gold standard and measure agreement; see [Validation and Rigor](/tutorials/nlp/tutorial5)
- **Run on KLC** — for larger corpora or batch jobs, see [LLM API Usage on KLC](/services/klc/user-guide/llm-api)
- **Sensitive data** — use [open-source models on KLC](/guides/llm/llm) instead of a paid API when data cannot leave Northwestern systems
- **Paid API basics** — [OpenAI API](/guides/openai/openai-api) and [Paid LLMs for Text Analysis](/tutorials/nlp/tutorial3)
