# Data Download Instructions

## Download this dataset: [WRDS Compustat Fundamentals Annual](https://wrds-www.wharton.upenn.edu/pages/get-data/compustat-capital-iq-standard-poors/compustat/north-america-daily/fundamentals-annual)

### Select:
- **Choose your date range:**
  - `datedate`, `1957-01`, `2022-12`
- **Apply your company codes:**
  - Search the entire database
- **Screening Variables (Select at least one per line):**
  - Consolidation Level -> `C`
  - Industry Format -> `INDL`
  - Data Format -> `STD`
  - Population Source -> `D`
  - Currency -> `USD`
  - Company Status -> `A`, `I`
- **Choose variable types:**
  - Select Variables Type -> `Data Items`
  - Select -> `All`
- **Select query output:**
  - `csv`, `Uncompressed`, `YYYY-MM-DD`
- **Press `Submit Form`**
- **Download the Output File**

### Drag and drop the file into the data folder as `raw_compustat_fundamentals_annual.csv`

---

## Download this dataset: [WRDS CRSP Monthly Stock File](https://wrds-www.wharton.upenn.edu/pages/get-data/center-research-security-prices-crsp/annual-update/stock-version-2/monthly-stock-file)

### Select:
- **Choose your date range:**
  - `1958-07-31`, `2022-12-30`
- **Apply your company codes:**
  - Search the entire database
- **Choose your query variables:**
  - Select -> `All`
- **Select query output:**
  - `csv`, `Uncompressed`, `YYYY-MM-DD`
- **Press `Submit Form`**
- **Download the Output File**

### Drag and drop the file into the data folder as `raw_crsp_monthly_stock_files.csv`

---

## Download this dataset: [WRDS CRSP Names](https://wrds-www.wharton.upenn.edu/pages/get-data/center-research-security-prices-crsp/annual-update/stock-events/names)

### Select:
- **Apply your company codes:**
  - Search the entire database
- **Choose query variables:**
  - Select -> `All`
- **Select query output:**
  - `csv`, `Uncompressed`, `YYYY-MM-DD`
- **Press `Submit Form`**
- **Download the Output File**

### Drag and drop the file into the data folder as `raw_crsp_historical_descriptive_information.csv`

---

## Download this dataset: [WRDS CRSP Delistings](https://wrds-www.wharton.upenn.edu/pages/get-data/center-research-security-prices-crsp/annual-update/stock-events/delist)

### Select:
- **Choose your date range:**
  - `1926-02`, `2022-12`
- **Apply your company codes:**
  - Search the entire database
- **Choose delisting codes for Delisting events:**
  - `Active (`100-199)`, `Mergers (200-299)`, `Exchanges (300-399)`, `Liquidations (400-499)`, `Dropped (500-599)`, `Expirations (600-699)`, `Domestics that became Foreign (900-999)`
- **Choose query variables:**
  - Select -> `All`
- **Select query output:**
  - `csv`, `Uncompressed`, `YYYY-MM-DD`
- **Press `Submit Form`**
- **Download the Output File**

### Drag and drop the file into the data folder as `raw_crsp_delisting_information.csv`

---

## Download this dataset: [WRDS CRSP/Compustat Merged](https://wrds-www.wharton.upenn.edu/pages/get-data/center-research-security-prices-crsp/annual-update/crspcompustat-merged/compustat-crsp-link)

### Select:
- **Apply your company codes:**
  - Search the entire database
- **Linking Options:**
  - `LC`, `LU`
- **Choose query variables:**
  - Select -> `All`
- **Select query output:**
  - `csv`, `Uncompressed`, `YYYY-MM-DD`
- **Press `Submit Form`**
- **Download the Output File**

### Drag and drop the file into the data folder as `raw_crsp_compustat_linking_table.csv`