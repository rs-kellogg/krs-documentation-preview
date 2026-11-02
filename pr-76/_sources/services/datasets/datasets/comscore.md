# Comscore

## At a Glance

| | |
|---|---|
| **Provider** | Comscore |
| **Coverage** | 2019–2020 |
| **Geographic scope** | US |
| **Update frequency** | Discontinued |
| **Access platforms** | KLC, AWS Athena |
| **Eligible users** | Northwestern faculty and doctoral students |
| **Questions** | [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) |

## Description

Historical data feeds and lookups include:

- **Desktop URL Traffic** — individual-level host, directory, and page of visited and referring sites
- **AdMetrix Traffic** — individual-level ad exposures, advertiser, and advertiser hierarchy
- **Ecommerce** — machine-level transaction data including item name, quantity purchased, and total basket cost where available

Data are suppressed for panelists identifiable as under the age of 18 at the time of measurement.

## Access

Comscore is licensed data. Email [Kellogg Research Support](mailto:rs@kellogg.northwestern.edu) to request access and to get advice about how to structure Athena queries for better performance.

- **Athena:** Pre-registered SQL tables in workgroup `comscore2` and database `comscore`. See the [Kellogg Data Hosting — Athena platform](../../kellogg-data-hosting/athena/athena).
- **KLC — Desktop URL traffic:** Hive-partitioned Parquet under `/kellogg/data/comscore/parquet/comscore_url_traffic/`. Query these files with DuckDB or another Parquet-aware tool. See [How to Access KLC](../../klc/user-guide/klc-accessing).
- **KLC — Other feeds:** AdMetrix, ecommerce, lookups, and demographics are available on Athena as registered tables. The DuckDB examples on this page cover URL traffic Parquet only.

Additional Comscore files may exist under `/kellogg/data/comscore`; contact Research Support if you need a path that is not listed here.

## Choosing Between DuckDB on KLC and Athena

Desktop URL traffic is available on KLC as Parquet and on Athena as the `comscore_url_traffic` table. Other Comscore tables in the sections below are registered in Athena.

| | DuckDB on KLC | Athena |
|---|---|---|
| **Setup required** | [KLC account](../../klc/user-guide/klc-accessing) | Athena database access; optional [KLC SSO setup](../../kellogg-data-hosting/athena/athena) |
| **Where compute runs** | KLC cluster | AWS (serverless) |
| **Cost / quota** | KLC compute limits; see the [24-core login node policy](../../klc-reserve/when-to-use) | [2 TB of data scanned per day](query-limits-and-reducing-data-scanned) |
| **Typical result size** | Large URL scans and derived Parquet on scratch | Small filtered extracts and multi-table joins |
| **Downstream workflow** | Python, R, or Stata on KLC; write derived files to the file system | Download CSV from the AWS Console, or query with Python on KLC and read the saved file in R or Stata |

::::{dropdown} When to Use Each Platform

**Use Athena when you want to:**

- Explore table schemas and run ad-hoc SQL without loading files
- Join URL traffic to `comscore_time_lookup`, demographics, AdMetrix, or ecommerce in one query
- Pull a small, filtered extract and download results to your laptop

**Use DuckDB on KLC when you want to:**

- Scan one or more URL traffic months from Parquet and aggregate before pulling data into memory
- Stage compact monthly visit counts under `/scratch/$USER/` and reuse them across panel months
- Iterate repeatedly on the same Parquet partitions without re-scanning raw events

```{note}
For URL traffic on KLC, hive partitions (`year=…`, `month=…`, `day=…`) replace a `comscore_time_lookup` join when you filter to a calendar month. Athena examples below still use the lookup table where that join is the clearest pattern.
```

```{tip}
Before running an Athena query, right-click a table in the Query editor and choose **Generate table DDL** to confirm table and column names. Filter on partition or indexed columns whenever possible to stay under the daily scan limit.
```

::::

## Data Coverage & Key Identifiers

| Attribute | Value |
|---|---|
| **Time period** | 2019–2020 |
| **Geographic coverage** | US |
| **Unit of observation** | Panelist-event |
| **Primary identifier** | `machine_id` (machine), `person_id` (person) |
| **Commonly linked via** | `machine_id`, `person_id`, `time_id` / `time_period_id` |
| **Key variables** | URL, page, ad exposure, advertiser, transaction amount, quantity, demographics |

## Tables

Expand a table name to view column definitions. Desktop URL traffic includes the KLC Parquet layout.

::::{dropdown} Desktop URL Traffic — `comscore_url_traffic`

**KLC Parquet layout.** Files are hive-partitioned under `/kellogg/data/comscore/parquet/comscore_url_traffic/` by `year`, `month`, and `day`:

```text
/kellogg/data/comscore/parquet/comscore_url_traffic/year=2019/month=1/day=1/*.parquet
```

Some months use a zero-padded directory name (`month=01`) instead of `month=1`. Resolve whichever directory exists for the month you need before calling `read_parquet()`.

| Column | Type | Description |
|---|---|---|
| `machine_id` | bigint | Unique identifier for each machine |
| `url_idc` | varchar | Unique event identifier |
| `person_id` | bigint | Unique identifier for each person |
| `ss2k` | bigint | Seconds since 2000 |
| `time_id` | int | Comscore date identifier (unique identifier for days) |
| `domain_name` | varchar | Domain name portion of URL |
| `url_host` | varchar | URL host portion of URL |
| `url_dir` | varchar | URL directory portion of URL (e.g. `/gp/product/`) |
| `url_page` | varchar | URL page portion of URL (e.g. `index.asp`) |
| `url_refer_domain` | varchar | Domain name portion of referring URL |
| `url_refer_host` | varchar | URL host portion of referring URL |
| `url_refer_dir` | varchar | URL directory portion of referring URL |
| `url_refer_page` | varchar | URL page portion of referring URL |
| `mimetype` | varchar | MIME type of URL; derived from content-type reply header |
| `http_rc` | int | Standard HTTP reply code (200, 302, 404, etc.) |
| `keywords` | varchar | Search keywords associated with the event |
| `html_title` | varchar | HTML title from the page |
| `pattern_id` | int | Comscore Client Focus Dictionary URL page mask ID |

::::

::::{dropdown} Desktop AdMetrix Ad Exposure — `comscore_admetrix`

| Column | Type | Description |
|---|---|---|
| `machine_id` | bigint | Unique identifier for each machine |
| `person_id` | bigint | Unique identifier for each person |
| `time_id` | int | Comscore date identifier (unique identifier for days) |
| `ss2k` | bigint | Seconds since 2000 |
| `adv_pattern_id` | int | Advertiser's AdMetrix Product Dictionary page mask ID |
| `pub_pattern_id` | int | Publisher's Comscore Client Focus Dictionary URL page mask ID |

::::

::::{dropdown} AdMetrix Advertiser Pattern Lookup — `comscore_admetrix_product_dictionary`

| Column | Type | Description |
|---|---|---|
| `month_id` | int | Comscore date identifier (unique identifier for months) |
| `adv_pattern_id` | int | Advertiser's AdMetrix Product Dictionary page mask ID |
| `adv_web_id` | int | Comscore AdMetrix Product Dictionary entity ID |
| `adv_web_name` | varchar | Comscore AdMetrix Product Dictionary entity name |
| `adv_level_id` | int | Comscore AdMetrix Product Dictionary level identifier |
| `adv_parent_id` | int | Comscore AdMetrix Product Dictionary parent ID |
| `adv_category` | varchar | Comscore AdMetrix Product Dictionary category name |
| `adv_subcategory` | varchar | Comscore AdMetrix Product Dictionary sub-category name |

::::

::::{dropdown} Desktop Ecommerce — `comscore_ecommerce`

| Column | Type | Description |
|---|---|---|
| `month_id` | int | Month number corresponding to Comscore time |
| `domain_name` | varchar(50) | Domain where transaction occurred |
| `machine_id` | bigint | Unique identifier for machines |
| `url_idc` | char(22) | Unique identifier for transactions |
| `time_id` | int | Comscore date identifier (unique identifier for days) |
| `event_time` | datetime | Timestamp of purchase in GMT |
| `payment_desc` | varchar(50) | Payment method used (where observable) |
| `machine_country` | varchar(2) | Country where the panelist who made the purchase is located |
| `itemName` | varchar(500) | Name of item (where observable; only available for retailers with item-level detail) |
| `productCategory` | varchar(250) | Product category name (where observable; only available for retailers with item-level detail) |
| `productSubCategory` | varchar(250) | Product sub-category name (where observable; only available for retailers with item-level detail) |
| `raw_basketTotal` | numeric(20,2) | Total spent for the transaction in USD |
| `raw_quantity` | int | Quantity of items (only available for retailers with item-level detail) |
| `raw_itemTotal` | numeric(20,2) | Total spent for specified item(s) in USD (only available for retailers with item-level detail) |

::::

::::{dropdown} Time Lookup — `comscore_time_lookup`

| Column | Type | Description |
|---|---|---|
| `time_id` | int | Comscore date identifier (unique identifier for days) |
| `week_id` | int | Comscore date identifier (unique identifier for weeks) |
| `month_id` | int | Comscore date identifier (unique identifier for months) |
| `calendar_day` | date | Calendar day associated with Comscore `time_id` |

::::

::::{dropdown} Traffic Category Map — `comscore_category_map`

| Column | Type | Description |
|---|---|---|
| `month_id` | int | Comscore date identifier (unique identifier for months) |
| `pattern_id` | int | Comscore Client Focus Dictionary URL page mask ID |
| `web_id` | int | Comscore Client Focus Dictionary entity ID |
| `web_name` | varchar(255) | Comscore Client Focus Dictionary entity name |
| `level_name` | varchar(255) | Comscore Client Focus Dictionary level name |
| `level_id` | int | Comscore Client Focus Dictionary level unique identifier |
| `parent_id` | int | Comscore Client Focus Dictionary parent ID |
| `subcategory` | varchar(255) | Comscore Media Metrix category to which entity belongs |
| `category` | varchar(255) | Parent category of the above category |
| `Magazine` | int | Comscore dictionary attribute (1 = True, 0 = False) |
| `Streaming_Video` | int | Comscore dictionary attribute (1 = True, 0 = False) |
| `Blog` | int | Comscore dictionary attribute (1 = True, 0 = False) |
| `Streaming_Audio` | int | Comscore dictionary attribute (1 = True, 0 = False) |
| `Cable_Broadcast_TV` | int | Comscore dictionary attribute (1 = True, 0 = False) |
| `Radio` | int | Comscore dictionary attribute (1 = True, 0 = False) |
| `Newspaper` | int | Comscore dictionary attribute (1 = True, 0 = False) |

::::

::::{dropdown} Browser Type Lookup — `comscore_browser_type_lookup`

| Column | Type | Description |
|---|---|---|
| `browser_type` | varchar | Numeric ID for the browser |
| `browser_name` | varchar | High-level browser name |
| `browser_name_detail` | varchar | Browser name with version |

::::

::::{dropdown} Desktop Operating System Lookup — `comscore_operating_system_lookup`

| Column | Type | Description |
|---|---|---|
| `month_id` | int | Unique identifier for the month |
| `machine_id` | bigint | Unique identifier for each machine |
| `os_version_name` | varchar | Operating system version name |

::::

::::{dropdown} Machine Demographics — `machine_demog`

| Column | Type | Description |
|---|---|---|
| `machine_id` | bigint | Unique identifier for each machine |
| `country` | string | Country where machine is located |
| `local_market` | string | Local market (Designated Market Area code; US only) |
| `computer_location` | string | Home or work (US only) |
| `age` | string | Head of household age |
| `income` | string | Household income |
| `education` | string | Head of household education |
| `child_present` | string | Child present in household |
| `hh_size` | string | Size of household |
| `time_period_id` | int | Unique identifier for the time period |

::::

::::{dropdown} Person Demographics — `person_demog`

| Column | Type | Description |
|---|---|---|
| `person_id` | bigint | Unique identifier for each person |
| `machine_id` | bigint | Unique identifier for each machine |
| `gender` | string | Gender of panelist |
| `age` | string | Age of panelist |
| `children_present` | string | Child present in household |
| `hh_income` | string | Household income |
| `hh_size` | string | Size of household |
| `ethnicity` | string | Ethnicity of panelist |
| `race` | string | Race of panelist |
| `hoh_education` | string | Head of household education level |
| `computer_location` | string | Home or work (US only) |
| `country` | string | Country where machine is located |
| `local_market` | string | Local market (Designated Market Area code; US only) |
| `time_period_id` | int | Unique identifier for the time period |

::::

::::{dropdown} Person Weights — `person_weights`

| Column | Type | Description |
|---|---|---|
| `machine_id` | bigint | Unique identifier for each machine |
| `person_id` | bigint | Unique identifier for each person |
| `time_period_id` | int | Unique identifier for weeks |
| `numeric_time_zone` | int | Time zone adjustment factor (converts event time from GMT to local) |
| `country` | string | Country where machine is located |
| `weight` | numeric | Weight assigned to the person on the machine |

::::

## Working with URL Traffic on KLC

The examples below run from a KLC main session or a [KLC Reserve](../../klc-reserve/when-to-use) batch job. They follow a practical pattern for large URL extracts: scan each raw month once, write compact visit-count Parquet to scratch, then build cohort and panel outputs from those stages instead of re-reading event-level files.

```{warning}
You can run the DuckDB examples on KLC main nodes. They set `PRAGMA memory_limit='128GB'` for large scans; follow the [24-core login node policy](../../klc-reserve/when-to-use). Use [KLC Reserve](../../klc-reserve/when-to-use) when you need dedicated cores and memory for long multi-month pipelines. Use Athena for small, filtered extracts when you do not need a full-month URL scan on KLC.
```

::::{dropdown} Connect DuckDB

```python
import os
from pathlib import Path

import duckdb

scratch = Path(f"/scratch/{os.environ['USER']}/duckdb")
temp_dir = scratch / "tmp"
temp_dir.mkdir(parents=True, exist_ok=True)

con = duckdb.connect()
con.execute("PRAGMA threads=8")
con.execute("PRAGMA memory_limit='128GB'")
con.execute(f"SET temp_directory = '{temp_dir}'")
con.execute("SET preserve_insertion_order = false")
```

::::

::::{dropdown} Read One Month (Preview)

Resolve `month=1` versus `month=01`, then aggregate domain visit counts for a single calendar month:

```python
from pathlib import Path

URL_ROOT = Path("/kellogg/data/comscore/parquet/comscore_url_traffic")


def month_parquet_glob(year: int, month: int) -> str:
    for directory in (
        URL_ROOT / f"year={year}" / f"month={month}",
        URL_ROOT / f"year={year}" / f"month={month:02d}",
    ):
        if directory.is_dir():
            return str(directory / "**" / "*.parquet")
    raise FileNotFoundError(f"No URL traffic partition for {year}-{month:02d}")


glob_path = month_parquet_glob(2020, 1)

df = con.execute(f"""
    SELECT
        domain_name,
        COUNT(*) AS events
    FROM read_parquet(
        '{glob_path}',
        hive_partitioning = true,
        union_by_name = true
    )
    WHERE domain_name IS NOT NULL
    GROUP BY domain_name
    ORDER BY events DESC
    LIMIT 20
""").fetchdf()
print(df)
```

::::

::::{dropdown} Stage Monthly Visit Counts

Project only `person_id`, `machine_id`, and `domain_name`, filter to domains your study needs, aggregate to visit counts, and write one Parquet file per month. Use an `_in_progress` directory and an `_SUCCESS` marker so a loop over many months can skip completed stages:

```python
import os
import shutil
from pathlib import Path

URL_ROOT = "/kellogg/data/comscore/parquet/comscore_url_traffic"
STAGE_ROOT = Path(f"/scratch/{os.environ['USER']}/comscore_stages")
YEAR, MONTH = 2020, 1
TRACKED_DOMAINS = ("amazon.com", "walmart.com")


def month_parquet_glob(url_root: str, year: int, month: int) -> str:
    root = Path(url_root)
    for directory in (
        root / f"year={year}" / f"month={month}",
        root / f"year={year}" / f"month={month:02d}",
    ):
        if directory.is_dir():
            return str(directory / "**" / "*.parquet")
    raise FileNotFoundError(f"No URL traffic partition for {year}-{month:02d}")


def sql_string_list(values: tuple[str, ...]) -> str:
    return ", ".join("'" + value.replace("'", "''") + "'" for value in values)


stage_dir = (
    STAGE_ROOT / "tracked_domain_counts" / f"year={YEAR}" / f"month={MONTH:02d}"
)
if (stage_dir / "_SUCCESS").is_file():
    print(f"Skipping completed stage: {stage_dir}")
else:
    in_progress = stage_dir.with_name(stage_dir.name + "_in_progress")
    shutil.rmtree(in_progress, ignore_errors=True)
    in_progress.mkdir(parents=True)

    month_glob = month_parquet_glob(URL_ROOT, YEAR, MONTH)
    output_file = in_progress / "part-00000.parquet"
    domain_list = sql_string_list(TRACKED_DOMAINS)

    con.execute(f"""
        COPY (
            SELECT
                u.person_id,
                u.machine_id,
                u.domain_name,
                COUNT(*)::UBIGINT AS n_visits
            FROM read_parquet(
                '{month_glob}',
                hive_partitioning = true,
                union_by_name = true
            ) AS u
            WHERE u.person_id IS NOT NULL
              AND u.machine_id IS NOT NULL
              AND u.domain_name IN ({domain_list})
            GROUP BY
                u.person_id,
                u.machine_id,
                u.domain_name
        )
        TO '{output_file}'
        WITH (FORMAT PARQUET, COMPRESSION ZSTD)
    """)

    in_progress.rename(stage_dir)
    (stage_dir / "_SUCCESS").write_text("ok\n")
    print(f"Wrote {stage_dir}")
```

Repeat the staging block for each month in your panel, checking `_SUCCESS` before scanning raw Parquet again.

::::

::::{dropdown} Build a Panel from Staged Files

After staging, define a person-machine cohort from the staged counts (for example, everyone who ever visited a tracked domain), then left-join each month back to that cohort so zero-visit months appear as zeros. Additional panel months should reuse the same cohort file and read only the corresponding monthly stage Parquet, not the raw URL traffic tree:

```python
from pathlib import Path

STAGE_ROOT = Path(f"/scratch/{os.environ['USER']}/comscore_stages")
OUTPUT_ROOT = STAGE_ROOT / "panel"
YEAR, MONTH = 2020, 1

stage_file = (
    STAGE_ROOT
    / "tracked_domain_counts"
    / f"year={YEAR}"
    / f"month={MONTH:02d}"
    / "part-00000.parquet"
)
cohort_dir = STAGE_ROOT / "visitor_cohort"
cohort_file = cohort_dir / "part-00000.parquet"

if not cohort_file.is_file():
    cohort_dir.mkdir(parents=True, exist_ok=True)
    con.execute(f"""
        COPY (
            SELECT DISTINCT person_id, machine_id
            FROM read_parquet('{stage_file}', union_by_name = true)
        )
        TO '{cohort_file}'
        WITH (FORMAT PARQUET, COMPRESSION ZSTD)
    """)

panel_dir = OUTPUT_ROOT / f"year={YEAR}" / f"month={MONTH:02d}"
panel_dir.mkdir(parents=True, exist_ok=True)
panel_file = panel_dir / "part-00000.parquet"

con.execute(f"""
    COPY (
        SELECT
            c.person_id,
            c.machine_id,
            {YEAR}::INTEGER AS year,
            {MONTH}::INTEGER AS month,
            COALESCE(SUM(s.n_visits), 0)::UBIGINT AS total_visits
        FROM read_parquet('{cohort_file}', union_by_name = true) AS c
        LEFT JOIN read_parquet('{stage_file}', union_by_name = true) AS s
            ON c.person_id = s.person_id
           AND c.machine_id = s.machine_id
        GROUP BY c.person_id, c.machine_id
    )
    TO '{panel_file}'
    WITH (FORMAT PARQUET, COMPRESSION ZSTD)
""")
print(f"Wrote {panel_file}")
```

::::

## Example Queries (Athena)

Run the SQL below in the Athena Query editor with workgroup `comscore2` and database `comscore`.

::::{dropdown} URL Traffic with Calendar Dates

Resolve `time_id` values to calendar dates using the time lookup table:

```sql
SELECT
    t.calendar_day,
    u.person_id,
    u.domain_name,
    u.url_host
FROM comscore_url_traffic u
JOIN comscore_time_lookup t ON u.time_id = t.time_id
WHERE t.calendar_day BETWEEN DATE '2020-01-01' AND DATE '2020-01-31'
LIMIT 100;
```

::::

::::{dropdown} URL Traffic with Demographics and Weights

Join URL traffic to person demographics and survey weights:

```sql
SELECT
    u.person_id,
    u.domain_name,
    p.gender,
    p.age,
    w.weight
FROM comscore_url_traffic u
JOIN person_demog p
    ON u.person_id = p.person_id
JOIN person_weights w
    ON u.person_id = w.person_id
   AND u.machine_id = w.machine_id
LIMIT 100;
```

::::

::::{dropdown} Ad Exposure with Advertiser Names

Look up ad exposure events with advertiser names:

```sql
SELECT
    a.person_id,
    a.time_id,
    d.adv_web_name,
    d.adv_category,
    d.adv_subcategory
FROM comscore_admetrix a
JOIN comscore_admetrix_product_dictionary d
    ON a.adv_pattern_id = d.adv_pattern_id
LIMIT 100;
```

::::

::::{dropdown} Ecommerce Spending by Domain

Summarize ecommerce spending by domain:

```sql
SELECT
    domain_name,
    COUNT(*) AS transactions,
    SUM(raw_basketTotal) AS total_spend
FROM comscore_ecommerce
GROUP BY domain_name
ORDER BY total_spend DESC
LIMIT 20;
```

::::

## Documentation

- [Desktop URL, AdMetrix, and Ecommerce schema](https://nuwildcat-my.sharepoint.com/:b:/r/personal/jpj8711_ads_northwestern_edu/Documents/Data%20Documentation/comScore/comScore%20Data%20Traffic%20Schema.pdf?csf=1&web=1&e=rsCRMJ)
- [Demographics schema](https://nuwildcat-my.sharepoint.com/:x:/r/personal/jpj8711_ads_northwestern_edu/Documents/Data%20Documentation/comScore/comScore%20Demographics%20Schema.xlsx?d=wdd59b6aaa55145a290e657e698d472c8&csf=1&web=1&e=tFYKmg)
