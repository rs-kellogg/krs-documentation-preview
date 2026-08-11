(klc)=
# Kellogg Linux Cluster

The Kellogg Linux Cluster (KLC) is a set of high-memory Linux servers available to Kellogg researchers for interactive computing, large-scale data analysis, and batch jobs. KLC is part of Northwestern's Quest cluster, sharing its file systems and software module library. You can submit a SLURM script from a KLC node to run jobs on Quest, but everyday KLC work (interactive sessions, scripts, batch jobs) doesn't require SLURM at all. Each node has 1.5–2 TB of RAM and up to 64 CPU cores.

::::{grid} 2
:gutter: 3

:::{grid-item-card} New to KLC?
:shadow: sm

The Getting Started guide walks you through getting an account, connecting, setting up your environment, and running your first job.

```{button-ref} /start/klc/klc-intro
:color: primary

Getting Started with KLC
```
:::

:::{grid-item-card} Know what you need?
:shadow: sm

The User Guide covers all KLC topics in depth: connecting, storing data, transferring files, scheduling jobs, accessing GPUs, and more.

```{button-ref} user-guide/klc-user-guide
:color: secondary

KLC User Guide
```
:::

:::{grid-item-card} Need a GPU or a long job?
:shadow: sm

KLC Reserve lets you use the SLURM job scheduler to reserve resources beyond what the shared login node provides.  This includes more than 24 cores on a single node, high-memory nodes, or GPU nodes.

```{button-ref} /services/klc-reserve/klc-reserve
:color: secondary

KLC Reserve
```
:::
::::

## KLC and KLC Reserve

KLC Reserve uses the same Northwestern NetID, KLC account, and Kellogg file systems as standard KLC login access. Reserve is where you submit SLURM jobs to the `kellogg` partition from any KLC node to access a KLC GPU node, high memory node, or full-node core counts that are not available on shared login nodes.

For the decision between direct login and scheduled jobs, see [When to Use KLC Reserve](/services/klc-reserve/when-to-use). For Reserve overview, resource specs, and your first submission, see [Kellogg Linux Cluster Reserve](/services/klc-reserve/klc-reserve).

## Quest Documentation

KLC is part of Quest. Northwestern RCDS maintains comprehensive documentation for Quest that applies to KLC as well:

* [Quest Overview](https://rcdsdocs.it.northwestern.edu/systems/quest/quest.html)
* [Quest User Guide](https://rcdsdocs.it.northwestern.edu/systems/quest/user-guide/quest-user-guide.html) — connecting, storage, data transfer, software modules, SLURM, GPUs
* [Quest Data Security Guidance](https://www.it.northwestern.edu/departments/it-services-support/research/computing/quest/data-security-guidance.html)


```{toctree}
:maxdepth: 1
:hidden:

Kellogg Linux Cluster Overview <https://www.kellogg.northwestern.edu/academics-research/research-support/computing/kellogg-linux-cluster/>
KLC User Guide <user-guide/klc-user-guide>
Datasets on KLC <klc-datasets>
Quest Documentation <https://rcdsdocs.it.northwestern.edu/systems/quest/quest.html>
Quest Data Security Guidance <https://www.it.northwestern.edu/departments/it-services-support/research/computing/quest/data-security-guidance.html>
```
