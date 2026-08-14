(kellogg-data-hosting)=
# Kellogg Data Hosting

**Kellogg Data Hosting (KDH)** is the collection of data platforms through which Kellogg Research Support provides access to licensed research datasets. It encompasses three platforms:

**[WRDS (Wharton Research Data Services)](wrds/wrds)** — A web-based platform providing access to financial, economic, and marketing datasets (CRSP, Compustat, Execucomp, and many others). Kellogg's site license lets all faculty, PhD students, and approved researchers create their own WRDS account and connect programmatically from KLC or their own computer.

**[Amazon Athena (AWS)](athena/athena)** — A serverless SQL query platform hosting large-scale Kellogg-licensed datasets, including data previously stored in the on-premise Kellogg Data Center. Access is through the AWS console or programmatically from KLC via ODBC.

**[Redivis](redivis/redivis)** — A browser-based data platform operated by Kellogg Research Support and Northwestern University Libraries. Redivis lets researchers discover, query, and analyze curated datasets directly in their browser, with no software installation required. It also supports programmatic access via API from KLC.

To request access to a dataset, contact [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu). For WRDS, you can [register directly](https://wrds-www.wharton.upenn.edu/register/) using your Northwestern email.

## Finding Data by Platform

Not all datasets are available on every platform. See [Find Data by Platform](/services/datasets/by-platform) for the full catalog organized by platform.

| Method | Platform | Best For |
|---|---|---|
| [WRDS web interface](https://wrds-www.wharton.upenn.edu/) | WRDS | Ad-hoc queries, small downloads, browsing available datasets |
| [WRDS from KLC](wrds/wrds) | WRDS | Integrating WRDS data into Python or R workflows on the cluster |
| [AWS Console](athena/athena) | Athena | Exploring Athena data, running ad-hoc SQL queries |
| [KLC via ODBC](athena/athena) | Athena | Integrating Athena data into Python, R, or Stata workflows |
| [Redivis](redivis/redivis) | Redivis | Browser-based discovery, querying, and analysis without local software |

```{toctree}
:maxdepth: 2
:hidden:

WRDS <wrds/wrds>
Athena (AWS) <athena/athena>
Redivis <redivis/redivis>
```
