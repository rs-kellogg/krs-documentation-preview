# Redivis

[Redivis](https://redivis.com) is a cloud-based data platform that lets researchers discover, query, and analyze datasets directly in their browser — without downloading files. Northwestern's Redivis Data Library is a collaboration between Kellogg Research Support and Northwestern University Libraries. It hosts a curated collection of research datasets that can be explored interactively, linked into analysis workflows, or accessed programmatically via API from the Kellogg Linux Cluster (KLC).

## Gaining Access

1. Visit the [Northwestern Redivis Data Library](https://redivis.com/Northwestern).

2. Click **Create account** in the upper right corner.

   ![Northwestern Redivis Data Library page with the Create account button highlighted](imgs/select-create-account-button-on-redivis.png)

3. Choose **Authenticate with your institution** and select **Northwestern University**. Sign in with your Northwestern NetID credentials.

   ![Sign in to Redivis with your Northwestern University account](imgs/sign-into-redivis-with-northwestern-account.png)

4. After signing in, you will be taken to the Northwestern organization page. Click **Join organization** and complete the short request form.

   ![Northwestern Redivis organization page showing the Join organization button](imgs/join-northwestern-redivis-org.png)

5. Once your request is approved, you will have access to the datasets hosted in the Northwestern Data Library. Some datasets additionally require you to **Apply for access** on the individual dataset page.

For a walkthrough, see the [Redivis discover and access data guide](https://docs.redivis.com/guides/discover-and-access-data).

## Exploring Datasets

Visit the [Northwestern datasets page](https://redivis.com/Northwestern/datasets) to browse all datasets hosted in the Northwestern Data Library.

When you open a dataset you will find three main tabs:

- **Overview** — General description, citation information, and access terms for the dataset.
- **Tables** — All tables included in the dataset. Click any table to open an exploration panel with three sub-tabs:
  - **Variables** — Full data dictionary listing every variable and its type.
  - **Cells** — A scrollable preview of the data. Select a column to see summary statistics in the right pane.
  - **Query** — An ad-hoc SQL interface for quick, transient queries. Results are shown inline but cannot be saved.

## Working with Data in Workflows

For deeper analysis, click **Analyze in workflow** (upper right of any dataset page) to open the dataset in a Redivis workflow. Inside the workflow canvas:

1. Click the circular dataset node to expand it, then hover over it to reveal two options: **Transform** and **Notebook**.

2. **Transform** — A graphical interface for building multi-step data pipelines:
   - From **New step**, select **SQL query** to write a SQL transformation.
   - From **New step**, choose other built-in operations (filter, aggregate, join, etc.) as needed.
   - Click **Run** in the upper right to execute the pipeline.
   - Click the output node, then use **Export table** in the right pane to download results.

3. **Notebook** — Opens a Jupyter notebook with a Python or R kernel pre-connected to your dataset:
   - Query tables programmatically using the Redivis client library.
   - See the API documentation: [Redivis Python](https://apidocs.redivis.com/client-libraries/redivis-python) | [Redivis R](https://apidocs.redivis.com/client-libraries/redivis-r)

For a walkthrough, see the [Redivis analyze data in a workflow guide](https://docs.redivis.com/guides/analyze-data-in-a-workflow).

## Accessing Redivis Data from KLC

You can query Redivis datasets programmatically from the Kellogg Linux Cluster using the Redivis Python client library.

### Step 1 — Generate an API token

1. Log in to Redivis and go to [Settings → API tokens](https://redivis.com/workspace/settings/tokens).
2. Click **Generate new token**.
3. Enable the **Data** and **Workflow** permissions, then click **Generate token**.
4. Copy the token text.

### Step 2 — Save the token on KLC

```bash
cd $HOME
mkdir -p keys
nano keys/redivis_api.txt
# Paste your token, then press Ctrl+X and save
```

### Step 3 — Run a query

Sample scripts are available on KLC at `/kellogg/software/redivis_scripts`. Copy them to your working directory and run:

```bash
cp /kellogg/software/redivis_scripts/sample_sql.py .
cp /kellogg/software/redivis_scripts/nu_author_openalex.sql .

module load mamba/23.1.0
source /hpc/software/mamba/23.1.0/etc/profile.d/conda.sh
conda activate /kellogg/software/envs/redivis_env
python sample_sql.py
```
