(klc-node-resources)=
# KLC Node Resources

Live CPU, RAM, and GPU availability for KLC login nodes and KLC Reserve SLURM nodes. Use these tables to pick an underutilized login node before connecting, or to check Reserve GPU and high-memory capacity before submitting a job.

- **KLC Direct Access** — shared login nodes for [SSH](/services/klc/user-guide/klc-ssh), [KLC OnDemand](/services/klc/user-guide/klc-ondemand), [VS Code](/services/klc/user-guide/klc-vscode), and [FastX](/services/klc/user-guide/klc-fastx). Choose a node with available CPU cores and RAM for your workload.
- **KLC Slurm** — [KLC Reserve](/services/klc-reserve/klc-reserve) GPU and high-memory nodes. A value of `0` in **Available GPU Cards** means those GPUs are currently allocated.

The tables update every 20 minutes. Reload this page to load the current snapshot.

[Open the live tables in a new tab](https://d1p18nmj81zs72.cloudfront.net/klcnodes/klcnodes.html)

<iframe class="klc-node-resources"
        src="https://d1p18nmj81zs72.cloudfront.net/klcnodes/klcnodes.html"
        title="Live KLC and KLC Reserve node resource availability"
        loading="lazy"></iframe>

For connection options, see [Logging Into KLC](/services/klc/user-guide/klc-accessing).
