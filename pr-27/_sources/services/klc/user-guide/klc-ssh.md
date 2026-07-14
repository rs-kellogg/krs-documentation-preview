# SSH

A plain SSH connection is a text-based terminal session to a KLC node — the fastest of the connection options, and the one that pairs most naturally with scripts, scheduled jobs, and version-controlled code.

## Mac Instructions

Mac computers come with the `Terminal` program already installed as a standard program.

To create a "plain" (not graphical) connection to a specific KLC node (for instance KLC0202), you would simply open `Terminal` and type:
```bash
ssh your-netid@klc0202.quest.northwestern.edu
```
If you prefer a graphical (X11) interface, just add the `-Y` option:
```bash
ssh -Y your-netid@klc0202.quest.northwestern.edu
```
Occasionally you might receive an error that says something like "host key verification failed." Most of the time, you can fix these problems by deleting your host key file and trying again:
```bash
rm ~/.ssh/known_hosts
```

:::{note}
Depending on the version of your Mac, you might need to install the free `XQuartz` application before X11 forwarding will work.
:::

## Windows Instructions

Windows 10 and later come with an SSH client built in, so there's nothing to install for a plain-text connection. Open `PowerShell` and type:
```powershell
ssh your-netid@klc0202.quest.northwestern.edu
```
Occasionally you might receive an error that says something like "host key verification failed." Most of the time, you can fix these problems by deleting your host key file and trying again:
```powershell
Remove-Item ~\.ssh\known_hosts
```

:::{note}
PowerShell's built-in SSH client doesn't include an X server, so it can't display graphical (X11) applications. If you need a graphical interface, use [KLC OnDemand](klc-ondemand) or [FastX](klc-fastx) instead — both are easier to set up on Windows than a third-party X11 SSH client.
:::

If you still want a graphical (X11) interface, a saved session manager, or other conveniences PowerShell doesn't offer, install a dedicated SSH client — `MobaXterm` is a popular choice with a solid free version. Note that support for MobaXterm is not provided by Research Support or KIS; consider the Pro version if you need technical help. Other options include `SecureCRT`, `PuTTY`, and `Cygwin`.

Common instructions for using these clients (may differ slightly for different clients):
- In the Sessions menu, select SSH.
- In Remote Host, give the address of the server (e.g. any KLC login node address: `klc0202.quest.northwestern.edu`)
- Specify your NetID as the username.
- Under Advanced SSH settings, check the box for X11-Forwarding if you want a graphical interface; leave it unchecked for a plain text interface.
- If you work on remote servers regularly, you will find it convenient to save and label a set of commonly used sessions.

## Passwordless SSH Login

**Passwordless SSH login** allows you to securely access remote servers without typing your password each time. It uses **SSH key pairs** (public/private keys) for authentication instead of passwords.

Benefits:
- **Convenience**: No need to repeatedly enter passwords when logging in or running automated tasks.
- **Security**: Stronger authentication using cryptographic keys, reducing the risk of brute-force attacks.
- **Automation**: Essential for running scripts, transferring files, or syncing data across servers without manual intervention.
- **Faster access**: Speeds up workflows for data analysis, code deployment, or managing remote jobs.

[Video instructions](https://kellogg-shared.s3.us-east-2.amazonaws.com/videos/sshpasswordless_login.mp4)

Text instructions:

1. Generate an SSH key pair.

   Run the following command in the **Terminal** app on macOS or **Command Prompt**/**PowerShell** on Windows:
   ```bash
   ssh-keygen -t rsa
   ```

   After running this, two files are created in your `~/.ssh` directory:

   | File | Description |
   |---|---|
   | `id_rsa` | Your **private** key — keep this secure and never share it |
   | `id_rsa.pub` | Your **public** key — safe to share with servers |

2. Copy the public key `id_rsa.pub` to KLC.

   On macOS or Linux, run the following command in the **Terminal**:
   ```bash
   ssh-copy-id your_netid@klc0202.quest.northwestern.edu
   ```

   To add it manually (works for all OS):
   - On your local machine, open `id_rsa.pub` in a text editor and copy its contents.
   - Open an SSH session to KLC, and create the `.ssh` directory if it doesn't exist:
     ```bash
     mkdir -p ~/.ssh
     ```
   - Then paste the contents of `id_rsa.pub` into the file:
     ```bash
     nano ~/.ssh/authorized_keys
     ```

3. Update permissions on KLC.

   Open an SSH session to KLC and update permissions:
   ```bash
   chmod 700 ~/.ssh
   chmod 600 ~/.ssh/authorized_keys
   ```

## Bonus

- [VS Code with the Remote-SSH extension](klc-vscode) builds a full graphical editor on top of this same SSH connection.
