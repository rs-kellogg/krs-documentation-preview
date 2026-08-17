# GPU Jobs

Kellogg-affiliated researchers access dedicated GPU nodes through KLC Reserve by submitting SLURM jobs to the **`kellogg` partition** with a **`--gres`** (generic resource) GPU request.

For CPU vs. GPU concepts and when a GPU helps, see [GPU Concepts and Options](/services/klc-reserve/gpu-concepts). For non-GPU batch jobs, see [Submitting SLURM Jobs](slurm-jobs).

## Available GPU Nodes

| Node type | Nodes | CPUs | Host RAM | GPUs per node | GPU memory | Typical use |
|---|---|---|---|---|---|---|
| L40S | 1 | 64 | — | 2 | 48 GB per GPU | LLM inference, rendering, general GPU workloads |
| A100 | 1 | 64 | 2 TB | 1 | 80 GB | Training and inference for medium-to-large models |
| H100 | 2 | 64 | 1 TB | 4 | 80 GB per GPU | Large-scale LLM training/inference, deep learning |

## Requesting a GPU with `--gres`

Use `--gres=gpu:1` unless you need a specific card type. SLURM assigns any available GPU, which usually reduces queue wait time.

Request a specific card when your workload requires it — for example, a model that needs more than 48 GB of GPU memory (ruling out L40S) or code tuned for H100 Tensor Core behavior:

```bash
--gres=gpu:1          # any available GPU (preferred default)
--gres=gpu:l40s:1     # specifically an L40S (48 GB)
--gres=gpu:a100:1     # specifically an A100 (80 GB)
--gres=gpu:h100:1     # specifically an H100 (80 GB)
```

Request multiple GPUs on one node (meaningful on L40S and H100 nodes, which have more than one GPU):

```bash
--gres=gpu:h100:4     # all 4 H100s on a single node
```

## Example Batch Script

```bash
#!/bin/bash

#SBATCH --account=kellogg
#SBATCH --partition=kellogg
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gres=gpu:1                    # any available GPU
#SBATCH --time=0:30:00
#SBATCH --mem=40G
#SBATCH --output=/kellogg/proj/<your-netid>/slurm-output/slurm-%j.out

module purge all
module use --append /kellogg/software/Modules/modulefiles
module load micromamba/latest
source /kellogg/software/Modules/modulefiles/micromamba/load_hook.sh
micromamba activate /kellogg/proj/<your-netid>/envs/my-gpu-env

python train.py
```

Submit with `sbatch gpu_job.sh`.

### Key Parameters

| Parameter | Description |
|---|---|
| `--account` | Your Kellogg SLURM account |
| `--partition=kellogg` | Routes the job to Kellogg GPU nodes |
| `--ntasks-per-node=1` | CPU cores; increase only if your code parallelizes on CPU |
| `--gres=gpu:1` | Number and type of GPUs |
| `--mem` | Host RAM (separate from GPU memory) |
| `--time` | Maximum wall time; job is killed if exceeded |
| `--output` | Log file path (`%j` = job ID) |

## Interactive GPU Session

For debugging GPU code interactively:

```bash
salloc --account=kellogg \
       --partition=kellogg \
       --nodes=1 \
       --ntasks-per-node=1 \
       --gres=gpu:1 \
       --mem=40G \
       --time=01:00:00
```

When the shell prompt returns, verify the GPU:

```bash
nvidia-smi
```

Release the allocation with `exit`.

## Verify GPU Access in Python

Before a long run, confirm your environment sees the GPU:

```python
# pytorch_gpu_test.py
import torch

if torch.cuda.is_available():
    print(f"CUDA version: {torch.version.cuda}")
    print(f"Number of GPUs: {torch.cuda.device_count()}")
    print(f"GPU name: {torch.cuda.get_device_name(0)}")
else:
    print("CUDA is not available — running on CPU")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"Using: {device}")

t1 = torch.randn(1000, 1000, device=device)
t2 = torch.randn(1000, 1000, device=device)
result = t1 + t2
print(f"Tensor shape: {result.shape}")
```

Sample scripts are in the [krs-openllm-cookbook GitHub repo](https://github.com/rs-kellogg/krs-openllm-cookbook/blob/main/scripts/slurm_basics).

A video walkthrough of running this in a Jupyter notebook is available in the [Quest OnDemand GPU notebook walkthrough](https://kellogg-shared.s3.us-east-2.amazonaws.com/videos/quest-on-demand-gpu-notebook.mp4).

## Check GPU Utilization

While a job runs, inspect GPU use:

```bash
nvidia-smi
watch -n 2 nvidia-smi    # refresh every 2 seconds
```

Low GPU utilization often means the bottleneck is data loading or CPU preprocessing, not the model itself.

## LLM Inference on GPU

For open-source LLM workflows on KLC, see [Open Source LLMs on KLC](/services/klc/user-guide/llm-klc). GPU nodes accelerate larger models and batch inference that are impractical on CPU-only login nodes.

For worked examples that serve a model in Singularity and query it from a login node, see [vLLM Inference on KLC Reserve GPUs](vllm-example) (OpenAI-compatible API) and [Ollama Inference on KLC Reserve GPUs](ollama-example) (submit the shared Ollama launcher with `sbatch` and query from a login node).

For hosted API workflows (OpenAI, Anthropic, etc.), see [LLM API Usage](/services/klc/user-guide/llm-api).

## Multi-GPU Jobs

Multi-GPU training requires framework support (PyTorch `DistributedDataParallel`, Hugging Face Accelerate, etc.) and matching `--gres` requests:

```bash
#SBATCH --gres=gpu:h100:4
```

Ensure your code initializes all visible devices. A single process that only uses `cuda:0` leaves other GPUs idle.

## Common Failures

| Symptom | Likely cause | What to do |
|---|---|---|
| `CUDA is not available` in logs | Job landed on a node without GPU, or driver/CUDA mismatch | Confirm `#SBATCH --gres=gpu:1`; verify PyTorch CUDA build matches node driver |
| `CUDA out of memory` | Model or batch size exceeds GPU memory | Reduce batch size; use a smaller model; request A100/H100 instead of L40S |
| Job pending indefinitely | No GPU of requested type free | Try `--gres=gpu:1` without a card name; check `squeue -j <job-id> --start` |
| Low `nvidia-smi` utilization | CPU-bound pipeline | Profile data loading; increase dataloader workers |

## Quest General GPU Access

This page covers GPU jobs on the **`kellogg` partition** — the Kellogg Reserve path. For Northwestern-wide GPUs at scale, use the Quest General Access **`gengpu`** partition instead.

Test and debug your GPU workflow on `kellogg` first. When the workflow is proven and you need more GPUs than Kellogg Reserve can provide, submit to `gengpu` with your [Quest allocation](https://www.it.northwestern.edu/departments/it-services-support/research/computing/quest/general-access-allocation-types.html). That path requires a separate Quest allocation, not just a KLC account. See [GPU Concepts and Options](gpu-concepts) for the full comparison and [GPUs on Quest](https://rcdsdocs.it.northwestern.edu/systems/quest/user-guide/gpu/gpu.html) for submission details.

## Further Reading

- [Submitting SLURM Jobs](slurm-jobs) — batch scripts, job arrays, monitoring
- [When to Use KLC Reserve](when-to-use) — case studies for GPU workloads
- [Quest GPU documentation](https://rcdsdocs.it.northwestern.edu/systems/quest/user-guide/gpu/gpu.html)
