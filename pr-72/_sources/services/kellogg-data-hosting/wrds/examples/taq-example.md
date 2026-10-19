# TAQ Example: Intraday Trades and Five-Minute Averages

This example uses the **NYSE Trade and Quote (TAQ)** millisecond database on WRDS to fetch second-by-second trade data for Apple (AAPL) on a single trading day, compute five-minute average prices, and graph the result. For one symbol on one day, expect roughly 110,000 rows.

:::{note}
Before You Start

Complete [Setting Up Credentials](setting-up-credentials) and [Connecting from KLC](connecting-from-klc) on the WRDS page. For dataset background, see the [Trade and Quote (TAQ) dataset page](../../../datasets/datasets/trade-and-quote-database).
:::

:::{warning}
TAQ tables are date-suffixed — each trading day is a separate table (for example, `taqmsec.ctm_20230622`). A single symbol on one day returns on the order of 100,000 rows. Multi-symbol or multi-day studies should run as batch jobs on KLC Reserve — see [Launching Jobs on KLC](../../../klc/user-guide/klc-software).
:::

## Workflow

1. Select a company and trading date. Fetch stock price data by the second from the TAQ consolidated trades table.
2. Compute the five-minute average stock price for each observation (not a rolling average).
3. Merge the two tables.
4. Graph the time series with the five-minute average indicated by blue dots.

## Step 1: Obtain WRDS Data Table

Select a company and date, then submit a SQL query against the date-suffixed TAQ table. The query filters to major exchanges (`ex` in N, T, Q, A), excludes zero prices, and requires valid trade correction codes.

::::{tab-set}

:::{tab-item} Python
:sync: python

```python
import wrds
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

conn = wrds.Connection(wrds_username="your-wrds-username")

dd = "20230622"
stock = "AAPL"

sql = f"""
SELECT CONCAT(date, ' ', time_m) AS dt,
       ex, sym_root, sym_suffix, price, size, tr_scond
FROM taqmsec.ctm_{dd}
WHERE (ex = 'N' OR ex = 'T' OR ex = 'Q' OR ex = 'A')
  AND sym_root = '{stock}'
  AND price != 0 AND tr_corr = '00'
"""

df_aapl = conn.raw_sql(sql)
print(df_aapl.columns.tolist())
print(df_aapl.shape)
```

:::

:::{tab-item} R
:sync: r

```r
library(DBI)
library(RPostgres)
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

dd <- "20230622"
stock <- "AAPL"

sql <- paste0("
  SELECT CONCAT(date, ' ', time_m) AS dt,
         ex, sym_root, sym_suffix, price, size, tr_scond
  FROM taqmsec.ctm_", dd, "
  WHERE (ex = 'N' OR ex = 'T' OR ex = 'Q' OR ex = 'A')
    AND sym_root = '", stock, "'
    AND price != 0 AND tr_corr = '00'
")

df_aapl <- dbGetQuery(wrds, sql)
print(colnames(df_aapl))
print(dim(df_aapl))
```

:::

::::

Expected output:

```text
['dt', 'ex', 'sym_root', 'sym_suffix', 'price', 'size', 'tr_scond']
(111590, 7)
```

## Step 2: Obtain Five-Minute Averages

Convert timestamps to datetime, round to the nearest five-minute mark, and resample to get the average price in each five-minute interval.

::::{tab-set}

:::{tab-item} Python
:sync: python

```python
df_aapl["dt"] = pd.to_datetime(df_aapl["dt"])
df_aapl["dt"] = df_aapl["dt"].dt.round("5Min")
df_aapl.set_index("dt", inplace=True)

df_aapl_resampled = df_aapl["price"].resample("5Min").mean()
print(df_aapl_resampled.shape)
```

:::

:::{tab-item} R
:sync: r

```r
df_aapl$dt <- round_date(
  as.POSIXct(df_aapl$dt, format = "%Y-%m-%d %H:%M:%OS"),
  "5 minutes"
)

df_aapl_resampled <- aggregate(
  price ~ dt, df_aapl, function(x) mean(x, na.rm = TRUE)
)
colnames(df_aapl_resampled)[2] <- "avg_price"
print(dim(df_aapl_resampled))
```

:::

::::

Expected output:

```text
(193,)
```

## Step 3: Merge Tables

Merge the tick-level data with the five-minute averages and forward-fill missing average values.

::::{tab-set}

:::{tab-item} Python
:sync: python

```python
df_aapl.reset_index(inplace=True)
df_aapl_resampled = df_aapl_resampled.reset_index()
df_aapl_resampled.rename(columns={"price": "avg_price"}, inplace=True)

df_aapl = df_aapl.merge(df_aapl_resampled, on="dt", how="left")
df_aapl["avg_price"] = df_aapl["avg_price"].ffill()

print(df_aapl.columns.tolist())
print(df_aapl.shape)
```

:::

:::{tab-item} R
:sync: r

```r
df_aapl$avg_price <- NULL
df_aapl <- merge(df_aapl, df_aapl_resampled, by = "dt", all.x = TRUE)

na_locs <- which(is.na(df_aapl$avg_price))
df_aapl$avg_price[na_locs] <- df_aapl$avg_price[na_locs - 1]

print(colnames(df_aapl))
print(dim(df_aapl))
```

:::

::::

Expected output:

```text
['dt', 'ex', 'sym_root', 'sym_suffix', 'price', 'size', 'tr_scond', 'avg_price']
(111590, 8)
```

## Step 4: Graph Results

Plot the tick-level price series in gray with five-minute average prices as blue dots.

::::{tab-set}

:::{tab-item} Python
:sync: python

```python
plt.figure(figsize=(10, 6))

sns.lineplot(x="dt", y="price", data=df_aapl, color="gray")
sns.scatterplot(x="dt", y="avg_price", data=df_aapl, color="blue", s=50)

plt.xlabel("")
plt.ylabel("Intraday price in USD")
plt.ylim(df_aapl["price"].min(), df_aapl["price"].max())
plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=60))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
plt.title(f"AAPL on {df_aapl['dt'].dt.date.unique()[0]}")
plt.show()

conn.close()
```

:::

:::{tab-item} R
:sync: r

```r
ggplot(df_aapl, aes(x = dt)) +
  geom_line(aes(y = price), color = "gray") +
  geom_point(aes(y = avg_price), color = "blue", size = 2) +
  scale_y_continuous(
    "Intraday price in USD",
    limits = c(min(df_aapl$price), max(df_aapl$price))
  ) +
  scale_x_datetime("", date_labels = "%H:%M", date_breaks = "60 min") +
  ggtitle(paste0("AAPL on ", unique(as.Date(df_aapl$dt)))) +
  theme_minimal()

dbDisconnect(wrds)
```

:::

::::

See the [TAQ Project in Python](https://rs-kellogg.github.io/wrds_workshop_public/workflow_p.html) and [TAQ Project in R](https://rs-kellogg.github.io/wrds_workshop_public/workflow_r.html) workshop pages for rendered plots and additional lab exercises.

## Complete Script

:::{dropdown} Python

```python
import wrds
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns

conn = wrds.Connection(wrds_username="your-wrds-username")

dd = "20230622"
stock = "AAPL"

sql = f"""
SELECT CONCAT(date, ' ', time_m) AS dt,
       ex, sym_root, sym_suffix, price, size, tr_scond
FROM taqmsec.ctm_{dd}
WHERE (ex = 'N' OR ex = 'T' OR ex = 'Q' OR ex = 'A')
  AND sym_root = '{stock}'
  AND price != 0 AND tr_corr = '00'
"""

df_aapl = conn.raw_sql(sql)

df_aapl["dt"] = pd.to_datetime(df_aapl["dt"])
df_aapl["dt"] = df_aapl["dt"].dt.round("5Min")
df_aapl.set_index("dt", inplace=True)

df_aapl_resampled = df_aapl["price"].resample("5Min").mean()

df_aapl.reset_index(inplace=True)
df_aapl_resampled = df_aapl_resampled.reset_index()
df_aapl_resampled.rename(columns={"price": "avg_price"}, inplace=True)

df_aapl = df_aapl.merge(df_aapl_resampled, on="dt", how="left")
df_aapl["avg_price"] = df_aapl["avg_price"].ffill()

plt.figure(figsize=(10, 6))
sns.lineplot(x="dt", y="price", data=df_aapl, color="gray")
sns.scatterplot(x="dt", y="avg_price", data=df_aapl, color="blue", s=50)
plt.xlabel("")
plt.ylabel("Intraday price in USD")
plt.ylim(df_aapl["price"].min(), df_aapl["price"].max())
plt.gca().xaxis.set_major_locator(mdates.MinuteLocator(interval=60))
plt.gca().xaxis.set_major_formatter(mdates.DateFormatter("%H:%M"))
plt.title(f"AAPL on {df_aapl['dt'].dt.date.unique()[0]}")
plt.show()

conn.close()
```

:::

:::{dropdown} R

```r
library(DBI)
library(RPostgres)
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

dd <- "20230622"
stock <- "AAPL"

sql <- paste0("
  SELECT CONCAT(date, ' ', time_m) AS dt,
         ex, sym_root, sym_suffix, price, size, tr_scond
  FROM taqmsec.ctm_", dd, "
  WHERE (ex = 'N' OR ex = 'T' OR ex = 'Q' OR ex = 'A')
    AND sym_root = '", stock, "'
    AND price != 0 AND tr_corr = '00'
")

df_aapl <- dbGetQuery(wrds, sql)

df_aapl$dt <- round_date(
  as.POSIXct(df_aapl$dt, format = "%Y-%m-%d %H:%M:%OS"),
  "5 minutes"
)

df_aapl_resampled <- aggregate(
  price ~ dt, df_aapl, function(x) mean(x, na.rm = TRUE)
)
colnames(df_aapl_resampled)[2] <- "avg_price"

df_aapl$avg_price <- NULL
df_aapl <- merge(df_aapl, df_aapl_resampled, by = "dt", all.x = TRUE)

na_locs <- which(is.na(df_aapl$avg_price))
df_aapl$avg_price[na_locs] <- df_aapl$avg_price[na_locs - 1]

ggplot(df_aapl, aes(x = dt)) +
  geom_line(aes(y = price), color = "gray") +
  geom_point(aes(y = avg_price), color = "blue", size = 2) +
  scale_y_continuous(
    "Intraday price in USD",
    limits = c(min(df_aapl$price), max(df_aapl$price))
  ) +
  scale_x_datetime("", date_labels = "%H:%M", date_breaks = "60 min") +
  ggtitle(paste0("AAPL on ", unique(as.Date(df_aapl$dt)))) +
  theme_minimal()

dbDisconnect(wrds)
```

:::

## Related Pages

- [Trade and Quote (TAQ) dataset page](../../../datasets/datasets/trade-and-quote-database) — coverage, identifiers, and documentation links
- [TAQ Project in Python](https://rs-kellogg.github.io/wrds_workshop_public/workflow_p.html) — workshop walkthrough with rendered plots
- [TAQ Project in R](https://rs-kellogg.github.io/wrds_workshop_public/workflow_r.html) — R version of the workshop walkthrough
- [A Note on Reproducibility](a-note-on-reproducibility) — save local copies of WRDS pulls for reproducible research
