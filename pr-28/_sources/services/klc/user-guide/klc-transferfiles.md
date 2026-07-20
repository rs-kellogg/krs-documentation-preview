# Transferring Files

## Command Line (scp / rsync / sftp)

For quick transfers from your local machine's terminal, use `scp` or `rsync`.

**Copy a single file to KLC:**
```bash
scp localfile.csv your-netid@klc0305.quest.northwestern.edu:/kellogg/proj/your-netid/data/
```

**Copy a directory to KLC:**
```bash
scp -r local-project/ your-netid@klc0305.quest.northwestern.edu:/kellogg/proj/your-netid/
```

**Copy a file from KLC to your local machine:**
```bash
scp your-netid@klc0305.quest.northwestern.edu:/kellogg/proj/your-netid/results/output.csv ~/Desktop/
```

**Sync a directory (only transfers changed files — preferred for large datasets):**
```bash
rsync -avz local-project/ your-netid@klc0305.quest.northwestern.edu:/kellogg/proj/your-netid/project/
```

The `-a` flag preserves permissions and timestamps; `-v` is verbose; `-z` compresses data in transit.

**Interactive SFTP session:**
```bash
sftp your-netid@klc0305.quest.northwestern.edu
sftp> put localfile.csv /kellogg/proj/your-netid/data/
sftp> get /kellogg/proj/your-netid/results/output.csv .
sftp> bye
```

## Graphical Tools (KLC ↔ Local Workstation)

### Quest OnDemand File Explorer

[Quest OnDemand](https://ondemand.quest.northwestern.edu) provides a browser-based file manager that requires no software installation. After logging in, use the **Files** menu to navigate to your home directory, project directories, or scratch space, then use the **Upload** and **Download** buttons to transfer files between Quest and your computer.

:::{note}
The maximum file size for upload and download is 10.7 GB. For best results, use Quest OnDemand for files under 2 GB. For larger transfers, use [Globus](#large-transfers-klc-onedrive-external-platforms).
:::

### SFTP Clients

These programs allow drag-and-drop file transfer using SFTP.

- **[Cyberduck](https://cyberduck.io/)** — Mac and Windows; free
- **[MobaXterm](https://mobaxterm.mobatek.net/)** — Windows; includes a built-in file browser alongside the terminal

Instructions using Cyberduck as an example:
1. Select "Open Connection"
![Cyberduck Open Connection](images/cyberduck_1.png)
2. Select the **SFTP** protocol
3. Enter the server address (e.g. `klc0202.quest.northwestern.edu`); leave port as 22
4. Enter your NU NetID and password
![Cyberduck Login](images/cyberduck_2.png)

(large-transfers-klc-onedrive-external-platforms)=
## Large Transfers (KLC ↔ OneDrive / External Platforms)

**Globus** is the recommended tool for large or recurring transfers between KLC and external platforms (Northwestern OneDrive, Quest, collaborator institutions). It supports high-speed parallel transfers, automatic retries, and resumable transfers — no need to zip files or worry about timeouts.

Detailed instructions are in the RCDS documentation:
- [Transferring Data To and From Quest](https://rcdsdocs.it.northwestern.edu/systems/quest/user-guide/data-transfer/data-transfer.html) — overview of all transfer methods
- [Globus documentation](https://rcdsdocs.it.northwestern.edu/systems/globus/globus-index.html) — detailed Globus setup and usage

## Choosing the Right Method

| Scenario | Recommended Tool |
|---|---|
| A few files, quick transfer | `scp` |
| Syncing a project directory | `rsync` |
| Drag-and-drop GUI (browser, no install) | Quest OnDemand File Explorer |
| Drag-and-drop GUI (desktop app) | Cyberduck / MobaXterm |
| Large datasets or recurring sync | Globus |

