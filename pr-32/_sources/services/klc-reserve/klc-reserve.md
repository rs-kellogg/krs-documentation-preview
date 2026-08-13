(klc-reserve)=
# Kellogg Linux Cluster Reserve

**Kellogg Linux Cluster Reserve (KLC Reserve)** gives Kellogg researchers scheduled access to dedicated compute resources through the **SLURM job scheduler** — including GPU nodes and high-core-count batch nodes that are not available when you log directly into a standard KLC login node.

Reserve resources are accessed by submitting jobs to the `kellogg` SLURM partition from any KLC node. Unlike standard KLC login nodes (shared interactively by many users), Reserve resources are allocated exclusively to your job for its duration.

## Standard KLC vs. KLC Reserve

| | Standard KLC login nodes | KLC Reserve |
|---|---|---|
| **Access** | SSH, OnDemand, VS Code, or FastX to a named node | Submit a SLURM job from any KLC node |
| **Resources** | Shared with all users on that node | Dedicated cores, memory, and GPUs for your job |
| **Core limit** | 24 cores at normal priority per user | Request up to full node capacity in one job |
| **GPUs** | Not available on login nodes | H100, A100, and L40S GPU nodes |
| **Connection** | Must stay connected (or use `tmux`/FastX) for interactive work | Batch jobs run after you log out |
| **Best for** | Development, debugging, short interactive runs | Production runs, GPUs, long jobs, parallel pipelines |

For the decision framework, see [When to Use KLC Reserve](when-to-use). For interactive work on login nodes, see the [KLC User Guide](/services/klc/user-guide/klc-user-guide).

## Available Resources

| Resource type | Nodes | Key specs | Best for |
|---|---|---|---|
| GPU — H100 | 2 | 64 cores, 1 TB RAM, 4 × 80 GB GPUs per node | Large-scale LLM training/inference, deep learning |
| GPU — A100 | 1 | 64 cores, 2 TB RAM, 1 × 80 GB GPU per node | GPU-accelerated ML training and inference |
| GPU — L40S | 1 | 64 cores, 2 × 48 GB GPUs per node | LLM inference, rendering, general GPU workloads |
| High-memory CPU | 1 | 64 cores, 2 TB RAM | Very large in-memory datasets, parallel CPU jobs |

Contact [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) for current availability and capacity questions.

## Getting Access

KLC Reserve uses the same Northwestern NetID and KLC account as standard KLC login access. If you already have a KLC account, submit jobs to the `kellogg` partition without additional setup.

```{note}
Run `groups` after logging into any KLC node to see the SLURM allocation names you belong to. Use `--account=kellogg` in job scripts. Contact [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) if jobs fail to submit.
```

## Submit Your First Job

1. **Log in to KLC** via [SSH](/services/klc/user-guide/klc-ssh), [KLC OnDemand](/services/klc/user-guide/klc-ondemand), or [VS Code](/services/klc/user-guide/klc-vscode).

2. **Write a job script** with `#SBATCH` directives for account, partition, cores, memory, and wall time. See [Submitting SLURM Jobs](slurm-jobs).

3. **Submit the job:**

   ```bash
   sbatch myjob.sh
   ```

4. **Monitor the job:**

   ```bash
   squeue -u $USER
   ```

5. **Inspect output** in the log file specified by `#SBATCH --output`.

For GPU jobs, add `--gres=gpu:1` (or a specific card type). See [GPU Jobs](gpu-jobs).

## Documentation Map

| Goal | Page |
|---|---|
| Decide whether Reserve fits your workload | [When to Use KLC Reserve](when-to-use) |
| Write and submit CPU batch jobs | [Submitting SLURM Jobs](slurm-jobs) |
| Request and use GPU nodes | [GPU Jobs](gpu-jobs) |
| Serve an open-source LLM with vLLM | [vLLM Inference on KLC Reserve GPUs](vllm-example) |
| Serve an open-source LLM with Ollama | [Ollama Inference on KLC Reserve GPUs](ollama-example) |
| Understand CPU vs. GPU concepts | [GPU Concepts and Options](/services/klc-reserve/gpu-concepts) |
| Interactive work on login nodes | [When to Use KLC Reserve](when-to-use) |
| Standard KLC overview | [Kellogg Linux Cluster](/services/klc/klc) |

```{toctree}
:maxdepth: 1
:hidden:

When to Use KLC Reserve <when-to-use>
GPU Concepts <gpu-concepts>
Submitting SLURM Jobs <slurm-jobs>
GPU Jobs <gpu-jobs>
vLLM on GPUs <vllm-example>
Ollama on GPUs <ollama-example>
```
