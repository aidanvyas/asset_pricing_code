# Import the necessary libraries.
import pandas as pd
from typing import List
import numpy as np
import statsmodels.api as sm
import time
from replicate_fama_french import sz_bucket, factor_bucket, wavg


def generate_variables():
    """
    This is a helper function that generates variables that require both CRSP and Compustat data.
    """

    # Read in the csv file.
    ccm_jun = pd.read_csv('processed_crsp_jun1.csv', parse_dates=['jdate'])

    # Calculate the free cash flow to enterprise value ratio.
    ccm_jun['FCF_EV'] = ccm_jun['FCF'] * 1000 / (ccm_jun['dec_me'] + ccm_jun['NETDEBT'] * 1000)

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

    # Calculate cash-based operating profits to enterprise value ratio.
    ccm_jun['COP_EV'] = ccm_jun['COP'] * 1000 / (ccm_jun['dec_me'] + ccm_jun['NETDEBT'] * 1000)

    # Calculate free cash flow + research and development expenses to enterprise value ratio.
    ccm_jun['FCF+xrd_EV'] = (ccm_jun['FCF'] + ccm_jun['xrd']) * 1000 / (ccm_jun['dec_me'] + ccm_jun['NETDEBT'] * 1000)

    # Calculate the cash-based operating profits - capital expenditures to enterprise value ratio.
    ccm_jun['COP-capx_EV'] = (ccm_jun['COP'] - ccm_jun['capx']) * 1000 / (ccm_jun['dec_me'] + ccm_jun['NETDEBT'] * 1000)

    # Save the dataframe to a csv file.
    ccm_jun.to_csv('processed_crsp_jun2.csv', index=False)


def fama_macbeth_regression(predictors: List):
    """
    This function conducts Fama-MacBeth regressions.
    As an input, it takes a list of signals to be put into the regression.
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
    controls = ['LOG_DEC_ME', 'BE_ME', 'OP_BE', 'INVESTMENT', 'MOMENTUM']

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


def create_fama_french_esque_factors(predictors: List):
    """
    This function creates Fama-French-esque factors.
    As input, it takes a list of signals to be put into the regression.
    """

    # Read in the csv files.
    ccm_jun = pd.read_csv('processed_crsp_jun2.csv', parse_dates=['jdate'])
    crsp3 = pd.read_csv('processed_crsp_data.csv', low_memory=False)

    # Select the universe NYSE common stocks with positive market equity.
    nyse = ccm_jun[(ccm_jun['EXCHCD'] == 1) &
                   (ccm_jun['me'] > 0) &
                   (ccm_jun['dec_me'] > 0) &
                   (ccm_jun['count'] >= 1) &
                   ((ccm_jun['SHRCD'] == 10) | (ccm_jun['SHRCD'] == 11))]

    # Get the size median breakpoints for each month.
    nyse_size = nyse.groupby(['jdate'])['me'].median().to_frame().reset_index().rename(columns={'me': 'sizemedn'})

    # Dictionary to store factor DataFrames.
    factor_dfs = {}

    # Iterate through the predictors.
    for predictor in predictors:

        # Get the BE_ME 30th and 70th percentile breakpoints for each month.
        nyse_predictor = nyse.groupby(['jdate'])[predictor].describe(percentiles=[0.3, 0.7]).reset_index()
        nyse_predictor = nyse_predictor[['jdate', '30%', '70%']]

        # Merge the breakpoint dataframes together.
        nyse_breaks = pd.merge(nyse_size, nyse_predictor, how='inner', on=['jdate'])

        # Merge the breakpoints with the CCM June data.
        ccm1_jun = pd.merge(ccm_jun, nyse_breaks, how='left', on=['jdate'])

        # Assign each stock to its proper size bucket.
        ccm1_jun['szport'] = np.where(
            (ccm_jun['dec_me'] > 0) & (ccm1_jun['me'] > 0) & (ccm1_jun['count'] >= 1),
            ccm1_jun.apply(sz_bucket, axis=1),
            ''
        )

        # Assign each stock to its proper book to market bucket.
        ccm1_jun['factor_portfolio'] = np.where(
            (ccm_jun['dec_me'] > 0) & (ccm1_jun['me'] > 0) & (ccm1_jun['count'] >= 1),
            ccm1_jun.apply(lambda row: factor_bucket(row, predictor), axis=1),
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
        ff_factors[predictor] = ff_factors['xH'] - ff_factors['xL']

        # Save only the necessary columns.
        factor_dfs[predictor] = ff_factors[['jdate', predictor]]

    # Merge all factor DataFrames together on 'jdate'
    merged_factors = None
    for predictor, df in factor_dfs.items():
        if merged_factors is None:
            merged_factors = df
        else:
            merged_factors = pd.merge(merged_factors, df, on='jdate', how='outer')

    # Rename the jdate column to date
    merged_factors = merged_factors.rename(columns={'jdate': 'date'})

    # Save the merged DataFrame to a CSV file
    merged_factors.to_csv('processed_fama_french_esque_factors.csv', index=False)


def regress_on_ff6(factors: List):
    fama_french_esque_factors = pd.read_csv('processed_fama_french_esque_factors.csv', parse_dates=['date'])
    replicated_factors = pd.read_csv('processed_ff_replicated.csv', parse_dates=['date'])

    merged_data = pd.merge(replicated_factors, fama_french_esque_factors, how='inner', on='date')

    # Ensure there are no missing values in the columns of interest.
    merged_data.dropna(inplace=True)

    # Define the independent variables (Fama-French 6 factors).
    X = merged_data[['xRm-Rf', 'xSMB', 'xHML', 'xRMW', 'xCMA', 'xUMD']]

    # Add a constant to the independent variables matrix (for intercept)
    X = sm.add_constant(X)

    # Store the statistics on the factors.
    results_list = []

    # Iterate through the factors.
    for factor in factors:

        # Set the dependent variable to be y.
        y = merged_data[factor]

        # Fit the OLS model.
        model = sm.OLS(y, X).fit()

        # Print the model summary.
        print(model.summary())

        # Calculate the annual return.
        annual_return = (1 + y.mean()) ** 12 - 1

        # Calculate the annual standard deviation.
        annual_std_dev = y.std() * (12 ** 0.5)

        # Calculate Sharpe Ratio (risk-free rate assumed to be 0 as it is a self-financing long-short portfolio).
        sharpe_ratio = annual_return / annual_std_dev

        # Store results in a list
        results_list.append({
            'Factor': factor,
            'Average Annual Return': annual_return,
            'Average Annual Std Dev': annual_std_dev,
            'Annual Sharpe Ratio': sharpe_ratio,
        })

    # Create DataFrame from results
    results_df = pd.DataFrame(results_list)

    # Print or save the DataFrame as needed
    print(results_df)


def produce_results():
    """
    This script calls the function to generate the variables, conduct the Fama-MacBeth regressions,
    and create the Fama-French-esque factors.
    """

    start_time = time.time()
    generate_variables()
    end_time = time.time()
    print("Generated Variables.")
    print("Time Elapsed: ", end_time - start_time)

    # start_time = time.time()
    # fama_macbeth_regression()
    # end_time = time.time()
    # print("Conducted Fama-MacBeth Regressions.")
    # print("Time Elapsed: ", end_time - start_time)

    start_time = time.time()
    create_fama_french_esque_factors(['NI_ME', 'OCF_ME', 'DIV_ME', 'COP_ME', 'FCF_EV', 'COP_EV', 'FCF+xrd_EV', 'COP-capx_EV'])
    end_time = time.time()
    print("Create Fama-French-esque factors.")
    print("Time Elapsed: ", end_time - start_time)

    start_time = time.time()
    regress_on_ff6(['NI_ME', 'OCF_ME', 'DIV_ME', 'COP_ME', 'FCF_EV', 'COP_EV', 'FCF+xrd_EV', 'COP-capx_EV'])
    end_time = time.time()
    print("Create Fama-French-esque factors..")
    print("Time Elapsed: ", end_time - start_time)
