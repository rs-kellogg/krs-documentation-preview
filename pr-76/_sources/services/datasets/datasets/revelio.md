(revelio)=
# Revelio Labs

## At a Glance

| | |
|---|---|
| **Provider** | Revelio Labs |
| **Coverage** | Snapshots (job postings: October 5, 2026; individual and lookup tables: October 19, 2026) on KLC; live tables on WRDS |
| **Geographic scope** | Global |
| **Update frequency** | Quarterly on KLC; monthly on WRDS |
| **Access platforms** | WRDS, KLC (local Parquet files) |
| **Eligible users** | <!-- TODO(KRS): confirm eligibility and license terms --> Northwestern community |
| **Questions** | [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) |

## Description

Revelio Labs compiles public professional profiles, job postings, and employee reviews into standardized, company-linked datasets. The tables fall into five groups:

- **Individual profiles**: one row per person, with predicted demographics, education, skills, and work history
- **Positions**: one row per employment spell, with company, location, role, seniority, and salary estimates
- **Job postings**: one row per posting, with company, role, location, salary, and source flags, plus a separate table of posting text
- **Company and school reference tables**: company identifiers, school mapping, and regions
- **Lookup and sentiment tables**: role and skill taxonomies, layoffs, and company sentiment scores

Revelio's data is available on [WRDS](/services/kellogg-data-hosting/wrds/wrds) in the `revelio` library. A bulk export of most tables is also stored as Parquet files on KLC, where we query it with [DuckDB](https://duckdb.org/) on the KLC file system without moving data over the network. Start with [Querying with DuckDB on KLC](revelio-duckdb). The WRDS-based workflow is covered in the [Revelio Labs WRDS example](/services/kellogg-data-hosting/wrds/examples/revelio-example).

## Access

Access is restricted to members of the Northwestern University community. Email [Kellogg Research Support](mailto:rs@kellogg.northwestern.edu) to request access.

- **KLC**: requires a KLC account. See [How to Access KLC](/services/klc/user-guide/klc-accessing) if you do not have one.
- **WRDS**: requires a WRDS account with Revelio access. See the [WRDS page](/services/kellogg-data-hosting/wrds/wrds).

<!-- TODO(KRS): confirm the access request process for the local KLC files (group membership vs. email request) -->

:::{important}
`individual_user` and the `individual_*` tables describe real people, including names and model-inferred demographics. Use of this data is subject to Revelio's license terms. Do not use it to re-identify individuals, and do not share raw records outside your approved research project.
:::

## Choosing Between WRDS and Local Parquet on KLC

| | WRDS | Local Parquet on KLC |
|---|---|---|
| **Tables** | All 33 tables in the `revelio` library | 31 tables (see [WRDS-Only Tables](revelio-wrds-only)) |
| **Freshness** | Revelio's current WRDS release | Fixed snapshot; dates are in the folder names |
| **Best for** | Single-firm pulls, `workforce_dynamics_geo` | Full-scale scans and aggregations over billions of rows |
| **Tooling** | `wrds` Python package, `RPostgres`, SAS | DuckDB |
| **Network** | Queries run on WRDS and results transfer to KLC | Reads from the KLC file system |

On KLC, look up a firm's `rcid` in `company_mapping`, then follow [Querying with DuckDB on KLC](revelio-duckdb). File paths and column definitions are in [Data Located on KLC](revelio-klc-data).

(revelio-duckdb)=
## Querying with DuckDB on KLC

DuckDB reads the Parquet files in place. On KLC main, cap every session at 16 threads and 128 GB. Queries that filter, aggregate, or write an extract stay on KLC main. Read [Use KLC Reserve Above This Budget](revelio-reserve) only when you will load the entire contents of one or more tables into memory.

### Before You Start

- Log in to KLC. See [How to Access KLC](/services/klc/user-guide/klc-accessing) if you do not have an account.
- Create a conda environment under `/kellogg/proj/<your-netid>/`. See [Conda Environments on KLC](/services/klc/user-guide/klc-conda).
- Store views and extracts under `/kellogg/proj/<your-netid>/revelio`. Home directories are 80 GB.
- Send DuckDB spill files to `/scratch/$USER/duckdb_tmp`. The Python and R examples set that path from the `USER` environment variable.

```bash
module load mamba/24.3.0
mamba create -p /kellogg/proj/<your-netid>/envs/revelio-duckdb -c conda-forge python-duckdb
source activate /kellogg/proj/<your-netid>/envs/revelio-duckdb
mkdir -p /kellogg/proj/<your-netid>/revelio /scratch/$USER/duckdb_tmp
```

For R, add `duckdb` and `DBI` to an R environment from the same conda page. Replace `<your-netid>` in every path below.

<!-- TODO(KRS): confirm the recommended way to get DuckDB on KLC (module, shared environment, or per-user install) and add the DuckDB command-line client if it is available -->

### Where to Run the Query

KLC main is the default. Check [KLC Node Resources](/services/klc-node-resources) and use a node with at least 128 GB free. A cap of 16 threads stays within the [24-core limit](/services/klc-reserve/when-to-use) on KLC main.

| Query | Where to Run |
|---|---|
| A DuckDB query that filters, aggregates, or writes an extract, including `DESCRIBE` and an unfiltered `COUNT(*)` | KLC main, at 16 threads and 128 GB |
| Reading the entire contents of one or more tables into pandas, Polars, or R | [Use KLC Reserve Above This Budget](revelio-reserve) |

### Query Rules

- Set `threads = 16` and `memory_limit = '128GB'` when you connect on KLC main. Raise either value only in a [KLC Reserve](revelio-reserve) job that loads entire tables into memory and requests those resources.
- Name the columns you need. DuckDB then skips the other Parquet columns, including `description` and review text.
- Filter and aggregate in DuckDB. Do not pull `individual_positions`, `postings_cosmos`, or `individual_user_skills` into pandas, Polars, or R.
- Save an extract under `/kellogg/proj/<your-netid>/revelio/` for repeated work. The files are not partitioned by `rcid`, so a firm filter still reads many parts.
- Run `DESCRIBE` or an unfiltered `COUNT(*)` to inspect a table. Both read Parquet metadata only.

### Create Views Once

A view gives each table a short name and hides the file glob. This script stores view definitions in a small DuckDB file. DuckDB reads the Parquet files when you query a view. Run the script again when a new snapshot folder replaces the dates below. The connection uses the same 16-thread and 128 GB cap.

```python
import os
import duckdb

TEMP_DIRECTORY = f"/scratch/{os.environ['USER']}/duckdb_tmp"

ROOT = "/kellogg/data/revelio"
JOBS = f"{ROOT}/Oct52026/revelio_job_postings"
INDIV = f"{ROOT}/Oct192026/revelio_individual"
MISC = f"{ROOT}/Oct192026/revelio"

tables = {
    # Job postings
    "postings_cosmos": JOBS,
    # Individual profiles
    "individual_positions": INDIV,
    "individual_positions_raw": INDIV,
    "individual_user": INDIV,
    "individual_user_raw": INDIV,
    "individual_user_education": INDIV,
    "individual_user_education_raw": INDIV,
    "individual_user_skills": INDIV,
    # Company, lookup, and miscellaneous tables
    "company_mapping": MISC,
    "individual_role_lookup_v2": MISC,
    "individual_role_lookup_v3": MISC,
    "postings_role_lookup_v2": MISC,
    "postings_role_lookup_v3": MISC,
    "individual_user_skill_lookup": MISC,
    "layoffs": MISC,
    "months": MISC,
    "regions": MISC,
    "school_mapping": MISC,
    "sentiment_individual_reviews": MISC,
    "sentiment_role_lookup": MISC,
    "sentiment_scores": MISC,
}

# Replace <your-netid> with your NetID
con = duckdb.connect(
    "/kellogg/proj/<your-netid>/revelio/revelio_views.duckdb",
    config={
        "threads": 16,
        "memory_limit": "128GB",
        "temp_directory": TEMP_DIRECTORY,
        "max_temp_directory_size": "200GB",
    },
)
con.execute("SET preserve_insertion_order = false")

for name, base in tables.items():
    con.execute(
        f"CREATE OR REPLACE VIEW {name} AS "
        f"SELECT * FROM read_parquet('{base}/{name}/*.parquet')"
    )

# Combined posting text for filtered joins, including a country-year extract.
raw_parts = [f"'{JOBS}/postings_cosmos_raw_p{i}/*.parquet'" for i in range(10)]
con.execute(
    "CREATE OR REPLACE VIEW postings_cosmos_raw AS "
    f"SELECT * FROM read_parquet([{', '.join(raw_parts)}])"
)

con.close()
```

`postings_cosmos_raw` unions all 10 posting-text tables. Use it for a filtered join, including the country-year extract in [Extract Posting Text for a Country and Year](revelio-country-postings). The join filters to the target `job_id`s first, so the memory footprint stays low.

Open the read-only connection from [Open a Connection](revelio-duckdb-limits) and check the views:

```sql
SHOW TABLES;

DESCRIBE company_mapping;

SELECT COUNT(*) AS n_companies FROM company_mapping;
```

(revelio-duckdb-limits)=
(revelio-run-query)=
### Open a Connection

Open the views file from the previous section. Set the cap on every connection, then run every later snippet in that same session. Each example below has a DuckDB tab and a WRDS tab. DuckDB reads the local Parquet views. The WRDS client queries the `revelio` library. For WRDS, complete [Setting Up Credentials](setting-up-credentials) and [Connecting from KLC](connecting-from-klc). Call `.pl()` instead of `.df()` when you want a Polars data frame from DuckDB.

The Python and R snippets set `temp_directory` from the `USER` environment variable. In the SQL tab, replace `<your-netid>` with your NetID.

::::{tab-set}

:::{tab-item} DuckDB
:sync: duckdb

```python
import os
import duckdb

TEMP_DIRECTORY = f"/scratch/{os.environ['USER']}/duckdb_tmp"

con = duckdb.connect(
    "/kellogg/proj/<your-netid>/revelio/revelio_views.duckdb",
    read_only=True,
    config={
        "threads": 16,
        "memory_limit": "128GB",
        "temp_directory": TEMP_DIRECTORY,
        "max_temp_directory_size": "200GB",
    },
)
con.execute("SET preserve_insertion_order = false")
```

:::

:::{tab-item} R
:sync: r

```r
library(DBI)
library(duckdb)

con <- dbConnect(
  duckdb(),
  dbdir = "/kellogg/proj/<your-netid>/revelio/revelio_views.duckdb",
  read_only = TRUE,
  config = list(
    threads = "16",
    memory_limit = "128GB",
    temp_directory = paste0("/scratch/", Sys.getenv("USER"), "/duckdb_tmp"),
    max_temp_directory_size = "200GB"
  )
)
dbExecute(con, "SET preserve_insertion_order = false")
```

:::

:::{tab-item} SQL

```sql
SET threads = 16;
SET memory_limit = '128GB';
SET temp_directory = '/scratch/<your-netid>/duckdb_tmp';
SET max_temp_directory_size = '200GB';
SET preserve_insertion_order = false;
```

:::

:::{tab-item} WRDS
:sync: wrds

```python
import wrds

conn = wrds.Connection(wrds_username="your-wrds-username")
```

:::

::::

| Setting | Controls | KLC Main Value |
|---|---|---|
| `threads` | CPU threads for query execution | `SET threads = 16;` |
| `memory_limit` | Maximum memory DuckDB uses before spilling to disk | `SET memory_limit = '128GB';` |
| `temp_directory` | Where DuckDB writes spill files | `SET temp_directory = '/scratch/<your-netid>/duckdb_tmp';` |
| `max_temp_directory_size` | Cap on total spill-file size | `SET max_temp_directory_size = '200GB';` |
| `preserve_insertion_order` | `false` lowers memory use for large scans and exports | `SET preserve_insertion_order = false;` |

The Python and R snippets fill `temp_directory` from `USER`. The SQL value above is the same path with your NetID written out.

Confirm the active values:

```sql
SELECT current_setting('threads') AS threads,
       current_setting('memory_limit') AS memory_limit,
       current_setting('temp_directory') AS temp_directory;
```

| Where You Run | `threads` | `memory_limit` |
|---|---|---|
| KLC main | 16 | `128GB` |
| KLC Reserve | The `--ntasks` value you request | About 90% of the `--mem` value you request |

When a query exceeds `memory_limit`, DuckDB spills to `temp_directory` and keeps running. When the spill would pass `max_temp_directory_size`, raise that cap. Loading an entire table into memory is covered in [Use KLC Reserve Above This Budget](revelio-reserve). See [High-Memory Jobs](/services/klc-reserve/highmem-jobs) for requests above 128 GB.

:::{note}
`memory_limit` applies to DuckDB's own buffers. Converting a result to pandas or R with `.df()` or `dbGetQuery()` allocates additional memory outside the limit. Return an aggregate or a small extract on KLC main.
:::

Close the session when you are finished: `con.close()` in DuckDB, or `conn.close()` in WRDS.

:::{warning}
Do not pull `individual_user_skills` (about 11.8 billion rows), `postings_cosmos` (about 2.9 billion rows), or `individual_positions` (about 1.8 billion rows) into pandas, Polars, or R in full. Filter or aggregate in DuckDB or in the WRDS query first. On WRDS, pass `chunksize` to `raw_sql` when a single-firm extract is still large.
:::

(revelio-one-firm)=
### One Firm, End to End

Run these four steps in order in the session opened above. Replace `123456` with the `rcid` from the first query. The DuckDB headcount reads the extract from step 3. The WRDS headcount applies the same filters on `revelio.individual_positions`.

#### Find a Firm's rcid

Look up `rcid` by ticker or name. `company_mapping` is a small table.

::::{tab-set}

:::{tab-item} DuckDB
:sync: duckdb

```python
df = con.sql("""
    SELECT rcid, company, ticker, cik, ultimate_parent_company_name
    FROM company_mapping
    WHERE ticker = 'AAPL'
       OR company ILIKE 'apple inc%'
    LIMIT 20
""").df()
print(df)
```

:::

:::{tab-item} WRDS
:sync: wrds

```python
df = conn.raw_sql("""
    SELECT rcid, company, ticker, cik, ultimate_parent_company_name
    FROM revelio.company_mapping
    WHERE ticker = 'AAPL'
       OR company ILIKE 'apple inc%'
    LIMIT 20
""")
print(df)
```

:::

::::

<!-- TODO(KRS): confirm the ticker and company name literals for the example firm in the local Parquet files -->

#### Count Positions for One Firm

Count the firm's position rows in the database. This returns one number.

::::{tab-set}

:::{tab-item} DuckDB
:sync: duckdb

```python
df = con.sql("""
    SELECT COUNT(*) AS n_positions
    FROM individual_positions
    WHERE rcid = 123456
""").df()
print(df)
```

:::

:::{tab-item} WRDS
:sync: wrds

```python
df = conn.raw_sql("""
    SELECT COUNT(*) AS n_positions
    FROM revelio.individual_positions
    WHERE rcid = 123456
""")
print(df)
```

:::

::::

(revelio-extract)=
#### Save an Extract

Write the columns you need to your own Parquet file, then query the extract for repeated work. On DuckDB, `preserve_insertion_order` is already `false` on the connection above.

::::{tab-set}

:::{tab-item} DuckDB
:sync: duckdb

```python
con.execute("""
    COPY (
        SELECT
            user_id,
            position_id,
            rcid,
            startdate,
            enddate,
            country,
            weight,
            salary
        FROM individual_positions
        WHERE rcid = 123456
    ) TO '/kellogg/proj/<your-netid>/revelio/positions_rcid_123456.parquet'
      (FORMAT parquet, COMPRESSION zstd)
""")
print(con.sql("""
    SELECT COUNT(*)
    FROM read_parquet('/kellogg/proj/<your-netid>/revelio/positions_rcid_123456.parquet')
""").df())
```

:::

:::{tab-item} WRDS
:sync: wrds

```python
positions = conn.raw_sql(
    """
    SELECT user_id, position_id, rcid, startdate, enddate,
           country, weight, salary
    FROM revelio.individual_positions
    WHERE rcid = 123456
    """,
    date_cols=["startdate", "enddate"],
)
positions.to_parquet(
    "/kellogg/proj/<your-netid>/revelio/positions_rcid_123456.parquet",
    index=False,
)
print(len(positions))
```

:::

::::

#### Monthly Headcount from the Extract

Compute a weighted monthly headcount for 2019 to 2023. The longer WRDS walkthrough, including separation rates and a plot, is the [Revelio Labs WRDS example](/services/kellogg-data-hosting/wrds/examples/revelio-example).

::::{tab-set}

:::{tab-item} DuckDB
:sync: duckdb

```python
df = con.sql("""
    WITH months AS (
        SELECT CAST(m AS DATE) AS month_start
        FROM generate_series(
            DATE '2019-01-01', DATE '2023-12-01', INTERVAL 1 MONTH
        ) AS t(m)
    )
    SELECT
        m.month_start,
        SUM(p.weight) AS weighted_headcount,
        COUNT(*) AS n_positions
    FROM months AS m
    JOIN read_parquet('/kellogg/proj/<your-netid>/revelio/positions_rcid_123456.parquet') AS p
      ON p.startdate <= m.month_start
     AND (p.enddate IS NULL OR p.enddate > m.month_start)
    WHERE p.country = 'United States'
    GROUP BY m.month_start
    ORDER BY m.month_start
""").df()
print(df.head())
```

:::

:::{tab-item} WRDS
:sync: wrds

```python
df = conn.raw_sql(
    """
    SELECT
        gs.month_start,
        SUM(p.weight) AS weighted_headcount,
        COUNT(*) AS n_positions
    FROM generate_series(
        DATE '2019-01-01', DATE '2023-12-01', INTERVAL '1 month'
    ) AS gs(month_start)
    JOIN revelio.individual_positions AS p
      ON p.startdate <= gs.month_start
     AND (p.enddate IS NULL OR p.enddate > gs.month_start)
    WHERE p.rcid = 123456
      AND p.country = 'United States'
    GROUP BY gs.month_start
    ORDER BY gs.month_start
    """,
    date_cols=["month_start"],
)
print(df.head())
```

:::

::::

<!-- TODO(KRS): confirm the country literal in the local Parquet files, as in the WRDS example -->

### More Examples

Use the session from [Open a Connection](revelio-run-query). Run `DESCRIBE` on a DuckDB view before a join, and cast both sides of a join key when the types differ. See [Key Identifiers and Joins](revelio-identifiers).

#### Positions by Role Group

Run this on KLC main at 16 threads and 128 GB. For repeated DuckDB runs, add `role_k17000_v3` and `remote_suitability` to the extract in [Save an Extract](revelio-extract) and query that file.

::::{tab-set}

:::{tab-item} DuckDB
:sync: duckdb

```python
df = con.sql("""
    SELECT
        l.role_k50_v3,
        COUNT(*) AS n_positions,
        AVG(p.salary) AS avg_predicted_salary,
        AVG(p.remote_suitability) AS avg_remote_suitability
    FROM individual_positions AS p
    JOIN individual_role_lookup_v3 AS l
      ON p.role_k17000_v3 = l.role_k17000_v3
    WHERE p.rcid = 123456
    GROUP BY l.role_k50_v3
    ORDER BY n_positions DESC
""").df()
print(df)
```

:::

:::{tab-item} WRDS
:sync: wrds

```python
df = conn.raw_sql("""
    SELECT
        l.role_k50_v3,
        COUNT(*) AS n_positions,
        AVG(p.salary) AS avg_predicted_salary,
        AVG(p.remote_suitability) AS avg_remote_suitability
    FROM revelio.individual_positions AS p
    JOIN revelio.individual_role_lookup_v3 AS l
      ON p.role_k17000_v3 = l.role_k17000_v3
    WHERE p.rcid = 123456
    GROUP BY l.role_k50_v3
    ORDER BY n_positions DESC
""")
print(df)
```

:::

::::

#### Skills of One Firm's Employees

Run this on KLC main at 16 threads and 128 GB. The result is an aggregate, so this query stays on KLC main. The firm filter runs first. DuckDB uses `SEMI JOIN` so the skills scan stays on those users. WRDS uses an inner join for the same filter. Prefer the DuckDB tab when the skills table is the main scan.

::::{tab-set}

:::{tab-item} DuckDB
:sync: duckdb

```python
df = con.sql("""
    WITH firm_users AS (
        SELECT DISTINCT user_id
        FROM individual_positions
        WHERE rcid = 123456
    )
    SELECT
        k.skill_k50,
        COUNT(*) AS n_skill_records,
        COUNT(DISTINCT s.user_id) AS n_users
    FROM individual_user_skills AS s
    SEMI JOIN firm_users AS u
      ON s.user_id = u.user_id
    JOIN individual_user_skill_lookup AS k
      ON s.skill_k35000 = k.skill_k35000
    GROUP BY k.skill_k50
    ORDER BY n_users DESC
    LIMIT 25
""").df()
print(df)
```

:::

:::{tab-item} WRDS
:sync: wrds

```python
df = conn.raw_sql("""
    WITH firm_users AS (
        SELECT DISTINCT user_id
        FROM revelio.individual_positions
        WHERE rcid = 123456
    )
    SELECT
        k.skill_k50,
        COUNT(*) AS n_skill_records,
        COUNT(DISTINCT s.user_id) AS n_users
    FROM revelio.individual_user_skills AS s
    JOIN firm_users AS u
      ON s.user_id = u.user_id
    JOIN revelio.individual_user_skill_lookup AS k
      ON s.skill_k35000 = k.skill_k35000
    GROUP BY k.skill_k50
    ORDER BY n_users DESC
    LIMIT 25
""")
print(df)
```

:::

::::

(revelio-country-postings)=
#### Extract Posting Text for a Country and Year

Run this filtered join on KLC main at 16 threads and 128 GB. `postings_cosmos_raw` is the combined view of all 10 posting-text tables. The join filters to the target `job_id`s first, so the memory footprint stays low. On WRDS, posting text is the single table `revelio.postings_cosmos_raw`.

::::{tab-set}

:::{tab-item} DuckDB
:sync: duckdb

```python
con.execute("""
    CREATE TEMP TABLE target_postings AS
    SELECT DISTINCT
        CAST(job_id AS HUGEINT) AS job_id,
        rcid,
        company,
        post_date
    FROM postings_cosmos
    WHERE country = 'Hong Kong'
      AND post_date >= DATE '2026-01-01'
      AND post_date < DATE '2027-01-01'
      AND job_id IS NOT NULL
""")
con.execute("""
    COPY (
        SELECT t.*, r.title_raw, r.jobtitle_translated, r.description
        FROM postings_cosmos_raw AS r
        JOIN target_postings AS t
          ON CAST(r.job_id AS HUGEINT) = t.job_id
    ) TO '/kellogg/proj/<your-netid>/revelio/hong_kong_postings_2026.parquet'
      (FORMAT parquet, COMPRESSION zstd)
""")
```

For text alone, replace `JOIN` with `SEMI JOIN` and select `r.job_id, r.description`.

:::

:::{tab-item} WRDS
:sync: wrds

```python
chunks = conn.raw_sql(
    """
    SELECT
        c.job_id, c.rcid, c.company, c.post_date,
        r.title_raw, r.jobtitle_translated, r.description
    FROM revelio.postings_cosmos AS c
    JOIN revelio.postings_cosmos_raw AS r
      ON CAST(c.job_id AS NUMERIC) = CAST(r.job_id AS NUMERIC)
    WHERE c.country = 'Hong Kong'
      AND c.post_date >= DATE '2026-01-01'
      AND c.post_date < DATE '2027-01-01'
    """,
    date_cols=["post_date"],
    chunksize=100_000,
)
```

`chunksize` returns an iterator of data frames. A country-year of posting text is large. Prefer the DuckDB tab when you want one Parquet file on the KLC file system.

:::

::::

<!-- TODO(KRS): confirm the country literal ('Hong Kong') and that job_id values in postings_cosmos_raw_p* match postings_cosmos after the HUGEINT cast; compare matched row counts to the number of target postings -->

(revelio-reserve)=
### Use KLC Reserve Above This Budget

Filtered scans, aggregates, and extracts stay on KLC main, including the country-year join against `postings_cosmos_raw`. Use [KLC Reserve](/services/klc-reserve/when-to-use) when you will read the entire contents of one or more tables into memory with `.df()`, Polars, or `dbGetQuery()`.

The script below reads `SLURM_NTASKS` and `SLURM_MEM_PER_NODE` (megabytes, set by `--mem`) and sets `memory_limit` to about 90% of that grant. Outside a SLURM job it uses the KLC main cap of 16 threads and 128 GB. Raise `--ntasks` and `--mem` when the in-memory table needs more than that. For RAM above a standard Reserve node, see [High-Memory Jobs](/services/klc-reserve/highmem-jobs).

:::{warning}
Do not load `individual_user_skills`, `postings_cosmos`, or `individual_positions` in full.
:::

Save this script as `revelio_job.py`:

```python
import os
import duckdb

TEMP_DIRECTORY = f"/scratch/{os.environ['USER']}/duckdb_tmp"

if os.environ.get("SLURM_JOB_ID"):
    threads = int(os.environ["SLURM_NTASKS"])
    mem_mb = int(os.environ["SLURM_MEM_PER_NODE"])
    memory_limit = f"{int(mem_mb * 0.9 / 1024)}GB"
else:
    threads = 16
    memory_limit = "128GB"

con = duckdb.connect(
    "/kellogg/proj/<your-netid>/revelio/revelio_views.duckdb",
    read_only=True,
    config={
        "threads": threads,
        "memory_limit": memory_limit,
        "temp_directory": TEMP_DIRECTORY,
        "max_temp_directory_size": "200GB",
    },
)
con.execute("SET preserve_insertion_order = false")

df = con.sql("SELECT * FROM sentiment_individual_reviews").df()
```

Save this as `revelio_job.sh`:

```bash
#!/bin/bash
#SBATCH --account=kellogg
#SBATCH --partition=kellogg
#SBATCH --job-name=revelio-duckdb
#SBATCH --nodes=1
#SBATCH --ntasks=16
#SBATCH --mem=128G
#SBATCH --time=04:00:00
#SBATCH --output=logs/slurm-%j.out

module purge
module use --append /kellogg/software/Modules/modulefiles
module load mamba/24.3.0
source activate /kellogg/proj/<your-netid>/envs/revelio-duckdb

mkdir -p /scratch/$USER/duckdb_tmp
python revelio_job.py
```

`#SBATCH --output` is opened when the job starts, so create the log directory before you submit. For submission options, monitoring, and tuning, see [Submitting SLURM Jobs](/services/klc-reserve/slurm-jobs).

```bash
mkdir -p logs
sbatch revelio_job.sh
```

(revelio-klc-data)=
## Data Located on KLC

All local files live under `/kellogg/data/revelio/`, in one folder per snapshot date:

| Folder | Contents |
|---|---|
| `/kellogg/data/revelio/Oct52026/revelio_job_postings/` | Job posting tables |
| `/kellogg/data/revelio/Oct192026/revelio_individual/` | Individual profile, position, education, and skills tables |
| `/kellogg/data/revelio/Oct192026/revelio/` | Company mapping, lookup, layoff, school, region, and sentiment tables |

Each table is a **directory** of Parquet files named `part-000000.parquet`, `part-000001.parquet`, and so on. Each directory also holds `_manifest.json`, `_plan.json`, and `_spec.json` metadata files that DuckDB ignores when you read `*.parquet`. Each snapshot folder includes a `download.log` recording the export.

:::{note}
A table is the whole directory, not a single file. Always read all of its parts with a glob such as `/kellogg/data/revelio/Oct192026/revelio_individual/individual_positions/*.parquet`.
:::

**Scale** is `Small` or `Large`. A large table still runs on KLC main within 16 threads and 128 GB when you name columns, filter, and aggregate in DuckDB. Use [KLC Reserve](revelio-reserve) when you will load the entire contents of one or more tables into memory.

### Job Postings

Path prefix: `/kellogg/data/revelio/Oct52026/revelio_job_postings/`

| Table | Approximate Rows | Scale | Description |
|---|---|---|---|
| `postings_cosmos` | 2.92 billion | Large | Posting-level attributes: company, role, location, salary, dates, and source flags |
| `postings_cosmos_raw_p0` to `postings_cosmos_raw_p9` | 292 million each | Large | Posting text (raw title, translated title, raw location, description), split into 10 tables |

### Individual Profiles

Path prefix: `/kellogg/data/revelio/Oct192026/revelio_individual/`

| Table | Approximate Rows | Scale | Description |
|---|---|---|---|
| `individual_positions` | 1.83 billion | Large | Mapped position spells: company, location, role, seniority, salary |
| `individual_positions_raw` | 1.83 billion | Large | Position text as reported: raw company, location, title, description |
| `individual_user` | 921 million | Large | Profile-level attributes and predicted demographics |
| `individual_user_raw` | 921 million | Large | Profile title and summary |
| `individual_user_education` | 799 million | Large | Mapped education records |
| `individual_user_education_raw` | 799 million | Large | Education text as reported |
| `individual_user_skills` | 11.76 billion | Large | Skills per user, reported or predicted |

### Company, Lookup, and Miscellaneous Tables

Path prefix: `/kellogg/data/revelio/Oct192026/revelio/`

`company_mapping` has 7 Parquet parts and `sentiment_individual_reviews` has 9. Every other table in this folder is a single `part-000000.parquet` file.

| Table | Approximate Rows | Scale | Description |
|---|---|---|---|
| `company_mapping` | 33.8 million | Small | Company identifiers (`rcid`, `gvkey`, `cik`, `isin`, `ticker`), headquarters, and industry |
| `individual_role_lookup_v2`, `individual_role_lookup_v3` | 1,500; 17,001 | Small | Role taxonomy for position tables (version 2 and version 3) |
| `postings_role_lookup_v2`, `postings_role_lookup_v3` | 1,501; 17,001 | Small | Role taxonomy for job postings |
| `individual_user_skill_lookup` | 31,288 | Small | Skill taxonomy, from `skill_k15` to `skill_k35000` |
| `layoffs` | 63,695 | Small | Layoff events by company and location |
| `months` | 2,260 | Small | Month and next-month calendar |
| `regions` | 380 | Small | Region and country pairs |
| `school_mapping` | 303,345 | Small | School identifiers and cleaned names |
| `sentiment_individual_reviews` | 44.6 million | Large | Review-level ratings and text |
| `sentiment_role_lookup` | 16,191 | Small | Role taxonomy for sentiment data |
| `sentiment_scores` | 9,830 | Small | Company-level sentiment scores |

(revelio-wrds-only)=
### WRDS-Only Tables

These two `revelio` library tables are **not** stored on KLC. Query them on WRDS.

| Table | Approximate Rows | Notes |
|---|---|---|
| `postings_cosmos_raw` | 2.92 billion | Combined posting text; on KLC, use the 10 `postings_cosmos_raw_p0` to `p9` tables |
| `workforce_dynamics_geo` | 7.24 billion | Monthly headcount, inflow, and outflow by company, geography, and role |

<!-- TODO(KRS): row counts are approximate, taken from a WRDS table listing on 2026-09-30; update after verifying on KLC -->

(revelio-identifiers)=
## Key Identifiers and Joins

| Identifier | Used In | Joins To |
|---|---|---|
| `user_id` | `individual_*` tables | Other `individual_*` tables |
| `position_id` | `individual_positions`, `individual_positions_raw` | One row per position in each table |
| `rcid` | `company_mapping`, positions, postings, layoffs, sentiment tables | Revelio company ID; `company_mapping` has the company name and external identifiers |
| `ultimate_parent_rcid` | positions, postings, layoffs | Parent-level company analysis |
| `role_k17000_v3`, `role_k1500_v2` | positions, postings | `individual_role_lookup_v3` or `postings_role_lookup_v3` (and `_v2` equivalents) for coarser role groups |
| `skill_k35000` | `individual_user_skills` | `individual_user_skill_lookup` |
| `rsid` | `individual_user_education` | `school_mapping` |
| `job_id` | `postings_cosmos`, `postings_cosmos_raw_p*` | Posting attributes to posting text |

:::{warning}
The column types in the table reference below are the WRDS types. DuckDB infers its own types from the Parquet files, so a column such as `NUMERIC(19, 0)` may arrive as `DECIMAL`, and `job_id` is `BIGINT` in `postings_cosmos` but `NUMERIC(32, 0)` in the text tables. Run `DESCRIBE` on a view before you join, and cast both sides of a join key to the same type.
:::

<!-- TODO(KRS): confirm the DuckDB column types for each table with DESCRIBE on KLC and update the warning above with specifics -->

## Table Reference

Column definitions come from the WRDS `revelio` library. Select a table to expand its columns.

::::{dropdown} Company Mapping (`company_mapping`)

| Column | WRDS Type | Description |
|---|---|---|
| `rcid` | NUMERIC(12, 0) | Revelio Labs Company ID |
| `company` | VARCHAR(400) | Company name |
| `factset_entity_id` | VARCHAR(8) | FactSet company ID |
| `year_founded` | VARCHAR(4) | Year founded |
| `ticker` | VARCHAR(20) | Ticker |
| `exchange_name` | VARCHAR(50) | Stock exchange |
| `sedol` | VARCHAR(7) | SEDOL |
| `isin` | VARCHAR(12) | ISIN |
| `cusip` | VARCHAR(9) | CUSIP |
| `url` | VARCHAR(400) | Website URL |
| `naics_code` | VARCHAR(6) | NAICS industry code |
| `cik` | VARCHAR(10) | CIK |
| `lei` | VARCHAR(20) | LEI |
| `linkedin_url` | VARCHAR(400) | Company LinkedIn URL |
| `child_rcid` | NUMERIC(12, 0) | Largest subsidiary RCID |
| `child_company` | VARCHAR(400) | Largest subsidiary Name |
| `child_linkedin_url` | VARCHAR(400) | LinkedIn URL of largest subsidiary |
| `ultimate_parent_rcid` | NUMERIC(12, 0) | Ultimate parent company RCID |
| `ultimate_parent_company_name` | VARCHAR(400) | Ultimate parent company name |
| `gvkey` | VARCHAR(6) | Compustat Global Company Key |
| `ein` | DOUBLE PRECISION | Employer Identification Number |
| `hq_street_address` | VARCHAR(40) | Headquarters street address |
| `hq_zip_code` | VARCHAR(25) | Headquarters ZIP code |
| `hq_city` | VARCHAR(70) | Headquarters city |
| `hq_metro_area` | VARCHAR(70) | Headquarters metro area |
| `hq_state` | VARCHAR(50) | Headquarters state |
| `hq_country` | VARCHAR(50) | Headquarters country |
| `hq_region` | VARCHAR(35) | Headquarters region |
| `rics_k50` | VARCHAR(40) | Revelio Industry Classification K=50 |
| `rics_k200` | VARCHAR(60) | Revelio Industry Classification K=200 |
| `rics_k400` | VARCHAR(60) | Revelio Industry Classification K=400 |
| `phone_number` | VARCHAR(25) | Phone number |
| `slogan` | VARCHAR(370) | Slogan |
| `description` | VARCHAR(10000) | Description |

::::

::::{dropdown} Individual Positions (`individual_positions`)

| Column | WRDS Type | Description |
|---|---|---|
| `user_id` | NUMERIC(19, 0) | User ID |
| `position_id` | NUMERIC(20, 0) | Position ID |
| `region` | VARCHAR(33) | Region |
| `country` | VARCHAR(40) | Country |
| `state` | VARCHAR(53) | State |
| `metro_area` | VARCHAR(53) | Metropolitan area |
| `msa` | VARCHAR(100) | Metropolitan Statistical Area |
| `city` | VARCHAR(100) | City |
| `startdate` | DATE | Position start date |
| `enddate` | DATE | Position end date |
| `role_k1500_v2` | VARCHAR(39) | Role Category k=1500 Version 2 |
| `role_k17000_v3` | VARCHAR(50) | Role Category k=17000 Version 3 |
| `remote_suitability` | DOUBLE PRECISION | Remote Suitability Proportion |
| `weight` | DOUBLE PRECISION | Individual sample weight |
| `start_salary` | NUMERIC(19, 2) | Salary at startdate |
| `end_salary` | NUMERIC(19, 2) | Salary at enddate |
| `seniority` | SMALLINT | Seniority level |
| `salary` | NUMERIC(19, 2) | Predicted salary |
| `position_number` | SMALLINT | Position Number |
| `rcid` | NUMERIC(12, 0) | Revelio Labs Company ID |
| `ultimate_parent_rcid` | NUMERIC(12, 0) | Ultimate parent company RCID |
| `onet_code` | VARCHAR(10) | ONET Occupation Code |
| `total_compensation` | NUMERIC(19, 2) | Total Compensation |
| `additional_compensation` | NUMERIC(19, 2) | Additional Compensation |

::::

::::{dropdown} Individual User (`individual_user`)

| Column | WRDS Type | Description |
|---|---|---|
| `user_id` | NUMERIC(19, 0) | Revelio Labs user ID |
| `fullname` | VARCHAR(104) | Full name |
| `f_prob` | DOUBLE PRECISION | Female Probability |
| `m_prob` | DOUBLE PRECISION | Male Probability |
| `white_prob` | DOUBLE PRECISION | Non-Hispanic White Probability |
| `black_prob` | DOUBLE PRECISION | Black or African American Probability |
| `api_prob` | DOUBLE PRECISION | Asian/Pacific Islander Probability |
| `hispanic_prob` | DOUBLE PRECISION | Hispanic or Latino Probability |
| `native_prob` | DOUBLE PRECISION | American Indian or Alaskan Native Probability |
| `multiple_prob` | DOUBLE PRECISION | Multiracial Probability |
| `prestige` | DOUBLE PRECISION | Prestige |
| `highest_degree` | VARCHAR(11) | Highest level of education |
| `sex_predicted` | VARCHAR(1) | Predicted Sex |
| `ethnicity_predicted` | VARCHAR(8) | Predicted Ethnicity |
| `profile_linkedin_url` | VARCHAR(220) | Profile Linkedin URL |
| `user_location` | VARCHAR(68) | User location |
| `user_country` | VARCHAR(40) | User country |
| `updated_dt` | DATE | Date profile was last refreshed |
| `numconnections` | INTEGER | Number of Connections |

::::

::::{dropdown} Individual User Education (`individual_user_education`)

| Column | WRDS Type | Description |
|---|---|---|
| `user_id` | NUMERIC(19, 0) | Revelio Labs User ID |
| `university_name` | VARCHAR(256) | School Name (mapped) |
| `rsid` | DOUBLE PRECISION | Revelio School ID |
| `education_number` | DOUBLE PRECISION | Education Number |
| `startdate` | DATE | Start date |
| `enddate` | DATE | End date |
| `degree` | VARCHAR(11) | Degree title (mapped) |
| `field` | VARCHAR(22) | Degree field (mapped) |
| `university_country` | VARCHAR(22) | School Country |
| `university_location` | VARCHAR(85) | School Location |

::::

::::{dropdown} Individual User Skills (`individual_user_skills`)

| Column | WRDS Type | Description |
|---|---|---|
| `user_id` | NUMERIC(19, 0) | Revelio Labs User ID |
| `skill_raw` | VARCHAR(64) | Skill (raw) |
| `skill_translated` | VARCHAR(64) | Skill (translated) |
| `first_reported` | DATE | Date skill was first reported |
| `skill_source` | VARCHAR(1) | Skill Source (p=Predicted, r=Reported) |
| `skill_k35000` | VARCHAR(85) | Skill category k=35000 (mapped) |

::::

::::{dropdown} Job Postings (`postings_cosmos`)

| Column | WRDS Type | Description |
|---|---|---|
| `job_id` | BIGINT | Posting key |
| `rcid` | INTEGER | Revelio Company ID |
| `company` | TEXT | Company name |
| `role_k1500_v2` | TEXT | Role category k=1500 Version 2 |
| `role_k17000_v3` | TEXT | Role category k=17000 Version 3 |
| `onet_code` | TEXT | O*NET Code |
| `country` | TEXT | Country |
| `state` | TEXT | State |
| `metro_area` | TEXT | Metropolitan Area |
| `seniority` | SMALLINT | Seniority |
| `salary` | DOUBLE PRECISION | Salary |
| `salary_min` | DOUBLE PRECISION | Salary Minimum |
| `salary_max` | DOUBLE PRECISION | Salary Maximum |
| `salary_predicted` | BOOLEAN | Salary Predicted Flag |
| `post_date` | DATE | Posting date |
| `remove_date` | DATE | Removal date |
| `ultimate_parent_rcid` | INTEGER | Ultimate parent RCID |
| `ultimate_parent_company_name` | TEXT | Ultimate parent company name |
| `remote_type` | TEXT | Remote work type |
| `expected_hires` | DOUBLE PRECISION | Expected number of hires |
| `source_company_sites` | BOOLEAN | Source Flag: Company websites |
| `source_linkedin` | BOOLEAN | Source Flag: LinkedIn |
| `source_indeed` | BOOLEAN | Source Flag: Indeed |
| `source_zhaopin` | BOOLEAN | Source Flag: Zhaopin |
| `source_51job` | BOOLEAN | Source Flag: 51job |
| `source_liepin` | BOOLEAN | Source Flag: Liepin |
| `source_other_aggregators` | BOOLEAN | Source Flag: Other aggregators |
| `source_staffingfirms` | BOOLEAN | Source Flag: Staffing firms |
| `source_regional_aggregators` | BOOLEAN | Source Flag: Regional aggregators |

::::

::::{dropdown} Job Posting Text (`postings_cosmos_raw_p0` to `p9`)

| Column | WRDS Type | Description |
|---|---|---|
| `job_id` | NUMERIC(32, 0) |  |
| `title_raw` | TEXT |  |
| `jobtitle_translated` | TEXT |  |
| `location_raw` | TEXT |  |
| `description` | TEXT |  |

::::

::::{dropdown} Layoffs (`layoffs`)

| Column | WRDS Type | Description |
|---|---|---|
| `company_raw` | VARCHAR(500) |  |
| `rcid` | NUMERIC(12, 0) | Revelio Labs Company ID |
| `company` | VARCHAR(100) | Company name |
| `state_raw` | VARCHAR(50) |  |
| `city_raw` | VARCHAR(500) |  |
| `msa_raw` | VARCHAR(60) |  |
| `county_or_region_raw` | VARCHAR(300) |  |
| `state` | VARCHAR(53) | State |
| `city` | VARCHAR(100) | City |
| `metro_area` | VARCHAR(50) |  |
| `notice_date` | DATE |  |
| `layoff_date` | DATE | Layoff date |
| `layoff_start_date` | DATE |  |
| `layoff_end_date` | DATE |  |
| `layoff_type` | VARCHAR(20) |  |
| `num_employees` | INTEGER | Number of employees |
| `num_employees_temporary` | INTEGER |  |
| `num_employees_furlough` | INTEGER |  |
| `ultimate_parent_rcid` | NUMERIC(12, 0) | Ultimate parent company RCID |
| `ultimate_parent_company_name` | VARCHAR(100) | Ultimate parent company name |

::::

::::{dropdown} School Mapping (`school_mapping`)

| Column | WRDS Type | Description |
|---|---|---|
| `rsid` | INTEGER | Revelio School ID |
| `school_name` | VARCHAR(500) | School Name |
| `school_cleaned` | VARCHAR(500) | School Name Cleaned |
| `whed_id` | VARCHAR(24) | WHED ID |
| `whed_url` | VARCHAR(100) | WHED URL |
| `factset_entity_id` | VARCHAR(8) | FactSet Entity ID |
| `website` | VARCHAR(1000) | Website |
| `region` | VARCHAR(33) | Region |
| `country` | VARCHAR(50) | Country |
| `state` | VARCHAR(50) | State |
| `city` | VARCHAR(50) | City |
| `metro_area` | VARCHAR(53) | Metro Area |
| `corresponding_rcid` | NUMERIC(12, 0) | Corresponding Company RCID |
| `corresponding_company_name` | VARCHAR(500) | Corresponding Company Name |
| `ultimate_parent_rsid` | INTEGER | Ultimate Parent School ID |
| `ultimate_parent_school_name` | VARCHAR(500) | Ultimate Parent School Name |

::::

::::{dropdown} Sentiment Scores (`sentiment_scores`)

| Column | WRDS Type | Description |
|---|---|---|
| `company` | VARCHAR(62) | Company name |
| `management_sentiment` | DOUBLE PRECISION | Management sentiment score |
| `innovative_technology_sentiment` | DOUBLE PRECISION | Innovative technology sentiment score |
| `work_life_balance_sentiment` | DOUBLE PRECISION | Work-life balance sentiment score |
| `mentorship_sentiment` | DOUBLE PRECISION | Mentorship sentiment score |
| `career_advancement_sentiment` | DOUBLE PRECISION | Career advancement sentiment score |
| `div_and_inclusion_sentiment` | DOUBLE PRECISION | Diversity and inclusion sentiment score |
| `coworkers_sentiment` | DOUBLE PRECISION | Coworkers sentiment score |
| `compensation_sentiment` | DOUBLE PRECISION | Compensation sentiment score |
| `culture_sentiment` | DOUBLE PRECISION | Culture sentiment score |
| `co_and_division_size_sentiment` | DOUBLE PRECISION | Company and division size sentiment score |
| `perks_and_benefits_sentiment` | DOUBLE PRECISION | Perks and benefits sentiment score |
| `onboarding_sentiment` | DOUBLE PRECISION | Onboarding sentiment score |
| `remote_work_sentiment` | DOUBLE PRECISION | Remote work sentiment score |
| `num_reviews` | INTEGER | Number of reviews factored into the scores |
| `rcid` | NUMERIC(12, 0) | Revelio Labs Company ID |

::::

::::{dropdown} Sentiment Reviews (`sentiment_individual_reviews`)

| Column | WRDS Type | Description |
|---|---|---|
| `rcid` | NUMERIC(12, 0) | Revelio Labs Company ID |
| `company_id` | INTEGER | Glassdoor Company ID |
| `company` | VARCHAR(100) | Company name |
| `review_id` | INTEGER | Review ID |
| `review_language_id` | VARCHAR(3) | Language identifier |
| `location_raw` | VARCHAR(50) | Location (raw) |
| `country` | VARCHAR(14) | Country |
| `state` | VARCHAR(26) | State |
| `metro_area` | VARCHAR(53) | Metropolitan area |
| `job_title_raw` | VARCHAR(200) | Position title (raw) |
| `role_k17000` | VARCHAR(50) | Role Category k=17000 |
| `seniority` | SMALLINT | Seniority |
| `review_iscovid19` | VARCHAR(5) | Covid-19 mentioned |
| `reviewer_employment_status` | VARCHAR(11) | Employment type |
| `reviewer_job_ending_year` | DOUBLE PRECISION | Final year of employment |
| `reviewer_length_of_employment` | DOUBLE PRECISION | Years worked at company |
| `reviewer_current_job` | VARCHAR(5) | Current employee |
| `rating_overall` | DOUBLE PRECISION | Overall rating |
| `rating_business_outlook` | VARCHAR(8) | Business outlook rating |
| `rating_career_opportunities` | DOUBLE PRECISION | Career opportunities rating |
| `rating_ceo` | VARCHAR(10) | CEO approval |
| `rating_compensation_and_benefits` | DOUBLE PRECISION | Compensation and benefits rating |
| `rating_culture_and_values` | DOUBLE PRECISION | Culture and values rating |
| `rating_diversity_and_inclusion` | DOUBLE PRECISION | Diversity and inclusion rating |
| `rating_recommend_to_friend` | VARCHAR(8) | Recommend to a friend sentiment |
| `rating_senior_leadership` | DOUBLE PRECISION | Senior management rating |
| `rating_work_life_balance` | DOUBLE PRECISION | Work-life balance rating |
| `review_summary` | VARCHAR(200) | Review Title |
| `review_advice` | VARCHAR(10000) | Reviewer’s advice to management |
| `review_pros` | VARCHAR(10000) | Reviewer’s positive comments |
| `review_cons` | VARCHAR(10000) | Reviewer’s negative comments |
| `review_count_helpful` | SMALLINT | Helpful Count |
| `review_count_not_helpful` | SMALLINT | Unhelpful Count |
| `ultimate_parent_rcid` | NUMERIC(12, 0) | Ultimate parent company RCID |
| `ultimate_parent_company_name` | VARCHAR(100) | Ultimate parent company name |
| `onet_code` | VARCHAR(10) | ONET Occupation Code |
| `review_date` | DATE | Review Posting date |
| `review_time` | TIME | Review Posting time |

::::

## Related Documentation

- [Revelio Labs WRDS Example](/services/kellogg-data-hosting/wrds/examples/revelio-example): pull position spells for one firm through WRDS
- [Datasets on KLC](/services/klc/klc-datasets): other datasets stored under `/kellogg/data/`
- [KLC Node Resources](/services/klc-node-resources): live CPU and RAM availability
- [When to Use KLC Reserve](/services/klc-reserve/when-to-use): choose a Reserve job when a full table must be loaded into memory
- [Submitting SLURM Jobs](/services/klc-reserve/slurm-jobs): batch job reference for KLC Reserve
- [High-Memory Jobs](/services/klc-reserve/highmem-jobs): Reserve jobs that need more than 128 GB
- [DuckDB Documentation](https://duckdb.org/docs/): configuration and SQL reference
