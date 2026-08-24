# WRDS

(wrds)=

[Wharton Research Data Services (WRDS)](https://wrds-www.wharton.upenn.edu/) is a research platform that provides access to a broad range of financial, economic, and marketing datasets — including CRSP, Compustat, Execucomp, and many others. WRDS is operated by the Wharton School of the University of Pennsylvania; Kellogg maintains a site license that gives all faculty, PhD students, and approved researchers access.

WRDS is one of three platforms under [Kellogg Data Hosting](../kdc). Unlike Athena and Redivis, WRDS is operated by the Wharton School and accessed through their infrastructure directly.

## Gaining Access

1. Go to [wrds-www.wharton.upenn.edu](https://wrds-www.wharton.upenn.edu/) and click **Register**.
2. Register using your Northwestern email address (e.g., `name@kellogg.northwestern.edu`).
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

(setting-up-credentials)=

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

## Setting Up Your Environment

KRS maintains a shared conda environment on KLC with the `wrds` package pre-installed. Install the required R packages into your own R environment on KLC (only needed once).

::::{tab-set}

:::{tab-item} Python
:sync: python

```bash
module load mamba
source activate /kellogg/software/envs/wrds25_env
```

You can also install the package into your own environment:

```bash
mamba install -c conda-forge wrds
# or: pip install wrds
```

:::

:::{tab-item} R
:sync: r

```r
install.packages(c("DBI", "RPostgres"))
```

:::

::::

## Connecting and Authenticating

(connecting-from-klc)=

Open a connection to WRDS using your WRDS username. The `.pgpass` file supplies your password automatically.

::::{tab-set}

:::{tab-item} Python
:sync: python

```python
import wrds

conn = wrds.Connection(wrds_username="your-wrds-username")
```

Test your connection:

```python
print(len(conn.list_libraries()))
```

:::

:::{tab-item} R
:sync: r

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

Test your connection:

```r
dbGetQuery(wrds, "SELECT 1")
```

:::

::::

:::{note}
The first time you connect, WRDS will send a **Duo two-factor authentication push** to your registered device. Follow the prompts to approve it. Subsequent connections using the `.pgpass` file will not prompt for a password, but may still require Duo depending on your session. See [WRDS two-factor authentication setup](https://wrds-www.wharton.upenn.edu/pages/about/log-in-to-wrds-using-two-factor-authentication/) if you have not yet enrolled.
:::

## Exploring Libraries and Tables

Before writing a query, you often need to know the exact library name (called a "schema" in PostgreSQL) and table name. WRDS organizes data into libraries by vendor; for example, CRSP data lives in the `crsp` library and Compustat data lives in `comp`.

You can also browse the [WRDS Data Vendors page](https://wrds-www.wharton.upenn.edu/pages/about/data-vendors/) and [WRDS Data Dictionaries](https://wrds-www.wharton.upenn.edu/data-dictionary/) in your browser.

### List All Libraries

A library refers to a database on WRDS (for example, `crsp`, `comp` for Compustat). Use `conn.list_libraries()` to retrieve a list of all databases your institution has access to. Sorting the results alphabetically makes them easier to browse.

::::{tab-set}

:::{tab-item} Python
:sync: python

```python
libraries = conn.list_libraries()
print(len(libraries))
print(sorted(libraries)[:20])
```

:::

:::{tab-item} R
:sync: r

```r
libs <- dbGetQuery(
  wrds,
  "SELECT schema_name FROM information_schema.schemata ORDER BY schema_name"
)
print(libs)
```

:::

::::

### List All Datasets in a Library

Each library contains many individual tables or datasets (for example, `company`, `funda`, `msf`). Use `conn.list_tables(library=...)` to list all available tables within a given library. Specify the library name as a string (for example, `'comp'` for Compustat).

::::{tab-set}

:::{tab-item} Python
:sync: python

```python
print(conn.list_tables(library="comp"))
```

:::

:::{tab-item} R
:sync: r

```r
tables <- dbGetQuery(
  wrds,
  "SELECT table_name FROM information_schema.tables
   WHERE table_schema = 'comp'
   ORDER BY table_name"
)
print(tables)
```

:::

::::

### Describe a Table

Before querying, inspect the columns and data types of a specific table.

::::{tab-set}

:::{tab-item} Python
:sync: python

```python
desc = conn.describe_table(library="crsp", table="dsf")
print(desc)
```

:::

:::{tab-item} R
:sync: r

```r
desc <- dbGetQuery(
  wrds,
  "SELECT column_name, data_type, is_nullable
   FROM information_schema.columns
   WHERE table_schema = 'crsp' AND table_name = 'dsf'
   ORDER BY ordinal_position"
)
print(desc)
```

:::

::::

For step-by-step workflows that pull and analyze data from specific datasets, see the worked examples below.

## Worked Examples

```{note}
The examples below are a selected subset of WRDS datasets with worked documentation on this site, not an exhaustive catalog. For an exhaustive list of datasets available to Kellogg researchers, see the [Kellogg Research Support Datasets page](https://www.kellogg.northwestern.edu/academics-research/research-support/dataset/).
```

Step-by-step examples for querying specific WRDS datasets from KLC. Each example covers a complete workflow in Python and R.

:::::{grid} 1 2 3 3
:gutter: 2

::::{grid-item-card} CRSP
:link: examples/crsp-example
:link-type: doc

Look up a stock by ticker, pull monthly returns from the CRSP monthly stock file, and plot cumulative return over time.
::::

::::{grid-item-card} NYSE Trade and Quote (TAQ)
:link: examples/taq-example
:link-type: doc

Fetch intraday trade data for a single stock on one trading day, compute five-minute average prices, and graph the result.
::::

::::{grid-item-card} Revelio Labs
:link: examples/revelio-example
:link-type: doc

Look up a firm by ticker, pull U.S. employment position spells, build a monthly weighted headcount and separation-rate panel, and plot the result.
::::

:::::

## A Note on Reproducibility

(a-note-on-reproducibility)=

WRDS datasets are updated and revised over time — data you pull today may differ from a pull made in six months. Save a local copy of any data you use in a project so your analysis is reproducible later:

```python
df.to_csv("/kellogg/proj/your-netid/data/crsp_dsf_2023.csv", index=False)
```

```r
write.csv(df, "/kellogg/proj/your-netid/data/crsp_dsf_2023.csv", row.names = FALSE)
```

## Datasets Available on WRDS

See [Find Data by Platform — WRDS](platform-wrds) for a convenience index of datasets documented on this site that are available through WRDS. Dataset documentation pages are being added progressively. For an exhaustive list of datasets available to Kellogg researchers, see the [Kellogg Research Support Datasets page](https://www.kellogg.northwestern.edu/academics-research/research-support/dataset/).

```{toctree}
:maxdepth: 2
:hidden:

CRSP Example <examples/crsp-example>
TAQ Example <examples/taq-example>
Revelio Labs Example <examples/revelio-example>
```
