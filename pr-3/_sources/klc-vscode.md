# VS Code

[Visual Studio Code](https://code.visualstudio.com/docs/getstarted/getting-started) (VS Code) is a free code editor with strong support for remote development, making it a popular way to edit files and run code directly on KLC.

![Laptop running VS Code with a plan to install VS Code, install extensions, and set up a KLC remote connection](images/vscode-workflow.png)

This page covers connecting to KLC over Remote-SSH. If you'd rather not install anything locally, KLC OnDemand's [VS Code Server](klc-ondemand) gives you the same editor directly in your browser.

## Essential Extensions

Install these from the Extensions view (`Ctrl+Shift+X` / `⌘⇧X`):

- **Remote - SSH** (`ms-vscode-remote.remote-ssh`) — connect to a remote machine like KLC and work with its files and terminal as if they were local.
- **Remote Explorer** (`ms-vscode.remote-explorer`) — a graphical view of your SSH targets and remote sessions.
- **Python** (`ms-python.python`) — code intelligence, linting, and debugging for Python.
- **Jupyter** (`ms-toolsai.jupyter`) — open and run Jupyter Notebooks inside VS Code.
- **GitHub Copilot** (`github.copilot`) — AI pair programmer that suggests code completions.
- **GitHub Copilot Chat** (`github.copilot-chat`) — ask Copilot questions, get code explanations, or generate snippets via natural language.

## Connecting to KLC

1. Open the Command Palette (`Ctrl+Shift+P` / `⌘⇧P`) and select **Remote-SSH: Connect to Host**.
2. Select **Add New SSH Host** and enter:

   ```
   ssh your-netid@klc0202.quest.northwestern.edu
   ```

3. VS Code opens a new window connected to that node. Use **File → Open Folder** to browse to your home directory or a Kellogg project directory.

:::{note}
To skip typing your password on every connection, set up [passwordless SSH login](klc-ssh) first.
:::

## Keyboard Shortcuts

| Action | macOS | Windows |
|---|---|---|
| **Activate Copilot inline chat** | `⌘I` | `Ctrl+I` |
| **Comment line** | `⌘/` | `Ctrl+/` |
| **Increase indent** | `⌘]` | `Ctrl+]` |
| **Decrease indent** | `⌘[` | `Ctrl+[` |
| **Go to file** | `⌘P` | `Ctrl+P` |
| **Switch tabs** | `Ctrl+1`, `Ctrl+2`, ... | `Ctrl+1`, `Ctrl+2`, ... |
| **Save** | `⌘S` | `Ctrl+S` |
| **Close tab** | `⌘W` | `Ctrl+W` |
| **Open terminal** | `` Ctrl+` `` | `` Ctrl+` `` |
| **Command palette** | `⌘⇧P` | `Ctrl+Shift+P` |
| **Toggle sidebar** | `⌘B` | `Ctrl+B` |
| **Find in file** | `⌘F` | `Ctrl+F` |
| **Find across files** | `⌘⇧F` | `Ctrl+Shift+F` |

## Bonus

- [tmux cheatsheet](klc-tmux) for managing sessions in the integrated terminal
