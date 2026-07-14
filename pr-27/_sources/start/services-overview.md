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

## Kellogg Datasets

Licensed access to more than 100 research datasets spanning finance, economics, healthcare, marketing, and more — available via WRDS, KLC, Redivis, and other platforms.

**Use Kellogg Datasets when:**
- You need a specific financial, economic, clinical, or consumer dataset
- You want to know what data KRS has licensed access to

→ [Kellogg Datasets](/services/datasets/datasets)

## Kellogg Data Cloud (KDC)

An AWS-hosted data warehouse for running SQL queries against large-scale datasets using Amazon Athena.

**Use KDC when:**
- You need to query structured data at scale using SQL
- You prefer a cloud-based environment over working on a Linux cluster

→ [Kellogg Data Cloud](/services/kellogg-data-cloud/kdc)

## Not Sure?

If you are unsure which service fits your research task, email [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) with a brief description of what you are trying to do. We can advise on the right tool and help you get started.
