(services-overview)=
# What Does KRS Offer?

Kellogg Research Support (KRS) provides computing infrastructure, data access, and technical support for Kellogg faculty and doctoral students. This page describes each service and helps you find the right one for your work.

## Kellogg Linux Cluster (KLC)

High-memory Linux servers for interactive computing, large-scale data analysis, and batch jobs.

**Use KLC when:**
- Your analysis is too slow or memory-intensive for a laptop
- You need to process large files or run jobs overnight
- You want access to datasets stored directly on the cluster
- You need a reproducible, shared computing environment

→ [Getting Started with KLC](klc/klc-intro) · [KLC User Guide](/services/klc/user-guide/klc-user-guide)

## Quest GPU Nodes

NVIDIA GPU nodes (L40S, A100, H100) for deep learning and large language model workloads, accessible via SLURM from KLC using `--partition=kellogg`.

**Use GPU nodes when:**
- You are training or running large language models
- Your code uses PyTorch, TensorFlow, or another GPU-accelerated framework
- Your workload involves matrix operations that benefit from parallel processing

→ [Using GPUs on Quest and KLC](/services/klc/user-guide/klc-gpu)

## Kellogg Data Hosting

WRDS, Amazon Athena, and Redivis — the three platforms through which KRS provides access to licensed research datasets.

**Use Kellogg Data Hosting when:**
- You need a specific financial, economic, clinical, or consumer dataset
- You want to query data through WRDS, Athena (SQL), or Redivis (browser-based)
- You want to know what data KRS has licensed access to and where it lives

→ [Kellogg Data Hosting](/services/kellogg-data-hosting/kdc) · [Find Data by Platform](/services/datasets/by-platform)

## Kellogg Linux Cluster Reserve

Dedicated GPU and high-memory compute nodes accessed through the SLURM job scheduler — for workloads that need more than a shared login node can provide.

**Use KLC Reserve when:**
- You are training or running machine learning models and need a GPU
- Your job needs dozens of CPU cores or very large memory for an extended period
- You want reproducible, scheduled batch jobs

→ [Kellogg Linux Cluster Reserve](/services/klc-reserve/klc-reserve)

## Not Sure?

If you are unsure which service fits your research task, email [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) with a brief description of what you are trying to do. We can advise on the right tool and help you get started.
