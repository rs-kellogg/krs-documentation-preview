(web-of-science)=
# Web of Science

## At a Glance

| | |
|---|---|
| **Provider** | Clarivate |
| **Coverage** | Varies by collection (see [Data Coverage](web-of-science-coverage)) |
| **Geographic scope** | Global |
| **Update frequency** | Continuous on the library web interface; 2025 extract on KLC |
| **KLC database** | `/kellogg/data/WOS/2025/db/wos2025.db` (`papers`, `paper_references`) |
| **Access platforms** | Northwestern Library (web), KLC (DuckDB) |
| **Eligible users** | Northwestern community (web); limited researchers (KLC) |
| **Questions** | [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) |

## Description

Multidisciplinary coverage of over 10,000 journals in the sciences, social sciences, and arts and humanities, as well as published proceedings for over 12,000 conferences per year, and over 50,000 scholarly books. The library web interface searches the database and lists articles that cite a given work.

On KLC, the 2025 extract is a [DuckDB](https://duckdb.org/) file. `papers` has one row per publication. `paper_references` has one row per cited reference. Query the file on the KLC file system. Start with [Querying with DuckDB on KLC](web-of-science-duckdb).

## Access

The Northwestern Library offers access to the [web interface](http://libguides.northwestern.edu/az.php?q=web%20of%20science).

A limited amount of Web of Science data can be made available to a limited number of academic researchers on KLC. Query the DuckDB file at `/kellogg/data/WOS/2025/db/wos2025.db`. See [How to Access KLC](/services/klc/user-guide/klc-accessing) if you do not have an account. To inquire about this resource, contact [Research Support](mailto:rs@kellogg.northwestern.edu).

(web-of-science-coverage)=
## Data Coverage

| Attribute | Value |
|---|---|
| **Time period** | Varies by collection; Web of Science Core Collection (SCI-E, SSCI) from 1900; AHCI from 1975; ESCI from 2005 |
| **Geographic coverage** | Global |
| **Unit of observation** | Publication in `papers`; cited reference in `paper_references` |
| **Primary identifier** | `uid` — for example, `WOS:001588455800012` |
| **Commonly linked via** | `doi`, `pmid`, `issn`, `eissn`; ORCID (`orcid_id`) and ResearcherID (`r_id`) inside `authors_json` |
| **Key variables** | Title, authors, affiliations, abstract, keywords, cited references, funding agencies, subject categories |

The dates below are Clarivate product coverage. In this file, each paper's edition codes are in `editions`, separated by `|`, and `coll_id` is the collection identifier, for example `WOS`. List the codes with [Editions](web-of-science-editions).

| Collection | Coverage |
|---|---|
| Science Citation Index Expanded (SCI-E) | 1900–present |
| Social Sciences Citation Index (SSCI) | 1900–present |
| Arts & Humanities Citation Index (AHCI) | 1975–present |
| Emerging Sources Citation Index (ESCI) | 2005–present |
| Book Citation Index — Science | 2005–present |
| Book Citation Index — Social Sciences & Humanities | 2005–present |
| MEDLINE | 1950s–present |
| Biological Abstracts / BIOSIS Previews | Varies |
| INSPEC | Varies |
| Derwent Innovations Index | Varies |
| Chinese Science Citation Database (CSCD) | Varies |
| Zoological Record | Varies |

(web-of-science-duckdb)=
## Querying with DuckDB on KLC

DuckDB reads `/kellogg/data/WOS/2025/db/wos2025.db` on the KLC file system. On KLC main, cap every session at 16 threads and 128 GB. Queries that filter, aggregate, or return a short sample stay on KLC main. Read [When to Use KLC Reserve](/services/klc-reserve/when-to-use) when you will load `papers` or `paper_references` into memory.

### Before You Start

- Log in to KLC. See [How to Access KLC](/services/klc/user-guide/klc-accessing) if you do not have an account.
- Create a conda environment under `/kellogg/proj/<your-netid>/`. See [Conda Environments on KLC](/services/klc/user-guide/klc-conda).
- Save extracts under `/kellogg/proj/<your-netid>/wos`. Home directories are 80 GB.
- Send DuckDB spill files to `/scratch/$USER/duckdb_tmp`. The connection snippet sets that path from the `USER` environment variable.

```bash
module load mamba/24.3.0
mamba create -p /kellogg/proj/<your-netid>/envs/wos-duckdb -c conda-forge python-duckdb
source activate /kellogg/proj/<your-netid>/envs/wos-duckdb
mkdir -p /kellogg/proj/<your-netid>/wos /scratch/$USER/duckdb_tmp
```

Replace `<your-netid>` in the environment path and the extract directory.

### Where to Run the Query

KLC main is the default. Check [KLC Node Resources](/services/klc-node-resources) and use a node with at least 128 GB free. A cap of 16 threads stays within the [24-core limit](/services/klc-reserve/when-to-use) on KLC main.

| Query | Where to Run |
|---|---|
| A DuckDB query that filters, aggregates, or returns a limited sample, including `DESCRIBE` and `COUNT(*)` | KLC main, at 16 threads and 128 GB |
| Reading `papers` or `paper_references` in full into pandas, Polars, or R | [When to Use KLC Reserve](/services/klc-reserve/when-to-use) |

### Query Rules

- Set `threads = 16` and `memory_limit = '128GB'` when you connect on KLC main. Raise either value only in a [KLC Reserve](/services/klc-reserve/when-to-use) job that loads either table into memory and requests those resources.
- Name the columns you need.
- Filter and aggregate in DuckDB. Return an aggregate or a small extract on KLC main.
- Split pipe-delimited columns with `string_split` and `unnest`. Those columns are listed in [Database Tables](web-of-science-klc-data).
- Run `SHOW TABLES`, `DESCRIBE papers`, or `DESCRIBE paper_references` to inspect the file. See [Inspect the Database](web-of-science-inspect).

(web-of-science-run-query)=
### Open a Connection

Open the database read-only. Set the cap on every connection, then run every later snippet in that same session.

```python
import os
import duckdb

TEMP_DIRECTORY = f"/scratch/{os.environ['USER']}/duckdb_tmp"

con = duckdb.connect(
    "/kellogg/data/WOS/2025/db/wos2025.db",
    read_only=True,
    config={
        "threads": 16,
        "memory_limit": "128GB",
        "temp_directory": TEMP_DIRECTORY,
        "max_temp_directory_size": "200GB",
    },
)
con.execute("SET preserve_insertion_order = false")
```

| Setting | Controls | KLC Main Value |
|---|---|---|
| `threads` | CPU threads for query execution | `SET threads = 16;` |
| `memory_limit` | Maximum memory DuckDB uses before spilling to disk | `SET memory_limit = '128GB';` |
| `temp_directory` | Where DuckDB writes spill files | `SET temp_directory = '/scratch/<your-netid>/duckdb_tmp';` |
| `max_temp_directory_size` | Cap on total spill-file size | `SET max_temp_directory_size = '200GB';` |
| `preserve_insertion_order` | `false` lowers memory use for large scans | `SET preserve_insertion_order = false;` |

The Python snippet fills `temp_directory` from `USER`. The SQL value above is the same path with your NetID written out.

Confirm the active values in the same session:

```python
df = con.sql("""
    SELECT current_setting('threads') AS threads,
           current_setting('memory_limit') AS memory_limit,
           current_setting('temp_directory') AS temp_directory
""").df()
print(df)
```

| Where You Run | `threads` | `memory_limit` |
|---|---|---|
| KLC main | 16 | `128GB` |
| KLC Reserve | The `--ntasks` value you request | About 90% of the `--mem` value you request |

When a query exceeds `memory_limit`, DuckDB spills to `temp_directory` and keeps running. When the spill would pass `max_temp_directory_size`, raise that cap. Loading the entire table into memory is covered in [When to Use KLC Reserve](/services/klc-reserve/when-to-use). See [High-Memory Jobs](/services/klc-reserve/highmem-jobs) for requests above 128 GB.

```{note}
`memory_limit` applies to DuckDB's own buffers. Converting a result to pandas with `.df()` allocates additional memory outside the limit. Return an aggregate or a small extract on KLC main.
```

```{warning}
Do not read `papers` or `paper_references` into pandas with `SELECT *`. `papers` includes full abstracts, and `paper_references` has one row per cited work. Aggregate, filter, or use `LIMIT` in DuckDB first.
```

Close the session when you are finished: `con.close()`.

### Example Queries

Run these queries in the session from [Open a Connection](web-of-science-run-query). Each snippet returns a small result.

(web-of-science-inspect)=
#### Inspect the Database

`SHOW TABLES` lists every table in the file. `DESCRIBE` lists columns and types. Definitions are in [Database Tables](web-of-science-klc-data).

```python
print(con.sql("SHOW TABLES").df())
print(con.sql("DESCRIBE papers").df())
print(con.sql("DESCRIBE paper_references").df())
```

#### Overview

Count papers, the year range, and the average number of cited references.

```python
df = con.sql("""
    SELECT
        COUNT(*) AS total_papers,
        MIN(pubyear) AS earliest_year,
        MAX(pubyear) AS latest_year,
        ROUND(AVG(reference_count), 1) AS avg_references
    FROM papers
""").df()
print(df)
```

#### Top Journals

Count papers by source title. `source_title` is stored in upper case.

```python
df = con.sql("""
    SELECT
        source_title,
        COUNT(*) AS paper_count
    FROM papers
    WHERE source_title IS NOT NULL
    GROUP BY source_title
    ORDER BY paper_count DESC
    LIMIT 10
""").df()
print(df)
```

#### Papers per Year

Count papers and open-access papers for the latest years. `is_oa` is `Yes` or `No`.

```python
df = con.sql("""
    SELECT
        pubyear,
        COUNT(*) AS papers,
        SUM(CASE WHEN is_oa = 'Yes' THEN 1 ELSE 0 END) AS open_access
    FROM papers
    WHERE pubyear IS NOT NULL
    GROUP BY pubyear
    ORDER BY pubyear DESC
    LIMIT 15
""").df()
print(df)
```

#### Open Access

List every stored `is_oa` value and its share of `papers`.

```python
df = con.sql("""
    SELECT
        is_oa,
        COUNT(*) AS papers,
        ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (), 1) AS pct
    FROM papers
    GROUP BY is_oa
    ORDER BY papers DESC
""").df()
print(df)
```

#### Reprint Countries

Count papers by reprint-author country.

```python
df = con.sql("""
    SELECT
        reprint_country,
        COUNT(*) AS papers
    FROM papers
    WHERE reprint_country IS NOT NULL
    GROUP BY reprint_country
    ORDER BY papers DESC
    LIMIT 10
""").df()
print(df)
```

(web-of-science-subjects)=
#### Subject Categories

`wos_subjects` stores several categories in one string, separated by `|`. Split the field, drop blanks, and count.

```python
df = con.sql("""
    SELECT
        subject,
        COUNT(*) AS papers
    FROM (
        SELECT TRIM(unnest(string_split(wos_subjects, '|'))) AS subject
        FROM papers
        WHERE wos_subjects IS NOT NULL
    )
    WHERE subject != ''
    GROUP BY subject
    ORDER BY papers DESC
    LIMIT 10
""").df()
print(df)
```

#### Recent Papers

Return five recent papers that have an abstract. `LEFT` shortens the title and abstract in the result. `has_abstract` is `Y` or `N`.

```python
df = con.sql("""
    SELECT
        uid,
        pubyear,
        first_author,
        LEFT(title, 80) AS title_snippet,
        LEFT(abstract, 120) AS abstract_snippet
    FROM papers
    WHERE has_abstract = 'Y'
    ORDER BY sortdate DESC
    LIMIT 5
""").df()
print(df)
```

(web-of-science-editions)=
#### Editions

`editions` stores one or more edition codes in a single string, separated by `|`. Split the field the same way as [Subject Categories](web-of-science-subjects).

```python
df = con.sql("""
    SELECT
        edition,
        COUNT(*) AS papers
    FROM (
        SELECT TRIM(unnest(string_split(editions, '|'))) AS edition
        FROM papers
        WHERE editions IS NOT NULL
    )
    WHERE edition != ''
    GROUP BY edition
    ORDER BY papers DESC
""").df()
print(df)
```

(web-of-science-references)=
#### Cited References

Each row of `paper_references` is one bibliography entry. `citing_uid` is the citing paper. `ref_uid` values that start with `WOS:` match `papers.uid`. Replace `WOS:001588455800012` with a `uid` from `papers`.

```python
df = con.sql("""
    SELECT
        r.occurrence_order,
        r.ref_uid,
        r.cited_author,
        r.year,
        r.cited_work,
        LEFT(r.cited_title, 80) AS title_snippet,
        cited.uid IS NOT NULL AS matched_in_papers
    FROM paper_references AS r
    LEFT JOIN papers AS cited
      ON r.ref_uid = cited.uid
    WHERE r.citing_uid = 'WOS:001588455800012'
    ORDER BY TRY_CAST(r.occurrence_order AS INTEGER)
""").df()
print(df)
```

(web-of-science-authors)=
#### Authors

`authors_json` is a JSON array of author objects. Unnest one paper at a time. `addr_no` matches `addresses_json`, and `reprint` is `Y` for the reprint author. ORCID is `orcid_id`. ResearcherID is `r_id`. Replace the `uid` below.

```python
df = con.sql("""
    SELECT
        p.uid,
        author.seq_no,
        author.display_name,
        author.orcid_id,
        author.r_id,
        author.reprint,
        author.addr_no
    FROM (
        SELECT uid, authors_json
        FROM papers
        WHERE uid = 'WOS:001588455800012'
          AND authors_json IS NOT NULL
    ) AS p,
    UNNEST(from_json(
        p.authors_json,
        '[
            {"seq_no":"VARCHAR","display_name":"VARCHAR","full_name":"VARCHAR",
             "wos_standard":"VARCHAR","first_name":"VARCHAR","last_name":"VARCHAR",
             "r_id":"VARCHAR","orcid_id":"VARCHAR","reprint":"VARCHAR","addr_no":"VARCHAR"}
        ]'
    )) AS t(author)
    ORDER BY TRY_CAST(author.seq_no AS INTEGER)
""").df()
print(df)
```

Unnest `addresses_json` with the same `from_json` pattern. Field lists for both JSON columns are under [Papers](web-of-science-fields). `organizations` is semicolon-delimited.

(web-of-science-klc-data)=
## Database Tables

The 2025 extract is one DuckDB file at `/kellogg/data/WOS/2025/db/wos2025.db`. Open it read-only, as in [Open a Connection](web-of-science-run-query).

| Table | One Row Is |
|---|---|
| `papers` | One publication |
| `paper_references` | One cited reference. A paper with 40 references contributes 40 rows |

`paper_references.citing_uid` is the citing paper. `ref_uid` values that start with `WOS:` match `papers.uid`. See [Cited References](web-of-science-references).

These columns store several values in one string, separated by `|`: `editions`, `doctypes`, `normalized_doctypes`, `keywords`, `keywords_plus`, `wos_headings`, `wos_subheadings`, `wos_subjects`, `fund_agencies`, `oa_types`, and `sdg_categories`. Split them as in [Subject Categories](web-of-science-subjects). `authors_display` and `organizations` inside `addresses_json` are semicolon-delimited. `source_title` is upper case.

Column types are `string` or `int32`. JSON columns are text. Open **Authors and Affiliations** for the author and affiliation fields. The reference-table fields are below.

(web-of-science-fields)=
### Papers (`papers`)

::::{dropdown} Identifiers

| Column | Type | Description |
|---|---|---|
| `uid` | string | Web of Science unique identifier, for example `WOS:001588455800012` |
| `accession_no` | string | Web of Science accession number |
| `doi` | string | Digital Object Identifier |
| `issn` | string | Print ISSN |
| `eissn` | string | Electronic ISSN |
| `pmid` | string | PubMed ID |
| `art_no` | string | Article number, for example `ARTN e44882` |
| `bib_id` | string | Bibliographic citation string |
| `coll_id` | string | Collection identifier, for example `WOS` |
| `editions` | string | Pipe-delimited edition codes, for example `WOS.SCI` and `WOS.SSCI` |
| `source_file` | string | Name of the source XML.gz file this record came from |

::::

::::{dropdown} Publication and Source

| Column | Type | Description |
|---|---|---|
| `sortdate` | string | ISO sort date, for example `2025-10-03` |
| `pubyear` | string | Publication year |
| `pubmonth` | string | Publication month or date string |
| `coverdate` | string | Cover date as printed |
| `pubtype` | string | Publication type, for example `Journal`, `Book`, or `Conference` |
| `vol` | string | Volume |
| `issue` | string | Issue |
| `page_begin` | string | First page |
| `page_end` | string | Last page |
| `page_count` | string | Number of pages |
| `pages` | string | Page range, for example `123-145` |
| `bib_pagecount` | string | Total page count in the issue |
| `title` | string | Article title |
| `source_title` | string | Journal or book title, stored in upper case |
| `source_abbrev` | string | Source abbreviation |
| `source_abbrev_iso` | string | ISO source abbreviation |
| `doctypes` | string | Pipe-delimited document types, for example `Article` |
| `normalized_doctypes` | string | Pipe-delimited normalized document types |
| `publisher` | string | Publisher name |
| `publisher_city` | string | Publisher city |
| `language` | string | Primary language of the article |

::::

::::{dropdown} Authors and Affiliations

| Column | Type | Description |
|---|---|---|
| `author_count` | int32 | Number of authors |
| `authors_display` | string | Semicolon-delimited display names |
| `first_author` | string | Display name of the first author |
| `authors_json` | string | JSON array of author objects. See [Authors](web-of-science-authors) |
| `addresses_json` | string | JSON array of affiliation objects |
| `reprint_address` | string | Full reprint author address |
| `reprint_city` | string | Reprint address city |
| `reprint_country` | string | Reprint address country |

`authors_json` has one object per author. `addr_no` matches `addresses_json`. `reprint` is `Y` for the reprint author.

| Field | Description |
|---|---|
| `seq_no` | Position in the author list, stored as text |
| `display_name` | Name as displayed, for example `Smith, John` |
| `full_name` | Fuller form, for example `Smith, John A` |
| `wos_standard` | Web of Science standard name, for example `Smith, JA` |
| `first_name` | Given name |
| `last_name` | Family name |
| `r_id` | ResearcherID |
| `orcid_id` | ORCID |
| `reprint` | `Y` for the reprint author |
| `addr_no` | Matches `addr_no` in `addresses_json` |

`addresses_json` has one object per affiliation. `organizations` is semicolon-delimited.

| Field | Description |
|---|---|
| `addr_no` | Address number. Matches `authors_json` |
| `full_address` | Full affiliation string |
| `city` | City |
| `country` | Country |
| `zip` | Postal code |
| `organizations` | Semicolon-delimited organization names |
| `suborganizations` | Department or similar unit |

::::

::::{dropdown} Text, Subjects, and Funding

| Column | Type | Description |
|---|---|---|
| `has_abstract` | string | `Y` or `N` |
| `abstract` | string | Full abstract text |
| `keywords` | string | Pipe-delimited author-supplied keywords |
| `keywords_plus` | string | Pipe-delimited KeyWords Plus terms |
| `wos_headings` | string | Pipe-delimited major subject headings |
| `wos_subheadings` | string | Pipe-delimited subject subheadings |
| `wos_subjects` | string | Pipe-delimited subject categories |
| `citation_topics_json` | string | JSON array of citation topic objects at the macro, meso, and micro levels |
| `sdg_categories` | string | Pipe-delimited UN Sustainable Development Goal categories |
| `fund_agencies` | string | Pipe-delimited funding agency names |
| `reference_count` | int32 | Number of references in the bibliography |
| `is_oa` | string | Open-access flag: `Yes` or `No` |
| `oa_types` | string | Pipe-delimited open-access routes, for example `gold` and `green_submitted` |

::::

### Reference Table (`paper_references`)

| Column | Type | Description |
|---|---|---|
| `citing_uid` | string | `uid` of the citing paper. Foreign key to `papers.uid` |
| `occurrence_order` | string | Order of the reference in the bibliography |
| `ref_uid` | string | `uid` of the cited paper, or a non-Web of Science stub ID |
| `cited_author` | string | First author of the cited work |
| `year` | string | Publication year of the cited work |
| `volume` | string | Volume |
| `issue` | string | Issue |
| `page` | string | Starting page |
| `cited_title` | string | Title of the cited work |
| `cited_work` | string | Journal or source title of the cited work |
| `doi` | string | DOI of the cited work |
| `pmid` | string | PubMed ID of the cited work |
| `issn` | string | ISSN of the cited journal |
| `eissn` | string | Electronic ISSN of the cited journal |
| `physical_sections_json` | string | JSON array of in-text citation locations |
| `source_file` | string | Name of the source XML.gz file |

`physical_sections_json` has one object per in-text citation of that reference. Unnest it with `from_json` the same way as [Authors](web-of-science-authors).

| Field | Description |
|---|---|
| `location` | Position indicator, for example `0.11` |
| `section` | Section name, for example `Introduction` |
| `function` | Rhetorical role, for example `background` |
| `text` | Section heading text |

## Related Documentation

- [How to Access KLC](/services/klc/user-guide/klc-accessing): request an account and log in
- [Conda Environments on KLC](/services/klc/user-guide/klc-conda): create the DuckDB environment under `/kellogg/proj/`
- [KLC Node Resources](/services/klc-node-resources): live CPU and RAM availability
- [When to Use KLC Reserve](/services/klc-reserve/when-to-use): choose a Reserve job when `papers` or `paper_references` must be loaded into memory
- [High-Memory Jobs](/services/klc-reserve/highmem-jobs): Reserve jobs that need more than 128 GB
- [Datasets on KLC](/services/klc/klc-datasets): other datasets stored under `/kellogg/data/`
- [DuckDB Documentation](https://duckdb.org/docs/): configuration and SQL reference
