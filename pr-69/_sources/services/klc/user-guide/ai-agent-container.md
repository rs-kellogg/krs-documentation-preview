# AI Coding Agents on KLC

KLC provides a container module for running command-line AI coding agents — [Claude Code](https://docs.anthropic.com/en/docs/claude-code), [OpenAI Codex CLI](https://developers.openai.com/codex/cli), and GitHub Copilot CLI — against your project files. The container isolates the agent's runtime from the shared KLC environment and mounts only the project and data directories you specify, so the agent cannot read outside of them.

```{warning}
Coding agents send file contents and prompts to Anthropic's, OpenAI's, or GitHub's servers. Follow your IRB protocol and Northwestern data governance policies before pointing an agent at a directory that contains identifiable human-subjects data or other restricted data. See [Data Governance and IRB](llm-api).
```

## 1. Install the CLI Tool

Each CLI installs with a single `curl` command into `~/.local/bin` — no environment setup required. Install whichever agent(s) you want to use.

:::::{tab-set}
::::{tab-item} Copilot CLI

See the [Copilot CLI install instructions](https://docs.github.com/en/copilot/how-tos/copilot-cli/set-up-copilot-cli/install-copilot-cli) for macOS and Linux, or run:

```bash
curl -fsSL https://gh.io/copilot-install | bash
~/.local/bin/copilot --version
```

You need a GitHub account with access to Copilot.
::::

::::{tab-item} Claude Code

See the [Claude Code install instructions](https://docs.anthropic.com/en/docs/claude-code), or run:

```bash
curl -fsSL https://claude.ai/install.sh | bash
~/.local/bin/claude --version
```

You need a Claude account.
::::

::::{tab-item} Codex CLI

See the [Codex CLI documentation](https://developers.openai.com/codex/cli), or run:

```bash
curl -fsSL https://chatgpt.com/codex/install.sh | sh
~/.local/bin/codex --version
```

You need a ChatGPT account with access to Codex.
::::
:::::

If the version check above fails with "command not found," add `~/.local/bin` to your `PATH`:

```bash
export PATH="$HOME/.local/bin:$PATH"
```

## 2. Load and Launch the Container

Load the container module and launch it with the agent you installed, passing the project directory and (optionally) a data directory to mount:

```bash
module load ai-agent-container

ai_agent_container -a claude /path/to/project /path/to/data
# or
ai_agent_container -a codex /path/to/project /path/to/data
# or
ai_agent_container -a copilot /path/to/project /path/to/data
```

Replace `/path/to/project` and `/path/to/data` with the directories the agent needs access to — for example your project repository under `/kellogg/proj/<your-netid>/` and a dataset path under `/kellogg/data/`. The agent cannot see anything outside the paths you pass in.

Append `:ro` to a path to mount it read-only:

```bash
ai_agent_container -a claude /path/to/project /path/to/data:ro
```

Use a read-only mount for reference data or licensed datasets you want the agent to read but never modify or delete.

## 3. Log in to Activate the Agent

The first time you launch, you're prompted to log in to your Anthropic, OpenAI, or GitHub account, depending on the agent. If no prompt appears, run the login command inside the agent's session:

```
/login
```

Your login persists for subsequent sessions in the same environment.

## Related Pages

- [LLM API Usage](llm-api) — data governance guidance that also applies to coding agents
- [KLC Filesystem](klc-files) — home directory and project directory quotas
