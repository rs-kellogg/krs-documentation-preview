# First Call Historical Database

## At a Glance

| | |
|---|---|
| **Provider** | Thomson Financial (First Call) |
| **Coverage** | 1980–TBD |
| **Geographic scope** | TBD |
| **Update frequency** | Archival |
| **Access platforms** | KLC |
| **Eligible users** | Kellogg faculty and doctoral students |
| **Questions** | [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) |

## Description

First Call Historical Database (FCHD) includes First Call's real-time earnings estimates and related information. Available data includes:

- Broker estimate detail and consensus estimates
- Estimate revision activity
- Actuals
- Company-issued guidelines
- Footnotes
- Stock splits
- Target prices (until 2003)
- Company and issuer information
- Cross-reference to other First Call products

The data goes back to 1987 (1980 in some cases). In addition to the date estimates were published, First Call includes a time stamp.

## Access

First Call Historical Database is available to current Kellogg faculty and doctoral students on the Kellogg Linux Cluster (KLC).

To facilitate access, the files have been read into SAS. The SAS files are available in the `/kellogg/data/firstcall/sasdata/` directory. Assign a library name to this directory to use these files.

**Note:** For the `deleted`, `source`, and `tgt_type` variables, there are some undocumented codes.

### File layouts

- **`tgt_prc_live.prn`** and **`tgt_prc_del.prn`** contain target prices for live and delisted companies, respectively. Both files are pipe-delimited and include a header row with variable names. Each date field includes a time stamp that must be parsed into two parts. Missing values for prices are coded `NA`; missing alphanumeric values are represented by a space. Price values have two implied decimals (e.g., `5760` = `$57.60`).
- **`cross_ref.dat`** contains a mapping between security ID, First Call ticker, and Thomson Financial ID. The file is tab-delimited without a header row. This file enables linking FCHD to other Thomson Financial datasets such as CDA/Spectrum or Lancer Analytics Insiders.

## Data Coverage & Key Identifiers

| Attribute | Value |
|---|---|
| **Time period** | 1980–TBD |
| **Geographic coverage** | TBD |
| **Unit of observation** | Analyst estimate |
| **Primary identifier** | First Call ticker, Thomson Financial ID |
| **Commonly linked via** | Thomson Financial ID |
| **Key variables** | Broker estimates, consensus estimates, actuals, company guidelines, target prices, stock splits |

## Documentation

- [FCHD User Guide](https://nuwildcat.sharepoint.com/:b:/s/KSM-RSDataDocumentation/ETxNWf0Xc55FhhtyvG84QkcBKGQzQP7RtChW9ZD_TFavRQ?e=nLt8Hj)
- [FCHD Technical Guide](https://nuwildcat.sharepoint.com/:b:/s/KSM-RSDataDocumentation/EfSLtw9mGnFLtkfA4-rm0acBZvBN-FffjcnPfw7OAnOx1w?e=YfJncwf)
- [Target Price History File](https://nuwildcat.sharepoint.com/:b:/s/KSM-RSDataDocumentation/Ef4nS8p8jIlKmBb72qrhSoIBpLjwSBq9316gTqtcMlZweQ?e=pGSXke)
- [Analyst-Recommendation History File](https://nuwildcat.sharepoint.com/:b:/s/KSM-RSDataDocumentation/EeSJqEUWNf1EpGpY59aCrVIBIyzQ0vlPWz0v52qHIgpdZg?e=vdeehH)
- [SAS conversion code](https://nuwildcat.sharepoint.com/:t:/s/KSM-RSDataDocumentation/EZIvasf0rPFDplCwwfQf4oIBvNPb0GLxA55IaCg8_NwI0w?e=DEfAgA)
- [SAS file contents](https://nuwildcat.sharepoint.com/:t:/s/KSM-RSDataDocumentation/EfSeaJi4rwVEsroyy6FSxpwB55L-lNh2jb1EkzrtxEyIyw?e=mKSUwy)

## Related Datasets

- CDA/Spectrum
- Lancer Analytics Insiders
