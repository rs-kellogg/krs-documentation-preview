# Scaling on High-Core Nodes

Parallel CPU jobs on the Emerald Rapids nodes (`qnode4043` and `qnode4044`) finish faster when the SLURM request matches how the program uses cores. The same 128 ordinary-least-squares (OLS) bootstrap replicates can run as threads inside one process, as worker processes on one node, or as a SLURM job array of independent tasks. Node limits and the `--constraint=quest14` feature are in [High-Core CPU Nodes](high-core-cpu-nodes).

Run the jobs below on the cluster, then bring the timing files back. The [Key Takeaways](high-core-scaling-takeaways) section is reserved for those measurements.

## Choose How the Cores Are Used

| Mode | What runs | SLURM request | Thread variables |
|---|---|---|---|
| Threads | One process. BLAS and OpenMP inside that process use the cores. | `--nodes=1 --ntasks=1 --cpus-per-task=N --constraint=quest14` | All four set to `N` |
| Workers | `N` processes from a Python `multiprocessing` pool or R `parallel::mclapply`. | `--nodes=1 --ntasks=1 --cpus-per-task=N --constraint=quest14` | All four set to `1` |
| Job array | One independent task per replicate, scheduled by SLURM. | `--array=1-128 --nodes=1 --ntasks=1 --cpus-per-task=1` | All four set to `1` |

Threads and workers request cores the same way. They differ in how many processes the program starts and in the thread variables. A pool or `mclapply` is still one program: SLURM runs the batch script once. `--ntasks=N` reserves tasks for `srun` to launch. It does not hand those cores to a pool started by that single script. Grant the cores with `--cpus-per-task`.

Leave `--constraint=quest14` off the job array. A one-core task does not belong on the two 128-core nodes.

```{warning}
Python's `threading` module does not speed a pure-Python loop, because of the global interpreter lock (GIL). Base R has no general user-level threading API. In this study the thread runs are the BLAS and OpenMP work inside `numpy.linalg.lstsq` and `lm.fit`.
```

## Set the Thread Variables in the Shell

Export these four variables before `python` or `Rscript` starts. Put the exports after `mamba activate`. An environment activation hook can replace a value exported earlier in the script.

| Variable | Library that reads it |
|---|---|
| `OMP_NUM_THREADS` | OpenMP |
| `MKL_NUM_THREADS` | MKL |
| `OPENBLAS_NUM_THREADS` | OpenBLAS |
| `NUMEXPR_NUM_THREADS` | numexpr |

Set all four on every job. An OpenBLAS build ignores `MKL_NUM_THREADS`. An MKL build ignores `OPENBLAS_NUM_THREADS`. numexpr starts its own pool when a later line of the program uses it.

For a thread run, set each variable to `$SLURM_CPUS_PER_TASK`. For a worker run or a job-array task, set each variable to `1`. Each worker otherwise opens its own BLAS pool, and `N` workers times `N` threads ask for `N × N` threads on `N` cores.

```{warning}
These scripts build the random matrix without a matrix product, then the worker modes fork. Each worker initializes BLAS after the fork. A BLAS call in the parent before `Pool` or `mclapply`, with a thread count above 1, can deadlock the job.
```

## The Scaling Study

Each run solves the same problem: 128 bootstrap replicates of an OLS fit. The design matrix is `n_obs = 20000` by `n_pred = 500` (80 MB as float64), drawn once from a fixed seed. Wall time is the time to finish the replicates. Building the matrix sits outside the timer.

The core counts are 1, 2, 4, 8, 16, 32, 64, and 128, for threads and for workers, in Python and in R. One extra job on each language runs 16 workers with the thread variables set to 16, so the allocation is 16 cores and the libraries ask for 256 threads. One job array on each language runs 128 tasks, one replicate each, with the thread variables set to 1.

If the 1-core run finishes in only a few seconds, increase `n_obs` in both scripts and resubmit the whole grid at that new size. Keep the size fixed across languages and modes.

Every job writes one CSV row:

`language,mode,cpus,workers,threads,elapsed_seconds,slurm_job_id,array_task_id`

For a thread or worker job, `elapsed_seconds` is the time for all 128 replicates. For an array task, `elapsed_seconds` is the time for that one replicate. The array number to compare against a single job is the clock span from the earliest task start to the latest task end, from `sacct`, not the sum of the task rows.

## Python Script

Save this as `/kellogg/proj/<your-netid>/scaling/bootstrap_scale.py`. The environment needs `numpy` and the base library `multiprocessing`.

```python
#!/usr/bin/env python
"""OLS bootstrap scaling study for the KLC Reserve high-core nodes.

Compare one threaded process, a pool of worker processes, and one SLURM
array task. The shell sets ``OMP_NUM_THREADS``, ``MKL_NUM_THREADS``,
``OPENBLAS_NUM_THREADS``, and ``NUMEXPR_NUM_THREADS`` before this process
starts. Each run writes one CSV row.
"""

import argparse
import csv
import multiprocessing
import os
import time

import numpy as np

N_OBS = 20_000
N_PRED = 500
N_REPS = 128
SEED = 20261117

_X = None
_Y = None


def build_data(seed):
    """Draw the shared design matrix and outcome without calling BLAS.

    Parameters
    ----------
    seed : int
        Seed for the random draw. Every mode uses the same matrix.

    Returns
    -------
    tuple of numpy.ndarray
        ``x`` with shape ``(N_OBS, N_PRED)`` and ``y`` with shape ``(N_OBS,)``.
        The first column of ``x`` is an intercept. Skipping the matrix product
        leaves BLAS uninitialized so worker processes can fork safely.
    """
    rng = np.random.default_rng(seed)
    x = rng.standard_normal((N_OBS, N_PRED))
    x[:, 0] = 1.0
    y = rng.standard_normal(N_OBS)
    return x, y


def one_replicate(x, y, seed):
    """Fit OLS on one bootstrap resample.

    Parameters
    ----------
    x : numpy.ndarray
        Design matrix, including the intercept column.
    y : numpy.ndarray
        Outcome vector.
    seed : int
        Seed for the row resample.

    Returns
    -------
    numpy.ndarray
        Coefficient vector from ``numpy.linalg.lstsq``. This call is the
        timed BLAS work.
    """
    rng = np.random.default_rng(seed)
    idx = rng.integers(0, x.shape[0], size=x.shape[0])
    coef, *_ = np.linalg.lstsq(x[idx], y[idx], rcond=None)
    return coef


def replicate_seeds(n_reps, seed):
    """Return one integer seed per replicate.

    Parameters
    ----------
    n_reps : int
        Number of bootstrap replicates.
    seed : int
        Root seed. Threads, workers, and the job array share this list so
        they fit the same replicates.

    Returns
    -------
    list of int
        Length ``n_reps``. Array task ``k`` uses entry ``k - 1``.
    """
    return np.random.SeedSequence(seed).generate_state(n_reps).tolist()


def _fit_seed(seed):
    """Fit one replicate inside a forked worker.

    Parameters
    ----------
    seed : int
        One value from :func:`replicate_seeds`.

    Returns
    -------
    numpy.ndarray
        Coefficient vector. The worker reads the design matrix from the
        module-level ``_X`` and ``_Y`` inherited at fork time.
    """
    return one_replicate(_X, _Y, int(seed))


def run(mode, n_workers, seeds):
    """Run every replicate and return the coefficient rows.

    Parameters
    ----------
    mode : {"threads", "workers", "workers-oversubscribed", "array"}
        ``threads`` and ``array`` loop in this process. ``workers`` and
        ``workers-oversubscribed`` use a pool of ``n_workers`` processes.
        The BLAS thread count is not an argument. The shell exports it
        before this process starts.
    n_workers : int
        Pool size for the worker modes. Ignored for ``threads`` and ``array``.
    seeds : sequence of int
        Replicate seeds. An array task passes a one-element sequence.

    Returns
    -------
    list of numpy.ndarray
        One coefficient vector per seed.
    """
    if mode in ("threads", "array"):
        return [one_replicate(_X, _Y, int(seed)) for seed in seeds]
    if mode in ("workers", "workers-oversubscribed"):
        with multiprocessing.Pool(processes=n_workers) as pool:
            return pool.map(_fit_seed, seeds)
    raise SystemExit(f"Unknown mode: {mode}")


def main():
    """Time the requested mode and write one CSV row.

    Reads ``--mode``, ``--workers``, ``--threads``, and ``--output``.
    ``--threads`` is recorded in the CSV. It does not change the BLAS pool.
    In ``array`` mode, ``SLURM_ARRAY_TASK_ID`` selects one seed. The row
    records language, mode, ``SLURM_CPUS_PER_TASK``, worker count, thread
    count, elapsed seconds, and the SLURM job and array ids.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        required=True,
        choices=("threads", "workers", "workers-oversubscribed", "array"),
    )
    parser.add_argument("--workers", type=int, required=True)
    parser.add_argument("--threads", type=int, required=True)
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    global _X, _Y
    _X, _Y = build_data(SEED)
    seeds = replicate_seeds(N_REPS, SEED)
    workers = args.workers
    array_id = ""

    if args.mode == "array":
        array_id = os.environ.get("SLURM_ARRAY_TASK_ID", "")
        if array_id == "":
            raise SystemExit("array mode requires SLURM_ARRAY_TASK_ID")
        seeds = [seeds[int(array_id) - 1]]
        workers = 1

    t0 = time.perf_counter()
    betas = run(args.mode, workers, seeds)
    elapsed = time.perf_counter() - t0
    float(np.vstack(betas).mean())

    cpus = os.environ.get("SLURM_CPUS_PER_TASK", "")
    job_id = os.environ.get("SLURM_JOB_ID", "")
    out_dir = os.path.dirname(args.output)
    if out_dir:
        os.makedirs(out_dir, exist_ok=True)
    with open(args.output, "w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "language",
                "mode",
                "cpus",
                "workers",
                "threads",
                "elapsed_seconds",
                "slurm_job_id",
                "array_task_id",
            ]
        )
        writer.writerow(
            [
                "python",
                args.mode,
                cpus,
                workers,
                args.threads,
                f"{elapsed:.4f}",
                job_id,
                array_id,
            ]
        )


if __name__ == "__main__":
    multiprocessing.set_start_method("fork")
    main()
```

## R Script

Save this as `/kellogg/proj/<your-netid>/scaling/bootstrap_scale.R`. It uses base R and `parallel::mclapply` only.

```r
#!/usr/bin/env Rscript

n_obs <- 20000L
n_pred <- 500L
n_reps <- 128L
seed <- 20261117L

parse_args <- function(args) {
  out <- list()
  i <- 1L
  while (i <= length(args)) {
    key <- sub("^--", "", args[[i]])
    if (i == length(args)) stop("Missing value for --", key)
    out[[key]] <- args[[i + 1L]]
    i <- i + 2L
  }
  out
}

opt <- parse_args(commandArgs(trailingOnly = TRUE))
missing <- vapply(
  c("mode", "workers", "threads", "output"),
  function(key) is.null(opt[[key]]),
  logical(1)
)
if (any(missing)) stop("Required arguments: --mode --workers --threads --output")
mode <- opt[["mode"]]
n_workers <- as.integer(opt[["workers"]])
n_threads <- as.integer(opt[["threads"]])
output <- opt[["output"]]

# rnorm and matrix do not call BLAS. Workers initialize BLAS after the fork.
build_data <- function(seed) {
  set.seed(seed)
  x <- matrix(rnorm(n_obs * n_pred), nrow = n_obs, ncol = n_pred)
  x[, 1] <- 1
  y <- rnorm(n_obs)
  list(x = x, y = y)
}

one_replicate <- function(x, y, seed) {
  set.seed(seed)
  idx <- sample.int(nrow(x), nrow(x), replace = TRUE)
  lm.fit(x[idx, , drop = FALSE], y[idx])$coefficients
}

data <- build_data(seed)
x <- data$x
y <- data$y
set.seed(seed)
rep_seeds <- sample.int(.Machine$integer.max, n_reps)

array_id <- ""
if (identical(mode, "array")) {
  array_id <- Sys.getenv("SLURM_ARRAY_TASK_ID", "")
  if (!nzchar(array_id)) stop("array mode requires SLURM_ARRAY_TASK_ID")
  rep_seeds <- rep_seeds[as.integer(array_id)]
  n_workers <- 1L
}

timing <- system.time({
  if (mode %in% c("threads", "array")) {
    betas <- lapply(rep_seeds, function(s) one_replicate(x, y, s))
  } else if (mode %in% c("workers", "workers-oversubscribed")) {
    betas <- parallel::mclapply(
      rep_seeds,
      function(s) one_replicate(x, y, s),
      mc.cores = n_workers,
      mc.set.seed = FALSE
    )
  } else {
    stop("Unknown mode: ", mode)
  }
  if (any(vapply(betas, inherits, logical(1), "try-error"))) {
    stop("A replicate failed")
  }
  mean(unlist(betas))
})
elapsed <- timing[["elapsed"]]

out_dir <- dirname(output)
if (!dir.exists(out_dir)) dir.create(out_dir, recursive = TRUE)
cpus <- Sys.getenv("SLURM_CPUS_PER_TASK", "")
job_id <- Sys.getenv("SLURM_JOB_ID", "")
workers_out <- if (mode %in% c("workers", "workers-oversubscribed")) n_workers else 1L
line <- sprintf(
  "r,%s,%s,%d,%d,%.4f,%s,%s",
  mode, cpus, workers_out, n_threads, elapsed, job_id, array_id
)
writeLines(
  c(
    "language,mode,cpus,workers,threads,elapsed_seconds,slurm_job_id,array_task_id",
    line
  ),
  output
)
```

## Batch Script

Save this as `/kellogg/proj/<your-netid>/scaling/scale_study.sh`. The submit commands pass the mode, the language, and the core request. The script sets the four thread variables from that mode before it starts Python or R.

```bash
#!/bin/bash
#SBATCH --account=kellogg
#SBATCH --partition=kellogg
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1          # overridden on the sbatch command line
#SBATCH --mem=16G                   # overridden for worker and array jobs
#SBATCH --time=01:00:00             # overridden for the job array
#SBATCH --job-name=scale
#SBATCH --output=/kellogg/proj/<your-netid>/scaling/logs/%x-%j.out

if [ -z "$SCALING_LANG" ] || [ -z "$SCALING_MODE" ]; then
  echo "Export SCALING_LANG (python or r) and SCALING_MODE" >&2
  exit 1
fi
if [ -z "$SLURM_CPUS_PER_TASK" ]; then
  echo "SLURM_CPUS_PER_TASK is unset" >&2
  exit 1
fi

case "$SCALING_MODE" in
  threads)
    THREADS="$SLURM_CPUS_PER_TASK"
    WORKERS=1
    ;;
  workers)
    THREADS=1
    WORKERS="$SLURM_CPUS_PER_TASK"
    ;;
  workers-oversubscribed)
    # N workers, each allowed N BLAS threads, on N cores.
    THREADS="$SLURM_CPUS_PER_TASK"
    WORKERS="$SLURM_CPUS_PER_TASK"
    ;;
  array)
    THREADS=1
    WORKERS=1
    ;;
  *)
    echo "Unknown SCALING_MODE=$SCALING_MODE" >&2
    exit 1
    ;;
esac

eval "$('/hpc/software/mamba/24.3.0/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
source "/hpc/software/mamba/24.3.0/etc/profile.d/mamba.sh"
mamba activate /kellogg/proj/<your-netid>/envs/my-env

# Export after activate. An environment hook can otherwise replace these values.
export OMP_NUM_THREADS="$THREADS"
export MKL_NUM_THREADS="$THREADS"
export OPENBLAS_NUM_THREADS="$THREADS"
export NUMEXPR_NUM_THREADS="$THREADS"

cd /kellogg/proj/<your-netid>/scaling
mkdir -p results

TAG="${SLURM_ARRAY_TASK_ID:-$SLURM_CPUS_PER_TASK}"
OUT="results/${SCALING_LANG}-${SCALING_MODE}-${TAG}-${SLURM_JOB_ID}.csv"

if [ "$SCALING_LANG" = "python" ]; then
  python bootstrap_scale.py \
    --mode "$SCALING_MODE" \
    --workers "$WORKERS" \
    --threads "$THREADS" \
    --output "$OUT"
elif [ "$SCALING_LANG" = "r" ]; then
  Rscript bootstrap_scale.R \
    --mode "$SCALING_MODE" \
    --workers "$WORKERS" \
    --threads "$THREADS" \
    --output "$OUT"
else
  echo "SCALING_LANG must be python or r" >&2
  exit 1
fi
```

Replace `<your-netid>` and `my-env` before submitting. The environment needs Python `numpy` and a base R install that provides `parallel`.

| Mode | Command-line overrides | Memory |
|---|---|---|
| Threads | `--cpus-per-task=N --mem=16G --constraint=quest14` | One shared copy of the matrix |
| Workers | `--cpus-per-task=N --mem=64G --constraint=quest14` | Each worker allocates its own resampled matrix, about 80 MB at the default size |
| Oversubscription | `--cpus-per-task=16 --mem=64G --constraint=quest14` | Same worker layout, with the thread variables set to 16 |
| Job array | `--array=1-128 --cpus-per-task=1 --mem=8G --time=00:30:00` | One replicate per task, and no `--constraint=quest14` |

Keep `--mem` under 503 GB. After a job finishes, `seff <job-id>` reports the memory it actually used. Lower the next request when the peak is far below the grant, and raise it when the job is killed for memory.

## Submit the Grid

Create the directories, then submit one 1-core Python thread job and confirm that a CSV row appears before submitting the rest:

```bash
mkdir -p /kellogg/proj/<your-netid>/scaling/logs /kellogg/proj/<your-netid>/scaling/results
cd /kellogg/proj/<your-netid>/scaling

sbatch --export=ALL,SCALING_LANG=python,SCALING_MODE=threads \
  --cpus-per-task=1 --mem=16G --constraint=quest14 \
  --job-name=python-threads-1 \
  --output=/kellogg/proj/<your-netid>/scaling/logs/python-threads-1-%j.out \
  scale_study.sh
```

Submit the full grid once that row looks right. The loop includes another 1-core thread job.

```bash
for lang in python r; do
  for n in 1 2 4 8 16 32 64 128; do
    sbatch --export=ALL,SCALING_LANG=$lang,SCALING_MODE=threads \
      --cpus-per-task=$n --mem=16G --constraint=quest14 \
      --job-name=${lang}-threads-$n \
      --output=/kellogg/proj/<your-netid>/scaling/logs/${lang}-threads-$n-%j.out \
      scale_study.sh
    sbatch --export=ALL,SCALING_LANG=$lang,SCALING_MODE=workers \
      --cpus-per-task=$n --mem=64G --constraint=quest14 \
      --job-name=${lang}-workers-$n \
      --output=/kellogg/proj/<your-netid>/scaling/logs/${lang}-workers-$n-%j.out \
      scale_study.sh
  done

  sbatch --export=ALL,SCALING_LANG=$lang,SCALING_MODE=workers-oversubscribed \
    --cpus-per-task=16 --mem=64G --constraint=quest14 \
    --job-name=${lang}-oversub \
    --output=/kellogg/proj/<your-netid>/scaling/logs/${lang}-oversub-%j.out \
    scale_study.sh

  sbatch --export=ALL,SCALING_LANG=$lang,SCALING_MODE=array \
    --array=1-128 --cpus-per-task=1 --mem=8G --time=00:30:00 \
    --job-name=${lang}-array \
    --output=/kellogg/proj/<your-netid>/scaling/logs/${lang}-array-%A_%a.out \
    scale_study.sh
done
```

Command-line `sbatch` options override the matching `#SBATCH` lines in `scale_study.sh`. The array submission does not pass `--constraint=quest14`.

## Collect the Results

Combine the one-row CSV files into a single file with one header:

```bash
cd /kellogg/proj/<your-netid>/scaling
awk 'FNR==1 && NR!=1 { next } { print }' results/*.csv > results/scaling.csv
```

For each array job id, record the task span:

```bash
sacct -j <array-job-id> -X --format=JobID,Start,End,Elapsed,AllocCPUS,State
```

Use the earliest `Start` and the latest `End` across the array tasks. That span is the number that sits next to the thread and worker times, which already cover all 128 replicates. Run `seff` on one thread job and one worker job before changing `--mem` or `--time` for a second grid.

(high-core-scaling-takeaways)=
## Key Takeaways

<!-- TODO(KRS): fill wall times and takeaways after the cluster runs -->

Wall-clock times go in the table after the grid has been run on KLC Reserve. Leave the cells blank until then. Fill one row from each CSV file. For each job array, fill one additional row whose elapsed time is the `sacct` span, and leave CPUs at 1.

| Language | Mode | CPUs | Workers | Threads | Elapsed seconds | SLURM job ID |
|---|---|---|---|---|---|---|
|  |  |  |  |  |  |  |

Use the filled table to compare:

- Thread runs and worker runs at the same core count, in each language
- The fastest single-node run and the job-array span
- The 16-core worker run with thread variables set to 1, and the 16-worker run with thread variables set to 16

## Further Reading

- [High-Core CPU Nodes](high-core-cpu-nodes) — 128-core Emerald Rapids nodes (`qnode4043`, `qnode4044`)
- [Submitting SLURM Jobs](slurm-jobs) — batch scripts, job arrays, and `seff`
- [High-Memory Jobs](highmem-jobs) — jobs that need more than 503 GB
- [Deep Dive: Scaling Studies](https://rs-kellogg.github.io/krs-intro-klc-reserve/deep-dive-scaling-studies) — turn a short test job into a wall-time request, from the AI Inference Using KLC Reserve workshop (October 2026)
