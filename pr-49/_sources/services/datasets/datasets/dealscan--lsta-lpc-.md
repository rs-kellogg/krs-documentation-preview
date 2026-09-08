# DealScan (LSTA/LPC)

## At a Glance

| | |
|---|---|
| **Provider** | Refinitiv LPC (Loan Pricing Corporation), via WRDS |
| **Coverage** | 1987–present |
| **Geographic scope** | Global (emphasis on US) |
| **Update frequency** | Quarterly |
| **Access platforms** | WRDS · KLC |
| **Eligible users** | Faculty and doctoral students |
| **Questions** | [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) |

## Description

DealScan (also known as LPC DealScan or Loan Pricing Corporation DealScan) is the primary source for information on the global commercial loan market. The database contains comprehensive historical information on loan pricing, contract details, terms, and conditions.

In addition to loan data, DealScan also provides contract information for:

- High-yield bonds
- Private placements
- Hybrid financial structures

DealScan data are compiled from SEC filings and public documents (10-Ks, 10-Qs, 8-Ks, and registration statements), loan syndicators, and other internal sources.

*Description courtesy of WRDS.*

## Access

> This dataset is available via [Wharton Research Data Services (WRDS)](https://wrds-www.wharton.upenn.edu/). WRDS offers both a web interface for small interactive queries and the WRDS Cloud for running batch programs. Faculty may request a temporary class account for course use.

> Files are located at `/kellogg/data/lpc/` on [KLC](/services/klc/user-guide/klc-user-guide). Contact [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) to confirm access.

**Note on KLC files:** KLC contains legacy "data dump" files from a previous subscription to DealScan in the `/kellogg/data/lpc` directory. **Current research should not use these files.** They are maintained only for reproducing earlier work that used them. Use the WRDS subscription for current research.

## Data Coverage & Key Identifiers

| Attribute | Value |
|---|---|
| **Time period** | 1987–present |
| **Geographic coverage** | Global (emphasis on US) |
| **Unit of observation** | Loan facility |
| **Primary identifier** | FacilityID (loan facility), BorrowerID |
| **Commonly linked via** | GVKEY or CUSIP to Compustat/CRSP using the Chava-Roberts or similar link table |
| **Key variables** | Loan amount, spread, maturity, loan type, covenants, lender identities, borrower identities |

## Documentation

- [DealScan documentation on WRDS](https://wrds-www.wharton.upenn.edu/pages/support/manuals-and-overviews/thomson-reuters/wrds-reuters-dealscan/)

## Related Datasets

- [SDC Platinum](sdc-platinum) — M&A and new issues transactions
- [Capital IQ](capital-iq) — private company financials and transactions
- [CRSP](crsp) · [Compustat North America](compustat-north-america) — for public company linkage
