# Import the necessary libraries.
import pandas as pd
from typing import List
import numpy as np
import statsmodels.api as sm
import time


def generate_variables():
    """
    This is a helper function that generates variables that require both CRSP and Compustat data.
    """

    # Read in the csv file.
    ccm_jun = pd.read_csv('processed_crsp_jun1.csv', parse_dates=['jdate'])

    # Calculate the free cash flow to enterprise value ratio.
    ccm_jun['FCF_EV'] = ccm_jun['FCF'] * 1000 / (ccm_jun['dec_me'] + ccm_jun['NETDEBT'])

    # Calculate the net income to market equity ratio.
    ccm_jun['NI_ME'] = ccm_jun['NI'] * 1000 / ccm_jun['dec_me']

    # Calculate the operating cash flow to market equity ratio.
    ccm_jun['OCF_ME'] = ccm_jun['OCF'] * 1000 / ccm_jun['dec_me']

    # Calculate the dividend yield.
    ccm_jun['DIV_ME'] = ccm_jun['DIVIDENDS'] * 1000 / ccm_jun['dec_me']

    # Calculate the cash-based operating profits to market equity ratio.
    ccm_jun['COP_ME'] = ccm_jun['COP'] * 1000 / ccm_jun['dec_me']

    # Calculate revenue scaled by book equity.
    ccm_jun['revt_BE'] = ccm_jun['revt'] / ccm_jun['BE']

    # Calculate cost of goods sold scaled by book equity.
    ccm_jun['cogs_BE'] = ccm_jun['cogs'] / ccm_jun['BE']

    # Calculate cost of goods sold exclusive of advertising expenses scaled by book equity.
    ccm_jun['cogs-xad_BE'] = (ccm_jun['cogs'] - ccm_jun['xad']) / ccm_jun['BE']

    # Calculate advertising expenses scaled by book equity.
    ccm_jun['xad_BE'] = ccm_jun['xad'] / ccm_jun['BE']

    # Calculate sales, general, and adminstrative expenses exclusive of research and development expenses scaled by book equity.
    ccm_jun['xsga-xrd_BE'] = (ccm_jun['xsga'] - ccm_jun['xrd']) / ccm_jun['BE']

    # Calculate research and development expenses scaled by book equity.
    ccm_jun['xrd_BE'] = ccm_jun['xrd'] / ccm_jun['BE']

    # Calculate depreciation and ammortization scaled by book equity.
    ccm_jun['dp_BE'] = ccm_jun['dp'] / ccm_jun['BE']

    # Calculate taxes scaled by book equity.
    ccm_jun['txt_BE'] = ccm_jun['txt'] / ccm_jun['BE']

    # Calculate interest expenses scaled by book equity.
    ccm_jun['xint_BE'] = ccm_jun['xint'] / ccm_jun['BE']

    # Calculate non-operating income scaled by book equity.
    ccm_jun['nopi_BE'] = ccm_jun['nopi'] / ccm_jun['BE']

    # Calculate special items scaled by book equity.
    ccm_jun['spi_BE'] = ccm_jun['spi'] / ccm_jun['BE']

    # Calculate minority interest income scaled by book equity.
    ccm_jun['mii_BE'] = ccm_jun['mii'] / ccm_jun['BE']

    # Calculate operating accruals scaled by book equity.
    ccm_jun['OACC_BE'] = ccm_jun['OACC'] / ccm_jun['BE']

    # Calculate capital expenditures scaled by book equity.
    ccm_jun['capx_BE'] = ccm_jun['capx'] / ccm_jun['BE']

    # Save the dataframe to a csv file.
    ccm_jun.to_csv('processed_crsp_jun2.csv', index=False)


def fama_macbeth_regression(predictors: List):
    """
    This function runs the Fama-MacBeth regressions.
    """

    # Read in the csv files.
    ccm_jun = pd.read_csv('processed_crsp_jun2.csv', parse_dates=['jdate'])
    crsp3 = pd.read_csv('processed_crsp_data.csv', parse_dates=['jdate', 'MthCalDt'], low_memory=False)

    # Calculate book to market equity ratio.
    ccm_jun['BE_ME'] = ccm_jun['BE'] * 1000 / ccm_jun['dec_me']

    # Calculate momentum.
    crsp3['MOMENTUM'] = crsp3.groupby('PERMNO')['retadj'].apply(lambda x: x.shift(2).rolling(window=11, min_periods=11).mean())

    # Create a column representing the Fama-French year.
    ccm_jun['ffyear'] = ccm_jun['jdate'].dt.year

    # Keep only the essential columns.
    crsp3 = crsp3[['MthCalDt', 'PERMNO', 'SHRCD', 'EXCHCD', 'retadj', 'me', 'wt', 'cumretx', 'ffyear', 'jdate', 'MOMENTUM']]

    # Keep only the common stocks in the NYSE, NASDAQ, and AMEX exchanges.
    crsp3 = crsp3[(crsp3['EXCHCD'].isin([1, 2, 3])) & (crsp3['SHRCD'].isin([10, 11]))]

    # Merge monthly CRSP data with the variables in June.
    ccm3 = pd.merge(crsp3[['MthCalDt', 'PERMNO', 'retadj', 'me', 'wt', 'ffyear', 'MOMENTUM']],
                    ccm_jun[['PERMNO', 'ffyear', 'BE_ME', 'OP_BE', 'INVESTMENT', 'dec_me'] + predictors],
                    how='left', on=['PERMNO', 'ffyear'])

    # Only keep the firm-months with positive book equity data.
    ccm3 = ccm3[ccm3['BE_ME'] > 0]

    # Take the logarithms of dec_me.
    ccm3['LOG_DEC_ME'] = np.log(ccm3['dec_me'])

    # Remove unnecessary columns.
    ccm3 = ccm3.drop(['dec_me'], axis=1)

    # State the controls.
    controls = ['LOG_DEC_ME', 'BE_ME', 'MOMENTUM', 'INVESTMENT']

    # Add the controls with the predictors.
    variables = controls + predictors

    # Drop any row with NaN data for our regression variables.
    ccm3 = ccm3.dropna(subset=['retadj'] + variables)

    # Winsorize the data at the 1st and 99th percentile.
    for col in variables:
        lower_bound = ccm3[col].quantile(0.01)
        upper_bound = ccm3[col].quantile(0.99)
        ccm3[col] = ccm3[col].clip(lower=lower_bound, upper=upper_bound)

    # Sort the dataframe by date.
    ccm3 = ccm3.sort_values(by='MthCalDt')

    # Define the dependent variable.
    dependent_var = 'retadj'

    # Define the constant and independent variables.
    ccm3['constant'] = 1
    independent_vars = ['constant'] + variables

    # Fama-MacBeth regression.
    # Create a list to store the results.
    results_list = []

    # Iterate through the dates.
    for date, group in ccm3.groupby('MthCalDt'):

        # Set the dependent and independent variables for said date to y and X, respectively.
        y = group[dependent_var]
        X = group[independent_vars]

        # Check to avoid singular matrix error.
        if X.shape[0] > X.shape[1]:

            # Fit the OLS model.
            model = sm.OLS(y, X)

            # Save the results and append them to the list.
            results = model.fit()
            results_list.append(results.params)

    # Transform the list of results into a dataframe.
    fm_results = pd.DataFrame(results_list)

    # Calculate the length, mean, and standard deviation of the monthly coefficients.
    T = len(fm_results)
    fm_mean = fm_results.mean()
    fm_se = fm_results.std()

    # Adjust the t-statistic given the number of observations.
    t_stats = fm_mean / (fm_se / np.sqrt(T))

    # Mulitply the mean by 100 as to be expressed as a percentage.
    fm_mean *= 100

    # Create a results DataFrame with rounded values
    results_df = pd.DataFrame({
        'Coefficient': fm_mean.round(4),
        'T-Statistic': t_stats.round(2)
    })

    # Transform the dataframe into a table.
    table = results_df.to_string(index=True)

    # Print the table.
    print(table)


def produce_results():
    """
    This script calls the function to generate the variables and conduct the Fama-MacBeth regressions.
    """

    start_time = time.time()
    generate_variables()
    end_time = time.time()
    print("Generated Variables.")
    print("Time Elapsed: ", end_time - start_time)

    start_time = time.time()
    fama_macbeth_regression()
    end_time = time.time()
    print("Conducted Fama-MacBeth Regressions.")
    print("Time Elapsed: ", end_time - start_time)
