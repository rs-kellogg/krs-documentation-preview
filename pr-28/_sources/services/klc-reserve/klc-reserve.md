(klc-reserve)=
# Kellogg Linux Cluster Reserve

**Kellogg Linux Cluster Reserve (KLC Reserve)** gives you access to dedicated compute resources through the **SLURM job scheduler** — including GPU nodes and high-core-count batch nodes that are not available on the standard KLC login nodes.

KLC Reserve resources are accessed by submitting jobs to the `kellogg` SLURM partition from a KLC node. Unlike the standard KLC login nodes (which are shared interactively), Reserve resources are allocated exclusively to your job for its duration.

## Available Resources

| Resource Type | Nodes | Key Specs | Best For |
|---|---|---|---|
| GPU — H100 | TBD | TBD | Large-scale LLM training/inference, deep learning |
| GPU — A100 | TBD | TBD | GPU-accelerated computation, ML training |
| GPU — L40S | TBD | TBD | LLM inference, rendering, general GPU workloads |
| High-memory CPU | TBD | TBD | Very large in-memory datasets, parallel jobs |

Contact [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) for current availability and to request access.

## Getting Access

KLC Reserve uses the same account as the standard KLC. If you already have a KLC account, you can submit to the `kellogg` partition without additional setup. Contact [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) if your jobs fail to submit or if you need a resource allocation increase.

## When Should I Use KLC Reserve?

See [When to Use KLC Reserve](when-to-use) for case studies comparing Reserve to standard KLC login nodes.

## How to Submit Jobs

See [Submitting SLURM Jobs](slurm-jobs) for a guide to writing and submitting batch and interactive SLURM jobs on the `kellogg` partition.

```{toctree}
:maxdepth: 1
:hidden:

When to Use KLC Reserve <when-to-use>
Submitting SLURM Jobs <slurm-jobs>
GPU Jobs <gpu-jobs>
```
