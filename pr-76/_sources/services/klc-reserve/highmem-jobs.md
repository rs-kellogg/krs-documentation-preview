# High-Memory Jobs

Kellogg-affiliated researchers access the dedicated high-memory node through KLC Reserve by submitting SLURM jobs to the **`kellogg` partition**, pinned to the high-memory node with **`--nodelist`**.

For GPU concepts and when a GPU helps, see [GPU Concepts and Options](/services/klc-reserve/gpu-concepts). For non-memory-intensive batch jobs, see [Submitting SLURM Jobs](slurm-jobs).

## Available High-Memory Node

| Node type | Nodes | CPUs | Host RAM | RAM per core | Typical use |
|---|---|---|---|---|---|
| qhimem0501 | 1 | 64 | 2 TB | ~32 GB | Large in-memory matrices, big panel merges, graph/network analysis |

## Requesting the High-Memory Node with `--nodelist`

Unlike GPU jobs, where `--gres` lets SLURM pick any available card, there is only one high-memory node, so jobs target it directly with `--nodelist=qhimem0501`:

```bash
--nodelist=qhimem0501    # pin the job to the high-memory node
```

Request only the memory you need with `--mem`. Since other jobs may share the node, avoid requesting the full 2 TB unless your job actually needs it:

```bash
--mem=200G     # request 200 GB of host RAM
--mem=800G     # request 800 GB of host RAM
```

## Example Batch Script

```bash
#!/bin/bash

#SBATCH --account=kellogg
#SBATCH --partition=kellogg
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --nodelist=qhimem0501
#SBATCH --mem=400G
#SBATCH --time=04:00:00
#SBATCH --output=/kellogg/proj/<your-netid>/slurm-output/slurm-%j.out

module purge all
module use --append /kellogg/software/Modules/modulefiles
module load mamba/24.3.0
source activate /kellogg/proj/<your-netid>/envs/my-highmem-env

python similarity_matrix.py
```

Submit with `sbatch highmem_job.sh`.

### Key Parameters

| Parameter | Description |
|---|---|
| `--account` | Your Kellogg SLURM account |
| `--partition=kellogg` | Routes the job to the Kellogg Reserve partition |
| `--nodelist=qhimem0501` | Pins the job to the high-memory node |
| `--ntasks-per-node=1` | CPU cores; increase only if your code parallelizes on CPU |
| `--mem` | Host RAM requested for the job |
| `--time` | Maximum wall time; job is killed if exceeded |
| `--output` | Log file path (`%j` = job ID) |

## Interactive High-Memory Session

For debugging memory-intensive code interactively:

```bash
srun --partition=kellogg \
     --account=kellogg \
     --nodes=1 \
     --ntasks-per-node=1 \
     --mem=200G \
     --time=00:30:00 \
     --nodelist=qhimem0501 \
     --pty bash -l
```

When the shell prompt returns, confirm you are on the node and check available memory:

```bash
hostname
free -h
```

Release the allocation with `exit`.

## Verify Memory Availability in Python

Before a long run, confirm how much memory your process can actually see. Install `psutil` in your environment if it is not already present (`pip install psutil`):

```python
# check_memory.py
import psutil

mem = psutil.virtual_memory()
print(f"Total RAM: {mem.total / 1e9:.1f} GB")
print(f"Available RAM: {mem.available / 1e9:.1f} GB")
print(f"Used RAM: {mem.used / 1e9:.1f} GB ({mem.percent}%)")
```

## Check Memory Utilization

While a job runs, inspect memory use on the node:

```bash
free -h
watch -n 2 free -h    # refresh every 2 seconds
```

You can also check your job's actual usage against what you requested:

```bash
sacct -j <job-id> --format=JobID,MaxRSS,ReqMem,Elapsed
```

If `MaxRSS` is far below `ReqMem`, you are over-requesting and slowing down your own queue time.

## Example Job: Full Pairwise Similarity Matrix

A good high-memory workload is not just "read in a big file" — it is a computation whose *intermediate output* is large, even if the input is not. A common example in text and network research is building a full pairwise similarity matrix, e.g., to deduplicate or cluster a large set of document embeddings (earnings calls, patent texts, survey responses).

The script below is an illustrative pattern. Supply your own pre-computed embeddings as a `.npy` file at the path shown in the script.

For `n` embeddings, the full similarity matrix has `n²` entries. At n = 200,000, a float32 similarity matrix alone is:

```
200,000 × 200,000 × 4 bytes ≈ 160 GB
```

That is before accounting for the input embeddings and intermediate copies numpy creates during the matrix multiply — well beyond a laptop or the shared KLC login node, but comfortable on `qhimem0501`.

```python
# similarity_matrix.py
import numpy as np

# Load pre-computed embeddings: shape (n_documents, embedding_dim)
# e.g. output of an LLM embedding model, stored as a .npy file
embeddings = np.load("/kellogg/proj/<your-netid>/data/embeddings.npy")
n, d = embeddings.shape
print(f"Loaded {n:,} embeddings of dimension {d}")

# Normalize rows to unit length so a dot product equals cosine similarity
norms = np.linalg.norm(embeddings, axis=1, keepdims=True)
normalized = embeddings / norms

# Full pairwise cosine similarity matrix — this is the memory-intensive step.
# The matrix itself is n x n and lives entirely in RAM during computation.
similarity = normalized @ normalized.T
print(f"Similarity matrix shape: {similarity.shape}, "
      f"size: {similarity.nbytes / 1e9:.1f} GB")

# Do not save the full matrix — extract what you actually need,
# e.g. top-k nearest neighbors per document for clustering/dedup
k = 10
np.fill_diagonal(similarity, -1)  # exclude self-matches
top_k_idx = np.argpartition(-similarity, k, axis=1)[:, :k]

np.save("/kellogg/proj/<your-netid>/output/top_k_neighbors.npy", top_k_idx)
print("Saved top-k neighbor indices.")
```

This pattern — input data that is modest in size, but an `O(n²)` computation that is not — generalizes to other memory-bound jobs: full correlation matrices across a large panel of firms, distance matrices for clustering, or dense adjacency matrices for network analysis.

## Common Failures

| Symptom | Likely cause | What to do |
|---|---|---|
| `Out of Memory` / job killed by SLURM | `--mem` request too low for actual usage | Check `sacct MaxRSS` from a prior run; increase `--mem` |
| `MemoryError` in Python logs | Process exceeded requested `--mem`, or matrix is larger than expected | Recompute expected matrix size (`n² × bytes per element`) before submitting; reduce precision (float32 instead of float64) or process in chunks |
| Job pending indefinitely | Node already fully allocated by another job | Check `squeue -p kellogg` for current usage; try a smaller `--mem` request or wait |
| Job runs but much slower than expected | Swapping to disk because requested memory was set too low elsewhere in the pipeline | Confirm no other step (e.g. a pandas merge) silently exceeds `--mem`; monitor with `free -h` during the run |

## Further Reading

- [Submitting SLURM Jobs](slurm-jobs) — batch scripts, job arrays, monitoring
- [GPU Jobs](gpu-jobs) — for workloads that need GPU acceleration instead of host RAM
- [When to Use KLC Reserve](when-to-use) — case studies for high-memory workloads
