# Comscore

## At a Glance

| | |
|---|---|
| **Provider** | Comscore |
| **Coverage** | 2019–2020 |
| **Geographic scope** | US |
| **Update frequency** | Discontinued |
| **Access platforms** | KLC, AWS Athena |
| **Eligible users** | Northwestern faculty and doctoral students |
| **Questions** | [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) |

## Description

Historical data feeds and lookups include:

- **Desktop URL Traffic** — individual-level host, directory, and page of visited and referring sites
- **AdMetrix Traffic** — individual-level ad exposures, advertiser, and advertiser hierarchy
- **Ecommerce** — machine-level transaction data including item name, quantity purchased, and total basket cost where available

Data are suppressed for panelists identifiable as under the age of 18 at the time of measurement.

## Access

Comscore data are available as pre-defined AWS Athena tables, which allow for rapid execution of SQL SELECT queries. The raw flat files also reside on KLC in the `/kellogg/data/comscore` directory for those who need to work with those directly.

Please email [Kellogg Research Support](mailto:rs@kellogg.northwestern.edu) to obtain access and to get advice about how to structure your Athena queries for better performance.

## Data Coverage & Key Identifiers

| Attribute | Value |
|---|---|
| **Time period** | 2019–2020 |
| **Geographic coverage** | US |
| **Unit of observation** | Panelist-event |
| **Primary identifier** | `machine_id` (machine), `person_id` (person) |
| **Commonly linked via** | `machine_id`, `person_id`, `time_id` / `time_period_id` |
| **Key variables** | URL, page, ad exposure, advertiser, transaction amount, quantity, demographics |

## Tables

### Desktop URL Traffic — `comscore_url_traffic`

| Column | Type | Description |
|---|---|---|
| `machine_id` | bigint | Unique identifier for each machine |
| `url_idc` | varchar | Unique event identifier |
| `person_id` | bigint | Unique identifier for each person |
| `ss2k` | bigint | Seconds since 2000 |
| `time_id` | int | Comscore date identifier (unique identifier for days) |
| `domain_name` | varchar | Domain name portion of URL |
| `url_host` | varchar | URL host portion of URL |
| `url_dir` | varchar | URL directory portion of URL (e.g. `/gp/product/`) |
| `url_page` | varchar | URL page portion of URL (e.g. `index.asp`) |
| `url_refer_domain` | varchar | Domain name portion of referring URL |
| `url_refer_host` | varchar | URL host portion of referring URL |
| `url_refer_dir` | varchar | URL directory portion of referring URL |
| `url_refer_page` | varchar | URL page portion of referring URL |
| `mimetype` | varchar | MIME type of URL; derived from content-type reply header |
| `http_rc` | int | Standard HTTP reply code (200, 302, 404, etc.) |
| `keywords` | varchar | Search keywords associated with the event |
| `html_title` | varchar | HTML title from the page |
| `pattern_id` | int | Comscore Client Focus Dictionary URL page mask ID |

### Desktop AdMetrix Ad Exposure — `comscore_admetrix`

| Column | Type | Description |
|---|---|---|
| `machine_id` | bigint | Unique identifier for each machine |
| `person_id` | bigint | Unique identifier for each person |
| `time_id` | int | Comscore date identifier (unique identifier for days) |
| `ss2k` | bigint | Seconds since 2000 |
| `adv_pattern_id` | int | Advertiser's AdMetrix Product Dictionary page mask ID |
| `pub_pattern_id` | int | Publisher's Comscore Client Focus Dictionary URL page mask ID |

### AdMetrix Advertiser Pattern Lookup — `comscore_admetrix_product_dictionary`

| Column | Type | Description |
|---|---|---|
| `month_id` | int | Comscore date identifier (unique identifier for months) |
| `adv_pattern_id` | int | Advertiser's AdMetrix Product Dictionary page mask ID |
| `adv_web_id` | int | Comscore AdMetrix Product Dictionary entity ID |
| `adv_web_name` | varchar | Comscore AdMetrix Product Dictionary entity name |
| `adv_level_id` | int | Comscore AdMetrix Product Dictionary level identifier |
| `adv_parent_id` | int | Comscore AdMetrix Product Dictionary parent ID |
| `adv_category` | varchar | Comscore AdMetrix Product Dictionary category name |
| `adv_subcategory` | varchar | Comscore AdMetrix Product Dictionary sub-category name |

### Desktop Ecommerce — `comscore_ecommerce`

| Column | Type | Description |
|---|---|---|
| `month_id` | int | Month number corresponding to Comscore time |
| `domain_name` | varchar(50) | Domain where transaction occurred |
| `machine_id` | bigint | Unique identifier for machines |
| `url_idc` | char(22) | Unique identifier for transactions |
| `time_id` | int | Comscore date identifier (unique identifier for days) |
| `event_time` | datetime | Timestamp of purchase in GMT |
| `payment_desc` | varchar(50) | Payment method used (where observable) |
| `machine_country` | varchar(2) | Country where the panelist who made the purchase is located |
| `itemName` | varchar(500) | Name of item (where observable; only available for retailers with item-level detail) |
| `productCategory` | varchar(250) | Product category name (where observable; only available for retailers with item-level detail) |
| `productSubCategory` | varchar(250) | Product sub-category name (where observable; only available for retailers with item-level detail) |
| `raw_basketTotal` | numeric(20,2) | Total spent for the transaction in USD |
| `raw_quantity` | int | Quantity of items (only available for retailers with item-level detail) |
| `raw_itemTotal` | numeric(20,2) | Total spent for specified item(s) in USD (only available for retailers with item-level detail) |

### Time Lookup — `comscore_time_lookup`

| Column | Type | Description |
|---|---|---|
| `time_id` | int | Comscore date identifier (unique identifier for days) |
| `week_id` | int | Comscore date identifier (unique identifier for weeks) |
| `month_id` | int | Comscore date identifier (unique identifier for months) |
| `calendar_day` | date | Calendar day associated with Comscore `time_id` |

### Traffic Category Map — `comscore_category_map`

| Column | Type | Description |
|---|---|---|
| `month_id` | int | Comscore date identifier (unique identifier for months) |
| `pattern_id` | int | Comscore Client Focus Dictionary URL page mask ID |
| `web_id` | int | Comscore Client Focus Dictionary entity ID |
| `web_name` | varchar(255) | Comscore Client Focus Dictionary entity name |
| `level_name` | varchar(255) | Comscore Client Focus Dictionary level name |
| `level_id` | int | Comscore Client Focus Dictionary level unique identifier |
| `parent_id` | int | Comscore Client Focus Dictionary parent ID |
| `subcategory` | varchar(255) | Comscore Media Metrix category to which entity belongs |
| `category` | varchar(255) | Parent category of the above category |
| `Magazine` | int | Comscore dictionary attribute (1 = True, 0 = False) |
| `Streaming_Video` | int | Comscore dictionary attribute (1 = True, 0 = False) |
| `Blog` | int | Comscore dictionary attribute (1 = True, 0 = False) |
| `Streaming_Audio` | int | Comscore dictionary attribute (1 = True, 0 = False) |
| `Cable_Broadcast_TV` | int | Comscore dictionary attribute (1 = True, 0 = False) |
| `Radio` | int | Comscore dictionary attribute (1 = True, 0 = False) |
| `Newspaper` | int | Comscore dictionary attribute (1 = True, 0 = False) |

### Browser Type Lookup — `comscore_browser_type_lookup`

| Column | Type | Description |
|---|---|---|
| `browser_type` | varchar | Numeric ID for the browser |
| `browser_name` | varchar | High-level browser name |
| `browser_name_detail` | varchar | Browser name with version |

### Desktop Operating System Lookup — `comscore_operating_system_lookup`

| Column | Type | Description |
|---|---|---|
| `month_id` | int | Unique identifier for the month |
| `machine_id` | bigint | Unique identifier for each machine |
| `os_version_name` | varchar | Operating system version name |

### Machine Demographics — `machine_demog`

| Column | Type | Description |
|---|---|---|
| `machine_id` | bigint | Unique identifier for each machine |
| `country` | string | Country where machine is located |
| `local_market` | string | Local market (Designated Market Area code; US only) |
| `computer_location` | string | Home or work (US only) |
| `age` | string | Head of household age |
| `income` | string | Household income |
| `education` | string | Head of household education |
| `child_present` | string | Child present in household |
| `hh_size` | string | Size of household |
| `time_period_id` | int | Unique identifier for the time period |

### Person Demographics — `person_demog`

| Column | Type | Description |
|---|---|---|
| `person_id` | bigint | Unique identifier for each person |
| `machine_id` | bigint | Unique identifier for each machine |
| `gender` | string | Gender of panelist |
| `age` | string | Age of panelist |
| `children_present` | string | Child present in household |
| `hh_income` | string | Household income |
| `hh_size` | string | Size of household |
| `ethnicity` | string | Ethnicity of panelist |
| `race` | string | Race of panelist |
| `hoh_education` | string | Head of household education level |
| `computer_location` | string | Home or work (US only) |
| `country` | string | Country where machine is located |
| `local_market` | string | Local market (Designated Market Area code; US only) |
| `time_period_id` | int | Unique identifier for the time period |

### Person Weights — `person_weights`

| Column | Type | Description |
|---|---|---|
| `machine_id` | bigint | Unique identifier for each machine |
| `person_id` | bigint | Unique identifier for each person |
| `time_period_id` | int | Unique identifier for weeks |
| `numeric_time_zone` | int | Time zone adjustment factor (converts event time from GMT to local) |
| `country` | string | Country where machine is located |
| `weight` | numeric | Weight assigned to the person on the machine |

## Example Queries

Resolve `time_id` values to calendar dates using the time lookup table:

```sql
SELECT
    t.calendar_day,
    u.person_id,
    u.domain_name,
    u.url_host
FROM comscore_url_traffic u
JOIN comscore_time_lookup t ON u.time_id = t.time_id
WHERE t.calendar_day BETWEEN DATE '2020-01-01' AND DATE '2020-01-31'
LIMIT 100;
```

Join URL traffic to person demographics and survey weights:

```sql
SELECT
    u.person_id,
    u.domain_name,
    p.gender,
    p.age,
    w.weight
FROM comscore_url_traffic u
JOIN person_demog p
    ON u.person_id = p.person_id
JOIN person_weights w
    ON u.person_id = w.person_id
   AND u.machine_id = w.machine_id
LIMIT 100;
```

Look up ad exposure events with advertiser names:

```sql
SELECT
    a.person_id,
    a.time_id,
    d.adv_web_name,
    d.adv_category,
    d.adv_subcategory
FROM comscore_admetrix a
JOIN comscore_admetrix_product_dictionary d
    ON a.adv_pattern_id = d.adv_pattern_id
LIMIT 100;
```

Summarize ecommerce spending by domain:

```sql
SELECT
    domain_name,
    COUNT(*) AS transactions,
    SUM(raw_basketTotal) AS total_spend
FROM comscore_ecommerce
GROUP BY domain_name
ORDER BY total_spend DESC
LIMIT 20;
```

## Documentation

- [Desktop URL, AdMetrix, and Ecommerce schema](https://nuwildcat-my.sharepoint.com/:b:/r/personal/jpj8711_ads_northwestern_edu/Documents/Data%20Documentation/comScore/comScore%20Data%20Traffic%20Schema.pdf?csf=1&web=1&e=rsCRMJ)
- [Demographics schema](https://nuwildcat-my.sharepoint.com/:x:/r/personal/jpj8711_ads_northwestern_edu/Documents/Data%20Documentation/comScore/comScore%20Demographics%20Schema.xlsx?d=wdd59b6aaa55145a290e657e698d472c8&csf=1&web=1&e=tFYKmg)
