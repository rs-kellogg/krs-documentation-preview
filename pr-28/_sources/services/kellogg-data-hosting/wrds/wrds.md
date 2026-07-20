# WRDS

[Wharton Research Data Services (WRDS)](https://wrds-www.wharton.upenn.edu/) is a research platform that provides access to a broad range of financial, economic, and marketing datasets — including CRSP, Compustat, Execucomp, and many others. WRDS is operated by the Wharton School of the University of Pennsylvania; Kellogg maintains a site license that gives all faculty, PhD students, and approved researchers access.

WRDS is one of three platforms under [Kellogg Data Hosting](../kdc). Unlike Athena and Redivis, WRDS is operated by the Wharton School and accessed through their infrastructure directly.

## Gaining Access

1. Go to [wrds-www.wharton.upenn.edu](https://wrds-www.wharton.upenn.edu/) and click **Register**.
2. Register using your Northwestern email address (e.g., `netid@u.northwestern.edu` or `name@kellogg.northwestern.edu`).
3. Your account will be reviewed before access is granted — allow a few business days. If your work is time-sensitive, contact [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu).

Once approved, you can log in to the WRDS web interface to browse datasets and run small interactive queries.

## Access Options

WRDS offers several ways to work with data:

| Method | Best For |
|---|---|
| [WRDS Web Interface](https://wrds-www.wharton.upenn.edu/) | Browsing datasets, running ad-hoc queries, downloading small results |
| [WRDS SAS Studio](https://wrds-cloud.wharton.upenn.edu/SASStudio/) | SAS-based analysis on WRDS Cloud |
| [WRDS JupyterHub](https://wrds-jupyter.wharton.upenn.edu/) | Python/R notebooks on WRDS Cloud |
| [WRDS RStudio](https://wrds-rstudio.wharton.upenn.edu/) | R analysis on WRDS Cloud |
| Python `wrds` package from KLC | Integrating WRDS data into Python workflows on KLC |
| R `RPostgres` package from KLC | Integrating WRDS data into R workflows on KLC |

The rest of this page covers the programmatic Python and R options from KLC, which integrate directly into your research scripts.

## Setting Up Credentials

WRDS uses a PostgreSQL connection that requires a username and password. Rather than hardcoding credentials in scripts, save them to a `.pgpass` file in your home directory. Both the Python `wrds` package and R's `RPostgres` read this file automatically.

On KLC, open a terminal and create the file with `nano`:

```bash
nano ~/.pgpass
```

Add this single line, replacing `your-wrds-username` and `your-wrds-password` with your actual credentials:

```
wrds-pgdata.wharton.upenn.edu:9737:wrds:your-wrds-username:your-wrds-password
```

Save and exit (`Ctrl+O`, then `Ctrl+X`), then restrict the file's permissions:

```bash
chmod 600 ~/.pgpass
```

The `chmod 600` step is required — PostgreSQL will ignore the file if it is readable by other users.

## Connecting from KLC

### Python

KRS maintains a shared conda environment on KLC with the `wrds` package pre-installed. To use it:

```bash
module load mamba
source activate /kellogg/software/envs/wrds25_env
```

You can also install the package into your own environment:

```bash
mamba install -c conda-forge wrds
# or: pip install wrds
```

Connect to WRDS in Python:

```python
import wrds

conn = wrds.Connection(wrds_username="your-wrds-username")
```

:::{note}
The first time you connect, WRDS will send a **Duo two-factor authentication push** to your registered device. Follow the prompts to approve it. Subsequent connections using the `.pgpass` file will not prompt for a password, but may still require Duo depending on your session. See [WRDS two-factor authentication setup](https://wrds-www.wharton.upenn.edu/pages/about/log-in-to-wrds-using-two-factor-authentication/) if you have not yet enrolled.
:::

Test your connection by fetching a few rows:

```python
df = conn.get_table(library="crsp", table="dsf", obs=10)
print(df.columns.tolist())
print(len(df))
```

### R

Install the required packages into your R environment on KLC (only needed once):

```r
install.packages(c("DBI", "RPostgres"))
```

Connect to WRDS in R:

```r
library(DBI)
library(RPostgres)

wrds <- dbConnect(
  Postgres(),
  host    = "wrds-pgdata.wharton.upenn.edu",
  port    = 9737,
  dbname  = "wrds",
  sslmode = "require",
  user    = "your-wrds-username"
)
```

:::{note}
The first time you connect, WRDS will send a **Duo two-factor authentication push** to your registered device. See [WRDS two-factor authentication setup](https://wrds-www.wharton.upenn.edu/pages/about/log-in-to-wrds-using-two-factor-authentication/) if you have not yet enrolled.
:::

Test your connection by fetching a few rows:

```r
res  <- dbSendQuery(wrds, "SELECT * FROM crsp.dsf LIMIT 10")
data <- dbFetch(res)
print(colnames(data))
print(nrow(data))
dbClearResult(res)
```

## Exploring Libraries and Tables

Before writing a query, you often need to know the exact library name (called a "schema" in PostgreSQL) and table name. WRDS organizes data into libraries by vendor; for example, CRSP data lives in the `crsp` library and Compustat data lives in `comp`.

You can also browse the [WRDS Data Vendors page](https://wrds-www.wharton.upenn.edu/pages/about/data-vendors/) and [WRDS Data Dictionaries](https://wrds-www.wharton.upenn.edu/data-dictionary/) in your browser.

### Python

```python
# List all libraries (schemas) your account can access
libs = conn.list_libraries()
print(libs)

# List all tables in a library
tables = conn.list_tables(library="crsp")
print(tables)

# Describe the columns of a specific table
desc = conn.describe_table(library="crsp", table="dsf")
print(desc)
```

### R

```r
# List all libraries (schemas)
libs <- dbGetQuery(wrds, "SELECT schema_name FROM information_schema.schemata ORDER BY schema_name")
print(libs)

# List tables in a specific library
tables <- dbGetQuery(wrds, "SELECT table_name FROM information_schema.tables WHERE table_schema = 'crsp' ORDER BY table_name")
print(tables)

# Describe the columns of a specific table
desc <- dbGetQuery(wrds, "
  SELECT column_name, data_type, is_nullable
  FROM information_schema.columns
  WHERE table_schema = 'crsp' AND table_name = 'dsf'
  ORDER BY ordinal_position
")
print(desc)
```

## Querying Data

### Python

Use `get_table()` to retrieve an entire table (with an optional row limit):

```python
df = conn.get_table(library="crsp", table="dsf", obs=1000)
```

Use `raw_sql()` for filtered queries:

```python
df = conn.raw_sql(
    """
    SELECT permno, date, ret
    FROM crsp.dsf
    WHERE date BETWEEN '2023-01-01' AND '2023-12-31'
    """,
    date_cols=["date"],
)
conn.close()
```

### R

```r
df <- dbGetQuery(
  wrds,
  "SELECT permno, date, ret
   FROM crsp.dsf
   WHERE date BETWEEN '2023-01-01' AND '2023-12-31'"
)
dbDisconnect(wrds)
```

## A Note on Reproducibility

WRDS datasets are updated and revised over time — data you pull today may differ from a pull made in six months. Save a local copy of any data you use in a project so your analysis is reproducible later:

```python
df.to_csv("/kellogg/proj/your-netid/data/crsp_dsf_2023.csv", index=False)
```

```r
write.csv(df, "/kellogg/proj/your-netid/data/crsp_dsf_2023.csv", row.names = FALSE)
```

## Datasets Available on WRDS

See [Find Data by Platform — WRDS](platform-wrds) for the full list of Kellogg-licensed datasets available through WRDS. Dataset documentation pages are being added progressively.
