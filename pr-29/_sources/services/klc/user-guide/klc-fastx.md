# FastX

`FastX` provides a full graphical desktop on a KLC node for software that requires a real X11 interface rather than a text terminal or code editor (MATLAB, Stata, SAS, and similar GUI-only applications).

For a browser-based graphical desktop with session tracking across nodes, see [KLC OnDemand](klc-ondemand).

## Prerequisites

- A KLC account and Northwestern NetID
- [Northwestern VPN](https://www.it.northwestern.edu/technology-services/infrastructure/network/vpn/index.html) when connecting from off campus
- A web browser (or the [FastX desktop client](https://starnet.com/download/fastx-client) for potentially better performance)
- Software to transfer files — FastX does not include file transfer. Use [Transferring Files](klc-transferfiles) or an SSH client

## Connect via the Web Browser

1. Open a FastX URL for the KLC node you want to use:

   ```
   https://klc0202.quest.northwestern.edu:3300/
   https://klc0203.quest.northwestern.edu:3300/
   https://klc0301.quest.northwestern.edu:3300/
   https://klc0302.quest.northwestern.edu:3300/
   https://klc0303.quest.northwestern.edu:3300/
   https://klc0304.quest.northwestern.edu:3300/
   https://klc0305.quest.northwestern.edu:3300/
   https://klc0306.quest.northwestern.edu:3300/
   https://klc0307.quest.northwestern.edu:3300/
   https://klc0401.quest.northwestern.edu:3300/
   https://klc0402.quest.northwestern.edu:3300/
   https://klc0503.quest.northwestern.edu:3300/
   ```

2. Log in with your NetID and password.

3. Click **Launch Session** and select the desktop environment or application.

4. Work in the graphical session. Sessions started through the FastX web client **persist after disconnect** until you terminate them or the server restarts.

## Choose a Node

Each URL connects to a specific KLC node. Check the **KLC Direct Access Resource Availability** table on [KLC OnDemand](klc-ondemand) and pick a node with available CPU and RAM before launching FastX on that host.

## Reconnect to an Existing Session

1. Open the **same** FastX URL you used to create the session.
2. Go to the **My Sessions** tab.
3. Select the running session and reconnect.

:::{note}
Unlike [KLC OnDemand](klc-ondemand), FastX does not surface sessions across nodes. You must reconnect to the specific node where the session was launched. Record the node name (for example, `klc0305`) when starting long-running work.
:::

## Terminate a Session

When you finish:

1. Open **My Sessions** on the same node.
2. Click **Actions** next to the session.
3. Select **Terminate**.

Terminate idle sessions to free resources for other researchers.

## Desktop Client

FastX also offers a [desktop client](https://starnet.com/download/fastx-client) that can perform better than browser access. Setup instructions are in the [Quest FastX documentation](https://rcdsdocs.it.northwestern.edu/systems/quest/user-guide/login/login-quest.html#option-2-fastx-desktop-client).

## Troubleshooting

| Symptom | What to do |
|---|---|
| Browser cannot reach the server | Confirm the URL and port `:3300`; check network/VPN requirements |
| Session not listed in My Sessions | Verify you are logged in to the same node where you launched the session |
| Application window is slow to respond | Expected for X11 over the network; try the desktop client or KLC OnDemand for that app |
| Cannot move files to KLC | Use [Transferring Files](klc-transferfiles); FastX does not transfer files |

## Related Pages

- [Logging Into KLC](klc-accessing) — compare FastX with SSH, OnDemand, and VS Code
- [KLC OnDemand](klc-ondemand) — browser-based alternative with cross-node session tracking
- [Transferring Files](klc-transferfiles) — move data to and from KLC
