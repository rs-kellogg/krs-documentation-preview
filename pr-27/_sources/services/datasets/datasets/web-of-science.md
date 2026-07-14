# Web of Science

## At a Glance

| | |
|---|---|
| **Provider** | Clarivate |
| **Coverage** | Varies by collection (see [Collections](#collections)) |
| **Geographic scope** | Global |
| **Update frequency** | Continuous |
| **Schema version** | WOK 5.30 (XML) |
| **Access platforms** | Northwestern Library (web), KDC (raw data), KLC |
| **Eligible users** | Northwestern community (web); limited researchers (raw data) |
| **Questions** | [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) |

## Description

Multidisciplinary coverage of over 10,000 journals in the sciences, social sciences, and arts and humanities, as well as published proceedings for over 12,000 conferences per year, and over 50,000 scholarly books. Powerful tools allow you to search and see what articles in the database have cited a particular work, as well as perform other analytics.

## Access

The Northwestern Library offers access to the [web interface](http://libguides.northwestern.edu/az.php?q=web%20of%20science).

A limited amount of Web of Science raw data can be made available to a limited number of academic researchers through the [Kellogg Data Cloud (KDC)](/services/kellogg-data-cloud/kdc.md), as well as the KLC at `/kellogg/data/WOS`. To inquire about this resource, contact [Research Support](mailto:rs@kellogg.northwestern.edu).

## Data Coverage & Key Identifiers

| Attribute | Value |
|---|---|
| **Time period** | Varies by collection; WOS Core Collection (SCI-E, SSCI) from 1900; AHCI from 1975; ESCI from 2005 |
| **Geographic coverage** | Global |
| **Unit of observation** | Publication record (article, book chapter, conference proceeding, etc.) |
| **Primary identifier** | `UID` — e.g., `WOS:000123456789012` |
| **Commonly linked via** | DOI, PMID (MEDLINE records), ISSN/eISSN, ORCID, ResearcherID |
| **Key variables** | Titles, authors, affiliations, abstract, keywords, citations, funding acknowledgements, subject categories |

## Collections

The raw data is organized into collections (databases). Each `REC` record carries an `edition` attribute indicating which collection(s) it belongs to.

| Collection | Edition value(s) | Coverage |
|---|---|---|
| Science Citation Index Expanded (SCI-E) | `WOS.SCI` | 1900–present |
| Social Sciences Citation Index (SSCI) | `WOS.SSCI` | 1900–present |
| Arts & Humanities Citation Index (AHCI) | `WOS.AHCI` | 1975–present |
| Emerging Sources Citation Index (ESCI) | `WOS.ESCI` | 2005–present |
| Book Citation Index — Science | `WOS.BSCI` | 2005–present |
| Book Citation Index — Social Sciences & Humanities | `WOS.BHCI` | 2005–present |
| MEDLINE | `MEDLINE.MEDLINE` | 1950s–present |
| Biological Abstracts / BIOSIS Previews | `BIOSIS.PREVIEWS` | Varies |
| INSPEC | `INSPEC.INSPEC` | Varies |
| Derwent Innovations Index | `DIIDW.CDerwent` | Varies |
| Chinese Science Citation Database (CSCD) | `CSCD.CSCD` | Varies |
| Zoological Record | `ZOOREC.RECORDS` | Varies |

## Raw Data File Format

Raw data is delivered as **XML files** conforming to the **WOK 5.30 schema** (namespace: `http://clarivate.com/schema/wok5.30/public/FullRecord`). Files may be delivered as plain `.xml` or compressed (`.xml.gz`).

Each file contains a `<records>` root element wrapping one or more `<REC>` elements — one per publication.

### Record Structure

```
<records>
  <REC>
    <UID>WOS:000123456789012</UID>
    <static_data>
      <summary>         <!-- Bibliographic summary -->
        <EWUID>         <!-- Collection/edition identifiers -->
        <pub_info>      <!-- Year, volume, issue, pages -->
        <titles>        <!-- Article title, source journal name, abbreviations -->
        <names>         <!-- Authors and editors -->
        <doctypes>      <!-- Source document type -->
        <publishers>    <!-- Publisher info -->
      </summary>
      <fullrecord_metadata>   <!-- Full bibliographic detail -->
        <languages>
        <normalized_doctypes>
        <references>    <!-- Cited references (when available) -->
        <addresses>     <!-- Author affiliations -->
        <category_info> <!-- Subject headings and categories -->
        <keywords>      <!-- Author-supplied keywords -->
        <abstracts>
        <fund_ack>      <!-- Funding acknowledgements -->
        <data_availability_statement>
      </fullrecord_metadata>
      <item>            <!-- Collection-specific fields (e.g., <item_wos>, <item_medline>) -->
    </static_data>
    <dynamic_data>
      <cluster_related>
        <identifiers>   <!-- DOI, ISSN, PMID, etc. -->
      </cluster_related>
      <citation_related>
        <SDG>           <!-- UN Sustainable Development Goals (added Dec 2024) -->
      </citation_related>
    </dynamic_data>
  </REC>
</records>
```

## Key Fields Reference

The table below covers the fields most commonly used in research. XPaths are relative to the `<REC>` element.

| Field | XPath | Notes |
|---|---|---|
| **Unique identifier** | `UID` | Format: `WOS:nnnnnnn` or `MEDLINE:nnnnn` |
| **Collection/edition** | `static_data/summary/EWUID/edition/@value` | e.g., `WOS.SCI`, `WOS.SSCI` |
| **Article title** | `static_data/summary/titles/title[@type='item']` | |
| **Source (journal) title** | `static_data/summary/titles/title[@type='source']` | |
| **ISO journal abbreviation** | `static_data/summary/titles/title[@type='abbrev_iso']` | |
| **Publication year** | `static_data/summary/pub_info/@pubyear` | |
| **Volume / issue** | `static_data/summary/pub_info/@vol` / `@issue` | |
| **Pages** | `static_data/summary/pub_info/page/@begin` / `@end` | |
| **Document type (source)** | `static_data/summary/doctypes/doctype` | Source-specific values |
| **Document type (normalized)** | `static_data/fullrecord_metadata/normalized_doctypes/doctype` | Standardized values (e.g., `Article`, `Review`) |
| **Authors** | `static_data/summary/names[@role='author']/name` | Multiple elements |
| **Author display name** | `.../name/display_name` | e.g., `Smith, John A` |
| **Author WOS-standard name** | `.../name/wos_standard` | e.g., `Smith, JA` |
| **Author ORCID** | `.../name/ORCID_ID` | When claimed |
| **Author ResearcherID** | `.../name/@r_id` | When available |
| **Affiliations** | `static_data/fullrecord_metadata/addresses/address_name/address_spec` | Linked to authors via `addr_no` |
| **Organization (normalized)** | `.../address_spec/organizations/organization[@pref='Y']` | Preferred/normalized form |
| **ROR ID** | `.../address_spec/organizations/ROR_ID` | Added Dec 2024 |
| **Abstract** | `static_data/fullrecord_metadata/abstracts/abstract/abstract_text/p` | May be multiple paragraphs |
| **Author keywords** | `static_data/fullrecord_metadata/keywords/keyword` | |
| **Keywords Plus** | `static_data/item/item_wos/keywords_plus/keyword` | Generated from cited reference titles; WOS records only |
| **Subject categories** | `static_data/fullrecord_metadata/category_info/subjects/subject[@ascatype='traditional']` | WOS classification |
| **Research areas** | `static_data/fullrecord_metadata/category_info/subjects/subject[@ascatype='extended']` | Broader groupings |
| **DOI** | `dynamic_data/cluster_related/identifiers/identifier[@type='doi']/@value` | |
| **ISSN** | `dynamic_data/cluster_related/identifiers/identifier[@type='issn']/@value` | |
| **eISSN** | `dynamic_data/cluster_related/identifiers/identifier[@type='eissn']/@value` | |
| **PMID** | `dynamic_data/cluster_related/identifiers/identifier[@type='pmid']/@value` | MEDLINE-indexed records |
| **Reference count** | `static_data/fullrecord_metadata/refs/@count` | Count only when full references not included |
| **Cited references** | `static_data/fullrecord_metadata/references/reference` | Full detail when available |
| **Funding agencies** | `static_data/fullrecord_metadata/fund_ack/grants/grant/grant_agency` | |
| **Grant IDs** | `static_data/fullrecord_metadata/fund_ack/grants/grant/grant_ids/grant_id` | |
| **UN SDGs** | `dynamic_data/citation_related/SDG` | Added Dec 2024 |

## Schema Files

The full schema (WOK 5.30) is available as XSD files. Contact [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) to request access:

- `clarivate.com.schema.wok5.30.rawxml.xsd` — Main schema entry point
- `summary.rawxml.xsd` — Summary (bibliographic) fields
- `fullrecord_metadata.rawxml.xsd` — Full record metadata fields
- `common_types.rawxml.xsd` — Common types (identifiers, names, addresses)
- `item_wos.rawxml.xsd` — WOS-specific item fields
- `item_medline.rawxml.xsd` — MEDLINE-specific item fields
- `CHANGELOG` — Schema changelog

## Python Example: Reading Raw XML

The example below reads a WOS XML file and extracts the most commonly used fields into a flat pandas DataFrame. It handles the XML namespace and works with both plain `.xml` and gzip-compressed `.xml.gz` files.

```python
import gzip
import xml.etree.ElementTree as ET
import pandas as pd

# ── namespace ──────────────────────────────────────────────────────────────────
NS = "http://clarivate.com/schema/wok5.30/public/FullRecord"
ns = {"wos": NS}

def text(element, xpath):
    """Return stripped text of first matching element, or None."""
    el = element.find(xpath, ns)
    return el.text.strip() if el is not None and el.text else None

def attr(element, xpath, attribute):
    """Return an attribute value from the first matching element, or None."""
    el = element.find(xpath, ns)
    return el.get(attribute) if el is not None else None

def parse_wos_xml(filepath):
    """
    Parse a WOS raw XML file (plain or gzip-compressed) and return a DataFrame
    with one row per record.
    """
    open_fn = gzip.open if filepath.endswith(".gz") else open

    with open_fn(filepath, "rb") as fh:
        tree = ET.parse(fh)

    root = tree.getroot()
    # Handle both <records> root and bare <REC> root (single-record files)
    recs = root.findall("wos:REC", ns) or ([root] if root.tag.endswith("REC") else [])

    rows = []
    for rec in recs:
        uid = text(rec, "wos:UID")

        # ── pub_info ───────────────────────────────────────────────────────────
        pub = rec.find("wos:static_data/wos:summary/wos:pub_info", ns)
        pubyear  = pub.get("pubyear")  if pub is not None else None
        pubmonth = pub.get("pubmonth") if pub is not None else None
        volume   = pub.get("vol")      if pub is not None else None
        issue    = pub.get("issue")    if pub is not None else None
        page_el  = rec.find(
            "wos:static_data/wos:summary/wos:pub_info/wos:page", ns
        )
        pages = (
            f"{page_el.get('begin')}–{page_el.get('end')}"
            if page_el is not None else None
        )

        # ── titles ─────────────────────────────────────────────────────────────
        titles_el = rec.find("wos:static_data/wos:summary/wos:titles", ns)
        title, source, abbrev = None, None, None
        if titles_el is not None:
            for t in titles_el.findall("wos:title", ns):
                ttype = t.get("type", "")
                ttext = (t.text or "").strip()
                if ttype == "item":
                    title = ttext
                elif ttype == "source":
                    source = ttext
                elif ttype == "abbrev_iso":
                    abbrev = ttext

        # ── document type (normalized) ─────────────────────────────────────────
        doctype = text(
            rec,
            "wos:static_data/wos:fullrecord_metadata/wos:normalized_doctypes/wos:doctype",
        )

        # ── authors ────────────────────────────────────────────────────────────
        authors = []
        for name_el in rec.findall(
            "wos:static_data/wos:summary/wos:names/wos:name", ns
        ):
            if name_el.get("role") == "author":
                dn = text(name_el, "wos:display_name")
                if dn:
                    authors.append(dn)
        authors_str = "; ".join(authors)

        # ── abstract ───────────────────────────────────────────────────────────
        abstract_parts = rec.findall(
            "wos:static_data/wos:fullrecord_metadata"
            "/wos:abstracts/wos:abstract/wos:abstract_text/wos:p",
            ns,
        )
        abstract = " ".join(
            (p.text or "").strip() for p in abstract_parts if p.text
        ) or None

        # ── author keywords ────────────────────────────────────────────────────
        kw_els = rec.findall(
            "wos:static_data/wos:fullrecord_metadata/wos:keywords/wos:keyword", ns
        )
        keywords = "; ".join((k.text or "").strip() for k in kw_els if k.text)

        # ── identifiers (DOI, ISSN, PMID) ──────────────────────────────────────
        doi, issn, pmid = None, None, None
        for id_el in rec.findall(
            "wos:dynamic_data/wos:cluster_related/wos:identifiers/wos:identifier", ns
        ):
            id_type  = id_el.get("type", "")
            id_value = id_el.get("value", "")
            if id_type == "doi":
                doi = id_value
            elif id_type == "issn":
                issn = id_value
            elif id_type == "pmid":
                pmid = id_value

        # ── reference count ────────────────────────────────────────────────────
        refs_el = rec.find(
            "wos:static_data/wos:fullrecord_metadata/wos:refs", ns
        )
        references_el = rec.find(
            "wos:static_data/wos:fullrecord_metadata/wos:references", ns
        )
        ref_count = None
        if refs_el is not None:
            ref_count = refs_el.get("count")
        elif references_el is not None:
            ref_count = references_el.get("count")

        # ── subject categories ─────────────────────────────────────────────────
        subjects = rec.findall(
            "wos:static_data/wos:fullrecord_metadata"
            "/wos:category_info/wos:subjects/wos:subject",
            ns,
        )
        categories = "; ".join(
            (s.text or "").strip()
            for s in subjects
            if s.get("ascatype") == "traditional" and s.text
        )

        rows.append({
            "uid":         uid,
            "pubyear":     pubyear,
            "pubmonth":    pubmonth,
            "volume":      volume,
            "issue":       issue,
            "pages":       pages,
            "doctype":     doctype,
            "title":       title,
            "source":      source,
            "abbrev_iso":  abbrev,
            "authors":     authors_str,
            "abstract":    abstract,
            "keywords":    keywords,
            "doi":         doi,
            "issn":        issn,
            "pmid":        pmid,
            "ref_count":   ref_count,
            "categories":  categories,
        })

    return pd.DataFrame(rows)


# ── usage ──────────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    # Works with plain XML or gzip-compressed XML
    df = parse_wos_xml("wos_records.xml")
    # df = parse_wos_xml("wos_records.xml.gz")

    print(df.shape)
    print(df[["uid", "pubyear", "doctype", "title", "doi"]].head())

    # Save to CSV for downstream analysis
    df.to_csv("wos_flat.csv", index=False)
```

```{tip}
For very large WOS files (hundreds of thousands of records), use `iterparse` to avoid loading the entire XML tree into memory:

```python
import xml.etree.ElementTree as ET

NS_TAG = f"{{{NS}}}"  # prepend namespace for iterparse tag matching

for event, elem in ET.iterparse("wos_records.xml", events=("end",)):
    if elem.tag == f"{NS_TAG}REC":
        uid = elem.findtext(f"{NS_TAG}UID")
        # ... process record ...
        elem.clear()  # free memory
```

## Linking WOS Records to Other Datasets

| Link target | Field(s) to use |
|---|---|
| PubMed / MEDLINE | `identifier[@type='pmid']` |
| Patent databases | `identifier[@type='patent_no']` (Derwent records) |
| WRDS / CRSP / Compustat | Via author affiliation + year (requires disambiguation) |
| OpenAlex / Semantic Scholar | DOI (`identifier[@type='doi']`) |
| Funding databases (NIH, NSF) | `fund_ack/grants/grant/grant_id` + `grant_agency` |
