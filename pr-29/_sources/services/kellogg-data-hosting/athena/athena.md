(athena)=
# Athena (AWS)

The Kellogg Data Hosting **Athena** platform is built on **Amazon Athena**, a serverless SQL query service. You can query Athena datasets either through the AWS web console or directly from KLC via an ODBC connection.

To request access to a specific dataset, contact [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu). Access is granted per database, not to the platform as a whole.

```{important}
Once logged in to AWS, you only have access to Athena. This account does not grant access to any other AWS service.
```

## Choosing an Access Method

| Method | Best For |
|---|---|
| [AWS Console](#accessing-via-the-aws-console) | Exploring data, running ad-hoc SQL queries, downloading CSV results |
| [KLC via ODBC](#accessing-via-klc) | Integrating Athena data into Python, R, or Stata workflows on the cluster |

The AWS Console requires no local setup. The KLC path requires temporary AWS credentials that expire every few hours and must be refreshed.

## Accessing via the AWS Console

### 1. Log in to AWS

Go to the [NUIT AWS login page](https://www.it.northwestern.edu/support/login/aws.html) and sign in with your Northwestern NetID credentials.

Click **General Use Login** and authenticate with your Northwestern NetID.

```{image} images/aws-login-page.png
:alt: NUIT AWS login page showing General Use Login and NIH-Funded Research Login buttons
:width: 50%
```

After signing in, you will land on the **AWS access portal** showing the accounts you have access to.

```{image} images/aws-access-portal-accounts.png
:alt: AWS access portal showing ksm-rch-data and ksm-rch-support accounts
:width: 50%
```

Click the arrow next to **ksm-rch-data** to expand it. You will see one entry per database you have been granted access to (for example, `ksm-rch-data-comscore2`). Click **Management console** next to your database to open the AWS Console.

```{image} images/aws-access-portal-expanded.png
:alt: ksm-rch-data expanded showing database roles such as ksm-rch-data-comscore2 and ksm-rch-data-fetchrewards
:width: 50%
```

The AWS Console opens already scoped to your database account. Confirm the **Region** in the upper right is **US East (Ohio) (us-east-2)**.

```{image} images/aws-console-home.png
:alt: AWS Console Home showing the correct region and account in the upper right
:width: 50%
```

### 2. Navigate to Athena

Type **Athena** in the search bar at the top of the console and select **Athena** from the results.

```{image} images/aws-console-search-athena.png
:alt: AWS Console search bar with "athena" typed, showing the Athena service result
:width: 50%
```

The Athena **Query editor** opens. The **Workgroup** (shown in the upper right of the editor) and **Database** (in the left panel) are set to the database you were granted access to. If either value is wrong, select the correct workgroup and database from the dropdown menus in the editor. The left panel lists all available tables.

```{image} images/athena-query-editor.png
:alt: Athena Query Editor with workgroup set to comscore2, database set to comscore, and 8 tables listed
:width: 50%
```

```{tip}
Right-click any table name in the left panel to access shortcuts such as **Preview Table** (generates a `SELECT *` query with a 10-row limit) and **Generate table DDL** (shows the table schema). Preview Table still scans data — see [Query Limits and Reducing Data Scanned](#query-limits-and-reducing-data-scanned) before previewing large tables.
```

```{image} images/athena-table-context-menu.png
:alt: Table context menu showing options including Preview Table, Generate table DDL, Insert into editor, and View properties
:width: 50%
```

### 3. Query and Download Results

Type your SQL query in the editor and click **Run**. The status bar below the editor shows the query progress.

```{image} images/athena-query-running.png
:alt: Athena Query Editor with a SELECT query running, showing "Running" status and time in queue
:width: 50%
```

When the query completes, results appear in the **Query results** panel. Click **Download results CSV** to save the output to your computer.

```{image} images/athena-query-results.png
:alt: Athena Query Editor showing completed query results with 10 rows and the Download results CSV button
:width: 50%
```

## Accessing via KLC

Querying Athena from KLC lets you integrate Kellogg Data Hosting datasets into Python, R, or Stata workflows running on the cluster.

**Prerequisites:**

- A [KLC account](../../klc/user-guide/klc-accessing) and an active terminal session on KLC
- Access to a specific Athena database already granted by Kellogg Research Support

```{note}
**Where to run queries:** Short interactive queries are fine on a KLC login node. Do not pull large result sets on a login node — see [When to Use KLC Reserve](../../klc-reserve/when-to-use) for the 24-core policy and batch options. Use [tmux](../../klc/user-guide/klc-tmux) to keep sessions alive after disconnecting.
```

### 1. Locate Your AWS Credentials

Go to the [NUIT AWS login page](https://www.it.northwestern.edu/support/login/aws.html):

- Select **ksm-rch-data** → your database → **Command line and programmatic access**
- Copy your temporary **AWS credentials file** from Option 2

:::{dropdown} Video: Locate AWS credentials

<iframe src="https://kellogg-northwestern.hosted.panopto.com/Panopto/Pages/Embed.aspx?id=d71384f3-6714-4618-8ad7-b0a0011dde0e&autoplay=false&offerviewer=true&showtitle=true&showbrand=true&captions=false&interactivity=all" height="405" width="720" title="Video walkthrough: locate AWS credentials" allowfullscreen allow="autoplay"></iframe>

:::

```{note}
These temporary credentials expire every few hours and must be refreshed.
```

### 2. Create a Credentials File on KLC

```bash
mkdir -p ~/.aws
nano ~/.aws/credentials
# Paste the copied credentials, then save (Ctrl+X, Y, Enter)
```

The credentials file contains one or more profile sections in square brackets (for example, `[ksm-rch-data-comscore2]`). You will use this profile name in step 3.

:::{dropdown} Video: Create credentials file on KLC

<iframe src="https://kellogg-northwestern.hosted.panopto.com/Panopto/Pages/Embed.aspx?id=e8943c0f-6d31-4ec6-8474-b09d01321104&autoplay=false&offerviewer=true&showtitle=true&showbrand=true&captions=false&interactivity=all" height="405" width="720" title="Video walkthrough: create credentials file on KLC" allowfullscreen allow="autoplay"></iframe>

:::

### 3. Load the AWS CLI

```bash
module load awscli/2
```

Verify your credentials work by listing accessible S3 buckets:

```bash
aws s3 ls --profile <account-profile>
```

Replace `<account-profile>` with the profile name from the square-bracket header in your credentials file (for example, `ksm-rch-data-comscore2`).

:::{dropdown} Video: Load AWS CLI and verify credentials

<iframe src="https://kellogg-northwestern.hosted.panopto.com/Panopto/Pages/Embed.aspx?id=860f70f1-a8b1-4e39-99c5-b09d013226fc&autoplay=false&offerviewer=true&showtitle=true&showbrand=true&captions=false&interactivity=all" height="405" width="720" title="Video walkthrough: load AWS CLI and verify credentials" allowfullscreen allow="autoplay"></iframe>

:::

### 4. Set Up the ODBC Environment

```bash
export ODBCSYSINI=/kellogg/software/.odbc/<workgroup-name>
export ODBCINI=/kellogg/software/.odbc/<workgroup-name>
```

Replace `<workgroup-name>` with your Athena workgroup name (for example, `comscore2`). This is the workgroup shown in the upper right of the Athena Query editor, not the database name in the left panel.

:::{dropdown} Video: Set up ODBC environment

<iframe src="https://kellogg-northwestern.hosted.panopto.com/Panopto/Pages/Embed.aspx?id=22ac65fe-040c-4caa-90ca-b09d0132196f&autoplay=false&offerviewer=true&showtitle=true&showbrand=true&captions=false&interactivity=all" height="405" width="720" title="Video walkthrough: set up ODBC environment" allowfullscreen allow="autoplay"></iframe>

:::

### 5. Copy and Run a Sample Script

Sample files for each language are at `/kellogg/software/aws_odbc_samples` on KLC. Copy them to your working directory:

```bash
mkdir -p ~/athena-work
cp /kellogg/software/aws_odbc_samples/* ~/athena-work/
cd ~/athena-work
```

::::{tab-set}

:::{tab-item} Python

```bash
module load python/3.10   # or your preferred version
```

Edit `athena_odbc.py` with your database name and table name, then run:

```bash
python athena_odbc.py
```

:::

:::{tab-item} R

```bash
module load R
```

Edit `athena_odbc.R` with your database name and table name, then run:

```bash
Rscript athena_odbc.R
```

:::

:::{tab-item} Stata

```bash
module load stata
```

Edit `athena_odbc.do` with your database name and table name, then run:

```bash
stata-mp -b athena_odbc.do
```

:::

::::

<!-- TODO(KRS): confirm whether module load python/3.10 includes the ODBC bindings required by athena_odbc.py -->

:::{dropdown} Video: Connect from Python

<iframe src="https://kellogg-northwestern.hosted.panopto.com/Panopto/Pages/Embed.aspx?id=a7e74d1c-2527-4455-b0ae-b09d01321108&autoplay=false&offerviewer=true&showtitle=true&showbrand=true&captions=false&interactivity=all" height="405" width="720" title="Video walkthrough: connect from Python" allowfullscreen allow="autoplay"></iframe>

:::

:::{dropdown} Video: Connect from R

<iframe src="https://kellogg-northwestern.hosted.panopto.com/Panopto/Pages/Embed.aspx?id=52c31140-fb33-4a07-b6cf-b09d0132110b&autoplay=false&offerviewer=true&showtitle=true&showbrand=true&captions=false&interactivity=all" height="405" width="720" title="Video walkthrough: connect from R" allowfullscreen allow="autoplay"></iframe>

:::

:::{dropdown} Video: Connect from Stata

<iframe src="https://kellogg-northwestern.hosted.panopto.com/Panopto/Pages/Embed.aspx?id=1977204b-10d4-41d4-aa71-b09d01321e16&autoplay=false&offerviewer=true&showtitle=true&showbrand=true&captions=false&interactivity=all" height="405" width="720" title="Video walkthrough: connect from Stata" allowfullscreen allow="autoplay"></iframe>

:::

## Query Limits and Reducing Data Scanned

Most Athena databases have a daily query limit of **2 TB of data scanned**, whether you query from the AWS Console or from KLC. Contact [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) if you need this limit increased.

Athena charges by data scanned, not rows returned. After each query, check the **Data scanned** value in the Query editor results panel before running follow-up queries.

To stay under the limit:

- Filter on partition columns (such as date or year) whenever the table schema supports it
- Select only the columns you need instead of using `SELECT *`
- Use **Generate table DDL** to inspect the schema before writing queries

<!-- TODO(KRS): confirm whether Preview Table (SELECT * with LIMIT 10) scans the full table or only a subset -->

## Troubleshooting

**Expired credentials**

If AWS CLI or ODBC commands fail with an authentication or token error, your temporary credentials have expired. Return to the [NUIT AWS login page](https://www.it.northwestern.edu/support/login/aws.html), copy fresh credentials from Option 2, and update `~/.aws/credentials`.

<!-- TODO(KRS): confirm the exact error message users see when credentials expire -->

**Database missing from the access portal**

If your database does not appear under **ksm-rch-data** in the AWS access portal, access has not been granted yet. Email [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) with the dataset name.

**Wrong AWS region**

Athena queries fail or return no tables when the region is not **US East (Ohio) (us-east-2)**. Confirm the region in the upper right of the AWS Console before opening the Query editor.

**ODBC connection failure**

If a sample script fails to connect, verify all of the following:

- The ODBC environment variables from step 4 are set in your current shell session
- `<workgroup-name>` matches your Athena workgroup, not the database name
- Your credentials file contains a current, unexpired profile

<!-- TODO(KRS): confirm common ODBC error messages and fixes -->

## Datasets on Athena

The dataset pages below document each Kellogg-licensed dataset hosted on the Athena platform:

- [Comscore](../../datasets/datasets/comscore)
- [Cotality (formerly CoreLogic)](../../datasets/datasets/cotality)
- [Equifax](../../datasets/datasets/equifax) <!-- TODO(KRS): confirm Equifax is available on Athena; equifax.md lists access platforms as TBD -->
- [PATSTAT](../../datasets/datasets/patstat)

For the full Kellogg Data Hosting overview, see [Kellogg Data Hosting](../kdc). For access requests or questions, see [Getting Help](../../../start/getting-help).

```{toctree}
:maxdepth: 1
:hidden:
:caption: Athena Datasets

Comscore <../../datasets/datasets/comscore>
Cotality (formerly CoreLogic) <../../datasets/datasets/cotality>
Equifax <../../datasets/datasets/equifax>
PATSTAT <../../datasets/datasets/patstat>
```
