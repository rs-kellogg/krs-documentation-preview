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

* **Load a module** (e.g., for R or Stata):

  ```bash
  module load R/4.5.1
  module load stata/17
  ```

  For Python, load `mamba/24.3.0` and activate a conda environment instead of a Python module — see [Conda Environments on KLC](klc-conda.md).

* **Check what you've loaded**:

  ```bash
  module list
  ```

* **Unload a module**:

  ```bash
  module unload R/4.5.1
  ```
* **Remove all modules**:

  ```bash
  module purge
  ```

Modules ensure you're using the correct version of software without interfering with others.

## Run a Script on KLC Main

After you log into a KLC node and activate your environment, run your script at the prompt:

```bash
cd /kellogg/proj/your-netid/project
source activate /kellogg/proj/your-netid/envs/my-project
python my_analysis.py
```

The same pattern works for R, Stata, or any command-line tool. VS Code Remote SSH and OnDemand integrated terminals behave the same way — they run on the KLC node you connected to.

## Capture Logs (Same Idea as SLURM `--output`)

On KLC Reserve, SLURM writes stdout and stderr to the file named in `#SBATCH --output`. On KLC main, nothing captures output automatically — you set that up yourself. Use both of the patterns below for a complete record.

### In the Script: Python Logging

Use Python's built-in `logging` module for timestamps, severity levels, and clear progress messages. `print()` alone is a poor audit trail — it has no timestamps and mixes with other terminal output.

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)
logger = logging.getLogger(__name__)

logger.info("Starting analysis")
# ... your work ...
logger.info("Finished row %d of %d", i, total)
```

For structured logs inside the script, add a `FileHandler`:

```python
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    handlers=[
        logging.FileHandler("logs/my_analysis.log"),
        logging.StreamHandler(),
    ],
)
```

### At the Shell: Save Terminal Output with `tee`

Capture everything the command prints — including errors — to a file while still watching it in the terminal:

```bash
mkdir -p logs
python starter-code/edgar_analysis.py 2>&1 | tee -a logs/edgar_analysis.log
```

The `2>&1` merges stderr into stdout; `tee -a` appends to the log file. The same pattern works for R, Stata, or any command.

Store log files under `/kellogg/proj/your-netid/`, not your 80 GB home directory. `tmux` scrollback is not a durable log — if the session ends without reattach, that history is gone. VS Code and OnDemand terminals have the same limitation unless you redirect output.

Follow a growing log with `tail -f logs/edgar_analysis.log`. See [Viewing and Editing Files](klc-editor) for other file-viewing commands.

## Keep the Session Alive

For jobs that should continue after you disconnect, run them inside a persistent session:

* Use **FastX**, a graphical remote desktop environment that keeps your session running on the server even if you disconnect.
* Use **`tmux`**, a terminal-based tool that lets you start a session, run your job, and safely disconnect. You can reconnect later and pick up right where you left off. See [Using tmux](klc-tmux.md) for full instructions.

Combine `tmux` and `tee` for long interactive runs — the session survives a disconnect and the log file survives the session:

```bash
tmux new -s my-job
mkdir -p logs
python starter-code/edgar_analysis.py 2>&1 | tee -a logs/edgar_analysis.log
# Press Ctrl+B then D to detach — job keeps running
# Reconnect later with: tmux attach -t my-job
```

## When to Use KLC Reserve

Submit through **KLC Reserve** when you need **GPUs**, **more than 24 CPU cores**, **guaranteed exclusive memory**, or **many parallel jobs** via a SLURM job array — not because KLC main cannot run overnight or produce log files. SLURM reserves resources exclusively for your job and runs it whether you are logged in or not.

See [When to Use KLC Reserve](/services/klc-reserve/when-to-use) for the full decision framework, and [Submitting SLURM Jobs](/services/klc-reserve/slurm-jobs) for how-to instructions.
