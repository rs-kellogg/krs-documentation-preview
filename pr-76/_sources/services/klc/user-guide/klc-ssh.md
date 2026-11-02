# SSH

A plain SSH connection is a text-based terminal session to a KLC node — the lightest-weight of the connection options, and the one that pairs most naturally with scripts, scheduled jobs, and version-controlled code.

Substitute any hostname from the list below for `klc0305` in the examples on this page. See [KLC Login Hostnames](klc-login-hostnames) for how to pick a node.

```{include} _includes/klc-login-hostnames.md
```

## Mac Instructions

Mac computers come with the `Terminal` program already installed as a standard program.

To create a "plain" (not graphical) connection to a specific KLC node, open `Terminal` and type:
```bash
ssh your-netid@klc0305.quest.northwestern.edu
```
If you prefer a graphical (X11) interface, just add the `-Y` option:
```bash
ssh -Y your-netid@klc0305.quest.northwestern.edu
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
ssh your-netid@klc0305.quest.northwestern.edu
```
Occasionally you might receive an error that says something like "host key verification failed." Most of the time, you can fix these problems by deleting your host key file and trying again:
```powershell
Remove-Item ~\.ssh\known_hosts
```

If you need a graphical interface on Windows, connect with [KLC OnDemand](klc-ondemand) or [FastX](klc-fastx). PowerShell's built-in SSH client is for plain terminal sessions only.

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
   ssh-copy-id your_netid@klc0305.quest.northwestern.edu
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

## See Also

- [VS Code with the Remote-SSH extension](klc-vscode) builds a full graphical editor on top of this same SSH connection.
