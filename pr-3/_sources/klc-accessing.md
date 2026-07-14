# Logging Into KLC

There are four ways to connect to a KLC node:

- **[KLC OnDemand](klc-ondemand)** — a browser-based interface with no installation required
- **[SSH](klc-ssh)** — a plain terminal connection
- **[VS Code with the Remote-SSH extension](klc-vscode)** — a graphical editor built on top of an SSH connection
- **[FastX](klc-fastx)** — a full graphical desktop

Not sure which one to use? Read on.

## Which One Should I Use?

**Start with KLC OnDemand if you're not sure.** It's browser-based, so there's nothing to install and no SSH client to configure — click a link, log in with your NetID, and launch a graphical desktop, Jupyter, RStudio, or VS Code session directly. It also tracks your sessions across nodes for you: log back in to **My Interactive Sessions** and any running session shows up regardless of which KLC node it's on. See [KLC OnDemand](klc-ondemand) for a full walkthrough.

**Use plain SSH for anything you'll do repeatedly or want to reproduce.** A plain-text terminal connection is the fastest of the four options and pairs naturally with scripts, scheduled jobs, and version-controlled code. Point-and-click interfaces are convenient and intuitive, but they don't leave behind a record of what you did. If reproducibility matters for your work — and on a shared research computing cluster, it usually does — it's worth becoming comfortable making SSH connections and using the command line, at least occasionally. See [SSH](klc-ssh) for setup instructions.

**Use VS Code with the Remote-SSH extension for active development.** Under the hood it's still an SSH connection, so you keep the same reproducibility benefits, but it adds a graphical editor, integrated terminal, file explorer, and Git/Copilot support on top. See [VS Code](klc-vscode) for setup instructions.

**Use FastX only when you need a full graphical desktop.** Some software (MATLAB, Stata, SAS, or anything else that's GUI-only) needs a real X11 desktop, not just a text terminal or code editor. FastX is relatively fast compared to other X11 tools, and sessions persist even if you disconnect. A few things to know: graphical interfaces are inherently slower than text ones — a program that opens instantly over plain SSH can take several seconds over X11; FastX doesn't include file transfer, so you'll need a separate program like Cyberduck (see [Transferring Files](klc-transferfiles)) to move files to and from KLC, whereas most SSH clients handle that natively; and unlike KLC OnDemand, FastX won't surface a previous session for you automatically — you have to remember and reconnect to the specific node it was launched on. See [FastX](klc-fastx) for connection details.

**Bottom line:** default to SSH — plain or through VS Code — for day-to-day work, since it's fastest and keeps your work reproducible. Reach for KLC OnDemand when you want zero setup, and FastX when you specifically need a graphical desktop application.
