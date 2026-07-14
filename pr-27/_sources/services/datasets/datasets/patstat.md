# PATSTAT

## At a Glance

| | |
|---|---|
| **Provider** | [European Patent Office (EPO)](https://www.epo.org/searching-for-patents/business/patstat.html) |
| **Coverage** | TBD |
| **Geographic scope** | Global |
| **Update frequency** | TBD |
| **Access platforms** | KLC, KDC |
| **Eligible users** | TBD |
| **Questions** | [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) |

## Description

PATSTAT is a worldwide database of patents, prepared by the European Patent Office (EPO). More information is available on the [PATSTAT website](https://www.epo.org/searching-for-patents/business/patstat.html).

## Access

- PATSTAT data files are loaded on the Kellogg Linux Cluster (KLC) in the `/kellogg/data/patstat` directory
- For your convenience, we joined the data files into CSV files in `/kellogg/data/patstat/CSV`
- We can also load the data into our MS SQL server. Please contact Kellogg Research Support for assistance with this.

This data is also available through the [Kellogg Data Cloud (KDC)](/services/kellogg-data-cloud/kdc.md). Contact [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) to request access.

## Data Coverage & Key Identifiers

| Attribute | Value |
|---|---|
| **Time period** | TBD |
| **Geographic coverage** | Global |
| **Unit of observation** | TBD |
| **Primary identifier** | TBD |
| **Commonly linked via** | TBD |
| **Key variables** | TBD |

## Documentation
### Example Queries

Simple: Applications by filing year and authority
```
SELECT
  appln_auth,
  appln_filing_year,
  COUNT(*) AS applications
FROM tls201_appln
WHERE appln_filing_year BETWEEN 2015 AND 2023
GROUP BY ALL
ORDER BY appln_filing_year, applications DESC;
```
Relationships used: `TLS201_APPLN` contains `APPLN_AUTH` and `APPLN_FILING_YEAR`.

2) First publication per application (earliest pub date)
```
WITH first_pub AS (
  SELECT
    a.appln_id,
    MIN(p.publn_date) AS first_pub_date
  FROM tls201_appln a
  JOIN tls211_pat_publn p USING (appln_id)
  WHERE p.publn_date IS NOT NULL
  GROUP BY a.appln_id
)
SELECT *
FROM first_pub
ORDER BY first_pub_date
LIMIT 100;
```

Join path: `TLS211_PAT_PUBLN.APPLN_ID` → `TLS201_APPLN.APPLN_ID`.

3) Top IPC sections for a given year (A…H)
```
SELECT
  SUBSTR(i.ipc_class_symbol, 1, 1) AS ipc_section,
  COUNT(DISTINCT i.appln_id) AS applns
FROM tls209_appln_ipc i
JOIN tls201_appln a USING (appln_id)
WHERE a.appln_filing_year = 2020
  AND i.ipc_class_level IN ('A', 'C', 'M')  -- keep main/class levels as available
GROUP BY ipc_section
ORDER BY applns DESC;
```
Classification link: `TLS209_APPLN_IPC.APPLN_ID` ↔ `TLS201_APPLN.APPLN_ID`.

4) CPC heatmap: top CPC main groups by authority and year
```
SELECT
  a.appln_auth,
  a.appln_filing_year,
  REGEXP_EXTRACT(c.cpc_class_symbol, '^[A-HY]\\d+\\D\\d+/?\\d*') AS cpc_main_group,
  COUNT(DISTINCT a.appln_id) AS applns
FROM tls224_appln_cpc c
JOIN tls201_appln a USING (appln_id)
WHERE a.appln_filing_year BETWEEN 2019 AND 2023
GROUP BY ALL
HAVING COUNT(DISTINCT a.appln_id) >= 100
ORDER BY appln_filing_year DESC, applns DESC
LIMIT 200;
```
CPC link: `TLS224_APPLN_CPC` ↔ `TLS201_APPLN`.

5) Applicant country roll‑up using person roles
```
-- Role values depend on PATSTAT coding; often 'applicant' vs 'inventor' is in ROLE.
-- This example treats ROLE='applicant' (adjust if your coding uses 'applicant', 'app', 'applicants', or numeric codes).
WITH applicants AS (
  SELECT pa.appln_id, pa.person_id
  FROM tls207_pers_appln pa
  WHERE LOWER(pa.role) = 'applicant'
),
applicant_ctry AS (
  SELECT a.appln_id, p.person_ctry_code
  FROM applicants a
  JOIN tls206_person p USING (person_id)
)
SELECT
  person_ctry_code,
  a.appln_filing_year,
  COUNT(DISTINCT a.appln_id) AS applns
FROM tls201_appln a
LEFT JOIN applicant_ctry ac USING (appln_id)
WHERE a.appln_filing_year BETWEEN 2018 AND 2023
GROUP BY ALL
ORDER BY appln_filing_year, applns DESC;
```

People link: `TLS207_PERS_APPLN.APPLN_ID/PERSON_ID` → `TLS206_PERSON.PERSON_ID`, with roles.
