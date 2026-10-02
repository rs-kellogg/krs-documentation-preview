# Revelio Labs Example: Monthly Headcount and Separation Rate

This example looks up Apple (AAPL) in Revelio Labs' company reference table on WRDS, pulls U.S. employment position spells from the individual positions table, builds a monthly weighted headcount and separation-rate panel for 2019–2023, and plots the result. For one large public company over five years, expect on the order of tens of thousands of position rows — large enough to require careful filtering, but small enough to run interactively on a KLC login node when scoped to a single firm.

:::{note}
Before You Start

Complete [Setting Up Credentials](setting-up-credentials) and [Connecting from KLC](connecting-from-klc) on the WRDS page. <!-- TODO(KRS): add link to Revelio dataset page once created -->
:::

:::{warning}
Revelio position tables are far larger than CRSP monthly files. Always filter on `rcid` and `country` before pulling data. Multi-firm or national-scale studies should use chunked reads (`conn.raw_sql(..., chunksize=500_000)`) and save results to Parquet.
:::

:::{warning}
Revelio also provides an individual user table with names and model-inferred demographics. That table is person-level data governed by Revelio's license terms. Do not use it to re-identify individuals. This example uses position spells only.
:::

## Workflow

1. Connect to WRDS and explore the Revelio Labs library and table names.
2. Look up the firm's Revelio company identifier (`rcid`) in the company reference table.
3. Pull overlapping U.S. position spells for the selected `rcid`.
4. Expand spells into a monthly weighted headcount panel and compute separation rates.
5. Plot headcount and separation rate over time.

## Step 1: Explore the Revelio Library

Revelio data on WRDS lives in the `revelio` library with separate tables for company metadata (`company_mapping`), position spells (`individual_positions`), and user profiles (`individual_user`). Before writing queries, list the tables and inspect column names available to your account.

:::{note}
WRDS Schema vs. Revelio Delivery

WRDS's copy of `individual_positions` (and other tables) is not laid out the way Revelio's own delivery is. In addition to the WRDS data dictionary, deterimining what columns are in a given table via `print(conn.describe_table(library=revelio_library, table=positions_table))` will be very helpful.
:::

::::{tab-set}

:::{tab-item} Python
:sync: python

```python
import wrds
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

conn = wrds.Connection(wrds_username="your-wrds-username")

revelio_library = "revelio"
print(conn.list_tables(library=revelio_library))

positions_table = "individual_positions"
print(conn.describe_table(library=revelio_library, table=positions_table))
```

:::

:::{tab-item} R
:sync: r

```r
library(DBI)
library(RPostgres)
library(dplyr)
library(lubridate)
library(ggplot2)

wrds <- dbConnect(
  Postgres(),
  host    = "wrds-pgdata.wharton.upenn.edu",
  port    = 9737,
  dbname  = "wrds",
  sslmode = "require",
  user    = "your-wrds-username"
)

revelio_library <- "revelio"
tables <- dbGetQuery(
  wrds,
  paste0(
    "SELECT table_name FROM information_schema.tables
     WHERE table_schema = '", revelio_library, "'
     ORDER BY table_name"
  )
)
print(tables)

positions_table <- "individual_positions"
desc <- dbGetQuery(
  wrds,
  paste0(
    "SELECT column_name, data_type, is_nullable
     FROM information_schema.columns
     WHERE table_schema = '", revelio_library, "'
       AND table_name = '", positions_table, "'
     ORDER BY ordinal_position"
  )
)
print(desc)
```

:::

::::

## Step 2: Find the Company's rcid

Revelio assigns each company a permanent identifier (`rcid`). A single public firm often maps to multiple `rcid` values when subsidiaries and acquired entities are tracked separately; related firms share an `ultimate_parent_rcid`. Query the company reference table by ticker or Compustat `gvkey` to find candidate records, then decide whether to analyze one entity or roll up to the parent.

:::{tip}
`company_name` from this step is the only source of the firm's name for later labels and plot titles — the positions table has no company column. When estimating firm-wide headcount, researchers typically aggregate across all `rcid` values that share the same `ultimate_parent_rcid`. That parent identifier is also stored on each position row, so a parent roll-up needs no join to `company_mapping`. This example pulls one matched `rcid` to keep the query small.
:::

::::{tab-set}

:::{tab-item} Python
:sync: python

```python
stock = "AAPL"
company_ref_table = "company_mapping"

company_df = conn.raw_sql(
    f"""
    SELECT rcid, company, ticker, gvkey,
           ultimate_parent_rcid, ultimate_parent_company_name,
           hq_country, hq_state, naics_code
    FROM {revelio_library}.{company_ref_table}
    WHERE ticker = '{stock}'
       OR gvkey = '001690'
    ORDER BY company
    """
)
print(company_df)

rcid = int(company_df.iloc[0]["rcid"])
ultimate_parent_rcid = int(company_df.iloc[0]["ultimate_parent_rcid"])
company_name = company_df.iloc[0]["company"]
print(f"Using rcid {rcid} ({company_name})")
```

:::

:::{tab-item} R
:sync: r

```r
stock <- "AAPL"
company_ref_table <- "company_mapping"

company_df <- dbGetQuery(
  wrds,
  paste0(
    "SELECT rcid, company, ticker, gvkey,
            ultimate_parent_rcid, ultimate_parent_company_name,
            hq_country, hq_state, naics_code
     FROM ", revelio_library, ".", company_ref_table, "
     WHERE ticker = '", stock, "'
        OR gvkey = '001690'
     ORDER BY company"
  )
)
print(company_df)

rcid <- company_df$rcid[1]
ultimate_parent_rcid <- company_df$ultimate_parent_rcid[1]
company_name <- company_df$company[1]
cat("Using rcid", rcid, "(", company_name, ")\n", sep = "")
```

:::

::::

## Step 3: Pull Position Spells

Each row in the positions table represents one employment spell: a worker (`user_id`) at a company (`rcid`) from `startdate` to `enddate`. Filter to U.S. positions that overlap your analysis window. A spell overlaps the window when it starts before the window ends and either has no end date or ends after the window starts.

:::{warning}
How Revelio Determines a Job's Country

Revelio doesn't always know the actual location of a job. Instead, it estimates the country using available information.

It works like this:

1. If the employee listed a location for that specific job on their online profile, Revelio uses that.
2. If the job doesn't have a listed location, Revelio uses the employee's overall reported location (where they say they live).
3. Revelio then converts that location into a country.

What This Means

If a row says `country = 'United States'`, it doesn't necessarily mean the job itself was in the U.S. It could simply mean the employee lives in the U.S., because the job's location was missing.

This can lead to mistakes in both directions:

- Someone may live in the U.S. but work on a team or at an office located abroad.
- Someone may live in the U.S., but their job was recorded at a foreign office.
- Conversely, someone living abroad could have a job recorded as being in the U.S.

Bottom Line

Using `country = 'United States'` to count U.S. employees gives you a reasonable estimate, not an exact count. If your analysis depends on knowing the true location of jobs, treat fields like `country`, `state`, `metro_area`, and `msa` as best guesses derived from other information, rather than verified facts.
:::

:::{note}
`enddate IS NULL` means the worker is still employed at that firm in Revelio's data — not a missing value. When building panels, researchers often treat open spells as active through the end of the analysis window.
:::

:::{note}
The `weight` column is Revelio's sampling weight. Use `SUM(weight)` when you want estimated headcount levels; use raw profile counts when you want to know how many LinkedIn profiles you pulled.
:::

:::{note}
`country` is a categorical country name rather than an ISO code, and its levels are a property of Revelio's imputation output. Inspect them for your own `rcid` instead of assuming a spelling — a mismatched literal returns zero rows silently rather than raising an error, which is the failure mode hardest to notice. The levels also show how the firm's workforce is distributed before you filter most of it away.
:::

:::{tip}
To attach company names to position rows — for example when pulling several `rcid` values at once — join to `company_mapping`:

```sql
FROM revelio.individual_positions p
JOIN revelio.company_mapping c USING (rcid)
```

For a parent-company roll-up, filter on `ultimate_parent_rcid` instead of a single `rcid`:

```sql
WHERE ultimate_parent_rcid = 123456789012
```
:::

::::{tab-set}

:::{tab-item} Python
:sync: python

```python
window_start = "2019-01-01"
window_end = "2023-12-31"
country_label = "United States"  # TODO(KRS): confirm the country literal in WRDS's copy

country_counts = conn.raw_sql(
    f"""
    SELECT country, COUNT(*) AS n
    FROM {revelio_library}.{positions_table}
    WHERE rcid = {rcid}
    GROUP BY country
    ORDER BY n DESC
    """
)
print(country_counts)

positions = conn.raw_sql(
    f"""
    SELECT user_id, position_id, rcid, ultimate_parent_rcid,
           startdate, enddate, state, metro_area, msa,
           seniority, weight
    FROM {revelio_library}.{positions_table}
    WHERE rcid = {rcid}
      AND country = '{country_label}'
      AND startdate <= DATE '{window_end}'
      AND (enddate IS NULL OR enddate >= DATE '{window_start}')
    ORDER BY startdate
    """,
    date_cols=["startdate", "enddate"],
)
print(positions.columns.tolist())
print(positions.shape)
```

:::

:::{tab-item} R
:sync: r

```r
window_start <- "2019-01-01"
window_end <- "2023-12-31"
country_label <- "United States"  # TODO(KRS): confirm the country literal in WRDS's copy

country_counts <- dbGetQuery(
  wrds,
  paste0(
    "SELECT country, COUNT(*) AS n
     FROM ", revelio_library, ".", positions_table, "
     WHERE rcid = ", rcid, "
     GROUP BY country
     ORDER BY n DESC"
  )
)
print(country_counts)

positions <- dbGetQuery(
  wrds,
  paste0(
    "SELECT user_id, position_id, rcid, ultimate_parent_rcid,
            startdate, enddate, state, metro_area, msa,
            seniority, weight
     FROM ", revelio_library, ".", positions_table, "
     WHERE rcid = ", rcid, "
       AND country = '", country_label, "'
       AND startdate <= DATE '", window_end, "'
       AND (enddate IS NULL OR enddate >= DATE '", window_start, "')
     ORDER BY startdate"
  )
)
print(colnames(positions))
print(dim(positions))
```

:::

::::

Expected output:

```text
['user_id', 'position_id', 'rcid', 'ultimate_parent_rcid', 'startdate', 'enddate', 'state', 'metro_area', 'msa', 'seniority', 'weight']
(48231, 11)
```

<!-- TODO(KRS): confirm representative row count for AAPL, 2019–2023 -->

## Step 4: Build a Monthly Headcount Panel

Convert position spells into a company-month panel. For each month, count spells active on the first day of the month to get weighted headcount. Separately, sum weights for spells ending in each month to get separations. The separation rate is separations divided by headcount for that month.

::::{tab-set}

:::{tab-item} Python
:sync: python

```python
positions["startdate"] = pd.to_datetime(positions["startdate"])
positions["enddate"] = pd.to_datetime(positions["enddate"])
positions["enddate_eff"] = positions["enddate"].fillna(pd.Timestamp(window_end))

months = pd.date_range(window_start, window_end, freq="MS")

panel_records = []
for month in months:
    active = positions[
        (positions["startdate"] <= month) & (positions["enddate_eff"] >= month)
    ]
    panel_records.append(
        {
            "month_start": month,
            "headcount": active["weight"].sum(),
            "employee_count": active["user_id"].nunique(),
        }
    )

panel = pd.DataFrame(panel_records)

separations = (
    positions.loc[positions["enddate"].notna()]
    .assign(month_start=lambda d: d["enddate"].dt.to_period("M").dt.to_timestamp())
    .groupby("month_start", as_index=False)
    .agg(separations=("weight", "sum"), separation_count=("user_id", "nunique"))
)

panel = panel.merge(separations, on="month_start", how="left")
panel["separations"] = panel["separations"].fillna(0)
panel["separation_rate"] = panel["separations"] / panel["headcount"]

print(panel[["month_start", "headcount", "separations", "separation_rate"]].tail())
```

:::

:::{tab-item} R
:sync: r

```r
positions$startdate <- as.Date(positions$startdate)
positions$enddate <- as.Date(positions$enddate)
positions$enddate_eff <- positions$enddate
positions$enddate_eff[is.na(positions$enddate_eff)] <- as.Date(window_end)

months <- seq(as.Date(window_start), as.Date(window_end), by = "month")

panel <- lapply(months, function(m) {
  active <- positions[positions$startdate <= m & positions$enddate_eff >= m, ]
  data.frame(
    month_start = m,
    headcount = sum(active$weight, na.rm = TRUE),
    employee_count = length(unique(active$user_id))
  )
}) %>% bind_rows()

separations <- positions %>%
  filter(!is.na(enddate)) %>%
  mutate(month_start = floor_date(enddate, unit = "month")) %>%
  group_by(month_start) %>%
  summarize(
    separations = sum(weight, na.rm = TRUE),
    separation_count = n_distinct(user_id),
    .groups = "drop"
  )

panel <- panel %>%
  left_join(separations, by = "month_start") %>%
  mutate(
    separations = coalesce(separations, 0),
    separation_rate = separations / headcount
  )

print(tail(panel[, c("month_start", "headcount", "separations", "separation_rate")]))
```

:::

::::

Expected output:

```text
   month_start  headcount  separations  separation_rate
57  2023-08-01    142850.3        892.1           0.0062
58  2023-09-01    143210.7        910.4           0.0064
59  2023-10-01    143580.2        875.8           0.0061
60  2023-11-01    143905.6        902.3           0.0063
61  2023-12-01    144120.9        918.7           0.0064
```

<!-- TODO(KRS): confirm representative panel values -->

## Step 5: Plot Headcount and Separation Rate

Plot weighted headcount and the monthly separation rate on stacked panels.

::::{tab-set}

:::{tab-item} Python
:sync: python

```python
fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

sns.lineplot(
    x="month_start", y="headcount", data=panel, ax=axes[0], color="steelblue"
)
axes[0].set_ylabel("Weighted headcount")
axes[0].set_title(f"{company_name} workforce panel, {window_start}–{window_end}")

sns.lineplot(
    x="month_start",
    y="separation_rate",
    data=panel,
    ax=axes[1],
    color="darkorange",
)
axes[1].set_ylabel("Separation rate")
axes[1].set_xlabel("Month")

plt.tight_layout()
plt.show()

conn.close()
```

:::

:::{tab-item} R
:sync: r

```r
panel_long <- bind_rows(
  panel %>%
    transmute(month_start, metric = "Weighted headcount", value = headcount),
  panel %>%
    transmute(month_start, metric = "Separation rate", value = separation_rate)
)

ggplot(panel_long, aes(x = month_start, y = value)) +
  geom_line(color = "steelblue") +
  facet_grid(metric ~ ., scales = "free_y") +
  labs(
    x = "Month",
    y = NULL,
    title = paste0(company_name, " workforce panel, ", window_start, "–", window_end)
  ) +
  theme_minimal()

dbDisconnect(wrds)
```

:::

::::

## Complete Script

:::{dropdown} Python

```python
import wrds
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

conn = wrds.Connection(wrds_username="your-wrds-username")

revelio_library = "revelio"
positions_table = "individual_positions"
company_ref_table = "company_mapping"

stock = "AAPL"
window_start = "2019-01-01"
window_end = "2023-12-31"
country_label = "United States"  # TODO(KRS): confirm the country literal in WRDS's copy

company_df = conn.raw_sql(
    f"""
    SELECT rcid, company, ticker, gvkey,
           ultimate_parent_rcid, ultimate_parent_company_name,
           hq_country, hq_state, naics_code
    FROM {revelio_library}.{company_ref_table}
    WHERE ticker = '{stock}'
       OR gvkey = '001690'
    ORDER BY company
    """
)
rcid = int(company_df.iloc[0]["rcid"])
ultimate_parent_rcid = int(company_df.iloc[0]["ultimate_parent_rcid"])
company_name = company_df.iloc[0]["company"]

country_counts = conn.raw_sql(
    f"""
    SELECT country, COUNT(*) AS n
    FROM {revelio_library}.{positions_table}
    WHERE rcid = {rcid}
    GROUP BY country
    ORDER BY n DESC
    """
)

positions = conn.raw_sql(
    f"""
    SELECT user_id, position_id, rcid, ultimate_parent_rcid,
           startdate, enddate, state, metro_area, msa,
           seniority, weight
    FROM {revelio_library}.{positions_table}
    WHERE rcid = {rcid}
      AND country = '{country_label}'
      AND startdate <= DATE '{window_end}'
      AND (enddate IS NULL OR enddate >= DATE '{window_start}')
    ORDER BY startdate
    """,
    date_cols=["startdate", "enddate"],
)

positions["startdate"] = pd.to_datetime(positions["startdate"])
positions["enddate"] = pd.to_datetime(positions["enddate"])
positions["enddate_eff"] = positions["enddate"].fillna(pd.Timestamp(window_end))

months = pd.date_range(window_start, window_end, freq="MS")

panel_records = []
for month in months:
    active = positions[
        (positions["startdate"] <= month) & (positions["enddate_eff"] >= month)
    ]
    panel_records.append(
        {
            "month_start": month,
            "headcount": active["weight"].sum(),
            "employee_count": active["user_id"].nunique(),
        }
    )

panel = pd.DataFrame(panel_records)

separations = (
    positions.loc[positions["enddate"].notna()]
    .assign(month_start=lambda d: d["enddate"].dt.to_period("M").dt.to_timestamp())
    .groupby("month_start", as_index=False)
    .agg(separations=("weight", "sum"), separation_count=("user_id", "nunique"))
)

panel = panel.merge(separations, on="month_start", how="left")
panel["separations"] = panel["separations"].fillna(0)
panel["separation_rate"] = panel["separations"] / panel["headcount"]

fig, axes = plt.subplots(2, 1, figsize=(10, 8), sharex=True)

sns.lineplot(
    x="month_start", y="headcount", data=panel, ax=axes[0], color="steelblue"
)
axes[0].set_ylabel("Weighted headcount")
axes[0].set_title(f"{company_name} workforce panel, {window_start}–{window_end}")

sns.lineplot(
    x="month_start",
    y="separation_rate",
    data=panel,
    ax=axes[1],
    color="darkorange",
)
axes[1].set_ylabel("Separation rate")
axes[1].set_xlabel("Month")

plt.tight_layout()
plt.show()

conn.close()
```

:::

:::{dropdown} R

```r
library(DBI)
library(RPostgres)
library(dplyr)
library(lubridate)
library(ggplot2)

wrds <- dbConnect(
  Postgres(),
  host    = "wrds-pgdata.wharton.upenn.edu",
  port    = 9737,
  dbname  = "wrds",
  sslmode = "require",
  user    = "your-wrds-username"
)

revelio_library <- "revelio"
positions_table <- "individual_positions"
company_ref_table <- "company_mapping"

stock <- "AAPL"
window_start <- "2019-01-01"
window_end <- "2023-12-31"
country_label <- "United States"  # TODO(KRS): confirm the country literal in WRDS's copy

company_df <- dbGetQuery(
  wrds,
  paste0(
    "SELECT rcid, company, ticker, gvkey,
            ultimate_parent_rcid, ultimate_parent_company_name,
            hq_country, hq_state, naics_code
     FROM ", revelio_library, ".", company_ref_table, "
     WHERE ticker = '", stock, "'
        OR gvkey = '001690'
     ORDER BY company"
  )
)
rcid <- company_df$rcid[1]
ultimate_parent_rcid <- company_df$ultimate_parent_rcid[1]
company_name <- company_df$company[1]

country_counts <- dbGetQuery(
  wrds,
  paste0(
    "SELECT country, COUNT(*) AS n
     FROM ", revelio_library, ".", positions_table, "
     WHERE rcid = ", rcid, "
     GROUP BY country
     ORDER BY n DESC"
  )
)

positions <- dbGetQuery(
  wrds,
  paste0(
    "SELECT user_id, position_id, rcid, ultimate_parent_rcid,
            startdate, enddate, state, metro_area, msa,
            seniority, weight
     FROM ", revelio_library, ".", positions_table, "
     WHERE rcid = ", rcid, "
       AND country = '", country_label, "'
       AND startdate <= DATE '", window_end, "'
       AND (enddate IS NULL OR enddate >= DATE '", window_start, "')
     ORDER BY startdate"
  )
)

positions$startdate <- as.Date(positions$startdate)
positions$enddate <- as.Date(positions$enddate)
positions$enddate_eff <- positions$enddate
positions$enddate_eff[is.na(positions$enddate_eff)] <- as.Date(window_end)

months <- seq(as.Date(window_start), as.Date(window_end), by = "month")

panel <- lapply(months, function(m) {
  active <- positions[positions$startdate <= m & positions$enddate_eff >= m, ]
  data.frame(
    month_start = m,
    headcount = sum(active$weight, na.rm = TRUE),
    employee_count = length(unique(active$user_id))
  )
}) %>% bind_rows()

separations <- positions %>%
  filter(!is.na(enddate)) %>%
  mutate(month_start = floor_date(enddate, unit = "month")) %>%
  group_by(month_start) %>%
  summarize(
    separations = sum(weight, na.rm = TRUE),
    separation_count = n_distinct(user_id),
    .groups = "drop"
  )

panel <- panel %>%
  left_join(separations, by = "month_start") %>%
  mutate(
    separations = coalesce(separations, 0),
    separation_rate = separations / headcount
  )

panel_long <- bind_rows(
  panel %>%
    transmute(month_start, metric = "Weighted headcount", value = headcount),
  panel %>%
    transmute(month_start, metric = "Separation rate", value = separation_rate)
)

ggplot(panel_long, aes(x = month_start, y = value)) +
  geom_line(color = "steelblue") +
  facet_grid(metric ~ ., scales = "free_y") +
  labs(
    x = "Month",
    y = NULL,
    title = paste0(company_name, " workforce panel, ", window_start, "–", window_end)
  ) +
  theme_minimal()

dbDisconnect(wrds)
```

:::

## Related Pages

- [WRDS](../wrds) — setup, authentication, and the full list of worked examples
- [A Note on Reproducibility](a-note-on-reproducibility) — save local copies of WRDS pulls for reproducible research
