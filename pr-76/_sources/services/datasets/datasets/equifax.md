# Equifax Analytic Dataset

## At a Glance

| | |
|---|---|
| **Provider** | Equifax (Analytic Dataset, layout ADS 3.0) |
| **Coverage** | Monthly archives, July 2005 – present |
| **Geographic scope** | United States, including territories and military addresses |
| **Update frequency** | Quarterly |
| **Unit of observation** | One account (tradeline) held by one consumer in one monthly archive |
| **Size** | ~140–150 million rows per month; ~11 GB per month; ~2.5 TiB total |
| **Access platforms** | KLC, AWS Athena |
| **Eligible users** | Guthrie Center for Real Estate Research affiliates |
| **Questions** | [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) |

## Description

The Equifax Analytic Dataset is a monthly panel of consumer credit accounts. Since every account carries both its own history and a snapshot of its holder's credit file, it supports research on:

- **Household borrowing and repayment**: balances, payments, and delinquency by product (mortgage, auto, bankcard, student loan) over time.
- **Credit access and lending decisions**: scores and income estimates *at the time each account was opened* let you study who gets credit without reconstructing past credit files.
- **Following accounts and consumers through time**: `trade_id` and `consumer_id` link records across monthly archives.
- **Geographic variation**: ZIP code and state of the consumer's current address.

**What it doesn't have:** names or street addresses, lender identities (only industry codes), interest rates, or measured income (`pim_score` and `consumer_income_score` are Equifax model estimates, not reported income). <span style="color:red; font-weight:bold">[TO CONFIRM: whether the panel is the full Equifax population or a sample]</span>

## Access

The Equifax data is available in two places, and both hold the same data. On the Kellogg Linux Cluster (KLC), it is stored as Parquet files under `/kellogg/data/equifax/parquet` that you query with DuckDB from Python or R. In AWS Athena, it is a single SQL table that you can query in a browser console, or from KLC with `kdcutils`. Access to either requires approval from the Guthrie Center for Real Estate Research.

Which to use depends on what you are trying to do:

| If you… | Use |
|---|---|
| Want to explore the data, get a feel for its structure, or check whether the values you want to analyze are mostly missing | Athena |
| Want all the data for a given month or year | KLC files with DuckDB |
| Have a structured SQL query that scans well under 5 TB and want to run it efficiently | Athena |
| Are unsure how much your query will scan or how long it will take | Athena, carefully: test on one month first (see [Athena](#equifax-athena)) |
| Have queries that scan more than 5 TB, or run too long in Athena | KLC files with DuckDB |

(equifax-klc)=
### KLC Parquet Files

The Parquet files are at:

```
/kellogg/data/equifax/parquet/equifax/
```

They are partitioned by folder, with unpadded month numbers. Each month is split into many files, so read a folder pattern rather than individual files:

```
year=2005/ … year=2026/
  month=1/ … month=12/
    <generated-name>.parquet
```

Reading these files does not count against the Athena scan budget, so you can rerun large queries as often as you need. New months are added to these files first, before Athena is updated.

If you receive `Permission denied` when listing or reading these paths, file-system access is not yet enabled. Contact [Kellogg Research Support](mailto:rs@kellogg.northwestern.edu).

In R, the `duckdb` package compiles from source when installed with `install.packages()`, which can take an hour on KLC. Installing the prebuilt `r-duckdb` package from conda-forge (`mamba install -c conda-forge r-duckdb`) takes a minute or two.

Run these examples from a KLC session. See [How to Access KLC](../../klc/user-guide/klc-accessing) if you do not yet have an account.

::::{tab-set}

:::{tab-item} Python
:sync: python

```python
import duckdb

EQUIFAX = "/kellogg/data/equifax/parquet/equifax/year=2020/month=1/*.parquet"

df = duckdb.sql(f"""
    SELECT *
    FROM read_parquet('{EQUIFAX}', hive_partitioning = true)
    LIMIT 10
""").df()
print(df)
```

:::

:::{tab-item} R
:sync: r

```r
library(duckdb)

equifax <- "/kellogg/data/equifax/parquet/equifax/year=2020/month=1/*.parquet"

con <- dbConnect(duckdb())
df <- dbGetQuery(con, sprintf("
    SELECT *
    FROM read_parquet('%s', hive_partitioning = true)
    LIMIT 10
", equifax))
print(df)
dbDisconnect(con, shutdown = TRUE)
```

R may warn that it is *coercing nanoseconds to a lower resolution*. The dates fall on whole days, so nothing is lost and the warning can be ignored.

:::

::::

To read one month, put it in the path. To read many months, use a wildcard path (`year=*/month=*/*.parquet`) and filter in `WHERE`; DuckDB reads `year` and `month` from the folder names as integers, so filter with `year = 2020`, not `'2020'`.

```{warning}
One month is about 11 GB. Do not load full months into memory on a KLC login node. Select only the columns you need, let DuckDB stream the data, and use a [KLC Reserve](../../klc-reserve/when-to-use) batch job for large extracts.
```

(equifax-athena)=
### Athena

Both the workgroup and the database are named `equifax` in the AWS Athena console, and the table is `equifax.equifax`.

The same first look as the DuckDB example above, run in the Athena console:

```sql
SELECT *
FROM equifax.equifax
WHERE year = '2020' AND month = '1'
LIMIT 10;
```

Note the quotes: in Athena, `year` and `month` are strings.

Athena queries share a **5 TB daily scan budget** across all users of the `equifax` workgroup, including queries submitted through `kdcutils`. The whole table is about 2.75 TB, so a single query rarely exceeds the budget on its own; the limit is reached when one person runs several large queries in a day, or several people work at once. Once the budget is reached, new queries are blocked until it resets.

Athena counts **data scanned**, not rows returned. A quick look like the example above is cheap: a plain `SELECT *` with `LIMIT 10` stops after 10 rows (about 2 MB scanned in testing). But once a query aggregates, sorts, or joins, `LIMIT` no longer helps, and `SELECT *` makes Athena read all 82 columns of every month the query touches. Two things keep scans small: filtering on `year` and `month`, and naming only the columns you need.

1. **Test in the console.** Check that the fields you need exist and are populated, and run your query on one month with only the columns you need. The console shows data scanned as the query runs; multiply by the number of months to estimate the full query. For queries that link records across months, test on two months or one year instead. Runtime does not scale as neatly as scanning: joins and distinct counts slow down disproportionately as you add months.
2. **Run the full query with `kdcutils` from KLC** when you want the results saved on KLC. Save your SQL to a `.sql` file and submit it. Each run adds about 30 seconds for submitting the query and downloading results, so use the console for quick exploratory queries. See the [kdcutils video](https://kellogg-shared.s3.us-east-2.amazonaws.com/videos/kdcutils.mp4).

   ```bash
   module load kdcutils/2.0
   kdcutils athena equifax equifax sample.sql --out <output-path>
   ```

   Results arrive as several Parquet files, even for a few rows. Read the output folder as one dataset, for example `read_parquet('<output-path>/*.parquet')` in DuckDB.

:::{important}
This dataset contains sensitive consumer credit information. Do not share record-level data or derived identifying information outside your approved research project.
:::

(equifax-dictionary)=
## Schema

In Athena, the Equifax data is a single table, `equifax.equifax`, partitioned by `year` and `month`. On KLC, the same data is stored as Parquet files under `/kellogg/data/equifax/parquet/equifax/year={YYYY}/month={M}/`, with many files per month. Each row is **one account (tradeline) held by one consumer in one monthly archive**, and every month has the same 84-column schema.

Field definitions and value codes are provided in Equifax's layout files:

- [Analytic Dataset Layout ADS 3.0](LINK-TO-ADS-3.0) (describes the Athena and KLC Parquet data)
- [Analytic Dataset Layout ADS 1.1, Ver. 4](LINK-TO-ADS-1.1) (describes the older 2021 CSV files)[^notdelivered]

### Key Field Groups

::::{dropdown} Identifiers and record tracking
| Field | Type | Description | Notes |
|---|---|---|---|
| `consumer_id` | bigint | Anonymous consumer ID | |
| `trade_id` | bigint | Anonymous account ID; links an account across archives | |
| `archive_date` | bigint | Date Equifax pulled the archive | Nanoseconds[^dates] |
| `year`, `month` | varchar | Partition keys | Unpadded strings: `'2008'`, `'5'` |
| `weight` | real | 0.5 for joint accounts, 1 otherwise | Not a sampling weight[^weight] |
| `joint_holders_in_set` | bigint | 1 = account also appears under another consumer | |
| `archive`, `meta_filename`, `meta_file_row_number`, `revision`, `asset` | mixed | Delivery and source-file tracking | Keep one `revision` per month (see [Important Notes](#equifax-notes)) |
::::

::::{dropdown} Consumer (repeats on each account row)
| Field | Type | Description | Notes |
|---|---|---|---|
| `zip_code`, `state` | varchar | Current address | `state` includes territories, military codes (AA, AE, AP), and a few blanks |
| `consumer_age_archive` | bigint | Age range at archive | Code 0–7, not years |
| `deceased_consumer` | bigint | 1 = deceased | |
| `vantage_score_3`, `vantage_score_4` | bigint | Credit risk scores | Valid 300–850; lower values are codes |
| `bankruptcy_navigator_index` | bigint | Bankruptcy risk; higher = riskier | |
| `consumer_income_score` | bigint | Estimated annual income (Consumer IncomeView) | |
| `inquiries_12_months` | bigint | Credit inquiries, last 12 months | Exception codes[^exceptions] |
| `age_oldest_account`, `age_newest_account`, `age_oldest_mortgage_account` | bigint | Months since accounts opened | Exception codes[^exceptions] |
| `number_of_accounts` and other `number_*` counts | bigint | Counts of accounts by type and status | Exception codes[^exceptions] |
| `number_revolving_accts_greater_than_or_equal_to_50_percent_utilization`, `bankcard_accts_over_75_percent_utilization` | bigint | High-utilization account counts | Exception codes[^exceptions] |
| `total_past_due_amount`, `total_amount_3rd_party_collections` | bigint | Dollar totals | Exception codes[^exceptions] |
| `bankruptcy_flag`, `foreclosure_flag` | bigint | 1 = current bankruptcy / foreclosure | Treat values other than 0/1 as missing |
| `revolver_transactor_behavior_last_{6,12,24}_months` | bigint | 1 = revolver, 2 = transactor | 7–9 = not available |
| `percent_actual_payment_to_scheduled_payment_{auto,mortage}_last_{6,12,24}_months` | bigint | Share of scheduled payments actually paid | Exception codes[^exceptions]; "mortage" spelling is Equifax's |
| `mortgage_inquiries_last_1_month`, `potential_mortgage_inquiries_last_1_month` | bigint | Recent mortgage shopping | |
::::

::::{dropdown} Consumer at account origination (can differ across a consumer's accounts)
| Field | Type | Description | Notes |
|---|---|---|---|
| `origination_vantage_score3`, `origination_vantage_score4` | bigint | Scores from the month before the account opened | |
| `origination_bankruptcy_navigator_index`, `origination_consumer_income_score` | bigint | Risk and income at origination | |
| `pim_score` | bigint | Estimated income at origination ($ thousands) | Predecessor to `consumer_income_score` |
| `consumer_age` | bigint | Age range at origination | Code 0–7, not years |
| `mortgage_indicator` | bigint | 1 = had a mortgage when account opened | |
| `small_business_owner_flag` | bigint | 1 = small business owner | Near zero before 2014, then rises gradually |
::::

::::{dropdown} Account
| Field | Type | Description | Notes |
|---|---|---|---|
| `product_category`, `portfolio_type`, `account_type`, `industry_code` | varchar | What kind of account and lender | Codes in dictionary |
| `origination_product_category`, `origination_portfolio_type`, `origination_industry_code` | varchar | Same, at origination | |
| `origination_date_open` | varchar | Month opened, `YYYYMM` | String, unlike other dates[^dates] |
| `balance`, `high_credit` | bigint | Balance; credit limit or highest balance | |
| `monthly_payment`, `scheduled_payment_amount`, `actual_payment_amount` | bigint | Equifax-calculated, lender-scheduled, and actual payments | Actual is reported on about a third of accounts overall, but on most mortgages |
| `terms` | bigint | Term in months (installment loans) | Mostly null |
| `status_category` | bigint | Standardized status: current, 30/60/90/120+ DPD, closed, etc. | Easiest field for delinquency |
| `rate_status`, `activity_designator`, `narrcode_1`–`narrcode_4` | mixed | Lender-reported status and remarks | Codes in dictionary |
| `ecoa` | varchar | Ownership (individual, joint, etc.) | |
| `new_origination_flag` | bigint | 1 = account first appears in this archive | Often opened months or years earlier; use `origination_date_open` to find new loans |
| `date_reported`, `date_of_last_activity`, `date_of_last_payment` | bigint | Account dates | Nanoseconds[^dates] |
::::

[^weight]: Joint accounts appear once under each holder, so multiply account amounts by `weight` when summing across consumers. `weight` is stored in single precision, so cast it first (`CAST(weight AS double)`) to keep sums accurate.

[^dates]: In Athena, these dates are stored as nanoseconds since 1970, not as `YYYYMMDD`. `origination_date_open` is the exception: a `YYYYMM` string.

[^exceptions]: Many credit attributes reserve the top of their range for codes. In 2-digit fields: 99 = no data, 98 = no account of this type, 93–97 = indeterminate, 92 = at or above maximum. Ages and payment ratios (4 digits) use 9999, 9998, 9993–9997, and 9992; dollar totals (7 digits) use 9999999, 9999998, 9999993–9999997, and 9999992. For counts, Equifax recommends mapping "no account of this type" to zero; for ages and payment ratios, treat it as missing.

[^notdelivered]: `transferred_sold_flag` and the FICO scores appear in the ADS 3.0 layout but are not in the data.

(equifax-notes)=
## Important Notes

Most mistakes with this data come from a handful of structural features. Read these before your first query.

**Each row is an account, not a person.** Consumer fields such as `vantage_score_3` repeat on every account row, so an average over rows over-weights people with many accounts. Reduce to one row per `consumer_id` per month before analyzing consumers. Some "consumer" fields describe the person *when a given account was opened* (`origination_*`, `pim_score`, `consumer_age`) and can differ across one person's accounts.

**Joint accounts appear under each holder.** Multiply account amounts by `weight` (0.5 for joint accounts) when summing across consumers.

**Some months appear under more than one revision.** Each delivery is tagged with a `revision` timestamp, and the table keeps every delivery as received. When a month was delivered more than once, its accounts appear once per revision, so counts and totals for that month are multiplied. In the cases we checked, the copies were identical. Keep one revision per month, the latest:

```sql
WITH latest AS (
    SELECT year, month, MAX(revision) AS revision
    FROM equifax.equifax
    WHERE year = '2020'
    GROUP BY year, month
)
SELECT e.month, COUNT(*) AS n_accounts
FROM equifax.equifax e
JOIN latest l
  ON e.year = l.year AND e.month = l.month AND e.revision = l.revision
GROUP BY e.month;
```

In DuckDB, the sample queries set this up once as a view, so later queries need no extra step. The `revision` column is small, so the extra step adds little to an Athena scan. To check a single month, run `SELECT revision, COUNT(*) ... GROUP BY revision` for it.

**Credit attributes contain exception codes.** Values such as 98 or 9998 mean "no account of this type," not a real count or age. Clean them before computing statistics; see the [Schema](#equifax-dictionary).

**Partition keys are unpadded strings in Athena.** Filter with `WHERE year = '2008' AND month = '5'`. `month = '05'` matches nothing, and `year = 2008` forces a cast that defeats partition pruning.

**Dates are nanoseconds since 1970 in Athena.** Convert with `CAST(from_unixtime(archive_date / 1e9) AS date)`. `origination_date_open` is the exception: a `YYYYMM` string. DuckDB on KLC reads the same columns as ordinary dates, so no conversion is needed there.

**Some fields have limited coverage.** `small_business_owner_flag` starts in January 2013. `date_reported` can lag the archive by a year or more, so some rows reflect stale lender reports.

**Two Equifax deliveries exist.** Athena and the KLC Parquet files come from a 2023 delivery (ADS 3.0). Older 2021 CSV files on KLC use an earlier layout (ADS 1.1) with fewer columns. Don't mix them.

(equifax-queries)=
## Sample Queries

The first examples show how each tool reads the monthly partitions. The toy projects that follow show how you might pull data for a real research question, with one cut of the data from Athena and another from the KLC files. Each project query is kept small, with a single month, `LIMIT 10`, or one state, which you can remove for your own work.

Every query keeps one revision per month, the latest, so months delivered more than once are not double counted (see [Important Notes](#equifax-notes)).

### Basics

#### Athena: build up from one month

Start small and grow the query one step at a time, checking **data scanned** in the console after each step. Because the scan grows with the months you touch, the first step tells you roughly what the full query will cost.

```sql
-- Step 1: one month
WITH latest AS (
    SELECT year, month, MAX(revision) AS revision
    FROM equifax.equifax
    WHERE year = '2020' AND month = '1'
    GROUP BY year, month
)
SELECT e.product_category,
       COUNT(*)                                AS n_accounts,
       SUM(e.balance * CAST(e.weight AS double)) AS total_balance
FROM equifax.equifax e
JOIN latest l
  ON e.year = l.year AND e.month = l.month AND e.revision = l.revision
GROUP BY e.product_category
ORDER BY e.product_category;

-- Step 2: three months (expect about three times the scan of step 1)
WITH latest AS (
    SELECT year, month, MAX(revision) AS revision
    FROM equifax.equifax
    WHERE year = '2020' AND month IN ('1', '2', '3')
    GROUP BY year, month
)
SELECT CAST(e.month AS integer) AS mo, e.product_category,
       COUNT(*)                                AS n_accounts,
       SUM(e.balance * CAST(e.weight AS double)) AS total_balance
FROM equifax.equifax e
JOIN latest l
  ON e.year = l.year AND e.month = l.month AND e.revision = l.revision
GROUP BY CAST(e.month AS integer), e.product_category
ORDER BY CAST(e.month AS integer), e.product_category;

-- Step 3: a full year
WITH latest AS (
    SELECT year, month, MAX(revision) AS revision
    FROM equifax.equifax
    WHERE year = '2020'
    GROUP BY year, month
)
SELECT CAST(e.month AS integer) AS mo, e.product_category,
       COUNT(*)                                AS n_accounts,
       SUM(e.balance * CAST(e.weight AS double)) AS total_balance
FROM equifax.equifax e
JOIN latest l
  ON e.year = l.year AND e.month = l.month AND e.revision = l.revision
GROUP BY CAST(e.month AS integer), e.product_category
ORDER BY CAST(e.month AS integer), e.product_category;
```

`total_balance` counts each joint account's dollars once. For an average balance per account, use `SUM(balance * CAST(weight AS double)) / SUM(CAST(weight AS double))`, not `total_balance / n_accounts`.

#### DuckDB: read and summarize months

Each DuckDB example starts with the same setup: a view named `equifax` over all the files that keeps the latest revision of each month. After that, you filter on `year` and `month` just as in Athena, and DuckDB reads only the months and columns your query uses.

::::{tab-set}

:::{tab-item} Python
:sync: python

```python
import duckdb

ALL_MONTHS = "/kellogg/data/equifax/parquet/equifax/year=*/month=*/*.parquet"

con = duckdb.connect()

# Setup: keep the latest revision of each month
con.sql(f"""
    CREATE VIEW equifax AS
    SELECT * FROM read_parquet('{ALL_MONTHS}', hive_partitioning = true)
    QUALIFY revision = MAX(revision) OVER (PARTITION BY year, month)
""")

# One month
print(con.sql("""
    SELECT product_category,
           COUNT(*)                              AS n_accounts,
           SUM(balance * CAST(weight AS double)) AS total_balance
    FROM equifax
    WHERE year = 2020 AND month = 1
    GROUP BY product_category
    ORDER BY product_category
""").df())

# One year
print(con.sql("""
    SELECT month, product_category,
           COUNT(*)                              AS n_accounts,
           SUM(balance * CAST(weight AS double)) AS total_balance
    FROM equifax
    WHERE year = 2020
    GROUP BY month, product_category
    ORDER BY month, product_category
""").df())
```

:::

:::{tab-item} R
:sync: r

```r
library(duckdb)

all_months <- "/kellogg/data/equifax/parquet/equifax/year=*/month=*/*.parquet"

con <- dbConnect(duckdb())

# Setup: keep the latest revision of each month
dbExecute(con, sprintf("
    CREATE VIEW equifax AS
    SELECT * FROM read_parquet('%s', hive_partitioning = true)
    QUALIFY revision = MAX(revision) OVER (PARTITION BY year, month)
", all_months))

# One month
print(dbGetQuery(con, "
    SELECT product_category,
           COUNT(*)                              AS n_accounts,
           SUM(balance * CAST(weight AS double)) AS total_balance
    FROM equifax
    WHERE year = 2020 AND month = 1
    GROUP BY product_category
    ORDER BY product_category
"))

# One year
print(dbGetQuery(con, "
    SELECT month, product_category,
           COUNT(*)                              AS n_accounts,
           SUM(balance * CAST(weight AS double)) AS total_balance
    FROM equifax
    WHERE year = 2020
    GROUP BY month, product_category
    ORDER BY month, product_category
"))

dbDisconnect(con, shutdown = TRUE)
```

:::

::::

### Toy Project 1: Auto Loan Performance

*Suppose your research project asks how a borrower's credit score at origination relates to how their auto loan performs afterward.*

#### Athena: the starting cohort

Auto loans opened in December 2018, with what the lender knew at origination. The cohort is taken from the March 2019 archive because lenders often take weeks to report a new loan. Define new loans by `origination_date_open`, not `new_origination_flag`: the flag marks accounts that first appear in an archive, many of which were opened years earlier. Remove `LIMIT 10` to pull the full cohort, and run it with `kdcutils` to save the results on KLC.

```sql
SELECT consumer_id, trade_id, origination_date_open, product_category,
       origination_vantage_score3, origination_consumer_income_score,
       high_credit, terms, monthly_payment, weight
FROM equifax.equifax
WHERE year = '2019' AND month = '3'
  AND revision = (SELECT MAX(revision) FROM equifax.equifax
                  WHERE year = '2019' AND month = '3')
  AND origination_date_open = '201812'
  AND product_category IN ('AB2', 'AF2')   -- auto bank and finance loans
LIMIT 10;
```

#### DuckDB: follow the cohort for 12 months

The same cohort, here limited to Illinois, followed month by month from March 2019 through March 2020. Linking accounts across 13 monthly archives is where the KLC files are the better fit. Each row is one holder of one loan in one month: joint loans appear once per holder, so count loans with `COUNT(DISTINCT trade_id)`. Accounts that close drop out of later archives. The Illinois version took under two minutes in testing.

::::{tab-set}

:::{tab-item} Python
:sync: python

```python
import duckdb

ALL_MONTHS = "/kellogg/data/equifax/parquet/equifax/year=*/month=*/*.parquet"

con = duckdb.connect()

# Setup: keep the latest revision of each month
con.sql(f"""
    CREATE VIEW equifax AS
    SELECT * FROM read_parquet('{ALL_MONTHS}', hive_partitioning = true)
    QUALIFY revision = MAX(revision) OVER (PARTITION BY year, month)
""")

# Follow December 2018 auto loans (Illinois) for 13 months
con.sql("""
    COPY (
        WITH cohort AS (
            SELECT trade_id, consumer_id
            FROM equifax
            WHERE year = 2019 AND month = 3
              AND origination_date_open = '201812'
              AND product_category IN ('AB2', 'AF2')   -- auto bank and finance loans
              AND state = 'IL'                         -- remove to follow all states
        )
        SELECT e.consumer_id, e.trade_id, e.year, e.month,
               e.balance, e.status_category
        FROM equifax e
        JOIN cohort USING (trade_id, consumer_id)
        WHERE (e.year = 2019 AND e.month >= 3) OR (e.year = 2020 AND e.month <= 3)
        ORDER BY e.trade_id, e.year, e.month
    ) TO '/scratch/<netid>/auto_cohort_panel.parquet' (FORMAT parquet)
""")
```

:::

:::{tab-item} R
:sync: r

```r
library(duckdb)

all_months <- "/kellogg/data/equifax/parquet/equifax/year=*/month=*/*.parquet"

con <- dbConnect(duckdb())

# Setup: keep the latest revision of each month
dbExecute(con, sprintf("
    CREATE VIEW equifax AS
    SELECT * FROM read_parquet('%s', hive_partitioning = true)
    QUALIFY revision = MAX(revision) OVER (PARTITION BY year, month)
", all_months))

# Follow December 2018 auto loans (Illinois) for 13 months
dbExecute(con, "
    COPY (
        WITH cohort AS (
            SELECT trade_id, consumer_id
            FROM equifax
            WHERE year = 2019 AND month = 3
              AND origination_date_open = '201812'
              AND product_category IN ('AB2', 'AF2')   -- auto bank and finance loans
              AND state = 'IL'                         -- remove to follow all states
        )
        SELECT e.consumer_id, e.trade_id, e.year, e.month,
               e.balance, e.status_category
        FROM equifax e
        JOIN cohort USING (trade_id, consumer_id)
        WHERE (e.year = 2019 AND e.month >= 3) OR (e.year = 2020 AND e.month <= 3)
        ORDER BY e.trade_id, e.year, e.month
    ) TO '/scratch/<netid>/auto_cohort_panel.parquet' (FORMAT parquet)
")

dbDisconnect(con, shutdown = TRUE)
```

:::

::::

### Toy Project 2: Mortgage Payment Behavior Across ZIP Codes

*Suppose your research project studies how mortgage borrowers' payment behavior varies across ZIP codes.*

#### Athena: one month of mortgage accounts

First mortgages in January 2020, with location, balances, status, and the consumer's recent mortgage payment record. Remove `LIMIT 10` for the full month.

```sql
SELECT consumer_id, trade_id, zip_code, state,
       balance, high_credit, monthly_payment,
       scheduled_payment_amount, actual_payment_amount, status_category,
       percent_actual_payment_to_scheduled_payment_mortage_last_6_months,
       weight
FROM equifax.equifax
WHERE year = '2020' AND month = '1'
  AND revision = (SELECT MAX(revision) FROM equifax.equifax
                  WHERE year = '2020' AND month = '1')
  AND product_category = 'FM'              -- first mortgages
LIMIT 10;
```

The payment-ratio field describes the consumer's mortgage payments overall, not this one account, and uses exception codes such as 9998 and 9999.

#### DuckDB: a year-long mortgage panel for one state

Every Illinois first mortgage in every month of 2020, written to your scratch folder. A full year of account-level rows is a pull, not a summary, so it belongs on KLC. The Illinois version took about a minute and a half in testing and returns about 4 million rows.

::::{tab-set}

:::{tab-item} Python
:sync: python

```python
import duckdb

ALL_MONTHS = "/kellogg/data/equifax/parquet/equifax/year=*/month=*/*.parquet"

con = duckdb.connect()

# Setup: keep the latest revision of each month
con.sql(f"""
    CREATE VIEW equifax AS
    SELECT * FROM read_parquet('{ALL_MONTHS}', hive_partitioning = true)
    QUALIFY revision = MAX(revision) OVER (PARTITION BY year, month)
""")

# Illinois first mortgages, every month of 2020
con.sql("""
    COPY (
        SELECT year, month, consumer_id, trade_id, zip_code,
               balance, scheduled_payment_amount, actual_payment_amount,
               status_category, weight
        FROM equifax
        WHERE year = 2020
          AND product_category = 'FM'   -- first mortgages
          AND state = 'IL'              -- remove to cover all states
    ) TO '/scratch/<netid>/il_mortgage_panel_2020.parquet' (FORMAT parquet)
""")
```

:::

:::{tab-item} R
:sync: r

```r
library(duckdb)

all_months <- "/kellogg/data/equifax/parquet/equifax/year=*/month=*/*.parquet"

con <- dbConnect(duckdb())

# Setup: keep the latest revision of each month
dbExecute(con, sprintf("
    CREATE VIEW equifax AS
    SELECT * FROM read_parquet('%s', hive_partitioning = true)
    QUALIFY revision = MAX(revision) OVER (PARTITION BY year, month)
", all_months))

# Illinois first mortgages, every month of 2020
dbExecute(con, "
    COPY (
        SELECT year, month, consumer_id, trade_id, zip_code,
               balance, scheduled_payment_amount, actual_payment_amount,
               status_category, weight
        FROM equifax
        WHERE year = 2020
          AND product_category = 'FM'   -- first mortgages
          AND state = 'IL'              -- remove to cover all states
    ) TO '/scratch/<netid>/il_mortgage_panel_2020.parquet' (FORMAT parquet)
")

dbDisconnect(con, shutdown = TRUE)
```

:::

::::


## Linking to Other Datasets

| Dataset | Linkage approach |
|---|---|
| Census / ACS | `zip_code` to ZIP Code Tabulation Areas (ZCTAs); ZIPs and ZCTAs are close but not identical |
| State-level data | `state` |

For linkage assistance, contact [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu).

## Citing This Data

<span style="color:red; font-weight:bold">[TO CONFIRM: acknowledgment required by the Equifax data use agreement]</span>

## <span style="color:red">Team Discussion (not for users)</span>

<span style="color:red">Remove this section before publishing. Findings from testing that may need action from the team or Equifax.</span>

**1. Four months are stored twice.** Each has two revisions with identical row counts, in both Athena and the KLC files. Every other month has one revision.

| Month | Revisions | Rows per copy |
|---|---|---|
| June 2012 | 2022-03-28T19:28:38.123Z, 2023-05-19T15:09:48.104Z | 136,596,364 |
| July 2020 | 2023-05-18T13:27:24.314Z, 2023-05-18T13:30:17.297Z | 133,427,842 |
| September 2021 | 2022-03-28T19:28:38.123Z, 2023-05-17T21:04:44.968Z | 132,322,469 |
| April 2022 | 2022-06-27T18:00:26.792Z, 2023-05-17T20:35:48.687Z | 134,306,761 |

For April 2022, a fingerprint over seven columns (IDs, balance, status, VantageScore 3 and 4, income score) matched across both revisions, so the copies are identical. June 2012 and September 2021 have not been fingerprinted. The page currently tells users to keep the latest revision per month; if the duplicates are removed, that note and the revision filters in the sample queries can be simplified. To reproduce the list from KLC at no Athena cost:

```python
import duckdb
FILES = "/kellogg/data/equifax/parquet/equifax/year=*/month=*/*.parquet"
print(duckdb.sql(f"""
    SELECT CAST(regexp_extract(file_name, 'year=(\\d+)', 1)  AS INTEGER) AS yr,
           CAST(regexp_extract(file_name, 'month=(\\d+)', 1) AS INTEGER) AS mo,
           list(DISTINCT stats_min_value) AS revisions
    FROM parquet_metadata('{FILES}')
    WHERE path_in_schema = 'revision'
    GROUP BY 1, 2
    HAVING COUNT(DISTINCT stats_min_value) > 1
    ORDER BY 1, 2
""").df().to_string())
```

**2. About 5.7 million accounts disappear between April and May 2020.** Using one revision per month, 2020 counts hold at 141–142 million through April, then drop and stay near 133 million:

| Month | Accounts |
|---|---|
| March 2020 | 141,629,692 |
| April 2020 | 140,475,158 |
| May 2020 | 134,803,341 |
| June 2020 | 133,691,060 |

The drop is concentrated in a few product categories (April → May): retail cards 27,659,884 → 24,700,457; bankcards 55,096,242 → 53,133,846; deferred student loans 6,581,896 → 4,689,290, while non-deferred student loans rose 11,153,209 → 12,937,760. The student loan shift may be reclassification under pandemic relief; the retail and bankcard drop is abrupt for real account closures. Worth asking Equifax whether reporting or sampling changed.

**3. `new_origination_flag` marks accounts new to the archive, not new loans.** Of 423,195 auto loans flagged in January 2019, by opening month:

| Opened | Loans |
|---|---|
| Dec 2018 – Jan 2019 | 180,275 |
| Jul–Nov 2018 | 62,360 |
| Jan–Jun 2018 | 2,435 |
| 2015–2017 | 109,003 |
| Before 2015 | 68,514 |

The page now defines new loans by `origination_date_open` instead. The near-absence of January–June 2018 loans between larger groups on either side is unexplained.

**4. Full population or sample?** Monthly archives hold about 133–142 million accounts, and about 240,000 auto loans opened in December 2018 appear by March 2019. Both look small relative to all U.S. credit accounts and auto lending, suggesting a sample, but this is a rough comparison. Needs confirmation from the Equifax contract or contact.

**5. Geographic scope is unverified.** At a Glance says "United States, including territories and military addresses," which no test has confirmed. To check, list the distinct `state` values in one month:

```sql
SELECT state, COUNT(*) AS n_accounts
FROM equifax.equifax
WHERE year = '2020' AND month = '1'
GROUP BY state
ORDER BY state;
```
