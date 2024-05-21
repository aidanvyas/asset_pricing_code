# Data Extraction Instructions

## Link to data: [WRDS Compustat Fundamentals Annual](https://wrds-www.wharton.upenn.edu/pages/get-data/compustat-capital-iq-standard-poors/compustat/north-america-daily/fundamentals-annual/)

### Select:
- **Choose your date range:**
  - `datedate`, `1962-01`, `2022-12`
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

### Save as: `data/raw_comp_funda.csv`

---

## Link to data: [WRDS CRSP Monthly Stock File](https://wrds-www.wharton.upenn.edu/pages/get-data/center-research-security-prices-crsp/annual-update/stock-version-2/monthly-stock-file/)

### Select:
- **Choose your date range:**
  - `1925-12-31`, `2022-12-30`
- **Apply your company codes:**
  - Search the entire database
- **Choose your query variables:**
  - `PERMNO`, `PERMCO`, `MthCalDt`, `MthRet`, `MthRetx`, `ShrOut`, `MthPrc`
- **Select query output:**
  - `csv`, Uncompressed, `YYYY-MM-DD`

### Save as: `raw_crsp_msf.csv`

---

## Link to data: [WRDS CRSP Names](https://wrds-www.wharton.upenn.edu/pages/get-data/center-research-security-prices-crsp/annual-update/stock-events/names/)

### Select:
- **Apply your company codes:**
  - Search the entire database
- **Choose query variables:**
  - `shrcd`, `exchcd`, `permno`, `nameendt`
- **Select query output:**
  - `csv`, Uncompressed, `YYYY-MM-DD`

### Save as: `raw_crsp_msenames.csv`

---

## Link to data: [WRDS CRSP Delistings](https://wrds-www.wharton.upenn.edu/pages/get-data/center-research-security-prices-crsp/annual-update/stock-events/delist/)

### Select:
- **Choose your date range:**
  - `1926-02`, `2022-12`
- **Apply your company codes:**
  - Search the entire database
- **Choose delisting codes for Delisting events:**
  - Active (`100-199`), Mergers (`200-299`), Exchanges (`300-399`), Liquidations (`400-499`), Dropped (`500-599`), Expirations (`600-699`), Domestics that became Foreign (`900-999`)
- **Choose query variables:**
  - `permno`, `dlret`, `dlstdt`, `dlstcd`
- **Select query output:**
  - `csv`, Uncompressed, `YYYY-MM-DD`

### Save as: `raw_crsp_msedelist.csv`

- Note: There are some errors redownloading this data. It is unclear what is causing them as this worked before.

---

## Link to data: [WRDS CRSP/Compustat Merged](https://wrds-www.wharton.upenn.edu/pages/get-data/center-research-security-prices-crsp/annual-update/crspcompustat-merged/compustat-crsp-link/)

### Select:
- **Apply your company codes:**
  - Search the entire database
- **Linking Options:**
  - `LC`, `LU`
- **Choose query variables:**
  - `gvkey`, `lpermno`, `linktype`, `linkprim`, `linkdt`, `linkenddt`
- **Select query output:**
  - `csv`, Uncompressed, `YYYY-MM-DD`

### Save as: `raw_crsp_ccmxpf_linktable.csv`
