# AthenaDB

The Kellogg Data Cloud (KDC) is built on **Amazon Athena**, a serverless SQL query service. You can query KDC datasets either through the AWS web console or directly from KLC via an ODBC connection.

To request access to a specific dataset, contact [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu). Access is granted per database, not to the platform as a whole.

## Accessing via the AWS Console

### 1. Log in to AWS

Use the NUIT link to sign in with your NetID credentials:
[it.northwestern.edu/support/login/aws.html](https://www.it.northwestern.edu/support/login/aws.html)

Select **ksm-rch-data**, find the database you want, then click **Management console**.

<iframe src="https://kellogg-northwestern.hosted.panopto.com/Panopto/Pages/Embed.aspx?id=a629a167-dac3-4d56-8989-b09d01322bfe&autoplay=false&offerviewer=true&showtitle=true&showbrand=true&captions=false&interactivity=all" height="405" width="720" style="border: 1px solid #464646; max-width: 100%;" allowfullscreen allow="autoplay"></iframe>

```{important}
Once logged in, you only have access to Athena. This account does not grant access to any other AWS service.
```

### 2. Set Up Athena

- From the search bar, navigate to **Athena**
- Set your **workgroup** to match the database name you were granted access to
- Confirm the **Region** (upper right) is **US East-2 (Ohio)**

<iframe src="https://kellogg-northwestern.hosted.panopto.com/Panopto/Pages/Embed.aspx?id=1f94d9dd-2188-4ade-86e5-b09d0137d141&autoplay=false&offerviewer=true&showtitle=true&showbrand=true&captions=false&interactivity=all" height="405" width="720" style="border: 1px solid #464646; max-width: 100%;" allowfullscreen allow="autoplay"></iframe>

### 3. Query and Download Results

Submit SQL queries directly from the Athena console.

<iframe src="https://kellogg-northwestern.hosted.panopto.com/Panopto/Pages/Embed.aspx?id=3aabaed1-a027-41ab-82a7-b09d0137d0e9&autoplay=false&offerviewer=true&showtitle=true&showbrand=true&captions=false&interactivity=all" height="405" width="720" style="border: 1px solid #464646; max-width: 100%;" allowfullscreen allow="autoplay"></iframe>

Query results can be downloaded by:

- Clicking **Download results** on the results panel, or
- Going to the **Recent queries** tab and downloading results for a specific query

<iframe src="https://kellogg-northwestern.hosted.panopto.com/Panopto/Pages/Embed.aspx?id=8e5c94fd-a05b-45bd-b5d7-b09d0137d112&autoplay=false&offerviewer=true&showtitle=true&showbrand=true&captions=false&interactivity=all" height="405" width="720" style="border: 1px solid #464646; max-width: 100%;" allowfullscreen allow="autoplay"></iframe>

```{note}
Most KDC databases have a daily query limit of **2 TB of data scanned**. Contact [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) if you need this limit increased.
```

## Accessing via KLC

Querying Athena from KLC lets you integrate KDC data into Python, R, or Stata workflows running on the cluster.

### 1. Locate Your AWS Credentials

Go to [it.northwestern.edu/support/login/aws.html](https://www.it.northwestern.edu/support/login/aws.html):

- Select **ksm-rch-data** → your database → **Command line and programmatic access**
- Copy your temporary **AWS credentials file** from Option 2

<iframe src="https://kellogg-northwestern.hosted.panopto.com/Panopto/Pages/Embed.aspx?id=d71384f3-6714-4618-8ad7-b0a0011dde0e&autoplay=false&offerviewer=true&showtitle=true&showbrand=true&captions=false&interactivity=all" height="405" width="720" style="border: 1px solid #464646; max-width: 100%;" allowfullscreen allow="autoplay"></iframe>

```{note}
These temporary credentials expire every few hours and must be refreshed.
```

### 2. Create a Credentials File on KLC

```bash
mkdir -p ~/.aws
nano ~/.aws/credentials
# Paste the copied credentials, then save (Ctrl+X, Y, Enter)
```

<iframe src="https://kellogg-northwestern.hosted.panopto.com/Panopto/Pages/Embed.aspx?id=e8943c0f-6d31-4ec6-8474-b09d01321104&autoplay=false&offerviewer=true&showtitle=true&showbrand=true&captions=false&interactivity=all" height="405" width="720" style="border: 1px solid #464646; max-width: 100%;" allowfullscreen allow="autoplay"></iframe>

### 3. Load the AWS CLI

```bash
module load awscli/2
```

Verify your credentials work by listing accessible S3 buckets:

```bash
aws s3 ls --profile <account-profile>
```

Replace `<account-profile>` with your database account profile name.

<iframe src="https://kellogg-northwestern.hosted.panopto.com/Panopto/Pages/Embed.aspx?id=860f70f1-a8b1-4e39-99c5-b09d013226fc&autoplay=false&offerviewer=true&showtitle=true&showbrand=true&captions=false&interactivity=all" height="405" width="720" style="border: 1px solid #464646; max-width: 100%;" allowfullscreen allow="autoplay"></iframe>

### 4. Set Up the ODBC Environment

```bash
export ODBCSYSINI=/kellogg/software/.odbc/<database_name>
export ODBCINI=/kellogg/software/.odbc/<database_name>
```

Replace `<database_name>` with the workgroup name you were provided.

<iframe src="https://kellogg-northwestern.hosted.panopto.com/Panopto/Pages/Embed.aspx?id=22ac65fe-040c-4caa-90ca-b09d0132196f&autoplay=false&offerviewer=true&showtitle=true&showbrand=true&captions=false&interactivity=all" height="405" width="720" style="border: 1px solid #464646; max-width: 100%;" allowfullscreen allow="autoplay"></iframe>

### 5. Connect from Code

Sample files for each language are at `/kellogg/software/aws_odbc_samples` on KLC.

**Python**

```bash
module load python/3.10   # or your preferred version
```

Edit `athena_odbc.py` with your database and table name, then run:

```bash
python athena_odbc.py
```

<iframe src="https://kellogg-northwestern.hosted.panopto.com/Panopto/Pages/Embed.aspx?id=a7e74d1c-2527-4455-b0ae-b09d01321108&autoplay=false&offerviewer=true&showtitle=true&showbrand=true&captions=false&interactivity=all" height="405" width="720" style="border: 1px solid #464646; max-width: 100%;" allowfullscreen allow="autoplay"></iframe>

**R**

```bash
module load R
```

Edit `athena_odbc.R` with your database and table name, then run:

```bash
Rscript athena_odbc.R
```

<iframe src="https://kellogg-northwestern.hosted.panopto.com/Panopto/Pages/Embed.aspx?id=52c31140-fb33-4a07-b6cf-b09d0132110b&autoplay=false&offerviewer=true&showtitle=true&showbrand=true&captions=false&interactivity=all" height="405" width="720" style="border: 1px solid #464646; max-width: 100%;" allowfullscreen allow="autoplay"></iframe>

**Stata**

```bash
module load stata
```

Edit `athena_odbc.do` with your database and table name, then run:

```bash
stata-mp -b athena_odbc.do
```

<iframe src="https://kellogg-northwestern.hosted.panopto.com/Panopto/Pages/Embed.aspx?id=1977204b-10d4-41d4-aa71-b09d01321e16&autoplay=false&offerviewer=true&showtitle=true&showbrand=true&captions=false&interactivity=all" height="405" width="720" style="border: 1px solid #464646; max-width: 100%;" allowfullscreen allow="autoplay"></iframe>

### Query Limits

The same 2 TB/day scan limit applies when querying from KLC. Contact [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) to request an increase.
