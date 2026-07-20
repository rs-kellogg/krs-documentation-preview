# VS Code Workflow for KLC

This guide walks through setting up **Visual Studio Code** with the Remote SSH extension to develop and run code on KLC directly from your laptop, and optionally enabling **GitHub Copilot** as an AI coding assistant.

The scripts and materials for the companion workshop are available in the [GitHub repository](https://github.com/rs-kellogg/krs-KLCworkflow-cookbook).

## System Overview

This workflow connects three components:

- **Your local machine** – runs VS Code and serves as the interface
- **KLC** – where your code actually executes, with access to datasets and compute
- **GitHub** – stores your code and enables collaboration and version control

## Local Machine Setup

Install the following before connecting to KLC.

### 1. Install VS Code

Download and install from [code.visualstudio.com](https://code.visualstudio.com/).

### 2. Install VS Code Extensions

Open the Extensions panel (`Ctrl+Shift+X` / `Cmd+Shift+X`) and install:

| Extension ID | Purpose |
|---|---|
| `ms-vscode-remote.remote-ssh` | Connect to KLC over SSH |
| `ms-vscode.remote-explorer` | Browse remote connections |
| `ms-python.python` | Python language support |
| `ms-toolsai.jupyter` | Run Jupyter notebooks |
| `github.copilot` | AI code suggestions |
| `github.copilot-chat` | AI chat for code (may not work on all systems) |

### 3. Install Git, Python, and Conda

- **Git**: [git-scm.com](https://git-scm.com/)
- **Python**: [python.org/downloads](https://www.python.org/downloads/)
- **Conda/Mamba**: [conda installation guide](https://docs.conda.io/projects/conda/en/latest/user-guide/install/index.html)

## GitHub Setup

1. Create a [GitHub account](https://github.com/) if you don't have one.
2. Sign up for [GitHub Copilot](https://github.com/features/copilot) — a free tier is available.
3. Set up SSH keys for KLC following the [passwordless SSH instructions](klc-accessing.md).

## Connecting VS Code to KLC

1. Open the Command Palette (`Ctrl+Shift+P` / `Cmd+Shift+P`) and run **Remote-SSH: Connect to Host…**
2. Enter a KLC node address, e.g. `your-netid@klc0305.quest.northwestern.edu`
3. VS Code opens a remote window connected to KLC. You can now open folders, edit files, and run terminals on KLC just as you would locally.

```{tip}
Once connected, use VS Code's integrated terminal (`Ctrl+\``) to run commands on KLC — `module load`, `mamba activate`, job scripts, etc.
```

## GitHub Copilot in VS Code

Once the Copilot extension is installed and you're signed in with your GitHub account:

- **Inline suggestions** appear automatically as you type — press `Tab` to accept
- **Copilot Chat** (`Ctrl+Alt+I`) lets you describe what you want in plain English and Copilot writes or explains code

Copilot is especially useful for:
- Writing boilerplate (file I/O, argument parsing, logging)
- Understanding unfamiliar code — highlight and ask "explain this"
- Generating unit tests

```{note}
GitHub Copilot does not have access to your KLC data or files. Avoid pasting sensitive or proprietary data directly into Copilot Chat prompts.
```

## Recommended Workflow

A typical session on KLC via VS Code:

1. **Connect** via Remote-SSH
2. **Open your project folder** on KLC (`/kellogg/proj/<your-netid>/…`)
3. **Activate your conda environment** in the integrated terminal:
   ```bash
   module load mamba
   source activate /kellogg/proj/<your-netid>/envs/<env-name>
   ```
4. **Edit code** with Copilot suggestions inline
5. **Run scripts** in the terminal or open Jupyter notebooks via the Jupyter extension
6. **Commit and push** changes to GitHub from the Source Control panel

## Additional Resources

- [VS Code Remote Development documentation](https://code.visualstudio.com/docs/remote/remote-overview)
- [GitHub Copilot documentation](https://docs.github.com/en/copilot)
- [Conda environments on KLC](klc-conda.md)
- [Using Git on KLC](klc-git.md)
