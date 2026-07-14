(introduction-to-klc)=
# Introduction to Kellogg Linux Cluster

The **Kellogg Linux Cluster (KLC)** is a set of high-memory Linux servers available to Kellogg researchers for interactive computing, data analysis, and running computationally intensive jobs. If your analysis is too slow on a laptop, requires more memory than you have locally, or needs to run overnight, KLC is the right tool.

## What KLC Offers

* **Large memory** — each node has 1.5–2 TB of RAM, far more than any laptop
* **Many CPU cores** — up to 64 cores per node for parallel workloads
* **Large storage** — 2 TB of project storage per researcher, separate from your home directory
* **Shared datasets** — curated research datasets pre-loaded and ready to use
* **Scientific software** — the same software library as Northwestern Quest, available via `module load`
* **Reproducible workflows** — run the same code on the same hardware every time

## KLC Architecture

KLC consists of 12 high-memory Linux nodes:

| Nodes | CPU Cores | RAM |
|---|---|---|
| klc0304 – klc0307, klc0401, klc0402, klc0503 (latest gen) | 64 cores | 2 TB |
| klc0202, klc0203, klc0301 – klc0303 | 52 cores | 1.5 TB |

All nodes share the same file systems, so a file saved on one node is accessible from any other.

**Usage policy:** Each user may use up to 24 CPU cores concurrently at normal priority. Going beyond this reduces priority for all your processes. Contact [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) if your work regularly needs more than 24 cores.

## Getting Started: Step by Step

### Step 1 — Get an Account

If you do not already have a KLC account, contact Kellogg Research Support at [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu).

### Step 2 — Connect to KLC

**KLC OnDemand (zero setup — start here if you're not sure)**

Go to [Quest OnDemand](https://ondemand.quest.northwestern.edu), log in with your NetID, and select the **Kellogg Linux Cluster** profile. From there you can launch Jupyter, RStudio, VS Code, or a full graphical desktop directly in your browser — nothing to install or configure. Full walkthrough: [KLC OnDemand](/services/klc/user-guide/klc-ondemand)

**SSH (command line)**

On **Mac**, open the built-in **Terminal** app and run:

```bash
ssh your-netid@klc0305.quest.northwestern.edu
```

On **Windows**, open **PowerShell** and run:

```powershell
ssh your-netid@klc0305.quest.northwestern.edu
```

Set up [passwordless SSH login](/services/klc/user-guide/klc-ssh) to avoid entering your password each time. Full instructions: [SSH](/services/klc/user-guide/klc-ssh)

**VS Code with Remote SSH (recommended for development)**

Connect VS Code directly to KLC and edit files, run notebooks, and use GitHub Copilot — all from your laptop. See [VS Code Workflow for KLC](/services/klc/user-guide/klc-vscode).

**FastX (full graphical desktop)**

For software that requires a full X11 desktop — MATLAB, Stata, SAS. See [FastX](/services/klc/user-guide/klc-fastx).

### Step 3 — Understand Your Storage

Once connected, you have two storage locations:

| Location | Path | Quota | Purpose |
|---|---|---|---|
| Home directory | `/home/your-netid/` | 80 GB | Personal files, config, small scripts |
| Project directory | `/kellogg/proj/your-netid/` | 2 TB | Data, conda environments, job output |

**Always store data and environments in your project directory** — the home directory fills up quickly.

Full details: [KLC Filesystem](/services/klc/user-guide/klc-files)

### Step 4 — Set Up a Python or R Environment

KLC uses `mamba` (a faster version of `conda`) to manage software environments. Create an isolated environment in your project directory:

```bash
module load mamba
mamba create -p /kellogg/proj/your-netid/envs/my-project python=3.11
source activate /kellogg/proj/your-netid/envs/my-project
mamba install pandas numpy matplotlib
```

Full details: [Conda Environments on KLC](/services/klc/user-guide/klc-conda)

### Step 5 — Run Your First Script

With your environment active, run a Python script:

```bash
python my_analysis.py
```

For long-running jobs, wrap your session in `tmux` first so it keeps running if you disconnect:

```bash
tmux new -s my-job
python my_analysis.py
# Press Ctrl+B then D to detach — job keeps running
# Reconnect later with: tmux attach -t my-job
```

Full details: [Launching Jobs](/services/klc/user-guide/klc-software) · [Using tmux](/services/klc/user-guide/klc-tmux)

## Key Things to Know

* **Do not run heavy jobs on the login node.** Start a `tmux` session for anything that runs more than a few seconds.
* **Use your project directory for data and environments**, not your home directory.
* **Load software with `module load`** before using R, Stata, or system Python versions: `module load R`, `module load stata`.
* **Check memory usage** before starting large jobs: `module load glances && glances` shows all users' CPU and memory in real time.

## Where to Go Next

| Goal | Page |
|---|---|
| Connect and log in | [Access KLC](/services/klc/user-guide/klc-accessing) |
| Set up a development environment | [Conda Environments](/services/klc/user-guide/klc-conda) |
| Transfer files to/from KLC | [Transferring Files](/services/klc/user-guide/klc-transferfiles) |
| Keep jobs running after disconnect | [Using tmux](/services/klc/user-guide/klc-tmux) |
| Full reference documentation | [KLC User Guide](/services/klc/user-guide/klc-user-guide) |
| Use VS Code with KLC | [VS Code Workflow](/services/klc/user-guide/klc-vscode) |
| Use LLMs on KLC | [Open Source LLMs](/services/klc/user-guide/llm-klc) |
| SLURM job scheduler (deep reference) | [Quest SLURM docs](https://rcdsdocs.it.northwestern.edu/systems/quest/user-guide/slurm/slurm.html) |
| Software modules reference | [Quest Modules docs](https://rcdsdocs.it.northwestern.edu/systems/quest/user-guide/modules/modules.html) |
| Filesystem quotas and permissions | [Quest Filesystem docs](https://rcdsdocs.it.northwestern.edu/systems/quest/user-guide/filesystem/filesystem.html) |
| Login methods (SSH, FastX, OnDemand) | [Quest Login docs](https://rcdsdocs.it.northwestern.edu/systems/quest/user-guide/login/login-quest.html) |
| SLURM jobs on Kellogg partition | [Interactive vs. SLURM Batch](/services/klc/user-guide/klc-slurm) |
| GPU jobs on Quest | [Using GPUs on Quest and KLC](/services/klc/user-guide/klc-gpu) |
