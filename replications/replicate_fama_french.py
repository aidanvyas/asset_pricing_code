# Import the necessary libraries
import pandas as pd
import numpy as np
import time
from pandas.tseries.offsets import MonthEnd
from scipy import stats
import os


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


def compute_rm():
    """
    Helper function to compute the Rm part of the Rm-Rf Fama-French factor.
    """

    # Read in the csv file.
    crsp3 = pd.read_csv('processed_crsp_data.csv', low_memory=False)

    # Select the correct universe of stocks.
    universe = crsp3[(crsp3['me'] > 0) &
                     (crsp3['wt'] > 0) &
                     ((crsp3['SHRCD'] == 10) | (crsp3['SHRCD'] == 11))]

    # Create a dataframe for the value-weighted returs.
    vwret = universe.groupby(['jdate']).apply(wavg, 'retadj', 'wt').to_frame().reset_index().rename(columns={0: 'vwret'})

    # Rename 'jdate' to 'date' and 'vwret' to 'xRm'.
    vwret = vwret.rename(columns={'jdate': 'date', 'vwret': 'xRm'})

    # Save the dataframe to a csv file.
    vwret.to_csv('processed_rm_factor.csv', index=False)


def compute_hml():
    """
    Helper function to compute the HML factor.
    """

    # Read in the csv files.
    ccm_jun = pd.read_csv('processed_crsp_jun1.csv', parse_dates=['jdate'])
    crsp3 = pd.read_csv('processed_crsp_data.csv', low_memory=False)

    # Calculate book to market equity ratio.
    ccm_jun['BE_ME'] = ccm_jun['BE'] * 1000 / ccm_jun['dec_me']

    # Select the universe NYSE common stocks with positive market equity.
    nyse = ccm_jun[(ccm_jun['EXCHCD'] == 1) &
                   (ccm_jun['me'] > 0) &
                   (ccm_jun['dec_me'] > 0) &
                   (ccm_jun['count'] >= 1) &
                   ((ccm_jun['SHRCD'] == 10) | (ccm_jun['SHRCD'] == 11))]

    # In the future, I will take a closer look on which stocks are allowed in the breakpoints and portfolios.
    # nyse_hml = nyse[(nyse['BE'] > 0)]

    # Get the size median breakpoints for each month.
    nyse_size = nyse.groupby(['jdate'])['me'].median().to_frame().reset_index().rename(columns={'me': 'sizemedn'})

    # Get the BE_ME 30th and 70th percentile breakpoints for each month.
    nyse_be_me = nyse.groupby(['jdate'])['BE_ME'].describe(percentiles=[0.3, 0.7]).reset_index()
    nyse_bm_me = nyse_be_me[['jdate', '30%', '70%']]

    # Merge the breakpoint dataframes together.
    nyse_breaks = pd.merge(nyse_size, nyse_bm_me, how='inner', on=['jdate'])

    # Merge the breakpoints with the CCM June data.
    ccm1_jun = pd.merge(ccm_jun, nyse_breaks, how='left', on=['jdate'])

    # In the future, I will take a closer look on which stocks are allowed in the breakpoints and portfolios.
    # Assign each stock to its proper size bucket.
    ccm1_jun['szport'] = np.where(
        (ccm_jun['dec_me'] > 0) & (ccm1_jun['me'] > 0) & (ccm1_jun['count'] >= 1),
        ccm1_jun.apply(sz_bucket, axis=1),
        ''
    )

    # In the future, I will take a closer look on which stocks are allowed in the breakpoints and portfolios.
    # Assign each stock to its proper book to market bucket.
    ccm1_jun['factor_portfolio'] = np.where(
        (ccm_jun['dec_me'] > 0) & (ccm1_jun['me'] > 0) & (ccm1_jun['count'] >= 1),
        ccm1_jun.apply(lambda row: factor_bucket(row, 'BE_ME'), axis=1),
        ''
    )

    # Create a 'valid_data' column that is 1 if company has valid June and December market equity data and has been in the dataframe at least once, and 0 otherwise.
    ccm1_jun['valid_data'] = np.where(
        (ccm_jun['dec_me'] > 0) & (ccm1_jun['me'] > 0) & (ccm1_jun['count'] >= 1),
        1,
        0
    )

    # Create a 'non_missing_portfolio' column that is 1 if the stock has been assigned to a portfolio, and 0 otherwise.
    ccm1_jun['non_missing_portfolio'] = np.where(
        (ccm1_jun['factor_portfolio'] != ''),
        1,
        0
    )

    # Create a new dataframe with only the essential columns for storing the portfolio assignments as of June.
    june = ccm1_jun[['PERMNO', 'MthCalDt', 'jdate', 'szport', 'factor_portfolio', 'valid_data', 'non_missing_portfolio']].copy()

    # Create a column representing the Fama-French year.
    june['ffyear'] = june['jdate'].dt.year

    # Keep only the essential columns.
    crsp3 = crsp3[['MthCalDt', 'PERMNO', 'SHRCD', 'EXCHCD', 'retadj', 'me', 'wt', 'cumretx', 'ffyear', 'jdate']]

    # Merge monthly CRSP data with the portfolio assignments in June.
    ccm3 = pd.merge(crsp3,
                    june[['PERMNO', 'ffyear', 'szport', 'factor_portfolio', 'valid_data', 'non_missing_portfolio']],
                    how='left', on=['PERMNO', 'ffyear'])

    # Keep only the common stocks with a positive weight, valid data, and a non-missing portfolio.
    ccm4 = ccm3[(ccm3['wt'] > 0) &
                (ccm3['valid_data'] == 1) &
                (ccm3['non_missing_portfolio'] == 1) &
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
    Helper function to compute the RMW factor.
    """

    # Read in the csv files.
    ccm_jun = pd.read_csv('processed_crsp_jun1.csv', parse_dates=['jdate'])
    crsp3 = pd.read_csv('processed_crsp_data.csv', low_memory=False)

    # Select the universe NYSE common stocks with positive market equity.
    nyse = ccm_jun[(ccm_jun['EXCHCD'] == 1) &
                   (ccm_jun['me'] > 0) &
                   (ccm_jun['dec_me'] > 0) &
                   (ccm_jun['count'] >= 1) &
                   ((ccm_jun['SHRCD'] == 10) | (ccm_jun['SHRCD'] == 11))]

    # In the future, I will take a closer look on which stocks are allowed in the breakpoints and portfolios.
    # nyse_rmw = nyse[(nyse['BE'] > 0)]

    # Get the size median breakpoints for each month.
    nyse_size = nyse.groupby(['jdate'])['me'].median().to_frame().reset_index().rename(columns={'me': 'sizemedn'})

    # Get the OP_BE 30th and 70th percentile breakpoints for each month.
    nyse_op_be = nyse.groupby(['jdate'])['OP_BE'].describe(percentiles=[0.3, 0.7]).reset_index()
    nyse_op_be = nyse_op_be[['jdate', '30%', '70%']]

    # Merge the breakpoint dataframes together.
    nyse_breaks = pd.merge(nyse_size, nyse_op_be, how='inner', on=['jdate'])

    # Merge the breakpoints with the CCM June data.
    ccm1_jun = pd.merge(ccm_jun, nyse_breaks, how='left', on=['jdate'])

    # Assign each stock to its proper size bucket.
    # ccm1_jun['size_portfolio'] = ccm1_jun.apply(sz_bucket, axis=1)
    ccm1_jun['szport'] = np.where(
        (ccm_jun['dec_me'] > 0) & (ccm1_jun['me'] > 0) & (ccm1_jun['count'] >= 1),
        ccm1_jun.apply(sz_bucket, axis=1),
        ''
    )

    # In the future, I will take a closer look on which stocks are allowed in the breakpoints and portfolios.
    # Assign each stock to its proper book to market bucket.
    ccm1_jun['factor_portfolio'] = np.where(
        (ccm_jun['dec_me'] > 0) & (ccm1_jun['me'] > 0) & (ccm1_jun['count'] >= 1),
        ccm1_jun.apply(lambda row: factor_bucket(row, 'OP_BE'), axis=1),
        ''
    )

    # Create a 'valid_data' column that is 1 if company has valid June and December market equity data and has been in the dataframe at least once, and 0 otherwise.
    ccm1_jun['valid_data'] = np.where(
        (ccm_jun['dec_me'] > 0) & (ccm1_jun['me'] > 0) & (ccm1_jun['count'] >= 1),
        1,
        0
    )

    # Create a 'non_missing_portfolio' column that is 1 if the stock has been assigned to a portfolio, and 0 otherwise.
    ccm1_jun['non_missing_portfolio'] = np.where(
        (ccm1_jun['factor_portfolio'] != ''),
        1,
        0
    )

    # Create a new dataframe with only the essential columns for storing the portfolio assignments as of June.
    june = ccm1_jun[['PERMNO', 'MthCalDt', 'jdate', 'szport', 'factor_portfolio', 'valid_data', 'non_missing_portfolio']].copy()

    # Create a column representing the Fama-French year.
    june['ffyear'] = june['jdate'].dt.year

    # Keep only the essential columns.
    crsp3 = crsp3[['MthCalDt', 'PERMNO', 'SHRCD', 'EXCHCD', 'retadj', 'me', 'wt', 'cumretx', 'ffyear', 'jdate']]

    # Merge monthly CRSP data with the portfolio assignments in June.
    ccm3 = pd.merge(crsp3,
                    june[['PERMNO', 'ffyear', 'szport', 'factor_portfolio', 'valid_data', 'non_missing_portfolio']],
                    how='left', on=['PERMNO', 'ffyear'])

    # Keep only the common stocks with a positive weight, valid data, and a non-missing portfolio.
    ccm4 = ccm3[(ccm3['wt'] > 0) &
                (ccm3['valid_data'] == 1) &
                (ccm3['non_missing_portfolio'] == 1) &
                ((ccm3['SHRCD'] == 10) | (ccm3['SHRCD'] == 11))]

    # Create a dataframe for the value-weighted returs.
    vwret = ccm4.groupby(['jdate', 'szport', 'factor_portfolio']).apply(wavg, 'retadj', 'wt').to_frame().reset_index().rename(columns={0: 'vwret'})

    # Create a column that represents the combined size, be_me portfolio that the stock is in.
    vwret['size_factor_portfolio'] = vwret['szport'] + vwret['factor_portfolio']

    # Tranpose the dataframes such that the rows are dates and the columns are portfolio returns.
    ff_factors = vwret.pivot(index='jdate', columns=['size_factor_portfolio'], values='vwret').reset_index()

    # Get the average return of the big and small robust operating profitability portfolios.
    ff_factors['xR'] = (ff_factors['BH'] + ff_factors['SH']) / 2

    # Get the average return of the big and small weak operating profitability portfolios.
    ff_factors['xW'] = (ff_factors['BL'] + ff_factors['SL']) / 2

    # Create the RMW factor which is the difference between the robust and weak operating profitability portfolios.
    ff_factors['xRMW'] = ff_factors['xR'] - ff_factors['xW']

    # Get the average return of the robust and weak small me portfolios.
    ff_factors['xS'] = (ff_factors['SH'] + ff_factors['SM'] + ff_factors['SL']) / 3

    # Get the average returnf of the robust and weak big me portfolios.
    ff_factors['xB'] = (ff_factors['BH'] + ff_factors['BM'] + ff_factors['BL']) / 3

    # Create the SMB factor based on the RMW breakpoints.
    ff_factors['xSRMW'] = ff_factors['xS'] - ff_factors['xB']

    # Rename the jdate column to date.
    ff_factors = ff_factors.rename(columns={'jdate': 'date'})

    # Save the dataframe to a csv file.
    ff_factors.to_csv('processed_rmw_factor.csv', index=False)


def compute_cma():
    """
    Helper function to compute CMA factor.
    """

    # Read in the csv files.
    ccm_jun = pd.read_csv('processed_crsp_jun1.csv', parse_dates=['jdate'])
    crsp3 = pd.read_csv('processed_crsp_data.csv', low_memory=False)

    # Select the universe NYSE common stocks with positive market equity.
    nyse = ccm_jun[(ccm_jun['EXCHCD'] == 1) &
                   (ccm_jun['me'] > 0) &
                   (ccm_jun['dec_me'] > 0) &
                   (ccm_jun['count'] >= 1) &
                   ((ccm_jun['SHRCD'] == 10) | (ccm_jun['SHRCD'] == 11))]

    # In the future, I will take a closer look on which stocks are allowed in the breakpoints and portfolios.
    # nyse_cma = nyse[(nyse['BE'] > 0)]

    # Get the size median breakpoints for each month.
    nyse_size = nyse.groupby(['jdate'])['me'].median().to_frame().reset_index().rename(columns={'me': 'sizemedn'})

    # Get the INVESTMENT 30th and 70th percentile breakpoints for each month.
    nyse_investment = nyse.groupby(['jdate'])['AT_GR1'].describe(percentiles=[0.3, 0.7]).reset_index()
    nyse_investment = nyse_investment[['jdate', '30%', '70%']]

    # Merge the breakpoint dataframes together.
    nyse_breaks = pd.merge(nyse_size, nyse_investment, how='inner', on=['jdate'])

    # Merge the breakpoints with the CCM June data.
    ccm1_jun = pd.merge(ccm_jun, nyse_breaks, how='left', on=['jdate'])

    # In the future, I will take a closer look on which stocks are allowed in the breakpoints and portfolios.
    # Assign each stock to its proper size bucket.
    ccm1_jun['szport'] = np.where(
        (ccm_jun['dec_me'] > 0) & (ccm1_jun['me'] > 0) & (ccm1_jun['count'] >= 1),
        ccm1_jun.apply(sz_bucket, axis=1),
        ''
    )

    # In the future, I will take a closer look on which stocks are allowed in the breakpoints and portfolios.
    # Assign each stock to its proper book to market bucket.
    ccm1_jun['factor_portfolio'] = np.where(
        (ccm_jun['dec_me'] > 0) & (ccm1_jun['me'] > 0) & (ccm1_jun['count'] >= 1),
        ccm1_jun.apply(lambda row: factor_bucket(row, 'AT_GR1'), axis=1),
        ''
    )

    # Create a 'valid_data' column that is 1 if company has valid June and December market equity data and has been in the dataframe at least once, and 0 otherwise.
    ccm1_jun['valid_data'] = np.where(
        (ccm_jun['dec_me'] > 0) & (ccm1_jun['me'] > 0) & (ccm1_jun['count'] >= 1),
        1,
        0
    )

    # Create a 'non_missing_portfolio' column that is 1 if the stock has been assigned to a portfolio, and 0 otherwise.
    ccm1_jun['non_missing_portfolio'] = np.where(
        (ccm1_jun['factor_portfolio'] != ''),
        1,
        0
    )

    # Create a new dataframe with only the essential columns for storing the portfolio assignments as of June.
    june = ccm1_jun[['PERMNO', 'MthCalDt', 'jdate', 'szport', 'factor_portfolio', 'valid_data', 'non_missing_portfolio']].copy()

    # Create a column representing the Fama-French year.
    june['ffyear'] = june['jdate'].dt.year

    # Keep only the essential columns.
    crsp3 = crsp3[['MthCalDt', 'PERMNO', 'SHRCD', 'EXCHCD', 'retadj', 'me', 'wt', 'cumretx', 'ffyear', 'jdate']]

    # Merge monthly CRSP data with the portfolio assignments in June.
    ccm3 = pd.merge(crsp3,
                    june[['PERMNO', 'ffyear', 'szport', 'factor_portfolio', 'valid_data', 'non_missing_portfolio']],
                    how='left', on=['PERMNO', 'ffyear'])

    # Keep only the common stocks with a positive weight, valid data, and a non-missing portfolio.
    ccm4 = ccm3[(ccm3['wt'] > 0) &
                (ccm3['valid_data'] == 1) &
                (ccm3['non_missing_portfolio'] == 1) &
                ((ccm3['SHRCD'] == 10) | (ccm3['SHRCD'] == 11))]

    # Create a dataframe for the value-weighted returs.
    vwret = ccm4.groupby(['jdate', 'szport', 'factor_portfolio']).apply(wavg, 'retadj', 'wt').to_frame().reset_index().rename(columns={0: 'vwret'})

    # Create a column that represents the combined size, be_me portfolio that the stock is in.
    vwret['size_factor_portfolio'] = vwret['szport'] + vwret['factor_portfolio']

    # Tranpose the dataframes such that the rows are dates and the columns are portfolio returns.
    ff_factors = vwret.pivot(index='jdate', columns=['size_factor_portfolio'], values='vwret').reset_index()

    # Get the average return of the big and small conservative investment portfolios.
    ff_factors['xC'] = (ff_factors['BL'] + ff_factors['SL']) / 2

    # Get the average return of the big and small aggresive investment portfolios.
    ff_factors['xA'] = (ff_factors['BH'] + ff_factors['SH']) / 2

    # Create the CMA factor which is the difference between the conservative and aggresive investment portfolios.
    ff_factors['xCMA'] = ff_factors['xC'] - ff_factors['xA']

    # Get the average return of the conservative and aggresive small investment portfolios.
    ff_factors['xS'] = (ff_factors['SH'] + ff_factors['SM'] + ff_factors['SL']) / 3

    # Get the average returnf of the conservative and aggresive big investment portfolios.
    ff_factors['xB'] = (ff_factors['BH'] + ff_factors['BM'] + ff_factors['BL']) / 3

    # Create the SMB factor based on the CMA breakpoints.
    ff_factors['xSCMA'] = ff_factors['xS'] - ff_factors['xB']

    # Rename the jdate column to date.
    ff_factors = ff_factors.rename(columns={'jdate': 'date'})

    # Save the dataframe to a csv file.
    ff_factors.to_csv('processed_cma_factor.csv', index=False)


def compute_umd():
    """
    Helper function to compute the UMD factor.
    """

    # Read in the csv file.
    crsp3 = pd.read_csv('processed_crsp_data.csv', low_memory=False)

    # Calculate momentum.
    crsp3['MOMENTUM'] = crsp3.groupby('PERMNO')['retadj'].apply(lambda x: x.shift(2).rolling(window=11, min_periods=11).mean())

    # Select the universe NYSE common stocks with positive market equity.
    nyse = crsp3[(crsp3['EXCHCD'] == 1) &
                 (crsp3['me'] > 0) &
                 (crsp3['count'] >= 1) &
                 ((crsp3['SHRCD'] == 10) | (crsp3['SHRCD'] == 11))]

    # Get the size median breakpoints for each month.
    nyse_size = nyse.groupby(['jdate'])['me'].median().to_frame().reset_index().rename(columns={'me': 'sizemedn'})

    # Get the MOMENTUM 30th and 70th percentile breakpoints for each month.
    nyse_mom = nyse.groupby(['jdate'])['MOMENTUM'].describe(percentiles=[0.3, 0.7]).reset_index()
    nyse_mom = nyse_mom[['jdate', '30%', '70%']]

    # Merge the breakpoint dataframes together.
    nyse_breaks = pd.merge(nyse_size, nyse_mom, how='inner', on=['jdate'])

    # Merge the breakpoints with the CRSP data.
    crsp4 = pd.merge(crsp3, nyse_breaks, how='left', on=['jdate'])

    # In the future, I will take a closer look on which stocks are allowed in the breakpoints and portfolios.
    # Assign each stock to its proper size bucket.
    crsp4['szport'] = np.where(
        (crsp4['me'] > 0) & (crsp4['count'] >= 1),
        crsp4.apply(sz_bucket, axis=1),
        ''
    )

    # In the future, I will take a closer look on which stocks are allowed in the breakpoints and portfolios.
    # Assign each stock to its proper momentum bucket.
    crsp4['factor_portfolio'] = np.where(
        (crsp4['me'] > 0) & (crsp4['count'] >= 1),
        crsp4.apply(lambda row: factor_bucket(row, 'MOMENTUM'), axis=1),
        ''
    )

    # Create a 'valid_data' column that is 1 if company has valid June and December market equity data and has been in the dataframe at least once, and 0 otherwise.
    crsp4['valid_data'] = np.where(
        (crsp4['me'] > 0) & (crsp4['count'] >= 1),
        1,
        0
    )

    # Create a 'non_missing_portfolio' column that is 1 if the stock has been assigned to a portfolio, and 0 otherwise.
    crsp4['non_missing_portfolio'] = np.where(
        (crsp4['factor_portfolio'] != ''),
        1,
        0
    )

    # Create a dataframe for the value-weighted returs.
    vwret = crsp4.groupby(['jdate', 'szport', 'factor_portfolio']).apply(wavg, 'retadj', 'wt').to_frame().reset_index().rename(columns={0: 'vwret'})

    # Create a column that represents the combined size, be_me portfolio that the stock is in.
    vwret['size_factor_portfolio'] = vwret['szport'] + vwret['factor_portfolio']

    # Tranpose the dataframes such that the rows are dates and the columns are portfolio returns.
    ff_factors = vwret.pivot(index='jdate', columns=['size_factor_portfolio'], values='vwret').reset_index()

    # Get the average return of the big and small up momentum portfolios.
    ff_factors['xU'] = (ff_factors['BH'] + ff_factors['SH']) / 2

    # Get the average return of the big and small low momentum portfolios.
    ff_factors['xD'] = (ff_factors['BL'] + ff_factors['SL']) / 2

    # Create the HML factor which is the difference between the up and low momentum portfolios.
    ff_factors['xUMD'] = ff_factors['xU'] - ff_factors['xD']

    # Rename the jdate column to date.
    ff_factors = ff_factors.rename(columns={'jdate': 'date'})

    # Save the dataframe to a csv file.
    ff_factors.to_csv('processed_umd_factor.csv', index=False)


def compare_with_fama_french():
    """
    This function compares the Fama-French factors (Mkt-Rf, SMB, HML, RMW, and CMA) that we have replicated with the original data.
    """

    # Read in the csv files.
    ff = pd.read_csv('raw_factors.csv')
    rm = pd.read_csv('processed_rm_factor.csv', parse_dates=['date'])
    hml = pd.read_csv('processed_hml_factor.csv', parse_dates=['date'])
    rmw = pd.read_csv('processed_rmw_factor.csv', parse_dates=['date'])
    cma = pd.read_csv('processed_cma_factor.csv', parse_dates=['date'])
    umd = pd.read_csv('processed_umd_factor.csv', parse_dates=['date'])

    # Keep only the essential columns.
    ff = ff[['date', 'Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA', 'UMD', 'RF']]

    # Parse the date column in the original Fama-French dataframe.
    ff['date'] = pd.to_datetime(ff['date'], format='%Y%m') + MonthEnd(0)

    # Merge my Fama-French factors with the original Fama-French factors.
    ffcomp = pd.merge(ff, rm[['date', 'xRm']], how='inner', on=['date'])
    ffcomp = pd.merge(ffcomp, hml[['date', 'xHML', 'xSHML']], how='inner', on=['date'])
    ffcomp = pd.merge(ffcomp, rmw[['date', 'xRMW', 'xSRMW']], how='inner', on=['date'])
    ffcomp = pd.merge(ffcomp, cma[['date', 'xCMA', 'xSCMA']], how='inner', on=['date'])
    ffcomp = pd.merge(ffcomp, umd[['date', 'xUMD']], how='inner', on=['date'])

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
    print(stats.pearsonr(ffcomp63['UMD'], ffcomp63['xUMD']))

    # Save the replicated Fama-French factors to a new dataframe.
    ff_replicated = ffcomp63[['date', 'xRm-Rf', 'xSMB', 'xHML', 'xRMW', 'xCMA', 'xUMD']]

    # Save the dataframe as a csv.
    ff_replicated.to_csv('processed_ff_replicated.csv', index=False)

    # Delete the intermediate csv files.
    files_to_delete = ['processed_rm_factor.csv', 'processed_hml_factor.csv', 'processed_rmw_factor.csv', 'processed_cma_factor.csv', 'processed_umd_factor.csv']
    for file in files_to_delete:
        if os.path.exists(file):
            os.remove(file)


def replicate_fama_french():
    """
    This script calls the functions to process Compustat, CRSP, and CCM data.
    """

    # Compute the Rm factor.
    start_time = time.time()
    compute_rm()
    end_time = time.time()
    print("Computed Rm.")
    print("Time Elapsed: ", end_time - start_time)

    # Compute the HML factor.
    start_time = time.time()
    compute_hml()
    end_time = time.time()
    print("Computed HML.")
    print("Time Elapsed: ", end_time - start_time)

    # Compute the RMW factor.
    start_time = time.time()
    compute_rmw()
    end_time = time.time()
    print("Computed RMW.")
    print("Time Elapsed: ", end_time - start_time)

    # Compute the CMA factor.
    start_time = time.time()
    compute_cma()
    end_time = time.time()
    print("Computed CMA.")
    print("Time Elapsed: ", end_time - start_time)

    # Compute the UMD factor.
    start_time = time.time()
    compute_umd()
    end_time = time.time()
    print("Computed UMD.")
    print("Time Elapsed: ", end_time - start_time)

    # Compare with the original Fama-French factors and print out the correlations.
    start_time = time.time()
    compare_with_fama_french()
    end_time = time.time()
    print("Compared with Fama-French.")
    print("Time Elapsed: ", end_time - start_time)
