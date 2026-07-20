# L2 VM2 Uniform

## At a Glance

| | |
|---|---|
| **Provider** | L2 Political (L2, Inc.) |
| **Coverage** | All 50 US states + DC |
| **Geographic scope** | United States |
| **Update frequency** | Periodic (see Redivis version history) |
| **Access platforms** | Redivis |
| **Eligible users** | Kellogg faculty, doctoral students, and approved researchers |
| **Questions** | [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) |

## Description

L2 VM2 Uniform is a national voter file compiled and standardized by [L2 Political](https://l2political.com/), one of the leading voter data vendors in the United States. L2 collects official voter registration records from all 50 states and the District of Columbia, enhances them with commercially sourced consumer and demographic data, and delivers a single harmonized schema — the "VM2 Uniform" format — across all states.

Because different states collect different registration fields, L2 applies statistical models to fill gaps and produce a nationally consistent dataset. Modeled fields are flagged in the data dictionary and should be interpreted accordingly.

The dataset contains approximately **200 million voter records** and includes:

- **Voter registration details** — state and county voter IDs, registration date, active/inactive status
- **Residential and mailing addresses** — fully parsed, CASS-standardized, geocoded with latitude/longitude
- **Demographics** — name, gender, age, date of birth, ethnicity, language, place of birth
- **Political data** — registered party, party modeling scores, voting history back to 2000
- **Consumer/lifestyle data** — estimated income, household net worth, home value, education, occupation, interests, investments
- **Household composition** — household size, children's ages, generational makeup
- **Geographic identifiers** — census tract/block, congressional district, state legislative district, school district, and hundreds of specialized districts
- **FEC donation history** — federal campaign donation counts, amounts, and dates

## Access

The L2 VM2 Uniform dataset is available on [Redivis](https://redivis.com) under the Northwestern organization. Access requires two steps beyond a standard Northwestern Redivis login:

### Step 1 — Apply for data access

On the dataset page in Redivis, open the **Access** panel. You will see that **Data access** (the ability to query tables) shows "0 / 1 complete". Click **Apply** next to the **L2 Req** requirement.

```{image} L2-Apply-For-Data-Access.png
:alt: Redivis access panel showing the Apply button next to L2 Req under Data access
:width: 480px
:align: center
```

### Step 2 — Sign the Data Use Agreement with your initials

After clicking Apply, the **L2 Req** application form opens. Read each of the four required statements and enter your initials in the field next to each one:

1. The L2 Current Voter List is solely for the purposes of non-profit academic research and education.
2. You will not transfer L2 data in whole or in part to any third parties (including AI APIs) without prior written permission of L2.
3. All research papers and publications based on L2 data will contain a public acknowledgment of L2.
4. Any personal information in the L2 data is for the limited purpose of academic research and education.

Once all four fields are initialled, click **Submit**. Your application will be reviewed by a Northwestern administrator.

```{image} L2-Sign-DUA-With-Initials.png
:alt: L2 Req application form showing four initial fields and the Submit button
:width: 480px
:align: center
```

Access is granted after administrator review. Access automatically expires after one year and may be renewed by repeating this process.

For questions or to expedite access, contact [Kellogg Research Support](mailto:rs@kellogg.northwestern.edu).

:::{important}
The VM2 Uniform dataset contains sensitive personal information including names, addresses, birth dates, phone numbers, and political affiliation. Use of this data is subject to L2's data licensing terms. Do not share raw records or derived identifying information outside your approved research project.
:::

---

(l2-schema)=
## Schema

On Redivis, the L2 VM2 Uniform data is organized as **one table per state**, named using the two-letter state abbreviation followed by `_Uniform` — for example `AK_Uniform`, `AL_Uniform`, `AR_Uniform`, … `WY_Uniform`. Each table has the same ~800-column schema. To work with multiple states, use `UNION ALL` across the relevant state tables (see the [multi-state query example](#l2-queries) below).

Field definitions, value codes, and modeled-data flags are provided in the full data dictionary:

- [VM2 Uniform Data Dictionary (Nov 2025)](https://usercontent.redivis.com/downloads/documentationFiles/e2c8df8e-2cef-431f-9f34-737364719d1b)
- [L2 Codebook (reference)](https://usercontent.redivis.com/downloads/documentationFiles/e35554a5-685d-48c6-8471-7e343ebf7e05)

### Key Field Groups

::::{dropdown} Voter Identity & Registration
| Field | Description |
|---|---|
| `LALVOTERID` | Permanent unique voter ID assigned by L2 (primary key) |
| `Voters_StateVoterID` | State-issued voter registration ID |
| `Voters_CountyVoterID` | County-issued voter ID (where available) |
| `Voters_FirstName` | First name |
| `Voters_MiddleName` | Middle name |
| `Voters_LastName` | Last name |
| `Voters_NameSuffix` | Name suffix (Jr., Sr., etc.) |
| `Voters_Active` | Active/inactive registration status (`A` = Active, `I` = Inactive) |
| `Voters_CalculatedRegDate` | Registration date as calculated by L2 |
| `Voters_OfficialRegDate` | Registration date as reported by the state |
| `AbsenteeTypes_Description` | Absentee/mail ballot type |
| `Parties_Description` | Registered party (text) |
| `VoterParties_Change_Changed_Party` | Whether the voter has changed party registration |
::::

::::{dropdown} Address & Geocoding
| Field | Description |
|---|---|
| `Residence_Addresses_AddressLine` | Full residential address string |
| `Residence_Addresses_City` | City |
| `Residence_Addresses_State` | State (2-letter) |
| `Residence_Addresses_Zip` | 5-digit ZIP code |
| `Residence_Addresses_ZipPlus4` | ZIP+4 |
| `Residence_Addresses_CensusTract` | Census tract |
| `Residence_Addresses_CensusBlock` | Census block |
| `Residence_Addresses_Latitude` | Latitude (decimal degrees) |
| `Residence_Addresses_Longitude` | Longitude (decimal degrees) |
| `Residence_Addresses_LatLongAccuracy` | Geocoding accuracy code (see codebook) |
| `Residence_Addresses_Property_Type` | Property type (single-family, condo, etc.) |
| `Mailing_Addresses_AddressLine` | Mailing address (if different from residence) |
| `Mailing_Addresses_City` | Mailing city |
| `Mailing_Addresses_State` | Mailing state |
| `Mailing_Addresses_Zip` | Mailing ZIP |
::::

::::{dropdown} Demographics
| Field | Description |
|---|---|
| `Voters_Gender` | Gender (M / F / U) |
| `Voters_Age` | Age in years |
| `Voters_BirthDate` | Date of birth (YYYYMMDD) |
| `BirthDateConfidence_Description` | Confidence level of birth date |
| `Voters_PlaceOfBirth` | State or country of birth |
| `Ethnic_Description` | Ethnic description (modeled) |
| `EthnicGroups_EthnicGroup1Desc` | Broad ethnic group (modeled) |
| `CountyEthnic_LALEthnicCode` | L2 ethnic code (see codebook) |
| `ConsumerData_Language_Code` | Likely primary language (modeled) |
| `ConsumerData_Marital_Status` | Marital status (modeled) |
| `ConsumerData_Education_of_Person` | Education level (modeled) |
::::

::::{dropdown} Political Scores & Voting History
Voting history fields are named `General_YYYY`, `Primary_YYYY`, and `PresidentialPrimary_YYYY`. Values are `Y` (voted) or null (no record). History extends back to 2000.

| Field | Description |
|---|---|
| `General_2024` | Voted in 2024 general election |
| `Primary_2024` | Voted in 2024 primary |
| `PresidentialPrimary_2024` | Voted in 2024 presidential primary |
| `General_2022` | Voted in 2022 general election |
| `General_2020` | Voted in 2020 general election |
| `PresidentialPrimary_2020` | Voted in 2020 presidential primary |
| `General_2016` | Voted in 2016 general election |
| … | History available back to 2000 |
| `ConsumerData_Progressive_Democrat_Score` | Model score: progressive Democrat propensity |
| `ConsumerData_Moderate_Democrat_Score` | Model score: moderate Democrat propensity |
| `ConsumerData_Moderate_Republican_Score` | Model score: moderate Republican propensity |
| `ConsumerData_Conservative_Republican_Score` | Model score: conservative Republican propensity |
::::

::::{dropdown} Consumer & Financial Data
| Field | Description |
|---|---|
| `ConsumerData_Estimated_Income_Amount` | Estimated household income (modeled) |
| `ConsumerData_Household_Net_Worth` | Estimated net worth (modeled) |
| `ConsumerData_EstimatedAreaMedianHHIncome` | Area median household income |
| `ConsumerData_StateIncomeDecile` | Income decile within state (modeled) |
| `ConsumerData_Home_Est_Current_Value_Code` | Estimated current home value range |
| `ConsumerData_Homeowner_Probability_Model` | Probability of homeownership (modeled) |
| `ConsumerData_Invest_Active` | Active investor indicator (modeled) |
| `ConsumerData_Investments` | General investment interest indicator |
| `ConsumerData_Investments_Realestate` | Real estate investment interest |
| `FECDonors_TotalDonationsAmount` | Total federal political donation amount |
| `FECDonors_NumberOfDonations` | Number of federal donations |
| `FECDonors_AvgDonation` | Average federal donation amount |
| `FECDonors_LastDonationDate` | Date of most recent federal donation |
| `ConsumerData_Business_Owner` | Business owner indicator (modeled) |
| `ConsumerData_Occupation_of_Person` | Occupation code (see codebook) |
::::

::::{dropdown} Household Composition
| Field | Description |
|---|---|
| `ConsumerData_Number_Of_Persons_in_HH` | Number of persons in household |
| `ConsumerData_Number_Of_Adults_in_HH` | Number of adults in household |
| `ConsumerData_Number_Of_Children_in_HH` | Number of children in household |
| `ConsumerData_Presence_Of_Children_in_HH` | Presence of children indicator |
| `ConsumerData_Senior_Adult_In_HH` | Senior adult (65+) in household |
| `ConsumerData_Veteran_In_HH` | Veteran in household |
| `ConsumerData_Generations_In_HH` | Number of generations in household |
| `Residence_HHGender_Description` | Household gender composition |
| `Residence_HHParties_Description` | Household party composition |
| `Residence_Families_HHVotersCount` | Number of registered voters in household |
::::

::::{dropdown} Geographic & Political Districts
The dataset includes hundreds of district-level fields. Key ones include:

| Field | Description |
|---|---|
| `Voters_FIPS` | FIPS county code |
| `County` | County name |
| `US_Congressional_District` | US House district |
| `State_Senate_District` | State senate district |
| `State_House_District` | State house/assembly district |
| `Precinct` | Voting precinct |
| `School_District` | School district |
| `City` | City/municipality |
| `2010_US_Congressional_District` | 2010 redistricting congressional district |
| `2024_Proposed_Congressional_District` | 2024 proposed congressional district |

Additional district fields cover judicial districts, special districts, utility districts, and more. See the data dictionary for the full list.
::::

---

(l2-queries)=
## Example Queries

The following SQL examples use Illinois (`IL_Uniform`) as the example state table. Replace `IL_Uniform` with the state table you need (e.g., `CA_Uniform`, `NY_Uniform`). To query multiple states, use `UNION ALL` as shown in the multi-state example below.

### Count registered voters by party in a single state

```sql
SELECT
    Parties_Description  AS party,
    COUNT(*)             AS voter_count
FROM IL_Uniform  -- replace with your target state table
WHERE Voters_Active = 'A'
GROUP BY 1
ORDER BY 2 DESC;
```

### Combine multiple states with UNION ALL

```sql
SELECT
    'IL' AS state, Parties_Description AS party, COUNT(*) AS voter_count
FROM IL_Uniform
WHERE Voters_Active = 'A'
GROUP BY 1, 2

UNION ALL

SELECT
    'IN' AS state, Parties_Description AS party, COUNT(*) AS voter_count
FROM IN_Uniform
WHERE Voters_Active = 'A'
GROUP BY 1, 2

ORDER BY 1, 3 DESC;
```

### Voter turnout rate in 2024 general election

```sql
SELECT
    COUNT(*)                                           AS registered_voters,
    COUNTIF(General_2024 = 'Y')                        AS voted_2024,
    ROUND(COUNTIF(General_2024 = 'Y') / COUNT(*), 4)  AS turnout_rate
FROM IL_Uniform  -- replace with your target state table
WHERE Voters_Active = 'A';
```

### Identify consistent general-election voters (voted in all elections 2016–2024)

```sql
SELECT
    LALVOTERID,
    Voters_FirstName,
    Voters_LastName,
    Parties_Description
FROM IL_Uniform  -- replace with your target state table
WHERE
    Voters_Active  = 'A'
    AND General_2024 = 'Y'
    AND General_2022 = 'Y'
    AND General_2020 = 'Y'
    AND General_2018 = 'Y'
    AND General_2016 = 'Y';
```

### Registered voters who did not vote in the last three general elections (2020, 2022, 2024)

```sql
SELECT
    LALVOTERID,
    Voters_FirstName,
    Voters_LastName,
    Parties_Description,
    Voters_Age
FROM IL_Uniform  -- replace with your target state table
WHERE
    Voters_Active    = 'A'
    AND General_2024 IS NULL
    AND General_2022 IS NULL
    AND General_2020 IS NULL;
```

### Age and income distribution of Democratic primary voters in Illinois

```sql
SELECT
    CASE
        WHEN CAST(Voters_Age AS INT64) BETWEEN 18 AND 29 THEN '18-29'
        WHEN CAST(Voters_Age AS INT64) BETWEEN 30 AND 44 THEN '30-44'
        WHEN CAST(Voters_Age AS INT64) BETWEEN 45 AND 64 THEN '45-64'
        WHEN CAST(Voters_Age AS INT64) >= 65            THEN '65+'
        ELSE 'Unknown'
    END                                             AS age_group,
    ConsumerData_Estimated_Income_Amount            AS income_range,
    COUNT(*)                                        AS voter_count
FROM IL_Uniform
WHERE
    Parties_Description = 'Democratic'
    AND Primary_2024    = 'Y'
GROUP BY 1, 2
ORDER BY 1, 3 DESC;
```

### Households with multiple registered voters and their party mix

```sql
SELECT
    Residence_Addresses_AddressLine,
    Residence_Addresses_City,
    Residence_HHParties_Description  AS household_party_mix,
    Residence_Families_HHVotersCount AS voters_in_household
FROM IL_Uniform
WHERE
    Voters_Active                        = 'A'
    AND Residence_Families_HHVotersCount > 1
LIMIT 500;
```

### Geocoded voter locations for mapping (sample)

```sql
SELECT
    LALVOTERID,
    CAST(Residence_Addresses_Latitude  AS FLOAT64) AS lat,
    CAST(Residence_Addresses_Longitude AS FLOAT64) AS lon,
    Residence_Addresses_CensusTract,
    Residence_Addresses_CensusBlock,
    Parties_Description
FROM IL_Uniform
WHERE
    Residence_Addresses_LatLongAccuracy IN ('1', '2', '3')  -- high-accuracy geocodes
    AND Voters_Active = 'A'
LIMIT 10000;
```

### Federal political donors with total giving over $1,000

```sql
SELECT
    LALVOTERID,
    Voters_FirstName,
    Voters_LastName,
    Parties_Description,
    CAST(FECDonors_TotalDonationsAmount AS FLOAT64) AS total_donated,
    FECDonors_NumberOfDonations                     AS num_donations,
    FECDonors_LastDonationDate
FROM IL_Uniform
WHERE
    FECDonors_TotalDonationsAmount IS NOT NULL
    AND CAST(FECDonors_TotalDonationsAmount AS FLOAT64) > 1000
ORDER BY total_donated DESC
LIMIT 1000;
```

---

## Notes on Modeled Data

Many fields in the VM2 Uniform dataset are **statistically modeled** rather than directly observed from voter registration records. These include ethnicity estimates, income, net worth, education, occupation, party propensity scores, and most `ConsumerData_*` fields. Modeled fields are flagged in the data dictionary (`Modeled Data?` column = `Y`).

When using modeled fields in research:

- Report that the variable is model-estimated, not administrative data
- Validate against known benchmarks where possible
- Be aware that model accuracy varies by state and demographic group

## Linking to Other Datasets

| Dataset | Linkage approach |
|---|---|
| Census / ACS | Via `Residence_Addresses_CensusTract` + `CensusBlock` |
| FEC individual contributions | `LALVOTERID` can be matched to FEC records via name + address; or use the pre-merged `FECDonors_*` fields |
| Other voter files | Match on `Voters_StateVoterID` within the same state |

For linkage assistance, contact [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu).
