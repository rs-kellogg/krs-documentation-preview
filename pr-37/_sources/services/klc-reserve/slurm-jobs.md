# Submitting SLURM Jobs

KLC Reserve jobs run on the **`kellogg` SLURM partition**. You submit a shell script that declares the resources your job needs; SLURM schedules the job and runs it on dedicated nodes whether you remain logged in or not. This page covers how to write, submit, monitor, and tune batch and interactive SLURM jobs.

For the decision between interactive login work and scheduled jobs, see [When to Use KLC Reserve](when-to-use). For GPU-specific requests, see [GPU Jobs](gpu-jobs). For comprehensive SLURM reference, see the [Quest SLURM documentation](https://rcdsdocs.it.northwestern.edu/systems/quest/user-guide/slurm/slurm.html).

## Prerequisites

- A KLC account and an active session on any KLC node
- A Kellogg SLURM account with access to the `kellogg` partition (verify with `groups`)
- Job scripts and output stored under `/kellogg/proj/<your-netid>/`, not your 80 GB home directory

## A Minimal Batch Script

Save this as `myjob.sh`:

```bash
#!/bin/bash
#SBATCH --account=kellogg                    ## Kellogg SLURM account
#SBATCH --partition=kellogg                  ## Kellogg Reserve partition
#SBATCH --job-name=my-analysis
#SBATCH --nodes=1
#SBATCH --ntasks=8                           ## CPU cores
#SBATCH --mem=64G                            ## RAM; request ~110% of expected peak use
#SBATCH --time=04:00:00                      ## Wall time limit HH:MM:SS
#SBATCH --output=logs/slurm-%j.out           ## stdout/stderr; %j = job ID

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

SLURM returns a job ID immediately and your job enters the queue:

```
Submitted batch job 1234567
```

## Partition Limits (`kellogg`)

| Policy | Value |
|---|---|
| `--account` | `kellogg` |
| Maximum wall time | 48 hours per job |
| Concurrent job limit | None |
| Default memory | 3 GB per core (if `--mem` is not specified) |

Request `--mem` explicitly when your job needs more than the per-core default.

## Key `#SBATCH` Options

| Option | What it controls |
|---|---|
| `--account` | SLURM account to charge; required |
| `--partition` | Node pool; use `kellogg` for KLC Reserve |
| `--nodes=1` | Physical machines; keep at 1 unless using MPI |
| `--ntasks` | CPU cores; increase only if your code parallelizes |
| `--mem` | RAM per node |
| `--time` | Maximum wall time; job is killed if it exceeds this |
| `--output` | File for stdout and stderr (`%j` = job ID) |
| `--gres=gpu:1` | Request one GPU (for GPU jobs; see [GPU Jobs](gpu-jobs)) |

```{warning}
`--ntasks` without `--nodes=1` can spread cores across multiple machines. Unless your code uses MPI, always pair `--ntasks` with `--nodes=1`.
```

```{note}
Run `groups` after logging into any KLC node to see the SLURM account names you belong to. Contact [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) if your jobs fail to submit.
```

## Interactive Sessions

For interactive work on a reserved node — useful for debugging or testing resource-intensive steps — use `salloc`:

```bash
salloc --account=kellogg \
       --partition=kellogg \
       --nodes=1 --ntasks=4 --mem=32G \
       --time=01:00:00
```

Once the allocation is granted, SLURM sets `$SLURM_NODELIST` and similar environment variables in your shell. To open an interactive shell on the allocated compute node, run:

```bash
srun --pty bash
```

This launches a bash session directly on the assigned node. When you are done, type `exit` to leave the `srun` session, then `exit` again to release the `salloc` allocation.

You can also use `srun` to run a single command on the allocated node without opening a full shell:

```bash
srun python my_script.py
```

To request a GPU interactively, add `--gres=gpu:1` to your `salloc` command:

```bash
salloc --account=kellogg \
       --partition=kellogg \
       --nodes=1 --ntasks=4 --mem=32G \
       --gres=gpu:1 --time=01:00:00
```

Then connect to the node and verify the GPU is visible:

```bash
srun --pty bash
nvidia-smi
```

For GPU setup and batch examples, see [GPU Jobs](gpu-jobs).

### Using `srun` Directly (One-Step Alternative)

You can skip `salloc` entirely and let `srun` handle both allocation and execution in a single command:

```bash
srun --account=kellogg \
     --partition=kellogg \
     --nodes=1 --ntasks=4 --mem=32G \
     --time=01:00:00 \
     --pty bash
```

For a GPU session:

```bash
srun --account=kellogg \
     --partition=kellogg \
     --nodes=1 --ntasks=4 --mem=32G \
     --gres=gpu:1 --time=01:00:00 \
     --pty bash
```

This is the simpler option for a quick one-off session. The tradeoff is that each `srun` call competes for resources independently — if you need to run several sequential steps and want them all to share the same allocation without requeuing, use `salloc` + `srun` instead.

## Job Arrays

Run the same script on many inputs with a **job array**. Each task receives a unique index in `$SLURM_ARRAY_TASK_ID`:

```bash
#!/bin/bash
#SBATCH --account=kellogg
#SBATCH --partition=kellogg
#SBATCH --job-name=batch-analysis
#SBATCH --array=1-50                      ## Tasks indexed 1 through 50
#SBATCH --nodes=1
#SBATCH --ntasks=4
#SBATCH --mem=16G
#SBATCH --time=01:00:00
#SBATCH --output=logs/job-%A_%a.out       ## %A = array job ID, %a = task index

module purge
module use --append /kellogg/software/Modules/modulefiles
module load mamba/latest
source activate /kellogg/proj/<your-netid>/envs/my-env

INPUT_FILE=/kellogg/proj/<your-netid>/data/input_${SLURM_ARRAY_TASK_ID}.csv

python process.py --input $INPUT_FILE \
                  --output /kellogg/proj/<your-netid>/results/output_${SLURM_ARRAY_TASK_ID}.csv
```

All tasks run in parallel subject to partition capacity.

## Monitoring and Cancelling Jobs

```bash
# Queued and running jobs
squeue -u $USER

# Expected start time for a pending job
squeue -j <job-id> --start

# Detailed status
checkjob <job-id>

# Resource efficiency after completion
seff <job-id>

# Cancel a job
scancel <job-id>
```

`seff` reports CPU efficiency and actual vs. requested memory — use it after each run to tighten your resource requests and reduce queue wait time.

## Common Pitfalls

| Symptom | Likely cause | What to do |
|---|---|---|
| `Invalid account` | Wrong `--account` or no partition access | Run `groups`; contact [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) |
| Job stays `PD` (pending) | Cluster busy or request too large | Check `squeue -j <job-id> --start`; reduce `--mem`, `--ntasks`, or `--time` |
| Job fails immediately | Missing `module load` or wrong conda path | Test the exact commands interactively first |
| Job ends with `OUT_OF_MEMORY` | `--mem` too low | Increase `--mem`; use `seff` on a failed job to see actual use |
| Job ends with `TIMEOUT` | `--time` too low | Increase `--time` and resubmit |
| Empty or missing output file | Wrong `--output` path | Create the log directory before submitting; use an absolute path under `/kellogg/proj/` |
| `--ntasks` spreads across nodes | Missing `--nodes=1` | Always add `--nodes=1` for non-MPI jobs |
| GPU not visible in Python | CUDA environment not loaded | Load the correct CUDA module; see [GPU Jobs](gpu-jobs) |

## Practical Workflow

1. **Develop interactively** on a login node with a small sample. Fix bugs and tune parameters.
2. **Capture commands** in a SLURM script — same `module load` steps and working directory.
3. **Submit one test job** on representative data; confirm output and runtime.
4. **Scale** with a job array if you have many inputs.
5. **Tune resources** with `seff` before the next large run.

## Further Reading

- [Quest SLURM documentation](https://rcdsdocs.it.northwestern.edu/systems/quest/user-guide/slurm/slurm.html) — comprehensive `#SBATCH` reference
- [When to Use KLC Reserve](when-to-use) — when to use SLURM vs. direct login
- [Launching Jobs on KLC](/services/klc/user-guide/klc-software) — modules and environment setup
- [Using tmux](/services/klc/user-guide/klc-tmux) — keeping interactive sessions alive on login nodes
- [GPU Jobs](gpu-jobs) — GPU requests on the `kellogg` partition
- [KLC Reserve overview](/services/klc-reserve/klc-reserve) — available hardware
