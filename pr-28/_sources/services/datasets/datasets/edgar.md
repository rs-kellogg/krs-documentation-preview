# EDGAR

## At a Glance

| | |
|---|---|
| **Provider** | U.S. Securities and Exchange Commission (public) |
| **Coverage** | 1993–present |
| **Geographic scope** | US public companies |
| **Update frequency** | Daily |
| **Access platforms** | KLC (`/kellogg/data/EDGAR/`) · Public ([SEC EDGAR full-text search](https://efts.sec.gov/LATEST/search-index?q=%22full-text+search%22)) |
| **Eligible users** | Northwestern community (public data) |
| **Questions** | [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) |

## Description

EDGAR is a collection of all Securities and Exchange Commission filings that are publicly available, in their raw format — either plain text or HTML. All companies, foreign and domestic, are required to file registration statements, periodic reports, and other forms electronically through EDGAR. This collection is suitable for researchers who wish to use scripts to extract variables or perform text analysis on a large set of filings.

## Access

EDGAR data is freely available to the public at [https://www.sec.gov/edgar/search/](https://www.sec.gov/edgar/search/).

Files are also loaded on the [Kellogg Linux Cluster (KLC)](/services/klc/user-guide/klc-user-guide) in the `/kellogg/data/EDGAR/` directory. Contact [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) to confirm access.

On KLC, files are organized into directories by Form Type, and then by Year. For example, all Form 4 filings from 1999 are in the `/kellogg/data/EDGAR/4/1999/` directory. Files have also been renamed to indicate the CIK number and quarter associated with each document. For example, `/kellogg/data/EDGAR/4/1999/9779_4_0000950142-99-000880.txt` is a Form 4 (insider trading) filing from the 4th quarter of 1999 by the entity with CIK = 9779.

If you need help writing a script to work with these files, please contact [Kellogg Research Support](mailto:rs@kellogg.northwestern.edu).

## Data Coverage & Key Identifiers

| Attribute | Value |
|---|---|
| **Time period** | 1993–present |
| **Geographic coverage** | US public companies (foreign companies filing with the SEC included) |
| **Unit of observation** | Filing |
| **Primary identifier** | CIK — Central Index Key (unique filer ID); form type; quarter |
| **Key variables** | Full text of SEC filings in original format (plain text or HTML) |
| **File formats** | Plain text (.txt), HTML |

## Documentation

- [SEC EDGAR Filings and Forms](https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany)

## Related Datasets

- [Compustat North America](compustat-north-america) — financial data linkable via CIK or CUSIP
- [CRSP](crsp) — equity data linkable via CUSIP or ticker
