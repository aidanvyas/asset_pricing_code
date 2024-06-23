import logging
import re
import pandas as pd
import numpy as np
from pandas.tseries.offsets import MonthEnd
import statsmodels.api as sm
from industry_handling import assign_industry


def setup_logging(logging_enabled: bool = True) -> None:
    """
    Set up logging configuration.

    This function configures the logging settings for the application. It sets
    the logging level to INFO and specifies the log message format. If logging
    is not enabled, it disables all logging messages.

    Args:
        logging_enabled (bool):
            Whether to enable logging. Defaults to True.

    Returns:
        None
    """
    if logging_enabled:
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
    else:
        logging.disable(logging.CRITICAL)


def quantile_bucket(row: pd.Series, factor: str, quantiles: int) -> str:
    """
    Assign a stock to the correct factor bucket.

    Args:
        row (pd.Series):
            The row of the DataFrame.
        factor (str):
            The factor to use for the bucketing.
        quantiles (int):
            The number of quantiles to use.

    Returns:
        str: The bucket to assign the stock to or '' if the value is NaN.
    """
    if pd.isna(row[factor]):
        return ''
    for i in range(1, quantiles):
        if row[factor] <= row[f'{i * 100 // quantiles}%']:
            return str(i)
    return str(quantiles)


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


def create_original_mom_transition_table(
    quantiles: int, 
    lookback_period: int, 
    lag: int, 
    nyse_only: bool = True, 
    logging_enabled: bool = True
) -> None:
    """
    Creates a transition table for the momentum portfolios.

    Args:
        quantiles (int):
            The number of quantiles to use for portfolio formation.
        lookback_period (int):
            The lookback period for calculating momentum.
        lag (int):
            The lag for calculating momentum.
        nyse_only (bool):
            Whether to use only NYSE common stocks.
        logging_enabled (bool):
            Whether to enable logging.

    Returns:
        None
    """

    # Set up logging.
    setup_logging(logging_enabled)

    logging.info("Reading in the csv files...")
    crsp3 = pd.read_csv('data/processed_crsp_data.csv', usecols=['PERMNO', 'retadj', 'jdate', 'me', 'wt', 'SHRCD', 'EXCHCD', 'count'], parse_dates=['jdate'])

    logging.info("Calculating momentum...")
    crsp3['MOMENTUM'] = crsp3.groupby('PERMNO')['retadj'].apply(lambda x: x.shift(lag + 1).rolling(window=lookback_period - lag, min_periods=lookback_period - lag).mean()).reset_index(level=0, drop=True)

    logging.info("Selecting the universe of stocks...")
    universe = crsp3[(crsp3['me'] > 0) &
                    (crsp3['count'] >= 1) &
                    ((crsp3['SHRCD'] == 10) | (crsp3['SHRCD'] == 11))]

    # If nyse_only is True, select only NYSE common stocks.
    if nyse_only:
        universe = crsp3[(crsp3['EXCHCD'] == 1)]

    logging.info("Getting the MOMENTUM quantile breakpoints...")
    percentiles = [i * 100 / quantiles for i in range(1, quantiles)]
    universe_mom = universe.groupby(['jdate'])['MOMENTUM'].describe(percentiles=[p / 100 for p in percentiles]).reset_index()
    percentile_columns = [f'{int(p)}%' for p in percentiles]
    universe_mom = universe_mom[['jdate'] + percentile_columns]

    logging.info("Merging the breakpoints with the CRSP data...")
    crsp4 = pd.merge(crsp3, universe_mom, how='left', on=['jdate'])

    logging.info("Assigning each stock to its proper momentum bucket...")
    crsp4['factor_portfolio'] = np.where(
        (crsp4['me'] > 0) & (crsp4['count'] >= 1),
        crsp4.apply(lambda row: quantile_bucket(row, 'MOMENTUM', quantiles), axis=1),
        ''
    )

    logging.info("Creating a 'valid_data' column...")
    crsp4['valid_data'] = np.where(
        (crsp4['me'] > 0) & (crsp4['count'] >= 1),
        1,
        0
    )

    logging.info("Creating a 'non_missing_portfolio' column...")
    crsp4['non_missing_portfolio'] = np.where(
        (crsp4['factor_portfolio'] != ''),
        1,
        0
    )

    logging.info("Keeping only the common stocks with a positive weight, valid data, and a non-missing portfolio...")
    crsp5 = crsp4[(crsp4['wt'] > 0) &
                  (crsp4['valid_data'] == 1) &
                  (crsp4['non_missing_portfolio'] == 1) &
                  ((crsp4['SHRCD'] == 10) | (crsp4['SHRCD'] == 11))]

    logging.info("Dropping columns and rows with missing values...")
    crsp5 = crsp5[['PERMNO', 'jdate', 'retadj', 'me', 'wt', 'MOMENTUM', 'factor_portfolio']]
    crsp5 = crsp5.dropna(subset=['MOMENTUM'])

    logging.info("Sorting the data by date and PERMNO...")
    crsp5 = crsp5.sort_values(by=['PERMNO', 'jdate'])

    logging.info("Creating a column for the past momentum portfolio assignment...")
    crsp5['past_portfolio'] = crsp5.groupby('PERMNO')['factor_portfolio'].shift(lookback_period)

    logging.info("Filtering out rows with missing current_portfolio or past_portfolio values...")
    crsp5 = crsp5.dropna(subset=['factor_portfolio', 'past_portfolio'])

    logging.info("Saving the data to a csv file...")
    crsp5.to_csv(f'back_momentum_skewness/data/processed_mom_transitions_{[lookback_period, lag]}_with_{quantiles}_quantiles.csv', index=False)
    logging.info("Saved the data to a csv file.")


def calculate_mom_transition_probabilities(quantiles: int,
                                       lookback_period: int,
                                       lag: int,
                                       logging_enabled: bool = True):
    """
    This function calculates the transition probabilities between momentum portfolios.

    Args:
        quantiles (int): The number of quantiles to use for portfolio formation.
        lookback_period (int): The lookback period for calculating momentum.
        lag (int): The lag for calculating momentum.
        logging_enabled (bool): Whether to enable logging.

    Returns:
        None
    """
     
    # Set up logging.
    setup_logging(logging_enabled)

    # Read in the csv file.
    crsp5 = pd.read_csv(f'back_momentum_skewness/data/processed_mom_transitions_{[lookback_period, lag]}_with_{quantiles}_quantiles.csv', parse_dates=['jdate'])
    logging.info("Read in the csv file.")

    # Set a date restriction from July 1963 to December 2022.
    crsp5 = crsp5[(crsp5['jdate'] >= '1963-07-01') & (crsp5['jdate'] <= '2022-12-31')]
    logging.info("Set a date restriction.")

    # Create a column to use as values for the pivot table
    crsp5['count'] = 1
    logging.info("Created a column to use as values for the pivot table.")

    # Create a pivot table to calculate the transition counts
    transition_counts = pd.pivot_table(crsp5, values='count', index='past_portfolio', columns='factor_portfolio', aggfunc='sum')
    logging.info("Created a pivot table to calculate the transition counts.")

    # Normalize the transition counts
    transition_probs = transition_counts.div(transition_counts.sum(axis=1), axis=0) * 100
    logging.info("Normalized the transition counts.")

    # Create a LaTeX table
    latex_content = [
        "\\begin{table*}[ht!]",
        "\\raggedright",
        "\\refstepcounter{table}",
        "\\label{tab: transition_probs_" + f"[{lookback_period}, {lag}]" + "_with_" + str(quantiles) + "_quantiles}",
        "\\textbf{Table \\thetable} \\\\",
        "Transition probabilities for " + f"[{lookback_period}, {lag}]" + " with " + str(quantiles) + " quantiles. \\\\",
        "\\hspace*{1em}" + latex_escape("This sample starts in July 1963, ends in December 2022, and includes all NYSE, AMEX, and NASDAQ common stocks for which we have market equity data for December of year t-1 and June of year t, and book equity data for t-1. The portfolios are constructed on book equity to market equity at the end of each June using quintile breakpoints.  The book equity used in June of year t is the book equity for the last fiscal year end in t-1.  Market equity is calculated at the end of December of year t-1.  More specific definitions can be found in the Appendix.  The data is measured monthly, with all statistics annualized.  1%, 5%, and 10% statistical significance are indicated with ***, **, and *, respectively.") + " \\\\",
        "\\vspace{0.5em}",
        "\\centering",
        "\\begin{adjustbox}{max width=\\textwidth}",
        "\\begin{tabular}{@{}c" + "c" * quantiles + "@{}}",
        "\\toprule",
        "Past & \\multicolumn{" + str(quantiles) + "}{c}{Current Momentum Portfolio} \\\\",
        "Portfolio & " + " & ".join(transition_probs.columns.astype(str)) + " \\\\",
        "\\midrule"
    ]

    for index, row in transition_probs.iterrows():
        row_str = str(index) + " & " + " & ".join(row.apply(lambda x: f"{x:.2f}\%")) + " \\\\"
        latex_content.append(row_str)

    latex_content.extend([
        "\\bottomrule",
        "\\end{tabular}",
        "\\end{adjustbox}",
        "\\end{table*}"
    ])
    logging.info("Added the table footer to the LaTeX table.")

    # Join the content and write it to a file
    latex_content = "\n".join(latex_content)
    file_name = f"back_momentum_skewness/tables/transition_probs_{[lookback_period, lag]}_with_{quantiles}_quantiles.tex"
    with open(file_name, 'w') as f:
        f.write(latex_content)
    logging.info(f"Saved the LaTeX table to '{file_name}'.")


def create_ff_transition_tables(
    quantiles: int,
    factor: str,
    nyse_only: bool = True,
    logging_enabled: bool = True
) -> None:
    """
    Perform quantile sorts on the Fama-French factors.

    Args:
        quantiles (int):
            The number of quantiles to use for portfolio formation.
        factor (str):
            The factor to use for the quantile sorts.
        nyse_only (bool):
            Whether to use only NYSE common stocks.
        logging_enabled (bool):
            Whether to enable logging.

    Returns:
        None
    """

    # Set up logging.
    setup_logging(logging_enabled)

    # Read in the csv files.
    ccm_jun = pd.read_csv('data/processed_crsp_jun1.csv', usecols=['BE', 'dec_me', 'EXCHCD', 'me', 'count', 'SHRCD', 'jdate', 'PERMNO', 'MthCalDt', 'OP', 'OP_BE', 'AT_GR1'], parse_dates=['jdate'])
    crsp3 = pd.read_csv('data/processed_crsp_data.csv', usecols=['MthCalDt', 'PERMNO', 'SHRCD', 'EXCHCD', 'retadj', 'me', 'wt', 'cumretx', 'ffyear', 'jdate'], parse_dates=['jdate'])
    logging.info("Read in the csv files.")

    # Calculate book to market equity ratio.
    ccm_jun['BE_ME'] = ccm_jun['BE'] * 1000 / ccm_jun['dec_me']
    logging.info("Calculated the book to market equity ratio.")
    
    # Select the universe of common stocks with positive market equity.
    universe = ccm_jun[
        (ccm_jun['me'] > 0) &
        (ccm_jun['count'] >= 1) &
        ((ccm_jun['SHRCD'] == 10) | (ccm_jun['SHRCD'] == 11))
    ]
    logging.info("Selected the universe of stocks.")

    # If nyse_only is True, select only NYSE common stocks.
    if (nyse_only):
        universe = universe[universe['EXCHCD'] == 1]
        logging.info("Selected only NYSE common stocks.")

    # Get the factor quantile breakpoints for each month.
    percentiles = [i * 100 / quantiles for i in range(1, quantiles)]
    universe_ff = (
        universe.groupby(['jdate'])[factor]
        .describe(percentiles=[p / 100 for p in percentiles])
        .reset_index()
    )
    percentile_columns = [f'{int(p)}%' for p in percentiles]
    universe_ff = universe_ff[['jdate'] + percentile_columns]
    logging.info(f"Got the {factor} quantile breakpoints.")

    # Merge the breakpoints with the CCM June data.
    ccm1_jun = pd.merge(ccm_jun, universe_ff, how='left', on=['jdate'])
    logging.info("Merged the breakpoints with the CCM June data.")

    # Assign each stock to its proper factor bucket.
    ccm1_jun['factor_portfolio'] = np.where(
        (ccm_jun['dec_me'] > 0) & (ccm1_jun['me'] > 0) & (ccm1_jun['count'] >= 1),
        ccm1_jun.apply(lambda row: quantile_bucket(row, factor, quantiles), axis=1),
        ''
    )
    logging.info("Assigned each stock to its proper book to market bucket.")

    # Create a 'valid_data' column that is 1 if company has valid June and December market equity data and has been in the dataframe at least once, and 0 otherwise.
    ccm1_jun['valid_data'] = np.where(
        (ccm_jun['dec_me'] > 0) & (ccm1_jun['me'] > 0) & (ccm1_jun['count'] >= 1),
        1,
        0
    )
    logging.info("Created a 'valid_data' column.")

    # Create a 'non_missing_portfolio' column that is 1 if the stock has been assigned to a portfolio, and 0 otherwise.
    ccm1_jun['non_missing_portfolio'] = np.where(
        (ccm1_jun['factor_portfolio'] != ''),
        1,
        0
    )
    logging.info("Created a 'non_missing_portfolio' column.")

    # Create a new dataframe with only the essential columns for storing the portfolio assignments as of June.
    june = ccm1_jun[['PERMNO', 'MthCalDt', 'jdate', 'factor_portfolio', 'valid_data', 'non_missing_portfolio']].copy()
    logging.info("Created a new dataframe with only the essential columns.")

    # Create a column representing the Fama-French year.
    june['ffyear'] = june['jdate'].dt.year
    logging.info("Created a column representing the Fama-French year.")

    # Merge monthly CRSP data with the portfolio assignments in June.
    ccm3 = pd.merge(crsp3,
                    june[['PERMNO', 'ffyear', 'factor_portfolio', 'valid_data', 'non_missing_portfolio']],
                    how='left', on=['PERMNO', 'ffyear'])
    logging.info("Merged monthly CRSP data with the portfolio assignments in June.")

    # Keep only the common stocks with a positive weight, valid data, and a non-missing portfolio.
    ccm4 = ccm3[(ccm3['wt'] > 0) &
                (ccm3['valid_data'] == 1) &
                (ccm3['non_missing_portfolio'] == 1) &
                ((ccm3['SHRCD'] == 10) | (ccm3['SHRCD'] == 11))]
    logging.info("Kept only the common stocks with a positive weight, valid data, and a non-missing portfolio.")

    # Keep only the essential columns.
    ccm4 = ccm4[['PERMNO', 'jdate', 'retadj', 'me', 'wt', 'factor_portfolio']]
    logging.info("Kept only the essential columns.")

    # Sort the data by date and PERMNO.
    ccm4 = ccm4.sort_values(by=['PERMNO', 'jdate'])
    logging.info("Sorted the data by date and PERMNO.")

    # Create a column for the past factor portfolio assignment.
    ccm4['past_portfolio'] = ccm4.groupby('PERMNO')['factor_portfolio'].shift(12)
    logging.info("Created a column for the past factor portfolio assignment.")

    # Filter out rows with missing current_portfolio or next_portfolio values.
    ccm4 = ccm4.dropna(subset=['factor_portfolio', 'past_portfolio'])
    logging.info("Filtered out rows with missing current_portfolio or past_portfolio values.")

    # Save the data to a csv file.
    ccm4.to_csv(f'back_momentum_skewness/data/processed_ff_transitions_{factor}_with_{quantiles}_quantiles.csv', index=False)
    logging.info("Saved the data to a csv file.")


def calculate_ff_transition_probabilities(
    quantiles: int,
    factor: str,
    logging_enabled: bool = True
) -> None:
    """
    This function calculates the transition probabilities between Fama-French factor portfolios.

    Args:
        quantiles (int): The number of quantiles to use for portfolio formation.
        factor (str): The factor to use for the quantile sorts.
        logging_enabled (bool): Whether to enable logging.

    Returns:
        None
    """

    # Set up logging.
    setup_logging(logging_enabled)

    # Read in the csv file.
    ccm4 = pd.read_csv(f'back_momentum_skewness/data/processed_ff_transitions_{factor}_with_{quantiles}_quantiles.csv', parse_dates=['jdate'])
    logging.info("Read in the csv file.")

    # Set a date restriction from July 1963 to December 2022.
    ccm4 = ccm4[(ccm4['jdate'] >= '1963-07-01') & (ccm4['jdate'] <= '2022-12-31')]
    logging.info("Set a date restriction.")

    # Create a column to use as values for the pivot table
    ccm4['count'] = 1
    logging.info("Created a column to use as values for the pivot table.")

    # Create a pivot table to calculate the transition counts.
    transition_counts = pd.pivot_table(ccm4, values='count', index='past_portfolio', columns='factor_portfolio', aggfunc='sum')
    logging.info("Created a pivot table to calculate the transition counts.")

    # Normalize the transition counts
    transition_probs = transition_counts.div(transition_counts.sum(axis=1), axis=0) * 100
    logging.info("Normalized the transition counts.")

    # Create a LaTeX table
    latex_content = [
        "\\begin{table*}[ht!]",
        "\\raggedright",
        "\\refstepcounter{table}",
        "\\label{tab: transition_probs_" + f"{factor}" + "_with_" + str(quantiles) + "_quantiles}",
        "\\textbf{Table \\thetable} \\\\",
        "Transition probabilities for " + f"factor" + " with " + str(quantiles) + " quantiles. \\\\",
        "\\hspace*{1em}" + latex_escape("This sample starts in July 1963, ends in December 2022, and includes all NYSE, AMEX, and NASDAQ common stocks for which we have market equity data for December of year t-1 and June of year t, and book equity data for t-1. The portfolios are constructed on book equity to market equity at the end of each June using quintile breakpoints.  The book equity used in June of year t is the book equity for the last fiscal year end in t-1.  Market equity is calculated at the end of December of year t-1.  More specific definitions can be found in the Appendix.  The data is measured monthly, with all statistics annualized.  1%, 5%, and 10% statistical significance are indicated with ***, **, and *, respectively.") + " \\\\",
        "\\vspace{0.5em}",
        "\\centering",
        "\\begin{adjustbox}{max width=\\textwidth}",
        "\\begin{tabular}{@{}c" + "c" * quantiles + "@{}}",
        "\\toprule",
        "Prior & \\multicolumn{" + str(quantiles) + "}{c}{Current Factor Portfolio} \\\\",
        "Portfolio & " + " & ".join(transition_probs.columns.astype(str)) + " \\\\",
        "\\midrule"
    ]

    for index, row in transition_probs.iterrows():
        row_str = str(index) + " & " + " & ".join(row.apply(lambda x: f"{x:.2f}\%")) + " \\\\"
        latex_content.append(row_str)

    latex_content.extend([
        "\\bottomrule",
        "\\end{tabular}",
        "\\end{adjustbox}",
        "\\end{table*}"
    ])
    logging.info("Added the table footer to the LaTeX table.")

    # Join the content and write it to a file
    latex_content = "\n".join(latex_content)
    file_name = f"back_momentum_skewness/tables/transition_probs_{factor}_with_{quantiles}_quantiles.tex"
    with open(file_name, 'w') as f:
        f.write(latex_content)
    logging.info(f"Saved the LaTeX table to '{file_name}'.")


def create_ff_multiyear_transition_tables(
    quantiles: int,
    factor: str,
    nyse_only: bool = True,
    logging_enabled: bool = True
) -> None:
    """
    Perform quantile sorts on the Fama-French factors, using a 5-year calculation for past portfolios
    and a single-year calculation for current portfolios.

    Args:
        quantiles (int):
            The number of quantiles to use for portfolio formation.
        factor (str):
            The factor to use for the quantile sorts.
        nyse_only (bool):
            Whether to use only NYSE common stocks.
        logging_enabled (bool):
            Whether to enable logging.

    Returns:
        None
    """

    # Set up logging.
    setup_logging(logging_enabled)

    # Read in the csv files.
    ccm_jun = pd.read_csv('data/processed_crsp_jun1.csv', usecols=['BE', 'dec_me', 'EXCHCD', 'me', 'count', 'SHRCD', 'jdate', 'PERMNO', 'MthCalDt', 'OP', 'OP_BE', 'AT_GR1'], parse_dates=['jdate'])
    crsp3 = pd.read_csv('data/processed_crsp_data.csv', usecols=['MthCalDt', 'PERMNO', 'SHRCD', 'EXCHCD', 'retadj', 'me', 'wt', 'cumretx', 'ffyear', 'jdate'], parse_dates=['jdate'])
    logging.info("Read in the csv files.")

    # Calculate book to market equity ratio.
    ccm_jun['BE_ME'] = ccm_jun['BE'] * 1000 / ccm_jun['dec_me']
    logging.info("Calculated the book to market equity ratio.")

    # Calculate multi-year factor excluding the current period.
    for lag in range(1, 6):
        ccm_jun[f'lag{lag}_{factor}'] = ccm_jun.groupby('PERMNO')[factor].shift(lag)
        ccm_jun[f'lag{lag}_{factor}'] = ccm_jun[f'lag{lag}_{factor}'].replace([np.inf, -np.inf], np.nan)
    ccm_jun[f'multiyear_{factor}'] = ccm_jun[[f'lag{lag}_{factor}' for lag in range(1, 6)]].mean(axis=1, skipna=True)
    logging.info(f"Calculated the multi-year {factor} excluding the current period.")

    logging.info("Removing NaN, inf, and -inf values from the factor column...")
    ccm_jun = ccm_jun[~ccm_jun[f'multiyear_{factor}'].isnull()]
    ccm_jun = ccm_jun[~np.isinf(ccm_jun[f'multiyear_{factor}'])]
    ccm_jun = ccm_jun[~np.isneginf(ccm_jun[f'multiyear_{factor}'])]

    # Select the universe of common stocks with positive market equity.
    universe = ccm_jun[
        (ccm_jun['me'] > 0) &
        (ccm_jun['count'] >= 1) &
        ((ccm_jun['SHRCD'] == 10) | (ccm_jun['SHRCD'] == 11))
    ]
    logging.info("Selected the universe of stocks.")

    # If nyse_only is True, select only NYSE common stocks.
    if nyse_only:
        universe = universe[universe['EXCHCD'] == 1]
        logging.info("Selected only NYSE common stocks.")

    logging.info("Removing NaN, inf, and -inf values from the factor column...")
    universe = universe[~universe[factor].isnull()]
    universe = universe[~np.isinf(universe[factor])]
    universe = universe[~np.isneginf(universe[factor])]

    # Get the factor quantile breakpoints for each month for the current portfolios.
    percentiles = [i * 100 / quantiles for i in range(1, quantiles)]
    universe_ff_current = (
        universe.groupby(['jdate'])[factor]
        .describe(percentiles=[p / 100 for p in percentiles])
        .reset_index()
    )
    percentile_columns = [f'{int(p)}%' for p in percentiles]
    universe_ff_current = universe_ff_current[['jdate'] + percentile_columns]
    logging.info(f"Got the {factor} quantile breakpoints for the current portfolios.")

    # Get the factor quantile breakpoints for each month for the past portfolios.
    universe_ff_past = (
        universe.groupby(['jdate'])[f'multiyear_{factor}']
        .describe(percentiles=[p / 100 for p in percentiles])
        .reset_index()
    )
    universe_ff_past = universe_ff_past[['jdate'] + percentile_columns]
    logging.info(f"Got the multi-year {factor} quantile breakpoints for the past portfolios.")

    # Merge the breakpoints with the CCM June data.
    ccm1_jun = pd.merge(ccm_jun, universe_ff_current, how='left', on=['jdate'])
    ccm1_jun = pd.merge(ccm1_jun, universe_ff_past, how='left', on=['jdate'], suffixes=('', '_past'))
    logging.info("Merged the breakpoints with the CCM June data.")

    # Assign each stock to its proper factor bucket for the current portfolio.
    ccm1_jun['factor_portfolio'] = np.where(
        (ccm1_jun['dec_me'] > 0) & (ccm1_jun['me'] > 0) & (ccm1_jun['count'] >= 1),
        ccm1_jun.apply(lambda row: quantile_bucket(row, factor, quantiles), axis=1),
        ''
    )
    logging.info("Assigned each stock to its proper factor bucket for the current portfolio.")

    # Assign each stock to its proper factor bucket for the past portfolio.
    ccm1_jun['past_factor_portfolio'] = np.where(
        (ccm1_jun['dec_me'] > 0) & (ccm1_jun['me'] > 0) & (ccm1_jun['count'] >= 1),
        ccm1_jun.apply(lambda row: quantile_bucket(row, f'multiyear_{factor}', quantiles), axis=1),
        ''
    )
    logging.info("Assigned each stock to its proper factor bucket for the past portfolio.")

    # Create a 'valid_data' column that is 1 if company has valid June and December market equity data and has been in the dataframe at least once, and 0 otherwise.
    ccm1_jun['valid_data'] = np.where(
        (ccm1_jun['dec_me'] > 0) & (ccm1_jun['me'] > 0) & (ccm1_jun['count'] >= 1),
        1,
        0
    )
    logging.info("Created a 'valid_data' column.")

    # Create a 'non_missing_portfolio' column that is 1 if the stock has been assigned to a portfolio, and 0 otherwise.
    ccm1_jun['non_missing_portfolio'] = np.where(
        (ccm1_jun['factor_portfolio'] != '') & (ccm1_jun['past_factor_portfolio'] != ''),
        1,
        0
    )
    logging.info("Created a 'non_missing_portfolio' column.")

    # Create a new dataframe with only the essential columns for storing the portfolio assignments as of June.
    june = ccm1_jun[['PERMNO', 'MthCalDt', 'jdate', 'factor_portfolio', 'past_factor_portfolio', 'valid_data', 'non_missing_portfolio']].copy()
    logging.info("Created a new dataframe with only the essential columns.")

    # Create a column representing the Fama-French year.
    june['ffyear'] = june['jdate'].dt.year
    logging.info("Created a column representing the Fama-French year.")

    # Merge monthly CRSP data with the portfolio assignments in June.
    ccm3 = pd.merge(crsp3,
                    june[['PERMNO', 'ffyear', 'factor_portfolio', 'past_factor_portfolio', 'valid_data', 'non_missing_portfolio']],
                    how='left', on=['PERMNO', 'ffyear'])
    logging.info("Merged monthly CRSP data with the portfolio assignments in June.")

    # Keep only the common stocks with a positive weight, valid data, and a non-missing portfolio.
    ccm4 = ccm3[(ccm3['wt'] > 0) &
                (ccm3['valid_data'] == 1) &
                (ccm3['non_missing_portfolio'] == 1) &
                ((ccm3['SHRCD'] == 10) | (ccm3['SHRCD'] == 11))]
    logging.info("Kept only the common stocks with a positive weight, valid data, and a non-missing portfolio.")

    # Keep only the essential columns.
    ccm4 = ccm4[['PERMNO', 'jdate', 'retadj', 'me', 'wt', 'factor_portfolio', 'past_factor_portfolio']]
    logging.info("Kept only the essential columns.")

    # Sort the data by date and PERMNO.
    ccm4 = ccm4.sort_values(by=['PERMNO', 'jdate'])
    logging.info("Sorted the data by date and PERMNO.")

    # Create a column for the past factor portfolio assignment.
    ccm4['past_portfolio'] = ccm4.groupby('PERMNO')['past_factor_portfolio'].shift(12)
    logging.info("Created a column for the past factor portfolio assignment.")

    # Filter out rows with missing current_portfolio or past_portfolio values.
    ccm4 = ccm4.dropna(subset=['factor_portfolio', 'past_portfolio'])
    logging.info("Filtered out rows with missing current_portfolio or past_portfolio values.")

    # Save the data to a csv file.
    ccm4.to_csv(f'back_momentum_skewness/data/processed_multiyear_ff_transitions_{factor}_with_{quantiles}_quantiles.csv', index=False)
    logging.info("Saved the data to a csv file.")


def calculate_ff_multiyear_transition_probabilities(
    quantiles: int,
    factor: str,
    logging_enabled: bool = True) -> None:
    """
    This function calculates the transition probabilities between Fama-French multi-year factor portfolios.

    Args:
        quantiles (int): The number of quantiles to use for portfolio formation.
        factor (str): The factor to use for the quantile sorts.
        logging_enabled (bool): Whether to enable logging.
    
    Returns:
        None
    """

    # Set up logging.
    setup_logging(logging_enabled)

    # Read in the csv file.
    ccm4 = pd.read_csv(f'back_momentum_skewness/data/processed_multiyear_ff_transitions_{factor}_with_{quantiles}_quantiles.csv', parse_dates=['jdate'])
    logging.info("Read in the csv file.")

    # Set a date restriction from July 1963 to December 2022.
    ccm4 = ccm4[(ccm4['jdate'] >= '1963-07-01') & (ccm4['jdate'] <= '2022-12-31')]
    logging.info("Set a date restriction.")

    # Create a column to use as values for the pivot table
    ccm4['count'] = 1
    logging.info("Created a column to use as values for the pivot table.")

    # Create a pivot table to calculate the transition counts.
    transition_counts = pd.pivot_table(ccm4, values='count', index='past_portfolio', columns='factor_portfolio', aggfunc='sum')
    logging.info("Created a pivot table to calculate the transition counts.")

    # Normalize the transition counts.
    transition_probs = transition_counts.div(transition_counts.sum(axis=1), axis=0) * 100
    logging.info("Normalized the transition counts.")

    # Create a LaTeX table.
    latex_content = [
        "\\begin{table*}[ht!]",
        "\\raggedright",
        "\\refstepcounter{table}",
        "\\label{tab: multiyear_transition_probs_" + f"{factor}" + "_with_" + str(quantiles) + "_quantiles}",
        "\\textbf{Table \\thetable} \\\\",
        "Multiyear transition probabilities for " + f"{factor}" + " with " + str(quantiles) + " quantiles. \\\\",
        "\\hspace*{1em}" + latex_escape("This sample starts in July 1963, ends in December 2022, and includes all NYSE, AMEX, and NASDAQ common stocks for which we have market equity data for December of year t-1 and June of year t, and book equity data for t-1. The portfolios are constructed on book equity to market equity at the end of each June using quintile breakpoints.  The book equity used in June of year t is the book equity for the last fiscal year end in t-1.  Market equity is calculated at the end of December of year t-1.  More specific definitions can be found in the Appendix.  The data is measured monthly, with all statistics annualized.  1%, 5%, and 10% statistical significance are indicated with ***, **, and *, respectively.") + " \\\\",
        "\\vspace{0.5em}",
        "\\centering",
        "\\begin{adjustbox}{max width=\\textwidth}",
        "\\begin{tabular}{@{}c" + "c" * quantiles + "@{}}",
        "\\toprule",
        "Prior & \\multicolumn{" + str(quantiles) + "}{c}{Current Factor Portfolio} \\\\",
        "Portfolio & " + " & ".join(transition_probs.columns.astype(str)) + " \\\\",
        "\\midrule"
    ]

    for index, row in transition_probs.iterrows():
        row_str = str(index) + " & " + " & ".join(row.apply(lambda x: f"{x:.2f}\%")) + " \\\\"
        latex_content.append(row_str)

    latex_content.extend([
        "\\bottomrule",
        "\\end{tabular}",
        "\\end{adjustbox}",
        "\\end{table*}"
    ])
    logging.info("Added the table footer to the LaTeX table.")

    # Join the content and write it to a file.
    latex_content = "\n".join(latex_content)
    file_name = f"back_momentum_skewness/tables/multiyear_transition_probs_{factor}_with_{quantiles}_quantiles.tex"
    with open(file_name, 'w') as f:
        f.write(latex_content)
    logging.info(f"Saved the LaTeX table to '{file_name}'.")


def create_ff_returns_transition_tables(
    quantiles: int,
    factor: str,
    nyse_only: bool = True,
    logging_enabled: bool = True
) -> None:
    """
    Perform quantile sorts on the Fama-French factors.

    Args:
        quantiles (int):
            The number of quantiles to use for portfolio formation.
        factor (str):
            The factor to use for the quantile sorts.
        nyse_only (bool):
            Whether to use only NYSE common stocks.
        logging_enabled (bool):
            Whether to enable logging.

    Returns:
        None
    """

    # Set up logging.
    setup_logging(logging_enabled)

    # Read in the csv files.
    ccm_jun = pd.read_csv('data/processed_crsp_jun1.csv', usecols=['BE', 'dec_me', 'EXCHCD', 'me', 'count', 'SHRCD', 'jdate', 'PERMNO', 'MthCalDt', 'OP', 'OP_BE', 'AT_GR1'], parse_dates=['jdate'])
    crsp3 = pd.read_csv('data/processed_crsp_data.csv', usecols=['MthCalDt', 'PERMNO', 'SHRCD', 'EXCHCD', 'retadj', 'me', 'wt', 'cumretx', 'ffyear', 'jdate'], parse_dates=['jdate'])
    logging.info("Read in the csv files.")

    # Calculate book to market equity ratio.
    ccm_jun['BE_ME'] = ccm_jun['BE'] * 1000 / ccm_jun['dec_me']
    logging.info("Calculated the book to market equity ratio.")

    # Select the universe of common stocks with positive market equity.
    universe = ccm_jun[
        (ccm_jun['me'] > 0) &
        (ccm_jun['count'] >= 1) &
        ((ccm_jun['SHRCD'] == 10) | (ccm_jun['SHRCD'] == 11))
    ]
    logging.info("Selected the universe of stocks.")

    # If nyse_only is True, select only NYSE common stocks.
    if (nyse_only):
        universe = universe[universe['EXCHCD'] == 1]
        logging.info("Selected only NYSE common stocks.")

    # Get the factor quantile breakpoints for each month.
    percentiles = [i * 100 / quantiles for i in range(1, quantiles)]
    universe_ff = (
        universe.groupby(['jdate'])[factor]
        .describe(percentiles=[p / 100 for p in percentiles])
        .reset_index()
    )
    percentile_columns = [f'{int(p)}%' for p in percentiles]
    universe_ff = universe_ff[['jdate'] + percentile_columns]
    logging.info(f"Got the {factor} quantile breakpoints.")

    # Merge the breakpoints with the CCM June data.
    ccm1_jun = pd.merge(ccm_jun, universe_ff, how='left', on=['jdate'])
    logging.info("Merged the breakpoints with the CCM June data.")

    # Assign each stock to its proper factor bucket.
    ccm1_jun['factor_portfolio'] = np.where(
        (ccm_jun['dec_me'] > 0) & (ccm1_jun['me'] > 0) & (ccm1_jun['count'] >= 1),
        ccm1_jun.apply(lambda row: quantile_bucket(row, factor, quantiles), axis=1),
        ''
    )
    logging.info("Assigned each stock to its proper book to market bucket.")

    # Create a 'valid_data' column that is 1 if company has valid June and December market equity data and has been in the dataframe at least once, and 0 otherwise.
    ccm1_jun['valid_data'] = np.where(
        (ccm_jun['dec_me'] > 0) & (ccm1_jun['me'] > 0) & (ccm1_jun['count'] >= 1),
        1,
        0
    )
    logging.info("Created a 'valid_data' column.")

    # Create a 'non_missing_portfolio' column that is 1 if the stock has been assigned to a portfolio, and 0 otherwise.
    ccm1_jun['non_missing_portfolio'] = np.where(
        (ccm1_jun['factor_portfolio'] != ''),
        1,
        0
    )
    logging.info("Created a 'non_missing_portfolio' column.")

    # Create a new dataframe with only the essential columns for storing the portfolio assignments as of June.
    june = ccm1_jun[['PERMNO', 'MthCalDt', 'jdate', 'count', 'factor_portfolio', 'valid_data', 'non_missing_portfolio']].copy()
    logging.info("Created a new dataframe with only the essential columns.")

    # Create a column representing the Fama-French year.
    june['ffyear'] = june['jdate'].dt.year
    logging.info("Created a column representing the Fama-French year.")

    # Merge monthly CRSP data with the portfolio assignments in June.
    ccm3 = pd.merge(crsp3,
                    june[['PERMNO', 'ffyear', 'count', 'factor_portfolio', 'valid_data', 'non_missing_portfolio']],
                    how='left', on=['PERMNO', 'ffyear'])
    logging.info("Merged monthly CRSP data with the portfolio assignments in June.")

    # Keep only the common stocks with a positive weight, valid data, and a non-missing portfolio.
    ccm4 = ccm3[(ccm3['wt'] > 0) &
                (ccm3['valid_data'] == 1) &
                (ccm3['non_missing_portfolio'] == 1) &
                ((ccm3['SHRCD'] == 10) | (ccm3['SHRCD'] == 11))]
    logging.info("Kept only the common stocks with a positive weight, valid data, and a non-missing portfolio.")

    # Keep only the essential columns.
    ccm4 = ccm4[['PERMNO', 'jdate', 'retadj', 'count', 'me', 'wt', 'factor_portfolio']]
    logging.info("Kept only the essential columns.")

    # Sort the data by date and PERMNO.
    ccm4 = ccm4.sort_values(by=['PERMNO', 'jdate'])
    logging.info("Sorted the data by date and PERMNO.")

    # Create a column for the past factor portfolio assignment.
    ccm4['past_portfolio'] = ccm4.groupby('PERMNO')['factor_portfolio'].shift(12)
    logging.info("Created a column for the past factor portfolio assignment.")

    # Calculate returns over the past 12 months - just add the last 12 months of returns.
    ccm4['ret12'] = ccm4.groupby('PERMNO')['retadj'].apply(lambda x: x.rolling(window=12, min_periods=12).sum())
    logging.info("Calculated returns over the past 12 months.")

    # I want to create the return quantiles, so I need to create the breakpoints.
    percentiles = [i * 100 / quantiles for i in range(1, quantiles)]
    universe_ff = (ccm4.groupby(['jdate'])['ret12']
                     .describe(percentiles=[p / 100 for p in percentiles])
                        .reset_index())
    percentile_columns = [f'{int(p)}%' for p in percentiles]
    universe_ff = universe_ff[['jdate'] + percentile_columns]
    logging.info("Got the return quantile breakpoints.")

    # Merge the breakpoints with the CRSP data.
    ccm4 = pd.merge(ccm4, universe_ff, how='left', on=['jdate'])
    logging.info("Merged the breakpoints with the CRSP data.")

    # Now I want to make to create return quantiles.
    ccm4['ret12_quantile'] = np.where(
        (ccm4['me'] > 0) & (ccm4['count'] >= 1),
        ccm4.apply(lambda row: quantile_bucket(row, 'ret12', quantiles), axis=1),
        ''
    )
    logging.info("Assigned each stock to its proper return bucket.")

    # Create a 'valid_data' column that is 1 if company has valid June and December market equity data and has been in the dataframe at least once, and 0 otherwise.
    ccm4['valid_data'] = np.where(
        (ccm4['me'] > 0) & (ccm4['count'] >= 1),
        1,
        0
    )
    logging.info("Created a 'valid_data' column.")

    # Create a 'non_missing_portfolio' column that is 1 if the stock has been assigned to a portfolio, and 0 otherwise.
    ccm4['non_missing_portfolio'] = np.where(
        (ccm4['factor_portfolio'] != ''),
        1,
        0
    )
    logging.info("Created a 'non_missing_portfolio' column.")

    # Keep only the common stocks with a positive weight, valid data, and a non-missing portfolio.
    ccm4 = ccm4[(ccm4['wt'] > 0) &
                (ccm4['valid_data'] == 1) &
                (ccm4['non_missing_portfolio'] == 1)]
    logging.info("Kept only the common stocks with a positive weight, valid data, and a non-missing portfolio.")

    # Filter out rows with missing current_portfolio or next_portfolio values.
    ccm4 = ccm4.dropna(subset=['ret12_quantile', 'past_portfolio'])
    logging.info("Filtered out rows with missing current_portfolio or past_portfolio values.")

    # Keep only the essential columns.
    ccm4 = ccm4[['PERMNO', 'jdate', 'retadj', 'me', 'wt', 'ret12_quantile', 'past_portfolio']]
    logging.info("Kept only the essential columns.")

    # Save the data to a csv file.
    ccm4.to_csv(f'back_momentum_skewness/data/processed_ff_returns_transitions_{factor}_with_{quantiles}_quantiles.csv', index=False)
    logging.info("Saved the data to a csv file.")

    return None


def calculate_ff_returns_transition_probabilities(
    quantiles: int,
    factor: str,
    logging_enabled: bool = True
) -> None:
    """
    This function calculates the transition probabilities between momentum portfolios.

    Args:
        quantiles (int): The number of quantiles to use for portfolio formation.
        factor (str): The factor to use for the quantile sorts.
        logging_enabled (bool): Whether to enable logging.

    Returns:
        None
    """

    # Set up logging.
    setup_logging(logging_enabled)

    # Read in the csv file.
    ccm4 = pd.read_csv(f'back_momentum_skewness/data/processed_ff_returns_transitions_{factor}_with_{quantiles}_quantiles.csv', parse_dates=['jdate'])
    logging.info("Read in the csv file.")

    # Set a date restriction from July 1963 to December 2022.
    ccm4 = ccm4[(ccm4['jdate'] >= '1963-07-01') & (ccm4['jdate'] <= '2022-12-31')]
    logging.info("Set a date restriction.")

    # Create a column to use as values for the pivot table
    ccm4['count'] = 1
    logging.info("Created a column to use as values for the pivot table.")

    # Create a pivot table to calculate the transition counts.
    transition_counts = pd.pivot_table(ccm4, values='count', index='past_portfolio', columns='ret12_quantile', aggfunc='sum')
    logging.info("Created a pivot table to calculate the transition counts.")

    # Normalize the transition counts
    transition_probs = transition_counts.div(transition_counts.sum(axis=1), axis=0) * 100
    logging.info("Normalized the transition counts.")

    # Create a LaTeX table
    latex_content = [
        "\\begin{table*}[ht!]",
        "\\raggedright",
        "\\refstepcounter{table}",
        "\\label{tab: transition_probs_" + f"{factor}" + "_with_" + str(quantiles) + "_quantiles}",
        "\\textbf{Table \\thetable} \\\\",
        "Transition probabilities for " + f"factor" + " with " + str(quantiles) + " quantiles. \\\\",
        "\\hspace*{1em}" + latex_escape("This sample starts in July 1963, ends in December 2022, and includes all NYSE, AMEX, and NASDAQ common stocks for which we have market equity data for December of year t-1 and June of year t, and book equity data for t-1. The portfolios are constructed on book equity to market equity at the end of each June using quintile breakpoints.  The book equity used in June of year t is the book equity for the last fiscal year end in t-1.  Market equity is calculated at the end of December of year t-1.  More specific definitions can be found in the Appendix.  The data is measured monthly, with all statistics annualized.  1%, 5%, and 10% statistical significance are indicated with ***, **, and *, respectively.") + " \\\\",
        "\\vspace{0.5em}",
        "\\centering",
        "\\begin{adjustbox}{max width=\\textwidth}",
        "\\begin{tabular}{@{}c" + "c" * quantiles + "@{}}",
        "\\toprule",
        "Prior & \\multicolumn{" + str(quantiles) + "}{c}{Current Factor Portfolio} \\\\",
        "Portfolio & " + " & ".join(transition_probs.columns.astype(int).astype(str)) + " \\\\",
        "\\midrule"
    ]

    for index, row in transition_probs.iterrows():
        row_str = str(index) + " & " + " & ".join(row.apply(lambda x: f"{x:.2f}\%")) + " \\\\"
        latex_content.append(row_str)

    latex_content.extend([
        "\\bottomrule",
        "\\end{tabular}",
        "\\end{adjustbox}",
        "\\end{table*}"
    ])

    # Join the content and write it to a file
    latex_content = "\n".join(latex_content)
    file_name = f"back_momentum_skewness/tables/transition_probs_{factor}_returns_with_{quantiles}_quantiles.tex"
    with open(file_name, 'w') as f:
        f.write(latex_content)
    logging.info(f"Saved the LaTeX table to '{file_name}'.")


def create_ff_industry_adjusted_transition_tables(
    quantiles: int,
    factor: str,
    nyse_only: bool = True,
    logging_enabled: bool = True
) -> None:
    """
    Create the industry-adjusted transition tables for the Fama-French factors.

    Args:
        quantiles (int):
            The number of quantiles to use for portfolio formation.
        factor (str):
            The factor to use for the quantile sorts.
        nyse_only (bool):
            Whether to use only NYSE common stocks.
        logging_enabled (bool):
            Whether to enable logging.

    Returns:
        None
    """

    # Set up logging.
    setup_logging(logging_enabled)

    # Read in the csv files.
    ccm_jun = pd.read_csv('data/processed_crsp_jun1.csv', usecols=['BE', 'dec_me', 'EXCHCD', 'me', 'count', 'SHRCD', 'jdate', 'PERMNO', 'MthCalDt', 'OP', 'OP_BE', 'AT_GR1', 'sic'], parse_dates=['jdate'])
    crsp3 = pd.read_csv('data/processed_crsp_data.csv', usecols=['MthCalDt', 'PERMNO', 'SHRCD', 'EXCHCD', 'retadj', 'me', 'wt', 'cumretx', 'ffyear', 'jdate'], parse_dates=['jdate'])
    logging.info("Read in the csv files.")

    # Call the industry function
    assign_industry(ccm_jun, 49)

    # Calculate book to market equity ratio.
    ccm_jun['BE_ME'] = ccm_jun['BE'] * 1000 / ccm_jun['dec_me']
    logging.info("Calculated the book to market equity ratio.")
    
    # Select the universe of common stocks with positive market equity.
    universe = ccm_jun[
        (ccm_jun['me'] > 0) &
        (ccm_jun['count'] >= 1) &
        ((ccm_jun['SHRCD'] == 10) | (ccm_jun['SHRCD'] == 11))
    ]
    logging.info("Selected the universe of stocks.")

    # If nyse_only is True, select only NYSE common stocks.
    if (nyse_only):
        universe = universe[universe['EXCHCD'] == 1]
        logging.info("Selected only NYSE common stocks.")

    logging.info("Removing NaN, inf, and -inf values from the factor column...")
    universe = universe[~universe[factor].isnull()]
    universe = universe[~np.isinf(universe[factor])]
    universe = universe[~np.isneginf(universe[factor])]

    # Calculate industry median factor for each date
    industry_medians = universe.groupby(['jdate', 'industry'])[factor].median().reset_index()
    industry_medians = industry_medians.rename(columns={factor: f'{factor}_industry_median'})

    # Merge industry medians back to the main dataframe
    universe = pd.merge(universe, industry_medians, on=['jdate', 'industry'], how='left')

    # Calculate industry-adjusted factor
    universe[f'{factor}_industry_adjusted'] = universe[factor] / universe[f'{factor}_industry_median']
    logging.info(f"Calculated industry-adjusted {factor}.")

    # Remove NaN, inf, and -inf values from the industry-adjusted factor column
    universe = universe[~universe[f'{factor}_industry_adjusted'].isnull()]
    universe = universe[~np.isinf(universe[f'{factor}_industry_adjusted'])]
    universe = universe[~np.isneginf(universe[f'{factor}_industry_adjusted'])]

    # Get the industry-adjusted factor quantile breakpoints for each month.
    percentiles = [i * 100 / quantiles for i in range(1, quantiles)]
    universe_ff = (
        universe.groupby(['jdate'])[f'{factor}_industry_adjusted']
        .describe(percentiles=[p / 100 for p in percentiles])
        .reset_index()
    )
    percentile_columns = [f'{int(p)}%' for p in percentiles]
    universe_ff = universe_ff[['jdate'] + percentile_columns]
    logging.info(f"Got the industry-adjusted {factor} quantile breakpoints.")

    # Merge the breakpoints with the CCM June data.
    ccm1_jun = pd.merge(universe, universe_ff, how='left', on=['jdate'])
    logging.info("Merged the breakpoints with the CCM June data.")

    # Assign each stock to its proper factor bucket.
    ccm1_jun['factor_portfolio'] = np.where(
        (ccm1_jun['dec_me'] > 0) & (ccm1_jun['me'] > 0) & (ccm1_jun['count'] >= 1),
        ccm1_jun.apply(lambda row: quantile_bucket(row, f'{factor}_industry_adjusted', quantiles), axis=1),
        ''
    )
    logging.info("Assigned each stock to its proper industry-adjusted factor bucket.")

    # Create a 'valid_data' column that is 1 if company has valid June and December market equity data and has been in the dataframe at least once, and 0 otherwise.
    ccm1_jun['valid_data'] = np.where(
        (ccm1_jun['dec_me'] > 0) & (ccm1_jun['me'] > 0) & (ccm1_jun['count'] >= 1),
        1,
        0
    )
    logging.info("Created a 'valid_data' column.")

    # Create a 'non_missing_portfolio' column that is 1 if the stock has been assigned to a portfolio, and 0 otherwise.
    ccm1_jun['non_missing_portfolio'] = np.where(
        (ccm1_jun['factor_portfolio'] != ''),
        1,
        0
    )
    logging.info("Created a 'non_missing_portfolio' column.")

    # Create a new dataframe with only the essential columns for storing the portfolio assignments as of June.
    june = ccm1_jun[['PERMNO', 'MthCalDt', 'jdate', 'factor_portfolio', 'valid_data', 'non_missing_portfolio']].copy()
    logging.info("Created a new dataframe with only the essential columns.")

    # Create a column representing the Fama-French year.
    june['ffyear'] = june['jdate'].dt.year
    logging.info("Created a column representing the Fama-French year.")

    # Merge monthly CRSP data with the portfolio assignments in June.
    ccm3 = pd.merge(crsp3,
                    june[['PERMNO', 'ffyear', 'factor_portfolio', 'valid_data', 'non_missing_portfolio']],
                    how='left', on=['PERMNO', 'ffyear'])
    logging.info("Merged monthly CRSP data with the portfolio assignments in June.")

    # Keep only the common stocks with a positive weight, valid data, and a non-missing portfolio.
    ccm4 = ccm3[(ccm3['wt'] > 0) &
                (ccm3['valid_data'] == 1) &
                (ccm3['non_missing_portfolio'] == 1) &
                ((ccm3['SHRCD'] == 10) | (ccm3['SHRCD'] == 11))]
    logging.info("Kept only the common stocks with a positive weight, valid data, and a non-missing portfolio.")

    # Keep only the essential columns.
    ccm4 = ccm4[['PERMNO', 'jdate', 'retadj', 'me', 'wt', 'factor_portfolio']]
    logging.info("Kept only the essential columns.")

    # Sort the data by date and PERMNO.
    ccm4 = ccm4.sort_values(by=['PERMNO', 'jdate'])
    logging.info("Sorted the data by date and PERMNO.")

    # Create a column for the past factor portfolio assignment.
    ccm4['past_portfolio'] = ccm4.groupby('PERMNO')['factor_portfolio'].shift(12)
    logging.info("Created a column for the past factor portfolio assignment.")

    # Filter out rows with missing current_portfolio or next_portfolio values.
    ccm4 = ccm4.dropna(subset=['factor_portfolio', 'past_portfolio'])
    logging.info("Filtered out rows with missing current_portfolio or past_portfolio values.")

    # Save the data to a csv file.
    ccm4.to_csv(f'back_momentum_skewness/data/processed_ff_transitions_{factor}_industry_adjusted_with_{quantiles}_quantiles.csv', index=False)
    logging.info("Saved the data to a csv file.")


def calculate_ff_industry_adjusted_transition_probabilities(
    quantiles: int,
    factor: str,
    logging_enabled: bool = True
) -> None:
    """
    This function calculates the industry-adjusted transition probabilities between Fama-French factor portfolios.

    Args:
        quantiles (int): The number of quantiles to use for portfolio formation.
        factor (str): The factor to use for the quantile sorts.
        logging_enabled (bool): Whether to enable logging.

    Returns:
        None
    """

    # Set up logging.
    setup_logging(logging_enabled)

    # Read in the csv file.
    ccm4 = pd.read_csv(f'back_momentum_skewness/data/processed_ff_transitions_{factor}_industry_adjusted_with_{quantiles}_quantiles.csv', parse_dates=['jdate'])
    logging.info("Read in the csv file.")

    # Set a date restriction from July 1963 to December 2022.
    ccm4 = ccm4[(ccm4['jdate'] >= '1963-07-01') & (ccm4['jdate'] <= '2022-12-31')]
    logging.info("Set a date restriction.")

    # Create a column to use as values for the pivot table
    ccm4['count'] = 1
    logging.info("Created a column to use as values for the pivot table.")

    # Create a pivot table to calculate the transition counts.
    transition_counts = pd.pivot_table(ccm4, values='count', index='past_portfolio', columns='factor_portfolio', aggfunc='sum')
    logging.info("Created a pivot table to calculate the transition counts.")

    # Normalize the transition counts
    transition_probs = transition_counts.div(transition_counts.sum(axis=1), axis=0) * 100
    logging.info("Normalized the transition counts.")

    # Create a LaTeX table
    latex_content = [
        "\\begin{table*}[ht!]",
        "\\raggedright",
        "\\refstepcounter{table}",
        "\\label{tab: transition_probs_" + f"{factor}" + "industry_adjusted_with_" + str(quantiles) + "_quantiles}",
        "\\textbf{Table \\thetable} \\\\",
        "Transition probabilities for " + f"factor" + " with " + str(quantiles) + " quantiles. \\\\",
        "\\hspace*{1em}" + latex_escape("This sample starts in July 1963, ends in December 2022, and includes all NYSE, AMEX, and NASDAQ common stocks for which we have market equity data for December of year t-1 and June of year t, and book equity data for t-1. The portfolios are constructed on book equity to market equity at the end of each June using quintile breakpoints.  The book equity used in June of year t is the book equity for the last fiscal year end in t-1.  Market equity is calculated at the end of December of year t-1.  More specific definitions can be found in the Appendix.  The data is measured monthly, with all statistics annualized.  1%, 5%, and 10% statistical significance are indicated with ***, **, and *, respectively.") + " \\\\",
        "\\vspace{0.5em}",
        "\\centering",
        "\\begin{adjustbox}{max width=\\textwidth}",
        "\\begin{tabular}{@{}c" + "c" * quantiles + "@{}}",
        "\\toprule",
        "Prior & \\multicolumn{" + str(quantiles) + "}{c}{Current Factor Portfolio} \\\\",
        "Portfolio & " + " & ".join(transition_probs.columns.astype(str)) + " \\\\",
        "\\midrule"
    ]

    for index, row in transition_probs.iterrows():
        row_str = str(index) + " & " + " & ".join(row.apply(lambda x: f"{x:.2f}\%")) + " \\\\"
        latex_content.append(row_str)

    latex_content.extend([
        "\\bottomrule",
        "\\end{tabular}",
        "\\end{adjustbox}",
        "\\end{table*}"
    ])
    logging.info("Added the table footer to the LaTeX table.")

    # Join the content and write it to a file
    latex_content = "\n".join(latex_content)
    file_name = f"back_momentum_skewness/tables/transition_probs_{factor}_industy_adjusted_with_{quantiles}_quantiles.tex"
    with open(file_name, 'w') as f:
        f.write(latex_content)
    logging.info(f"Saved the LaTeX table to '{file_name}'.")


def create_industry_specific_transition_tables(
    quantiles: int,
    factor: str,
    nyse_only: bool = True,
    logging_enabled: bool = True
) -> None:
    """
    Create industry-specific transition tables for the Fama-French factors.

    Args:
        quantiles (int): The number of quantiles to use for portfolio formation.
        factor (str): The factor to use for the quantile sorts.
        nyse_only (bool): Whether to use only NYSE common stocks.
        logging_enabled (bool): Whether to enable logging.

    Returns:
        None
    """

    # Set up logging
    setup_logging(logging_enabled)

    # Read in the csv files
    ccm_jun = pd.read_csv('data/processed_crsp_jun1.csv', usecols=['BE', 'dec_me', 'EXCHCD', 'me', 'count', 'SHRCD', 'jdate', 'PERMNO', 'MthCalDt', 'OP', 'OP_BE', 'AT_GR1', 'sic'], parse_dates=['jdate'])
    crsp3 = pd.read_csv('data/processed_crsp_data.csv', usecols=['MthCalDt', 'PERMNO', 'SHRCD', 'EXCHCD', 'retadj', 'me', 'wt', 'cumretx', 'ffyear', 'jdate'], parse_dates=['jdate'])
    logging.info("Read in the csv files.")

    # Assign industry
    assign_industry(ccm_jun, 49)

    # Calculate book to market equity ratio
    ccm_jun['BE_ME'] = ccm_jun['BE'] * 1000 / ccm_jun['dec_me']
    
    # Select the universe of common stocks with positive market equity
    universe = ccm_jun[
        (ccm_jun['me'] > 0) &
        (ccm_jun['count'] >= 1) &
        ((ccm_jun['SHRCD'] == 10) | (ccm_jun['SHRCD'] == 11))
    ]

    if nyse_only:
        universe = universe[universe['EXCHCD'] == 1]

    # Remove NaN, inf, and -inf values from the factor column
    universe = universe[~universe[factor].isnull() & ~np.isinf(universe[factor])]

    # Get list of all industries
    industries = universe['industry'].unique().tolist()

    for industry in industries:
        logging.info(f"Processing industry: {industry}")
        
        # Filter data for the current industry
        industry_data = universe[universe['industry'] == industry]

        # Calculate factor quantiles for the industry
        percentiles = [i * 100 / quantiles for i in range(1, quantiles)]
        industry_quantiles = (
            industry_data.groupby(['jdate'])[factor]
            .describe(percentiles=[p / 100 for p in percentiles])
            .reset_index()
        )
        percentile_columns = [f'{int(p)}%' for p in percentiles]
        industry_quantiles = industry_quantiles[['jdate'] + percentile_columns]

        # Merge quantiles with industry data
        industry_data = pd.merge(industry_data, industry_quantiles, how='left', on=['jdate'])

        # Assign each stock to its proper factor bucket
        industry_data['factor_portfolio'] = industry_data.apply(
            lambda row: quantile_bucket(row, factor, quantiles), axis=1
        )

        # Create 'valid_data' and 'non_missing_portfolio' columns
        industry_data['valid_data'] = np.where(
            (industry_data['dec_me'] > 0) & (industry_data['me'] > 0) & (industry_data['count'] >= 1),
            1, 0
        )
        industry_data['non_missing_portfolio'] = np.where(
            (industry_data['factor_portfolio'] != ''), 1, 0
        )

        # Prepare data for merging with CRSP data
        june_data = industry_data[['PERMNO', 'MthCalDt', 'jdate', 'factor_portfolio', 'valid_data', 'non_missing_portfolio']].copy()
        june_data['ffyear'] = june_data['jdate'].dt.year

        # Merge with CRSP data
        industry_crsp = pd.merge(
            crsp3,
            june_data[['PERMNO', 'ffyear', 'factor_portfolio', 'valid_data', 'non_missing_portfolio']],
            how='left', on=['PERMNO', 'ffyear']
        )

        # Filter and prepare final dataset
        industry_final = industry_crsp[
            (industry_crsp['wt'] > 0) &
            (industry_crsp['valid_data'] == 1) &
            (industry_crsp['non_missing_portfolio'] == 1) &
            ((industry_crsp['SHRCD'] == 10) | (industry_crsp['SHRCD'] == 11))
        ][['PERMNO', 'jdate', 'retadj', 'me', 'wt', 'factor_portfolio']]

        industry_final = industry_final.sort_values(by=['PERMNO', 'jdate'])
        industry_final['past_portfolio'] = industry_final.groupby('PERMNO')['factor_portfolio'].shift(12)
        industry_final = industry_final.dropna(subset=['factor_portfolio', 'past_portfolio'])

        # Calculate transition probabilities
        industry_final['count'] = 1
        transition_counts = pd.pivot_table(
            industry_final, values='count', index='past_portfolio', 
            columns='factor_portfolio', aggfunc='sum'
        )
        transition_probs = transition_counts.div(transition_counts.sum(axis=1), axis=0) * 100

        # Create a LaTeX table
        latex_content = [
            "\\begin{table*}[ht!]",
            "\\raggedright",
            "\\refstepcounter{table}",
            f"\\label{{tab: transition_probs_{factor}_{industry}_with_{quantiles}_quantiles}}",
            "\\textbf{Table \\thetable} \\\\",
            f"Transition probabilities for {factor} with {quantiles} quantiles in the {industry} industry. \\\\",
            "\\hspace*{1em}" + latex_escape("This sample starts in July 1963, ends in December 2022, and includes all NYSE, AMEX, and NASDAQ common stocks for which we have market equity data for December of year t-1 and June of year t, and book equity data for t-1. The portfolios are constructed on book equity to market equity at the end of each June using quintile breakpoints.  The book equity used in June of year t is the book equity for the last fiscal year end in t-1.  Market equity is calculated at the end of December of year t-1.  More specific definitions can be found in the Appendix.  The data is measured monthly, with all statistics annualized.  1%, 5%, and 10% statistical significance are indicated with ***, **, and *, respectively.") + " \\\\",
            "\\vspace{0.5em}",
            "\\centering",
            "\\begin{adjustbox}{max width=\\textwidth}",
            "\\begin{tabular}{@{}c" + "c" * quantiles + "@{}}",
            "\\toprule",
            "Prior & \\multicolumn{" + str(quantiles) + "}{c}{Current Factor Portfolio} \\\\",
            "Portfolio & " + " & ".join(transition_probs.columns.astype(str)) + " \\\\",
            "\\midrule"
        ]

        for index, row in transition_probs.iterrows():
            row_str = str(index) + " & " + " & ".join(row.apply(lambda x: f"{x:.2f}\%")) + " \\\\"
            latex_content.append(row_str)

        latex_content.extend([
            "\\bottomrule",
            "\\end{tabular}",
            "\\end{adjustbox}",
            "\\end{table*}"
        ])

        # Join the content and write it to a file
        latex_content = "\n".join(latex_content)
        file_name = f"back_momentum_skewness/tables/transition_probs_{factor}_{industry}_with_{quantiles}_quantiles.tex"
        with open(file_name, 'w') as f:
            f.write(latex_content)
        logging.info(f"Saved the LaTeX table to '{file_name}'.")


