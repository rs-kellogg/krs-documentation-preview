# Using GPUs on Quest and KLC

KLC nodes are CPU-based. For workloads that benefit from GPU acceleration — especially running large language models and deep learning — you can access **Quest GPU nodes** via SLURM.

## CPU vs. GPU: Key Concepts

### CPU (Central Processing Unit)

A CPU handles all mathematical and logical calculations on a node. CPU cores are extremely powerful but run tasks **sequentially** — one at a time per core. KLC's latest nodes have 64 CPU cores and up to 2 TB of shared RAM, which means you can run up to 64 parallel processes on a single node.

### GPU (Graphics Processing Unit)

A GPU is a specialized processor designed for massively parallel mathematical operations. Where you can use 24 CPU cores on KLC under normal priority, a single A100 GPU contains **6,912 CUDA cores** (the H100 has 18,432). While individual GPU cores are less powerful than CPU cores, their sheer number makes them ideal for the vector and matrix operations at the heart of LLM inference and training.

```{note}
GPUs are not universally faster. Some tasks can't be parallelized at all (serial dependencies), and for small jobs the coordination overhead can actually make a GPU slower than a CPU. Use GPUs when your workload is inherently parallel — matrix multiplications, batch inference, training neural networks.
```

### CUDA (Compute Unified Device Architecture)

**CUDA** is Nvidia's software platform that manages when to route computations to GPU cores vs. CPU cores. You will not typically write CUDA code directly. Most researchers use high-level libraries — like [Hugging Face Transformers](https://huggingface.co/docs/transformers/index) or PyTorch — that call CUDA automatically.

The CUDA software stack looks like:

```
Your code (Python / Hugging Face / Ollama)
       ↓
PyTorch / TensorFlow
       ↓
CUDA
       ↓
GPU Hardware
```

When setting up your environment, you need to ensure your CUDA version, PyTorch/TensorFlow version, and GPU driver are compatible.

## GPU Options at Northwestern

**Kellogg GPU nodes (for Kellogg-affiliated researchers)**
- Dedicated GPU nodes accessed via `--partition=kellogg` and `--account=kellogg`
- Three node configurations available — L40S, A100, and H100 (see [Kellogg GPU Nodes](#kellogg-gpu-nodes) below)
- No separate allocation request needed for Kellogg-affiliated researchers

**Quest GPU nodes (general Northwestern access)**
- Dozens of Nvidia A100 and H100 GPU nodes
- Access via SLURM scheduler or Quest OnDemand
- Requires a [Quest allocation](https://www.it.northwestern.edu/departments/it-services-support/research/computing/quest/general-access-allocation-types.html)
- See [Quest GPU documentation](https://rcdsdocs.it.northwestern.edu/systems/quest/user-guide/gpu/gpu.html)

**Other options**
- [Google Colab](https://colab.research.google.com/) — free browser-based GPU notebooks
- AWS, Google Cloud, Microsoft Azure — cloud GPUs (usage-based cost)

(kellogg-gpu-nodes)=
## Kellogg GPU Nodes

Kellogg-affiliated researchers can submit jobs directly to Kellogg's dedicated GPU nodes using `--partition=kellogg` and `--account=kellogg`. The partition contains three node configurations:

| Node type | GPUs per node | GPU memory |
|---|---|---|
| L40S | 2 | 48 GB per GPU |
| A100 | 1 | 80 GB |
| H100 | 4 | 80 GB per GPU |

### Requesting a GPU with `--gres`

Use `--gres=gpu:1` unless the specific card type matters for your workload. This lets SLURM assign any available GPU and generally reduces queue wait time.

Only request a specific card when your job has a concrete reason — for example, a model that requires more than 48 GB of GPU memory (ruling out the L40S) or code that is tuned for H100 Tensor Core behavior:

```bash
--gres=gpu:1          # any available GPU (preferred default)
--gres=gpu:l40s:1     # specifically an L40S (48 GB)
--gres=gpu:a100:1     # specifically an A100 (80 GB)
--gres=gpu:h100:1     # specifically an H100 (80 GB)
```

To request multiple GPUs on the same node (only meaningful on the L40S or H100 nodes, which have more than one):

```bash
--gres=gpu:h100:4     # all 4 H100s on a single node
```

### Example SLURM Script (Kellogg partition)

```bash
#!/bin/bash

#SBATCH --account=kellogg               # Kellogg account
#SBATCH --partition=kellogg             # Kellogg GPU partition
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gres=gpu:1                    # any available GPU; specify card type only if needed
#SBATCH --time=0:30:00
#SBATCH --mem=40G
#SBATCH --output=/kellogg/proj/<your-netid>/slurm-output/slurm-%j.out

module purge all
module use --append /kellogg/software/Modules/modulefiles
module load micromamba/latest
source /kellogg/software/Modules/modulefiles/micromamba/load_hook.sh
micromamba activate /kellogg/software/envs/llm-test-env

python pytorch_gpu_test.py
```

## Testing GPU Availability

Before running a full job, verify that your environment can see the GPU:

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

# Basic tensor operation to confirm GPU is working
t1 = torch.randn(1000, 1000, device=device)
t2 = torch.randn(1000, 1000, device=device)
result = t1 + t2
print(f"Tensor shape: {result.shape}")
```

A sample script is also in the [krs-openllm-cookbook GitHub repo](https://github.com/rs-kellogg/krs-openllm-cookbook/blob/main/scripts/slurm_basics).

A video walkthrough of running this in a Jupyter notebook is available [here](https://kellogg-shared.s3.us-east-2.amazonaws.com/videos/quest-on-demand-gpu-notebook.mp4).

## Submitting a GPU Job with SLURM

Quest uses the **SLURM** scheduler to allocate GPU resources. You submit a shell script that specifies your resource requirements.

### Example SLURM Script

```bash
#!/bin/bash

#SBATCH --account=<your_allocation>      # Your Quest allocation ID
#SBATCH --partition=gengpu              # GPU partition on Quest
#SBATCH --nodes=1
#SBATCH --ntasks-per-node=1
#SBATCH --gres=gpu:a100:1               # Request 1 A100 GPU
#SBATCH --constraint=pcie               # pcie = 40 GB; sxm = 80 GB
#SBATCH --time=0:30:00                  # Max wall time (HH:MM:SS)
#SBATCH --mem=40G                       # RAM to request
#SBATCH --output=/projects/<allocation>/slurm-output/slurm-%j.out

module purge all
module use --append /kellogg/software/Modules/modulefiles
module load micromamba/latest
source /kellogg/software/Modules/modulefiles/micromamba/load_hook.sh
micromamba activate /kellogg/software/envs/llm-test-env

python pytorch_gpu_test.py
```

### Key Parameters Explained

| Parameter | Description |
|---|---|
| `--account` | Your [Quest allocation](https://www.it.northwestern.edu/departments/it-services-support/research/computing/quest/general-access-allocation-types.html) ID |
| `--partition=gengpu` | Routes job to Quest GPU nodes |
| `--ntasks-per-node` | Number of CPU cores to use; only increase if your code is parallelizable |
| `--gres=gpu:a100:1` | Request 1 A100 GPU; increase the number for multi-GPU jobs |
| `--constraint` | A100 memory: `pcie` = 40 GB, `sxm` = 80 GB |
| `--time` | Maximum allowed wall time; job is killed if it exceeds this |
| `--mem` | RAM requested (separate from GPU memory) |
| `--output` | Path for stdout/stderr logs (`%j` = job ID) |

### Submitting and Monitoring

```bash
# Submit the job
sbatch pytorch_gpu_test.sh

# Check job status
squeue -u $USER

# Cancel a job
scancel <job_id>
```

### Via Quest OnDemand

You can also submit SLURM jobs and run Jupyter notebooks with GPU access through the [Quest OnDemand](https://rcdsdocs.it.northwestern.edu/systems/quest/ondemand/ondemand.html) web interface — no command line required.

Video walkthroughs:
- [Submitting a SLURM job via Quest OnDemand](https://kellogg-shared.s3.us-east-2.amazonaws.com/videos/quest-on-demand-gpu-slurm.mp4)
- [Submitting a SLURM job via terminal](https://kellogg-shared.s3.us-east-2.amazonaws.com/videos/console-gpu-slurm.mp4)

## Getting a Quest Allocation

GPU nodes require a Quest allocation. Request one at:
[it.northwestern.edu — Quest Allocation Types](https://www.it.northwestern.edu/departments/it-services-support/research/computing/quest/general-access-allocation-types.html)

Contact [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) if you need guidance on which allocation type is right for your project.

## Related Pages

- [Launching Jobs on KLC](klc-software) — CPU-based job submission on KLC
- [Open Source LLMs on KLC](llm-klc) — running LLMs (including Ollama) on KLC CPU nodes
- [Open Source LLMs Guide](/guides/llm/llm) — broader guide including GPU-accelerated workflows
