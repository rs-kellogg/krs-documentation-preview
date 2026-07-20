# Launching Jobs

```{seealso}
For comprehensive SLURM documentation — partitions, submission scripts, job monitoring commands, fairshare, and interactive jobs — see the [Quest SLURM documentation](https://rcdsdocs.it.northwestern.edu/systems/quest/user-guide/slurm/slurm.html).
```

## Setting Up a Conda/Mamba Environment

Before running a job, set up an isolated Python or R environment using `conda`/`mamba`. See [Conda Environments on KLC](klc-conda.md) for full instructions on creating, activating, exporting, and sharing environments.

## Loading Software with Modules

KLC uses Environment Modules to give users access to the software installed on KLC. See the [Quest Software Module documentation](https://rcdsdocs.it.northwestern.edu/systems/quest/user-guide/modules/modules.html) for a full reference on module commands.

* **List available modules**:

  ```bash
  module avail
  ```

* **Load a module** (e.g., for R or Python):

  ```bash
  module load R
  module load python/3.10
  ```

* **Check what you’ve loaded**:

  ```bash
  module list
  ```

* **Unload a module**:

  ```bash
  module unload R
  ```

Modules ensure you're using the correct version of software without interfering with others.





## Long-Running Jobs

For long-running jobs, it's important to avoid losing progress if your connection drops. You have two main options:

* Use **FastX**, a graphical remote desktop environment that keeps your session running on the server even if you disconnect.
* Use **`tmux`**, a terminal-based tool that lets you start a session, run your job, and safely disconnect. You can reconnect later and pick up right where you left off. [Here](./klc-tmux.md) is detailed information for using `tmux` on KLC.

If your job will run for many hours, needs more than 24 CPU cores, or you want to run many similar jobs in parallel, consider **submitting through SLURM** instead of running directly on a KLC node. SLURM reserves resources exclusively for your job and runs it whether you are logged in or not. See [Interactive Jobs vs. SLURM Batch Jobs](klc-slurm) for a guide on when and how to make the switch.


