# GitHub Copilot

**GitHub Copilot** is an AI coding assistant developed by GitHub and OpenAI. It integrates directly into your editor and helps you write, understand, and debug code faster.

## Ways to Use Copilot

- **Inline suggestions** — Copilot suggests code as you type; press `Tab` to accept
- **Copilot Chat** — Describe what you want in plain English; Copilot writes or explains code
- **Command palette** — Ask Copilot to explain, fix, or generate code on selected text

## Setup in VS Code

1. Install the extensions from the VS Code Marketplace:
   - `github.copilot`
   - `github.copilot-chat`

2. Sign in with your GitHub account when prompted.

3. [Sign up for a Copilot plan](https://github.com/features/copilot) — a free tier is available for individual use. Students and educators may qualify for free access.

For connecting VS Code to KLC via Remote SSH, see the [VS Code Workflow for KLC](../../services/klc/user-guide/klc-vscode) guide.

## Using Copilot for Research Code

Copilot is especially helpful for:

- **Boilerplate code** — file I/O, argument parsing, logging, CSV/JSON handling
- **API calls** — generating OpenAI, Anthropic, or Hugging Face API request patterns
- **Data manipulation** — pandas, NumPy, and SQL query patterns
- **Unit tests** — ask Copilot to generate tests for your functions
- **Understanding unfamiliar code** — highlight a block and ask "explain this"

## Example: Using Copilot Chat

Select a function in your editor, then open Copilot Chat (`Ctrl+Alt+I` / `Cmd+Alt+I`) and ask:

- *"Write a unit test for this function"*
- *"Refactor this to handle a missing file gracefully"*
- *"Explain what this regex pattern matches"*

## Privacy Considerations

```{important}
GitHub Copilot sends your code context to GitHub's servers to generate suggestions. Do not paste sensitive data, API keys, or proprietary research data directly into the editor or Copilot Chat when working with such material.
```

For code that operates on sensitive data, consider:
- Keeping variable names generic while developing
- Using Copilot for the logic/structure, not the data

## Related Pages

- [VS Code Workflow for KLC](../../services/klc/user-guide/klc-vscode) — Full setup guide including Remote SSH
- [OpenAI API](openai-api) — Using the OpenAI API directly in your research code
