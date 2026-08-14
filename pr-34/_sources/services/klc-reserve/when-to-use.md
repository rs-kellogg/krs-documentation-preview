# When to Use KLC Reserve

KLC gives you two distinct ways to run computational work. Understanding when to use each saves time and makes research more reproducible.

## Two Ways to Run on KLC

**Option 1 — Direct login (interactive)**

You SSH, use OnDemand, VS Code, or FastX to log into a KLC node (for example, `klc0305.quest.northwestern.edu`) and run commands at the prompt. Your process competes for CPU and memory with every other user on that node.

**Option 2 — SLURM batch job (scheduled)**

You write a shell script describing what your job needs (cores, memory, time, GPUs), submit it with `sbatch`, and the SLURM scheduler places it on KLC Reserve nodes when resources are available. SLURM reserves those resources *exclusively* for your job while it runs.

Both options use the same Kellogg file systems and software modules. The difference is *how resources are allocated* and *how you interact with the job*.

---

## How to Think About the Choice

| | Direct Login | SLURM Batch (KLC Reserve) |
|---|---|---|
| **Resource allocation** | Shared with all users on the node | Dedicated; no other jobs use your reserved cores/RAM |
| **Core limit** | 24 cores at normal priority per user, across all KLC nodes | Request up to the node's full capacity for a single job |
| **Connection required** | Must remain connected (or use `tmux`/FastX) | Runs independently; you can log out |
| **Output visibility** | Real time in the terminal | Written to a log file; inspect with `cat` or `tail -f` |
| **Reproducibility** | Steps in your head or a scratch session | Submission script documents every command, module, and parameter |
| **Running many jobs** | One at a time manually | Submit dozens or hundreds at once with job arrays |
| **Scheduling** | Starts immediately; resources not guaranteed | May wait in queue; SLURM manages fairness |
| **GPUs** | Not available on login nodes | Available via `--partition=kellogg` and `--gres=gpu:...` |
| **Best for** | Development, debugging, exploration | Production runs, overnight jobs, GPUs, parallel pipelines |

Still unsure? Contact [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu).

---

## When Direct Login Is the Right Choice

Stick with direct login when you are:

- **Writing and testing code** — iterate quickly, see errors immediately, and edit in place
- **Exploring data interactively** — Jupyter notebooks, quick plots, sanity checks
- **Running a short job** (under ~30 minutes) that you want to watch run
- **Working in an IDE** — VS Code Remote SSH and similar tools connect directly to the node

```{tip}
For interactive work, open a `tmux` session first so your work survives a dropped connection. See [Using tmux](/services/klc/user-guide/klc-tmux).
```

---

## When SLURM Is the Right Choice

Move to KLC Reserve when:

- **Your job runs for hours or overnight** — SLURM runs the job whether you are logged in or not
- **You need more than 24 cores** — direct login enforces a 24-core soft limit across all KLC nodes; Reserve lets you request up to full node capacity for one job
- **You need guaranteed memory** — on a busy login node, another user's process can consume RAM you counted on; SLURM reserves what you request
- **You want to run the same script many times** with different inputs — job arrays fan out one script into many independent tasks
- **Reproducibility matters** — a SLURM script is a complete record of how a result was produced
- **You need GPU resources** — GPUs are available only through SLURM on the `kellogg` partition. See [GPU Jobs](gpu-jobs)

The sections below walk through common Reserve scenarios in more detail.

---

## You Need a GPU

**Symptom:** Training a classifier, fine-tuning an LLM, or running GPU-accelerated inference; login nodes have no GPUs.

**Why login nodes fall short:** GPU hardware exists only on Reserve compute nodes. Running on CPU works for small models but becomes impractical for modern deep learning workloads.

**What to request:** Submit to `--partition=kellogg` with `--gres=gpu:1` (or a specific card if memory requirements demand it).

**Example:** A marketing researcher fine-tuning a BERT model on proprietary survey text uses an A100 via `--gres=gpu:a100:1` and a four-hour wall time.

**How-to:** [GPU Jobs](gpu-jobs) · [GPU Concepts and Options](/services/klc-reserve/gpu-concepts)

When the workflow is proven and you need more GPUs than Kellogg Reserve can provide, scale out to Quest General Access on the `gengpu` partition. See [GPU Concepts and Options](/services/klc-reserve/gpu-concepts).

---

## Your Job Needs More CPU or Memory Than a Login Node Can Spare

**Symptom:** Analysis needs 32+ cores or hundreds of GB of RAM; other users on the node compete for the same resources.

**Why login nodes fall short:** Each user is limited to 24 cores at normal priority across all KLC nodes, and memory is shared — another user's process can consume RAM you expected to use.

**What to request:** A batch job with `--ntasks` up to the node capacity and `--mem` set to your expected peak plus headroom (~110%).

**Example:** A finance researcher bootstraps a simulation across 48 cores on a high-memory Reserve node instead of throttling to the 24-core login limit.

**How-to:** [Submitting SLURM Jobs](slurm-jobs)

---

## Your Job Takes Hours or Days

**Symptom:** Overnight econometric estimation, large-scale data merge, or model training that exceeds a work session.

**Why login nodes fall short:** SSH sessions drop; login nodes may be restarted; long jobs on shared nodes affect other users.

**What to request:** A batch job with a wall time covering the full expected runtime. Log out after submitting — SLURM keeps the job running.

**Example:** A PhD student submits a Stata-free Python pipeline at 6 PM with `--time=12:00:00` and collects output the next morning from the log file.

**How-to:** [Submitting SLURM Jobs](slurm-jobs) · [Using tmux](/services/klc/user-guide/klc-tmux) for interactive work that must survive disconnects on login nodes

---

## You Need Reproducible, Time-Stamped Compute Environments

**Symptom:** A coauthor, reviewer, or future you must rerun the exact analysis with the same software versions and resource requests.

**Why login nodes fall short:** Interactive sessions depend on commands typed at the prompt; module loads and working directories are easy to omit from notes.

**What to request:** A SLURM script that records `#SBATCH` resources, every `module load`, environment activation, and the exact command line.

**Example:** A research team archives `analysis_job.sh` alongside paper code so replication uses `sbatch analysis_job.sh` with identical inputs.

**How-to:** [Submitting SLURM Jobs](slurm-jobs)

---

## You Need to Run Many Jobs in Parallel

**Symptom:** Same pipeline applied to hundreds of firms, years, or simulation draws.

**Why login nodes fall short:** Running dozens of processes manually on a shared node is slow, hard to monitor, and competes with other users.

**What to request:** A SLURM **job array** — one script, many tasks indexed by `$SLURM_ARRAY_TASK_ID`.

**Example:** A researcher classifies 200 10-K filings in parallel with `#SBATCH --array=1-200`, each task reading one file ID from the array index.

**How-to:** [Submitting SLURM Jobs](slurm-jobs) (Job Arrays section)

---

## Related Pages

- [Kellogg Linux Cluster Reserve](/services/klc-reserve/klc-reserve) — overview and first-job path
- [Submitting SLURM Jobs](slurm-jobs) — batch scripts and job arrays
- [GPU Jobs](gpu-jobs) — GPU requests on the `kellogg` partition
- [Launching Jobs on KLC](/services/klc/user-guide/klc-software) — modules and environments on login nodes
