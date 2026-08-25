# When to Use KLC Reserve

KLC gives you two distinct ways to run computational work. Both paths support long-running, reproducible jobs — the difference is **how resources are allocated** (shared vs exclusive) and **how you launch the work** (at the prompt vs `sbatch`).

## Two Ways to Run on KLC

**Option 1 — Direct login (KLC main, interactive)**

You SSH, use OnDemand, VS Code, or FastX to log into a KLC node (for example, `klc0305.quest.northwestern.edu`) and run commands at the prompt. Your process competes for CPU and memory with every other user on that node.

**Option 2 — SLURM batch job (KLC Reserve, scheduled)**

You write a shell script describing what your job needs (cores, memory, time, GPUs), submit it with `sbatch`, and the SLURM scheduler places it on KLC Reserve nodes when resources are available. SLURM reserves those resources *exclusively* for your job while it runs.

Both options use the same Kellogg file systems and software modules. On KLC main, a versioned script, [conda/mamba environment](/services/klc/user-guide/klc-conda), Python `logging`, and `tmux` plus `tee` give you the same kind of durable log and reproducible record that SLURM `--output` provides on Reserve. See [Launching Jobs on KLC](/services/klc/user-guide/klc-software) for how to capture logs on interactive runs.

---

## How to Think About the Choice

| | Direct Login (KLC main) | SLURM Batch (KLC Reserve) |
|---|---|---|
| **Resource allocation** | Shared with all users on the node | Dedicated; no other jobs use your reserved cores/RAM |
| **Core limit** | 24 cores at normal priority per user, across all KLC nodes | Request up to the node's full capacity for a single job |
| **Connection required** | Must remain connected (or use `tmux`/FastX) | Runs independently; you can log out |
| **Output visibility** | Terminal in real time; save to a log file with `tee` | Written to a log file via `#SBATCH --output`; inspect with `cat` or `tail -f` |
| **Reproducibility** | Script, conda env, and log files on either path | SLURM script additionally records resource requests (`#SBATCH` directives) |
| **Running many jobs** | One at a time manually | Submit dozens or hundreds at once with job arrays |
| **Scheduling** | Starts immediately; resources not guaranteed | May wait in queue; SLURM manages fairness |
| **GPUs** | Not available on login nodes | Available via `--partition=kellogg` and `--gres=gpu:...` |
| **Best for** | Development, debugging, and logged production runs within the 24-core limit | Dedicated resources, GPUs, job arrays, and exclusive memory |

Still unsure? Contact [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu).

---

## When Direct Login Is the Right Choice

Stick with direct login on KLC main when you are:

- **Writing and testing code** — iterate quickly, see errors immediately, and edit in place
- **Exploring data interactively** — Jupyter notebooks, quick plots, sanity checks
- **Running a script for hours** — use `tmux` so the job survives a disconnect and `tee` to save a log file; see [Launching Jobs on KLC](/services/klc/user-guide/klc-software)
- **Working in an IDE** — VS Code Remote SSH and similar tools connect directly to the node

```{tip}
For any job that should keep running after you disconnect, open a `tmux` session first and redirect output to a log file. See [Using tmux](/services/klc/user-guide/klc-tmux) and [Launching Jobs on KLC](/services/klc/user-guide/klc-software).
```

---

## When SLURM Is the Right Choice

Move to KLC Reserve when:

- **You need more than 24 cores** — direct login enforces a 24-core soft limit across all KLC nodes; Reserve lets you request up to full node capacity for one job
- **You need guaranteed memory** — on a busy login node, another user's process can consume RAM you counted on; SLURM reserves what you request
- **You want to run the same script many times** with different inputs — job arrays fan out one script into many independent tasks
- **You need GPU resources** — GPUs are available only through SLURM on the `kellogg` partition. See [GPU Jobs](gpu-jobs)

The sections below walk through common Reserve scenarios in more detail.

---

## You Need a GPU

**Symptom:** Training a classifier, fine-tuning an LLM, or running GPU-accelerated inference; login nodes have no GPUs.

**Why KLC main falls short:** GPU hardware exists only on Reserve compute nodes. Running on CPU works for small models but becomes impractical for modern deep learning workloads.

**What to request:** Submit to `--partition=kellogg` with `--gres=gpu:1` (or a specific card if memory requirements demand it).

**Example:** A marketing researcher fine-tuning a BERT model on proprietary survey text uses an A100 via `--gres=gpu:a100:1` and a four-hour wall time.

**How-to:** [GPU Jobs](gpu-jobs) · [GPU Concepts and Options](/services/klc-reserve/gpu-concepts)

When the workflow is proven and you need more GPUs than Kellogg Reserve can provide, scale out to Quest General Access on the `gengpu` partition. See [GPU Concepts and Options](/services/klc-reserve/gpu-concepts).

---

## Your Job Needs More CPU or Memory Than a Login Node Can Spare

**Symptom:** Analysis needs 32+ cores or hundreds of GB of RAM; other users on the node compete for the same resources.

**Why KLC main falls short:** Each user is limited to 24 cores at normal priority across all KLC nodes, and memory is shared — another user's process can consume RAM you expected to use.

**What to request:** A batch job with `--ntasks` up to the node capacity and `--mem` set to your expected peak plus headroom (~110%).

**Example:** A finance researcher bootstraps a simulation across 48 cores on a high-memory Reserve node instead of throttling to the 24-core login limit.

**How-to:** [Submitting SLURM Jobs](slurm-jobs) · [High-Memory Jobs](highmem-jobs)

---

## Your Job Uses Many Cores for Hours on a Shared Node

**Symptom:** Overnight econometric estimation, large-scale data merge, or model training that runs for many hours while using a large share of the node's CPU or memory.

**Why Reserve may be a better fit:** KLC main supports long-running scripts with `tmux` and log files — see [Launching Jobs on KLC](/services/klc/user-guide/klc-software). Reserve is the right choice when you need **exclusive** cores or memory so other users are not competing for the same resources. Node maintenance reboots are uncommon; use `tmux` and `tee` so a dropped SSH connection does not interrupt your work.

**What to request:** A batch job with a wall time covering the full expected runtime. Log out after submitting — SLURM keeps the job running and writes output to your `#SBATCH --output` file.

**Example:** A PhD student submits a Python pipeline at 6 PM with `--time=12:00:00` and collects output the next morning from the log file.

**How-to:** [Submitting SLURM Jobs](slurm-jobs) · [Launching Jobs on KLC](/services/klc/user-guide/klc-software) for the interactive equivalent (script, `tmux`, and `tee`)

---

## You Need Reproducible, Time-Stamped Compute Environments

**Symptom:** A coauthor, reviewer, or future you must rerun the exact analysis with the same software versions and resource requests.

**On KLC main:** Use a version-controlled script, a pinned [conda/mamba environment](/services/klc/user-guide/klc-conda), Python `logging` for timestamps and progress, and `tee` to capture stdout and stderr. See [Launching Jobs on KLC](/services/klc/user-guide/klc-software).

**On KLC Reserve:** A SLURM script additionally records `#SBATCH` resource requests, every `module load`, environment activation, and the exact command line in one file.

**Example:** A research team archives `analysis_job.sh` alongside paper code so replication uses `sbatch analysis_job.sh` with identical inputs. The same script can be run interactively on KLC main with logging and `tee` when Reserve resources are not required.

**How-to:** [Launching Jobs on KLC](/services/klc/user-guide/klc-software) · [Submitting SLURM Jobs](slurm-jobs)

---

## You Need to Run Many Jobs in Parallel

**Symptom:** Same pipeline applied to hundreds of firms, years, or simulation draws.

**Why KLC main falls short:** Running dozens of processes manually on a shared node is slow, hard to monitor, and competes with other users.

**What to request:** A SLURM **job array** — one script, many tasks indexed by `$SLURM_ARRAY_TASK_ID`.

**Example:** A researcher classifies 200 10-K filings in parallel with `#SBATCH --array=1-200`, each task reading one file ID from the array index.

**How-to:** [Submitting SLURM Jobs](slurm-jobs) (Job Arrays section)

---

## Related Pages

- [Kellogg Linux Cluster Reserve](/services/klc-reserve/klc-reserve) — overview and first-job path
- [Submitting SLURM Jobs](slurm-jobs) — batch scripts and job arrays
- [GPU Jobs](gpu-jobs) — GPU requests on the `kellogg` partition
- [High-Memory Jobs](highmem-jobs) — case studies for high-memory workloads
- [Launching Jobs on KLC](/services/klc/user-guide/klc-software) — scripts, logging, and `tmux` on KLC main
