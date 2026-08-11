# ProxyCurl

## At a Glance

| | |
|---|---|
| **Provider** | ProxyCurl |
| **Coverage** | Snapshot |
| **Geographic scope** | Global |
| **Update frequency** | TBD |
| **Access platforms** | Redivis, KLC |
| **Eligible users** | Northwestern community |
| **Questions** | [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) |

## Description

ProxyCurl's **Person Profile Data** is a snapshot of approximately 170 million public LinkedIn profiles. Each record includes:

- **Identifying information**: name, headline, location, occupation, and summary
- **Work history**: companies, titles, dates, and descriptions
- **Education**: schools, degrees, fields of study, and dates
- **Accomplishments**: certifications, patents, publications, courses, projects, honors/awards, and test scores
- **Network data**: connections count, follower count, and related profiles
- **Other content**: languages, group memberships, articles, volunteer work, recommendations, and activities

## Access

Access is restricted to members of the Northwestern University community. Please email [Kellogg Research Support](mailto:rs@kellogg.northwestern.edu) to obtain access.

ProxyCurl data can be found on [Redivis](https://redivis.com/datasets/3dny-9zgev30ag) as well as on KLC at `/kellogg/data/proxycurl/proxycurl.duckdb`.

## Data Coverage & Key Identifiers

| Attribute | Value |
|---|---|
| **Time period** | Snapshot |
| **Geographic coverage** | Global |
| **Unit of observation** | LinkedIn profile |
| **Primary identifier** | `id` (profile table); `profile_id` (all other tables) |
| **Commonly linked via** | `profile_id` |
| **Key variables** | Name, headline, occupation, location, employment history, education, certifications, accomplishments, connections, follower count |

## Database Details

Below is a summary of the table names and columns for the ProxyCurl dataset.

| Table Name | Columns |
|-----------|---------|
| profile | profile_pic_url, city, country, first_name, full_name, headline, last_name, state, summary, background_cover_image_url, birth_date, connections, country_full_name, occupation, follower_count, id |
| profile_education | starts_at, ends_at, field_of_study, degree_name, school, school_profile_url, profile_id, description, logo_url, grade, activities_and_societies |
| profile_course | name, number, profile_id |
| profile_honour_award | title, issuer, issued_on, description, profile_id |
| profile_recommendation | content, profile_id |
| profile_test_score | name, score, date_on, description, profile_id |
| profile_certification | starts_at, ends_at, url, name, license_number, display_source, authority, profile_id |
| profile_organization | starts_at, ends_at, name, title, description, profile_id |
| profile_patent | title, description, url, issued_on, issuer, patent_number, profile_id, application_number |
| profile_article | title, link, published_date, author, image_url, profile_id |
| profile_activity | title, link, activity_status, profile_id |
| profile_publication | name, publisher, published_on, description, url, profile_id |
| profile_people_also_viewed | link, name, summary, location, profile_id |
| profile_group | profile_pic_url, name, url, profile_id |
| profile_volunteering_experience | starts_at, ends_at, cause, company, company_profile_url, title, profile_id, company_urn, description, logo_url |
| profile_experience | starts_at, ends_at, company, company_profile_url, title, location, profile_id, description, company_urn, logo_url, company_id |
| profile_project | title, description, url, profile_id, ends_at, starts_at |
| profile_language | name, profile_id |
| profile_similar_named | link, name, summary, location, profile_id |

### Profile Table Column Descriptions

The following table describes the columns in the `profile` table. Date sub-fields (`starts_at`, `ends_at`, etc.) in other tables are stored as structured objects with `day`, `month`, and `year` components.

| Column | Description |
|---|---|
| `id` | Vanity identifier of the public LinkedIn profile (the slug after `/in/` in the profile URL). |
| `first_name` | First name of the user. |
| `last_name` | Last name of the user. |
| `full_name` | Full name of the user (first name + last name combined). |
| `headline` | Tagline written by the user for their profile. |
| `occupation` | Title and company name of the user's current employment. |
| `summary` | Longer biographical blurb written by the user for their profile. |
| `city` | City where the user lives. |
| `state` | State where the user lives. |
| `country` | Country of residence as a 2-letter ISO 3166-1 alpha-2 code (e.g., `US`). |
| `country_full_name` | Country of residence in English (e.g., `United States of America`). |
| `connections` | Total count of LinkedIn connections. |
| `follower_count` | Follower count for this profile. |
| `profile_pic_url` | URL of the user's profile picture. |
| `background_cover_image_url` | URL of the user's background cover image. |
| `birth_date` | Date of birth of the user. |

You can also find further details about these columns in the [data feed descriptions](https://nuwildcat.sharepoint.com/:f:/s/KSM-RSDataDocumentation/Eo8pOuQJCEFGsqGO8ko8pUIBUB-LIrBydai5NjvHvOIp2A?e=KC9tBm).

:::{note}
When performing JOINs in SQL, use `profile_id` for all tables except the `profile` table. For the `profile` table, the JOIN key is the column `id`.
:::

## Example Queries

Below are examples of how to query the ProxyCurl dataset using the Redivis API or using DuckDB while on KLC with a local copy of the dataset.

### Redivis API

```python
import redivis
from urllib.parse import unquote
import html
import pandas as pd

# If you do not have a Redivis API Token (https://docs.redivis.com/api/rest-api/authorization#api-token)
# then when you run this line, you will be asked to authenticate to allow the Python API to work
# the authentication will last for a few hours before it will ask you to authenticate again.
organization = redivis.organization("Northwestern")

# Specify which dataset we are using
dataset = organization.dataset("ProxyCurl:3dny")

# Execute your Redivis query
query = dataset.query("""
SELECT
    p.id AS profile_id,
    p.first_name,
    p.last_name,
    p.headline,
    p.city,
    p.country,
    p.profile_pic_url,
    -- Latest education info
    e.school,
    e.degree_name,
    e.field_of_study,
    e.starts_at AS education_start,
    e.ends_at AS education_end,
    -- Latest experience info
    exp.company AS current_company,
    exp.title AS current_title,
    exp.starts_at AS experience_start,
    exp.ends_at AS experience_end,
    -- Certifications
    c.name AS certification_name,
    c.authority AS certification_authority,
    c.starts_at AS certification_start,
    c.ends_at AS certification_end
FROM profile AS p
LEFT JOIN profile_education AS e
    ON p.id = e.profile_id
LEFT JOIN profile_experience AS exp
    ON p.id = exp.profile_id
LEFT JOIN profile_certification AS c
    ON p.id = c.profile_id
WHERE p.country = 'US'
ORDER BY p.last_name, p.first_name
LIMIT 100
""")

# Convert to pandas DataFrame
df = query.to_pandas_dataframe()

# Automatically decode URL-encoded and HTML-encoded strings for relevant columns
string_cols = df.select_dtypes(include='object').columns

# Decode all string columns
for col in string_cols:
    df[col] = df[col].apply(lambda x: html.unescape(unquote(x)) if pd.notnull(x) else x)

# Inspect results
print(df)
```

### DuckDB with Local KLC Data

A version of the ProxyCurl data exists on KLC in DuckDB format at:

```
/kellogg/data/proxycurl/proxycurl.duckdb
```

```python
import duckdb

# Connect to the local ProxyCurl DuckDB
con = duckdb.connect("/kellogg/data/proxycurl/proxycurl.duckdb")


# A DuckDB query that finds all the unique combinations of
#     - company
#     - company_profile_url
#     - company_urn
#     - company_id
 
# that occur any time the lowercase version of the company name has the substring "merck" in it.


query = f"""
SET threads to 16;
SELECT DISTINCT company, company_id, company_urn, company_profile_url
FROM profile_experience
WHERE lower(company) LIKE '%merck%'
"""
```
