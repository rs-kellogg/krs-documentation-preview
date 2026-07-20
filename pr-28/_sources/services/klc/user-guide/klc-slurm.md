# Interactive Jobs vs. SLURM Batch Jobs

KLC gives you two distinct ways to run computational work, and understanding when to use each will save you time and make your research more reproducible.

## Two Ways to Run on KLC

**Option 1 — Direct login (interactive)**

You SSH or use FastX to log directly into a KLC node (e.g., `klc0305.quest.northwestern.edu`) and run commands at the prompt. Your process competes for CPU and memory with every other user currently logged into that same node.

**Option 2 — SLURM batch job (scheduled)**

You write a shell script describing what your job needs (cores, memory, time), submit it with `sbatch`, and the SLURM scheduler places it on the Kellogg partition nodes when the requested resources are available. SLURM reserves those resources *exclusively* for your job while it runs.

Both options give you access to the same Kellogg nodes and the same software. The difference is in *how resources are allocated* and *how you interact with the job*.

---

## How to Think About the Choice

The table below captures the most important factors:

| | Direct Login | SLURM Batch |
|---|---|---|
| **Resource allocation** | Shared with all users on the node | Dedicated; no other jobs use your reserved cores/RAM |
| **Core limit** | 24 cores at normal priority per user, across all KLC nodes | Governed by your allocation; you can request up to the node's full capacity |
| **Connection required** | Must remain connected (or use `tmux`/FastX) | Runs independently; you can log out |
| **Output visibility** | You see it in real time | Written to a log file; inspect with `cat` or `tail -f` |
| **Reproducibility** | Steps are in your head or a scratch session | Submission script documents every command, module, and parameter |
| **Running many jobs** | One at a time | Submit dozens or hundreds at once with job arrays |
| **Scheduling** | Starts immediately, but resources are not guaranteed | May wait in queue; SLURM manages fairness |
| **Best for** | Development, debugging, exploration | Production runs, overnight jobs, parallel pipelines |

---

## When Direct Login Is the Right Choice

Stick with direct login when you are:

- **Writing and testing code.** You need to iterate quickly, see errors immediately, and make edits. The overhead of writing a SLURM script slows you down.
- **Exploring data interactively.** Launching a Jupyter notebook, inspecting a dataset, or running a quick visualization.
- **Running a short job** (under ~30 minutes) that you want to watch run.
- **Working in an IDE.** VS Code Remote SSH and other editors connect directly to the node; they are not designed to submit jobs to a scheduler.

```{tip}
Even for interactive work, open a `tmux` session first. This keeps your session alive if your connection drops. See [Using tmux](klc-tmux) for a quick start.
```

---

## When SLURM Is the Right Choice

Move to SLURM when:

- **Your job runs for hours or overnight.** SLURM runs the job whether you are logged in or not. You do not need `tmux` or an open connection.
- **You need more than 24 cores.** Direct login enforces a 24-core soft limit for all your processes combined across all KLC nodes. SLURM lets you request up to the full node capacity (52 or 64 cores) *for a single job*.
- **You need guaranteed memory.** On a busy node, another user's process can consume the RAM you were counting on. SLURM reserves the memory you request.
- **You want to run the same script many times** with different inputs. SLURM job arrays let you submit a single script that fans out into dozens of independent jobs.
- **Reproducibility matters.** A SLURM script is a complete, self-contained record of exactly how a result was produced — what software, what parameters, what resources. It is the most reliable way to make your analysis reproducible.
- **You need GPU resources.** GPUs are only accessible through SLURM (via the `gengpu` partition). See [Using GPUs on Quest and KLC](klc-gpu).

---

## Submitting a Job to the Kellogg Partition

The Kellogg partition gives KRS researchers priority access to the KLC nodes through SLURM.

```{note}
Contact [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) to confirm your Kellogg SLURM account name and verify that you have access to the Kellogg partition. Run `groups` after logging into any KLC node to see the allocation names you belong to.
```

### A Minimal Submission Script

Save this as `myjob.sh`:

```bash
#!/bin/bash
#SBATCH --account=<your-kellogg-account>  ## Your Kellogg SLURM account (e.g., kellogg or b1234)
#SBATCH --partition=kellogg               ## The Kellogg priority partition
#SBATCH --job-name=my-analysis
#SBATCH --nodes=1
#SBATCH --ntasks=8                        ## Number of CPU cores
#SBATCH --mem=64G                         ## RAM (separate from GPU memory)
#SBATCH --time=04:00:00                   ## Wall time limit HH:MM:SS
#SBATCH --output=logs/slurm-%j.out        ## stdout/stderr; %j = job ID

## Load software
module purge
module use --append /kellogg/software/Modules/modulefiles
module load mamba/latest
source activate /kellogg/proj/<your-netid>/envs/my-env

## Run your code
cd /kellogg/proj/<your-netid>/project
python analysis.py
```

Submit it:

```bash
sbatch myjob.sh
```

SLURM returns a job ID immediately:

```
Submitted batch job 1234567
```

Your job enters the queue and starts as soon as the requested resources are free.

### Key `#SBATCH` Options

| Option | What it controls |
|---|---|
| `--account` | Which SLURM account to charge; required |
| `--partition` | Which set of nodes to target; use `kellogg` for KLC nodes |
| `--nodes=1` | Number of physical machines; keep this at 1 unless using MPI |
| `--ntasks` | Number of CPU cores; only increase if your code actually parallelizes |
| `--mem` | RAM per node; request ~110% of what you expect to use |
| `--time` | Maximum wall time; your job is killed if it exceeds this |
| `--output` | File where stdout and stderr are written (`%j` = job ID) |

```{warning}
`--ntasks` without `--nodes=1` can spread your cores across multiple machines. Unless your code uses MPI, always pair `--ntasks` with `--nodes=1`.
```

---

## Running Many Similar Jobs: Job Arrays

If you need to run the same analysis on 50 different input files, a **job array** submits all 50 as a single SLURM submission. Each task gets a unique index via `$SLURM_ARRAY_TASK_ID`.

```bash
#!/bin/bash
#SBATCH --account=<your-kellogg-account>
#SBATCH --partition=kellogg
#SBATCH --job-name=batch-analysis
#SBATCH --array=1-50                      ## Runs 50 tasks, indexed 1 through 50
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --mem=16G
#SBATCH --time=01:00:00
#SBATCH --output=logs/job-%A_%a.out       ## %A = array job ID, %a = task index

module purge
module use --append /kellogg/software/Modules/modulefiles
module load mamba/latest
source activate /kellogg/proj/<your-netid>/envs/my-env

## Use the task index to select the input file
INPUT_FILE=/kellogg/proj/<your-netid>/data/input_${SLURM_ARRAY_TASK_ID}.csv

python process.py --input $INPUT_FILE \
                  --output /kellogg/proj/<your-netid>/results/output_${SLURM_ARRAY_TASK_ID}.csv
```

All 50 tasks run in parallel (subject to resource availability) without any extra scripting on your part.

---

## Monitoring Your Jobs

Once a job is submitted, use these commands to check on it:

```bash
# See all your queued and running jobs
squeue -u $USER

# See expected start time for a pending job
squeue -j <job-id> --start

# Detailed status of a specific job
checkjob <job-id>

# Check resource usage after a job finishes
seff <job-id>

# Cancel a job
scancel <job-id>
```

`seff` is especially useful for tuning future submissions — it reports CPU efficiency and actual vs. requested memory, helping you request resources more accurately next time.

---

## A Practical Workflow

1. **Develop and test interactively.** Log in, load your environment, and run your code on a small sample. Fix bugs, tune parameters.
2. **Write a SLURM script.** Capture the exact commands and `module load` steps from step 1. Start with conservative resource requests.
3. **Submit a test job.** Run one job on a representative input to confirm it completes and produces correct output.
4. **Scale up.** Once confident, use a job array to process all your data.
5. **Check efficiency.** Use `seff` after completion and tighten your resource requests for the next run.

---

## Further Reading

- [Quest SLURM documentation](https://rcdsdocs.it.northwestern.edu/systems/quest/user-guide/slurm/slurm.html) — comprehensive reference for all `#SBATCH` options, partitions, fairshare, interactive jobs
- [Launching Jobs on KLC](klc-software) — loading modules and environment setup
- [Using tmux](klc-tmux) — keeping interactive sessions alive
- [Using GPUs on Quest and KLC](klc-gpu) — GPU jobs via the `gengpu` partition
