# Cotality (formerly CoreLogic)

## At a Glance

| | |
|---|---|
| **Provider** | Cotality (formerly CoreLogic, formerly DataQuick) |
| **Geographic scope** | US (all counties) |
| **Access platforms** | KLC, KDC |
| **Eligible users** | Northwestern faculty and doctoral students affiliated with the Guthrie Center for Real Estate Research |
| **Questions** | [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) |

## Description

Cotality (formerly CoreLogic) compiles real property data from county assessor and recorder offices, covering over 147 million properties in over 2,300 jurisdictions across the United States. Kellogg's subscription includes six distinct datasets covering property characteristics, ownership transfers, mortgages, historical assessor records, loan performance, and MLS listings.

## Access

Access to Cotality data requires direct affiliation with the Guthrie Center for Real Estate Research. Contact [Professor Efraim Benmelech](mailto:e-benmelech@kellogg.northwestern.edu), Director of the Guthrie Center, to request access.

On KLC, Cotality files are under `/kellogg/data/corelogic` in dataset-specific subfolders. On the [Kellogg Data Hosting — Athena platform](../../kellogg-data-hosting/athena/athena), each dataset is registered in a separate database. See the table below and the per-dataset sections for paths and database names.

| Dataset | On KLC | On Athena (KDC database) |
|---|---|---|
| Smart Data Platform: Owner Transfer and Mortgage | Yes | `corelogic-202604` (most current), `corelogic2` (2022–2024 snapshots) |
| Smart Data Platform: Property | Yes | `corelogic2` |
| Smart Data Platform: Historical Property | Yes | `corelogic2` |
| Tax and Deed | Yes (pipe-separated text files) | `corelogic` |
| Loan-Level Market Analytics (LLMA) | No | `llma` |
| Multiple Listing Service (MLS) | No | `corelogic-mls` |

## Choosing Between DuckDB on KLC and Athena

Most Cotality datasets are available on both KLC (as Parquet or text files queryable with DuckDB) and Athena (as pre-registered SQL tables). LLMA and MLS are available on Athena only; Tax and Deed pipe-separated files are on KLC only, though a related subset is also registered in the `corelogic` Athena database.

| | DuckDB on KLC | Athena |
|---|---|---|
| **Setup required** | [KLC account](../../klc/user-guide/klc-accessing) | Athena database access; optional [SSO setup for ODBC](accessing-via-klc) |
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
The two platforms expose the same underlying records, but column names differ. KLC Parquet files use quoted identifiers with spaces (for example, `"SITUS STATE"`). Athena tables use lowercase identifiers (for example, `situs_state`). Queries are not copy-paste portable between the two.
```

```{tip}
Before running an Athena query, right-click a table in the Query editor and choose **Generate table DDL** to confirm table and column names. Filter on partition columns whenever possible to stay under the daily scan limit.
```

---

## Datasets

The sections below are ordered from most recently updated to oldest.

### Cotality Smart Data Platform: Owner Transfer and Mortgage

| | |
|---|---|
| **Coverage** | Owner transfers through Apr 2026; mortgages through Dec 2026 (includes future-dated records) |
| **Update status** | No longer updated (one-time snapshot downloaded Apr 2026) |
| **Format** | Parquet |
| **KLC path (most current)** | `/kellogg/data/corelogic/corelogic_202604-onetime_parquet/parquet/` |
| **KLC path (2022–2024 snapshots)** | `/kellogg/data/corelogic/corelogic_202210-202407_parquet/parquet/` |
| **KDC workgroup** | `corelogic` |
| **KDC database (older snapshots)** | `corelogic2` |
| **KDC database (most current)** | `corelogic-202604` |
| **KDC tables** | `ownertransfer`, `mortgage` |

Transaction-level records for property ownership transfers and mortgage originations across all US counties. The `ownertransfer` table captures deed-level sale events including sale price, sale date, buyer/seller names, and transaction characteristics. The `mortgage` table captures mortgage originations including loan amount, interest rate, loan type, and lender information.

The most current copy is a one-time snapshot downloaded in April 2026. Earlier recurring quarterly snapshots (Oct 2022 – Jul 2024) are also available and may be useful for longitudinal or panel analyses.

#### Data Description

- [Data Dictionary](https://nuwildcat.sharepoint.com/:b:/r/sites/KSM-RSDataDocumentation/Shared%20Documents/manuals/Corelogic/CORELOGIC%20data%20exhibit.pdf?csf=1&web=1&e=8e2ome)

#### Example Queries

::::{tab-set}

:::{tab-item} DuckDB on KLC

```python
import duckdb

con = duckdb.connect()
con.execute("PRAGMA threads=8")
con.execute("PRAGMA memory_limit='128GB'")

# Most current data (one-time snapshot, April 2026)
base = "/kellogg/data/corelogic/corelogic_202604-onetime_parquet/parquet"

con.execute(f"""
    CREATE VIEW ownertransfer AS
    SELECT * FROM read_parquet('{base}/ownertransfer/*/*.parquet')
""")

# Annual sale counts and average sale price
df = con.execute("""
    SELECT
        substr("SALE DERIVED DATE", 1, 4) AS year,
        COUNT(*) AS transfers,
        AVG("SALE AMOUNT") AS avg_sale_price
    FROM ownertransfer
    WHERE "SALE DERIVED DATE" > '20020101'
    GROUP BY year
    ORDER BY year
    LIMIT 10
""").fetchdf()
print(df)
```

:::

:::{tab-item} Athena SQL

In the Athena Query editor, select workgroup `corelogic` and database `corelogic-202604`.

<!-- TODO(KRS): confirm column identifiers via Generate table DDL -->

```sql
SELECT
    substr(sale_derived_date, 1, 4) AS year,
    COUNT(*) AS transfers,
    AVG(sale_amount) AS avg_sale_price
FROM ownertransfer
WHERE sale_derived_date > '20020101'
GROUP BY 1
ORDER BY 1
LIMIT 10;
```

:::

::::

---

### Cotality Smart Data Platform: Property

| | |
|---|---|
| **Coverage** | Snapshots Oct 2022 – Jul 2024; property sale dates back to ~1902 |
| **Update status** | No longer updated (last snapshot Jul 2024) |
| **Format** | Parquet |
| **KLC path** | `/kellogg/data/corelogic/corelogic_202210-202407_parquet/parquet/property_basic/` |
| **KDC workgroup** | `corelogic` |
| **KDC database** | `corelogic2` |
| **KDC table** | `property_basic` |

Current-state property snapshots covering residential and commercial properties across all US counties. Each record represents a property at a point in time and includes assessor information, ownership, tax data, structure characteristics (bedrooms, bathrooms, square footage, year built), geocodes, and the most recent sale. Records are partitioned by archive date (quarterly from Oct 2022 through Jul 2024).

#### Example Queries

::::{tab-set}

:::{tab-item} DuckDB on KLC

```python
import duckdb

con = duckdb.connect()
con.execute("PRAGMA threads=8")
con.execute("PRAGMA memory_limit='128GB'")

con.execute("""
    CREATE VIEW property_basic AS
    SELECT * FROM read_parquet(
        '/kellogg/data/corelogic/corelogic_202210-202407_parquet/parquet/property_basic/*/*.parquet'
    )
""")

# Count properties by state in the most recent snapshot
df = con.execute("""
    SELECT "SITUS STATE", COUNT(*) AS properties
    FROM property_basic
    WHERE archive_date = 202407
    GROUP BY "SITUS STATE"
    ORDER BY properties DESC
    LIMIT 10
""").fetchdf()
print(df)
```

:::

:::{tab-item} Athena SQL

In the Athena Query editor, select workgroup `corelogic` and database `corelogic2`.

<!-- TODO(KRS): confirm column identifiers via Generate table DDL -->

```sql
SELECT
    situs_state,
    COUNT(*) AS properties
FROM property_basic
WHERE archive_date = 202407
GROUP BY situs_state
ORDER BY properties DESC
LIMIT 10;
```

:::

::::

---

### Cotality Smart Data Platform: Historical Property

| | |
|---|---|
| **Coverage** | Tax years through 2022; archive snapshots Sep 2009 – Oct 2021 |
| **Update status** | No longer updated |
| **Format** | Parquet |
| **KLC path** | `/kellogg/data/corelogic/corelogic_202210-202407_parquet/parquet/property_history/` |
| **KDC workgroup** | `corelogic` |
| **KDC database** | `corelogic2` |
| **KDC table** | `property_history` |

Year-over-year historical snapshots of property records, enabling longitudinal analysis of changes in assessed value, ownership, tax amounts, and physical characteristics. Each record represents a property in a given tax year.

#### Example Queries

::::{tab-set}

:::{tab-item} DuckDB on KLC

```python
import duckdb

con = duckdb.connect()
con.execute("PRAGMA threads=8")
con.execute("PRAGMA memory_limit='128GB'")

con.execute("""
    CREATE VIEW property_history AS
    SELECT * FROM read_parquet(
        '/kellogg/data/corelogic/corelogic_202210-202407_parquet/parquet/property_history/*/*.parquet'
    )
""")

# Average assessed value by tax year
df = con.execute("""
    SELECT "TAX YEAR", AVG("ASSESSED TOTAL VALUE") AS avg_assessed_value
    FROM property_history
    WHERE "TAX YEAR" BETWEEN 2010 AND 2022
    GROUP BY "TAX YEAR"
    ORDER BY "TAX YEAR"
""").fetchdf()
print(df)
```

:::

:::{tab-item} Athena SQL

In the Athena Query editor, select workgroup `corelogic` and database `corelogic2`.

<!-- TODO(KRS): confirm column identifiers via Generate table DDL -->

```sql
SELECT
    tax_year,
    AVG(assessed_total_value) AS avg_assessed_value
FROM property_history
WHERE tax_year BETWEEN 2010 AND 2022
GROUP BY tax_year
ORDER BY tax_year;
```

:::

::::

---

### CoreLogic Tax and Deed

| | |
|---|---|
| **Coverage** | 2015 Q2 – 2022 Q3 (quarterly snapshots); DataQuick historical 1995–2012 |
| **Update status** | No longer updated |
| **Format** | Pipe-separated text files |
| **KLC path** | `/kellogg/data/corelogic/corelogic_201504-202207/` |
| **KDC workgroup** | `corelogic` |
| **KDC database** | `corelogic` |

Tax (assessor) and deed (transaction) data for residential and commercial properties across all US counties, delivered as quarterly snapshots from April 2015 through July 2022. Each snapshot includes a Tax file and a Deed file. Variable type, length, and format information can be found in the layout files below. Example SAS and Stata code is available at `/kellogg/data/corelogic/examples`.

**DataQuick historical data:** Assessor data (all 50 states) and transaction data (34 states) from CoreLogic's predecessor DataQuick, covering January 1, 1995 through February 10, 2012, are located at `/kellogg/data/dataquick` in the original fixed-width text format.

#### Example Queries

::::{tab-set}

:::{tab-item} DuckDB on KLC

```python
import duckdb

con = duckdb.connect()

# Read a quarterly deed snapshot (pipe-separated)
df = con.execute("""
    SELECT *
    FROM read_csv(
        '/kellogg/data/corelogic/corelogic_201504-202207/20220701Deed/*',
        delim='|', header=True
    )
    LIMIT 5
""").fetchdf()
print(df)
```

:::

:::{tab-item} Athena SQL

In the Athena Query editor, select workgroup `corelogic` and database `corelogic`.

<!-- TODO(KRS): confirm table names in the corelogic Athena database -->

```sql
SELECT *
FROM <table>
LIMIT 5;
```

:::

::::

#### Documentation

- [Variable Descriptions](https://nuwildcat.sharepoint.com/:b:/s/KSM-RSDataDocumentation/EbtN028dquhNisktTJGuvCABFTJEK_A1NFqvdbbCZa-ufA?e=8USAd7)
- [Assessor Code Tables](https://nuwildcat.sharepoint.com/:x:/s/KSM-RSDataDocumentation/ETWlNWgQAJBBqV5UsYNDukABHA__gmQd5RT2-Gfi32vpSQ?e=yqKCLg)
- [Deed Code Tables](https://nuwildcat.sharepoint.com/:x:/s/KSM-RSDataDocumentation/EWmCsymfcxZOtziM9XwD3aIBiNEIye1LTgA7xjxzdvlZ5Q?e=OcBJeh)
- [Longitude Decoding Table](https://nuwildcat.sharepoint.com/:x:/s/KSM-RSDataDocumentation/EVGpBQsEFNZNrnUj1fRAhr0Bm6mrdxppbAZUENjuEXMcHA?e=0P4yn6)
- [Tax File Layout](https://nuwildcat.sharepoint.com/:x:/s/KSM-RSDataDocumentation/EY7ATqh7dJVEsH3vz0TZ6z8BwVKFEG9aEEGHJfmT2A0KjQ?e=Pwjewu)
- [Deed File Layout](https://nuwildcat.sharepoint.com/:x:/s/KSM-RSDataDocumentation/EYQt9ql9C1FJljpNCwTGKv0BkiCiMs0pogHu69R5Zoxhqw?e=M9bn5Q)

**DataQuick file layouts:**

- [History File Layout](https://nuwildcat.sharepoint.com/:x:/s/KSM-RSDataDocumentation/EexFDzL9mcdFnNC4NIG3z00B53PDRHP-UcrHiYurI8bInA?e=EgIr7B)
- [Assessor File Layout](https://nuwildcat.sharepoint.com/:x:/s/KSM-RSDataDocumentation/EcwvRy3PL5FNqW_epC2e2Q0BnJvpen9fiCnQ5sMnmDOdTw?e=IkroZ0)

---

### Cotality Loan-Level Market Analytics (LLMA)

| | |
|---|---|
| **Formerly known as** | CoreLogic Loan-Level Market Analytics (LLMA) |
| **Coverage** | 1992 - 2016 |
| **Update status** |  No longer updated |
| **KDC workgroup** | `llma` |
| **KDC database** | `llma` |

Cotality Loan-Level Market Analytics (LLMA) for primary mortgages contains detailed loan data, including origination, events, performance, forbearance and inferred modification data. The foundation data includes:

- **Loan Origination Data** — loan, property, and borrower characteristics at origination, including loan amount, interest rate, product type, LTV, occupancy, and lender information
- **Loan Performance Data** — monthly delinquency status and servicing information
- **Events Data** — loan-level events such as modifications, bankruptcy, and REO
- **Inferred Modification Data** — modification records inferred from performance data
- **Contributed Modification Data** — modification records as reported by servicers

#### Example Queries

LLMA is available on Athena only. In the Athena Query editor, select workgroup `llma` and database `llma`.

<!-- TODO(KRS): confirm table names in the llma Athena database -->

```sql
SELECT *
FROM <table>
LIMIT 5;
```

#### Data Description

- [Data Dictionary](https://nuwildcat.sharepoint.com/:b:/r/sites/KSM-RSDataDocumentation/Shared%20Documents/manuals/Corelogic/CL_LLMA_Data_Dictionary.pdf?csf=1&web=1&e=tYw4jJ)

---

### Cotality Multiple Listing Service (MLS)

| | |
|---|---|
| **Coverage** | <!-- TODO: confirm coverage dates for Kellogg's MLS data --> |
| **Update status** | <!-- TODO: confirm whether MLS data is still being updated --> |
| **KDC workgroup** | `corelogic-mls` |
| **KDC database** | `corelogic-mls` |

A multiple listing service (MLS) is an exchange where real estate brokers share information about properties they are selling. Other real estate brokers review the listings, and are compensated if they can identify a buyer for a property. Multiple listing services promote cooperation and mutual benefit for real estate brokers representing buyers and sellers. The Cotality Multiple Listing Service data contains listings from 135 real estate boards utilizing Cotality's multiple listing service software. The data was produced in TBD.
