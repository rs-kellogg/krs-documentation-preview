# GPU Concepts and Options

KLC **login nodes are CPU-only**. For workloads that benefit from GPU acceleration — especially large language models and deep learning — use **KLC Reserve GPU nodes** via SLURM on the `kellogg` partition.

This page explains **concepts and options**. For submission scripts and `--gres` syntax, see [GPU Jobs](gpu-jobs).

## CPU vs. GPU: Key Concepts

### CPU (Central Processing Unit)

A CPU handles mathematical and logical calculations on a node. CPU cores are powerful but run tasks **sequentially** — one at a time per core. KLC's latest nodes have 64 CPU cores and up to 2 TB of shared RAM, which means you can run up to 64 parallel processes on a single node when using Reserve.

### GPU (Graphics Processing Unit)

A GPU is a specialized processor designed for massively parallel mathematical operations. Where you can use 24 CPU cores on KLC login nodes under normal priority, a single A100 GPU contains **6,912 CUDA cores** (the H100 has 18,432). Individual GPU cores are less powerful than CPU cores, but their number makes GPUs ideal for the vector and matrix operations at the heart of LLM inference and training.

```{note}
GPUs are not universally faster. Some tasks cannot be parallelized (serial dependencies), and for small jobs the coordination overhead can make a GPU slower than a CPU. Use GPUs when your workload is inherently parallel — matrix multiplications, batch inference, training neural networks.
```

### CUDA (Compute Unified Device Architecture)

**CUDA** is Nvidia's software platform that routes computations to GPU cores vs. CPU cores. You will not typically write CUDA code directly. Most researchers use high-level libraries — like [Hugging Face Transformers](https://huggingface.co/docs/transformers/index) or PyTorch — that call CUDA automatically.

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

When setting up your environment, ensure your CUDA version, PyTorch/TensorFlow version, and GPU driver are compatible.

## GPU Options at Northwestern

### Kellogg GPU nodes (KLC Reserve)

- Dedicated GPU nodes on the **`kellogg` partition** with `--account=kellogg`
- Three node configurations — L40S, A100, and H100 (see [GPU Jobs](gpu-jobs))
- Primary path for Kellogg-affiliated researchers

### Quest GPU nodes (general Northwestern access)

See [GPU Jobs](gpu-jobs) for the `gengpu` partition and Quest allocation requirements.

### Other options

- [Google Colab](https://colab.research.google.com/) — browser-based GPU notebooks
- AWS, Google Cloud, Microsoft Azure — cloud GPUs (usage-based cost)

## Choosing a Path

| Need | Recommended path |
|---|---|
| Kellogg researcher, standard ML/LLM workload | KLC Reserve — `kellogg` partition |
| Already have a Quest allocation, need Quest-specific nodes | Quest — `gengpu` partition |
| Sensitive data must stay on-cluster, no GPU needed | [Open Source LLMs on KLC](/services/klc/user-guide/llm-klc) on CPU login nodes |
| Sensitive data, GPU needed | KLC Reserve GPU nodes |
| Quick experiment, no cluster setup | Google Colab or cloud (check data governance first) |

Contact [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) if you need guidance on which allocation or partition fits your project.

## Open-Source LLMs on CPU vs. GPU

Smaller open-source models run on KLC main via the shared [Ollama launcher](/services/klc/user-guide/llm-klc). Larger models and batch inference benefit from Reserve GPU nodes (`sbatch` the same script). See [Open Source LLMs Guide](/guides/llm/llm) for the broader comparison with hosted APIs.

## Related Pages

- [GPU Jobs](gpu-jobs) — how to request and run GPU jobs on `kellogg`
- [When to Use KLC Reserve](when-to-use) — case studies for GPU workloads
- [Launching Jobs on KLC](/services/klc/user-guide/klc-software) — CPU-based work on login nodes
- [Open Source LLMs on KLC](/services/klc/user-guide/llm-klc) — running LLMs (including Ollama) on KLC CPU nodes
- [LLM API Usage](/services/klc/user-guide/llm-api) — hosted LLM APIs from KLC
