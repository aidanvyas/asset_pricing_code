"""
This script contains functions to process Compustat, CRSP, and CCM data.
"""

# Import the necessary libraries
import logging
from functools import reduce
import time
import pandas as pd
import numpy as np
from pandas.tseries.offsets import MonthEnd, YearEnd


def setup_logging(logging_enabled):
    """
    Helper function to setup logging.
    """
    if logging_enabled:
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    else:
        logging.disable(logging.CRITICAL)


def coalesce(*args):
    """
    Helper function that the first non-None value across given pandas Series for each row.
    """
    # Ensure all arguments are pandas Series.
    args = [arg if isinstance(arg, pd.Series) else pd.Series(arg) for arg in args]

    # Use reduce with a lambda that explicitly checks for notnull() and selects accordingly.
    return reduce(lambda x, y: x.where(x.notnull(), y), args)


def process_compustat_data(logging_enabled: bool = True):
    """
    Helper function to process Compustat data and construct intermediate variables (e.g. book equity, operating profits, etc.).

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
    - sale: Sales/Turnover (Net)
    - revt: Revenue - Total
    - xopr: Operating Expenses - Total
    - cogs: Cost of Goods Sold
    - xsga: Selling, General and Administrative Expense
    - gp: Gross Profit (Loss)
    - ebitda: Earnings Before Interest
    - oibdp: Operating Income Before Depreciation
    - xint: Interest and Related Expense - Total
    - dltt: Long-Term Debt - Total
    - lct: Current Liabilities - Total
    - lo: Liabilities - Other, Total

    When I have created variables, those are denoted by using all upper-case.
    The original Compustat variables are in all lower-case.
    """

    # Set up logging.
    setup_logging(logging_enabled)

    # Read in the csv file.
    comp = pd.read_csv('data/raw_compustat_fundamentals_annual.csv', parse_dates=['datadate'], usecols=['gvkey', 'datadate', 'pstkrv', 'pstkl', 'pstk', 'seq', 'ceq', 'at', 'lt', 'txditc', 'txdb', 'itcb', 'sale', 'revt', 'xopr', 'cogs', 'xsga', 'gp', 'ebitda', 'oibdp', 'xint', 'dltt', 'lct', 'lo'])
    logging.info("Read in the csv file.")

    # Create a year column.
    comp['year'] = comp['datadate'].dt.year
    logging.info("Created a year column.")

    # Sort the dataframe by gvkey (company code) and then date.
    comp = comp.sort_values(by=['gvkey', 'datadate'])
    logging.info("Sorted the dataframe by gvkey (company code) and then date.")

    # Create a 'count' column which equals the number of time that company has appeared in the dataframe.
    comp['count'] = comp.groupby(['gvkey']).cumcount()
    logging.info("Created a 'count' column which equals the number of time that company has appeared in the dataframe.")

    # PSTK = pstkrv, if missing, use pstkl, if missing, use pstk.
    comp['PSTK'] = coalesce(comp['pstkrv'], comp['pstkl'], comp['pstk'])
    logging.info("Created a 'PSTK' column.")

    # SEQ = seq, if missing, use ceq + PSTK (if missing set to 0), if missing, use at - lt.
    comp['SEQ'] = coalesce(comp['seq'], comp['ceq'] + comp['PSTK'].fillna(0), comp['at'] - comp['lt'])
    logging.info("Created a 'SEQ' column.")

    # TXDITC = txditc, if missing, use txdb + itcb.
    comp['TXDITC'] = coalesce(comp['txditc'], comp['txdb'] + comp['itcb'])
    logging.info("Created a 'TXDITC' column.")

    # Book Equity = SEQ + TXDITC (if missing set to 0) - PSTK (if missing set to 0).
    comp['BE'] = comp['SEQ'] + comp['TXDITC'].fillna(0) - comp['PSTK'].fillna(0)
    logging.info("Created a 'BE' column.")

    # SALE = sale, if missing, use revt.
    comp['SALE'] = coalesce(comp['sale'], comp['revt'])
    logging.info("Created a 'SALE' column.")

    # OPEX = xopr, if missing, use cogs + xsga.
    comp['OPEX'] = coalesce(comp['xopr'], comp['cogs'] + comp['xsga'])
    logging.info("Created a 'OPEX' column.")

    # GP = gp, if missing, use SALE - cogs.
    comp['GP'] = coalesce(comp['gp'], comp['SALE'] - comp['cogs'])
    logging.info("Created a 'GP' column.")

    # EBITDA = ebitda, if missing, use oibdp, if missing, use SALE - OPEX, if missing, use GP - xsga.
    comp['EBITDA'] = coalesce(comp['ebitda'], comp['oibdp'], comp['SALE'] - comp['OPEX'], comp['GP'] - comp['xsga'])
    logging.info("Created a 'EBITDA' column.")

    # Operating Profits = EBITDA - xint.
    comp['OP'] = comp['EBITDA'] - comp['xint']
    logging.info("Created a 'OP' column.")

    # Operating Profitability = Operating Profits / Book Equity.
    comp['OP_BE'] = comp['OP'] / comp['BE']
    logging.info("Created a 'OP_BE' column.")

    # AT = at, if missing, use SEQ + dltt + lct (if missing set to 0) + lo (if missing set to 0) + txditc (if missing set to 0).
    comp['AT'] = coalesce(comp['at'], comp['SEQ'] + comp['dltt'] + comp['lct'].fillna(0) + comp['lo'].fillna(0) + comp['txditc'].fillna(0))
    logging.info("Created a 'AT' column.")

    # AT_GR1 = percentage change in AT.
    comp['AT_GR1'] = comp.groupby('gvkey')['AT'].pct_change(fill_method=None)
    logging.info("Created a 'AT_GR1' column.")

    # Save the dataframe to a csv.
    comp.to_csv('data/processed_comp_funda.csv', index=False)
    logging.info("Saved the dataframe to a csv.")


def process_crsp_data(logging_enabled: bool = True):
    """
    Helper function to process CRSP data.
    """
    # Set up logging.
    setup_logging(logging_enabled)

    # Read in the csv files.
    msf = pd.read_csv('data/raw_monthly_stock_files.csv', usecols=['PERMNO', 'PERMCO', 'MthCalDt', 'MthRet', 'MthRetx', 'ShrOut', 'MthPrc'], parse_dates=['MthCalDt'])
    msenames = pd.read_csv('data/raw_compustat_historical_descriptive_information.csv', usecols=['PERMNO', 'DATE', 'NAMEENDT', 'SHRCD', 'EXCHCD'], parse_dates=['DATE', 'NAMEENDT'])
    dlret = pd.read_csv('data/raw_crsp_delisting_information.csv', usecols=['PERMNO', 'DLSTDT', 'DLRET', 'DLSTCD'], parse_dates=['DLSTDT'])
    logging.info("Read in the csv files.")

    # Merge the monthly stock files and names dataframes together.
    crsp_m = pd.merge(msf, msenames, left_on='PERMNO', right_on='PERMNO', how='left')
    logging.info("Merged the monthly stock files and names dataframes.")

    # Filter the data such that the dates are in the correct range.
    crsp_m = crsp_m[(crsp_m['NAMEENDT'] >= crsp_m['MthCalDt']) &
                    (crsp_m['MthCalDt'] >= crsp_m['DATE']) &
                    (crsp_m['MthCalDt'] >= pd.to_datetime('1958-07-01')) &
                    (crsp_m['MthCalDt'] <= pd.to_datetime('2022-12-30'))]
    logging.info("Filtered the data.")

    # Filter the data such that we only get NYSE, NASDAQ, and AMEX stocks.
    crsp_m = crsp_m[(crsp_m['EXCHCD'].between(1, 3))]
    logging.info("Filtered the data to only include NYSE, NASDAQ, and AMEX stocks.")

    # Change the variable format to int.
    crsp_m[['PERMCO', 'PERMNO', 'SHRCD', 'EXCHCD']] = crsp_m[['PERMCO', 'PERMNO', 'SHRCD', 'EXCHCD']].astype(int)
    dlret['PERMNO'] = dlret['PERMNO'].astype(int)
    logging.info("Changed the variable format to int.")

    # Line up the dates to be at the end of the month.
    crsp_m['jdate'] = crsp_m['MthCalDt'] + MonthEnd(0)
    dlret['jdate'] = dlret['DLSTDT'] + MonthEnd(0)
    logging.info("Lined up the dates to be at the end of the month.")

    # Merge all of the CRSP dataframes together.
    crsp = pd.merge(crsp_m, dlret, how='left', on=['PERMNO', 'jdate'])
    logging.info("Merged all of the CRSP dataframes together.")

    # Create a boolean series representing whether the delising is performance related.
    DLCode = (crsp['DLSTCD'] == 500) | ((crsp['DLSTCD'] >= 520) & (crsp['DLSTCD'] <= 584))
    logging.info("Created a boolean series representing whether the delisting is performance related.")

    # If the delisting is for performance related and the delisting return is NaN, set the delisting return to be -30% for NYSE and AMEX stocks and -55% for NASDAQ stocks.
    crsp['DLRET'] = np.where(DLCode & crsp['DLRET'].isnull() & crsp['DLRET'].isin([1,2]), -0.3, crsp['DLRET'])
    crsp['DLRET'] = np.where(DLCode & crsp['DLRET'].isnull() & (crsp['DLRET']==3), -0.55, crsp['DLRET'])
    logging.info("Set the delisting return to be -30% for NYSE and AMEX stocks and -55% for NASDAQ stocks.")

    # Set the NaN returns to 0 and coerce the delisting returns to numeric types.
    crsp['DelRet'] = crsp['DLRET'].fillna(0)
    crsp['DelRet'] = pd.to_numeric(crsp['DelRet'], errors='coerce')
    crsp['MthRet'] = crsp['MthRet'].fillna(0)
    logging.info("Set the NaN returns to 0 and coerced the delisting returns to numeric types.")

    # Calculate the delisting adjusted-returns.
    crsp['retadj'] = (1 + crsp['MthRet']) * (1 + crsp['DelRet']) - 1
    logging.info("Calculated the delisting adjusted-returns.")

    # Calculate market equity.
    crsp['me'] = crsp['MthPrc'].abs() * crsp['ShrOut']
    logging.info("Calculated market equity.")

    # Remove unnecessary columns.
    crsp = crsp.drop(['DelRet', 'DLRET', 'DLSTDT', 'MthPrc', 'ShrOut'], axis=1)
    logging.info("Removed unnecessary columns.")

    # Sort the values by company code (jdate, PERMCO) and then market equity.
    crsp = crsp.sort_values(by=['jdate', 'PERMCO', 'me'])
    logging.info("Sorted the values by company code (jdate, PERMCO) and then market equity.")

    # Sum the market caps for different securities (PERMNO) within the same company (PERMCO) for each date.
    crsp_summe = crsp.groupby(['jdate', 'PERMCO'])['me'].sum().reset_index()
    logging.info("Summed the market caps for different securities (PERMNO) within the same company (PERMCO) for each date.")

    # Find the largest market cap for a given date and PERMCO.
    crsp_maxme = crsp.groupby(['jdate', 'PERMCO'])['me'].max().reset_index()
    logging.info("Found the largest market cap for a given date and PERMCO.")

    # Merge the max market cap dataframe with our CRSP dataframe such that each company / date pair aligns with the max market cap, in essence, only keeping the primary security.
    crsp1 = pd.merge(crsp, crsp_maxme, how='inner', on=['jdate', 'PERMCO', 'me'])
    logging.info("Merged the max market cap dataframe with our CRSP dataframe.")

    # Drop the market equity column.
    crsp1 = crsp1.drop(['me'], axis=1)
    logging.info("Dropped the market equity column.")

    # Merge the summed market cap dataframe with the dataframe 'crsp1' which has the primary securities, such that the summed market cap is assigned to the primary security.
    crsp2 = pd.merge(crsp1, crsp_summe, how='inner', on=['jdate', 'PERMCO'])
    logging.info("Merged the summed market cap dataframe with the dataframe 'crsp1'.")

    # Sort by PERMNO and then date, and after that, drop the duplicates.
    crsp2 = crsp2.sort_values(by=['PERMNO', 'jdate']).drop_duplicates()
    logging.info("Sorted by PERMNO and then date, and after that, dropped the duplicates.")

    # Create columns representing the year and the month.
    crsp2['year'] = crsp2['jdate'].dt.year
    crsp2['month'] = crsp2['jdate'].dt.month
    logging.info("Created columns representing the year and the month.")

    # Create a new dataframe with only the December data.
    decme = crsp2[crsp2['month'] == 12]
    logging.info("Created a new dataframe with only the December data.")

    # Keep only the essential columns and then rename 'me' to 'dec_me'.
    decme = decme[['PERMNO', 'MthCalDt', 'jdate', 'me', 'year']].rename(columns={'me': 'dec_me'})
    logging.info("Kept only the essential columns and then renamed 'me' to 'dec_me'.")

    # Create columns for the Fama-French date, year, and month.
    crsp2['ffdate'] = crsp2['jdate'] + MonthEnd(-6)
    crsp2['ffyear'] = crsp2['ffdate'].dt.year
    crsp2['ffmonth'] = crsp2['ffdate'].dt.month
    logging.info("Created columns for the Fama-French date, year, and month.")

    # Create a columnn '1+retx' for ease of calculations.
    crsp2['1+retx'] = 1 + crsp2['MthRetx']
    logging.info("Created a column '1+retx' for ease of calculations.")

    # Create a column for the cumulative return of each stock in each Fama-French year.
    crsp2['cumretx'] = crsp2.groupby(['PERMNO', 'ffyear'])['1+retx'].cumprod()
    logging.info("Created a column for the cumulative return of each stock in each Fama-French year.")

    # Create a column for the lagged cumulative return.
    crsp2['lcumretx'] = crsp2.groupby(['PERMNO'])['cumretx'].shift(1)
    logging.info("Created a column for the lagged cumulative return.")

    # Sort the dataframe by company and then date.
    crsp2 = crsp2.sort_values(by=['PERMNO', 'MthCalDt'])
    logging.info("Sorted the dataframe by company and then date.")

    # Create a column for the lagged market cap.
    crsp2['lme'] = crsp2.groupby(['PERMNO'])['me'].shift(1)
    logging.info("Created a column for the lagged market cap.")

    # Create a count column which equals the number of times that company has appeared in the dataframe.
    crsp2['count'] = crsp2.groupby(['PERMNO']).cumcount()
    logging.info("Created a count column which equals the number of times that company has appeared in the dataframe.")

    # If this is the first time the company appears in the dataframe, then we need to input the correct lagged market cap, else, we should stick with the current lagged market cap.
    crsp2['lme'] = np.where(crsp2['count'] == 0, crsp2['me'] / crsp2['1+retx'], crsp2['lme'])
    logging.info("If this is the first time the company appears in the dataframe, then we need to input the correct lagged market cap, else, we should stick with the current lagged market cap.")

    # Create a new dataframe that only includes months at the beginning of a Fama-French year.
    mebase = crsp2[crsp2['ffmonth'] == 1][['PERMNO', 'ffyear', 'lme']].rename(columns={'lme': 'mebase'})
    logging.info("Created a new dataframe that only includes months at the beginning of a Fama-French year.")

    # Merge in the 'mebase' dataframe into our main 'crsp2' dataframe.
    crsp3 = pd.merge(crsp2, mebase, how='left', on=['PERMNO', 'ffyear'])
    logging.info("Merged in the 'mebase' dataframe into our main 'crsp2' dataframe.")

    # Create a weight column that equals the lagged market equity for any given month.
    crsp3['wt'] = np.where(crsp3['ffmonth'] == 1, crsp3['lme'], crsp3['mebase'] * crsp3['lcumretx'])
    logging.info("Created a weight column that equals the lagged market equity for any given month.")

    # Increment the year column by 1.
    decme['year'] = decme['year'] + 1
    logging.info("Incremented the year column by 1.")

    # Keep only the essential columns.
    decme = decme[['PERMNO', 'year', 'dec_me']]
    logging.info("Kept only the essential columns.")

    # Create a dataframe with only the data from June.
    crsp3_jun = crsp3[crsp3['month'] == 6]
    logging.info("Created a dataframe with only the data from June.")

    # Merge the June and December dataframes.
    crsp_jun = pd.merge(crsp3_jun, decme, how='inner', on=['PERMNO', 'year'])
    logging.info("Merged the June and December dataframes.")

    # Keep only the essential columns.
    crsp_jun = crsp_jun[['PERMNO', 'MthCalDt', 'jdate', 'SHRCD', 'EXCHCD', 'retadj', 'me', 'wt', 'cumretx', 'mebase', 'lme', 'dec_me']]
    logging.info("Kept only the essential columns.")

    # Sort the June dataframe by PERMNO and then date, and after that, drop the duplicates.
    crsp_jun = crsp_jun.sort_values(by=['PERMNO', 'jdate']).drop_duplicates()
    logging.info("Sorted the June dataframe by PERMNO and then date, and after that, dropped the duplicates.")

    # Save the dataframe to csv files.
    crsp_jun.to_csv('data/processed_crsp_jun.csv', index=False)
    crsp3.to_csv('data/processed_crsp_data.csv', index=False)
    logging.info("Saved the dataframe to csv files.")


def process_ccm_data(logging_enabled: bool = True):
    """
    Helper function to process CCM data.
    """

    # Set up logging.
    setup_logging(logging_enabled=True)

    # Read in the csv files.
    ccm = pd.read_csv('data/raw_crsp_compustat_linking_table.csv', usecols=['gvkey', 'LPERMNO', 'LINKTYPE', 'LINKPRIM', 'LINKDT', 'LINKENDDT'], parse_dates=['LINKDT', 'LINKENDDT'])
    comp = pd.read_csv('data/processed_comp_funda.csv')
    crsp_jun = pd.read_csv('data/processed_crsp_jun.csv', parse_dates=['jdate'])
    logging.info("Read in the csv files.")

    # Keep only the primary securities.
    ccm = ccm[(ccm['LINKPRIM'] == 'C') | (ccm['LINKPRIM'] == 'P')]
    logging.info("Kept only the primary securities.")

    # Rename LPERMNO to PERMNO to be consistent with the other dataframes.
    ccm = ccm.rename(columns={'LPERMNO': 'PERMNO'})
    logging.info("Renamed LPERMNO to PERMNO.")

    # If the stock still trades, set the date to NaN.
    ccm['LINKENDDT'] = ccm['LINKENDDT'].replace('E', np.nan)
    logging.info("If the stock still trades, set the date to NaN.")

    # If the LINKENDDT is NaN, then we set it to today's date.
    ccm['LINKENDDT'] = ccm['LINKENDDT'].fillna(pd.to_datetime('today'))
    logging.info("If the LINKENDDT is NaN, then we set it to today's date.")

    # Merge the Compustat data with the CRSP linking table.
    ccm1 = pd.merge(comp, ccm, how='left', on=['gvkey'])
    logging.info("Merged the Compustat data with the CRSP linking table.")

    # Parse the date columns as datetime objects.
    ccm1['datadate'] = pd.to_datetime(ccm1['datadate'])
    ccm1['LINKENDDT'] = pd.to_datetime(ccm1['LINKENDDT'])
    logging.info("Parsed the date columns as datetime objects.")

    # Create yearend and June date columns.
    ccm1['yearend'] = ccm1['datadate'] + YearEnd(0)
    ccm1['jdate'] = ccm1['yearend'] + MonthEnd(6)
    logging.info("Created yearend and June date columns.")

    # Set the link date bounds and create a copy of the dataframe.
    ccm2 = ccm1[(ccm1['jdate'] >= ccm1['LINKDT']) & (ccm1['jdate'] <= ccm1['LINKENDDT'])].copy()
    logging.info("Set the link date bounds and created a copy of the dataframe.")

    # Drop the unnecessary columns.
    ccm2.drop(['LINKPRIM', 'LINKTYPE', 'LINKDT', 'LINKENDDT'], axis=1, inplace=True)
    logging.info("Dropped the unnecessary columns.")

    # Change the variable type to int.
    crsp_jun['PERMNO'] = crsp_jun['PERMNO'].astype(int)
    ccm2['PERMNO'] = ccm2['PERMNO'].astype(int)
    logging.info("Changed the variable type to int.")

    # Parse the June date column as a datetime object.
    ccm2['jdate'] = pd.to_datetime(ccm2['jdate'])
    logging.info("Parsed the June date column as a datetime object.")

    # Merge the combined CRSP linking table and Compustat data with the CRSP june date.
    ccm_jun = pd.merge(crsp_jun, ccm2, how='inner', on=['PERMNO', 'jdate'])
    logging.info("Merged the combined CRSP linking table and Compustat data with the CRSP june date.")

    # Save the dataframe to a csv.
    ccm_jun.to_csv('data/processed_crsp_jun1.csv', index=False)
    logging.info("Saved the dataframe to a csv.")


def process_data(logging_enabled: bool = True):
    """
    This script calls the functions to process Compustat, CRSP, and CCM data.
    """

    # Process Compustat data.
    start_time = time.time()
    process_compustat_data(logging_enabled=logging_enabled)
    elapsed_time = time.time() - start_time
    print(f"Processed Compustat Data in {elapsed_time:.2f} seconds.")

    # Process CRSP data.
    start_time = time.time()
    process_crsp_data(logging_enabled=logging_enabled)
    elapsed_time = time.time() - start_time
    print(f"Processed CRSP Data in {elapsed_time:.2f} seconds.")

    # Process CCM data.
    start_time = time.time()
    process_ccm_data(logging_enabled=logging_enabled)
    elapsed_time = time.time() - start_time
    print(f"Processed CCM Data in {elapsed_time:.2f} seconds.")
