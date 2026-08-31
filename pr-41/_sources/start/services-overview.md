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
- Your job needs dozens of CPU cores or very large exclusive memory
- You want scheduled batch jobs with dedicated resources or job arrays

→ [Kellogg Linux Cluster Reserve](/services/klc-reserve/klc-reserve)

## Other Northwestern Resources

These university-wide resources are operated by Northwestern IT, not Kellogg Research Support.

### Quest General Access GPUs

Northwestern-wide NVIDIA GPU nodes (A100 and H100) on the **`gengpu` partition** — for workloads that need GPUs at scale beyond what Kellogg Reserve provides.

**Use `gengpu` when:**
- Your GPU workflow is already working on KLC Reserve and you need more cards or concurrent GPU jobs
- You hold a Quest allocation and want access to the larger General Access GPU pool

Test on [KLC Reserve](/services/klc-reserve/klc-reserve) first, then scale out to `gengpu`.

→ [GPU Concepts and Options](/services/klc-reserve/gpu-concepts) · [GPUs on Quest](https://rcdsdocs.it.northwestern.edu/systems/quest/user-guide/gpu/gpu.html)

## Not Sure?

If you are unsure which service fits your research task, email [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) with a brief description of what you are trying to do. We can advise on the right tool and help you get started.
