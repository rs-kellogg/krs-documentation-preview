# PATSTAT

## At a Glance

| | |
|---|---|
| **Provider** | [European Patent Office (EPO)](https://www.epo.org/searching-for-patents/business/patstat.html) |
| **Coverage** | Through January 1, 2024 |
| **Geographic scope** | Global |
| **Update frequency** | 2023 Autumn snapshot (delivered 2023-11-22) <!-- TODO(KRS): confirm whether newer PATSTAT editions will be loaded --> |
| **Access platforms** | KLC, AWS Athena |
| **Eligible users** | TBD <!-- TODO(KRS): confirm eligible users --> |
| **Questions** | [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) |

## Description

PATSTAT is a worldwide database of patents, prepared by the European Patent Office (EPO). More information is available on the [PATSTAT website](https://www.epo.org/searching-for-patents/business/patstat.html).

## Access

PATSTAT is licensed data. Email [Kellogg Research Support](mailto:rs@kellogg.northwestern.edu) to request access.

- **KLC:** Parquet files under `/kellogg/data/PATSTAT-2023-11-22/PATSTAT/parquet/`. Each subfolder name matches an EPO table name (for example, `tls201_appln`, `tls211_pat_publn`). Query the files with DuckDB or another Parquet-aware tool. See [How to Access KLC](../../klc/user-guide/klc-accessing).
- **Athena:** Pre-registered SQL tables in workgroup `patstat` and database `patstat`. See the [Kellogg Data Hosting — Athena platform](../../kellogg-data-hosting/athena/athena).

## Choosing Between DuckDB on KLC and Athena

PATSTAT is available on both KLC (as Parquet files queryable with DuckDB) and Athena (as pre-registered SQL tables). Table and column names use lowercase EPO identifiers on both platforms, so queries are closer to copy-paste portable than datasets where KLC Parquet uses quoted names with spaces.

| | DuckDB on KLC | Athena |
|---|---|---|
| **Setup required** | [KLC account](../../klc/user-guide/klc-accessing) | Athena database access; optional [SSO setup for ODBC](../../kellogg-data-hosting/athena/athena) |
| **Where compute runs** | KLC cluster | AWS (serverless) |
| **Cost / quota** | KLC compute limits; see the [24-core login node policy](../../klc-reserve/when-to-use) | [2 TB of data scanned per day](query-limits-and-reducing-data-scanned) |
| **Typical result size** | Large extracts and full-table scans | Small filtered extracts |
| **Downstream workflow** | Python, R, or Stata on KLC; write derived files to the file system | Download CSV from the AWS Console, or query via ODBC from KLC scripts |

**Use Athena when you want to:**

- Explore table schemas and run ad-hoc SQL without loading files
- Pull a small, filtered extract and download results to your laptop
- Work from the AWS Console with no KLC session

**Use DuckDB on KLC when you want to:**

- Scan large portions of a table or join many columns
- Iterate repeatedly on the same local Parquet files
- Write derived Parquet or other outputs alongside the rest of a KLC pipeline

```{note}
Queries are not fully copy-paste portable between the two platforms. DuckDB accepts `GROUP BY ALL` and `read_parquet()`; Athena does not. Function names also differ (for example, `REGEXP_EXTRACT` in DuckDB versus `regexp_extract` in Athena).
```

```{warning}
The DuckDB examples set `PRAGMA memory_limit='128GB'` for large scans. Run those queries in a [KLC Reserve](../../klc-reserve/when-to-use) batch job, not on a login node. Use Athena for small, filtered extracts when you do not need a full-table scan on KLC.
```

```{tip}
Before running an Athena query, right-click a table in the Query editor and choose **Generate table DDL** to confirm table and column names. Filter on indexed or partition columns whenever possible to stay under the daily scan limit.
```

## Data Coverage & Key Identifiers

| Attribute | Value |
|---|---|
| **Time period** | Through January 1, 2024 |
| **Geographic coverage** | Global |
| **Unit of observation** | Patent application (`tls201_appln`) |
| **Primary identifier** | `appln_id` |
| **Commonly linked via** | `appln_id`, `person_id`, `pat_publn_id`, `docdb_family_id` |
| **Key variables** | Filing authority and year, publication date, IPC/CPC classifications, applicants and inventors, citations, legal events |

## Tables on KLC

The hosted snapshot includes these EPO tables as Parquet subfolders under `/kellogg/data/PATSTAT-2023-11-22/PATSTAT/parquet/`:

- `tls201_appln`, `tls202_appln_title`, `tls203_appln_abstr`, `tls204_appln_prior`, `tls205_tech_rel`
- `tls206_person`, `tls207_pers_appln`, `tls209_appln_ipc`, `tls210_appln_n_cls`, `tls211_pat_publn`
- `tls212_citation`, `tls214_npl_publn`, `tls215_citn_categ`, `tls216_appln_contn`, `tls222_appln_jp_class`
- `tls224_appln_cpc`, `tls225_docdb_fam_cpc`, `tls226_person_orig`, `tls227_pers_publn`, `tls228_docdb_fam_citn`
- `tls229_appln_nace2`, `tls230_appln_techn_field`, `tls231_inpadoc_legal_event`
- `tls801_country`, `tls803_legal_event_code`, `tls901_techn_field_ipc`, `tls902_ipc_nace2`, `tls904_nuts`

The same tables are registered in the Athena `patstat` database.

:::{dropdown} Register all tables in DuckDB

```python
import duckdb

base = "/kellogg/data/PATSTAT-2023-11-22/PATSTAT/parquet"
tables = [
    "tls201_appln", "tls202_appln_title", "tls203_appln_abstr", "tls204_appln_prior",
    "tls205_tech_rel", "tls206_person", "tls207_pers_appln", "tls209_appln_ipc",
    "tls210_appln_n_cls", "tls211_pat_publn", "tls212_citation", "tls214_npl_publn",
    "tls215_citn_categ", "tls216_appln_contn", "tls222_appln_jp_class", "tls224_appln_cpc",
    "tls225_docdb_fam_cpc", "tls226_person_orig", "tls227_pers_publn", "tls228_docdb_fam_citn",
    "tls229_appln_nace2", "tls230_appln_techn_field", "tls231_inpadoc_legal_event",
    "tls801_country", "tls803_legal_event_code", "tls901_techn_field_ipc",
    "tls902_ipc_nace2", "tls904_nuts",
]

con = duckdb.connect()
con.execute("PRAGMA threads=8")
con.execute("PRAGMA memory_limit='128GB'")

for table_name in tables:
    con.execute(
        f"CREATE OR REPLACE VIEW {table_name} AS "
        f"SELECT * FROM read_parquet('{base}/{table_name}/*.parquet')"
    )
```

:::

## Example Queries

Each example below registers only the tables it needs. Join paths follow EPO table documentation: `tls211_pat_publn.appln_id` links to `tls201_appln.appln_id`; `tls207_pers_appln` links people to applications via `appln_id` and `person_id`.

### Applications by Filing Year and Authority

::::{tab-set}

:::{tab-item} DuckDB on KLC

```python
import duckdb

con = duckdb.connect()
con.execute("PRAGMA threads=8")
con.execute("PRAGMA memory_limit='128GB'")

base = "/kellogg/data/PATSTAT-2023-11-22/PATSTAT/parquet"

def register(name):
    con.execute(
        f"CREATE OR REPLACE VIEW {name} AS "
        f"SELECT * FROM read_parquet('{base}/{name}/*.parquet')"
    )

register("tls201_appln")

df = con.execute("""
    SELECT
        appln_auth,
        appln_filing_year,
        COUNT(*) AS applications
    FROM tls201_appln
    WHERE appln_filing_year BETWEEN 2015 AND 2023
    GROUP BY ALL
    ORDER BY appln_filing_year, applications DESC
""").fetchdf()
print(df)
```

:::

:::{tab-item} Athena SQL

In the Athena Query editor, select workgroup `patstat` and database `patstat`.

```sql
SELECT
    appln_auth,
    appln_filing_year,
    COUNT(*) AS applications
FROM tls201_appln
WHERE appln_filing_year BETWEEN 2015 AND 2023
GROUP BY appln_auth, appln_filing_year
ORDER BY appln_filing_year, applications DESC;
```

:::

::::

### First Publication per Application

::::{tab-set}

:::{tab-item} DuckDB on KLC

```python
import duckdb

con = duckdb.connect()
con.execute("PRAGMA threads=8")
con.execute("PRAGMA memory_limit='128GB'")

base = "/kellogg/data/PATSTAT-2023-11-22/PATSTAT/parquet"

def register(name):
    con.execute(
        f"CREATE OR REPLACE VIEW {name} AS "
        f"SELECT * FROM read_parquet('{base}/{name}/*.parquet')"
    )

register("tls201_appln")
register("tls211_pat_publn")

df = con.execute("""
    WITH first_pub AS (
        SELECT
            a.appln_id,
            MIN(p.publn_date) AS first_pub_date
        FROM tls201_appln a
        JOIN tls211_pat_publn p USING (appln_id)
        WHERE p.publn_date IS NOT NULL
        GROUP BY a.appln_id
    )
    SELECT *
    FROM first_pub
    ORDER BY first_pub_date
    LIMIT 100
""").fetchdf()
print(df)
```

:::

:::{tab-item} Athena SQL

In the Athena Query editor, select workgroup `patstat` and database `patstat`.

```sql
WITH first_pub AS (
    SELECT
        a.appln_id,
        MIN(p.publn_date) AS first_pub_date
    FROM tls201_appln a
    JOIN tls211_pat_publn p ON a.appln_id = p.appln_id
    WHERE p.publn_date IS NOT NULL
    GROUP BY a.appln_id
)
SELECT *
FROM first_pub
ORDER BY first_pub_date
LIMIT 100;
```

:::

::::

### Top IPC Sections for a Given Year

::::{tab-set}

:::{tab-item} DuckDB on KLC

```python
import duckdb

con = duckdb.connect()
con.execute("PRAGMA threads=8")
con.execute("PRAGMA memory_limit='128GB'")

base = "/kellogg/data/PATSTAT-2023-11-22/PATSTAT/parquet"

def register(name):
    con.execute(
        f"CREATE OR REPLACE VIEW {name} AS "
        f"SELECT * FROM read_parquet('{base}/{name}/*.parquet')"
    )

register("tls201_appln")
register("tls209_appln_ipc")

df = con.execute("""
    SELECT
        SUBSTR(i.ipc_class_symbol, 1, 1) AS ipc_section,
        COUNT(DISTINCT i.appln_id) AS applns
    FROM tls209_appln_ipc i
    JOIN tls201_appln a USING (appln_id)
    WHERE a.appln_filing_year = 2020
      AND i.ipc_class_level = 'A'
    GROUP BY ipc_section
    ORDER BY applns DESC
""").fetchdf()
print(df)
```

:::

:::{tab-item} Athena SQL

In the Athena Query editor, select workgroup `patstat` and database `patstat`.

```sql
SELECT
    substr(i.ipc_class_symbol, 1, 1) AS ipc_section,
    COUNT(DISTINCT i.appln_id) AS applns
FROM tls209_appln_ipc i
JOIN tls201_appln a ON i.appln_id = a.appln_id
WHERE a.appln_filing_year = 2020
  AND i.ipc_class_level = 'A'
GROUP BY 1
ORDER BY applns DESC;
```

:::

::::

### CPC Heatmap: Top CPC Main Groups by Authority and Year

::::{tab-set}

:::{tab-item} DuckDB on KLC

```python
import duckdb

con = duckdb.connect()
con.execute("PRAGMA threads=8")
con.execute("PRAGMA memory_limit='128GB'")

base = "/kellogg/data/PATSTAT-2023-11-22/PATSTAT/parquet"

def register(name):
    con.execute(
        f"CREATE OR REPLACE VIEW {name} AS "
        f"SELECT * FROM read_parquet('{base}/{name}/*.parquet')"
    )

register("tls201_appln")
register("tls224_appln_cpc")

df = con.execute("""
    SELECT
        a.appln_auth,
        a.appln_filing_year,
        REGEXP_EXTRACT(c.cpc_class_symbol, '^[A-HY]\\d+\\D\\d+/?\\d*') AS cpc_main_group,
        COUNT(DISTINCT a.appln_id) AS applns
    FROM tls224_appln_cpc c
    JOIN tls201_appln a USING (appln_id)
    WHERE a.appln_filing_year BETWEEN 2019 AND 2023
    GROUP BY ALL
    HAVING COUNT(DISTINCT a.appln_id) >= 100
    ORDER BY appln_filing_year DESC, applns DESC
    LIMIT 200
""").fetchdf()
print(df)
```

:::

:::{tab-item} Athena SQL

In the Athena Query editor, select workgroup `patstat` and database `patstat`.

```sql
SELECT
    a.appln_auth,
    a.appln_filing_year,
    regexp_extract(c.cpc_class_symbol, '^[A-HY]\d+\D\d+/?\d*') AS cpc_main_group,
    COUNT(DISTINCT a.appln_id) AS applns
FROM tls224_appln_cpc c
JOIN tls201_appln a ON c.appln_id = a.appln_id
WHERE a.appln_filing_year BETWEEN 2019 AND 2023
GROUP BY 1, 2, 3
HAVING COUNT(DISTINCT a.appln_id) >= 100
ORDER BY appln_filing_year DESC, applns DESC
LIMIT 200;
```

:::

::::

### Applicant Country Roll-Up

::::{tab-set}

:::{tab-item} DuckDB on KLC

```python
import duckdb

con = duckdb.connect()
con.execute("PRAGMA threads=8")
con.execute("PRAGMA memory_limit='128GB'")

base = "/kellogg/data/PATSTAT-2023-11-22/PATSTAT/parquet"

def register(name):
    con.execute(
        f"CREATE OR REPLACE VIEW {name} AS "
        f"SELECT * FROM read_parquet('{base}/{name}/*.parquet')"
    )

register("tls201_appln")
register("tls207_pers_appln")
register("tls206_person")

df = con.execute("""
    WITH applicants AS (
        SELECT pa.appln_id, pa.person_id
        FROM tls207_pers_appln pa
        WHERE pa.applt_seq_nr > 0
    ),
    applicant_ctry AS (
        SELECT a.appln_id, p.person_ctry_code
        FROM applicants a
        JOIN tls206_person p USING (person_id)
    )
    SELECT
        person_ctry_code,
        a.appln_filing_year,
        COUNT(DISTINCT a.appln_id) AS applns
    FROM tls201_appln a
    LEFT JOIN applicant_ctry ac USING (appln_id)
    WHERE a.appln_filing_year BETWEEN 2018 AND 2023
    GROUP BY ALL
    ORDER BY appln_filing_year, applns DESC
""").fetchdf()
print(df)
```

:::

:::{tab-item} Athena SQL

In the Athena Query editor, select workgroup `patstat` and database `patstat`.

```sql
WITH applicants AS (
    SELECT pa.appln_id, pa.person_id
    FROM tls207_pers_appln pa
    WHERE pa.applt_seq_nr > 0
),
applicant_ctry AS (
    SELECT a.appln_id, p.person_ctry_code
    FROM applicants a
    JOIN tls206_person p ON a.person_id = p.person_id
)
SELECT
    person_ctry_code,
    a.appln_filing_year,
    COUNT(DISTINCT a.appln_id) AS applns
FROM tls201_appln a
LEFT JOIN applicant_ctry ac ON a.appln_id = ac.appln_id
WHERE a.appln_filing_year BETWEEN 2018 AND 2023
GROUP BY person_ctry_code, a.appln_filing_year
ORDER BY appln_filing_year, applns DESC;
```

:::

::::

## Documentation

- [PATSTAT product page (EPO)](https://www.epo.org/searching-for-patents/business/patstat.html)
- [PATSTAT data documentation (EPO)](https://www.epo.org/searching-for-patents/business/patstat/data.html)
