# Import the necessary libraries.
import pandas as pd
from typing import List, Dict
import numpy as np
import statsmodels.api as sm
import time
from replicate_fama_french import sz_bucket, factor_bucket, wavg
from scipy.stats import skew, kurtosis
import matplotlib.pyplot as plt


def decile_bucket(row, factor):
    """
    Helper function to assign a stock to the correct decile bucket.
    """
    if row[factor] <= row['10%']:
        value = '1'
    elif row[factor] <= row['20%']:
        value = '2'
    elif row[factor] <= row['30%']:
        value = '3'
    elif row[factor] <= row['40%']:
        value = '4'
    elif row[factor] <= row['50%']:
        value = '5'
    elif row[factor] <= row['60%']:
        value = '6'
    elif row[factor] <= row['70%']:
        value = '7'
    elif row[factor] <= row['80%']:
        value = '8'
    elif row[factor] <= row['90%']:
        value = '9'
    elif row[factor] > row['90%']:
        value = '10'
    else:
        value = ''
    return value


def generate_variables():
    """
    This is a helper function that generates variables beyond the previously generated Compustat variables..
    """

    # Read in the csv file.
    ccm_jun = pd.read_csv('processed_crsp_jun1.csv', parse_dates=['jdate'])

    # Calculate the book equity to market equity ratio.
    ccm_jun['BE\_ME'] = (ccm_jun['BE'] * 1000) / ccm_jun['dec_me']

    # Calculate the net income to book equity ratio.
    ccm_jun['Net Income'] = ccm_jun['NI'] / ccm_jun['BE']

    # Calculate the depreciation and amortization to book equity ratio.
    ccm_jun['Depreciation and Amortization'] = ccm_jun['dp'] / ccm_jun['BE']

    # Calculate the capital expenditures to book equity ratio.
    ccm_jun['Capital Expenditures'] = ccm_jun['capx'] / ccm_jun['BE']

    # Calculate the enterprise value to book equity ratio.
    ccm_jun['Enterprise Value'] = (ccm_jun['dec_me'] + (ccm_jun['NETDEBT']) * 1000) / (ccm_jun['BE'] * 1000)

    # Calculate Buffett's owner's earnings.
    ccm_jun['Buffett\'s Owner\'s Earnings'] = ccm_jun['Net Income'] + ccm_jun['Depreciation and Amortization'] - ccm_jun['Capital Expenditures']

    # Calculate the net income to market equity ratio.
    ccm_jun['ni\_me'] = (ccm_jun['NI'] * 1000) / ccm_jun['dec_me']

    # Calculate the operating cash flow to market equity ratio.
    ccm_jun['ocf\_me'] = (ccm_jun['OCF'] * 1000) / ccm_jun['dec_me']

    # Calculate the total dividends to market equity ratio.
    ccm_jun['div\_me'] = (ccm_jun['DIVIDENDS'] * 1000) / ccm_jun['dec_me']

    # Calculate the cash-based operating profits to market equity ratio.
    ccm_jun['cop\_me'] = (ccm_jun['COP'] * 1000) / ccm_jun['dec_me']

    # Calculate enterprise value.
    ccm_jun['ev'] = (ccm_jun['dec_me'] + (ccm_jun['NETDEBT']) * 1000)

    # Calculate the free cash flow to enterprise value ratio.
    ccm_jun['fcf\_ev'] = (ccm_jun['FCF'] * 1000) / (ccm_jun['ev'])

    # Calculate the Buffett's owner's earnings to enterprise value ratio.
    ccm_jun['boe\_ev'] = ((ccm_jun['NI'] + ccm_jun['dp'] - ccm_jun['capx']) * 1000) / (ccm_jun['ev'])

    # Calculate the net income - capital expenditures to book equity ratio.
    ccm_jun['Net Income - Capital Expenditures'] = (ccm_jun['NI'] - ccm_jun['capx']) / ccm_jun['BE']

    # Calculate the operating accruals to book equity ratio.
    ccm_jun['Operating Accruals'] = ccm_jun['OACC'] / ccm_jun['BE']

    # Calculate the free cash flow to book equity ratio.
    ccm_jun['Free Cash Flow'] = ccm_jun['FCF'] / ccm_jun['BE']

    # Calculate the research and development expenses to book equity ratio.
    ccm_jun['Research and Development Expenses'] = ccm_jun['xrd'] / ccm_jun['BE']

    # Calculate the revised owner's earnings to book equity ratio.
    ccm_jun['Revised Owner\'s Earnings'] = (ccm_jun['FCF'] + ccm_jun['xrd']) / ccm_jun['BE']

    # Calculate the revised owner's earnings to enterprise value ratio.
    ccm_jun['roe\_ev'] = (((ccm_jun['FCF'] + ccm_jun['xrd'])) * 1000) / ccm_jun['ev']

    # Save the dataframe to a csv file.
    ccm_jun.to_csv('processed_crsp_jun2.csv', index=False)


def fama_macbeth_regression(list_of_predictor_lists, vars_order):
    """
    Performs Fama-MacBeth regressions using multiple sets of predictor variables and outputs the results in a single LaTeX table format. This function processes two datasets, merges them based on certain criteria, computes regressions for each specified set of predictors, and finally generates a LaTeX table summarizing the slope coefficients and statistics of each predictor across all regressions.

    Parameters:
    - list_of_predictor_lists (list of list of str): A list where each element is a list of strings, with each string representing a predictor variable's name. Each sublist corresponds to a different set of predictors to be used in a separate Fama-MacBeth regression.
    - vars_order (list of str): A list specifying the order in which predictor variables should be displayed in the output LaTeX table. This allows for customization of the table's appearance by prioritizing certain predictors over others.

    The function reads in two CSV files containing stock return data and firm characteristics, respectively, then preprocesses the data by merging these datasets, calculating additional variables, and filtering based on specific criteria. It performs the Fama-MacBeth regression for each set of predictors, collects and summarizes the results, and prints a LaTeX table containing the slope coefficients (multiplied by 100) and their corresponding t-statistics for each predictor variable across all regressions.

    The output LaTeX table is structured with predictors as rows and each regression model as a column, facilitating easy comparison of predictors' effects across different models.

    Note:
    - The CSV files 'processed_crsp_jun2.csv' and 'processed_crsp_data.csv' must be present in the working directory and formatted correctly for the function to work.
    - This function requires pandas, numpy, and statsmodels libraries for data manipulation and regression analysis.

    Example usage:
    vars_order = ['Net Income', 'Depreciation and Amortization', ...]
    fama_macbeth_regression([['Net Income'], ['Depreciation and Amortization'], ...], vars_order)
    """

    # Read in the csv files.
    ccm_jun = pd.read_csv('processed_crsp_jun2.csv', parse_dates=['jdate'])
    crsp3 = pd.read_csv('processed_crsp_data.csv', parse_dates=['jdate', 'MthCalDt'], low_memory=False)

    # Create a column for the Fama-French year.
    ccm_jun['ffyear'] = ccm_jun['jdate'].dt.year

    # Create columns for short-term reversal and momentum.
    crsp3['$r_{1,0}$'] = crsp3.groupby('PERMNO')['retadj'].apply(lambda x: x.shift(1).rolling(window=1, min_periods=1).mean())
    crsp3['$r_{12,2}$'] = crsp3.groupby('PERMNO')['retadj'].apply(lambda x: x.shift(2).rolling(window=11, min_periods=11).mean())

    # Keep only the essential columns from the monthly CRSP data.
    crsp3 = crsp3[['MthCalDt', 'PERMNO', 'SHRCD', 'EXCHCD', 'retadj', 'me', 'wt', 'cumretx', 'ffyear', 'jdate', '$r_{1,0}$', '$r_{12,2}$']]

    # Keep only the common stocks on the NYSE, NASDAQ, or AMEX exchanges.
    crsp3 = crsp3[(crsp3['EXCHCD'].isin([1, 2, 3])) & (crsp3['SHRCD'].isin([10, 11]))]

    # Initialize a dictionary to store the results for each set of predictors.
    all_results = {}

    # Iterate over each list of predictors.
    for i, predictors in enumerate(list_of_predictor_lists):

        # Merge the essential monthly CRSP data with the essential annual CCM data and the current list of predictors.
        ccm3 = pd.merge(crsp3[['MthCalDt', 'PERMNO', 'retadj', 'me', 'wt', 'ffyear', '$r_{1,0}$', '$r_{12,2}$']],
                        ccm_jun[['PERMNO', 'ffyear', 'BE\_ME', 'OP_BE', 'AT_GR1', 'dec_me'] + predictors],
                        how='left', on=['PERMNO', 'ffyear'])

        # Only keep the stocks with a positive book equity to market equity ratio.
        ccm3 = ccm3[ccm3['BE\_ME'] > 0]
        ccm3 = ccm3[ccm3['dec_me'] > 0]

        # Take the logarithm of market equity and the book equity to market equity ratio.
        ccm3['log(ME)'] = np.log(ccm3['dec_me'])
        ccm3['log(BE\_ME)'] = np.log(ccm3['BE\_ME'])

        # Rename the operating profits and asset growth columns to match the LaTeX table.
        ccm3['OP\_BE'] = ccm3['OP_BE']
        ccm3['AT\_GR1'] = ccm3['AT_GR1']

        # Define the control variables.
        controls = ['log(ME)', 'log(BE\_ME)', 'OP\_BE', 'AT\_GR1', '$r_{12,2}$']

        # Add both the predictors and controls into one variables list.
        variables = predictors + controls

        # Drop the rows with NaN variable data.
        ccm3 = ccm3.dropna(subset=['retadj'] + variables)

        # Iterate through the variables for winsorization.
        for variable in variables:

            # Determine the lower and upper bounds as the 1st and 99th percentiles.
            lower_bound = ccm3[variable].quantile(0.01)
            upper_bound = ccm3[variable].quantile(0.99)

            # Any values below or above the lower and upper bounds respectively are set to the lower and upper bounds.
            ccm3[variable] = ccm3[variable].clip(lower=lower_bound, upper=upper_bound)

        # Set the returns to be the dependent variable.
        dependent_var = 'retadj'

        # Create a constant.
        ccm3['constant'] = 1

        # Create a list to store the results of the Fama-MacBeth regressions.
        results_list = []

        # Iterate through the groups by date.
        for _, group in ccm3.groupby('MthCalDt'):

            # Set y and X to be the dependent and independent variables, respectively.
            y = group[dependent_var]
            X = group[['constant'] + variables]

            # Run the OLS regression for this time period.
            model = sm.OLS(y, X)

            # Fit the model.
            results = model.fit()

            # Save the results to our previously creating list.
            results_list.append(results.params)

        # Create a DataFrame from the results list.
        fm_results = pd.DataFrame(results_list)

        # Calculate the length, mean, and standard error of the results.
        T = len(fm_results)
        fm_mean = fm_results.mean()
        fm_se = fm_results.std()

        # Calculate the t-statistics.
        t_stats = fm_mean / (fm_se / np.sqrt(T))

        # Multiply the mean by 100 to get the percentage.
        fm_mean *= 100

        # Round the mean and t-stats to 2 decimal places
        fm_mean = fm_mean.round(2)
        t_stats = t_stats.round(2)

        # Store the results.
        all_results[f"({i+1})"] = pd.DataFrame({'Coefficient': fm_mean, 'T-Statistic': t_stats})

    # Collect all unique predictors from all models
    unique_predictors = set()
    for predictors in list_of_predictor_lists:
        unique_predictors.update(predictors)

    # Now we will order them correctly
    ordered_vars = [var for var in vars_order if var in unique_predictors] + controls

    # Initialize LaTeX table structure
    latex_str = "\\begin{table}[ht]\n\\centering\n"
    latex_str += "\\caption{Slope coefficients ($\\times 10^2$) and [test-statistics] from Fama-MacBeth regressions}\n"
    latex_str += "\\begin{tabular}{@{}l" + "c" * len(list_of_predictor_lists) + "@{}}\n"
    latex_str += "\\toprule\n"
    header_row = "\\textbf{Independent variable} & " + " & ".join([f"({i})" for i in range(1, len(list_of_predictor_lists) + 1)]) + " \\\\\n"
    latex_str += header_row
    latex_str += "\\midrule\n"

    # Construct the table rows
    for var in ordered_vars:
        coeff_row = f"{var} "
        t_stat_row = " "  # Empty string for alignment of t-stats row
        for i in range(1, len(list_of_predictor_lists) + 1):
            model_key = f"({i})"
            if var in all_results[model_key].index:
                coeff = all_results[model_key].loc[var, 'Coefficient']
                t_stat = all_results[model_key].loc[var, 'T-Statistic']
                coeff_row += f"& {coeff:.2f} "  # Format for 2 decimal places
                t_stat_row += f"& [{t_stat:.2f}] "  # Format for 2 decimal places
            else:
                # Leave the space blank for models without the predictor
                coeff_row += "& "
                t_stat_row += "& "
        coeff_row = coeff_row.strip()  # Remove trailing spaces
        t_stat_row = t_stat_row.strip()  # Remove trailing spaces
        latex_str += coeff_row + "\\\\\n"
        latex_str += t_stat_row + "\\\\\n"

    # Finish LaTeX table
    latex_str += "\\bottomrule\n"
    latex_str += "\\end{tabular}\n"
    latex_str += "\\end{table}"

    # Print the LaTeX table.
    print(latex_str)


def create_fama_french_esque_factors(predictors: List[str]):
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

        # Get the factor's 30th and 70th percentile breakpoints for each month.
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

        # Create a column that represents the combined size, factor portfolio that the stock is in.
        vwret['size_factor_portfolio'] = vwret['szport'] + vwret['factor_portfolio']

        # Tranpose the dataframes such that the rows are dates and the columns are portfolio returns.
        ff_factors = vwret.pivot(index='jdate', columns=['size_factor_portfolio'], values='vwret').reset_index()

        # Get the average return of the big and small high factor portfolios.
        ff_factors['xH'] = (ff_factors['BH'] + ff_factors['SH']) / 2

        # Get the average return of the big and small low factor portfolios.
        ff_factors['xL'] = (ff_factors['BL'] + ff_factors['SL']) / 2

        # Create the factor portfolio which is the difference between the high and low factor portfolios.
        ff_factors[predictor] = ff_factors['xH'] - ff_factors['xL']

        # Save only the necessary columns.
        factor_dfs[predictor] = ff_factors[['jdate', predictor]]

    # Set merged_factors as None to start merging the factor dataframes.
    merged_factors = None

    # Iterate through the factor dataframes.
    for predictor, df in factor_dfs.items():

        # If this is the first dataframe, set it as the merged dataframe.
        if merged_factors is None:
            merged_factors = df

        # Else merge the dataframes together.
        else:
            merged_factors = pd.merge(merged_factors, df, on='jdate', how='outer')

    # Rename the jdate column to date.
    merged_factors = merged_factors.rename(columns={'jdate': 'date'})

    # Save the merged DataFrame to a CSV file.
    merged_factors.to_csv('processed_fama_french_esque_factors.csv', index=False)


def output_summary_statistics(factors: List[str]):

    # Read in the csvs.
    fama_french_esque_factors = pd.read_csv('processed_fama_french_esque_factors.csv', parse_dates=['date'])
    replicated_factors = pd.read_csv('processed_ff_replicated.csv', parse_dates=['date'])

    # Merge the replicated factors with the list of signals passed in.
    merged_data = pd.merge(replicated_factors, fama_french_esque_factors, how='inner', on='date')

    # Ensure there are no missing values in the columns of interest.
    merged_data.dropna(inplace=True)

    # Initialize a DataFrame to store the summary statistics.
    summary_df = pd.DataFrame()

    # Loop through each factor to calculate the statistics.
    for factor in factors:

        # If the factor is in the merged data, calculate the statistics.
        if factor in merged_data.columns:

            # Calculate the mean, standard deviation, Sharpe ratio, skewness, and kurtosis
            mean = round(merged_data[factor].mean() * 12 * 100, 2)
            std_dev = round(merged_data[factor].std() * (12 ** 0.5) * 100, 2)
            sharpe = round(mean / std_dev, 2) if std_dev != 0 else None
            skewness = round(skew(merged_data[factor]), 2)
            kurt = round(kurtosis(merged_data[factor]), 2)

            # Create a new row for the summary DataFrame.
            new_row = pd.DataFrame({
                'Factor': [factor],
                'Return': [mean],
                'Volatility': [std_dev],
                'Sharpe': [sharpe],
                'Skew': [skewness],
                'Kurtosis': [kurt]
            })

            # Concatenate the new row to the summary DataFrame.
            summary_df = pd.concat([summary_df, new_row], ignore_index=True)

    # Initialize LaTeX table structure
    latex_str = "\\begin{table}[ht]\n\\centering\n"
    latex_str += "\\caption{Summary Statistics of Factors}\n"
    latex_str += "\\label{tab:summary_statistics}\n"
    latex_str += "\\begin{tabular}{@{}lrrrrr@{}}\n"
    latex_str += "\\toprule\n"
    latex_str += "Factor & Return (\\%) & Volatility (\\%) & Sharpe & Skew & Kurtosis \\\\\n"
    latex_str += "\\midrule\n"

    # Construct the table rows
    for index, row in summary_df.iterrows():
        latex_str += f"{row['Factor']} & {row['Return']:.2f}\\% & {row['Volatility']:.2f}\\% & {row['Sharpe']:.2f} & {row['Skew']:.2f} & {row['Kurtosis']:.2f} \\\\\n"

    # Finish LaTeX table
    latex_str += "\\bottomrule\n"
    latex_str += "\\end{tabular}\n"
    latex_str += "\\end{table}"

    # Print the LaTeX table.
    print(latex_str)


def regress_on_ff6(factors: List[str]):
    """
    This function performs regressions on the Fama-French 6 factor model.
    As input, it takes a list of signals for which, one by one, it will regress against the FF6.
    """

    # Read in the csvs.
    fama_french_esque_factors = pd.read_csv('processed_fama_french_esque_factors.csv', parse_dates=['date'])
    replicated_factors = pd.read_csv('processed_ff_replicated.csv', parse_dates=['date'])

    # Merge the replicated factors with the list of signals passed in.
    merged_data = pd.merge(replicated_factors, fama_french_esque_factors, how='inner', on='date')

    # Ensure there are no missing values in the columns of interest.
    merged_data.dropna(inplace=True)

    # Define the independent variables (Fama-French 6 factors).
    X = merged_data[['xRm-Rf', 'xSMB', 'xHML', 'xRMW', 'xCMA', 'xUMD']]

    # Add a constant to the independent variables matrix (for intercept)
    X = sm.add_constant(X)

    # Initialize LaTeX table structure
    latex_str = "\\begin{table}[ht]\n\\centering\n"
    latex_str += "\\caption{Regression Results on FF6 Factors}\n"
    latex_str += "\\label{tab:regression_results}\n"
    latex_str += "\\begin{tabular}{@{}l" + "rr" * len(X.columns) + "@{}}\n"
    latex_str += "\\toprule\n"
    header_row = "Factor & " + " & ".join([f"{factor}" for factor in X.columns]) + " \\\\\n"
    latex_str += header_row
    latex_str += "\\midrule\n"

    # Iterate through the factors.
    for factor in factors:

        # Set the dependent variable to be y.
        y = merged_data[factor]

        # Fit the OLS model.
        model = sm.OLS(y, X).fit()

        # Extract coefficients and t-stats.
        coef_row = f"{factor} "
        t_stat_row = " "

        # Iterate through the factors to extract the coefficients and t-stats.
        for ff_factor in X.columns:
            coef = model.params[ff_factor]
            t_stat = model.tvalues[ff_factor]
            coef_row += f"& {coef:.4f} "
            t_stat_row += f"& [{t_stat:.2f}] "

        # String manipulation to remove trailing spaces and add line breaks.
        latex_str += coef_row.rstrip() + " \\\\\n"
        latex_str += t_stat_row.rstrip() + " \\\\\n"

    # Finish LaTeX table.
    latex_str += "\\bottomrule\n"
    latex_str += "\\end{tabular}\n"
    latex_str += "\\end{table}\n"

    # Print the LaTeX table.
    print(latex_str)


def spanning_regressions(factors):
    """
    This function performs regressions of each factor against all other factors in the list.
    Each factor is regressed on the other factors, excluding itself.
    """

    # Read in the csvs.
    fama_french_esque_factors = pd.read_csv('processed_fama_french_esque_factors.csv', parse_dates=['date'])
    replicated_factors = pd.read_csv('processed_ff_replicated.csv', parse_dates=['date'])

    # Merge the replicated factors with the list of signals passed in.
    merged_data = pd.merge(replicated_factors, fama_french_esque_factors, how='inner', on='date')

    # Ensure there are no missing values in the columns of interest.
    merged_data.dropna(inplace=True)

    # Initialize LaTeX table structure
    latex_str = "\\begin{table}[ht]\n\\centering\n"
    latex_str += "\\caption{Spanning Regression Results}\n"
    latex_str += "\\label{tab:spanning_regression_results}\n"
    latex_str += "\\resizebox{\\textwidth}{!}{%\n"
    latex_str += "\\begin{tabular}{@{}l" + "c" * (len(factors) + 2) + "@{}}\n"  # +2 for Alpha and R^2
    latex_str += "\\toprule\n"
    header_row = "Dependent Variable & " + " & ".join(["Alpha"] + factors + ["$R^2$"]) + " \\\\\n"  # Add $R^2$ to header
    latex_str += header_row
    latex_str += "\\midrule\n"

    # Iterate over each factor as the dependent variable.
    for dependent_factor in factors:

        # Prepare the independent variables (all factors except the dependent one).
        independent_factors = [f for f in factors if f != dependent_factor]
        X = merged_data[independent_factors]

        # Set the dependent variable.
        y = merged_data[dependent_factor]

        # Add a constant to the independent variables for intercept (alpha).
        X = sm.add_constant(X)

        # Fit the OLS model.
        model = sm.OLS(y, X).fit()

        # Extract the R-squared value.
        r_squared = model.rsquared

        # Initialize row strings for coefficients and t-statistics.
        alpha = (1 + model.params['const']) ** 12 - 1
        coef_row_str = f"{dependent_factor} & {alpha * 100:.2f}\% "
        t_stat_row_str = " & [{:.2f}] ".format(model.tvalues['const'])

        # Iterate through the independent factors to extract the coefficients and t-stats.
        for independent_factor in factors:

            # Skip the dependent factor.
            if independent_factor == dependent_factor:
                coef_row_str += "& "
                t_stat_row_str += "& "

            # Extract the coefficient and t-statistic for the independent factor.
            else:
                coef = model.params[independent_factor]
                coef_t_stat = model.tvalues[independent_factor]
                coef_row_str += f"& {coef:.4f} "
                t_stat_row_str += f"& [{coef_t_stat:.2f}] "

        # Append R-squared at the end of the coefficients row and end the line.
        coef_row_str += f"& {r_squared:.3f} \\\\\n"

        # Append the line break for the t-statistics row.
        t_stat_row_str += "\\\\\n"

        # Add both rows to the LaTeX table string.
        latex_str += coef_row_str
        latex_str += t_stat_row_str

    # Finish LaTeX table structure.
    latex_str += "\\bottomrule\n"
    latex_str += "\\end{tabular}\n"
    latex_str += "}% End of resizebox\n"
    latex_str += "\\end{table}\n"

    # Print the LaTeX table.
    print(latex_str)


def factor_regressions(factors, control_factors):
    """
    This function performs regressions of each factor against the control factors.
    """

    # Read in the csvs.
    fama_french_esque_factors = pd.read_csv('processed_fama_french_esque_factors.csv', parse_dates=['date'])
    replicated_factors = pd.read_csv('processed_ff_replicated.csv', parse_dates=['date'])

    # Merge the replicated factors with the list of signals passed in.
    merged_data = pd.merge(replicated_factors, fama_french_esque_factors, how='inner', on='date')

    # Ensure there are no missing values in the columns of interest.
    merged_data.dropna(inplace=True)

    # Initialize LaTeX table structure
    latex_str = "\\begin{table}[ht]\n\\centering\n"
    latex_str += "\\caption{Panel Regression Results}\n"
    latex_str += "\\label{tab:panel_regression_results}\n"
    latex_str += "\\resizebox{\\textwidth}{!}{%\n"
    latex_str += "\\begin{tabular}{@{}l" + "c" * (len(control_factors) + 2) + "@{}}\n"  # +2 for Alpha and R^2
    latex_str += "\\toprule\n"
    header_row = "Dependent Variable & " + " & ".join(["Alpha"] + control_factors + ["$R^2$"]) + " \\\\\n"
    latex_str += header_row
    latex_str += "\\midrule\n"

    # Iterate over each factor as the dependent variable.
    for dependent_factor in factors:

        # Prepare the independent variables (control factors).
        X = merged_data[control_factors]
        y = merged_data[dependent_factor]

        # Add a constant to the independent variables for intercept (alpha).
        X = sm.add_constant(X)

        # Fit the OLS model.
        model = sm.OLS(y, X).fit()

        # Extract alpha (intercept) and R-squared.
        alpha = (1 + model.params['const']) ** 12 - 1
        alpha_t_stat = model.tvalues['const']
        r_squared = model.rsquared

        # Prepare coefficient row string for the LaTeX table.
        coef_row_str = f"{dependent_factor} & {alpha*100:.2f}\% "

        # Prepare t-statistics row string for the LaTeX table.
        t_stat_row_str = f"& [{alpha_t_stat:.2f}] "

        # Iterate through the control factors to extract the coefficients and t-stats.
        for control_factor in control_factors:

            # Extract the coefficient and t-statistic for the control factor.
            coef = model.params[control_factor]
            t_stat = model.tvalues[control_factor]
            coef_row_str += f"& {coef:.4f} "
            t_stat_row_str += f"& [{t_stat:.2f}] "

        # Append R-squared at the end of the coefficient row and end the line.
        coef_row_str += f"& {r_squared:.4f} \\\\\n"

        # End the t-statistics line.
        t_stat_row_str += "\\\\\n"

        # Add both rows to the LaTeX table string.
        latex_str += coef_row_str
        latex_str += t_stat_row_str

    # Finish LaTeX table structure.
    latex_str += "\\bottomrule\n"
    latex_str += "\\end{tabular}\n"
    latex_str += "}% End of resizebox\n"
    latex_str += "\\end{table}\n"

    # Print the LaTeX table.
    print(latex_str)


def perform_decile_sorts(predictor: str):
    """
    This function performs decile sorts on stocks.
    As input, it takes a string which represents the predictor.
    """

    # Read in the csv files.
    ccm_jun = pd.read_csv('processed_crsp_jun2.csv', parse_dates=['jdate'])
    crsp3 = pd.read_csv('processed_crsp_data.csv', low_memory=False)
    ff = pd.read_csv('raw_fama_french_factors.csv', parse_dates=['date'])

    # Select the universe NYSE common stocks with positive market equity.
    nyse = ccm_jun[(ccm_jun['EXCHCD'] == 1) &
                   (ccm_jun['me'] > 0) &
                   (ccm_jun['dec_me'] > 0) &
                   (ccm_jun['count'] >= 1) &
                   ((ccm_jun['SHRCD'] == 10) | (ccm_jun['SHRCD'] == 11))]

    # Get the decile breakpoints for each month.
    nyse_breaks = nyse.groupby(['jdate'])[predictor].describe(percentiles=[0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]).reset_index()
    nyse_breaks = nyse_breaks[['jdate', '10%', '20%', '30%', '40%', '50%', '60%', '70%', '80%', '90%']]

    # Merge the decile breakpoints with the CCM June data.
    ccm1_jun = pd.merge(ccm_jun, nyse_breaks, how='left', on=['jdate'])

    # Assign each stock to its proper book to market bucket.
    ccm1_jun['decile_portfolio'] = np.where(
        (ccm_jun['dec_me'] > 0) & (ccm1_jun['me'] > 0) & (ccm1_jun['count'] >= 1),
        ccm1_jun.apply(lambda row: decile_bucket(row, predictor), axis=1),
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
        (ccm1_jun['decile_portfolio'] != ''),
        1,
        0
    )

    # Create a new dataframe with only the essential columns for storing the portfolio assignments as of June.
    june = ccm1_jun[['PERMNO', 'MthCalDt', 'jdate', 'decile_portfolio', 'valid_data', 'non_missing_portfolio']].copy()

    # Create a column representing the Fama-French year.
    june['ffyear'] = june['jdate'].dt.year

    # Keep only the essential columns.
    crsp3 = crsp3[['MthCalDt', 'PERMNO', 'SHRCD', 'EXCHCD', 'retadj', 'me', 'wt', 'cumretx', 'ffyear', 'jdate']]

    # Merge monthly CRSP data with the portfolio assignments in June.
    ccm3 = pd.merge(crsp3,
                    june[['PERMNO', 'ffyear', 'decile_portfolio', 'valid_data', 'non_missing_portfolio']],
                    how='left', on=['PERMNO', 'ffyear'])

    # Keep only the common stocks with a positive weight, valid data, and a non-missing portfolio.
    ccm4 = ccm3[(ccm3['wt'] > 0) &
                (ccm3['valid_data'] == 1) &
                (ccm3['non_missing_portfolio'] == 1) &
                ((ccm3['SHRCD'] == 10) | (ccm3['SHRCD'] == 11))]

    # Create a dataframe for the value-weighted returns.
    vwret = ccm4.groupby(['jdate', 'decile_portfolio']).apply(wavg, 'retadj', 'wt').to_frame().reset_index().rename(columns={0: 'vwret'})

    # Tranpose the dataframes such that the rows are dates and the columns are portfolio returns.
    decile_portfolios = vwret.pivot(index='jdate', columns=['decile_portfolio'], values='vwret').reset_index()

    # Rename the jdate column to date.
    decile_portfolios = decile_portfolios.rename(columns={'jdate': 'date'})

    # DataFrame to store statistics
    stats_df = pd.DataFrame(columns=['Portfolio', 'Mean', 'Std Dev', 'Annual Return', 'Annual Std Dev', 'Sharpe Ratio'])

    # Change the date to a datetime object.
    ff['date'] = pd.to_datetime(ff['date'], format='%Y%m').dt.to_period('M').dt.to_timestamp('M')

    # Create a date column in the decile portfolios DataFrame.
    decile_portfolios['date'] = pd.to_datetime(decile_portfolios['date'])

    # Merge ff_factors with the risk-free rate data
    ff_factors = ff[['date', 'RF', 'Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA', 'UMD']]
    decile_portfolios = pd.merge(decile_portfolios, ff_factors, on='date', how='inner')

    # Create a '10-1' column which is the difference between the 10th and 1st decile portfolios.
    decile_portfolios['10-1'] = decile_portfolios['10'] - decile_portfolios['1']

    # reorder the columns such that it is date, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 10-1, Mkt-RF, SMB, HML, RMW, CMA, UMD
    decile_portfolios = decile_portfolios[['date', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '10-1', 'Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA', 'UMD', 'RF']]

    # Create a DataFrame to store the statistics.
    stats_df = pd.DataFrame(columns=['Portfolio', 'Alpha', 'tstat', 'Excess Return', 'Volatility', 'Sharpe Ratio'])

    # Iterate over the decile portfolios to calculate the statistics.
    for column in list(decile_portfolios.columns[1:12]):

        # If not the 10-1 column, subtract the risk-free rate from the portfolio returns.
        if column != '10-1':
            portfolio_returns = decile_portfolios[column] - (decile_portfolios['RF'] / 100)

        # If the 10-1 column, use the portfolio returns as is.
        else:
            portfolio_returns = decile_portfolios[column]

        # Set the independent variables for the regression.
        X = decile_portfolios[['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA', 'UMD']]
        X = sm.add_constant(X)

        # Fit the OLS model.
        model = sm.OLS(portfolio_returns, X).fit()
        alpha = model.params['const']
        alpha_t_stat = model.tvalues['const']

        # Calculate the mean, standard deviation, and Sharpe ratio.
        mean = (1 + portfolio_returns.mean()) ** 12 - 1
        std_dev = portfolio_returns.std() * (12 ** 0.5)
        sharpe_ratio = mean / std_dev

        # Append the statistics to the DataFrame.
        stats_df = stats_df.append({
            'Portfolio': column,
            'Alpha': f"{alpha * 100 * 12:.2f}\%",
            'tstat': f"{alpha_t_stat:.2f}",
            'Excess Return': f"{mean * 100:.2f}\%",
            'Volatility': f"{std_dev * 100:.2f}\%",
            'Sharpe Ratio': f"{sharpe_ratio:.2f}"
        }, ignore_index=True)

    # Set the index of the DataFrame to the Portfolio column.
    stats_df = stats_df.set_index('Portfolio')

    # Initialize LaTeX table structure with proper formatting
    latex_str = "\\begin{table}[ht]\n\\centering\n"
    latex_str += "\\caption{Decile Portfolio Statistics}\n"
    latex_str += "\\label{tab:decile_portfolio_statistics}\n"
    latex_str += "\\begin{tabular}{@{}lcccccc@{}}\n"  # Define the column alignment
    latex_str += "\\toprule\n"
    latex_str += "Portfolio & Alpha [t-stat] & Annual Return & Annual Std Dev & Sharpe Ratio \\\\\n"  # Header row
    latex_str += "\\midrule\n"

    # Iterate over rows to populate the table
    for index, row in stats_df.iterrows():

        # Combine alpha and t-stat in one column for compactness
        alpha_tstat = f"{row['Alpha']} [{row['tstat']}]"

        # Format other columns
        row_str = f"{index} & {alpha_tstat} & {row['Excess Return']} & {row['Volatility']} & {row['Sharpe Ratio']} \\\\\n"
        latex_str += row_str

    # Finish LaTeX table structure
    latex_str += "\\bottomrule\n"
    latex_str += "\\end{tabular}\n"
    latex_str += "\\end{table}\n"

    # Print the LaTeX table.
    print(latex_str)

    # save the decile portfolios to a csv
    decile_portfolios.to_csv('processed_decile_portfolios.csv', index=False)


def display_cumulative_returns(factors: List[str], legend_names: Dict[str, str]):
    """
    This function graphs the cumulative returns of the given  portfolios.
    """

    # Read in the csvs.
    fama_french_esque_factors = pd.read_csv('processed_fama_french_esque_factors.csv', parse_dates=['date'])
    replicated_factors = pd.read_csv('processed_ff_replicated.csv', parse_dates=['date'])
    decile_portfolios = pd.read_csv('processed_decile_portfolios.csv', parse_dates=['date'])

    # Merge the replicated factors with the list of signals passed in and the decile portfolios.
    merged_data = pd.merge(replicated_factors, fama_french_esque_factors, how='inner', on='date')
    merged_data = pd.merge(merged_data, decile_portfolios, how='inner', on='date')

    # Ensure there are no missing values for a given date.
    merged_data.dropna(inplace=True)

    # Only keep the date and the factors of interest.
    merged_data = merged_data[['date'] + factors]

    # Set the data frame index to 'date'.
    merged_data = merged_data.set_index('date')

    # Calculate the cumulative returns, adjusting the starting point to 100.
    cum_returns = 100 * (1 + merged_data).cumprod()

    # Rename columns based on the provided legend names for plotting.
    cum_returns.rename(columns=legend_names, inplace=True)

    # Plot the cumulative returns.
    cum_returns.plot(figsize=(12, 8), logy=True)
    plt.title('Cumulative Returns of Factors')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Return')
    plt.yscale('log')
    plt.legend(title='Factors')

    # Save the image.
    plt.savefig('processed_cumulative_returns.png')


def produce_results():
    """
    This script calls the function to generate the variables, conduct the Fama-MacBeth regressions,
    create the Fama-French-esque factors, and perform decile sorts.
    """

    start_time = time.time()
    generate_variables()
    end_time = time.time()
    print("Generated Variables.")
    print("Time Elapsed: ", end_time - start_time)

    # Table 1
    start_time = time.time()
    vars_order = ['Net Income', 'Net Income - Capital Expenditures', 'Depreciation and Amortization', 'Capital Expenditures', 'Enterprise Value',
                  'Operating Accruals', 'Free Cash Flow', 'Research and Development Expenses', 'Revised Owner\'s Earnings', 'Buffett\'s Owner\'s Earnings']
    fama_macbeth_regression([['Net Income'], ['Depreciation and Amortization'], ['Capital Expenditures'], ['Enterprise Value'], ['Net Income', 'Depreciation and Amortization', 'Capital Expenditures', 'Enterprise Value'], ['Buffett\'s Owner\'s Earnings']], vars_order)
    end_time = time.time()
    print("Conducted Fama-MacBeth Regressions.")
    print("Time Elapsed: ", end_time - start_time)

    start_time = time.time()
    create_fama_french_esque_factors(['ni\_me', 'ocf\_me', 'div\_me', 'cop\_me', 'fcf\_ev', 'boe\_ev', 'roe\_ev'])
    end_time = time.time()
    print("Created Fama-French-esque factors.")
    print("Time Elapsed: ", end_time - start_time)

    # Table 2
    start_time = time.time()
    output_summary_statistics(['xRm-Rf', 'xSMB', 'xHML', 'xRMW', 'xCMA', 'xUMD', 'ni\_me', 'ocf\_me', 'div\_me', 'cop\_me', 'fcf\_ev', 'boe\_ev'])
    end_time = time.time()
    print("Outputed Summary Statistics.")
    print("Time Elapsed: ", end_time - start_time)

    # Table 3
    start_time = time.time()
    regress_on_ff6(['boe\_ev'])
    end_time = time.time()
    print("Regressed on FF6.")
    print("Time Elapsed: ", end_time - start_time)

    # Table 4
    start_time = time.time()
    fama_macbeth_regression([['Net Income - Capital Expenditures', 'Depreciation and Amortization', 'Operating Accruals'], ['Free Cash Flow', 'Research and Development Expenses'], ['Revised Owner\'s Earnings'], ['Buffett\'s Owner\'s Earnings'], ['Revised Owner\'s Earnings', 'Buffett\'s Owner\'s Earnings']])
    end_time = time.time()
    print("Conducted Fama-MacBeth Regressions.")
    print("Time Elapsed: ", end_time - start_time)

    # Table 5
    start_time = time.time()
    output_summary_statistics(['boe\_ev', 'fcf\_ev', 'roe\_ev'])
    end_time = time.time()
    print("Outputed Summary Statistics.")
    print("Time Elapsed: ", end_time - start_time)

    # Table 6
    start_time = time.time()
    spanning_regressions(['xRm-Rf', 'xSMB', 'xHML', 'xRMW', 'xCMA', 'xUMD', 'roe\_ev'])
    end_time = time.time()
    print("Performed spanning regressions.")
    print("Time Elapsed: ", end_time - start_time)

    # Table 7
    start_time = time.time()
    factor_regressions(['ni\_me', 'ocf\_me', 'div\_me', 'cop\_me', 'fcf\_ev', 'boe\_ev'], ['xRm-Rf', 'xSMB', 'xRMW', 'xCMA', 'xUMD', 'roe\_ev'])
    end_time = time.time()
    print("Performed panel regressions.")
    print("Time Elapsed: ", end_time - start_time)

    # Table 8
    start_time = time.time()
    perform_decile_sorts('roe\_ev')
    end_time = time.time()
    print("Performed decile sorts.")
    print("Time Elapsed: ", end_time - start_time)

    # Table 9
    start_time = time.time()
    display_cumulative_returns(['xRm-Rf', 'xHML', 'roe\_ev', '10'], {'xRm-Rf': 'Rm-RF', 'xHML': 'HML', 'roe\_ev': 'roe_ev', '10': 'Decile 10'})
    end_time = time.time()
    print("Displayed cumulative returns.")
    print("Time Elapsed: ", end_time - start_time)
