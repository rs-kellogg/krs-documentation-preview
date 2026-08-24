# Value Line

## At a Glance

| | |
|---|---|
| **Provider** | Value Line |
| **Coverage** | July 1987–April 2005 |
| **Geographic scope** | US |
| **Update frequency** | Archival |
| **Access platforms** | KLC |
| **Eligible users** | Northwestern faculty and doctoral students |
| **Questions** | [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) |

## Description

Value Line's Historical Estimates & Projections File provides a variety of Value Line analysts' estimates and 3-to-5-year projections for approximately 1,700 companies and industries, the same broad group covered by [Value Line Investment Survey](http://libguides.northwestern.edu/az.php?q=value). Among the variables included are:

- Value Line proprietary rankings (timeliness, safety, financial strength)
- Price performance indicators (beta, stability, growth persistence, earnings predictability)
- Year-ahead estimates (EPS, dividends)
- 3-to-5-year performance projections (appreciation, total return)
- Projected growth rates of key financial indicators
- Annual estimates of selected financial indicators
- Quarterly estimates of sales, EPS
- Aggregate information for around 90 industries

## Access

Value Line's Historical and Projections File is available to current Kellogg faculty and doctoral students on the [Kellogg Linux Cluster (KLC)](http://www.kellogg.northwestern.edu/rs/computing/kellogg-linux-cluster.aspx).

The original Value Line data files were in Microsoft Access format. For user convenience, they have been read into SAS as a single data file, uploaded to KLC under `/kellogg/data/valueline`. The file name is `estimatesvalueline_1987_2005.sas7bdat`. A variable `original_file` was added to flag the origin of the record.

The list of companies covered by Value Line between 04/23/1965 and 05/09/2008 is available in `/kellogg/data/valueline/arnknam2.txt`. The exact coverage list for every Value Line issue date is in `/kellogg/data/valueline/arnknamf.txt`.

## Data Coverage & Key Identifiers

| Attribute | Value |
|---|---|
| **Time period** | July 1987–April 2005 |
| **Geographic coverage** | US |
| **Unit of observation** | Company-period |
| **Primary identifier** | TBD |
| **Commonly linked via** | TBD |
| **Key variables** | Timeliness ranking, safety ranking, EPS estimates, dividend estimates, beta, projected growth rates |

## Documentation

- [Value Line Estimates and Projections File](https://nuwildcat.sharepoint.com/:b:/s/KSM-RSDataDocumentation/EaZWWMuwlFdFpZUAeWd8Hu8BnxmsoFNpj3TK_NUCfyxiJw?e=a0pr0T) (PDF): vendor description
- [Estimates Database Field Descriptions](https://nuwildcat.sharepoint.com/:b:/s/KSM-RSDataDocumentation/EVImwdarliJCp-5_kGj63_wBlW1e2SSOF0DnxlMSlfmNvA?e=e0iPGs) (PDF)
- [Value Line's Glossary of Terms](http://www.valueline.com/Tools/glossary.aspx)
- [How to Invest in Common Stocks: The Complete Guide to Using the Value Line Investment Survey](https://nuwildcat.sharepoint.com/:b:/s/KSM-RSDataDocumentation/EaBxwLnSUbNOgJ5spztE5uMB90GTmoPtXd995M8d4uV5XA?e=E64f8g) (PDF): guide for understanding variables in the dataset
- [Layout of Value Line data on KLC](https://nuwildcat.sharepoint.com/:t:/s/KSM-RSDataDocumentation/EdGSUX0ZwkNIjXJiETNUFAQBYH5ENRkIGWZxYJOxfzc6DQ?e=GnjgwL)
