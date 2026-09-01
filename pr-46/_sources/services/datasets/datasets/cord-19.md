# CORD-19

## At a Glance

| | |
|---|---|
| **Provider** | Allen Institute for AI |
| **Coverage** | 2020 |
| **Geographic scope** | Global |
| **Update frequency** | Archival |
| **Access platforms** | KLC |
| **Eligible users** | Northwestern community |
| **Questions** | [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) |

## Description

In response to the COVID-19 pandemic, the Allen Institute for AI partnered with leading research groups to prepare and distribute the COVID-19 Open Research Dataset (CORD-19), a free resource of thousands of scholarly articles — including many with full text — about COVID-19 and the coronavirus family of viruses for use by the global research community.

This dataset was intended to mobilize researchers to apply recent advances in natural language processing to generate new insights in support of the fight against this infectious disease. During its active period, the corpus was updated weekly as new research was published in peer-reviewed publications and archival services like bioRxiv, medRxiv, and others.

## Access

Data were downloaded weekly from the CORD-19 site and are saved on KLC in the `/kellogg/data/CORD-19/yyyy-mm-dd` directory. Data files are in JSON or CSV format. Each weekly directory contains:

- Commercial use subset (`comm_use_subset/`)
- Non-commercial use subset (`noncomm_use_subset/`)
- Custom license content (`custom_license/`)
- Preprints that are not peer reviewed (`bioRxiv_medRxiv/`)
- Metadata with Microsoft Academic ID mapping (`metadata.csv`)

## Data Coverage & Key Identifiers

| Attribute | Value |
|---|---|
| **Time period** | 2020 |
| **Geographic coverage** | Global |
| **Unit of observation** | Article |
| **Primary identifier** | TBD |
| **Commonly linked via** | Microsoft Academic ID |
| **Key variables** | Article full text, metadata, license type |

## Documentation

- [CORD-19 dataset](https://www.semanticscholar.org/paper/CORD-19%3A-The-Covid-19-Open-Research-Dataset-Wang-Lo/bc411487f305e451d7485e53202ec241fcc97d3b)
