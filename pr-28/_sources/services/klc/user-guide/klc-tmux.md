# Using tmux

## Introduction to `tmux`

`tmux` is a powerful command-line tool that allows users to manage multiple terminal sessions within a single window.    

With `tmux`, you can:
- Split your terminal into multiple panes
- Run multiple shell sessions simultaneously
- Detach from a session and return later — ideal for long-running tasks
- Keep your work alive on remote systems, even after disconnecting




## Basic Usage of `tmux`

Below are the essential commands to help you begin using `tmux`.

###  Starting a New tmux Session

```bash
tmux
```

This opens a new session. You can run commands here just like a regular terminal.

Or, to name your session:

```bash
tmux new -s mysession
```

### Detaching and Reattaching

- Detach (leave the session running in the background):

  ```
  Ctrl + b, then press d
  ```

- Reattach to an existing session:

  ```bash
  tmux attach-session -t mysession
  ```

- List all sessions:

  ```bash
  tmux ls
  ```

### Splitting the Screen

Split your terminal into multiple panes to multitask efficiently:

- Horizontal split:

  ```
  Ctrl + b, then press "
  ```

- Vertical split:

  ```
  Ctrl + b, then press %
  ```

- Switch between panes:

  ```
  Ctrl + b, then use arrow keys
  ```

---

### Creating and Managing Windows

Each window is like a new tab inside your tmux session:

- New window:

  ```
  Ctrl + b, then press c
  ```

- Switch windows:

  ```
  Ctrl + b, then press n (next) or p (previous)
  ```

- List windows:

  ```
  Ctrl + b, then press w
  ```

### Ending a Session

To end your session, simply type `exit` in each pane or window. When all windows are closed, the session ends.

Or, kill it directly:

```bash
tmux kill-session -t mysession
```


## `tmux` Basic Essentials Cheatsheet 📄
| Action                         | Command                        |
|--------------------------------|--------------------------------|
| Start a new session            | `tmux`                         |
| Reattach to last session       | `tmux attach` or `tmux a`      |
| Detach from session            | `Ctrl+b`, then `d`             |
| Create new window              | `Ctrl+b`, then `c`             |
| Switch window (next/prev)      | `Ctrl+b`, then `n` / `p`       |
| Close pane/window              | `exit` or `Ctrl+d`             |

For handling more than one tmux sessions:
| Action                         | Command                        |
|--------------------------------|--------------------------------|
| List sessions                  | `tmux ls`                      |
| Start a named session          | `tmux new -s mysession`        |
| Attach to a named session      | `tmux attach -t mysession`     |

