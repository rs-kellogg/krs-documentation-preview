# Numerator

```{grid} 1 2 2 4
:gutter: 3

:::{grid-item-card} 📊 Schema Reference
:link: schema
:link-type: ref
Current table schemas and field definitions for all 8 tables (September 2025+).
:::

:::{grid-item-card} 🕒 Version History
:link: redivis-versions
:link-type: ref
Redivis version timeline, BATCH_DATE values, and which version was served on a given date.
:::

:::{grid-item-card} 🔄 Migrating Old Queries
:link: migration
:link-type: ref
BATCH_DATE deduplication patterns and a step-by-step query migration example (Athena/v1.x → v3.x).
:::

:::{grid-item-card} 📥 Data Dictionaries
Contact [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) to request the full field definitions:

- Current (Sep 2025): `Numerator_QuarterlyDataFeed_DataDictionary_091925.xlsx`
- Pre-Sep 2025: `NorthwesternU_Data_Feed_DisaggLv3_Data_Scope_20250808.xlsx`
:::
```

## Overview

| | |
|---|---|
| **Provider** | Numerator |
| **Time period** | January 1, 2019 – latest completed quarter |
| **Update frequency** | Quarterly |
| **Geographic scope** | US |
| **Unit of observation** | Trip (basket), with item-level detail in `itemlvl_fact_table` |
| **Primary identifiers** | `BASKET_ID` (trip) · `USER_ID` (panelist) · `ITEM_ID` (product) |
| **Commonly linked via** | `USER_ID` → people / history / static / attributes; `BANNER_ID` → banner; `ITEM_ID` → item |
| **Key variables** | Purchase histories, demographics, psychographics, media consumption, premium people groups (pet, mom+baby, health) |
| **Access platforms** | Redivis |
| **Eligible users** | Northwestern community |
| **Questions** | [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) |

## Description

Numerator is a market research firm that collects longitudinal purchase data from consumers via purchase-tracking apps and survey panels. Kellogg's subscription covers individual-level transaction histories, item-level product detail, household demographics, psychographics, and media attributes for a US panel. The data tracks purchases across all product categories and retail channels — in-store, online, and delivery.

```{important}
The Numerator schema underwent a significant restructuring in **September 2025**: the single fact table was split into an item-level fact table and a summary-level fact table. If you have queries written against the old schema or are working with Athena/Redivis v1.x data, see the [Legacy Schema & Query Migration](#migration) section below.
```

## Access

Access is restricted to members of the Northwestern University community on the Redivis platform. [Access instructions are available on SharePoint.](https://nuwildcat.sharepoint.com/:b:/s/KSM-RSDataDocumentation/EQrjBdUWcmZFiknDuw6WyiUBRPwtOIlTYhpAXd6nTwklGA?e=psQYGF) Please email [Kellogg Research Support](mailto:rs@kellogg.northwestern.edu) to confirm access.

(redivis-versions)=
## Redivis Dataset Versions

The Numerator dataset was originally hosted on Athena and then migrated to Redivis. A `BATCH_DATE` column was present on **both platforms** and was required for correct deduplication in both environments. This changed significantly with the September 2025 schema restructure.

### Athena & Redivis v1.x (pre-September 2025 schema)

Both the original Athena tables and Redivis versions **v1.0 through v1.3** use the old single-fact-table schema. Each quarterly delivery appended a full re-delivery of the historical data as a new batch, tagging rows with a `BATCH_DATE`. As a result, **the same purchase record can appear multiple times** in the table.

| Redivis version | BATCH_DATE values present | Data added |
|---|---|---|
| **v1.0** | 2024-05-13, 2024-07-22, 2024-10-21 | Coverage 1/1/2018 – 9/30/2024 |
| **v1.1** | + 2025-01-17 | Added Q4 2024 (1/1/2024 – 12/31/2024) |
| **v1.2** | + 2025-05-01 | Added Q1 2025 (1/1/2025 – 3/31/2025) |
| **v1.3** | + 2025-07-24 | Added Q2 2025 (1/1/2025 – 6/30/2025) |

```{warning}
Querying an Athena or Redivis v1.x table **without filtering on** `BATCH_DATE` returns duplicate rows and will cause inflated trip counts and spend totals. See the [Legacy Schema & Query Migration](#migration) section below for the correct deduplication pattern.
```

### v3.x (September 2025+ schema)

Redivis versions **v3.0 and later** use the new split-fact-table schema and **do not include a `BATCH_DATE` column**. Each version is a clean, complete snapshot. Deduplication is no longer necessary.

| Redivis version | Time period covered |
|---|---|
| **v3.0** | 1/1/2019 – 6/30/2025 |
| **v3.1** | 1/1/2019 – 9/1/2025 |
| **v3.2** | 1/1/2019 – 12/31/2025 |

```{note}
There is no v2.x of the Numerator dataset on Redivis. The version jump from v1.x to v3.x reflects the major schema restructure in September 2025.
```

### Default version served by date

If you queried Redivis **without pinning to a specific version** (e.g., via the Redivis Python API without a version tag), the version you received depended on when the query ran.

| Query ran between | Default version | Schema era |
|---|---|---|
| 2024-12-16 – 2025-02-25 | **v1.0** | Old schema — BATCH_DATE deduplication required |
| 2025-02-25 – 2025-07-11 | **v1.1** | Old schema — BATCH_DATE deduplication required |
| 2025-07-11 – 2025-07-30 | **v1.2** | Old schema — BATCH_DATE deduplication required |
| 2025-07-30 – 2025-10-07 | **v1.3** | Old schema — BATCH_DATE deduplication required |
| 2025-10-07 – 2025-10-30 | **v3.0** | New schema — no deduplication needed |
| 2025-10-30 – 2026-03-02 | **v3.1** | New schema — no deduplication needed |
| 2026-03-02 – present | **v3.2** | New schema — no deduplication needed |

```{important}
If you have saved results from an unversioned query, use the date above to confirm whether BATCH_DATE deduplication was necessary and which time period was covered. Any query run before 2025-10-07 used the old single-fact-table schema.
```

```{seealso}
For BATCH_DATE deduplication SQL patterns and a step-by-step query migration example, see the [Legacy Schema & Query Migration](#migration) section below.
```

## Data History

Routine quarterly deliveries that contain only new data (no schema changes) are not listed here.

| Date | Change |
|---|---|
| **July 2023** | Initial delivery. Seven tables: `fact`, `banner`, `item`, `people`, `static`, `people_attributes`, `validation`. Coverage: January 1, 2019 – July 13, 2023. |
| **May 2024** | Contract expansion: additional fields added to Fact, People, and Item tables; more attributes added to People Attributes table; historical coverage extended back to January 1, 2018 *(later retracted — see August 2025)* |
| **April 2025** | Static panel expanded to 200K households; People History table (`people_history`) added; Damped Metrics removed from Fact table |
| **July 2025** | `PAYMENT_METHOD` field added to Fact table |
| **August 2025** | Time scope corrected to January 1, 2019 onward (pre-2019 data removed); files reorganized into per-table folders; file format changed to **snappy.parquet**; `WALMART_PLUS_MEMBERSHIP` added to People table; `ER_FACTOR` added to Fact table |
| **September 2025** ⚠️ | **Major restructure:** Fact table split into `standard_nmr_feed_itemlvl_fact_table` (item-level trips) and `standard_nmr_feed_summarylvl_fact_table` (all trips, basket-level only); new fields added to Summary Level Fact and Banner tables |
| **January 2026** | Q4 2025 data added; coverage now January 1, 2019 – December 31, 2025 |

(schema)=
## Schema

### Current Schema (from September 2025)

- Data Dictionary — Current (September 2025, XLSX): contact [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) to request access.

| Table | Description |
|---|---|
| `standard_nmr_feed_itemlvl_fact_table` | Trip-level data for fully transcribed shopping trips with item-level detail |
| `standard_nmr_feed_summarylvl_fact_table` | Trip-level basket totals for **all** trips — more trips than item-level, but no item breakdown |
| `standard_nmr_feed_banner_table` | Store/retailer hierarchy lookup |
| `standard_nmr_feed_item_table` | Product hierarchy lookup |
| `standard_nmr_feed_people_table` | Current panelist demographics |
| `standard_nmr_feed_people_history_table` | Time-varying panelist demographics (added April 2025) |
| `standard_nmr_feed_static_table` | Projection weights for a given 12-month static period |
| `standard_nmr_feed_people_attributes_table` | Psychographic and behavioral attribute tags per panelist |
| `standard_nmr_feed_validation_table` | Data ingestion validation checks |

```{note}
`summarylvl_fact_table` contains more trips than `itemlvl_fact_table` because it includes trips where only basket totals (not individual items) were captured. Use `itemlvl_fact_table` for category-level or product-level analysis. Use `summarylvl_fact_table` for total spending, trip frequency, or retailer-level analysis where the larger panel coverage matters more than item detail.
```

Click a table name below to expand its field definitions.

:::{dropdown} Item Level Fact Table — `standard_nmr_feed_itemlvl_fact_table`

| Field | Type | Description |
|---|---|---|
| `BASKET_ID` | INTEGER | Unique trip identifier |
| `USER_ID` | INTEGER | Panelist identifier (join to People table) |
| `BANNER_ID` | VARCHAR | Store banner (join to Banner table) |
| `ITEM_ID` | INTEGER | Product identifier (join to Item table) |
| `ITEM_QUANTITY` | INTEGER | Count of this item on the transaction line |
| `ITEM_UNIT_PRICE` | INTEGER | Unit price in local currency |
| `ITEM_TOTAL` | NUMERIC(15,2) | Total dollars for this item on the transaction line |
| `BASKET_SUB_TOTAL` | NUMERIC(15,2) | Basket sub-total pre-tax |
| `BASKET_TOTAL` | NUMERIC(15,2) | Basket total as listed on receipt |
| `BASKET_QUANTITY` | INTEGER | Total number of items in the basket |
| `TRANSACTION_DATE` | DATE | Date of the transaction |
| `SUBSCRIPTION_TYPE` | VARCHAR | Subscription type (Amazon Subscribe & Save or other) |
| `SOLD_BY` | VARCHAR | For ecommerce baskets: name of 1P/3P seller |
| `TREND_FACTOR` | NUMERIC | Trend adjustment factor (part of projection factors) |
| `ER_FACTOR` | NUMERIC | Early read trend adjustment factor (part of projection factors) |
:::

:::{dropdown} Summary Level Fact Table — `standard_nmr_feed_summarylvl_fact_table`

| Field | Type | Description |
|---|---|---|
| `BASKET_ID` | INTEGER | Unique trip identifier |
| `USER_ID` | INTEGER | Panelist identifier (join to People table) |
| `BANNER_ID` | VARCHAR | Store banner (join to Banner table) |
| `BASKET_SUB_TOTAL` | NUMERIC | Basket sub-total pre-tax |
| `BASKET_TOTAL` | NUMERIC | Basket total as listed on receipt |
| `BASKET_QUANTITY` | NUMERIC | Total number of items in the basket |
| `BASKET_SALESTAX` | NUMERIC | Sales tax as listed on receipt (where available) |
| `BASKET_ADJUSTED_SUBTOTAL` | NUMERIC | Pre-tax sub-total adjusted for missing/invalid data; use for basket projections |
| `TRANSCRIBED` | BOOLEAN | True if full item-level transcription is available for this trip |
| `TRANSACTION_DATE` | DATE | Date of the transaction |
| `TRANSACTION_DT_LOCAL` | TIMESTAMP | Date and time of transaction (where available) |
| `STORE_ID` | NUMERIC | Internal store ID (where available) |
| `STORE_NAME` | VARCHAR | Store name (where available) |
| `STORE_ADDRESS` | VARCHAR | Store address (where available) |
| `STORE_CITY` | VARCHAR | Store city (where available) |
| `STORE_POSTAL_CODE` | VARCHAR | Store postal code (where available) |
| `STORE_PHONE_NO` | VARCHAR | Store phone number (where available) |
| `STORE_NUMBER` | VARCHAR | Retailer-specific store number from receipt (where available) |
| `STORE_LONGITUDE` | NUMERIC | Longitude of store (where available) |
| `STORE_LATITUDE` | NUMERIC | Latitude of store (where available) |
| `ORDER_METHOD_TYPE` | VARCHAR | Where order was placed: `IN_STORE` or `ONLINE` |
| `ORDER_PROVIDER` | VARCHAR | Restaurant/QSR name for online food delivery orders |
| `DELIVERY_METHOD_TYPE` | VARCHAR | Where order was delivered: `IN_STORE`, `SHIPPING`, or `DOWNLOAD` |
| `DELIVERY_PROVIDER` | VARCHAR | Delivery provider name (e.g., Instacart) |
| `ORDER_DELIVERY_TYPE` | VARCHAR | Trip type based on order/delivery method combination |
| `DAY_PART` | VARCHAR | Time of day of the trip |
| `PAYMENT_METHOD` | VARCHAR | Presumed tender method |
| `WIC_USED` | VARCHAR | WIC benefits used on trip |
| `SNAP_USED` | VARCHAR | SNAP benefits used on trip |
| `BENEFITS_USED` | VARCHAR | SNAP, WIC, or both used on trip |
| `GAS_ONLY` | BOOLEAN | True if trip was gas only |
| `BASKET_TREND_FACTOR` | NUMERIC | Basket-level trend adjustment factor |
| `BASKET_ER_FACTOR` | NUMERIC | Basket-level early read trend adjustment factor |
:::

:::{dropdown} Banner Table — `standard_nmr_feed_banner_table`

```{tip}
Use `RETAILER_ID`, `CHANNEL_ID`, and `PARENT_CHANNEL_ID` rather than the description fields when writing code — the ID fields are stable across updates, whereas description strings can change.
```

| Field | Type | Description |
|---|---|---|
| `BANNER_ID` | VARCHAR | Store banner ID (e.g., `krogercom`) — join to Fact tables |
| `BANNER` | VARCHAR | Store banner description (e.g., `Kroger.com`) |
| `RETAILER_ID` | VARCHAR | Retailer ID (e.g., `kroger`) — stable key |
| `RETAILER` | VARCHAR | Retailer description (e.g., `Kroger`) |
| `CHANNEL_ID` | VARCHAR | Channel ID (e.g., `online`) — stable key |
| `CHANNEL` | VARCHAR | Channel description (e.g., `Online`) |
| `PARENT_CHANNEL_ID` | VARCHAR | Parent channel ID (e.g., `ecommerce`) — stable key |
| `PARENT_CHANNEL` | VARCHAR | Parent channel description (e.g., `eCommerce`) |
:::

:::{dropdown} Item Table — `standard_nmr_feed_item_table`

| Field | Type | Description |
|---|---|---|
| `ITEM_ID` | INTEGER | Product identifier (join to Fact tables) |
| `GTIN` | VARCHAR | Global Trade Item Number (standardized to 14 digits) |
| `UPC` | VARCHAR | 12- or 10-digit UPC code as printed on receipt (where available) |
| `RIN` | VARCHAR | Retail Identification Number |
| `BRAND_ID` | VARCHAR | Internal brand ID |
| `BRAND` | VARCHAR | Brand name (e.g., `Crest ProHealth`) |
| `PARENTBRAND_ID` | VARCHAR | Internal parent brand ID |
| `PARENT_BRAND_DESCRIPTION` | VARCHAR | Parent brand name (e.g., `Crest`) |
| `SUBCAT_ID` | VARCHAR | Internal sub-category ID |
| `SUB_CATEGORY_DESCRIPTION` | VARCHAR | Sub-category name (not always available) |
| `CATEGORY_ID` | VARCHAR | Internal category ID |
| `CATEGORY_DESCRIPTION` | VARCHAR | Category name (e.g., `Whitening Toothpaste`) |
| `MAJORCAT_ID` | VARCHAR | Internal major category ID |
| `MAJOR_CATEGORY_DESCRIPTION` | VARCHAR | Major category name (e.g., `Toothpaste`) |
| `DEPT_ID` | VARCHAR | Internal department ID |
| `DEPARTMENT_DESCRIPTION` | VARCHAR | Department name (e.g., `Oral Care`) |
| `SECTOR_ID` | VARCHAR | Internal sector ID |
| `SECTOR_DESCRIPTION` | VARCHAR | Sector name (e.g., `Health and Beauty`) |
| `MANUFACTURER_ID` | VARCHAR | Internal manufacturer ID |
| `MANUFACTURER_DESCRIPTION` | VARCHAR | Manufacturer name (e.g., `Procter & Gamble`) |
| `ITEM_DESCRIPTION` | VARCHAR | Best available item description (receipt, online, or normalized) |
| `RECEIPT_SHORT_DESCRIPTION` | VARCHAR | Full description as printed on receipt |
| `FIRST_OBSERVATION_DATE` | DATE | Date this item (RIN/GTIN combination) was first observed |
:::

:::{dropdown} People Table — `standard_nmr_feed_people_table`

Current snapshot of panelist demographics. For time-varying demographics, use the People History table.

| Field | Type | Description |
|---|---|---|
| `USER_ID` | INTEGER | Panelist identifier (join to Fact tables) |
| `GENDER_APP_USER` | VARCHAR | User-reported gender |
| `AGE_BUCKET` | VARCHAR | User-reported age bucket |
| `POSTAL_CODE` | VARCHAR | User-reported home postal code |
| `METRO_AREA` | VARCHAR | Metropolitan area name |
| `CENSUS_DIVISION_NAME` | VARCHAR | US Census division |
| `CENSUS_REGION_NAME` | VARCHAR | US Census region |
| `HOUSE_HOLD_SIZE` | VARCHAR | Household size |
| `MARITAL_STATUS` | VARCHAR | Marital status |
| `HAS_CHILDREN` | VARCHAR | Whether children are present in household |
| `HAS_CHILDREN_AGES_0_5` | VARCHAR | Child present aged 0–5 |
| `HAS_CHILDREN_AGES_6_12` | VARCHAR | Child present aged 6–12 |
| `HAS_CHILDREN_AGES_13_17` | VARCHAR | Child present aged 13–17 |
| `EDUCATION_GROUP` | VARCHAR | Education level (short) |
| `EDUCATION_DESCRIPTION` | VARCHAR | Education level (detailed) |
| `EMPLOYMENT` | VARCHAR | Employment status |
| `INCOME_BUCKET` | VARCHAR | Household income (short, e.g., `low`) |
| `INCOME_BUCKET_LONG` | VARCHAR | Household income (detailed, e.g., `$20,000–$29,999`) |
| `ETHNICITY` | VARCHAR | Ethnicity |
| `IS_US_BORN` | VARCHAR | Born in US flag |
| `IS_LATINO` | VARCHAR | Latino heritage flag |
| `MCU` | INTEGER | Months of consecutive upload activity (any transaction) |
| `PRIME_MEMBERSHIP_TYPE` | VARCHAR | Amazon Prime membership status |
| `WALMART_PLUS_MEMBERSHIP` | VARCHAR | Walmart+ membership status (added August 2025) |
:::

:::{dropdown} People History Table — `standard_nmr_feed_people_history_table`

Added April 2025. Tracks how each panelist's demographics changed over time. Join to `static_table` via `USER_SK`.

| Field | Type | Description |
|---|---|---|
| `USER_ID` | INTEGER | Panelist identifier |
| `USER_SK` | VARCHAR | Unique demographic-user key for the time period (join to Static table) |
| `FROM_DATE` | DATE | Start of the demographic time period |
| `UNTIL_DATE` | DATE | End of the demographic time period |
| `GENDER_APP_USER` | VARCHAR | User-reported gender |
| `AGE_BUCKET` | VARCHAR | User-reported age bucket |
| `POSTAL_CODE` | VARCHAR | Home postal code |
| `METRO_AREA` | VARCHAR | Metropolitan area name |
| `CENSUS_DIVISION_NAME` | VARCHAR | US Census division |
| `CENSUS_REGION_NAME` | VARCHAR | US Census region |
| `HOUSE_HOLD_SIZE` | VARCHAR | Household size |
| `MARITAL_STATUS` | VARCHAR | Marital status |
| `HAS_CHILDREN` | VARCHAR | Child present flag |
| `HAS_CHILDREN_AGES_0_5` | VARCHAR | Child present aged 0–5 |
| `HAS_CHILDREN_AGES_6_12` | VARCHAR | Child present aged 6–12 |
| `HAS_CHILDREN_AGES_13_17` | VARCHAR | Child present aged 13–17 |
| `EDUCATION_GROUP` | VARCHAR | Education level (short) |
| `EDUCATION_DESCRIPTION` | VARCHAR | Education level (detailed) |
| `EMPLOYMENT` | VARCHAR | Employment status |
| `INCOME_BUCKET` | VARCHAR | Household income (short) |
| `INCOME_BUCKET_LONG` | VARCHAR | Household income (detailed) |
| `ETHNICITY` | VARCHAR | Ethnicity |
| `IS_US_BORN` | VARCHAR | Born in US flag |
| `IS_LATINO` | VARCHAR | Latino heritage flag |
:::

:::{dropdown} Static Table — `standard_nmr_feed_static_table`

Contains projection weights for 12-month static periods. Use `USER_SK` to join to People History.

| Field | Type | Description |
|---|---|---|
| `START_DATE` | DATE | Start of the 12-month static period |
| `END_DATE` | DATE | End of the 12-month static period |
| `USER_ID` | INTEGER | Panelist identifier |
| `USER_SK` | VARCHAR | Unique demographic-user key (join to People History table) |
| `DEMO_WEIGHT` | NUMERIC(38,0) | Demographic weight (part of projection factors) |
| `NATIONAL_FACTOR` | NUMERIC(38,6) | National scale-up factor (part of projection factors) |
:::

:::{dropdown} People Attributes Table — `standard_nmr_feed_people_attributes_table`

Psychographic and behavioral attributes organized in a five-level hierarchy: **Theme → Subtheme → Topic → Header → Tag**. Each row is a tag applied to a panelist.

| Field | Type | Description |
|---|---|---|
| `USER_ID` | INTEGER | Panelist identifier (join to Fact tables) |
| `THEME_ID` | INTEGER | Top-level classification ID |
| `THEME_DESCRIPTION` | VARCHAR | Top-level classification (e.g., `Psychographics`) |
| `SUBTHEME_ID` | INTEGER | Second-level classification ID |
| `SUBTHEME_DESCRIPTION` | VARCHAR | Second-level classification |
| `TOPIC_ID` | INTEGER | Third-level classification ID |
| `TOPIC_DESCRIPTION` | VARCHAR | Third-level classification |
| `HEADER_ID` | INTEGER | Fourth-level classification ID |
| `HEADER_DESCRIPTION` | VARCHAR | Fourth-level classification |
| `TAG_ID` | INTEGER | Leaf-level attribute ID |
| `TAG_DESCRIPTION` | VARCHAR | Leaf-level attribute description |
| `TAG_DATE` | DATE | Date the tag was applied |
:::

```{seealso}
For migrating Athena/v1.x queries to this schema — including BATCH_DATE deduplication and a worked example — see the [Legacy Schema & Query Migration](#migration) section below.
```

(migration)=
## Legacy Schema & Query Migration

:::{dropdown} BATCH_DATE Deduplication — Athena & Redivis v1.x

Both the original Athena tables and Redivis v1.x used a `BATCH_DATE` column to tag which quarterly delivery each row came from. Because each delivery was a full re-delivery of the historical record, **the same purchase appears multiple times** in the table — once per batch. A purchase from January 2024 appears in the 2024-10-21 batch, the 2025-01-17 batch, and any later batch, with corrections applied in each successive delivery.

The correct deduplication strategy is to **keep only the most recent batch's copy of each row**, identified by the record's natural key:

- **Fact table:** natural key is `BASKET_ID` + `ITEM_ID`
- **Lookup tables (banner, item, people, static):** natural key is the table's primary identifier (e.g., `BANNER_ID`, `ITEM_ID`, `USER_ID`)

**Recommended deduplication pattern:**

```sql
-- Deduplicate Athena / v1.x fact table: keep the most recently delivered copy of each row
WITH deduped AS (
    SELECT
        *,
        ROW_NUMBER() OVER (
            PARTITION BY BASKET_ID, ITEM_ID
            ORDER BY BATCH_DATE DESC
        ) AS rn
    FROM standard_nmr_feed_fact_table
)
SELECT * EXCEPT (rn)
FROM deduped
WHERE rn = 1;
```

**Do not** use `WHERE BATCH_DATE = (SELECT MAX(BATCH_DATE) FROM ...)` as a shortcut — that drops all records from earlier quarters that were not re-delivered in the latest batch, leaving only a single quarter of data.

The same pattern applies to all lookup tables, e.g.:

```sql
WITH deduped_banner AS (
    SELECT *, ROW_NUMBER() OVER (
        PARTITION BY BANNER_ID ORDER BY BATCH_DATE DESC
    ) AS rn
    FROM standard_nmr_feed_banner_table
)
SELECT * EXCEPT (rn)
FROM deduped_banner
WHERE rn = 1;
```
:::

:::{dropdown} Migrating Queries to the September 2025 Schema

The September 2025 restructure split `standard_nmr_feed_fact_table` into two tables. Which replacement you use depends on what your query does:

| If your original query… | Use |
|---|---|
| Joins on `ITEM_ID`, uses `ITEM_TOTAL`, or filters on product category | `itemlvl_fact_table` |
| Counts trips, sums `BASKET_TOTAL`, or groups by retailer/channel | `summarylvl_fact_table` |
| Uses both item detail and full trip coverage | Join both: `summarylvl` for trip universe, then LEFT JOIN `itemlvl` for items |

Several fields also moved: store location fields (`LATITUDE`, `LONGITUDE`, `STORE_POSTAL_CODE`) now live only in `summarylvl_fact_table`, and `BASKET_TREND_FACTOR` / `BASKET_ER_FACTOR` replaced `TREND_FACTOR` / `ER_FACTOR` at the basket level.

**Original query (Athena or Redivis v1.x, with `BATCH_DATE` deduplication):**

```sql
WITH deduped_fact AS (
    SELECT *, ROW_NUMBER() OVER (
        PARTITION BY BASKET_ID, ITEM_ID ORDER BY BATCH_DATE DESC
    ) AS rn
    FROM standard_nmr_feed_fact_table
),
deduped_banner AS (
    SELECT *, ROW_NUMBER() OVER (
        PARTITION BY BANNER_ID ORDER BY BATCH_DATE DESC
    ) AS rn
    FROM standard_nmr_feed_banner_table
),
deduped_item AS (
    SELECT *, ROW_NUMBER() OVER (
        PARTITION BY ITEM_ID ORDER BY BATCH_DATE DESC
    ) AS rn
    FROM standard_nmr_feed_item_table
)
SELECT
    b.CHANNEL,
    DATE_TRUNC('month', f.TRANSACTION_DATE)  AS month,
    COUNT(DISTINCT f.BASKET_ID)              AS trips,
    SUM(f.ITEM_TOTAL)                        AS total_spend
FROM deduped_fact   AS f WHERE f.rn = 1
JOIN deduped_banner AS b ON f.BANNER_ID = b.BANNER_ID AND b.rn = 1
JOIN deduped_item   AS i ON f.ITEM_ID   = i.ITEM_ID   AND i.rn = 1
WHERE i.DEPARTMENT = 'BEVERAGES'
  AND f.TRANSACTION_DATE BETWEEN DATE '2024-01-01' AND DATE '2024-12-31'
GROUP BY 1, 2
ORDER BY 1, 2;
```

**Migrated to Redivis v3.x (new schema, no deduplication needed):**

Because this query filters on `DEPARTMENT` and sums `ITEM_TOTAL`, it maps to `itemlvl_fact_table`. The deduplication CTEs are gone entirely — the only change from Stage 1 is the fact table name:

```sql
SELECT
    b.CHANNEL,
    DATE_TRUNC('month', f.TRANSACTION_DATE)  AS month,
    COUNT(DISTINCT f.BASKET_ID)              AS trips,
    SUM(f.ITEM_TOTAL)                        AS total_spend
FROM standard_nmr_feed_itemlvl_fact_table  AS f   -- new table name
JOIN standard_nmr_feed_banner_table        AS b ON f.BANNER_ID = b.BANNER_ID
JOIN standard_nmr_feed_item_table          AS i ON f.ITEM_ID   = i.ITEM_ID
WHERE i.DEPARTMENT = 'BEVERAGES'
  AND f.TRANSACTION_DATE BETWEEN DATE '2024-01-01' AND DATE '2024-12-31'
GROUP BY 1, 2
ORDER BY 1, 2;
```

`itemlvl_fact_table` covers only fully transcribed trips. For total channel spend across all trips, use `summarylvl_fact_table` and `BASKET_ADJUSTED_SUBTOTAL` — but note you lose the ability to filter by product category.
:::

:::{dropdown} Pre-September 2025 Schema — Fact Table (`standard_nmr_feed_fact_table`)

- Data Dictionary — Pre-September 2025 (August 2025 version, XLSX): contact [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) to request access.

This single table contained both item-level and basket-level data. It was replaced by `itemlvl_fact_table` and `summarylvl_fact_table` in the September 2025 restructure.

| Field | Type | Description |
|---|---|---|
| `BASKET_ID` | INTEGER | Unique trip identifier |
| `USER_ID` | INTEGER | Panelist identifier |
| `BANNER_ID` | VARCHAR | Store banner (join to Banner table) |
| `ITEM_ID` | INTEGER | Product identifier (join to Item table) |
| `ITEM_QUANTITY` | INTEGER | Count of this item on the transaction line |
| `ITEM_UNIT_PRICE` | INTEGER | Unit price in local currency |
| `ITEM_TOTAL` | NUMERIC(15,2) | Total dollars for this item |
| `BASKET_SUB_TOTAL` | NUMERIC(15,2) | Basket sub-total pre-tax |
| `BASKET_TOTAL` | NUMERIC(15,2) | Basket total as listed on receipt |
| `STORE_NUMBER` | VARCHAR | Retailer-specific store number (where available) |
| `TRANSACTION_DATE` | DATE | Date of the transaction |
| `BASKET_QUANTITY` | INTEGER | Total number of items in the basket |
| `TRANSACTION_DT_LOCAL` | TIMESTAMP | Date and time of transaction (where available) |
| `TREND_FACTOR` | NUMERIC | Trend adjustment factor |
| `LONGITUDE` | NUMERIC | Store longitude (where available) |
| `LATITUDE` | NUMERIC | Store latitude (where available) |
| `SUBSCRIPTION_TYPE` | VARCHAR | Subscription type |
| `ORDER_METHOD_TYPE` | VARCHAR | `IN_STORE` or `ONLINE` |
| `ORDER_PROVIDER` | VARCHAR | Restaurant/QSR for online food delivery |
| `DELIVERY_METHOD_TYPE` | VARCHAR | `IN_STORE`, `SHIPPING`, or `DOWNLOAD` |
| `DELIVERY_PROVIDER` | VARCHAR | Delivery provider name |
| `SOLD_BY` | VARCHAR | 1P/3P seller name for ecommerce |
| `CLICK_AND_COLLECT` | BOOLEAN | Order online, pick up in store |
| `DAY_PART` | VARCHAR | Time of day of the trip |
| `STORE_POSTAL_CODE` | VARCHAR | Store postal code (where available) |
| `WIC_USED` | VARCHAR | WIC benefits used |
| `SNAP_USED` | VARCHAR | SNAP benefits used |
| `BENEFITS_USED` | VARCHAR | SNAP, WIC, or both used |
| `PAYMENT_METHOD` | VARCHAR | Presumed tender method *(added July 2025)* |
| `ER_FACTOR` | NUMERIC | Early read trend adjustment factor *(added August 2025)* |
| `BATCH_DATE` | DATE | Delivery batch date — **required for deduplication** |
:::

:::{dropdown} Pre-September 2025 Schema — Banner Table (`standard_nmr_feed_banner_table`)

The September 2025 update added `RETAILER_ID`, `CHANNEL_ID`, and `PARENT_CHANNEL_ID` stable key fields. The pre-September 2025 version had only the description fields below.

| Field | Type | Description |
|---|---|---|
| `BANNER_ID` | VARCHAR | Store banner ID (join to Fact table) |
| `BANNER` | VARCHAR | Store banner name |
| `RETAILER` | VARCHAR | Retailer name |
| `CHANNEL` | VARCHAR | Channel name |
| `PARENT_CHANNEL` | VARCHAR | Parent channel name |
| `BATCH_DATE` | DATE | Delivery batch date — **required for deduplication** |
:::
