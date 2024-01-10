"""
A special thank you to Qingyi (Freda) Song Drechsler whose code on WRDS served as the base of this implementation.
And to THEIS INGERSLEV JENSEN, BRYAN KELLY, and LASSE HEJE PEDERSEN whose "Is There A Replication Crisis in Finance?" appendix contained useful definitions which are employed here.
"""

# Import the necessary libraries
import pandas as pd
import numpy as np
import time
from pandas.tseries.offsets import MonthEnd, YearEnd
from scipy import stats


def sz_bucket(row):
    """
    Helper function to assign a stock to the correct size bucket.
    """
    if row['me'] == np.nan:
        value = ''
    elif row['me'] <= row['sizemedn']:
        value = 'S'
    else:
        value = 'B'
    return value


def factor_bucket(row, factor):
    """
    Helper function to assign a stock to the correct factor bucket.
    """
    if row[factor] <= row['30%']:
        value = 'L'
    elif row[factor] <= row['70%']:
        value = 'M'
    elif row[factor] > row['70%']:
        value = 'H'
    else:
        value = ''
    return value


def wavg(group, avg_name, weight_name):
    """
    Helper function to calculate value-weighted returns.
    """
    d = group[avg_name]
    w = group[weight_name]
    try:
        return (d * w).sum() / w.sum()
    except ZeroDivisionError:
        return np.nan


def calculate_book_equity(comp):
    """
    Helper function to calculate book equity.
    This function contains a variety of Compustat variable abbreviations and acronyms, which might cause confusion.
    To rememedy this, the full Compustat names will be included here:
    - pstkrv: Preferred Stock - Redemption Value
    - pstkl: Preferred Stock - Liquidating Value
    - pstk: Preferred/Preference Stock (Capital) - Total
    - seq: Stockholders Equity - Parent
    - ceq: Common/Ordinary Equity - Total
    - at: Assets - Total
    - lt: Liabilities - Total
    - txditc: Deferred Taxes and Investment Tax Credit
    - txdb: Deferred Taxes (Balance Sheet)
    - itcb: Investment Tax Credit (Balance Sheet)
    """

    # PSTK = pstkrv, if missing use pstkl, if missing use pstk.
    comp['PSTK'] = np.where(
        comp['pstkrv'].isnull(),
        np.where(comp['pstkl'].isnull(), comp['pstk'], comp['pstkl']),
        comp['pstkrv']
    )

    # SEQ = seq, if missing use ceq + PSTK, if PSTK missing, set to 0, if ceq missing, use at - lt.
    comp['SEQ'] = np.where(
        comp['seq'].isnull(),
        np.where(
            (comp['ceq'] + np.where(comp['PSTK'].isnull(), 0, comp['PSTK'])).isnull(),
            comp['at'] - comp['lt'],
            comp['ceq'] + np.where(comp['PSTK'].isnull(), 0, comp['PSTK'])
        ),
        comp['seq']
    )

    # TXDITC = txditc, if missing use txdb + itcb.
    comp['TXDITC'] = np.where(
        comp['txditc'].isnull(),
        comp['txdb'] + comp['itcb'],
        comp['txditc']
    )

    # be = SEQ + TXDITC - PSTK, if TXDITC, PSTK are missing, set to 0.
    be = comp['SEQ'] + np.where(comp['TXDITC'].isnull(), 0, comp['TXDITC']) - np.where(comp['PSTK'].isnull(), 0, comp['PSTK'])

    # Return book equity.
    return be


def calculate_operating_profitability(comp):
    """
    Helper function to calculate operating profitability.
    This function contains a variety of Compustat variable abbreviations and acronyms, which might cause confusion.  
    To rememedy this, the full Compustat names will be included here:
    - sale: Sales/Turnover (Net)
    - revt: Revenue - Total
    - xopr: Operating Expenses - Total
    - cogs: Cost of Goods Sold
    - xsga: Selling, General and Administrative Expense
    - gp: Gross Profit (Loss)
    - ebitda: Earnings Before Interest
    - oibdp: Operating Income Before Depreciation
    - xint: Interest and Related Expense - Total
    - pstkrv: Preferred Stock - Redemption Value
    - pstkl: Preferred Stock - Liquidating Value
    - pstk: Preferred/Preference Stock (Capital) - Total
    - seq: Stockholders Equity - Parent
    - ceq: Common/Ordinary Equity - Total
    - at: Assets - Total
    - lt: Liabilities - Total
    - txditc: Deferred Taxes and Investment Tax Credit
    - txdb: Deferred Taxes (Balance Sheet)
    - itcb: Investment Tax Credit (Balance Sheet)
    """
    
    # SALE = sale, if missing use revt
    comp['SALE'] = np.where(
        comp['sale'].isnull(),
        comp['revt'],
        comp['sale']
    )

    # OPEX = xopr, if missing use cogs + xsga
    comp['OPEX'] = np.where(
        comp['xopr'],
        comp['cogs'] + comp['xsga'],
        comp['xopr']
    )

    # GP = gp, if missing use SALE - cogs
    comp['GP'] = np.where(
        comp['gp'].isnull(),
        comp['SALE'] - comp['cogs'],
        comp['gp']
    )

    # EBITDA = ebitda, if missing use oibdp, if missing use SALE - OPEX, if missing use GP - xsga
    comp['EBITDA'] = np.where(
        comp['ebitda'].isnull(),
        np.where(
            comp['oibdp'].isnull(),
            np.where(
                (comp['SALE'] - comp['OPEX']).isnull(),
                comp['GP'] - comp['xsga'],
                comp['SALE'] - comp['OPEX']
            ),
            comp['oibdp']),
        comp['ebitda']
    )

    # OP = EBITDA - xint
    comp['OP'] = comp['EBITDA'] - comp['xint']

    # PSTK = pstkrv, if missing use pstkl, if missing use pstk
    comp['PSTK'] = np.where(
        comp['pstkrv'].isnull(),
        np.where(
            comp['pstkl'].isnull(),
            comp['pstk'],
            comp['pstkl']
        ),
        comp['pstkrv']
    )

    # SEQ = seq, if missing use ceq + PSTK*, if PSTK* missing, set to 0, if ceq missing, use at - lt
    comp['SEQ'] = np.where(
        comp['seq'].isnull(),
        np.where(
            (comp['ceq'] + np.where(comp['PSTK'].isnull(), 0, comp['PSTK'])).isnull(),
            comp['at'] - comp['lt'],
            comp['ceq'] + np.where(comp['PSTK'].isnull(), 0, comp['PSTK'])
        ),
        comp['seq']
    )

    # TXDITC = txditc, if missing use txdb + itcb
    comp['TXDITC'] = np.where(
        comp['txditc'].isnull(),
        comp['txdb'] + comp['itcb'],
        comp['txditc']
    )

    # Book Equity = SEQ* + TXDITC* - PSTK*, if TXDITC*, PSTK* are missing, set to 0
    comp['BE'] = comp['SEQ'] + np.where(comp['TXDITC'].isnull(), 0, comp['TXDITC']) - np.where(comp['PSTK'].isnull(), 0, comp['PSTK'])

    # Operating profitability = OP / BE.
    op_be = comp['OP'] / comp['BE']

    # Return operating profitability.
    return op_be


def calculate_investment(comp):
    """
    Helper function to calculate investment.
    This function contains a Compustat variable acronyms, which might cause confusion.  
    To rememedy this, the full Compustat name is included here:
    - at: Assets - Total
    """

    # Sort the dataframe by company and then date.
    comp = comp.sort_values(by=['gvkey', 'datadate'])

    # Calculate investment which is the percent change in total assets.
    investment = comp.groupby('gvkey')['at'].pct_change()

    # Return investment.
    return investment
    

def process_compustat_data():
    """
    Link to data: https://wrds-www.wharton.upenn.edu/pages/get-data/compustat-capital-iq-standard-poors/compustat/north-america-daily/fundamentals-annual/
    Select:
        - Choose your date range
            - datedate, 1950-06, 2022-12
        - Apply your company codes
            - Search the entire database
        - Screening Variables (Select at least one per line)
            - Consolidation Level -> C
            - Industry Format -> INDL
            - Data Format -> STD
            - Population Source -> D
            - Currency -> USD
            - Company Status -> A, I
        - Choose variable types
            - Data Items
            - gvkey, seq, ceq, at, lt, pstkrv, pstkl, pstk, txditc, txdb, itcb, xint, ebitda, oibdp, xsga,
            sale, revt, xopr, cogs, gp, capx, oancf, dp, wcap, ib, ni, txt, mii, xido, xi,
            do, pi, spi, nopi, ebit, oiadp, che, act, rect, invt, aco, dlc, lct, ap, txp, lco,
            ivao, dltt, lo, xrd
            - Note this is only for size, be_me, op_be, asset growth, cop_at, fcf_ev
        - Select query output
            - csv, Uncompressed, YYYY-MM-DD
        Save as: 'raw_comp_funda.csv'
    """

    # Read in the csv file.
    comp = pd.read_csv('raw_comp_funda.csv', parse_dates=['datadate'])

    # Create a year column.
    comp['year'] = comp['datadate'].dt.year
    
    # Sort the dataframe by gvkey (company code) and then date.
    comp = comp.sort_values(by=['gvkey', 'datadate'])

    # Create a count column which equals the number of times that company has appeared in the dataframe.
    comp['count'] = comp.groupby(['gvkey']).cumcount()

    # Drop the unnecessary columns.
    comp.drop(['fyear', 'indfmt', 'consol', 'popsrc', 'datafmt', 'tic', 'curcd', 'costat'], axis=1, inplace=True)

    # Save the dataframe to a csv.
    comp.to_csv('processed_comp_funda.csv', index = False)


def process_crsp_data():
    """
    Link to data: https://wrds-www.wharton.upenn.edu/pages/get-data/center-research-security-prices-crsp/annual-update/stock-version-2/monthly-stock-file/
    Select:
        - Choose your date range
            - 1959-01-01, 2022-12-30
        - Apply your company codes
            - Search the entire database
        - Choose your query variables
            - PERMNO, PERMCO, MthCalDate, MthRet, MthRetx, ShrOut, MthPrc
        - Select query output
            - csv, Uncompressed, YYYY-MM-DD
    Save as: 'raw_crsp_msf.csv'

    Link to data: https://wrds-www.wharton.upenn.edu/pages/get-data/center-research-security-prices-crsp/annual-update/stock-events/names/
    Select:
        - Apply your company codes
            - Search the entire database
        - Choose query variables
            - shrcd, exchcd, permno, nameendt
        - Select query output
            - csv, Uncompressed, YYYY-MM-DD
    Save as: 'raw_crsp_msenames.csv'

    Link to data: https://wrds-www.wharton.upenn.edu/pages/get-data/center-research-security-prices-crsp/annual-update/stock-version-2/delisting-information/
    Select:
        - Choose your date range
            - 1959-01-01, 2022-12-29
        - Apply your company codes
            - Search the entire database
        - Choose delisting corporate action type
            - Dropped, Exchange, Liquidation, Lost Source, Merger
        - Choose query variables
            - permno, delret, delistingdt
        - Select query output
            - csv, Uncompressed, YYYY-MM-DD
    Save as: 'raw_crsp_msedelist.csv'
    """

    # Read in the csv files.
    msf = pd.read_csv('raw_crsp_msf.csv', parse_dates = ['MthCalDt'])
    msenames = pd.read_csv('raw_crsp_msenames.csv', parse_dates = ['DATE', 'NAMEENDT'])
    dlret = pd.read_csv('raw_crsp_msedelist.csv', parse_dates = ['DelistingDt'])

    # Merge the monthly stock files and names dataframes together.
    crsp_m = pd.merge(msf, msenames, left_on = 'PERMNO', right_on = 'PERMNO', how = 'left')

    # Filter the data such that the dates are in the correct range.
    crsp_m = crsp_m[(crsp_m['NAMEENDT'] >= crsp_m['MthCalDt']) & 
                    (crsp_m['MthCalDt'] >= crsp_m['DATE']) &
                    (crsp_m['MthCalDt'] >= pd.to_datetime('1959-01-01')) & 
                    (crsp_m['MthCalDt'] <= pd.to_datetime('2022-12-30'))]

    # Filter the data such that we only get NYSE, NASDAQ, and AMEX stocks.
    crsp_m = crsp_m[(crsp_m['EXCHCD'].between(1, 3))]
    
    # Change the variable format to int.
    crsp_m[['PERMCO', 'PERMNO', 'SHRCD', 'EXCHCD']] = crsp_m[['PERMCO', 'PERMNO', 'SHRCD', 'EXCHCD']].astype(int)
    dlret['PERMNO'] = dlret['PERMNO'].astype(int)

    # Line up the dates to be at the end of the month.
    crsp_m['jdate'] = crsp_m['MthCalDt'] + MonthEnd(0)
    dlret['jdate'] = dlret['DelistingDt'] + MonthEnd(0)

    # Merge all of the CRSP dataframes together.
    crsp = pd.merge(crsp_m, dlret, how='left', on=['PERMNO', 'jdate'])

    # Set the NaN returns to 0.
    crsp['DelRet'] = crsp['DelRet'].fillna(0)
    crsp['MthRet'] = crsp['MthRet'].fillna(0)

    # Calculate the delisting adjusted-returns.
    crsp['retadj']=(1 + crsp['MthRet']) * (1 + crsp['DelRet']) - 1

    # Calculate market equity.
    crsp['me'] = crsp['MthPrc'].abs() * crsp['ShrOut'] 

    # Remove unnecessary columns.
    crsp = crsp.drop(['DelRet', 'DelistingDt', 'MthPrc', 'ShrOut'], axis=1)

    # Sort the values by company code (jdate, PERMCO) and then market equity.
    crsp = crsp.sort_values(by = ['jdate', 'PERMCO', 'me'])

    # Sum the market caps for different securities (PERMNO) within the same company (PERMCO) for each date.
    crsp_summe = crsp.groupby(['jdate', 'PERMCO'])['me'].sum().reset_index()

    # Find the largest market cap for a given date and PERMCO.
    crsp_maxme = crsp.groupby(['jdate', 'PERMCO'])['me'].max().reset_index()

    # Merge the max market cap dataframe with our CRSP dataframe such that each company / date pair aligns with the max market cap, in essence, only keeping the primary security. 
    crsp1 = pd.merge(crsp, crsp_maxme, how='inner', on=['jdate', 'PERMCO', 'me'])

    # Drop the market equity column.
    crsp1 = crsp1.drop(['me'], axis=1)

    # Merge the summed market cap dataframe with the dataframe 'crsp1' which has the primary securities, such that the summed market cap is assigned to the primary security.
    crsp2 = pd.merge(crsp1, crsp_summe, how = 'inner', on = ['jdate', 'PERMCO'])

    # Sort by PERMNO and then date, and after that, drop the duplicates.
    crsp2 = crsp2.sort_values(by = ['PERMNO', 'jdate']).drop_duplicates()

    # Create columns representing the year and the month.
    crsp2['year'] = crsp2['jdate'].dt.year
    crsp2['month'] = crsp2['jdate'].dt.month

    # Create a new dataframe with only the December data.
    decme = crsp2[crsp2['month'] == 12]

    # Keep only the essential columns and then rename 'me' to 'dec_me'.
    decme = decme[['PERMNO', 'MthCalDt', 'jdate', 'me', 'year']].rename(columns = {'me': 'dec_me'})

    # Create columns for the Fama-French date, year, and month.
    crsp2['ffdate'] = crsp2['jdate'] + MonthEnd(-6)
    crsp2['ffyear'] = crsp2['ffdate'].dt.year
    crsp2['ffmonth'] = crsp2['ffdate'].dt.month

    # Create a columnn '1+retx' for ease of calculations.
    crsp2['1+retx'] = 1 + crsp2['MthRetx']

    # Create a column for the cumulative return of each stock in each Fama-French year.
    crsp2['cumretx'] = crsp2.groupby(['PERMNO', 'ffyear'])['1+retx'].cumprod()

    # Create a column for the lagged cumulative return.
    crsp2['lcumretx'] = crsp2.groupby(['PERMNO'])['cumretx'].shift(1)

    # Sort the dataframe by company and then date.
    crsp2 = crsp2.sort_values(by = ['PERMNO', 'MthCalDt'])

    # Create a column for the lagged market cap.
    crsp2['lme'] = crsp2.groupby(['PERMNO'])['me'].shift(1)

    # Create a count column which equals the number of times that company has appeared in the dataframe.
    crsp2['count'] = crsp2.groupby(['PERMNO']).cumcount()

    # If this is the first time the company appears in the dataframe, then we need to input the correct lagged market cap, else, we should stick with the current lagged market cap.
    crsp2['lme'] = np.where(crsp2['count'] == 0, crsp2['me'] / crsp2['1+retx'], crsp2['lme'])

    # Create a new dataframe that only includes months at the beginning of a Fama-French year.
    mebase = crsp2[crsp2['ffmonth'] == 1][['PERMNO', 'ffyear', 'lme']].rename(columns={'lme': 'mebase'})

    # Merge in the 'mebase' dataframe into our main 'crsp2' dataframe.
    crsp3 = pd.merge(crsp2, mebase, how = 'left', on = ['PERMNO', 'ffyear'])

    # Create a weight column that equals the lagged market equity for any given month.
    crsp3['wt'] = np.where(crsp3['ffmonth'] == 1, crsp3['lme'], crsp3['mebase'] * crsp3['lcumretx'])

    # Increment the year column by 1.
    decme['year'] = decme['year'] + 1

    # Keep only the essential columns.
    decme = decme[['PERMNO', 'year', 'dec_me']]

    # Create a dataframe with only the data from June.
    crsp3_jun = crsp3[crsp3['month'] == 6]

    # Merge the June and December dataframes.
    crsp_jun = pd.merge(crsp3_jun, decme, how = 'inner', on = ['PERMNO', 'year'])

    # Keep only the essential columns.
    crsp_jun = crsp_jun[['PERMNO', 'MthCalDt', 'jdate', 'SHRCD', 'EXCHCD', 'retadj', 'me', 'wt', 'cumretx', 'mebase', 'lme', 'dec_me']]

    # Sort the June dataframe by PERMNO and then date, and after that, drop the duplicates.
    crsp_jun = crsp_jun.sort_values(by = ['PERMNO', 'jdate']).drop_duplicates()

    # Save the dataframea to csv files.
    crsp_jun.to_csv('processed_crsp_jun.csv', index = False)
    crsp3.to_csv('processed_crsp_data.csv', index = False)


def process_ccm_data():
    """
    Link to data: https://wrds-www.wharton.upenn.edu/pages/get-data/center-research-security-prices-crsp/annual-update/crspcompustat-merged/compustat-crsp-link/
    Select:
        - Apply your company codes
            - Search the entire database
        - Linking Options
            - LC, LU
        - Choose query variables
            - gvkey, lpermno, linktype, linkprim, linkdt, linkenddt
        - Select query output
            - csv, Uncompressed, YYYY-MM-DD
    Save as: 'raw_crsp_ccmxpf_linktable.csv'
    """

    # Read in the csv files.
    ccm = pd.read_csv('raw_crsp_ccmxpf_linktable.csv', parse_dates=['LINKDT'])
    comp = pd.read_csv('processed_comp_funda.csv')
    crsp_jun = pd.read_csv('processed_crsp_jun.csv', parse_dates=['jdate'])

    # Keep only the primary securities.
    ccm = ccm[(ccm['LINKPRIM'] == 'C') | (ccm['LINKPRIM'] == 'P')]

    # Rename LPERMNO to PERMNO to be consistent with the other dataframes.
    ccm = ccm.rename(columns={'LPERMNO': 'PERMNO'})

    # If the stock still trades, set the date to NaN.
    ccm['LINKENDDT'] = ccm['LINKENDDT'].replace('E', np.nan)

    # If the LINKENDDT is NaN, then we set it to today's date.
    ccm['LINKENDDT'] = ccm['LINKENDDT'].fillna(pd.to_datetime('today'))

    # Merge the Compustat data with the CRSP linking table.
    ccm1 = pd.merge(comp, ccm, how='left', on=['gvkey'])

    # Parse the date columns as datetime objects.
    ccm1['datadate'] = pd.to_datetime(ccm1['datadate'])
    ccm1['LINKENDDT'] = pd.to_datetime(ccm1['LINKENDDT'])

    # Create yearend and June date columns.
    ccm1['yearend'] = ccm1['datadate'] + YearEnd(0)
    ccm1['jdate'] = ccm1['yearend'] + MonthEnd(6)

    # Set the link date bounds and create a copy of the dataframe.
    ccm2 = ccm1[(ccm1['jdate'] >= ccm1['LINKDT']) & (ccm1['jdate'] <= ccm1['LINKENDDT'])].copy()

    # Drop the unnecessary columns.
    ccm2.drop(['LINKPRIM', 'LIID', 'LINKTYPE', 'LPERMCO', 'LINKDT', 'LINKENDDT'], axis=1, inplace=True)

    # Change the variable type to int.
    crsp_jun['PERMNO'] = crsp_jun['PERMNO'].astype(int)
    ccm2['PERMNO'] = ccm2['PERMNO'].astype(int)

    # Parse the June date column as a datetime object.
    ccm2['jdate'] = pd.to_datetime(ccm2['jdate'])

    # Merge the combined CRSP linking table and Compustat data with the CRSP june date.
    ccm_jun = pd.merge(crsp_jun, ccm2, how='inner', on=['PERMNO', 'jdate'])

    # Save the dataframe to a csv.
    ccm_jun.to_csv('processed_crsp_jun1.csv', index=False)


def compute_rm():
    """
    This function computes the Rm factor which is the total rate of return of the market.
    """

    # Read in the csv files.
    ccm_jun = pd.read_csv('processed_crsp_jun1.csv', parse_dates=['jdate'])
    crsp3 = pd.read_csv('processed_crsp_data.csv', low_memory=False)

    # Select the correct universe of stocks.
    universe = ccm_jun[(ccm_jun['me'] > 0) & 
                   (ccm_jun['dec_me'] > 0) &
                   (ccm_jun['count'] >= 1) & 
                   ((ccm_jun['SHRCD'] == 10) | (ccm_jun['SHRCD'] == 11))]
    
    # Create a new dataframe with only the essential columns as of June. 
    june = universe[['PERMNO', 'MthCalDt', 'jdate']].copy()

    # Create a column representing the Fama-French year.
    june['ffyear'] = june['jdate'].dt.year

    # Keep only the essential columns.
    crsp3 = crsp3[['MthCalDt', 'PERMNO', 'SHRCD', 'EXCHCD', 'retadj', 'me', 'wt', 'cumretx', 'ffyear', 'jdate']]
    
    # Merge monthly CRSP data with the portfolio assignments in June.
    ccm3 = pd.merge(crsp3, 
                    june[['PERMNO', 'ffyear']],
                    how='left', on=['PERMNO', 'ffyear'])

    # Keep only the common stocks with positive weight.
    ccm4 = ccm3[(ccm3['wt'] > 0) & 
                ((ccm3['SHRCD'] == 10) | (ccm3['SHRCD'] == 11))]
        
    # Create a dataframe for the value-weighted returs.
    vwret = ccm4.groupby(['jdate']).apply(wavg, 'retadj', 'wt').to_frame().reset_index().rename(columns={0: 'vwret'})

    # Rename 'jdate' to 'date' and 'vwret' to 'xRm'.
    vwret = vwret.rename(columns={'jdate': 'date', 'vwret': 'xRm'})

    # Save the dataframe to a csv file.
    vwret.to_csv('processed_rm_factor.csv', index=False)


def compute_hml():
    """
    This function computes the HML factor which is the performance of stocks with high book to market ratios minus the performance of stocks with low book to market ratios.
    """

    # Read in the csv files.
    ccm_jun = pd.read_csv('processed_crsp_jun1.csv', parse_dates=['jdate'])
    crsp3 = pd.read_csv('processed_crsp_data.csv', low_memory=False)

    # Calculate the book equity.
    ccm_jun['be'] = calculate_book_equity(ccm_jun)
    
    # Calculate book to market equity ratio.
    ccm_jun['be_me'] = ccm_jun['be'] * 1000 / ccm_jun['dec_me']

    # Select the universe NYSE common stocks with positive market equity.
    nyse = ccm_jun[(ccm_jun['EXCHCD'] == 1) & 
                   (ccm_jun['me'] > 0) & 
                   (ccm_jun['dec_me'] > 0) &
                   (ccm_jun['count'] >= 1) & 
                   ((ccm_jun['SHRCD'] == 10) | (ccm_jun['SHRCD'] == 11))]
    
    # # Select the universe of stocks for the HML breakpoints.
    # nyse_hml = nyse[(nyse['be'] > 0)]

    # Get the size median breakpoints for each month.
    nyse_size = nyse.groupby(['jdate'])['me'].median().to_frame().reset_index().rename(columns={'me': 'sizemedn'})

    # Get the be_me 30th and 70th percentile breakpoints for each month.
    nyse_be_me = nyse.groupby(['jdate'])['be_me'].describe(percentiles = [0.3, 0.7]).reset_index()
    nyse_bm_me = nyse_be_me[['jdate', '30%', '70%']]

    # Merge the breakpoint dataframes together.
    nyse_breaks = pd.merge(nyse_size, nyse_bm_me, how='inner', on=['jdate'])

    # Merge the breakpoints with the CCM June data.
    ccm1_jun = pd.merge(ccm_jun, nyse_breaks, how='left', on=['jdate'])

    # Assign each stock to its proper size bucket.
    ccm1_jun['szport'] = ccm1_jun.apply(sz_bucket, axis=1)
    
    # Assign each stock to its proper book to market bucket.
    ccm1_jun['factor_portfolio'] = ccm1_jun.apply(lambda row: factor_bucket(row, 'be_me'), axis=1)

    # Create a new dataframe with only the essential columns for storing the portfolio assignments as of June. 
    june = ccm1_jun[['PERMNO', 'MthCalDt', 'jdate', 'szport', 'factor_portfolio']].copy()

    # Create a column representing the Fama-French year.
    june['ffyear'] = june['jdate'].dt.year

    # Keep only the essential columns.
    crsp3 = crsp3[['MthCalDt', 'PERMNO', 'SHRCD', 'EXCHCD', 'retadj', 'me', 'wt', 'cumretx', 'ffyear', 'jdate']]
    
    # Merge monthly CRSP data with the portfolio assignments in June.
    ccm3 = pd.merge(crsp3, 
                    june[['PERMNO', 'ffyear', 'szport', 'factor_portfolio']],
                    how='left', on=['PERMNO', 'ffyear'])

    # Keep only the common stocks with positive weight.
    ccm4 = ccm3[(ccm3['wt'] > 0) & 
                ((ccm3['SHRCD'] == 10) | (ccm3['SHRCD'] == 11))]
        
    # Create a dataframe for the value-weighted returs.
    vwret = ccm4.groupby(['jdate', 'szport', 'factor_portfolio']).apply(wavg, 'retadj', 'wt').to_frame().reset_index().rename(columns={0: 'vwret'})

    # Create a column that represents the combined size, be_me portfolio that the stock is in.
    vwret['size_factor_portfolio'] = vwret['szport'] + vwret['factor_portfolio']

    # Tranpose the dataframes such that the rows are dates and the columns are portfolio returns.
    ff_factors = vwret.pivot(index='jdate', columns=['size_factor_portfolio'], values='vwret').reset_index()

    # Get the average return of the big and small high be_me portfolios.
    ff_factors['xH'] = (ff_factors['BH'] + ff_factors['SH']) / 2

    # Get the average return of the big and small low be_me portfolios.
    ff_factors['xL'] = (ff_factors['BL'] + ff_factors['SL']) / 2

    # Create the HML factor which is the difference between the high and low be_me portfolios.
    ff_factors['xHML'] = ff_factors['xH'] - ff_factors['xL']

    # Get the average return of the high and low small me portfolios.
    ff_factors['xS'] = (ff_factors['SH'] + ff_factors['SM'] + ff_factors['SL']) / 3

    # Get the average returnf of the high and low big me portfolios.
    ff_factors['xB'] = (ff_factors['BH'] + ff_factors['BM'] + ff_factors['BL']) / 3

    # Create the SMB factor based on the HML breakpoints.
    ff_factors['xSHML'] = ff_factors['xS'] - ff_factors['xB']

    # Rename the jdate column to date.
    ff_factors = ff_factors.rename(columns={'jdate': 'date'})
    
    # Save the dataframe to a csv file.
    ff_factors.to_csv('processed_hml_factor.csv', index=False)


def compute_rmw():
    """
    This function computes the RMW factor which is the performance of stocks with high operating profitability minus the performance of stocks with low operating profitability.
    """

    # Read in the csv files.
    ccm_jun = pd.read_csv('processed_crsp_jun1.csv', parse_dates=['jdate'])
    crsp3 = pd.read_csv('processed_crsp_data.csv', low_memory=False)

    # Calculate the book equity and operating profitability.
    ccm_jun['be'] = calculate_book_equity(ccm_jun)
    ccm_jun['op_be'] = calculate_operating_profitability(ccm_jun)
    
    # Select the universe NYSE common stocks with positive market equity.
    nyse = ccm_jun[(ccm_jun['EXCHCD'] == 1) & 
                   (ccm_jun['me'] > 0) & 
                   (ccm_jun['dec_me'] > 0) &
                   (ccm_jun['count'] >= 1) & 
                   ((ccm_jun['SHRCD'] == 10) | (ccm_jun['SHRCD'] == 11))]
    
    # # Select the universe of stocks for the RMW breakpoints.
    # nyse_rmw = nyse[(nyse['be'] > 0) &
    #                 (nyse['revt'].notnull() &
    #                 nyse['cogs'].notnull() | nyse['xsga'].notnull() | nyse['xint'].notnull())]

    # Get the size median breakpoints for each month.
    nyse_size = nyse.groupby(['jdate'])['me'].median().to_frame().reset_index().rename(columns={'me': 'sizemedn'})

    # Get the op_be 30th and 70th percentile breakpoints for each month.
    nyse_op_be = nyse.groupby(['jdate'])['op_be'].describe(percentiles = [0.3, 0.7]).reset_index()
    nyse_op_be = nyse_op_be[['jdate', '30%', '70%']]

    # Merge the breakpoint dataframes together.
    nyse_breaks = pd.merge(nyse_size, nyse_op_be, how='inner', on=['jdate'])

    # Merge the breakpoints with the CCM June data.
    ccm1_jun = pd.merge(ccm_jun, nyse_breaks, how='left', on=['jdate'])

    # Assign each stock to its proper size bucket.
    ccm1_jun['szport'] = ccm1_jun.apply(sz_bucket, axis=1)

    # Assign each stock to its proper book to market bucket.
    ccm1_jun['factor_portfolio'] = ccm1_jun.apply(lambda row: factor_bucket(row, 'op_be'), axis=1)

    # Create a new dataframe with only the essential columns for storing the portfolio assignments as of June. 
    june = ccm1_jun[['PERMNO', 'MthCalDt', 'jdate', 'szport', 'factor_portfolio']].copy()

    # Create a column representing the Fama-French year.
    june['ffyear'] = june['jdate'].dt.year

    # Keep only the essential columns.
    crsp3 = crsp3[['MthCalDt', 'PERMNO', 'SHRCD', 'EXCHCD', 'retadj', 'me', 'wt', 'cumretx', 'ffyear', 'jdate']]
    
    # Merge monthly CRSP data with the portfolio assignments in June.
    ccm3 = pd.merge(crsp3, 
                    june[['PERMNO', 'ffyear', 'szport', 'factor_portfolio']],
                    how='left', on=['PERMNO', 'ffyear'])

    # Keep only the common stocks with positive weight, book and market equity, and are assigned to a portfolio.
    ccm4 = ccm3[(ccm3['wt'] > 0) & 
                ((ccm3['SHRCD'] == 10) | (ccm3['SHRCD'] == 11))]

    # Create a dataframe for the value-weighted returs.
    vwret = ccm4.groupby(['jdate', 'szport', 'factor_portfolio']).apply(wavg, 'retadj', 'wt').to_frame().reset_index().rename(columns={0: 'vwret'})

    # Create a column that represents the combined size, op_be portfolio that the stock is in.
    vwret['size_factor_portfolio'] = vwret['szport'] + vwret['factor_portfolio']

    # Tranpose the dataframes such that the rows are dates and the columns are portfolio returns.
    ff_factors = vwret.pivot(index='jdate', columns=['size_factor_portfolio'], values='vwret').reset_index()

    # Get the average return of the big and small robust op_be portfolios.
    ff_factors['xR'] = (ff_factors['BH'] + ff_factors['SH']) / 2

    # Get the average return of the big and small weak op_be portfolios.
    ff_factors['xW'] = (ff_factors['BL'] + ff_factors['SL']) / 2

    # Create the RMW factor which is the difference between the robust and weak op_be portfolios.
    ff_factors['xRMW'] = ff_factors['xR'] - ff_factors['xW']

    # Get the average return of the robust and weak small me portfolios.
    ff_factors['xS'] = (ff_factors['SH'] + ff_factors['SM'] + ff_factors['SL']) / 3

    # Get the average return of the robust and weak big me portfolios.
    ff_factors['xB'] = (ff_factors['BH'] + ff_factors['BM'] + ff_factors['BL']) / 3

    # Create the SMB factor based on the RMW breakpoints.
    ff_factors['xSRMW'] = ff_factors['xS'] - ff_factors['xB']

    # Rename the jdate column to date.
    ff_factors = ff_factors.rename(columns={'jdate': 'date'})
    
    # Save the dataframe to a csv file.
    ff_factors.to_csv('processed_rmw_factor.csv', index=False)


def compute_cma():
    """
    This function computes the CMA factor which is the performance of stocks with low investment minus the performance of stocks with high investment.
    """

    # Read in the csv files.
    ccm_jun = pd.read_csv('processed_crsp_jun1.csv', parse_dates=['jdate'])
    crsp3 = pd.read_csv('processed_crsp_data.csv', low_memory=False)

    # Calculate investment.
    ccm_jun['investment'] = calculate_investment(ccm_jun)
    
    # Select the universe NYSE common stocks with positive market equity.
    nyse = ccm_jun[(ccm_jun['EXCHCD'] == 1) & 
                   (ccm_jun['me'] > 0) & 
                   (ccm_jun['dec_me'] > 0) &
                   (ccm_jun['count'] >= 1) & 
                   ((ccm_jun['SHRCD'] == 10) | (ccm_jun['SHRCD'] == 11))]
    
    # # Select the universe of stocks for the CMA breakpoints.
    # nyse_cma = nyse[(nyse['at'] > 0)]
    # Lagged 'at' should also be positive.

    # Get the size median breakpoints for each month.
    nyse_size = nyse.groupby(['jdate'])['me'].median().to_frame().reset_index().rename(columns={'me': 'sizemedn'})

    # Get the investment 30th and 70th percentile breakpoints for each month.
    nyse_inv = nyse.groupby(['jdate'])['investment'].describe(percentiles = [0.3, 0.7]).reset_index()
    nyse_inv = nyse_inv[['jdate', '30%', '70%']]

    # Merge the breakpoint dataframes together.
    nyse_breaks = pd.merge(nyse_size, nyse_inv, how='inner', on=['jdate'])

    # Merge the breakpoints with the CCM June data.
    ccm1_jun = pd.merge(ccm_jun, nyse_breaks, how='left', on=['jdate'])

    # # Assign each stock to its proper size bucket.
    ccm1_jun['szport'] = ccm1_jun.apply(sz_bucket, axis=1)

    # # Assign each stock to its proper book to market bucket.
    ccm1_jun['factor_portfolio'] = ccm1_jun.apply(lambda row: factor_bucket(row, 'investment'), axis=1)

    # Create a new dataframe with only the essential columns for storing the portfolio assignments as of June. 
    june = ccm1_jun[['PERMNO', 'MthCalDt', 'jdate', 'szport', 'factor_portfolio']].copy()

    # Create a column representing the Fama-French year.
    june['ffyear'] = june['jdate'].dt.year

    # Keep only the essential columns.
    crsp3 = crsp3[['MthCalDt', 'PERMNO', 'SHRCD', 'EXCHCD', 'retadj', 'me', 'wt', 'cumretx', 'ffyear', 'jdate']]
    
    # Merge monthly CRSP data with the portfolio assignments in June.
    ccm3 = pd.merge(crsp3, 
                    june[['PERMNO', 'ffyear', 'szport', 'factor_portfolio']],
                    how='left', on=['PERMNO', 'ffyear'])

    # Keep only the common stocks with positive weight.
    ccm4 = ccm3[(ccm3['wt'] > 0) & 
                ((ccm3['SHRCD'] == 10) | (ccm3['SHRCD'] == 11))]

    # Create a dataframe for the value-weighted returs.
    vwret = ccm4.groupby(['jdate', 'szport', 'factor_portfolio']).apply(wavg, 'retadj', 'wt').to_frame().reset_index().rename(columns={0: 'vwret'})

    # Create a column that represents the combined size, investment portfolio that the stock is in.
    vwret['size_factor_portfolio'] = vwret['szport'] + vwret['factor_portfolio']

    # Tranpose the dataframes such that the rows are dates and the columns are portfolio returns.
    ff_factors = vwret.pivot(index='jdate', columns=['size_factor_portfolio'], values='vwret').reset_index()

    # Get the average return of the big and small aggressive investment portfolios.
    ff_factors['xA'] = (ff_factors['BH'] + ff_factors['SH']) / 2

    # Get the average return of the big and small conservative investment portfolios.
    ff_factors['xC'] = (ff_factors['BL'] + ff_factors['SL']) / 2

    # Create the CMA factor which is the difference between the conservative and aggressive investment portfolios.
    ff_factors['xCMA'] = ff_factors['xC'] - ff_factors['xA']

    # Get the average return of the conservative and aggressive small me portfolios.
    ff_factors['xS'] = (ff_factors['SH'] + ff_factors['SM'] + ff_factors['SL']) / 3

    # Get the average return of the conservative and aggressive big me portfolios.
    ff_factors['xB'] = (ff_factors['BH'] + ff_factors['BM'] + ff_factors['BL']) / 3

    # Create the SMB factor based on the CMA breakpoints.
    ff_factors['xSCMA'] = ff_factors['xS'] - ff_factors['xB']

    # Rename the jdate column to date.
    ff_factors = ff_factors.rename(columns={'jdate': 'date'})
    
    # Save the dataframe to a csv file.
    ff_factors.to_csv('processed_cma_factor.csv', index=False)


def compare_with_fama_french():
    """
    This function compares the Fama-French factors (Mkt-Rf, SMB, HML, RMW, and CMA) that we have replicated with the original data.
    """

    # Read in the csv file.
    ff = pd.read_csv('raw_fama_french_factors.csv')
    rm = pd.read_csv('processed_rm_factor.csv', parse_dates=['date'])
    hml = pd.read_csv('processed_hml_factor.csv', parse_dates=['date'])
    rmw = pd.read_csv('processed_rmw_factor.csv', parse_dates=['date'])
    cma = pd.read_csv('processed_cma_factor.csv', parse_dates=['date'])
                             
    # Keep only the essential columns.
    ff = ff[['date', 'Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA', 'RF']]

    # Parse the date column in the original Fama-French dataframe.
    ff['date'] = pd.to_datetime(ff['date'], format='%Y%m') + MonthEnd(0)

    # Merge my Fama-French factors with the original Fama-French factors.
    ffcomp = pd.merge(ff, rm[['date', 'xRm']], how='inner', on=['date'])
    ffcomp = pd.merge(ffcomp, hml[['date', 'xHML', 'xSHML']], how='inner', on=['date'])
    ffcomp = pd.merge(ffcomp, rmw[['date', 'xRMW', 'xSRMW']], how='inner', on=['date'])
    ffcomp = pd.merge(ffcomp, cma[['date', 'xCMA', 'xSCMA']], how='inner', on=['date'])

    # Set a date restriction.
    ffcomp63 = ffcomp[ffcomp['date'] >= '07/01/1963']

    # Subtract the risk-free rate from the return of the market.
    ffcomp63['xRm-Rf'] = ffcomp63['xRm'] - ffcomp63['RF'] / 100

    # Create the SMB factor by averaging the difference in returns between small and big stocks based on the other factor portfolios.
    ffcomp63['xSMB'] = (ffcomp63['xSHML'] + ffcomp63['xSRMW'] + ffcomp63['xSCMA']) / 3

    # Print out the correlation between the two datasets.
    print(stats.pearsonr(ffcomp63['Mkt-RF'], ffcomp63['xRm-Rf']))
    print(stats.pearsonr(ffcomp63['SMB'], ffcomp63['xSMB']))
    print(stats.pearsonr(ffcomp63['HML'], ffcomp63['xHML']))
    print(stats.pearsonr(ffcomp63['RMW'], ffcomp63['xRMW']))
    print(stats.pearsonr(ffcomp63['CMA'], ffcomp63['xCMA']))

    # Save the replicated Fama-French factors to a new dataframe.
    ff_replicated = ffcomp63[['xRm-Rf', 'xSMB', 'xHML', 'xRMW', 'xCMA']]

    # Save the dataframe as a csv.
    ff_replicated.to_csv('processed_ff_replicated.csv', index=False)


def main():
    """
    This is the main function.
    Process_compustat_data, process_crsp_data, and process_ccm_data are pretty self-explanatory, as they process the given csv files.
    Compute_rm, compute_smb, compute_rmw, compute_cma, and compare_with_fama_french replicate the Fama-French 5 factors, and then compare them with the original data.
    The replicated code will be saved in: 'processed_ff_replicated.csv'

    Future editions of this code will be focused on the follow:
    - Ensuring that the correct filters are imposed (i.e. currently we are putting firms with negative book equity into the HML factor and etc.)
    - Adding the MOM factor
    - Adding other value factors
    - Adding factors relevant to my research
    - Simplifying the factor creating process
    - Adding decile sorts
    - Adding Fama-MacBeth regressions
    - Added different factor methologies
    - Adhering more to Python styleguides
    """

    actual_start_time = time.time()

    # start_time = time.time()
    # process_compustat_data()
    # end_time = time.time()
    # print("Processed Compustat data.")
    # print("Time Elapsed: ", end_time - start_time)

    # start_time = time.time()
    # process_crsp_data()
    # end_time = time.time()
    # print("Processed CRSP data.")
    # print("Time Elapsed: ", end_time - start_time)
    
    # start_time = time.time()
    # process_ccm_data()
    # end_time = time.time()
    # print("Processed CCM data.")
    # print("Time Elapsed: ", end_time - start_time)

    # start_time = time.time()
    # compute_rm()
    # end_time = time.time()
    # print("Computed Rm.")
    # print("Time Elapsed: ", end_time - start_time)

    # start_time = time.time()
    # compute_hml()
    # end_time = time.time()
    # print("Computed HML.")
    # print("Time Elapsed: ", end_time - start_time)

    # start_time = time.time()
    # compute_rmw()
    # end_time = time.time()
    # print("Computed RMW.")
    # print("Time Elapsed: ", end_time - start_time)

    # start_time = time.time()
    # compute_cma()
    # end_time = time.time()
    # print("Computed CMA.")
    # print("Time Elapsed: ", end_time - start_time)

    start_time = time.time()
    compare_with_fama_french()
    end_time = time.time()
    print("Compared with Fama-French.")
    print("Time Elapsed: ", end_time - start_time)

    actual_end_time = time.time()
    print("Total Time Elapsed: ", actual_end_time - actual_start_time)

main()