# AI Coding Agents on KLC

The `ai-agent-container` module runs GitHub Copilot CLI, Claude Code, or Codex inside a Singularity container on KLC. You choose which directories the container can read or write.

:::{warning}
File contents the agent reads are sent to that vendor. Do not mount directories that contain restricted data. See [Data Security Guidance](https://www.it.northwestern.edu/departments/it-services-support/research/computing/quest/) before you point an agent at project or research files.
:::

## Install the CLI

Install the agent on KLC with the vendor curl script. Each script places the binary in `~/.local/bin`. Each CLI needs an account with that vendor.

::::{tab-set}

:::{tab-item} GitHub Copilot CLI

See the [Copilot CLI install instructions for macOS and Linux](https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/install-copilot-cli#installing-with-the-install-script-macos-and-linux), or run:

```bash
curl -fsSL https://gh.io/copilot-install | bash
~/.local/bin/copilot --version
```

You need a GitHub account with access to Copilot.
:::

:::{tab-item} Claude Code

See the [Claude Code install instructions](https://code.claude.com/docs/en/setup#install-claude-code), or run:

```bash
curl -fsSL https://claude.ai/install.sh | bash
~/.local/bin/claude --version
```

You need a Claude account.
:::

:::{tab-item} Codex

See the [Codex CLI documentation](https://developers.openai.com/codex/cli), or run:

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
~/.local/bin/codex --version
```

You need a ChatGPT account with access to Codex.
:::

::::

## Start the Agent

Load the module, then start an agent with `-a` and at least one directory to mount:

```bash
module load ai-agent-container
ai_agent_container -a copilot /path/to/project
```

Replace `copilot` with `claude` or `codex`, and replace `/path/to/project` with a directory the agent should see.

## Mount Directories

Pass one or more directories after the agent name. Append `:ro` to mount a path read-only. Put `--` before any arguments that should go to the agent program itself.

| Option | Purpose |
|---|---|
| `-a <agent>` | Agent to run (required): `copilot`, `claude`, or `codex` |
| `<directory>` | Bind-mount this path into the container |
| `<directory>:ro` | Bind-mount this path read-only |
| `-- <agent args>` | Arguments passed through to the agent |

These examples show the same options. Run one of them:

```bash
ai_agent_container -a copilot /path/to/project
ai_agent_container -a copilot /path/to/project /path/to/data
ai_agent_container -a claude /path/to/project /path/to/data:ro
ai_agent_container -a codex /path/to/project:ro /path/to/scratch
ai_agent_container -a claude /path/to/project -- --model claude-opus-4-5
ai_agent_container -a codex /path/to/project -- --approval-mode full-auto --quiet
```

## Conda and Mamba Environments

If the agent binary is installed in the active conda environment, the module bind-mounts `$CONDA_PREFIX` and runs the agent from that environment.

The curl installers place the binary in `~/.local/bin`, so that automatic mount does not apply. Mount the directory that contains your project environment when you want the agent to use it.

One practical layout is a parent directory with `envs/` and your repository underneath it. Mount that parent from the agent session, and leave conda inactive there.

## Worked Example

Keep the agent in one [SSH](klc-ssh) session and run your own commands in another. A [tmux](klc-tmux) session is another way to keep the agent process alive if the connection drops.

1. Open two SSH sessions to a KLC login host. Leave the agent running in one session. Use the other session for your own commands.

2. In the work session, create a parent directory, a repository, and a Python environment. The Mamba hook matches [Open Source LLMs on KLC](llm-klc). See [Conda/Mamba Environments](klc-conda) for more on environments.

   ```bash
   mkdir -p ~/agent-work/envs ~/agent-work/repos
   cd ~/agent-work/repos
   git init demo
   module load mamba/24.3.0
   eval "$('/hpc/software/mamba/24.3.0/bin/conda' 'shell.bash' 'hook' 2> /dev/null)"
   source "/hpc/software/mamba/24.3.0/etc/profile.d/mamba.sh"
   mamba create --prefix=~/agent-work/envs/demo python=3.12 --yes
   conda activate ~/agent-work/envs/demo
   ```

3. In the agent session, install the CLI with the curl script above, load the module, and mount the parent directory:

   ```bash
   module load ai-agent-container
   ai_agent_container -a claude ~/agent-work/
   ```

   Substitute `copilot` or `codex` for `claude`. This shell has no active conda environment, so the module cannot see `$CONDA_PREFIX`. Mounting `~/agent-work/` exposes both `repos/demo` and `envs/demo`.

:::{note}
Add R packages to the same environment when the agent needs both Python and R. Install them with `mamba` in the work session. See [Conda/Mamba Environments](klc-conda).
:::

## Sign In the First Time

The first launch prints a URL and a one-time code. Open the URL in a browser on your local machine, then paste the code. On a shared cluster, decline a "stay logged in" prompt when the CLI offers that choice.
