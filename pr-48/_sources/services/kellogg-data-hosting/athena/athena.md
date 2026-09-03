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

The AWS Console requires no local setup. The KLC path requires a one-time `aws configure sso` setup; in future sessions, refresh your SSO session with `aws sso login` (the default session length is 4 hours).

## Accessing via the AWS Console

**Prerequisites:**

- A Northwestern NetID
- Access to a specific Athena database already granted by Kellogg Research Support
- No local setup or software installation

### 1. Log in to AWS

1. Go to the [NUIT AWS login page](https://www.it.northwestern.edu/support/login/aws.html), click **General Use Login**, and authenticate with your Northwestern NetID.
2. On the **AWS access portal**, click the arrow next to **ksm-rch-data** to expand it.
3. Click **Management console** next to your database, for example `ksm-rch-data-comscore2`.
4. Confirm the **Region** in the upper right is **US East (Ohio) (us-east-2)**.

:::{dropdown} Screenshots: Logging In to AWS

**1. NUIT AWS login page**

```{image} images/aws-login-page.png
:alt: NUIT AWS login page showing General Use Login and NIH-Funded Research Login buttons
:scale: 50%
```

**2. AWS access portal**

```{image} images/aws-access-portal-accounts.png
:alt: AWS access portal showing ksm-rch-data and ksm-rch-support accounts
:scale: 50%
```

**3. ksm-rch-data expanded**

```{image} images/aws-access-portal-expanded.png
:alt: ksm-rch-data expanded showing database roles such as ksm-rch-data-comscore2 and ksm-rch-data-fetchrewards
:scale: 50%
```

**4. AWS Console Home**

```{image} images/aws-console-home.png
:alt: AWS Console Home showing the correct region and account in the upper right
:scale: 50%
```

:::

### 2. Navigate to Athena

1. Type **Athena** in the search bar at the top of the console and select **Athena** from the results.
2. Right-click any table name in the left panel to access shortcuts such as **Preview Table** and **Generate table DDL**.

The Athena **Query editor** opens. The **Workgroup** (shown in the upper right of the editor) and **Database** (in the left panel) are set to the database you were granted access to. If either value is wrong, select the correct workgroup and database from the dropdown menus in the editor. The left panel lists all available tables.

```{tip}
Right-click any table name in the left panel to access shortcuts such as **Preview Table** (generates a `SELECT *` query with a 10-row limit) and **Generate table DDL** (shows the table schema). Preview Table still scans data — see [Query Limits and Reducing Data Scanned](#query-limits-and-reducing-data-scanned) before previewing large tables.
```

:::{dropdown} Screenshots: Navigating to Athena

**1. Search for Athena**

```{image} images/aws-console-search-athena.png
:alt: AWS Console search bar with "athena" typed, showing the Athena service result
:scale: 50%
```

**2. Athena Query editor**

```{image} images/athena-query-editor.png
:alt: Athena Query Editor with workgroup set to comscore2, database set to comscore, and 8 tables listed
:scale: 50%
```

**3. Table context menu**

```{image} images/athena-table-context-menu.png
:alt: Table context menu showing options including Preview Table, Generate table DDL, Insert into editor, and View properties
:scale: 50%
```

:::

### 3. Query and Download Results

1. Type your SQL query in the editor and click **Run**. The status bar below the editor shows the query progress.
2. When the query completes, click **Download results CSV** in the **Query results** panel to save the output to your computer.

:::{dropdown} Screenshots: Querying and Downloading Results

**1. Query running**

```{image} images/athena-query-running.png
:alt: Athena Query Editor with a SELECT query running, showing "Running" status and time in queue
:scale: 50%
```

**2. Query results**

```{image} images/athena-query-results.png
:alt: Athena Query Editor showing completed query results with 10 rows and the Download results CSV button
:scale: 50%
```

:::

(accessing-via-klc)=
## Accessing via KLC

Querying Athena from KLC lets you integrate Kellogg Data Hosting datasets into Python, R, or Stata workflows running on the cluster.

**Prerequisites:**

- A [KLC account](../../klc/user-guide/klc-accessing) and an active terminal session on KLC
- Access to a specific Athena database already granted by Kellogg Research Support
- The `awscli/latest` module on KLC, which provides AWS CLI 2.22.7 (`aws configure sso` requires 2.9.0 or later)

```{note}
**Where to run queries:** Short interactive queries are fine on a KLC login node. Do not pull large result sets on a login node — see [When to Use KLC Reserve](../../klc-reserve/when-to-use) for the 24-core policy and batch options. Use [tmux](../../klc/user-guide/klc-tmux) to keep sessions alive after disconnecting.
```

### 1. Load the AWS CLI

```bash
module load awscli/latest
```

Optionally confirm the version:

```bash
aws --version
```

### 2. Configure NetID Authentication

KLC login nodes have no GUI browser. AWS CLI 2.22.0 and later also default to a PKCE authorization flow that cannot complete on a login node. Use `aws configure sso --no-browser --use-device-code` and enter the values below when prompted:

| Prompt | Value |
|---|---|
| SSO session name | `nu-sso` |
| SSO start URL | `https://nu-sso.awsapps.com/start` |
| SSO region | `us-east-2` |
| SSO registration scopes | Accept the default (`sso:account:access`) |

```bash
aws configure sso --no-browser --use-device-code
```

```{note}
`--use-device-code` is required on AWS CLI 2.22.0 and later. On AWS CLI older than 2.22.0, `--use-device-code` is not recognized; those versions already use the device-code flow, so `--no-browser` alone is enough. 

To avoid passing the `--use-device-code` flag on every SSO command, add `export AWS_CLI_SSO_RETRY_MODE=device-code` to `~/.bashrc`.
```

1. Copy the URL the CLI prints into a browser on your local machine, sign in with your NetID, and pass the Duo MFA challenge.
2. Choose **Allow access** when the browser asks to authorize `botocore-client-nu-sso`.
3. Back in the terminal, arrow-key to **ksm-rch-data** and press Enter. Do not select any other AWS account.
4. Select the role matching your database, for example `ksm-rch-data-fetchrewards`.
5. Enter `us-east-2` for the default region, then press Enter to accept the defaults for output format and profile name. The default profile name is `ksm-rch-data-<database>-<account-id>`.

:::{dropdown} Screenshots: Configuring NetID Authentication

**2. Allow access**

```{image} images/aws-cli-sso-allow-access.png
:alt: AWS SSO authorization dialog asking Allow botocore-client-nu-sso to access your data with an Allow access button
:scale: 33%
```

**3. Select AWS account**

```{image} images/aws-cli-sso-select-account.png
:alt: Terminal account selection during aws configure sso with ksm-rch-data highlighted
:scale: 33%
```

**4. Select role**

```{image} images/aws-cli-sso-select-role.png
:alt: Terminal role selection during aws configure sso showing ksm-rch-data roles
:scale: 33%
```

**5. CLI options**

```{image} images/aws-cli-sso-cli-options.png
:alt: Terminal prompts for CLI default region, output format, and profile name during aws configure sso
:scale: 33%
```

:::

```{warning}
Note the exact profile name the CLI prints at the end of setup. You will pass this name to `--profile` and `AWS_PROFILE` in later steps.
<!-- TODO(KRS): confirm whether the ODBC configuration in /kellogg/software/.odbc/<workgroup-name> expects a specific AWS profile name (previously ksm-rch-data-<database>). If so, users must name their SSO profile to match. -->
```

```{tip}
If you have access to multiple accounts or roles, copy the profile block that `aws configure sso` writes to `~/.aws/config` for each additional account or role, reusing the same `sso_session` (`nu-sso`). You can then choose which profile to use for each AWS CLI command without re-authenticating.
```

```{note}
The default SSO session length is 4 hours. In future sessions, if you are not prompted to log in automatically when running an AWS CLI command, run the command below.
```

```bash
aws sso login --sso-session nu-sso --no-browser --use-device-code
```

For more details, see [Configuring IAM Identity Center authentication with the AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-sso.html).

### 3. Verify Access

Verify your SSO profile works by listing accessible S3 buckets:

```bash
aws s3 ls --profile <account-profile>
```

Replace `<account-profile>` with the profile name from step 2 (for example, `ksm-rch-data-comscore2-<account-id>`).

<!-- TODO(KRS): re-record; this video shows the retired credentials-file workflow and the old awscli/2 module -->

:::{dropdown} Video: Load AWS CLI and verify credentials

<iframe src="https://kellogg-northwestern.hosted.panopto.com/Panopto/Pages/Embed.aspx?id=860f70f1-a8b1-4e39-99c5-b09d013226fc&autoplay=false&offerviewer=true&showtitle=true&showbrand=true&captions=false&interactivity=all" height="405" width="720" title="Video walkthrough: load AWS CLI and verify credentials" allowfullscreen allow="autoplay"></iframe>

:::

### 4. Set Up the ODBC Environment

The shared ODBC configuration at `/kellogg/software/.odbc/<workgroup-name>` must use `AuthenticationType=Default Credentials` so the driver reads the SSO token that `aws sso login` cached under `~/.aws/sso/cache`. Export your profile name alongside the ODBC paths:

```bash
export ODBCSYSINI=/kellogg/software/.odbc/<workgroup-name>
export ODBCINI=/kellogg/software/.odbc/<workgroup-name>
export AWS_PROFILE=<account-profile>
```

Replace the placeholders in the commands above:

- `<workgroup-name>` — your Athena workgroup, for example `comscore2`. This is the workgroup shown in the upper right of the Athena Query editor, not the database name in the left panel.
- `<account-profile>` — the profile name from step 2

<!-- TODO(KRS): confirm the driver version at /kellogg/software/.odbc/<workgroup-name> is the Athena ODBC v2 driver, and update AuthenticationType to Default Credentials. -->
<!-- TODO(KRS): confirm the driver's bundled AWS SDK supports the sso_session config format that `aws configure sso` writes ([sso-session nu-sso]) rather than only the legacy inline sso_start_url format. -->

If ODBC commands fail to pick up your SSO token, export static credentials from your active SSO session into the environment:

```bash
eval "$(aws configure export-credentials --profile <account-profile> --format env)"
```

Both `Default Credentials` and `IAM Profile` with `credential_source=Environment` accept these environment variables.

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
module load mamba/24.3.0
mamba create -p /kellogg/proj/<your-netid>/envs/athena python=3.10   # choose your Python version
source activate /kellogg/proj/<your-netid>/envs/athena
mamba install pyodbc   # or pip install pyodbc
```

See [Conda Environments on KLC](/services/klc/user-guide/klc-conda) for full environment setup.

Edit `athena_odbc.py` with your database name and table name, then run:

```bash
python athena_odbc.py
```

:::

:::{tab-item} R

```bash
module load R/4.5.1
```

Edit `athena_odbc.R` with your database name and table name, then run:

```bash
Rscript athena_odbc.R
```

:::

:::{tab-item} Stata

```bash
module load stata/17
```

Edit `athena_odbc.do` with your database name and table name, then run:

```bash
stata-mp -b athena_odbc.do
```

:::

::::

:::{dropdown} Video: Connect from Python

<iframe src="https://kellogg-northwestern.hosted.panopto.com/Panopto/Pages/Embed.aspx?id=a7e74d1c-2527-4455-b0ae-b09d01321108&autoplay=false&offerviewer=true&showtitle=true&showbrand=true&captions=false&interactivity=all" height="405" width="720" title="Video walkthrough: connect from Python" allowfullscreen allow="autoplay"></iframe>

:::

:::{dropdown} Video: Connect from R

<iframe src="https://kellogg-northwestern.hosted.panopto.com/Panopto/Pages/Embed.aspx?id=52c31140-fb33-4a07-b6cf-b09d0132110b&autoplay=false&offerviewer=true&showtitle=true&showbrand=true&captions=false&interactivity=all" height="405" width="720" title="Video walkthrough: connect from R" allowfullscreen allow="autoplay"></iframe>

:::

:::{dropdown} Video: Connect from Stata

<iframe src="https://kellogg-northwestern.hosted.panopto.com/Panopto/Pages/Embed.aspx?id=1977204b-10d4-41d4-aa71-b09d01321e16&autoplay=false&offerviewer=true&showtitle=true&showbrand=true&captions=false&interactivity=all" height="405" width="720" title="Video walkthrough: connect from Stata" allowfullscreen allow="autoplay"></iframe>

:::

(query-limits-and-reducing-data-scanned)=
## Query Limits and Reducing Data Scanned

Most Athena databases have a daily query limit of **2 TB of data scanned**, whether you query from the AWS Console or from KLC. Contact [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) if you need this limit increased.

Athena charges by data scanned, not rows returned. After each query, check the **Data scanned** value in the Query editor results panel before running follow-up queries.

To stay under the limit:

- Filter on partition columns (such as date or year) whenever the table schema supports it
- Select only the columns you need instead of using `SELECT *`
- Use **Generate table DDL** to inspect the schema before writing queries

<!-- TODO(KRS): confirm whether Preview Table (SELECT * with LIMIT 10) scans the full table or only a subset -->

## Troubleshooting

:::{dropdown} AWS CLI or ODBC commands fail with an authentication or token error

If AWS CLI or ODBC commands fail with an authentication or token error, your SSO session has expired. Run:

```bash
aws sso login --sso-session nu-sso --no-browser --use-device-code
```

<!-- TODO(KRS): confirm the exact error message users see when an SSO session expires -->

:::

:::{dropdown} `aws configure sso` or `--no-browser` is not recognized, or the SSO flow hangs

If the CLI reports that `aws configure sso` or `--no-browser` is not recognized, an older `awscli` module is loaded. Run `module load awscli/latest` and try again.

If the SSO flow hangs or reports a connection or callback error instead of printing a URL and code, device-code mode was not requested. Add `--use-device-code` to the command, or set `AWS_CLI_SSO_RETRY_MODE=device-code` in `~/.bashrc`.

:::

:::{dropdown} Your database does not appear under **ksm-rch-data**

If your database does not appear under **ksm-rch-data** in the AWS access portal, access has not been granted yet. Email [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) with the dataset name.

:::

:::{dropdown} Athena returns no tables, or queries fail immediately

Athena queries fail or return no tables when the region is not **US East (Ohio) (us-east-2)**. Confirm the region in the upper right of the AWS Console before opening the Query editor.

:::

:::{dropdown} A sample script cannot connect through ODBC

If a sample script fails to connect, verify all of the following:

- The ODBC environment variables from step 4 are set in your current shell session
- `<workgroup-name>` matches your Athena workgroup, not the database name
- `AWS_PROFILE` matches the profile name from step 2
- Your SSO session is active (`aws sso login --sso-session nu-sso --no-browser --use-device-code`)

<!-- TODO(KRS): confirm common ODBC error messages and fixes -->

:::

## Datasets on Athena

The dataset pages below document a selected subset of datasets hosted on the Athena platform with documentation on this site.

```{note}
The datasets listed below are a selected subset with documentation on this site, not an exhaustive catalog. For an exhaustive list of datasets available to Kellogg researchers, see the [Kellogg Research Support Datasets page](https://www.kellogg.northwestern.edu/academics-research/research-support/dataset/).
```

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
