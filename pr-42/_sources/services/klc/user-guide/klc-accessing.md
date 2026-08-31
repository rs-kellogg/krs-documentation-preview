# Logging Into KLC

There are four ways to connect to a KLC node:

- **[KLC OnDemand](klc-ondemand)** — browser-based interface with no installation required
- **[SSH](klc-ssh)** — plain terminal connection
- **[VS Code with the Remote-SSH extension](klc-vscode)** — graphical editor built on top of an SSH connection
- **[FastX](klc-fastx)** — full graphical desktop

## Choose a Connection Method

| Goal | Recommended method |
|---|---|
| Zero local setup; Jupyter, RStudio, or VS Code in the browser | [KLC OnDemand](klc-ondemand) |
| Scripts, automation, and reproducible command-line workflows | [SSH](klc-ssh) |
| Active code development with editor, terminal, and Git | [VS Code + Remote SSH](klc-vscode) |
| GUI-only software (MATLAB, Stata, SAS) | [FastX](klc-fastx) or KLC OnDemand GNOME Desktop |

## Which One Should I Use?

**Start with KLC OnDemand when you want zero setup.** It is browser-based — log in with your NetID and launch a graphical desktop, Jupyter, RStudio, or VS Code session directly. **My Interactive Sessions** tracks running sessions across nodes: log back in and reconnect regardless of which KLC node hosts the session. See [KLC OnDemand](klc-ondemand) for a full walkthrough.

**Use plain SSH for work you will repeat or need to reproduce.** A plain-text terminal connection is the fastest of the four options and pairs naturally with scripts, scheduled jobs, and version-controlled code. Point-and-click interfaces are convenient, but they do not leave behind a command history in the same way. On a shared research cluster, reproducibility matters — use SSH for routine work even when you also use graphical tools. See [SSH](klc-ssh) for setup instructions.

**Use VS Code with the Remote-SSH extension for active development.** Under the hood it is still an SSH connection, so you keep the same reproducibility benefits, with a graphical editor, integrated terminal, file explorer, and Git/Copilot support. See [VS Code](klc-vscode) for setup instructions.

**Use FastX when you need a full graphical desktop outside the browser.** Some software (MATLAB, Stata, SAS, or other GUI-only applications) needs a real X11 desktop. FastX sessions persist after disconnect, with these tradeoffs:

- Graphical interfaces are slower than text terminals — a program that opens instantly over SSH can take several seconds over X11
- FastX does not include file transfer; use [Transferring Files](klc-transferfiles) or an SSH client with built-in transfer
- Unlike KLC OnDemand, FastX does not list sessions across nodes — reconnect to the **same KLC node** where you launched the session

See [FastX](klc-fastx) for connection details.

**Default to SSH — plain or through VS Code — for day-to-day work.** Use KLC OnDemand when you want zero setup, and FastX when you specifically need a graphical desktop application outside the browser.
