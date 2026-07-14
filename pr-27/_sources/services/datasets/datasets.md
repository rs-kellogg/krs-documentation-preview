(klc-datasets)=
# Kellogg Datasets

Kellogg Research Support maintains licensed access to over 100 research datasets spanning finance, economics, healthcare, marketing, and more. This catalog describes what is available and how to access it.

**To request access or get help**, contact [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu).

In addition to the datasets below, [Social Science Data Services (SSDS)](https://www.library.northwestern.edu/use-the-libraries/research-teaching/digital-scholarship/) provides data, software, and software training to support research and instruction in those social sciences that require analysis of quantitative or qualitative data.

---

## Finding Data by Platform

Most datasets are accessed through one or more of the following platforms:

| Platform | Description | Who can access |
|---|---|---|
| **[WRDS](https://wrds-www.wharton.upenn.edu/)** | Wharton Research Data Services — web interface and cloud computing environment for ~50 of our most-used finance and economics datasets | Kellogg faculty, doctoral students, and approved researchers |
| **[Kellogg Linux Cluster (KLC)](../klc/klc)** | Datasets stored as files under `/kellogg/data/` on KLC nodes; query with Python, R, Stata, or SAS directly | KLC account holders |
| **[Redivis](https://redivis.com/)** | Cloud data platform with SQL query interface; used for select large-scale datasets | See individual dataset page |
| **[Kellogg Data Cloud (KDC)](../kellogg-data-cloud/kdc)** | AWS-hosted data warehouse; query via Athena or ODBC | Approved researchers; contact RS |
| **Bloomberg Terminal** | Physical terminals in Kellogg Global Hub | Kellogg faculty and students |
| **Direct access** | Some datasets require a request or special arrangement | Contact RS |

---

## Dataset Catalog by Research Domain

### Equities & Stock Markets

| Dataset | Description |
|---|---|
| [Arca](datasets/arca) | Complete limit order book for NYSE Arca ECN (Sep–Oct 2008) |
| [Bloomberg](datasets/bloomberg) | Real-time and historical data, analytics, and news across global markets |
| [CBOE Indexes](datasets/cboe-indexes) | CBOE Volatility Index (VIX) and related volatility measures |
| [Compustat Global](datasets/compustat-global) | Financial and stock market data for 82 countries |
| [Compustat North America](datasets/compustat-north-america) | Annual and quarterly financials for US and Canadian public companies |
| [CRSP](datasets/crsp) | US equity returns, prices, and market data (NYSE, AMEX, NASDAQ) |
| [Capital IQ](datasets/capital-iq) | Corporate information, financials, and transactions for public and private companies |
| [Datastream](datasets/datastream) | Global historical financial data — equities, bonds, derivatives |
| [Dow Jones Averages & Total Return Indexes](datasets/dow-jones-averages-&-total-return-indexes) | Daily and monthly Dow Jones Composite, Industrial, Transportation, Utility indexes |
| [Economatica](datasets/economatica) | Company data for 5,000+ firms in Latin America |
| [EDGAR](datasets/edgar) | Local collection of SEC EDGAR filings updated daily; stored on KLC at `/kellogg/data/EDGAR` |
| [EDGAR Online](datasets/edgar-online) | Web service for all SEC filings since 1994 |
| [Emerging Markets Database](datasets/emerging-markets-database) | Stock market performance and indicators for emerging and frontier markets |
| [ExecuComp](datasets/execucomp) | Executive compensation for S&P 500, MidCap, and SmallCap companies |
| [FactSet](datasets/factset) | Financial data and analytics for public/private companies, PE/VC, M&A, ownership |
| [Fama-French Portfolios and Factors](datasets/fama-french-portfolios-and-factors) | Size/value portfolio returns and factor series |
| [FTSE/Russell](datasets/ftse-russell) | Comprehensive equity and fixed income market coverage |
| [Global Financial Database](datasets/global-financial-database) | Long historical time series (some from 1265) for 200+ global markets |
| [I/B/E/S Earnings Estimate History](datasets/i-b-e-s-earnings-estimate-history) | Analyst forecasts of earnings, cash flows, and buy/sell recommendations |
| [Mergent Investext](datasets/mergent-investext) | SEC filings, annual reports, and analyst research reports from 1,000+ institutions |
| [Value Line](datasets/value-line) | Analyst estimates and 3–5 year projections for ~1,700 companies |
| [Zacks](datasets/zacks) | Analyst forecasts, revisions, price targets, and recommendations |

---

### Fixed Income, Credit & Derivatives

| Dataset | Description |
|---|---|
| [CBOT Treasury Package](datasets/cbot-treasury-package) | *Legacy — no longer updated.* Tick-by-tick CBOT futures data |
| [CME](datasets/cme) | *Legacy — no longer updated.* Selective CME time and sales data |
| [Federal Reserve Bank Reports](datasets/federal-reserve-bank-reports) | Foreign exchange rates and interest rates from Federal Reserve Banks (via WRDS) |
| [ISSM Transactions File Database](datasets/issm-transactions-file-database) | Tick-by-tick NYSE/AMEX/NASDAQ data, 1983–1992 |
| [Institute for Financial Markets](datasets/institute-for-financial-markets) | Daily futures data for 115 contracts across US, Canadian, and international exchanges |
| [LIFFE Tick Data](datasets/liffe-tick-data) | Futures and options data from the London International Financial Futures Exchange |
| [Mergent FISD](datasets/mergent-fisd) | Fixed Income Securities Database — debt securities and NAIC pricing data |
| [MSRB](datasets/msrb--municipal-securities-transaction-data-) | Municipal securities transaction data from the $3.7 trillion muni market |
| [OTC Markets](datasets/otc-markets) | Closing quote, trade, and security reference data for OTCQX, OTCQB, and OTC Pink |
| [OptionMetrics Ivy DB](datasets/optionmetrics-ivy-db) | End-of-day quotes, open interest, and volume for all US-listed equity options |
| [Philadelphia Stock Exchange (PHLX)](datasets/philadelphia-stock-exchange--phlx-) | Stock, equity option, index option, and currency option data |
| [R&C Futures Data](datasets/r&c-futures-data) | End-of-day and intraday data for 80 global commodity futures |
| [TRACE](datasets/trace) | OTC corporate bond transaction data — investment grade, high yield, convertible |
| [Trade and Quote Database](datasets/trade-and-quote-database) | Intraday trades and quotes for NYSE, AMEX, Nasdaq (1993–present) |

---

### Corporate Governance, ESG & Ownership

| Dataset | Description |
|---|---|
| [Audit Analytics](datasets/audit-analytics) | Audit information for ~20,000 public firms — auditors, SOX disclosures, litigation |
| [Bank Regulatory](datasets/bank-regulatory) | Five regulatory databases for depository financial institutions |
| [Blockholders](datasets/blockholders) | Standardized blockholder data for 1,913 companies |
| [BoardEx](datasets/boardex) | Profiles of business executives worldwide — career history, compensation, board memberships, and network connections |
| [ISS Dilution Data](datasets/iss-dilution-data) | Option grants, exercise prices, and contractual life for S&P 1500 companies |
| [ISS Directors Data](datasets/iss-directors-data) | Board composition for S&P 1500 — demographics, compensation, committee memberships |
| [ISS Governance Data](datasets/iss-governance-data) | Corporate governance provisions compiled from public sources for ~2,000 corporations |
| [ISS Securities Class Action Services](datasets/iss-securities-class-action-services) | Litigation research and claims filing for equities and fixed income |
| [ISS Shareholder Proposals](datasets/iss-shareholder-proposals) | Governance-related shareholder resolutions, sponsors, votes, and outcomes |
| [ISS Voting Analytics](datasets/iss-voting-analytics) | Voting policies, meeting results, and institutional voting patterns |
| [MSCI (formerly KLD and GMI Ratings)](datasets/msci--formerly-klc-and-gmi-ratings-) | Annual ESG performance indicators for publicly traded companies |
| [Refinitiv ESG](datasets/refinitiv-esg) | ESG scores across 10 themes based on publicly reported company data |
| [RiskMetrics CEPD](datasets/riskmetrics-cepd) | Environmental profiles for 2,065 public companies across 19 environmental statutes |
| [RiskMetrics Intangible Value Assessment](datasets/riskmetrics-intangible-value-assessment) | ESG risk ratings and analysis of financially material ESG factors |

---

### Deals, M&A & Institutional Holdings

| Dataset | Description |
|---|---|
| [Bureau van Dijk](datasets/bureau-van-dijk) | AMADEUS, ORBIS, and OSIRIS — accounting and firm-level data for US and Europe |
| [DealScan (LSTA/LPC)](datasets/dealscan--lsta-lpc-) | Global commercial loan market data |
| [First Call Historical Database](datasets/first-call-historical-database) | Real-time earnings estimates, broker details, and company-issued guidance |
| [Lipper Hedge Fund](datasets/lipper-hedge-fund) | Performance data for 6,300+ active and 7,000+ closed hedge funds |
| [SDC Platinum](datasets/sdc-platinum) | US/non-US M&A, global new issues, and corporate restructuring transactions |
| [Thomson Institutional (13F) and Mutual Fund (S12) Holdings](datasets/thomson-institutional--13f--and-mutual-fund--s12--holdings) | Quarterly institutional and mutual fund holdings from 1980 to present |

---

### Healthcare & Health Policy

| Dataset | Description |
|---|---|
| [AHA Annual Survey](datasets/aha-annual-survey) | American Hospital Association annual data (1990–2012, even years) |
| [CA Hospital Financial Data](datasets/ca-hospital-financial-data) | California hospital financial data, 1983–2003 |
| [CA Hospital Inpatient Utilization](datasets/ca-hospital-inpatient-utilization) | 3M+ California inpatient records per year, 1989–2004 |
| [Florida AHCA Inpatient Discharge Data](datasets/florida-ahca-inpatient-discharge-data) | Florida inpatient utilization data |
| [HCUP NIS](datasets/hcup-nis) | 20% sample of all US inpatient admissions (AHRQ Healthcare Cost and Utilization Project) |
| [HCUP SID](datasets/hcup-sid) | State-level inpatient admissions data for selected states and years (AHRQ HCUP) |
| [Health and Retirement Study](datasets/health-and-retirement-study) | Longitudinal survey of near-retirement individuals — health, wealth, employment, family |
| [Levin Associates Health Care Acquisition Reports](datasets/levin-associates-health-care-acquisition-reports) | M&A data across health care industry sectors |
| [NAIC Financial Statement Data](datasets/naic-financial-statement-data) | Insurance company financial data from NAIC, 2001–2017 |
| [NAIC Health Insurance Data](datasets/naic-health-insurance-data) | Private health insurance enrollment and premium data, 2001–2014 |
| [NAIC Property/Casualty Insurance Data](datasets/naic-property-casualty-insurance-data) | Detailed financial data for US property/casualty insurers, 1993–2004 |
| [New York SPARCS Inpatient Databases](datasets/new-york-sparcs-inpatient-databases) | New York inpatient utilization data |

---

### Marketing & Consumer Behavior

| Dataset | Description |
|---|---|
| [Comscore](datasets/comscore) | Individual-level URL traffic, ad exposure, and e-commerce transactions (2019–20) |
| [Direct Marketing Educational Foundation (DMEF)](datasets/direct-marketing-educational-foundation--dmef-) | Customer buying history for ~100,000 customers across four catalog/non-profit businesses |
| [Forrester Research](datasets/forrester-research) | Annual survey of 40,000+ US/Canadian households on technology behavior |
| [IRI Marketing FactBook](datasets/iri-marketing-factbook) | Point-of-sale data from 11,300+ grocery stores and 7,500 drug stores |
| [Nielsen Marketing Data](datasets/nielsen-marketing-data) | Consumer Panel, Retail Scanner, and Ad Intel data from all US markets |
| [Numerator](datasets/numerator) | Purchase-tracking and consumer survey panel data |

---

### Political Science & Voter Data

| Dataset | Description |
|---|---|
| [L2 VM2 Uniform](datasets/l2-vm2-uniform) | National voter file with ~200M records: registration, voting history back to 2000, demographics, and consumer data for all 50 states |

---

### Macroeconomics & International

| Dataset | Description |
|---|---|
| [IMF International Financial Statistics](datasets/imf-international-financial-statistics) | Exchange rates, monetary data, interest rates, prices, and national accounts since 1940 |

---

### Real Estate

| Dataset | Description |
|---|---|
| [Cotality (formerly CoreLogic)](datasets/cotality) | 147M+ US properties — sales transactions, property descriptions, ownership changes |
| [RCA](datasets/rca) | Commercial property transactions ($2.5M+ US, $10M+ global) |
| [SNL](datasets/snl) | Real estate company data and banking/financial services/insurance data |

---

### Alternative & Emerging Data

| Dataset | Description |
|---|---|
| [Equifax](datasets/equifax) | Credit risk scores and consumer data at the loan level for a US population sample |
| [PATSTAT](datasets/patstat) | Worldwide patent database from the European Patent Office |
| [ProxyCurl](datasets/proxycurl) | Professional profiles and company data sourced from LinkedIn (Redivis + KLC) |
| [RavenPack News Analytics](datasets/ravenpack-news-analytics) | Real-time sentiment, relevance, and novelty data extracted from news text |
| [Research Quotient](datasets/research-quotient) | Firm-level R&D productivity measure linking R&D spending to growth and market value |
| [Taxi](datasets/taxi) | 2013 New York City taxi operations from NYC Taxi & Limousine Commission FOIL request |

---

### Academic, Government & Public Records

| Dataset | Description |
|---|---|
| [Census Data](datasets/census-data) | US Census Bureau data on people, business, and economy |
| [Chicago Research Data Center](datasets/chicago-research-data-center) | Restricted-access Census microdata through collaboration with the Census Bureau |
| [CORD-19](datasets/cord-19) | COVID-19 open research dataset — scholarly articles on KLC at `/kellogg/data/CORD-19` |
| [ICPSR](datasets/icpsr) | Multi-disciplinary social science data archive (political science, economics, health, etc.) |
| [Social Science Research Network](datasets/social-science-research-network) | Working paper abstracts, conference announcements, and accepted papers across social sciences |
| [Web of Science](datasets/web-of-science) | 10,000+ journals and 12,000+ conference proceedings in sciences, social sciences, and humanities |

---

## Datasets Available on the Kellogg Linux Cluster

The following datasets have files stored directly on KLC under `/kellogg/data/`. Access requires a KLC account. See the individual dataset page for the exact path and file format.

[Arca](datasets/arca) {octicon}`dot-fill` [BoardEx](datasets/boardex) {octicon}`dot-fill` [CBOT Treasury Package](datasets/cbot-treasury-package) {octicon}`dot-fill` [CME](datasets/cme) {octicon}`dot-fill` [Comscore](datasets/comscore) {octicon}`dot-fill` [CORD-19](datasets/cord-19) {octicon}`dot-fill` [Cotality (formerly CoreLogic)](datasets/cotality) {octicon}`dot-fill` [DealScan](datasets/dealscan--lsta-lpc-) {octicon}`dot-fill` [EDGAR](datasets/edgar) {octicon}`dot-fill` [First Call Historical Database](datasets/first-call-historical-database) {octicon}`dot-fill` [Forrester Research](datasets/forrester-research) {octicon}`dot-fill` [I/B/E/S](datasets/i-b-e-s-earnings-estimate-history) {octicon}`dot-fill` [Institute for Financial Markets](datasets/institute-for-financial-markets) {octicon}`dot-fill` [ISS Securities Class Action Services](datasets/iss-securities-class-action-services) {octicon}`dot-fill` [ISSM Transactions File Database](datasets/issm-transactions-file-database) {octicon}`dot-fill` [Lipper Hedge Fund](datasets/lipper-hedge-fund) {octicon}`dot-fill` [MSCI](datasets/msci--formerly-klc-and-gmi-ratings-) {octicon}`dot-fill` [NAIC Financial Statement Data](datasets/naic-financial-statement-data) {octicon}`dot-fill` [NAIC Property/Casualty Insurance Data](datasets/naic-property-casualty-insurance-data) {octicon}`dot-fill` [Nielsen Marketing Data](datasets/nielsen-marketing-data) {octicon}`dot-fill` [PATSTAT](datasets/patstat) {octicon}`dot-fill` [ProxyCurl](datasets/proxycurl) {octicon}`dot-fill` [R&C Futures Data](datasets/r&c-futures-data) {octicon}`dot-fill` [Value Line](datasets/value-line) {octicon}`dot-fill` [Zacks](datasets/zacks)

---

## Datasets Available on Redivis

The following datasets are available through the [Redivis](https://redivis.com/) cloud data platform. Contact [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) to confirm access.

[Numerator](datasets/numerator) {octicon}`dot-fill` [L2 VM2 Uniform](datasets/l2-vm2-uniform) {octicon}`dot-fill` [ProxyCurl](datasets/proxycurl)

---

```{toctree}
:maxdepth: 1
:hidden:
Find Data by Platform <by-platform>
AHA Annual Survey <datasets/aha-annual-survey>
Arca <datasets/arca>
Audit Analytics <datasets/audit-analytics>
Bank Regulatory <datasets/bank-regulatory>
Blockholders <datasets/blockholders>
Bloomberg <datasets/bloomberg>
BoardEx <datasets/boardex>
Bureau van Dijk <datasets/bureau-van-dijk>
CA Hospital Financial Data <datasets/ca-hospital-financial-data>
CA Hospital Inpatient Utilization <datasets/ca-hospital-inpatient-utilization>
CBOE Indexes <datasets/cboe-indexes>
CBOT Treasury Package <datasets/cbot-treasury-package>
CME <datasets/cme>
CORD-19 <datasets/cord-19>
CRSP <datasets/crsp>
Capital IQ <datasets/capital-iq>
Census Data <datasets/census-data>
Chicago Research Data Center <datasets/chicago-research-data-center>
Compustat Global <datasets/compustat-global>
Compustat North America <datasets/compustat-north-america>
Comscore <datasets/comscore>
Cotality (formerly CoreLogic) <datasets/cotality>
Datastream <datasets/datastream>
DealScan (LSTA/LPC) <datasets/dealscan--lsta-lpc->
Direct Marketing Educational Foundation (DMEF) <datasets/direct-marketing-educational-foundation--dmef->
Dow Jones Averages & Total Return Indexes <datasets/dow-jones-averages-&-total-return-indexes>
EDGAR <datasets/edgar>
EDGAR Online <datasets/edgar-online>
Economatica <datasets/economatica>
Emerging Markets Database <datasets/emerging-markets-database>
Equifax <datasets/equifax>
ExecuComp <datasets/execucomp>
FTSE/Russell <datasets/ftse-russell>
FactSet <datasets/factset>
Fama-French Portfolios and Factors <datasets/fama-french-portfolios-and-factors>
Federal Reserve Bank Reports <datasets/federal-reserve-bank-reports>
First Call Historical Database <datasets/first-call-historical-database>
Florida AHCA Inpatient Discharge Data <datasets/florida-ahca-inpatient-discharge-data>
Forrester Research <datasets/forrester-research>
Global Financial Database <datasets/global-financial-database>
HCUP NIS <datasets/hcup-nis>
HCUP SID <datasets/hcup-sid>
Health and Retirement Study <datasets/health-and-retirement-study>
I/B/E/S Earnings Estimate History <datasets/i-b-e-s-earnings-estimate-history>
ICPSR <datasets/icpsr>
IMF International Financial Statistics <datasets/imf-international-financial-statistics>
IRI Marketing FactBook <datasets/iri-marketing-factbook>
ISS Dilution Data <datasets/iss-dilution-data>
ISS Directors Data <datasets/iss-directors-data>
ISS Governance Data <datasets/iss-governance-data>
ISS Securities Class Action Services <datasets/iss-securities-class-action-services>
ISS Shareholder Proposals <datasets/iss-shareholder-proposals>
ISS Voting Analytics <datasets/iss-voting-analytics>
ISSM Transactions File Database <datasets/issm-transactions-file-database>
Institute for Financial Markets <datasets/institute-for-financial-markets>
LIFFE Tick Data <datasets/liffe-tick-data>
Levin Associates Health Care Acquisition Reports <datasets/levin-associates-health-care-acquisition-reports>
L2 VM2 Uniform <datasets/l2-vm2-uniform>
Lipper Hedge Fund <datasets/lipper-hedge-fund>
MSCI (formerly KLC and GMI Ratings) <datasets/msci--formerly-klc-and-gmi-ratings->
MSRB (Municipal Securities Transaction Data) <datasets/msrb--municipal-securities-transaction-data->
Mergent FISD <datasets/mergent-fisd>
Mergent Investext <datasets/mergent-investext>
NAIC Financial Statement Data <datasets/naic-financial-statement-data>
NAIC Health Insurance Data <datasets/naic-health-insurance-data>
NAIC Property/Casualty Insurance Data <datasets/naic-property-casualty-insurance-data>
New York SPARCS Inpatient Databases <datasets/new-york-sparcs-inpatient-databases>
Nielsen Marketing Data <datasets/nielsen-marketing-data>
Numerator <datasets/numerator>
OTC Markets <datasets/otc-markets>
OpenAlex <datasets/openalex>
OptionMetrics Ivy DB <datasets/optionmetrics-ivy-db>
PATSTAT <datasets/patstat>
Philadelphia Stock Exchange (PHLX) <datasets/philadelphia-stock-exchange--phlx->
Proxycurl <datasets/proxycurl>
R&C Futures Data <datasets/r&c-futures-data>
RCA <datasets/rca>
RavenPack News Analytics <datasets/ravenpack-news-analytics>
Refinitiv ESG <datasets/refinitiv-esg>
Research Quotient <datasets/research-quotient>
RiskMetrics CEPD <datasets/riskmetrics-cepd>
RiskMetrics Intangible Value Assessment <datasets/riskmetrics-intangible-value-assessment>
SDC Platinum <datasets/sdc-platinum>
SNL <datasets/snl>
Social Science Research Network <datasets/social-science-research-network>
TRACE <datasets/trace>
Taxi <datasets/taxi>
Thomson Institutional (13F) and Mutual Fund (S12) Holdings <datasets/thomson-institutional--13f--and-mutual-fund--s12--holdings>
Trade and Quote Database <datasets/trade-and-quote-database>
Value Line <datasets/value-line>
Web of Science <datasets/web-of-science>
Zacks <datasets/zacks>
```
