# Kellogg Data Cloud

The **Kellogg Data Cloud (KDC)** is a collection of cloud-based data platforms that host Kellogg-licensed datasets. It encompasses two platforms:

**[Amazon Athena (AWS)](athena/athena)** — A serverless SQL query platform for Kellogg-licensed datasets, including data previously stored in the on-premise Kellogg Data Center (Microsoft SQL Server). Access is through the AWS console or programmatically from KLC via an ODBC connection.

**[Redivis](redivis/redivis)** — A browser-based data platform operated by Kellogg Research Support and Northwestern University Libraries. Redivis lets researchers discover, query, and analyze curated datasets directly in their browser, with no software installation required. It also supports programmatic access via API from KLC.

To request access to any KDC dataset, contact [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu). Access is granted per dataset or database, not to the platforms as a whole.

## What Datasets Are Available and Where?

Not all datasets are available on every platform. See [Find Data by Platform](/services/datasets/by-platform) for a full catalog of Kellogg datasets organized by the platform through which they are accessed.

## How to Access KDC Data

| Method | Platform | Best For |
|---|---|---|
| [AWS Console](athena/athena) | Amazon Athena | Exploring data, running ad-hoc SQL queries, downloading results |
| [KLC via ODBC](athena/athena) | Amazon Athena | Integrating KDC data into Python, R, or Stata workflows on the cluster |
| [Redivis](redivis/redivis) | Redivis | Browser-based discovery, querying, and analysis without local software |

```{toctree}
:maxdepth: 2
:hidden:

Athena DB (AWS) <athena/athena>
Redivis <redivis/redivis>
```
