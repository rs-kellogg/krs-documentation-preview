# ISSM Transactions File Database

## At a Glance

Find information [here](https://wrds-www.wharton.upenn.edu/pages/about/data-vendors/issm/).

If you have questions, reach out to [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu).

## Description

The ISSM Transactions File Database provides tick-by-tick data covering the NYSE and AMEX from 1983 to 1992, and NASDAQ from 1987 to 1992. Each year of data is divided into two files: one for trades and one for quotes. For researchers interested in market microstructure, ISSM is complementary to the NYSE's Trade and Quote (TAQ) Database, which starts in 1993.

Each trade record contains the time to the second, price, volume, originating exchange, and condition codes.

Each quote record contains bid and ask prices timed to the second, originating exchange, bid and ask size (market depth), condition codes, and market maker (for third market quotes).

Supplementary files available on KLC include CUSIP numbers, number of trades and quotes per year, firm name, issue description, margin/option flag, and SIC code.

## Access

This data is available via [Wharton Research Data Services (WRDS)](https://wrds-www.wharton.upenn.edu/). WRDS offers both a web interface for small interactive queries and the WRDS Cloud for running batch programs. Faculty may request a temporary class account for course use.

ISSM data is also available on the Kellogg Linux Cluster (KLC) in the directory `/kellogg/data/issm`, where files are stored in flat ASCII format. The KLC collection includes supplementary files matching stock ticker symbols to CUSIP numbers (constructed by other researchers based on end-year ticker assignments; may include some errors). These supplementary files are not available in WRDS.

## Data Coverage & Key Identifiers

| Attribute | Value |
|---|---|
| **Time period** | NYSE/AMEX 1983–1992; NASDAQ 1987–1992 |
| **Geographic coverage** | US (NYSE, AMEX, NASDAQ) |
| **Unit of observation** | Trade or quote (tick-by-tick) |
| **Primary identifier** | CUSIP (supplementary files on KLC) |
| **Commonly linked via** | Ticker symbol (supplementary files on KLC) |
| **Key variables** | Trade: time, price, volume, exchange, condition codes; Quote: bid price, ask price, bid size, ask size, exchange, condition codes |

## Documentation

- [ISSM Manuals and Overviews](https://wrds-www.wharton.upenn.edu/pages/support/manuals-and-overviews/issm/)
