# Import the necessary libraries.
import re
import pandas as pd
from typing import List, Dict
import numpy as np
import statsmodels.api as sm
import time
from replicate_fama_french import sz_bucket, factor_bucket, wavg
from scipy.stats import skew, kurtosis, zscore
from scipy.stats.mstats import winsorize
import matplotlib.pyplot as plt
from process_data import coalesce
from pathlib import Path
from joblib import Parallel, delayed
import dask.dataframe as dd
from dask.delayed import delayed


def latex_escape(text):
    """
    Escape special characters in the given text with their LaTeX equivalents.

    Args:
        text (str): The input text containing special characters.

    Returns:
        str: The text with special characters replaced by their LaTeX equivalents.
    """

    # Define the mapping of special characters to their LaTeX equivalents.
    LATEX_MAPPING = {
        '&': r'\&',
        '%': r'\%',
        '#': r'\#',
        '_': r'\_',
        '{': r'\{',
        '}': r'\}',
        '~': r'\textasciitilde',
        '^': r'\textasciicircum',
        '\\': r'\textbackslash',
        '−': r'-',
    }

    # Create a regular expression pattern to match special characters.
    LATEX_REGEX = re.compile('|'.join(re.escape(str(key)) for key in LATEX_MAPPING.keys()))

    # Replace special characters with their LaTeX equivalents.
    return LATEX_REGEX.sub(lambda mo: LATEX_MAPPING[mo.group()], text)


def get_decile_bucket(factor_value, decile_thresholds):
    """
    Assign a value to the correct decile bucket based on factor value and decile thresholds.

    Args:
        factor_value (float): The factor value to be assigned to a decile bucket.
        decile_thresholds (list): A list of decile thresholds in ascending order.

    Returns:
        str: The decile bucket as a string value from '1' to '10', or an empty string if not found.
    """

    # Iterate over the decile thresholds and assign the factor value to the corresponding decile bucket.
    for i, threshold in enumerate(decile_thresholds, 1):

        # Check if the factor value is less than or equal to the current threshold.
        if factor_value <= threshold:

            # Return the decile bucket as a string value.
            return str(i)

    # Return '10' if the factor value is greater than the last threshold.
    return '10' if factor_value > decile_thresholds[-1] else ''


def decile_bucket(row, factor):
    """
    Assign a stock to the correct decile bucket based on the factor value.

    Args:
        row (pandas.Series): A row from a pandas DataFrame containing factor values and decile thresholds.
        factor (str): The name of the factor column in the DataFrame.

    Returns:
        str: The decile bucket as a string value from '1' to '10', or an empty string if not found.
    """

    # Get the decile thresholds from the row.
    decile_thresholds = [row[f'{i}0%'] for i in range(1, 10)]

    # Return the decile bucket for the factor value.
    return get_decile_bucket(row[factor], decile_thresholds)


def calculate_variables(df):
    """
    Calculate various financial variables for the given DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame containing financial data.

    Returns:
        pd.DataFrame: The DataFrame with calculated financial variables.
        
    This function contains a variety of Compustat variable abbreviations and acronyms, which might cause confusion.
    
    To remedy this, the full Compustat names will be included here:
    - sic: Standard Industrial Classification Code
    - ib: Income Before Extraordinary Items
    - ni: Net Income
    - txt: Income Taxes - Total
    - mii: Noncontrolling Interest (Income Account)
    - xido: Extraordinary Items and Discontinued Operations
    - xi: Extraordinary Items
    - do: Discontinued Operations
    - pi: Pretax Income
    - xint: Interest and Related Expense - Total
    - spi: Special Items
    - nopi: Nonoperating Income (Expense)
    - ebit: Earnings Before Interest and Taxes
    - oiadp: Operating Income After Depreciation
    - dp: Depreciation and Amortization
    - oancf: Operating Activities - Net Cash Flow
    - wcap: Working Capital (Balance Sheet)
    - che: Cash and Short-Term Investments
    - act: Current Assets - Total
    - rect: Receivables - Total
    - invt: Inventories - Total
    - aco: Current Assets - Other - Total
    - dlc: Debt in Current Liabilities - Total
    - lct: Current Liabilities - Total
    - ap: Accounts Payable - Trade
    - txp: Income Taxes Payable
    - lco: Current Liabilities - Other - Total
    - ivao: Investment and Advances - Other
    - lt: Liabilities - Total
    - dltt: Long-Term Debt - Total
    - capx: Capital Expenditures
    - xrd: Research and Development Expense
    - dvt: Dividends - Total
    - dv: Cash Dividends (Cash Flow)
    - sstk: Sale of Common and Preferred Stock
    - prstkc: Purchase of Common and Preferred Stock
    - re: Retained Earnings
    - acominc: Accumulated Other Comprehensive Income (Loss)
    """

    # Calculate 'XIDO' as 'xido', and if missing, use 'xi' + 'do' (if missing, use 0).
    df['XIDO'] = coalesce(df['xido'], df['xi'] + df['do'].fillna(0))

    # Calculate 'EBIT' as 'ebit', if missing, use 'oiadp', and if missing, use 'EBITDA' - 'dp'.
    df['EBIT'] = coalesce(df['ebit'], df['oiadp'], df['EBITDA'] - df['dp'])

    # Calculate 'PI' as 'pi', if missing, use 'EBIT' - 'xint' + 'spi' (if missing, use 0) + 'nopi' (if missing, use 0).
    df['PI'] = coalesce(df['pi'], df['EBIT'] - df['xint'] + df['spi'].fillna(0) + df['nopi'].fillna(0))

    # Calculate 'NI' as 'ib', if missing, use 'ni' - 'XIDO', and if missing, use 'PI' - 'txt' - 'mii' (if missing, use 0).
    df['NI'] = coalesce(df['ib'], df['ni'] - df['XIDO'], df['PI'] - df['txt'] - df['mii'].fillna(0))

    # Calculate 'CA' as 'act', if missing, use 'rect' + 'invt' + 'che' + 'aco'.
    df['CA'] = coalesce(df['act'], df['rect'] + df['invt'] + df['che'] + df['aco'])

    # Calculate 'COA' as 'CA' - 'che'.
    df['COA'] = df['CA'] - df['che']

    # Calculate 'CL' as 'lct', if missing, use 'ap' + 'dlc' + 'txp' + 'lco'.
    df['CL'] = coalesce(df['lct'], df['ap'] + df['dlc'] + df['txp'] + df['lco'])

    # Calculate 'COL' as 'CL' - 'dlc' (if missing, use 0).
    df['COL'] = df['CL'] - df['dlc'].fillna(0)

    # Calculate 'COWC' as 'COA' - 'COL'.
    df['COWC'] = df['COA'] - df['COL']

    # Calculate 'NCOA' as 'AT' - 'CA' - 'ivao'.
    df['NCOA'] = df['AT'] - df['CA'] - df['ivao']

    # Calculate 'NCOL' as 'lt' - 'CL' - 'dltt'.
    df['NCOL'] = df['lt'] - df['CL'] - df['dltt']

    # Calculate 'NNCOA' as 'NCOA' - 'NCOL'.
    df['NNCOA'] = df['NCOA'] - df['NCOL']

    # Calculate 'OACC' as 'NI' - 'oancf', and if missing, use the yearly change in 'COWC' + the yearly change in 'NNCOA'.
    df['OACC'] = coalesce(df['NI'] - df['oancf'], df['COWC'].diff() + df['NNCOA'].diff())

    # Calculate 'OCF' as 'oancf', if missing, use 'NI' - 'OACC', and if missing, use 'NI' + 'dp' - 'wcap' (if missing, use 0).
    df['OCF'] = coalesce(df['oancf'], df['NI'] - df['OACC'], df['NI'] + df['dp'] - df['wcap'].fillna(0))

    # Calculate 'FCF' as 'OCF' - 'capx'.
    df['FCF'] = df['OCF'] - df['capx']

    # Calculate 'COP' as 'EBITDA' + 'xrd' (if missing, use 0) - 'OACC'.
    df['COP'] = df['EBITDA'] + df['xrd'].fillna(0) - df['OACC']

    # Calculate 'DIV' as 'dvt', if missing, use 'dv'.
    df['DIV'] = coalesce(df['dvt'], df['dv'])

    # Calculate 'EQBB' as 'prstkc' (if missing, use 0).
    df['EQBB'] = df['prstkc'].fillna(0)

    # Calculate 'EQIS' as 'sstk' (if missing, use 0).
    df['EQIS'] = df['sstk'].fillna(0)

    # Calculate 'EQNIS' as 'EQIS' (if missing, use 0) - 'EQBB' (if missing, use 0).
    df['EQNIS'] = df['EQIS'].fillna(0) - df['EQBB'].fillna(0)

    # Calculate 'NP' as 'DIV' + 'EQBB'.
    df['NP'] = df['DIV'] - df['EQNIS']
    
    # Calculate 'RE' as 're' - 'acominc' (if missing, use 0).
    df['RE'] = df['re'] - df['acominc'].fillna(0)

    # Calculate 'BOP' as 'EBITDA' + 'xrd' (if missing, use 0).
    df['BOP'] = df['EBITDA'] + df['xrd'].fillna(0)

    # Return the DataFrame with calculated variables.
    return df


def calculate_ratios(df):
    """
    Calculate various financial ratios for the given DataFrame.

    Args:
        df (pd.DataFrame): The input DataFrame containing financial data.

    Returns:
        pd.DataFrame: The DataFrame with calculated financial ratios.
    """

    # Calculate the Book Equity to Market Equity ratio.
    df['Book Equity to Market Equity'] = df['BE'] * 1000 / df['dec_me']

    # Calculate the Sales to Market Equity ratio.
    df['Sales to Market Equity'] = df['SALE'] * 1000 / df['dec_me']

    # Calculate the Net Income to Market Equity ratio.
    df['Net Income to Market Equity'] = df['NI'] * 1000 / df['dec_me']

    # Calculate the Operating Cash Flow to Market Equity ratio.
    df['Operating Cash Flow to Market Equity'] = df['OCF'] * 1000 / df['dec_me']

    # Calculate the Free Cash Flow to Market Equity ratio.
    df['Free Cash Flow to Market Equity'] = df['FCF'] * 1000 / df['dec_me']

    # Calculate the Dividends to Market Equity ratio.
    df['Dividends to Market Equity'] = df['DIV'] * 1000 / df['dec_me']

    # Calculate the Net Payouts to Market Equity ratio.
    df['Net Payouts to Market Equity'] = df['NP'] * 1000 / df['dec_me']

    # Calculate the Retained Earnings to Market Equity ratio.
    df['Retained Earnings to Market Equity'] = df['RE'] * 1000 / df['dec_me']

    # Calculate the Cash-Based Operating Profits to Market Equity ratio.
    df['Cash-Based Operating Profits to Market Equity'] = df['COP'] * 1000 / df['dec_me']

    # Calculate the Capital Expenditures to Market Equity ratio.
    df['Capital Expenditures to Market Equity'] = df['capx'] * 1000 / df['dec_me']

    # Calculate the Owner's Earnings to Market Equity ratio.
    df['Owner\'s Earnings to Market Equity'] = (df['COP'] - df['capx']) * 1000 / df['dec_me']

    # Calculate the Gross Profits to Total Assets ratio.
    df['Gross Profits to Total Assets'] = df['GP'] / df['AT']

    # Calculate the Operating Profits to Total Assets ratio.
    df['Operating Profits to Total Assets'] = df['BOP'] / df['AT']

    # Calculate the Cash-Based Operating Profits to Total Assets ratio.
    df['Cash-Based Operating Profits to Total Assets'] = df['COP'] / df['AT']

    # Calculate the Capital Expenditures to Total Assets ratio.
    df['Capital Expenditures to Total Assets'] = df['capx'] / df['AT']

    # Calculate the Owner's Earnings to Total Assets ratio.
    df['Owner\'s Earnings to Total Assets'] = (df['COP'] - df['capx']) / df['AT']

    # Calculate the Cash-Based Operating Profits to Book Equity ratio.
    df['Cash-Based Operating Profits to Book Equity'] = df['COP'] / df['BE']

    # Calculate the Gross Profits to Book Equity ratio.
    df['Gross Profits to Book Equity'] = df['GP'] / df['BE']

    # Calculate the Operating Profits to Book Equity ratio.
    df['Operating Profits to Book Equity'] = df['BOP'] / df['BE']

    # Calculate the Capital Expenditures to Book Equity ratio.
    df['Capital Expenditures to Book Equity'] = df['capx'] / df['BE']

    # Calculate the Owner's Earnings to Book Equity ratio.
    df['Owner\'s Earnings to Book Equity'] = (df['COP'] - df['capx']) / df['BE']

    # Calculate the Owner's Earnings Composite metric.
    df['Owner\'s Earnings Composite'] = df.groupby('MthCalDt')['Owner\'s Earnings to Market Equity'].rank() + df.groupby('MthCalDt')['Owner\'s Earnings to Total Assets'].rank() + df.groupby('MthCalDt')['Owner\'s Earnings to Book Equity'].rank()

    # Return the DataFrame with calculated ratios.
    return df


def generate_variables():
    """
    Generate variables beyond the previously generated Compustat variables.

    This function reads the processed_crsp_jun1.csv file, filters the data,
    calculates various financial variables and ratios, and saves the result
    to a new csv file named processed_crsp_jun2.csv.
    """

    # Read in the csv file.
    df = pd.read_csv('processed_crsp_jun1.csv', parse_dates=['jdate'])

    # Only keep the NYSE, AMEX, and NASDAQ stocks.
    df = df[df['EXCHCD'].isin([1, 2, 3])]

    # Only keep the orindary common shares.
    df = df[df['SHRCD'].isin([10, 11])]

    # Remove the financial firms.
    df = df[df['sic'].astype(str).str[0] != '6']

    # Ensure that we have non-missing values for book equity, market equity, and the current monthly return.
    df = df.dropna(subset=['BE', 'AT', 'dec_me', 'retadj'])

    # Calculate the variables.
    df = calculate_variables(df)

    # Calculate the ratios.
    df = calculate_ratios(df)

    # Save the DataFrame to a csv file.
    df.to_csv('processed_crsp_jun2.csv', index=False)


def process_period_data(period_data, variable, correlation_variables):
    """
    Process data for a specific period and variable.

    Args:
        period_data (DataFrame): Data for a specific period.
        variable (str): Variable to process.
        correlation_variables (list): Variables for correlation calculation.

    Returns:
        tuple: Summary statistics, Pearson correlation matrix, and Spearman correlation matrix.
    """

    # Ensure the variable is numeric and replace infinite values with NaN.
    period_data[variable] = pd.to_numeric(period_data[variable], errors='coerce').replace([np.inf, -np.inf], np.nan)

    # Winsorize the variable to remove outliers.
    lower_bound = period_data[variable].quantile(0.01)
    upper_bound = period_data[variable].quantile(0.99)
    period_data[variable] = period_data[variable].apply(lambda x: x if pd.isnull(x) else max(min(x, upper_bound), lower_bound))

    # Calculate the required summary statistics for the winsorized data
    stats = {
        'Mean': period_data[variable].mean(skipna=True),
        'SD': period_data[variable].std(skipna=True),
        '1st': period_data[variable].quantile(0.01),
        '25th': period_data[variable].quantile(0.25),
        '50th': period_data[variable].quantile(0.5),
        '75th': period_data[variable].quantile(0.75),
        '99th': period_data[variable].quantile(0.99)
    }

    # Calculate the Pearson and Spearman correlation
    pearson_matrix = period_data[correlation_variables].corr(method='pearson')
    spearman_matrix = period_data[correlation_variables].corr(method='spearman')

    # Return the summary statistics, Pearson correlation matrix, and Spearman correlation
    return stats, pearson_matrix, spearman_matrix


def generate_variable_descriptive_statistics(distribution_variables: List[str], correlation_variables: List[str], title, short_description, long_description, ouput_file: str):
    """
    Generate descriptive statistics for variables and export to a LaTeX file.

    Args:
        distribution_variables (list): Variables for distribution analysis.
        correlation_variables (list): Variables for correlation analysis.
        title (str): Title of the LaTeX table.
        short_description (str): Short description for the LaTeX table.
        long_description (str): Long description for the LaTeX table.
        output_file (str): Output file path for the LaTeX table.

    Returns:
        str: Path of the generated LaTeX file.
    """

    # Read in the csv files.
    ccm_jun = pd.read_csv('processed_crsp_jun2.csv', parse_dates=['jdate'])
    crsp3 = pd.read_csv('processed_crsp_data.csv', parse_dates=['jdate', 'MthCalDt'], low_memory=False)

    # Create a column for the Fama-French year.
    ccm_jun['ffyear'] = ccm_jun['jdate'].dt.year

    # Create columns for short-term reversal and momentum.
    crsp3['r_{1,0}'] = crsp3.groupby('PERMNO')['retadj'].shift(1).rolling(window=1, min_periods=1).mean()
    crsp3['r_{12,2}'] = crsp3.groupby('PERMNO')['retadj'].shift(2).rolling(window=11, min_periods=11).sum()

    # Keep only the essential columns from the monthly CRSP data.
    crsp3 = crsp3[['MthCalDt', 'PERMNO', 'SHRCD', 'EXCHCD', 'retadj', 'me', 'wt', 'cumretx', 'ffyear', 'jdate', 'r_{1,0}', 'r_{12,2}']]

    # Keep only the common stocks on the NYSE, NASDAQ, or AMEX exchanges.
    crsp3 = crsp3[(crsp3['EXCHCD'].isin([1, 2, 3])) & (crsp3['SHRCD'].isin([10, 11]))]

    # Get the union of the distribution and correlation variables.
    all_variables = list(set(distribution_variables + correlation_variables))

    # Merge the monthly CRSP data with the annual CCM data.
    ccm3 = pd.merge(crsp3[['MthCalDt', 'PERMNO', 'retadj', 'me', 'wt', 'ffyear', 'r_{1,0}', 'r_{12,2}']],
                    ccm_jun[['PERMNO', 'ffyear', 'dec_me', 'Book Equity to Market Equity', 'BE', 'AT'] + all_variables],
                    how='left', on=['PERMNO', 'ffyear'])

    # Only keep the rows with a date of 1963-07-30 or later.
    ccm3 = ccm3[ccm3['MthCalDt'] >= '1963-07-30']

    # Ensure that we have non-missing values for book equity, market equity, and the current monthly return.
    ccm3 = ccm3.dropna(subset=['BE', 'AT', 'dec_me', 'retadj'])

    # Ensure that we have positive values for book equity and total assets.
    ccm3 = ccm3[(ccm3['BE'] > 0) & (ccm3['AT'] > 0)]

    # Ensure data types are suitable for operations.
    ccm3['dec_me'] = pd.to_numeric(ccm3['dec_me'], errors='coerce')
    ccm3['Book Equity to Market Equity'] = pd.to_numeric(ccm3['Book Equity to Market Equity'], errors='coerce')

    # Apply log transformations
    ccm3['log(ME)'] = np.log1p(ccm3['dec_me'] * 1000)
    ccm3['log(BE/ME)'] = np.log1p(ccm3['Book Equity to Market Equity'])

    # Create a list of all variables including the newly created log variables
    all_variables = distribution_variables + ['log(ME)', 'log(BE/ME)', 'r_{1,0}', 'r_{12,2}']

    # Get unique periods (MthCalDt)
    periods = ccm3['MthCalDt'].unique()

    # Create a Dask DataFrame from ccm3
    ddf = dd.from_pandas(ccm3, npartitions=8)

    # Process data for each period in parallel using Dask
    results = []
    for period in periods:
        period_data = ddf[ddf['MthCalDt'] == period]
        for variable in all_variables:
            result = delayed(process_period_data)(period_data, variable, correlation_variables)
            results.append(result)

    results = dd.compute(*results)

    # Separate the results into summary statistics, Pearson matrices, and Spearman matrices
    period_stats = [result[0] for result in results]
    pearson_matrices = [result[1] for result in results[::len(all_variables)]]
    spearman_matrices = [result[2] for result in results[::len(all_variables)]]

    # Calculate the average of each statistic across periods
    summary_statistics = {variable: {k: np.mean([d[k] for d in period_stats[i::len(all_variables)]]) for k in period_stats[0]} for i, variable in enumerate(all_variables)}

    # Calculate the average of Pearson and Spearman correlation matrices
    avg_pearson_matrix = sum(pearson_matrices) / len(pearson_matrices)
    avg_pearson_matrix = avg_pearson_matrix.round(3)
    avg_spearman_matrix = sum(spearman_matrices) / len(spearman_matrices)
    avg_spearman_matrix = avg_spearman_matrix.round(3)

    # Convert the summary_statistics dictionary to a pandas DataFrame for easy LaTeX export
    summary_df = pd.DataFrame.from_dict(summary_statistics, orient='index')
    summary_df.index.name = 'Variable'
    summary_df = summary_df.reset_index()

    # Create LaTeX table content
    num_vars = max(8, len(correlation_variables))
    latex_content = [
        "\\begin{table*}[ht!]",
        "\\textbf{" + title + "} \\\\",
        latex_escape(short_description) + "\\\\",
        "\\hspace*{1em} " + latex_escape(long_description),
        "\\begin{tabularx}{\\textwidth}{X*{7}{r}}",
        "\\toprule",
        "\\multicolumn{8}{l}{\\textit{" + latex_escape("Panel A: Distributions of Major Variables Employed") + "}} \\\\",
        "\\midrule",
        "Variable & Mean & SD & 1st & 25th & 50th & 75th & 99th \\\\",
        "\\midrule"
    ]

    # Adding rows from the dataframe to LaTeX table
    for _, row in summary_df.iterrows():
        row_list = []
        for val in row:
            if isinstance(val, float):
                val_str = f"{val:.3f}"
            else:
                if '_' in val and '{' in val and '}' in val:
                    val_str = val.replace('_', '_').replace('{', '{').replace('}', '}')
                    val_str = f"${val_str}$"
                else:
                    val_str = latex_escape(val)
            row_list.append(val_str)
        row_str = " & ".join(row_list)
        latex_content.append(row_str + " \\\\")

    # Add Pearson Correlations Panel to LaTeX content
    latex_content.extend([
        "\\midrule",
        "\\multicolumn{" + str(num_vars) + "}{l}{\\textit{" + latex_escape("Panel B: Selected Pearson Correlations") + "}} \\\\",
        "\\midrule",
    ])

    # Iterate over rows to create the triangular matrix for Pearson
    for row_idx, row in enumerate(avg_pearson_matrix.itertuples(index=False, name=None)):
        row_values = [f"{v:.3f}" if i < row_idx else "1.000" if i == row_idx else "" for i, v in enumerate(row)]
        latex_content.append(latex_escape(str(avg_pearson_matrix.index[row_idx])) + " & " + " & ".join(row_values) + " \\\\")

    # Add Spearman Correlations Panel to LaTeX content
    latex_content.extend([
        "\\midrule",
        "\\multicolumn{" + str(num_vars) + "}{l}{\\textit{" + latex_escape("Panel C: Selected Spearman Correlations") + "}} \\\\",
        "\\midrule",
    ])

    # Iterate over rows to create the triangular matrix for Spearman
    for row_idx, row in enumerate(avg_spearman_matrix.itertuples(index=False, name=None)):
        row_values = [f"{v:.3f}" if i < row_idx else "1.000" if i == row_idx else "" for i, v in enumerate(row)]
        latex_content.append(latex_escape(str(avg_spearman_matrix.index[row_idx])) + " & " + " & ".join(row_values) + " \\\\")

    # Closing the table environment
    latex_content.extend([
        "\\bottomrule",
        "\\end{tabularx}",
        "\\end{table*}"
    ])

    # Join the content and write to a .tex file
    tex_file_path = Path(ouput_file)
    with open(tex_file_path, 'w') as tex_file:
        tex_file.write("\n".join(latex_content))

    return str(tex_file_path)


def fama_macbeth_regression(list_of_predictor_lists, vars_order, title, short_description, long_description, output_file):

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

    # Calculate the 20th percentile of NYSE stocks' market equity each month.
    nyse_thresholds = crsp3[crsp3['EXCHCD'] == 1].groupby('MthCalDt')['wt'].quantile(0.20).reset_index()
    nyse_thresholds.rename(columns={'wt': 'nyse_20th_percentile'}, inplace=True)

    # Merge the NYSE threshold back into the crsp3 dataframe to get the NYSE 20th percentile market equity for each row.
    crsp3 = pd.merge(crsp3, nyse_thresholds, on='MthCalDt', how='left')

    # Initialize dictionaries to store the results for each set of predictors.
    all_results = {'all_but_microcaps': {}, 'microcaps': {}}

    # Iterate over each list of predictors.
    for i, predictors in enumerate(list_of_predictor_lists):

        # Merge the essential monthly CRSP data with the essential annual CCM data and the current list of predictors.
        ccm3 = pd.merge(crsp3[['MthCalDt', 'PERMNO', 'retadj', 'me', 'wt', 'ffyear', '$r_{1,0}$', '$r_{12,2}$', 'nyse_20th_percentile']],
                        ccm_jun[['PERMNO', 'ffyear', 'Book Equity to Market Equity',  'AT', 'dec_me'] + predictors],
                        how='left', on=['PERMNO', 'ffyear'])

        # Only keep the stocks with a positive book equity to market equity ratio.
        ccm3 = ccm3[ccm3['Book Equity to Market Equity'] > 0]
        ccm3 = ccm3[ccm3['dec_me'] > 0]
        ccm3 = ccm3[ccm3['AT'] > 0]

        # Take the logarithm of market equity and the book equity to market equity ratio.
        ccm3['log(ME)'] = np.log(ccm3['dec_me'])
        ccm3['log(BE/ME)'] = np.log(ccm3['Book Equity to Market Equity'])

        # Define the control variables.
        controls = ['log(ME)', 'log(BE/ME)', '$r_{1,0}$', '$r_{12,2}$']
        
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

        # Perform Fama-MacBeth regression for all but microcaps and microcaps separately
        for category in ['all_but_microcaps', 'microcaps']:

            # Filter the data based on the category
            if category == 'all_but_microcaps':
                filtered_ccm3 = ccm3[ccm3['wt'] >= ccm3['nyse_20th_percentile']]
            else:
                filtered_ccm3 = ccm3[ccm3['wt'] < ccm3['nyse_20th_percentile']]

            # Create a list to store the results of the Fama-MacBeth regressions.
            results_list = []

            # Iterate through the groups by date.
            for _, group in filtered_ccm3.groupby('MthCalDt'):

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
            all_results[category][f"({i+1})"] = pd.DataFrame({'Coefficient': fm_mean, 'T-Statistic': t_stats})

    # Collect all unique predictors from all models
    unique_predictors = set()
    for predictors in list_of_predictor_lists:
        unique_predictors.update(predictors)

    # Now we will order them correctly
    ordered_vars = [var for var in vars_order if var in unique_predictors] + controls

    # Create LaTeX table content
    num_vars = len(list_of_predictor_lists) + 1
    latex_content = [
        "\\begin{table*}[ht!]",
        "\\textbf{" + title + "} \\\\",
        "\\raggedright",
        latex_escape(short_description) + "\\\\",
        "\\hspace*{1em} " + latex_escape(long_description) + "\\\\",
        "\\centering",
        "\\scalebox{1}{\\begin{adjustbox}{max width=\\textwidth}",
        "\\begin{tabular}{@{}l*{" + str(num_vars - 1) + "}{c}@{}}",
        "\\toprule",
        "\\multicolumn{" + str(num_vars) + "}{l}{\\textit{" + latex_escape("Panel A: All but Microcaps") + "}} \\\\",
        "\\midrule",
        "\\textbf{Independent variable} & " + " & ".join([f"({i})" for i in range(1, num_vars)]) + " \\\\"
        "\\midrule"
    ]

    # Construct the table rows for all but microcaps
    for var in ordered_vars:
        coeff_row = f"{var} "
        t_stat_row = " "  # Empty string for alignment of t-stats row
        for i in range(1, len(list_of_predictor_lists) + 1):
            model_key = f"({i})"
            if var in all_results['all_but_microcaps'][model_key].index:
                coeff = all_results['all_but_microcaps'][model_key].loc[var, 'Coefficient']
                t_stat = all_results['all_but_microcaps'][model_key].loc[var, 'T-Statistic']
                coeff_row += f"& {coeff:.2f} "  # Format for 2 decimal places
                t_stat_row += f"& [{t_stat:.2f}] "  # Format for 2 decimal places
            else:
                # Leave the space blank for models without the predictor
                coeff_row += "& "
                t_stat_row += "& "
        coeff_row = coeff_row.strip()  # Remove trailing spaces
        t_stat_row = t_stat_row.strip()  # Remove trailing spaces
        latex_content.append(coeff_row + " \\\\")
        latex_content.append(t_stat_row + " \\\\")

    # Add the panel for microcaps
    latex_content.extend([
        "\\midrule",
        "\\multicolumn{" + str(num_vars) + "}{l}{\\textit{" + latex_escape("Panel B: Microcaps") + "}} \\\\",
        "\\midrule",
        "\\textbf{Independent variable} & " + " & ".join([f"({i})" for i in range(1, num_vars)]) + " \\\\"
        "\\midrule"
    ])

    # Construct the table rows for microcaps
    for var in ordered_vars:
        coeff_row = f"{var} "
        t_stat_row = " "  # Empty string for alignment of t-stats row
        for i in range(1, len(list_of_predictor_lists) + 1):
            model_key = f"({i})"
            if var in all_results['microcaps'][model_key].index:
                coeff = all_results['microcaps'][model_key].loc[var, 'Coefficient']
                t_stat = all_results['microcaps'][model_key].loc[var, 'T-Statistic']
                coeff_row += f"& {coeff:.2f} "  # Format for 2 decimal places
                t_stat_row += f"& [{t_stat:.2f}] "  # Format for 2 decimal places
            else:
                # Leave the space blank for models without the predictor
                coeff_row += "& "
                t_stat_row += "& "
        coeff_row = coeff_row.strip()  # Remove trailing spaces
        t_stat_row = t_stat_row.strip()  # Remove trailing spaces
        latex_content.append(coeff_row + " \\\\")
        latex_content.append(t_stat_row + " \\\\")

    # Closing the table environment
    latex_content.extend([
        "\\bottomrule",
        "\\end{tabular}",
        "\\end{adjustbox}}",  # Note the extra closing brace for \scalebox
        "\\end{table*}"
    ])

    # Join the content and write to a .tex file
    tex_file_path = Path(output_file)
    with open(tex_file_path, 'w') as tex_file:
        tex_file.write('\n'.join(latex_content))

    return str(tex_file_path)


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


def output_summary_statistics(factors: List[str], title, short_description, long_description, output_file: str):
    """
    Generate summary statistics and correlations for factors and export to a LaTeX file.

    Args:
        factors (list): Factors for analysis.
        title (str): Title of the LaTeX table.
        short_description (str): Short description for the LaTeX table.
        long_description (str): Long description for the LaTeX table.
        output_file (str): Output file path for the LaTeX table.

    Returns:
        str: Path of the generated LaTeX file.
    """

    # Read in the csvs.
    fama_french_esque_factors = pd.read_csv('processed_fama_french_esque_factors.csv', parse_dates=['date'])
    replicated_factors = pd.read_csv('raw_factors.csv', parse_dates=['date'])

    for factor in ['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA', 'UMD', 'IA', 'ROE', 'EG', 'MGMT', 'PERF', 'PEAD', 'FIN']:
        replicated_factors[factor] /= 100

    # Convert YYYYMM to datetime format.
    replicated_factors['date'] = pd.to_datetime(replicated_factors['date'], format='%Y%m') + pd.offsets.MonthEnd(1)

    # Merge the replicated factors with the list of signals passed in.
    merged_data = pd.merge(replicated_factors, fama_french_esque_factors, how='inner', on='date')

    # Initialize a DataFrame to store the summary statistics.
    summary_df = pd.DataFrame()

    # Loop through each factor to calculate the statistics.
    for factor in factors:
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

    # Calculate the Pearson and Spearman correlation matrices
    pearson_matrix = merged_data[factors].corr(method='pearson')
    spearman_matrix = merged_data[factors].corr(method='spearman')

    # Create LaTeX table content
    num_vars = max(6, len(factors))
    latex_content = [
        "\\begin{table*}[ht!]",
        "\\textbf{" + title + "} \\\\",
        "\\raggedright",  # Left-align the next line
        latex_escape(short_description) + "\\\\",
        "\\hspace*{1em} " + latex_escape(long_description) + "\\\\",
        "\\centering",  # Center the table content
        "\\scalebox{1}{\\begin{adjustbox}{max width=\\textwidth}",
        "\\begin{tabular}{@{}l*{" + str(num_vars) + "}{c}@{}}",
        "\\toprule",
        "\\multicolumn{6}{l}{\\textit{" + latex_escape("Panel A: Summary Statistics of Factors") + "}} \\\\",
        "\\midrule",
        "Factor & Return (\\%) & Volatility (\\%) & Sharpe & Skew & Kurtosis \\\\",
        "\\midrule"
    ]

    # Adding rows from the dataframe to LaTeX table
    for _, row in summary_df.iterrows():
        row_list = [latex_escape(str(val)) for val in row]
        row_str = " & ".join(row_list)
        latex_content.append(row_str + " \\\\")

    # Add Pearson Correlations Panel to LaTeX content
    latex_content.extend([
        "\\midrule",
        "\\multicolumn{" + str(num_vars) + "}{l}{\\textit{" + latex_escape("Panel B: Pearson Correlations") + "}} \\\\",
        "\\midrule",
    ])

    # Iterate over rows to create the triangular matrix for Pearson
    for row_idx, row in enumerate(pearson_matrix.itertuples(index=False, name=None)):
        row_values = [f"{v:.3f}" if i < row_idx else "1.000" if i == row_idx else "" for i, v in enumerate(row)]
        latex_content.append(latex_escape(str(pearson_matrix.index[row_idx])) + " & " + " & ".join(row_values) + " \\\\")

    # Add Spearman Correlations Panel to LaTeX content
    latex_content.extend([
        "\\midrule",
        "\\multicolumn{" + str(num_vars) + "}{l}{\\textit{" + latex_escape("Panel C: Spearman Correlations") + "}} \\\\",
        "\\midrule",
    ])

    # Iterate over rows to create the triangular matrix for Spearman
    for row_idx, row in enumerate(spearman_matrix.itertuples(index=False, name=None)):
        row_values = [f"{v:.3f}" if i < row_idx else "1.000" if i == row_idx else "" for i, v in enumerate(row)]
        latex_content.append(latex_escape(str(spearman_matrix.index[row_idx])) + " & " + " & ".join(row_values) + " \\\\")

    # Closing the table environment
    latex_content.extend([
        "\\bottomrule",
        "\\end{tabular}",
        "\\end{adjustbox}}",  # Note the extra closing brace for \scalebox
        "\\end{table*}"
    ])

    # Join the content and write to a .tex file
    tex_file_path = Path(output_file)
    with open(tex_file_path, 'w') as tex_file:
        tex_file.write("\n".join(latex_content))

    return str(tex_file_path)


def spanning_regressions(independent_vars, control_vars_lists, constant_control_vars, title, short_description, long_description, output_file: str):
    """
    This function performs regressions of each independent variable against the control variables and exports the results to a LaTeX file.

    Args:
        independent_vars (list): Independent variables for analysis.
        control_vars_lists (list): Lists of control variables for regression.
        constant_control_vars (list): Control variables to be included in every regression.
        title (str): Title of the LaTeX table.
        short_description (str): Short description for the LaTeX table.
        long_description (str): Long description for the LaTeX table.
        output_file (str): Output file path for the LaTeX table.

    Returns:
        str: Path of the generated LaTeX file.
    """

    # Read in the csvs.
    fama_french_esque_factors = pd.read_csv('processed_fama_french_esque_factors.csv', parse_dates=['date'])
    raw_factors = pd.read_csv('raw_factors.csv', parse_dates=['date'], usecols=['date', 'Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA', 'UMD'])

    # Convert YYYYMM to datetime format.
    raw_factors['date'] = pd.to_datetime(raw_factors['date'], format='%Y%m') + pd.offsets.MonthEnd(1)
    
    # Divide the Fama-French factors by 100 to match the raw factors.
    for factor in ['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA', 'UMD']:
        raw_factors[factor] /= 100

    # Merge the replicated factors with the list of signals passed in.
    merged_data = pd.merge(raw_factors, fama_french_esque_factors, how='inner', on='date')

    # Ensure there are no missing values in the columns of interest.
    merged_data.dropna(inplace=True)

    # Initialize LaTeX table content
    if len(independent_vars) == 1 and len(control_vars_lists) > 1:
        dependent_var_row = "& " + " & ".join([f"({i+1})" for i in range(len(control_vars_lists))]) + " \\\\"
    else:
        dependent_var_row = "& " + " & ".join(independent_vars * len(control_vars_lists)) + " \\\\"

    latex_content = [
        "\\begin{table*}[ht!]",
        "\\textbf{" + title + "} \\\\",
        "\\raggedright",  # Left-align the next line
        latex_escape(short_description) + "\\\\",
        "\\hspace*{1em} " + latex_escape(long_description) + "\\\\",
        "\\centering",  # Center the table content
        "\\begin{adjustbox}{max width=\\textwidth}",
        "\\begin{tabular}{@{}l*{" + str(len(independent_vars) * len(control_vars_lists)) + "}{c}@{}}",
        "\\toprule",
        "\\multicolumn{" + str(len(independent_vars) * len(control_vars_lists)) + "}{l}{\\textit{" + latex_escape("Panel A") + "}} \\\\",
        "\\midrule",
        dependent_var_row,
        "\\midrule"
    ]

    # Add alpha row
    alpha_row = "Alpha "
    alpha_t_stat_row = " "

    # Initialize control variable rows and t-stat rows dictionaries
    control_var_rows = {}
    control_var_t_stat_rows = {}
    all_control_vars = [var for sublist in control_vars_lists for var in sublist] + constant_control_vars
    for control_var in all_control_vars:
        control_var_rows[control_var] = f"{control_var} "
        control_var_t_stat_rows[control_var] = " "

    # Add R-squared row
    r_squared_row = "$R^2$ "

    # Iterate over each list of control variables.
    for i, control_vars_list in enumerate(control_vars_lists):
        current_control_vars = control_vars_list + constant_control_vars

        # Iterate through the independent variables.
        for j, independent_var in enumerate(independent_vars):
            # Set X and y based on the control variables and independent variable.
            X = merged_data[current_control_vars]
            y = merged_data[independent_var]

            # Add a constant to the independent variables for intercept (alpha).
            X = sm.add_constant(X)

            # Fit the OLS model.
            model = sm.OLS(y, X).fit()

            # Extract alpha (intercept) and t-statistic for alpha.
            alpha = (1 + model.params['const']) ** 12 - 1
            alpha_t_stat = model.tvalues['const']

            # Add alpha and its t-statistic to the respective rows.
            alpha_row += f"& {alpha*100:.2f}\\% "
            alpha_t_stat_row += f"& [{alpha_t_stat:.2f}] "

            # Iterate through all control variables (current list and constant) to extract the coefficients and t-stats.
            for control_var in all_control_vars:
                if control_var in model.params:
                    # Extract the coefficient and t-statistic for the control variable.
                    coef = model.params[control_var]
                    t_stat = model.tvalues[control_var]
                    control_var_rows[control_var] += f"& {coef:.2f} "
                    control_var_t_stat_rows[control_var] += f"& [{t_stat:.2f}] "
                else:
                    # Add "&" to indicate missing control variable
                    control_var_rows[control_var] += "& "
                    control_var_t_stat_rows[control_var] += "& "

            # Extract R-squared.
            r_squared = model.rsquared

            # Add R-squared to the R-squared row.
            r_squared_row += f"& {r_squared:.4f} "

        # Add "&" for the remaining columns in the current control variable list
        for k in range(j + 1, len(independent_vars)):
            for control_var in all_control_vars:
                control_var_rows[control_var] += "& "
                control_var_t_stat_rows[control_var] += "& "

    # Remove trailing spaces from all rows
    alpha_row = alpha_row.strip()
    alpha_t_stat_row = alpha_t_stat_row.strip()
    for control_var in control_var_rows:
        control_var_rows[control_var] = control_var_rows[control_var].strip()
        control_var_t_stat_rows[control_var] = control_var_t_stat_rows[control_var].strip()
    r_squared_row = r_squared_row.strip()

    # Add the rows to the LaTeX table content.
    latex_content.append(alpha_row + " \\\\")
    latex_content.append(alpha_t_stat_row + " \\\\")
    for control_var in all_control_vars:
        latex_content.append(control_var_rows[control_var] + " \\\\")
        latex_content.append(control_var_t_stat_rows[control_var] + " \\\\")
    latex_content.append("\\midrule")
    latex_content.append(r_squared_row + " \\\\")

    dummy = independent_vars
    independent_vars = []
    for factor in control_vars_lists:
        independent_vars.append(factor[0])
    control_vars_lists = [dummy]

    # Initialize LaTeX table content
    if len(independent_vars) == 1 and len(control_vars_lists) > 1:
        dependent_var_row = "& " + " & ".join([f"({i+1})" for i in range(len(control_vars_lists))]) + " \\\\"
    else:
        dependent_var_row = "& " + " & ".join(independent_vars * len(control_vars_lists)) + " \\\\"

    latex_content.extend([
        "\\midrule",
        "\\multicolumn{" + str(len(independent_vars) * len(control_vars_lists)) + "}{l}{\\textit{" + latex_escape("Panel B") + "}} \\\\",
        "\\midrule",
        dependent_var_row,
        "\\midrule"
    ])

    # Add alpha row
    alpha_row = "Alpha "
    alpha_t_stat_row = " "

    # Initialize control variable rows and t-stat rows dictionaries
    control_var_rows = {}
    control_var_t_stat_rows = {}
    all_control_vars = [var for sublist in control_vars_lists for var in sublist] + constant_control_vars
    for control_var in all_control_vars:
        control_var_rows[control_var] = f"{control_var} "
        control_var_t_stat_rows[control_var] = " "

    # Add R-squared row
    r_squared_row = "$R^2$ "

    # Iterate over each list of control variables.
    for i, control_vars_list in enumerate(control_vars_lists):
        current_control_vars = control_vars_list + constant_control_vars

        # Iterate through the independent variables.
        for j, independent_var in enumerate(independent_vars):
            # Set X and y based on the control variables and independent variable.
            X = merged_data[current_control_vars]
            y = merged_data[independent_var]

            # Add a constant to the independent variables for intercept (alpha).
            X = sm.add_constant(X)

            # Fit the OLS model.
            model = sm.OLS(y, X).fit()

            # Extract alpha (intercept) and t-statistic for alpha.
            alpha = (1 + model.params['const']) ** 12 - 1
            alpha_t_stat = model.tvalues['const']

            # Add alpha and its t-statistic to the respective rows.
            alpha_row += f"& {alpha*100:.2f}\\% "
            alpha_t_stat_row += f"& [{alpha_t_stat:.2f}] "

            # Iterate through all control variables (current list and constant) to extract the coefficients and t-stats.
            for control_var in all_control_vars:
                if control_var in model.params:
                    # Extract the coefficient and t-statistic for the control variable.
                    coef = model.params[control_var]
                    t_stat = model.tvalues[control_var]
                    control_var_rows[control_var] += f"& {coef:.2f} "
                    control_var_t_stat_rows[control_var] += f"& [{t_stat:.2f}] "
                else:
                    # Add "&" to indicate missing control variable
                    control_var_rows[control_var] += "& "
                    control_var_t_stat_rows[control_var] += "& "

            # Extract R-squared.
            r_squared = model.rsquared

            # Add R-squared to the R-squared row.
            r_squared_row += f"& {r_squared:.4f} "

        # Add "&" for the remaining columns in the current control variable list
        for k in range(j + 1, len(independent_vars)):
            for control_var in all_control_vars:
                control_var_rows[control_var] += "& "
                control_var_t_stat_rows[control_var] += "& "

    # Remove trailing spaces from all rows
    alpha_row = alpha_row.strip()
    alpha_t_stat_row = alpha_t_stat_row.strip()
    for control_var in control_var_rows:
        control_var_rows[control_var] = control_var_rows[control_var].strip()
        control_var_t_stat_rows[control_var] = control_var_t_stat_rows[control_var].strip()
    r_squared_row = r_squared_row.strip()

    # Add the rows to the LaTeX table content.
    latex_content.append(alpha_row + " \\\\")
    latex_content.append(alpha_t_stat_row + " \\\\")
    for control_var in all_control_vars:
        latex_content.append(control_var_rows[control_var] + " \\\\")
        latex_content.append(control_var_t_stat_rows[control_var] + " \\\\")
    latex_content.append("\\midrule")
    latex_content.append(r_squared_row + " \\\\")

    # Finish LaTeX table structure.
    latex_content.extend([
        "\\bottomrule",
        "\\end{tabular}",
        "\\end{adjustbox}",
        "\\end{table*}"
    ])

    # Join the content and write to a .tex file
    tex_file_path = Path(output_file)
    with open(tex_file_path, 'w') as tex_file:
        tex_file.write("\n".join(latex_content))

    return str(tex_file_path)


def regress_on_factor_models(predictor: str, title, short_description, long_description, output_file: str):
    # Read in the csv files.
    fama_french_esque_factors = pd.read_csv('processed_fama_french_esque_factors.csv', parse_dates=['date'])
    factors = pd.read_csv('raw_factors.csv', parse_dates=['date'])

    # Convert YYYYMM to datetime format.
    factors['date'] = pd.to_datetime(factors['date'], format='%Y%m') + pd.offsets.MonthEnd(1)

    for factor in ['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA', 'UMD', 'IA', 'ROE', 'EG', 'MGMT', 'PERF', 'PEAD', 'FIN']:
        factors[factor] /= 100

    # Merge the data frames based on the 'date' column
    merged_data = pd.merge(fama_french_esque_factors, factors, on='date')

    # Only keep the data from 1963-07-31 onwards
    merged_data = merged_data[merged_data['date'] >= '1963-07-31']

    # Define the factor models
    factor_models = {
        'FF6': ['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA', 'UMD'],
        'Q5': ['Mkt-RF', 'SMB', 'IA', 'ROE', 'EG'],
        'DHS3': ['Mkt-RF', 'MGMT', 'PERF'],
        'SY4': ['Mkt-RF', 'SMB', 'PEAD', 'FIN']
    }

    # Define the order of factors
    factor_order = ['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA', 'UMD', 'IA', 'ROE', 'EG', 'MGMT', 'PERF', 'PEAD', 'FIN']

    # Initialize LaTeX table content
    latex_content = [
        "\\begin{table*}[ht!]",
        "\\textbf{" + title + "} \\\\",
        "\\raggedright",  # Left-align the next line
        latex_escape(short_description) + "\\\\",
        "\\hspace*{1em} " + latex_escape(long_description) + "\\\\",
        "\\centering",  # Center the table content
        "\\begin{adjustbox}{max width=\\textwidth}",
        "\\begin{tabular}{@{}l*{" + str(len(factor_models)) + "}{c}@{}}",
        "\\toprule",
        "& " + " & ".join([f"({i+1})" for i in range(len(factor_models))]) + " \\\\",
        "\\midrule"
    ]

    # Add alpha row
    alpha_row = "Alpha "
    alpha_t_stat_row = " "

    # Initialize factor rows and t-stat rows
    factor_rows = [f"{factor} " for factor in factor_order]
    factor_t_stat_rows = [" " for _ in factor_order]

    # Add R-squared row
    r_squared_row = "$R^2$ "

    # Iterate over each factor model
    for model_name, model_factors in factor_models.items():
        # Only keep the valid data for what is needed, ensure no missing values
        model_data = merged_data[model_factors + [predictor]].dropna()

        # Set X and y based on the factor model and predictor
        X = model_data[model_factors]
        y = model_data[predictor]

        # Add a constant to the independent variables for intercept (alpha)
        X = sm.add_constant(X)

        # Fit the OLS model
        model = sm.OLS(y, X).fit()

        # Extract alpha (intercept) and t-statistic for alpha.
        alpha = (1 + model.params['const']) ** 12 - 1
        alpha_t_stat = model.tvalues['const']

        # Add alpha and its t-statistic to the respective rows.
        alpha_row += f"& {alpha*100:.2f}\\% "
        alpha_t_stat_row += f"& [{alpha_t_stat:.2f}] "

        # Iterate through the factor order to extract the coefficients and t-stats
        for i, factor in enumerate(factor_order):
            if factor in model_factors:
                # Extract the coefficient and t-statistic for the factor
                coef = model.params[factor]
                t_stat = model.tvalues[factor]
                factor_rows[i] += f"& {coef:.4f} "
                factor_t_stat_rows[i] += f"& [{t_stat:.2f}] "
            else:
                # Add empty cell for missing factor
                factor_rows[i] += "& "
                factor_t_stat_rows[i] += "& "

        # Extract R-squared
        r_squared = model.rsquared

        # Add R-squared to the R-squared row
        r_squared_row += f"& {r_squared:.4f} "

    # Remove trailing spaces from all rows
    alpha_row = alpha_row.strip()
    alpha_t_stat_row = alpha_t_stat_row.strip()
    factor_rows = [row.strip() for row in factor_rows]
    factor_t_stat_rows = [row.strip() for row in factor_t_stat_rows]
    r_squared_row = r_squared_row.strip()

    # Add the rows to the LaTeX table content
    latex_content.append(alpha_row + " \\\\")
    latex_content.append(alpha_t_stat_row + " \\\\")
    for factor_row, factor_t_stat_row in zip(factor_rows, factor_t_stat_rows):
        latex_content.append(factor_row + " \\\\")
        latex_content.append(factor_t_stat_row + " \\\\")
    latex_content.append("\\midrule")
    latex_content.append(r_squared_row + " \\\\")

    # Finish LaTeX table structure
    latex_content.extend([
        "\\bottomrule",
        "\\end{tabular}",
        "\\end{adjustbox}",
        "\\end{table*}"
    ])

    # Join the content and write to a .tex file
    tex_file_path = Path(output_file)
    with open(tex_file_path, 'w') as tex_file:
        tex_file.write("\n".join(latex_content))

    return str(tex_file_path)


def perform_decile_sorts(predictor: str, title, short_description, long_description, output_file: str):
    # Read in the csv files.
    ccm_jun = pd.read_csv('processed_crsp_jun2.csv', parse_dates=['jdate'])
    crsp3 = pd.read_csv('processed_crsp_data.csv', low_memory=False)
    ff = pd.read_csv('raw_factors.csv', parse_dates=['date'])

    # Convert YYYYMM to datetime format.
    ff['date'] = pd.to_datetime(ff['date'], format='%Y%m') + pd.offsets.MonthEnd(1)

    for factor in ['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA', 'UMD', 'IA', 'ROE', 'EG', 'MGMT', 'PERF', 'PEAD', 'FIN']:
        ff[factor] /= 100

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

    # Initialize LaTeX table content
    latex_content = [
        "\\begin{table*}[ht!]",
        "\\textbf{" + title + "} \\\\",
        "\\raggedright",  # Left-align the next line
        latex_escape(short_description) + "\\\\",
        "\\hspace*{1em} " + latex_escape(long_description) + "\\\\",
        "\\centering",  # Center the table content
        "\\begin{adjustbox}{max width=\\textwidth}",
        "\\begin{tabular}{@{}c*{5}{c}@{}}",
        "\\toprule",
        "Portfolio & Excess Return & Volatility & Sharpe Ratio & Alpha \\\\",
        "\\midrule"
    ]

    # Iterate over rows to populate the table
    for index, row in stats_df.iterrows():

        # Format columns
        row_str = f"{index} & {row['Excess Return']} & {row['Volatility']} & {row['Sharpe Ratio']} & {row['Alpha']} [{row['tstat']}] \\\\"
        latex_content.append(row_str)

    # Finish LaTeX table structure
    latex_content.extend([
        "\\bottomrule",
        "\\end{tabular}",
        "\\end{adjustbox}",
        "\\end{table*}"
    ])

    # Join the content and write to a .tex file
    tex_file_path = Path(output_file)
    with open(tex_file_path, 'w') as tex_file:
        tex_file.write("\n".join(latex_content))

    # Save the first 12 columns of the decile portfolios to a csv
    decile_portfolios.iloc[:, :12].to_csv('processed_decile_portfolios.csv', index=False)

    return str(tex_file_path)


def display_cumulative_returns(factors: List[str], output_file: str):
    """
    This function graphs the cumulative returns of the given  portfolios.
    """

    # Read in the csvs.
    fama_french_esque_factors = pd.read_csv('processed_fama_french_esque_factors.csv', parse_dates=['date'])
    ff = pd.read_csv('raw_factors.csv', parse_dates=['date'])
    decile_portfolios = pd.read_csv('processed_decile_portfolios.csv', parse_dates=['date'])

    # Convert YYYYMM to datetime format.
    ff['date'] = pd.to_datetime(ff['date'], format='%Y%m') + pd.offsets.MonthEnd(1)

    for factor in ['Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA', 'UMD', 'IA', 'ROE', 'EG', 'MGMT', 'PERF', 'PEAD', 'FIN']:
        ff[factor] /= 100

    # Merge the replicated factors with the list of signals passed in and the decile portfolios.
    merged_data = pd.merge(ff, fama_french_esque_factors, how='inner', on='date')
    merged_data = pd.merge(merged_data, decile_portfolios, how='inner', on='date')

    # Only keep the date and the factors of interest.
    merged_data = merged_data[['date'] + factors]

    # Ensure there are no missing values for a given date.
    merged_data.dropna(inplace=True)

    # Set the data frame index to 'date'.
    merged_data = merged_data.set_index('date')

    # Calculate the cumulative returns, adjusting the starting point to 100.
    cum_returns = 100 * (1 + merged_data).cumprod()

    # Plot the cumulative returns.
    cum_returns.plot(figsize=(12, 8), logy=True)
    plt.title('Cumulative Returns of Portfolios')
    plt.xlabel('Date')
    plt.ylabel('Cumulative Return')
    plt.yscale('log')
    plt.legend(title='Portfolios')

    # Save the image.
    plt.savefig(output_file)


def produce_results():
    """
    This script calls the function to generate the variables, conduct the Fama-MacBeth regressions,
    create the Fama-French-esque factors, and perform decile sorts.
    """

    # Generate the variables.
    start_time = time.time()
    generate_variables()
    end_time = time.time()
    print("Generated Variables.")
    print("Time Elapsed: ", end_time - start_time)

    # Output Table 1.
    start_time = time.time()
    distribution_variables = ['Cash-Based Operating Profits to Market Equity', 'Capital Expenditures to Market Equity', 'Owner\'s Earnings to Market Equity', 'Cash-Based Operating Profits to Total Assets', 'Capital Expenditures to Total Assets', 'Owner\'s Earnings to Total Assets', 'Cash-Based Operating Profits to Book Equity', 'Capital Expenditures to Book Equity', 'Owner\'s Earnings to Book Equity']
    correlation_variables = ['Cash-Based Operating Profits to Market Equity',  'Capital Expenditures to Market Equity', 'Owner\'s Earnings to Market Equity']
    title = "Table 1"
    ouput_file = "table1.tex"
    short_description = "Descriptive statistics for the major variables employed in this paper."
    long_description = "Panel A presents the mean, standard deviation, 1st, 25th, 50th, 75th, and 99th percentiles for the major variables employed in this paper – Cash-Based Operating Profits, Capital Expenditures, and Owner's Earnings – scaled by market equity, total assets, and book equity.  Four controls – the natural logarithm of market equity, the natural logarithm of the book equity to market equity, the past one month return, and the sum of monthly returns for the past year excluding the last month – are also included.  Panel B presents Pearson correlations between the main variables deflated by market equity, and Panel C presents Spearman correlations for the same variables."
    generate_variable_descriptive_statistics(distribution_variables, correlation_variables, title, short_description, long_description, ouput_file)
    end_time = time.time()
    print("Generated descriptive statistics.")
    print("Time Elapsed: ", end_time - start_time)

    # Output Table 2.
    start_time = time.time()
    regression = [['Cash-Based Operating Profits to Market Equity'], ['Capital Expenditures to Market Equity'], ['Cash-Based Operating Profits to Market Equity', 'Capital Expenditures to Market Equity'], ['Owner\'s Earnings to Market Equity'], ['Cash-Based Operating Profits to Market Equity', 'Owner\'s Earnings to Market Equity']]
    variables_order = ['Cash-Based Operating Profits to Market Equity', 'Capital Expenditures to Market Equity', 'Owner\'s Earnings to Market Equity']
    title = "Table 2"
    short_description = "Cash-based operating profits, capital expenditures, and owner's earnings deflated by market equity in Fama-MacBeth regressions."
    long_description = "This table presents the average Fama and MacBeth (1973) cross sectional regression slopes (multiplied by 100) and their respective t-statistics from regressions that predict monthly returns.  The regressions spanned from July 1963 to December 2022. Panel A presents the results for All-but-microcaps, while Panel B presents the data for Microcaps – defined as having a market equity above the 20th percentile of all NYSE securities in the previous month.  The construction of cash-based operating profits and owner's earnings is presented in Appendix A.  All variables are winsorized at the 1st and 99th percentile.  All columns require non-missing data for the variables of interest, book equity, market equity, and total assets."
    output_file = "table2.tex"
    fama_macbeth_regression(regression, variables_order, title, short_description, long_description, output_file)
    end_time = time.time()
    print("Conducted Fama-MacBeth Regressions for Market Equity.")
    print("Time Elapsed: ", end_time - start_time)

    # Create the Fama-French-esque factors.
    start_time = time.time()
    create_fama_french_esque_factors(['Sales to Market Equity', 'Net Income to Market Equity', 'Operating Cash Flow to Market Equity', 'Free Cash Flow to Market Equity', 'Dividends to Market Equity', 'Net Payouts to Market Equity', 'Retained Earnings to Market Equity', 'Cash-Based Operating Profits to Market Equity', 'Owner\'s Earnings to Market Equity', 'Gross Profits to Total Assets', 'Operating Profits to Total Assets', 'Cash-Based Operating Profits to Total Assets', 'Owner\'s Earnings to Total Assets', 'Gross Profits to Book Equity', 'Operating Profits to Book Equity', 'Cash-Based Operating Profits to Book Equity', 'Owner\'s Earnings to Book Equity', 'Cash-Based Operating Profits Composite', 'Owner\'s Earnings Composite'])
    end_time = time.time()
    print("Created Fama-French-esque factors.")
    print("Time Elapsed: ", end_time - start_time)

    # Output Table 3.
    start_time = time.time()
    title = "Table 3"
    short_description = "Descriptive statistics for value factors."
    long_description = "Panel A reports the annual return, standard deviation, and Sharpe ratio for the given factors.  Factor construction is consistent with Fama and French (1993) as outlined in the Data section, and the variable definitions are provided in Appendix A.  Panel B presents the Pearson correlations between the factors.  Panel C presents the Spearman correlations between the factors, while Panel C presents the Spearman correlations."
    output_file = "table3.tex"
    output_summary_statistics(['Sales to Market Equity', 'Net Income to Market Equity', 'Operating Cash Flow to Market Equity', 'Free Cash Flow to Market Equity', 'Dividends to Market Equity', 'Net Payouts to Market Equity', 'Retained Earnings to Market Equity', 'Cash-Based Operating Profits to Market Equity', 'Owner\'s Earnings to Market Equity'], title, short_description, long_description, output_file)
    end_time = time.time()
    print("Outputed Summary Statistics.")
    print("Time Elapsed: ", end_time - start_time)

    # Output Table 4.
    start_time = time.time()
    factors = ['Owner\'s Earnings to Market Equity']
    control_factors = [['Sales to Market Equity'], ['Net Income to Market Equity'], ['Operating Cash Flow to Market Equity'], ['Free Cash Flow to Market Equity'], ['Dividends to Market Equity'], ['Net Payouts to Market Equity'], ['Retained Earnings to Market Equity'], ['Cash-Based Operating Profits to Market Equity']]
    constant_controls = ['Mkt-RF', 'SMB']
    title = "Table 4"
    short_description = "Spanning regressions for value factors."
    long_description = "This table presents a battery of spanning regressions on factor returns from July 1963 to December 2022..  Factor construction is consistent with Fama and French (1993) as outlined in the Data section, and the variable definitions are provided in Appendix A.  Panel A regresses the Owner's Earnings to Market Equity factor on the other value factors, while Panel B regresses the other value factors on the Owner's Earnings to Market Equity factor.  The annualized alpha, monthly coefficients, t-statistics, and R-squared values are presented in both panels.  Sales to Market Equity is shortened to S/P, Net Income to Market Equity to NI/ME, Operating Cash Flow to Market Equity to OCF/ME, Free Cash Flow to Market Equity to FCF/ME, Dividends to Market Equity to D/ME, Net Payouts to Market Equity to NP/ME, Retained Earnings to Market Equity to RE/ME, Cash-Based Operating Profits to Market Equity to CbOP/ME, and Owner's Earnings to Market Equity to OE/ME.  The excess return of the market and the Fama-French SMB factor are included as controls in all regressions."
    output_file = "table4.tex"
    spanning_regressions(factors, control_factors, constant_controls, title, short_description, long_description, output_file)
    end_time = time.time()
    print("Performed spanning regressions.")
    print("Time Elapsed: ", end_time - start_time)

    # Output Table 5.
    start_time = time.time()
    regression = [['Cash-Based Operating Profits to Total Assets'], ['Capital Expenditures to Total Assets'], ['Cash-Based Operating Profits to Total Assets', 'Capital Expenditures to Total Assets'], ['Owner\'s Earnings to Total Assets'], ['Cash-Based Operating Profits to Total Assets', 'Owner\'s Earnings to Total Assets']]
    variables_order = ['Cash-Based Operating Profits to Total Assets', 'Capital Expenditures to Total Assets', 'Owner\'s Earnings to Total Assets']
    title = "Table 5"
    short_description = "Cash-based operating profits, capital expenditures, and owner's earnings deflated by total assets in Fama-MacBeth regressions."
    long_description = "This table presents the average Fama and MacBeth (1973) cross sectional regression slopes (multiplied by 100) and their respective t-statistics from regressions that predict monthly returns.  The regressions spanned from July 1963 to December 2022. Panel A presents the results for All-but-microcaps, while Panel B presents the data for Microcaps – defined as having a market equity above the 20th percentile of all NYSE securities in the previous month.  The construction of cash-based operating profits and owner's earnings is presented in Appendix A.  All variables are winsorized at the 1st and 99th percentile.  All columns require non-missing data for the variables of interest, book equity, market equity, and total assets."
    output_file = "table5.tex"
    fama_macbeth_regression(regression, variables_order, title, short_description, long_description, output_file)
    end_time = time.time()
    print("Conducted Fama-MacBeth Regressions for Total Assets.")
    print("Time Elapsed: ", end_time - start_time)

    # Output Table 6.
    start_time = time.time()
    title = "Table 6"
    short_description = "Descriptive statistics for profitability factors."
    long_description = "Panel A reports the annual return, standard deviation, and Sharpe ratio for the given factors.  Factor construction is consistent with Fama and French (1993) as outlined in the Data section, and the variable definitions are provided in Appendix A.  Panel B presents the Pearson correlations between the factors.  Panel C presents the Spearman correlations between the factors, while Panel C presents the Spearman correlations."
    output_file = "table6.tex"
    output_summary_statistics(['Gross Profits to Total Assets', 'Operating Profits to Total Assets', 'Cash-Based Operating Profits to Total Assets', 'Owner\'s Earnings to Total Assets'], title, short_description, long_description, output_file)
    end_time = time.time()
    print("Outputed Summary Statistics.")
    print("Time Elapsed: ", end_time - start_time)

    # Output Table 7.
    start_time = time.time()
    factors = ['Owner\'s Earnings to Total Assets']
    control_factors = [['Gross Profits to Total Assets'], ['Operating Profits to Total Assets'], ['Cash-Based Operating Profits to Total Assets']]
    constant_controls = ['Mkt-RF', 'SMB', 'HML']
    title = "Table 7"
    short_description = "Spanning regressions for profitability factors."
    long_description = "This table presents a battery of spanning regressions on factor returns from July 1963 to December 2022.  Factor construction is consistent with Fama and French (1993) as outlined in the Data section, and the variable definitions are provided in Appendix A.  Panel A regresses the Owner's Earnings to Total Assets factor on the other profitability factors, while Panel B regresses the other profitability factors on the Owner's Earnings to Total Assets factor.  The annualized alpha, monthly coefficients, t-statistics, and R-squared values are presented in both panels.  Gross Profits to Total Assets is shortened to GP/A, Operating Profits to Total Assets to OP/A, Cash-Based Operating Profits to Total Assets to CbOP/A, and Owner's Earnings to Total Assets to OE/A.  The excess return of the market and the Fama-French SMB and HML factors are included as controls in all regressions."
    output_file = "table7.tex"
    spanning_regressions(factors, control_factors, constant_controls, title, short_description, long_description, output_file)
    end_time = time.time()
    print("Performed spanning regressions.")
    print("Time Elapsed: ", end_time - start_time)

    # Output Table 8.
    start_time = time.time()
    regression = [['Owner\'s Earnings to Market Equity'], ['Owner\'s Earnings to Total Assets'], ['Owner\'s Earnings to Book Equity'], ['Owner\'s Earnings Composite'],  ['Owner\'s Earnings to Market Equity', 'Owner\'s Earnings to Total Assets', 'Owner\'s Earnings to Book Equity', 'Owner\'s Earnings Composite']]
    variables_order = ['Owner\'s Earnings to Market Equity', 'Owner\'s Earnings to Total Assets', 'Owner\'s Earnings to Book Equity', 'Owner\'s Earnings Composite', 'Cash-Based Operating Profits Composite']
    title = "Table 8"
    short_description = "Owner's earnings in Fama-MacBeth regressions."
    long_description = "This table presents the average Fama and MacBeth (1973) cross sectional regression slopes (multiplied by 100) and their respective t-statistics from regressions that predict monthly returns.  The regressions spanned from July 1963 to December 2022. Panel A presents the results for All-but-microcaps, while Panel B presents the data for Microcaps – defined as having a market equity above the 20th percentile of all NYSE securities in the previous month.  The construction of owner's earnings is presented in Appendix A.  All variables are winsorized at the 1st and 99th percentile.  All columns require non-missing data for the variables of interest, book equity, market equity, and total assets."
    output_file = "table8.tex"
    fama_macbeth_regression(regression, variables_order, title, short_description, long_description, output_file)
    end_time = time.time()
    print("Conducted Fama-MacBeth Regressions for Owner's Earnings metrics.")
    print("Time Elapsed: ", end_time - start_time)

    # Output Table 9.
    start_time = time.time()
    title = "Table 9"
    short_description = "Descriptive statistics for factors."
    long_description = "Panel A reports the annual return, standard deviation, and Sharpe ratio for the given factors.  The owner's earnings factor is contructed as outlined in the Data section, and the underlying variable is simply the sum of the ranks of the owner's earnings to market equity and owner's earnings to total assets.  The Fama and French (2018) 6-factors are taken from the Ken French data library.  Panel B presents the Pearson correlations between the factors.  Panel C presents the Spearman correlations between the factors."
    output_file = "table9.tex"
    output_summary_statistics(['Owner\'s Earnings Composite', 'Mkt-RF', 'SMB', 'HML', 'RMW', 'CMA', 'UMD'], title, short_description, long_description, output_file)
    end_time = time.time()
    print("Outputed Summary Statistics.")
    print("Time Elapsed: ", end_time - start_time)

    # Output Table 10.
    start_time = time.time()
    predictor = 'Owner\'s Earnings Composite'
    title = "Table 10"
    short_description = "Factor regressions."
    long_description = "This table presents regressions of the owner's earnings composite factor against the Fama and French (2018) 6-factor model, the Hou et al. (2021) $q5$-factor model, the Daniel et al. (2019) 3-factor model, and the Stambaugh and Yuan (2017) 4-factor model.  These factor returns were taken from their respective websites.  The Fama and French (2018) market and size factors were used as a stand-in for all market and size factors."
    output_file = "table10.tex"
    regress_on_factor_models(predictor, title, short_description, long_description, output_file)
    end_time = time.time()
    print("Conducted Fama-MacBeth Regressions for Market Equity.")
    print("Time Elapsed: ", end_time - start_time)

    # Output Table 11.
    start_time = time.time()
    predictor = 'Owner\'s Earnings Composite'
    title = "Table 11"
    short_description = "Decile sorts."
    long_description = "This table presents the average annualized excess returns, standard deviation, and Sharpe ratio for the portfolios formed on the NYSE deciles of the owner's earnings composite factor.  These portfolios are then regressed upon the Fama and French (2018) 6-factor model (from the Ken French Data Library), and the resulting alpha and t-statistics are presented."
    output_file = "table11.tex"
    perform_decile_sorts(predictor, title, short_description, long_description, output_file)
    end_time = time.time()
    print("Performed decile sorts.")
    print("Time Elapsed: ", end_time - start_time)

    # Output Figure 1.
    start_time = time.time()
    portfolio_returns = ['Mkt-RF', 'Owner\'s Earnings Composite', '10']
    output_file = "figure1.png"
    display_cumulative_returns(portfolio_returns, output_file)
    end_time = time.time()
    print("Displayed cumulative returns.")
    print("Time Elapsed: ", end_time - start_time)

    # Output Table B1.
    start_time = time.time()
    regression = [['Cash-Based Operating Profits to Book Equity'], ['Capital Expenditures to Book Equity'], ['Cash-Based Operating Profits to Book Equity', 'Capital Expenditures to Book Equity'], ['Owner\'s Earnings to Book Equity'], ['Cash-Based Operating Profits to Book Equity', 'Owner\'s Earnings to Book Equity']]
    variables_order = ['Cash-Based Operating Profits to Book Equity', 'Capital Expenditures to Book Equity', 'Owner\'s Earnings to Book Equity']
    title = "Table B1"
    short_description = "Cash-based operating profits, capital expenditures, and owner's earnings deflated by book equity in Fama-MacBeth regressions."
    long_description = "This table presents the average Fama and MacBeth (1973) cross sectional regression slopes (multiplied by 100) and their respective t-statistics from regressions that predict monthly returns.  The regressions spanned from July 1963 to December 2022. Panel A presents the results for All-but-microcaps, while Panel B presents the data for Microcaps – defined as having a market equity above the 20th percentile of all NYSE securities in the previous month.  The construction of cash-based operating profits and owner's earnings is presented in Appendix A.  All variables are winsorized at the 1st and 99th percentile.  All columns require non-missing data for the variables of interest, book equity, market equity, and total assets."
    output_file = "tableb1.tex"
    fama_macbeth_regression(regression, variables_order, title, short_description, long_description, output_file)
    end_time = time.time()
    print("Conducted Fama-MacBeth Regressions for Book Equity.")
    print("Time Elapsed: ", end_time - start_time)

    # Output Table B2.
    start_time = time.time()
    title = "Table B2"
    short_description = "Descriptive statistics for profitability factors."
    long_description = "Panel A reports the annual return, standard deviation, and Sharpe ratio for the given factors.  Factor construction is consistent with Fama and French (1993) as outlined in the Data section, and the variable definitions are provided in Appendix A.  Panel B presents the Pearson correlations between the factors.  Panel C presents the Spearman correlations between the factors, while Panel C presents the Spearman correlations."
    output_file = "tableb2.tex"
    output_summary_statistics(['Gross Profits to Book Equity', 'Operating Profits to Book Equity', 'Cash-Based Operating Profits to Book Equity', 'Owner\'s Earnings to Book Equity'], title, short_description, long_description, output_file)
    end_time = time.time()
    print("Outputed Summary Statistics.")
    print("Time Elapsed: ", end_time - start_time)

    # Output Table B3.
    start_time = time.time()
    factors = ['Owner\'s Earnings to Book Equity']
    control_factors = [['Gross Profits to Book Equity'], ['Operating Profits to Book Equity'], ['Cash-Based Operating Profits to Book Equity']]
    constant_controls = ['Mkt-RF', 'SMB', 'HML']
    title = "Table B3"
    short_description = "Spanning regressions for profitability factors."
    long_description = "This table presents a battery of spanning regressions on factor returns from July 1963 to December 2022.  Factor construction is consistent with Fama and French (1993) as outlined in the Data section, and the variable definitions are provided in Appendix A.  Panel A regresses the Owner's Earnings to Book Equity factor on the other profitability factors, while Panel B regresses the other profitability factors on the Owner's Earnings to Book Equity factor.  The annualized alpha, monthly coefficients, t-statistics, and R-squared values are presented in both panels.  Gross Profits to Book Equity is shortened to GP/BE, Operating Profits to Book Equity to OP/BE, Cash-Based Operating Profits to Book Equity to CbOP/BE, and Owner's Earnings to Book Equity to OE/BE.  The excess return of the market and the Fama-French SMB and HML factors are included as controls in all regressions."
    output_file = "tableb3.tex"
    spanning_regressions(factors, control_factors, constant_controls, title, short_description, long_description, output_file)
    end_time = time.time()
    print("Performed spanning regressions.")
    print("Time Elapsed: ", end_time - start_time)