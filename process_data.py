# Import the necessary libraries
import pandas as pd
import numpy as np
from pandas.tseries.offsets import MonthEnd, YearEnd
import time


def process_compustat_data():
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
    - lo: Liabilities - Other - Total
    - xido: Extraordinary Items and Discontinued Operations
    - xi: Extraordinary Items
    - do: Discontinued Operations
    - ebit: Earnings Before Interest and Taxes
    - oiadp: Operating Income After Depreciation
    - dp: Depreciation and Amortization
    - pi: Pretax Income
    - spi: Special Items
    - nopi: Nonoperating Income (Expense)
    - ib: Income Before Extraordinary Items
    - ni: Net Income (Loss)
    - txt: Income Taxes - Total
    - mii: Noncontrolling Interest (Income Account)
    - act: Current Assets - Total
    - rect: Receivables - Total
    - invt: Inventories - Total
    - che: Cash and Short-Term Investments
    - aco: Current Assets - Other - Total
    - ap: Accounts Payable - Trade
    - lco: Current Liabilities - Other - Total
    - dlc: Debt in Current Liabilities - Total
    - txp: Income Taxes Payable
    - ivao: Investment and Advances - Other
    - oancf: Operating Activities - Net Cash Flow
    - wcap: Working Capital (Balance Sheet)
    - capx: Capital Expenditures
    - dvt: Dividends - Total
    - dv: Cash Dividends (Cash Flow)
    - xrd: Research and Development Expense
    - xad: Advertising Expense

    When I have created variables, those are denoted by using all upper-case.
    The original Compustat variables are in all lower-case.
    """

    # Read in the csv file.
    comp = pd.read_csv('raw_comp_funda.csv', parse_dates=['datadate'])

    # Create a year column.
    comp['year'] = comp['datadate'].dt.year

    # Sort the dataframe by gvkey (company code) and then date.
    comp = comp.sort_values(by=['gvkey', 'datadate'])

    # Create a 'count' column which equals the number of time that company has appeared in the dataframe.
    comp['count'] = comp.groupby(['gvkey']).cumcount()

    # PSTK = pstkrv, if missing, use pstkl, if missing, use pstk.
    comp['PSTK'] = np.where(
        comp['pstkrv'].isnull(),
        np.where(comp['pstkl'].isnull(), comp['pstk'], comp['pstkl']),
        comp['pstkrv']
    )

    # SEQ = seq, if missing, use ceq + PSTK (if missing set to 0), if missing use at - lt.
    comp['SEQ'] = np.where(
        comp['seq'].isnull(),
        np.where(
            (comp['ceq'] + np.where(comp['PSTK'].isnull(), 0, comp['PSTK'])).isnull(),
            comp['at'] - comp['lt'],
            comp['ceq'] + np.where(comp['PSTK'].isnull(), 0, comp['PSTK'])
        ),
        comp['seq']
    )

    # TXDITC = txditc, if missing, use txdb + itcb.
    comp['TXDITC'] = np.where(
        comp['txditc'].isnull(),
        comp['txdb'] + comp['itcb'],
        comp['txditc']
    )

    # Book Equity = SEQ + TXDITC (if missing set to 0) - PSTK (if missing set to 0).
    comp['BE'] = comp['SEQ'] + np.where(comp['TXDITC'].isnull(), 0, comp['TXDITC']) - np.where(comp['PSTK'].isnull(), 0, comp['PSTK'])

    # SALE = sale, if missing, use revt.
    comp['SALE'] = np.where(
        comp['sale'].isnull(),
        comp['revt'],
        comp['sale']
    )

    # OPEX = xopr, if missing, use cogs + xsga.
    comp['OPEX'] = np.where(
        comp['xopr'],
        comp['cogs'] + comp['xsga'],
        comp['xopr']
    )

    # GP = gp, if missing, use SALE - cogs.
    comp['GP'] = np.where(
        comp['gp'].isnull(),
        comp['SALE'] - comp['cogs'],
        comp['gp']
    )

    # EBITDA = ebitda, if missing, use oibdp, if missing, use SALE - OPEX, if missing, use GP - xsga.
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

    # Operating Profits = EBITDA - xint.
    comp['OP'] = comp['EBITDA'] - comp['xint']

    # Operating Profitability = Operating Profits / Book Equity.
    comp['OP_BE'] = comp['OP'] / comp['BE']

    # AT = at, if missing, use SEQ + dltt + lct (if missing set to 0) + lo (if missing set to 0) + txditc (if missing set to 0).
    comp['AT'] = np.where(
        comp['at'].isnull(),
        (comp['SEQ'] + comp['dltt'] + np.where(comp['lct'].isnull(), 0, comp['lct']) + np.where(comp['lo'].isnull(), 0, comp['lo']) + np.where(comp['txditc'].isnull(), 0, comp['txditc'])),
        comp['at']
    )

    # INVESTMENT = percentage change in AT.
    comp['INVESTMENT'] = comp.groupby('gvkey')['AT'].pct_change()

    # XIDO = xido, if missing, use xi + do (if missing set to 0).
    comp['XIDO'] = np.where(
        comp['xido'].isnull(),
        (comp['xi'] + comp['do']),
        comp['xido']
    )

    # EBIT = ebit, if missing, use oiadp, if missing, use EBITDA - dp.
    comp['EBIT'] = np.where(
        comp['ebit'].isnull(),
        np.where(
            comp['oiadp'].isnull(),
            (comp['EBITDA'] - comp['dp']),
            comp['oiadp']
        ),
        comp['ebit']
    )

    # PI = pi, if missing, use EBIT - xint + spi (if missing set to 0) + nopi (if missing set to 0).
    comp['PI'] = np.where(
        comp['pi'].isnull(),
        (comp['EBIT'] - comp['xint'] + np.where(comp['spi'].isnull(), 0, comp['spi']) + np.where(comp['nopi'].isnull(), 0, comp['nopi'])),
        comp['pi']
    )

    # NI = ib, if missing, use ni - XIDO, if missing, use PI - txt - mii (if missing set to 0).
    comp['NI'] = np.where(
        comp['ib'].isnull(),
        np.where(
            (comp['ni'] - comp['XIDO']).isnull(),
            (comp['PI'] - comp['txt'] - np.where(comp['mii'].isnull(), 0, comp['mii'])),
            (comp['ni'] - comp['XIDO'])
        ),
        comp['ib']
    )

    # CA = act, is missing, use rect + invt + che + aco.
    comp['CA'] = np.where(
        comp['act'].isnull(),
        (comp['rect'] + comp['invt'] + comp['che'] + comp['aco']),
        comp['act']
    )

    # COA = CA - che.
    comp['COA'] = comp['CA'] - comp['che']

    # CL = lct, if missing, use ap + dlc + txp + lco.
    comp['CL'] = np.where(
        comp['lct'].isnull(),
        (comp['ap'] + comp['dlc'] + comp['txp'] + comp['lco']),
        comp['lct']
    )

    # COL = CL - dlc (if missing set to 0).
    comp['COL'] = comp['CL'] - np.where(comp['dlc'].isnull(), 0, comp['dlc'])

    # COWC = COA - COL.
    comp['COWC'] = comp['COA'] - comp['COL']

    # NCAO = AT - CA - ivao.
    comp['NCOA'] = comp['AT'] - comp['CA'] - comp['ivao']

    # NCOL = lt - CL - dltt.
    comp['NCOL'] = comp['lt'] - comp['CL'] - comp['dltt']

    # NNCOA = NCOA - NCOL.
    comp['NNCOA'] = comp['NCOA'] - comp['NCOL']

    # OACC = NI - oancf, if missing, use the annual change in COWC + the annual change in NNCOA.
    comp['OACC'] = np.where(
        (comp['NI'] - comp['oancf']).isnull(),
        (comp.groupby('gvkey')['COWC'].diff() + comp.groupby('gvkey')['NNCOA'].diff()),
        (comp['NI'] - comp['oancf'])
    )

    # OCF = oancf, if missing, use NI - OACC, if missing, use NI + dp - wcap (if missing set to 0).
    comp['OCF'] = np.where(
        comp['oancf'].isnull(),
        np.where(
            (comp['NI'] - comp['OACC']).isnull(),
            (comp['NI'] + comp['dp'] - np.where(comp['wcap'].isnull(), 0, comp['wcap'])),
            (comp['NI'] - comp['OACC'])
        ),
        comp['oancf']
    )

    # Free Cash Flow = OCF - capx.
    comp['FCF'] = comp['OCF'] - comp['capx']

    # DEBT = dltt (if missing set to 0) + dlc (if missing set to 0).
    comp['DEBT'] = np.where(comp['dltt'].isnull(), 0, comp['dltt']) + np.where(comp['dlc'].isnull(), 0, comp['dlc'])

    # Net Debt = DEBT - che (if missing set to 0).
    comp['NETDEBT'] = comp['DEBT'] - np.where(comp['che'].isnull(), 0, comp['che'])

    # Total Dividends = dvt, if missing, use dv.
    comp['DIVIDENDS'] = np.where(
        comp['dvt'].isnull(),
        comp['dv'],
        comp['dvt']
    )

    # Cash-based Operating Profits = EBITDA + xrd (if missing set to 0) - OACC.
    comp['COP'] = comp['EBITDA'] + np.where(comp['xrd'].isnull(), 0, comp['xrd']) - comp['OACC']

    # Net Current Asset Value = CA - lt.
    comp['NCAV'] = comp['CA'] - comp['lt']

    # Free Cash Flow + Research and Development = FCF + xrd.
    comp['FCF+XRD'] = comp['FCF'] + np.where(comp['xrd'].isnull(), 0, comp['xrd'])

    # Cash-based Operating Profits - capx = COP - capx.
    comp['COP-CAPX'] = comp['COP'] - comp['capx']

    # Save the dataframe to a csv.
    comp.to_csv('processed_comp_funda.csv', index=False)


def process_crsp_data():
    """
    Helper function to process CRSP data.
    """

    # Read in the csv files.
    msf = pd.read_csv('raw_crsp_msf.csv', parse_dates=['MthCalDt'])
    msenames = pd.read_csv('raw_crsp_msenames.csv', parse_dates=['DATE', 'NAMEENDT'])
    dlret = pd.read_csv('raw_crsp_msedelist.csv', parse_dates=['DelistingDt'])

    # Merge the monthly stock files and names dataframes together.
    crsp_m = pd.merge(msf, msenames, left_on='PERMNO', right_on='PERMNO', how='left')

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
    crsp['retadj'] = (1 + crsp['MthRet']) * (1 + crsp['DelRet']) - 1

    # Calculate market equity.
    crsp['me'] = crsp['MthPrc'].abs() * crsp['ShrOut']

    # Remove unnecessary columns.
    crsp = crsp.drop(['DelRet', 'DelistingDt', 'MthPrc', 'ShrOut'], axis=1)

    # Sort the values by company code (jdate, PERMCO) and then market equity.
    crsp = crsp.sort_values(by=['jdate', 'PERMCO', 'me'])

    # Sum the market caps for different securities (PERMNO) within the same company (PERMCO) for each date.
    crsp_summe = crsp.groupby(['jdate', 'PERMCO'])['me'].sum().reset_index()

    # Find the largest market cap for a given date and PERMCO.
    crsp_maxme = crsp.groupby(['jdate', 'PERMCO'])['me'].max().reset_index()

    # Merge the max market cap dataframe with our CRSP dataframe such that each company / date pair aligns with the max market cap, in essence, only keeping the primary security.
    crsp1 = pd.merge(crsp, crsp_maxme, how='inner', on=['jdate', 'PERMCO', 'me'])

    # Drop the market equity column.
    crsp1 = crsp1.drop(['me'], axis=1)

    # Merge the summed market cap dataframe with the dataframe 'crsp1' which has the primary securities, such that the summed market cap is assigned to the primary security.
    crsp2 = pd.merge(crsp1, crsp_summe, how='inner', on=['jdate', 'PERMCO'])

    # Sort by PERMNO and then date, and after that, drop the duplicates.
    crsp2 = crsp2.sort_values(by=['PERMNO', 'jdate']).drop_duplicates()

    # Create columns representing the year and the month.
    crsp2['year'] = crsp2['jdate'].dt.year
    crsp2['month'] = crsp2['jdate'].dt.month

    # Create a new dataframe with only the December data.
    decme = crsp2[crsp2['month'] == 12]

    # Keep only the essential columns and then rename 'me' to 'dec_me'.
    decme = decme[['PERMNO', 'MthCalDt', 'jdate', 'me', 'year']].rename(columns={'me': 'dec_me'})

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
    crsp2 = crsp2.sort_values(by=['PERMNO', 'MthCalDt'])

    # Create a column for the lagged market cap.
    crsp2['lme'] = crsp2.groupby(['PERMNO'])['me'].shift(1)

    # Create a count column which equals the number of times that company has appeared in the dataframe.
    crsp2['count'] = crsp2.groupby(['PERMNO']).cumcount()

    # If this is the first time the company appears in the dataframe, then we need to input the correct lagged market cap, else, we should stick with the current lagged market cap.
    crsp2['lme'] = np.where(crsp2['count'] == 0, crsp2['me'] / crsp2['1+retx'], crsp2['lme'])

    # Create a new dataframe that only includes months at the beginning of a Fama-French year.
    mebase = crsp2[crsp2['ffmonth'] == 1][['PERMNO', 'ffyear', 'lme']].rename(columns={'lme': 'mebase'})

    # Merge in the 'mebase' dataframe into our main 'crsp2' dataframe.
    crsp3 = pd.merge(crsp2, mebase, how='left', on=['PERMNO', 'ffyear'])

    # Create a weight column that equals the lagged market equity for any given month.
    crsp3['wt'] = np.where(crsp3['ffmonth'] == 1, crsp3['lme'], crsp3['mebase'] * crsp3['lcumretx'])

    # Increment the year column by 1.
    decme['year'] = decme['year'] + 1

    # Keep only the essential columns.
    decme = decme[['PERMNO', 'year', 'dec_me']]

    # Create a dataframe with only the data from June.
    crsp3_jun = crsp3[crsp3['month'] == 6]

    # Merge the June and December dataframes.
    crsp_jun = pd.merge(crsp3_jun, decme, how='inner', on=['PERMNO', 'year'])

    # Keep only the essential columns.
    crsp_jun = crsp_jun[['PERMNO', 'MthCalDt', 'jdate', 'SHRCD', 'EXCHCD', 'retadj', 'me', 'wt', 'cumretx', 'mebase', 'lme', 'dec_me']]

    # Sort the June dataframe by PERMNO and then date, and after that, drop the duplicates.
    crsp_jun = crsp_jun.sort_values(by=['PERMNO', 'jdate']).drop_duplicates()

    # Save the dataframea to csv files.
    crsp_jun.to_csv('processed_crsp_jun.csv', index=False)
    crsp3.to_csv('processed_crsp_data.csv', index=False)


def process_ccm_data():
    """
    Helper function to process CCM data.
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


def process_data():
    """
    This script calls the functions to process Compustat, CRSP, and CCM data.
    """

    # Process Compustat data.
    start_time = time.time()
    process_compustat_data()
    end_time = time.time()
    print("Processed Compustat data.")
    print("Time Elapsed: ", end_time - start_time)

    # # Process CRSP data.
    # start_time = time.time()
    # process_crsp_data()
    # end_time = time.time()
    # print("Processed CRSP data.")
    # print("Time Elapsed: ", end_time - start_time)

    # Process CCM data.
    start_time = time.time()
    process_ccm_data()
    end_time = time.time()
    print("Processed CCM data.")
    print("Time Elapsed: ", end_time - start_time)
