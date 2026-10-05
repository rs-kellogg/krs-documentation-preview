# AI Coding Agents on KLC

KLC provides a container module for running command-line AI coding agents — [Claude Code](https://docs.anthropic.com/en/docs/claude-code) and [OpenAI Codex CLI](https://developers.openai.com/codex/cli) — against your project files. The container isolates the agent's runtime from the shared KLC environment and mounts only the project and data directories you specify, so the agent cannot read outside of them.

```{warning}
Coding agents send file contents and prompts to Anthropic's or OpenAI's servers. Follow your IRB protocol and Northwestern data governance policies before pointing an agent at a directory that contains identifiable human-subjects data or other restricted data. See [Data Governance and IRB](llm-api).
```

## 1. Create a Conda/Mamba Environment with Node.js

Both CLI tools need a Node.js runtime (or, for the Claude Code installer, a user-writable location for its install script). Create a dedicated environment in your project directory rather than your home directory — the home directory has an [80 GB quota](klc-files) that is easy to exhaust with Node packages and model caches.

```bash
module load mamba/24.3.0
source /hpc/software/mamba/24.3.0/etc/profile.d/conda.sh

mamba create -p /kellogg/proj/<your-netid>/envs/coding-agent nodejs
mamba activate /kellogg/proj/<your-netid>/envs/coding-agent
```

## 2. Install the CLI Tool

With the environment active, install whichever agent you want to use.

:::::{tab-set}
::::{tab-item} Codex

```bash
npm i -g @openai/codex
```
::::

::::{tab-item} Claude Code

```bash
curl -fsSL https://claude.ai/install.sh | bash
```
::::
:::::

You only need to do this once per environment — the CLI persists in the environment's prefix until you remove or recreate it.

## 3. Load and Launch the Container

Load the container module and launch it with the agent you installed, passing the project directory and (optionally) a data directory to mount:

```bash
module load ai-agent-container

ai_agent_container -a claude /path/to/project /path/to/data
# or
ai_agent_container -a codex /path/to/project /path/to/data
```

Replace `/path/to/project` and `/path/to/data` with the directories the agent needs access to — for example your project repository under `/kellogg/proj/<your-netid>/` and a read-only dataset path under `/kellogg/data/`. The agent cannot see anything outside the paths you pass in.

## 4. Log in to Activate the Agent

The first time you launch, you're prompted to log in to your Anthropic or OpenAI account. If no prompt appears, run the login command inside the agent's session:

```
/login
```

Your login persists for subsequent sessions in the same environment.

## Related Pages

- [Conda/Mamba Environments](klc-conda) — general environment management on KLC
- [LLM API Usage](llm-api) — data governance guidance that also applies to coding agents
- [KLC Filesystem](klc-files) — home directory and project directory quotas
