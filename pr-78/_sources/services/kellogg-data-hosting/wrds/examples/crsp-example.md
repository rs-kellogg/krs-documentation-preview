# CRSP Example: Cumulative Return from Monthly Stock File

This example pulls monthly returns for Apple (AAPL) from the CRSP monthly stock file (`crsp.msf`), computes cumulative return over 2015–2023, and plots the result. The full pull returns roughly 100 rows — small enough to run interactively on a KLC login node.

:::{note}
Before You Start

Complete [Setting Up Credentials](setting-up-credentials) and [Connecting from KLC](connecting-from-klc) on the WRDS page. For dataset background, see the [CRSP dataset page](../../../datasets/datasets/crsp).
:::

:::{note}
CRSP offers two table formats on WRDS: the legacy **SIZ** format (`crsp.msf`, `crsp.dsf`) and the newer **CIZ** format (`crsp.msf_v2`, `crsp.wrds_msfv2`). This example uses the SIZ monthly stock file. <!-- TODO(KRS): confirm which CRSP format Kellogg researchers should default to -->
:::

## Workflow

1. Connect to WRDS and look up the PERMNO for AAPL in `crsp.stocknames`.
2. Pull monthly returns, price, and shares outstanding from `crsp.msf`.
3. Compute cumulative return from the monthly return series.
4. Plot cumulative return over time.

## Step 1: Find the PERMNO

CRSP assigns each security a permanent identifier (`permno`) that stays constant even when the ticker changes. Query `crsp.stocknames` to find the PERMNO for a given ticker. A single ticker can map to multiple PERMNOs over time (for example, after a corporate action), so check `namedt` and `nameenddt` to select the correct record.

::::{tab-set}

:::{tab-item} Python
:sync: python

```python
import wrds
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

conn = wrds.Connection(wrds_username="your-wrds-username")

stock = "AAPL"

permno_df = conn.raw_sql(
    f"""
    SELECT permno, comnam, namedt, nameenddt, ticker
    FROM crsp.stocknames
    WHERE ticker = '{stock}'
    ORDER BY namedt DESC
    """,
    date_cols=["namedt", "nameenddt"],
)
print(permno_df)
permno = permno_df.iloc[0]["permno"]
print(f"Using PERMNO: {permno}")
```

:::

:::{tab-item} R
:sync: r

```r
library(DBI)
library(RPostgres)
library(ggplot2)

wrds <- dbConnect(
  Postgres(),
  host    = "wrds-pgdata.wharton.upenn.edu",
  port    = 9737,
  dbname  = "wrds",
  sslmode = "require",
  user    = "your-wrds-username"
)

stock <- "AAPL"

permno_df <- dbGetQuery(
  wrds,
  paste0(
    "SELECT permno, comnam, namedt, nameenddt, ticker
     FROM crsp.stocknames
     WHERE ticker = '", stock, "'
     ORDER BY namedt DESC"
  )
)
print(permno_df)
permno <- permno_df$permno[1]
cat("Using PERMNO:", permno, "\n")
```

:::

::::

## Step 2: Pull Monthly Returns

Query the CRSP monthly stock file for the selected PERMNO over your date range.

::::{tab-set}

:::{tab-item} Python
:sync: python

```python
df = conn.raw_sql(
    f"""
    SELECT permno, date, ret, prc, shrout
    FROM crsp.msf
    WHERE permno = {permno}
      AND date BETWEEN '2015-01-01' AND '2023-12-31'
    ORDER BY date
    """,
    date_cols=["date"],
)
print(df.columns.tolist())
print(df.shape)
```

:::

:::{tab-item} R
:sync: r

```r
df <- dbGetQuery(
  wrds,
  paste0(
    "SELECT permno, date, ret, prc, shrout
     FROM crsp.msf
     WHERE permno = ", permno, "
       AND date BETWEEN '2015-01-01' AND '2023-12-31'
     ORDER BY date"
  )
)
print(colnames(df))
print(dim(df))
```

:::

::::

Expected output:

```text
['permno', 'date', 'ret', 'prc', 'shrout']
(108, 5)
```

## Step 3: Compute Cumulative Return

Convert monthly returns to a cumulative return series. CRSP codes missing returns as special values — drop rows with missing `ret` before computing the cumulative product.

::::{tab-set}

:::{tab-item} Python
:sync: python

```python
df = df.dropna(subset=["ret"])
df["cum_ret"] = (1 + df["ret"]).cumprod() - 1
print(df[["date", "ret", "cum_ret"]].tail())
```

:::

:::{tab-item} R
:sync: r

```r
df <- df[!is.na(df$ret), ]
df$cum_ret <- cumprod(1 + df$ret) - 1
print(tail(df[, c("date", "ret", "cum_ret")]))
```

:::

::::

## Step 4: Plot Cumulative Return

::::{tab-set}

:::{tab-item} Python
:sync: python

```python
plt.figure(figsize=(10, 6))
sns.lineplot(x="date", y="cum_ret", data=df)
plt.ylabel("Cumulative return")
plt.title(f"{stock} cumulative return, 2015–2023")
plt.tight_layout()
plt.show()

conn.close()
```

:::

:::{tab-item} R
:sync: r

```r
ggplot(df, aes(x = date, y = cum_ret)) +
  geom_line() +
  ylab("Cumulative return") +
  ggtitle(paste0(stock, " cumulative return, 2015–2023")) +
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

stock = "AAPL"

permno_df = conn.raw_sql(
    f"""
    SELECT permno, comnam, namedt, nameenddt, ticker
    FROM crsp.stocknames
    WHERE ticker = '{stock}'
    ORDER BY namedt DESC
    """,
    date_cols=["namedt", "nameenddt"],
)
permno = permno_df.iloc[0]["permno"]

df = conn.raw_sql(
    f"""
    SELECT permno, date, ret, prc, shrout
    FROM crsp.msf
    WHERE permno = {permno}
      AND date BETWEEN '2015-01-01' AND '2023-12-31'
    ORDER BY date
    """,
    date_cols=["date"],
)

df = df.dropna(subset=["ret"])
df["cum_ret"] = (1 + df["ret"]).cumprod() - 1

plt.figure(figsize=(10, 6))
sns.lineplot(x="date", y="cum_ret", data=df)
plt.ylabel("Cumulative return")
plt.title(f"{stock} cumulative return, 2015–2023")
plt.tight_layout()
plt.show()

conn.close()
```

:::

:::{dropdown} R

```r
library(DBI)
library(RPostgres)
library(ggplot2)

wrds <- dbConnect(
  Postgres(),
  host    = "wrds-pgdata.wharton.upenn.edu",
  port    = 9737,
  dbname  = "wrds",
  sslmode = "require",
  user    = "your-wrds-username"
)

stock <- "AAPL"

permno_df <- dbGetQuery(
  wrds,
  paste0(
    "SELECT permno, comnam, namedt, nameenddt, ticker
     FROM crsp.stocknames
     WHERE ticker = '", stock, "'
     ORDER BY namedt DESC"
  )
)
permno <- permno_df$permno[1]

df <- dbGetQuery(
  wrds,
  paste0(
    "SELECT permno, date, ret, prc, shrout
     FROM crsp.msf
     WHERE permno = ", permno, "
       AND date BETWEEN '2015-01-01' AND '2023-12-31'
     ORDER BY date"
  )
)

df <- df[!is.na(df$ret), ]
df$cum_ret <- cumprod(1 + df$ret) - 1

ggplot(df, aes(x = date, y = cum_ret)) +
  geom_line() +
  ylab("Cumulative return") +
  ggtitle(paste0(stock, " cumulative return, 2015–2023")) +
  theme_minimal()

dbDisconnect(wrds)
```

:::

## Related Pages

- [CRSP dataset page](../../../datasets/datasets/crsp) — coverage, identifiers, and documentation links
- [Compustat North America](../../../datasets/datasets/compustat-north-america) — linked to CRSP via the CRSP/Compustat Merged database (CRSPLink)
- [A Note on Reproducibility](a-note-on-reproducibility) — save local copies of WRDS pulls for reproducible research
