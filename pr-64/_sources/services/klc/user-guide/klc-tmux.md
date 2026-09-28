# Using tmux

On KLC, `tmux` keeps terminal sessions alive on the node where you started them — so long-running commands continue if your SSH connection drops and you can reattach later. Use `tmux` for any interactive job that should survive a disconnect, including runs that last hours.

For jobs that need **dedicated resources**, **more than 24 CPU cores**, **GPUs**, or **many parallel tasks**, submit a [SLURM batch job](/services/klc-reserve/slurm-jobs) on KLC Reserve instead.

## Why Use tmux on KLC

- **Survive disconnects** — close your laptop; the process keeps running on the KLC node
- **Multitask in one window** — split the terminal into panes for editing, running, and monitoring
- **Return later** — detach and reattach from another machine

:::{warning}
A `tmux` session exists only on the **node where you created it**. If you SSH to `klc0305` and start `tmux`, you must SSH to `klc0305` again to reattach. Sessions do not follow you across nodes.
:::

## Basic Usage

### Start a Session

```bash
tmux
```

Or name the session:

```bash
tmux new -s mysession
```

Run commands as in a normal terminal. To save output to a log file while the job runs, redirect with `tee`:

```bash
mkdir -p logs
python my_analysis.py 2>&1 | tee -a logs/my_analysis.log
```

See [Launching Jobs on KLC](klc-software) for Python `logging` and the full logging pattern.

### Detach and Reattach

Detach (leave the session running):

```
Ctrl + b, then press d
```

Reattach:

```bash
tmux attach-session -t mysession
```

List sessions:

```bash
tmux ls
```

### Split the Screen

Horizontal split:

```
Ctrl + b, then press "
```

Vertical split:

```
Ctrl + b, then press %
```

Switch panes:

```
Ctrl + b, then use arrow keys
```

### Scroll Through Output (Copy Mode)

`tmux` does not scroll with the mouse by default. Enter copy mode to review long output:

```
Ctrl + b, then press [
```

Use arrow keys or Page Up/Down to scroll. Press `q` to exit copy mode.

### Windows (Tabs)

New window:

```
Ctrl + b, then press c
```

Switch windows:

```
Ctrl + b, then press n (next) or p (previous)
```

List windows:

```
Ctrl + b, then press w
```

### End a Session

Type `exit` in each pane, or kill the session directly:

```bash
tmux kill-session -t mysession
```

## tmux Essentials Cheatsheet

| Action | Command |
|---|---|
| Start a new session | `tmux` |
| Start a named session | `tmux new -s mysession` |
| Reattach to last session | `tmux attach` or `tmux a` |
| Detach from session | `Ctrl+b`, then `d` |
| List sessions | `tmux ls` |
| Attach to a named session | `tmux attach -t mysession` |
| Create new window | `Ctrl+b`, then `c` |
| Switch window (next/prev) | `Ctrl+b`, then `n` / `p` |
| Scroll output (copy mode) | `Ctrl+b`, then `[` |
| Close pane/window | `exit` or `Ctrl+d` |

## When tmux Is Not Enough

Move to [KLC Reserve](/services/klc-reserve/klc-reserve) when:

- The job needs **more than 24 CPU cores** or **guaranteed exclusive memory**
- You need a **GPU**
- You want to submit **many parallel jobs** with a job array

See [When to Use KLC Reserve](/services/klc-reserve/when-to-use) for the full decision framework.

## Related Pages

- [Launching Jobs on KLC](klc-software) — scripts, logging, and `tmux` on KLC main
- [When to Use KLC Reserve](/services/klc-reserve/when-to-use) — interactive vs. scheduled work
- [Submitting SLURM Jobs](/services/klc-reserve/slurm-jobs) — batch jobs that outlive any terminal session
