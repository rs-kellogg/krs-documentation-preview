# FastX

`FastX` gives you a full graphical desktop on a KLC node, for software that needs a real X11 interface rather than just a text terminal or code editor (MATLAB, Stata, SAS, and similar GUI-only applications).

Getting a `FastX` graphical interface to a KLC server is as simple as putting your web browser to one of these server addresses:

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

After you log in with your NetID and password, click the "Launch Session" button, and then select the application you want to run. By default, the sessions you start through the `FastX` web client will **persist indefinitely** — until either you terminate the session or the server is restarted.

If you need to find a session you launched previously, you can find it on the My Sessions tab, but you must be logged on to the **same KLC node** where that session was launched. We advise you to remember the specific node you are on if you intend to run very long jobs on KLC, and to **terminate sessions (under the Actions button in My Sessions) when you are done with your session**.

:::{note}
Unlike [KLC OnDemand](klc-ondemand), FastX won't surface a previous session for you automatically across nodes — you have to remember and reconnect to the specific node it was launched on.
:::

`FastX` also has a [desktop client](https://starnet.com/download/fastx-client) available. It can have better performance than browser access. Detailed instructions can be found in the [Quest documentation](https://rcdsdocs.it.northwestern.edu/systems/quest/user-guide/login/login-quest.html#option-2-fastx-desktop-client).
