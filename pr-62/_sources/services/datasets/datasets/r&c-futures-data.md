# R&C Futures Data

## At a Glance

| | |
|---|---|
| **Provider** | R&C |
| **Coverage** | ~1959–2004 (varies by commodity) |
| **Geographic scope** | Global |
| **Update frequency** | Archival |
| **Access platforms** | KLC |
| **Eligible users** | Kellogg faculty and doctoral students |
| **Questions** | [rs@kellogg.northwestern.edu](mailto:rs@kellogg.northwestern.edu) |

## Description

The R&C historical futures dataset includes both end-of-day and intraday data covering 80 global commodities.

**Historical End-of-Day Futures** cover 80 global commodities with actual contract data and continuous contracts. Files are in plain ASCII format with fields: Date, Open, High, Low, Close, Volume, and Open Interest. Coverage varies by commodity; some series (e.g., Cocoa) date back to 1959. Most commodity series end in 2003.

**Intraday Futures** cover six index futures series through August 2004:

| Series | Description | Start |
|---|---|---|
| sp | S&P 500 Futures (tick data) | 1982 |
| dj | Dow Jones Futures (tick data) | 1998 |
| nd | NASDAQ 100 Futures (tick data) | 1998 |
| us | Thirty-Year Bond Futures (tick data) | 1978 |
| minisp | Mini S&P 500 Futures (1-min.) | 1998 |
| minind | Mini NASDAQ 100 Futures (1-min.) | 1998 |

Variables for intraday data: Date, Time, Open, High, Low, Close. **Note:** Volume and open interest columns are present in intraday files but contain internal programming codes only — they do not represent actual volume or open interest.

## Access

R&C futures data are available to current Kellogg faculty and doctoral students on the Kellogg Linux Cluster (KLC) at `/kellogg/data/rcfuture`. Files are in comma-delimited flat ASCII format with headers.

### Historical End-of-Day Futures

Data are organized into 80 subdirectories by ticker symbol. Each subdirectory contains actual contract series for that commodity. File names are formed from the ticker symbol, the last two digits of the year, and the contract month code (e.g., March 1992 Corn = `c/c92h.txt`).

The [list of symbols by alphabetical order](https://nuwildcat.sharepoint.com/:x:/s/KSM-RSDataDocumentation/EdS-AnPEBWxDpR80w0u3cKYBA-W9-F4MogKeGKahlp1GvQ?e=B79k2W) is available as an Excel sheet.

Example file format:

```text
"Date","Open","High","Low","Close","Volume","OpenInt"
02/05/1997,192.25,192.50,191.75,192.00,3500,18300
```

### Intraday Futures

The `intraday` directory contains six subdirectories by index futures commodity (sp, dj, nd, us, minisp, minind). Each is further grouped by time interval: 15-minute, 10-minute, 5-minute, end-of-day, and tick-by-tick. File names are formed from the index symbol, an underscore, the last two digits of the year, and the contract month code (e.g., June 2000 S&P 500 tick data = `/intraday/sp/tick/sp_00m.txt`).

Example file format:

```text
"DATE","TIME","OTHER","OPEN","HIGH","LOW","CLOSE","VOLUME","OI"
19990712,1040,"DJ_00H",11500.00,11500.00,11500.00,11500.00,1,0
```

### Continuous Contracts

Continuous contracts are in `/kellogg/data/rcfutures/cont_contract`. The record layout is the same as the historical daily futures data.

### Contract Month Codes

| Code | Month | Code | Month |
|---|---|---|---|
| F | January | N | July |
| G | February | Q | August |
| H | March | U | September |
| J | April | V | October |
| K | May | X | November |
| M | June | Z | December |

## Data Coverage & Key Identifiers

| Attribute | Value |
|---|---|
| **Time period** | ~1959–2004 (varies by commodity) |
| **Geographic coverage** | Global |
| **Unit of observation** | Contract-day (end-of-day); contract-tick or contract-interval (intraday) |
| **Primary identifier** | Ticker symbol + contract month code |
| **Commonly linked via** | TBD |
| **Key variables** | Date, Open, High, Low, Close, Volume, Open Interest |
