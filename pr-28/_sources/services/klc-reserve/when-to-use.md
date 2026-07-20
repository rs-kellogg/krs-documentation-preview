# When to Use KLC Reserve

The standard KLC login nodes are shared interactively — many users run on the same node simultaneously. KLC Reserve gives you a dedicated, scheduled allocation. Use Reserve when your job has requirements that don't fit the shared environment.

The case studies below describe the most common reasons to use KLC Reserve.

---

## You Need a GPU

*Coming soon.*

Training or fine-tuning machine learning models, running LLM inference, or any other GPU-accelerated workload requires one of the GPU nodes in KLC Reserve. GPU nodes are not available on the standard KLC login nodes.

**Relevant resources:**
- [GPU Jobs](gpu-jobs)
- [Using GPUs on Quest and KLC](/services/klc/user-guide/klc-gpu)

---

## Your Job Needs More CPU or Memory Than a Login Node Can Spare

*Coming soon.*

Login nodes are shared by many users at once. A job that needs dozens of cores or very large memory for an extended stretch runs better — and more politely — on a scheduled, dedicated node through KLC Reserve.

---

## Your Job Takes Hours or Days

*Coming soon.*

Long-running jobs can be disconnected from a login node if your SSH session drops or the node is restarted. A SLURM batch job through KLC Reserve runs in the background and continues regardless of your connection.

---

## You Need Reproducible, Time-Stamped Compute Environments

*Coming soon.*

SLURM job scripts capture your full environment — modules loaded, resources requested, working directory — making it straightforward to re-run the exact same job or document what resources a result required.

---

## You Need to Run Many Jobs in Parallel

*Coming soon.*

SLURM job arrays let you submit hundreds of independent tasks (different parameters, different data slices) as a single job, with the scheduler managing concurrency automatically.
