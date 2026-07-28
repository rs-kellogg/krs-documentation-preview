# CRSP

## At a Glance

Find information [here](https://wrds-www.wharton.upenn.edu/pages/about/data-vendors/center-for-research-in-security-prices-crsp/).

If you have questions, reach out to [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu).

## Description

[CRSP](https://www.crsp.org) is a collection of datasets with basic and derived information for securities traded on US exchanges (NYSE, AMEX, and NASDAQ). Monthly data generally starts in 1925, while daily data starts in 1962. Kellogg subscribes to the following CRSP datasets:

- **US Stock databases:** The end-of-day and month-end files include high, low and closing prices, trading volumes, shares outstanding, total returns, year-end capitalization, distribution information, etc.
- **US Indices database and security-portfolio assignment module:** These files provide market indices on a daily, monthly, quarterly, and annual basis, additional market and security-level portfolio statistics, and decile portfolio assignment data.
- **US Treasury databases:** These files contain data on US Treasury bills, notes, and bonds, providing complete historical descriptive information and market data including prices, returns, accrued interest, yields, and durations. Four groups of supplemental files extract term structures and risk-free rates (Treasury bill term structure files, Fama-Bliss discount bond files, risk-free rates file, maturity portfolio returns file).
- **Survivor-Bias-Free US Mutual Fund database:** This database provides survivor-bias-free open-ended data for funds of all investment objectives, such as monthly and annual returns, monthly total net assets, monthly net asset values, and distributions.
- **CRSP/Compustat Merged database:** This database contains the Compustat data reformatted into CRSPAccess format with "CRSPLink", linking CRSP data and Compustat data. CRSPLink links Compustat's unique identifier for companies (GVKEY) with CRSP's unique identifiers (PERMNO and PERMCO).

Security identifiers such as name, CUSIP, and ticker are linked to unique CRSP identifiers, allowing complete time-series analysis even if the security identifiers change over time.

## Access

This dataset is available via [Wharton Research Data Services (WRDS)](https://wrds-www.wharton.upenn.edu/). WRDS offers both a web interface for small interactive queries and the WRDS Cloud for running batch programs. Faculty may request a temporary class account for course use.

## Data Coverage & Key Identifiers

| Attribute | Value |
|---|---|
| **Time period** | Monthly 1925–present; Daily 1962–present |
| **Geographic coverage** | US (NYSE, AMEX, NASDAQ) |
| **Unit of observation** | Security |
| **Primary identifier** | PERMNO — unique security ID; PERMCO — unique company ID |
| **Commonly linked via** | CUSIP, ticker; GVKEY via CRSPLink merge with Compustat |
| **Key variables** | Prices (high, low, close), trading volume, shares outstanding, total returns, dividends, market capitalization |

## Documentation

- [CRSP Support Articles](https://wrds-www.wharton.upenn.edu/pages/support/support-articles/crsp/)
- [CRSP Manuals & Overviews](https://wrds-www.wharton.upenn.edu/pages/support/manuals-and-overviews/crsp/)

## Related Datasets

- [Compustat North America](compustat-north-america) — linked via the CRSP/Compustat Merged database (CRSPLink)
- [ExecuComp](execucomp) — linked via GVKEY
- [Compustat Global](compustat-global)
