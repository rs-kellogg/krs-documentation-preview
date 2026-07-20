# Conda/Mamba Environment

## Managing Environments with `conda` and `mamba`

In computational research, ensuring that code runs consistently across different systems and over time is essential. This is where **environment management tools** like `conda` and `mamba` come in.

`conda` is a powerful package and environment manager that allows you to create isolated environments — each with its own versions of Python and packages. `mamba` is a faster, drop-in replacement for `conda` that significantly speeds up environment creation and dependency resolution.

## Why It Matters: **Reproducibility**

In modern research, reproducibility isn't optional — it's a **core requirement**. By using `conda` or `mamba` environments, you can:

- **Isolate dependencies** for specific projects
- **Avoid version conflicts** between packages
- **Share exact software environments** with collaborators
- **Ensure long-term reproducibility** of analysis and results

Imagine you share a Jupyter notebook with a colleague. If you’ve used a `conda`/`mamba` environment and included an `environment.yml` file, your colleague can recreate your exact setup — no more "it works on my machine" problems.

Without proper environment management, research code that runs today may fail tomorrow due to subtle changes in software versions. By making `conda` or `mamba` environments part of your standard workflow, you are not just managing software — you are investing in the **integrity, longevity, and reproducibility** of your research.



## 🛠️ Basic Workflow

```{seealso}
KLC uses the [LMOD module system](https://lmod.readthedocs.io/en/latest/). For a full reference on `module avail`, `module load`, and related commands, see the [Quest Software Modules documentation](https://rcdsdocs.it.northwestern.edu/systems/quest/user-guide/modules/modules.html).
```

1. Create a new environment:

- Python environment
    ```bash
    module load mamba
    mamba create -p /kellogg/proj/<your_netid>/envs/python_proj python=3.10
    ```

- R environment with optional `dplyr` packages 
    ```bash
    module load mamba
    mamba create -p /kellogg/proj/<your_netid>/envs/r_proj -c conda-forge r-base=4.4.0 r-dplyr 
    ```

2. Activate the environment:

   ```bash
   module load mamba
   source activate /kellogg/proj/<your_netid>/envs/python_proj
   ```

3. Install packages:

   ```bash
   mamba install pandas 
   ```

4. Export environment (for sharing or archiving):

   ```bash
   mamba env export > environment.yml
   ```

5. Recreate environment from a file:

   ```bash
   mamba env create -f environment.yml
   ```

6. Leave an environment
   ```bash
   conda deactivate
   ```



