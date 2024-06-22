import logging
import re
import pandas as pd
import numpy as np
from pandas.tseries.offsets import MonthEnd
import statsmodels.api as sm

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
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    else:
        logging.disable(logging.CRITICAL)


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


def quantile_bucket(row: pd.Series,factor: str, quantiles: int) -> str:
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


def wavg(group: pd.DataFrame, avg_name: str, weight_name: str) -> float:
    """
    Calculate the value-weighted returns.

    Args:
        group (pd.DataFrame):
            The group to calculate the value-weighted returns for.
        avg_name (str):
            The name of the average column.
        weight_name (str):
            The name of the weight column.

    Returns:
        float: The value-weighted return.
    """
    average_column = group[avg_name]
    weight_column = group[weight_name]
    try:
        return (average_column * weight_column).sum() / weight_column.sum()
    except ZeroDivisionError:
        return np.nan
    

def add_significance_stars(value: float, t_stat: float) -> str:
    """
    Add significance stars to the value based on the t-statistic.

    Args:
        value (float):
            The value to add significance stars to.
        t_stat (float):
            The t-statistic to determine the number of significance stars.
    
    Returns:
        str: The value with significance stars added.
    """
    if abs(t_stat) >= 2.58:
        return f'{value:.2f}%***'
    elif abs(t_stat) >= 1.96:
        return f'{value:.2f}%**'
    elif abs(t_stat) >= 1.64:
        return f'{value:.2f}%*'
    else:
        return f'{value:.2f}%'


def perform_ff_quantile_sorts(quantiles: int, 
                              factor: str, 
                              nyse_only: bool = True, 
                              sign: int = 1, 
                              logging_enabled: bool = True) -> None:
    """
    Perform quantile sorts on the Fama-French factors.

    Args:
        quantiles (int):
            The number of quantiles to use for portfolio formation.
        factor (str):
            The factor to use for the quantile sorts.
        nyse_only (bool):
            Whether to use only NYSE common stocks.
        sign (int):
            The sign of the factor (1 for positive, -1 for negative).
        logging_enabled (bool):
            Whether to enable logging.

    Returns:
        None
    """

    # Set up logging.
    setup_logging(logging_enabled)

    logging.info("Reading in the csv files...")
    ccm_jun = pd.read_csv('data/processed_crsp_jun1.csv', usecols=['BE', 'dec_me', 'EXCHCD', 'me', 'count', 'SHRCD', 'jdate', 'PERMNO', 'MthCalDt', 'OP', 'OP_BE', 'AT_GR1'], parse_dates=['jdate'])
    crsp3 = pd.read_csv('data/processed_crsp_data.csv', usecols=['MthCalDt', 'PERMNO', 'SHRCD', 'EXCHCD', 'retadj', 'me', 'wt', 'cumretx', 'ffyear', 'jdate'], parse_dates=['jdate'])

    logging.info("Calculating the book to market equity ratio...")
    ccm_jun['BE_ME'] = ccm_jun['BE'] * 1000 / ccm_jun['dec_me']

    # get the rank of me where the smallest me gets the highest rank
    logging.info("Calculating the rank of market equity...")
    ccm_jun['rank_me'] = ccm_jun.groupby('jdate')['me'].rank(ascending=False)

    # get the rank of BE_ME where the smallest BE_ME gets the lowest rank
    logging.info("Calculating the rank of the book to market equity ratio...")
    ccm_jun['rank_BE_ME'] = ccm_jun.groupby('jdate')['BE_ME'].rank()

    # get the rank of OP_BE where the smallest OP_BE gets the lowest rank
    logging.info("Calculating the rank of the operating profit to book equity ratio...")
    ccm_jun['rank_OP_BE'] = ccm_jun.groupby('jdate')['OP_BE'].rank()

    # get the rank of AT_GR1 where the smallest AT_GR1 gets the highest rank
    logging.info("Calculating the rank of the asset growth rate...")
    ccm_jun['rank_AT_GR1'] = ccm_jun.groupby('jdate')['AT_GR1'].rank(ascending=False)

    # add the ranks together to get the multi_rank
    logging.info("Calculating the multi-factor rank...")
    ccm_jun['multi_rank'] = ccm_jun['rank_BE_ME'] + ccm_jun['rank_OP_BE'] + ccm_jun['rank_AT_GR1'] + ccm_jun['rank_me']

    logging.info("Selecting the universe of stocks...")
    universe = ccm_jun[
        (ccm_jun['me'] > 0) &
        (ccm_jun['count'] >= 1) &
        ((ccm_jun['SHRCD'] == 10) | (ccm_jun['SHRCD'] == 11))
    ]

    # Filter the universe to include only NYSE common stocks if specified.
    if nyse_only:
        universe = universe[universe['EXCHCD'] == 1]

    logging.info("Removing NaN, inf, and -inf values from the factor column...")
    universe = universe[~universe[factor].isnull()]
    universe = universe[~np.isinf(universe[factor])]
    universe = universe[~np.isneginf(universe[factor])]

    logging.info(f"Calculating the {factor} quantile breakpoints...")
    percentiles = [i * 100 / quantiles for i in range(1, quantiles)]
    universe_ff = (
        universe.groupby(['jdate'])[factor]
        .describe(percentiles=[p / 100 for p in percentiles])
        .reset_index()
    )
    percentile_columns = [f'{int(p)}%' for p in percentiles]
    universe_ff = universe_ff[['jdate'] + percentile_columns]

    logging.info("Merging the breakpoints with the CCM June data...")
    ccm1_jun = pd.merge(ccm_jun, universe_ff, how='left', on=['jdate'])

    logging.info("Assigning each stock to its proper book to market bucket...")
    ccm1_jun['factor_portfolio'] = np.where(
        (ccm_jun['dec_me'] > 0) & (ccm1_jun['me'] > 0) & (ccm1_jun['count'] >= 1),
        ccm1_jun.apply(lambda row: quantile_bucket(row, factor, quantiles), axis=1),
        ''
    )

    logging.info("Creating a 'valid_data' column...")
    ccm1_jun['valid_data'] = np.where(
        (ccm_jun['dec_me'] > 0) & (ccm1_jun['me'] > 0) & (ccm1_jun['count'] >= 1),
        1,
        0
    )

    logging.info("Creating a 'non_missing_portfolio' column...")
    ccm1_jun['non_missing_portfolio'] = np.where(
        (ccm1_jun['factor_portfolio'] != ''),
        1,
        0
    )

    logging.info("Creating a new dataframe with only the essential columns...")
    june = ccm1_jun[['PERMNO', 'MthCalDt', 'jdate', 'factor_portfolio', 'valid_data', 'non_missing_portfolio']].copy()

    logging.info("Creating a column representing the Fama-French year...")
    june['ffyear'] = june['jdate'].dt.year

    logging.info("Merging the monthly CRSP data with the portfolio assignments in June...")
    ccm3 = pd.merge(crsp3,
                    june[['PERMNO', 'ffyear', 'factor_portfolio', 'valid_data', 'non_missing_portfolio']],
                    how='left', on=['PERMNO', 'ffyear'])

    logging.info("Keeping only the common stocks with a positive weight, valid data, and a non-missing portfolio...")
    ccm4 = ccm3[(ccm3['wt'] > 0) &
                (ccm3['valid_data'] == 1) &
                (ccm3['non_missing_portfolio'] == 1) &
                ((ccm3['SHRCD'] == 10) | (ccm3['SHRCD'] == 11))]

    logging.info("Creating a dataframe for the value-weighted returns...")
    vwret = ccm4.groupby(['jdate', 'factor_portfolio']).apply(wavg, 'retadj', 'wt').to_frame().reset_index().rename(columns={0: 'vwret'})

    logging.info("Transposing the dataframes...")
    ff_factors = vwret.pivot(index='jdate', columns=['factor_portfolio'], values='vwret').reset_index()

    logging.info("Calculating the difference in returns between the high and low factor portfolios...")
    low_portfolio = '1' if sign == 1 else str(quantiles)
    high_portfolio = str(quantiles) if sign == 1 else '1'
    ff_factors['H-L'] = (ff_factors[high_portfolio] - ff_factors[low_portfolio])

    logging.info("Renaming the jdate column to date...")
    ff_factors = ff_factors.rename(columns={'jdate': 'date'})

    logging.info("Setting a date restriction...")
    ff_factors63 = ff_factors[
        (ff_factors['date'] >= '1963-07-01') &
        (ff_factors['date'] <= '2022-12-31')
    ]

    logging.info("Saving the dataframe to a CSV file...")
    filename = (
        f'back_momentum_skewness/data/processed_ff_'
        f'{factor}_with_{quantiles}_quantiles.csv'
    )
    ff_factors63.to_csv(filename, index=False)

    logging.info("Reading in the risk-free rate and market return data...")
    ff = pd.read_csv('data/raw_factors.csv')
    ff['date'] = pd.to_datetime(ff['date'], format='%Y%m') + MonthEnd(0)
    ff = ff[ff['date'] >= ff_factors63['date'].min()]
    ff = ff[ff['date'] <= ff_factors63['date'].max()]

    logging.info("Merging the data and risk-free rate/market return data...")
    merged_data = pd.merge(ff_factors63, ff[['date', 'RF', 'Mkt-RF']], on='date', how='inner')

    logging.info("Initializing an empty list to store dictionaries...")
    stats_list = []

    # Iterate over the factor portfolios (including H-L) to calculate the statistics.
    logging.info("Calculating the statistics for each factor portfolio...")
    for column in merged_data.columns[1:-2]:

        # Calculate the total returns (without subtracting the risk-free rate).
        total_returns = merged_data[column]

        # Calculate the mean, standard deviation, and number of observations for total returns.
        total_mean = total_returns.mean()
        total_std_dev = total_returns.std()
        n = len(total_returns)

        # Calculate the t-statistic for total returns.
        total_t_stat = total_mean / (total_std_dev / (n ** 0.5))

        # Subtract the risk-free rate from all the portfolios except H-L.
        if column == 'H-L':
            excess_returns = merged_data[column]
        else:
            excess_returns = merged_data[column] - (merged_data['RF'] / 100)

        # Calculate the mean and standard deviation of the excess returns.
        excess_mean = excess_returns.mean()
        excess_std_dev = excess_returns.std()

        # Calculate the t-statistic.
        t_stat = excess_mean / (excess_std_dev / (n ** 0.5))

        # Fit the CAPM model and calculate alpha, alpha t-statistic, and beta.
        X = sm.add_constant(merged_data['Mkt-RF'])
        model = sm.OLS(excess_returns, X).fit()
        alpha = model.params.iloc[0]
        alpha_t_stat = model.tvalues.iloc[0]
        beta = model.params.iloc[1]

        # Calculate the skewness, kurtosis, and Sharpe ratio.
        skew = excess_returns.skew()
        kurtosis = excess_returns.kurtosis()
        sharpe_ratio = excess_mean / excess_std_dev

        # Calculate the tracking error (standard deviation of the residuals).
        residuals = model.resid
        tracking_error = residuals.std()

        # Calculate Jensen's alpha (already calculated as `alpha`).
        jensens_alpha = alpha

        # Calculate the Appraisal Ratio.
        appraisal_ratio = jensens_alpha / tracking_error

        # Annualize the statistics using compound returns.
        total_mean = (1 + total_mean) ** 12 - 1
        excess_mean = (1 + excess_mean) ** 12 - 1
        excess_std_dev = excess_std_dev * (12 ** 0.5)
        sharpe_ratio = excess_mean / excess_std_dev
        jensens_alpha = (1 + jensens_alpha) ** 12 - 1
        tracking_error = tracking_error * (12 ** 0.5)
        appraisal_ratio = appraisal_ratio * (12 ** 0.5)

        # Append the statistics as a dictionary to the list
        stats_list.append({
            'Portfolio': column,
            'Total Return': add_significance_stars(total_mean * 100, total_t_stat),
            'Total t-stat': f"[{total_t_stat:.2f}]",
            'Excess Return': add_significance_stars(excess_mean * 100, t_stat),
            'Excess t-stat': f"[{t_stat:.2f}]",
            'Volatility': f"{excess_std_dev * 100:.2f}%",
            'Skew': f"{skew:.2f}",
            'Kurtosis': f"{kurtosis:.2f}",
            'Sharpe Ratio': f"{sharpe_ratio:.2f}",
            'CAPM Alpha': add_significance_stars(jensens_alpha * 100, alpha_t_stat),
            'Alpha t-stat': f"[{alpha_t_stat:.2f}]",
            'Market Beta': f"{beta * 100:.2f}",
            'Tracking Error': f"{tracking_error * 100:.2f}%",
            'Appraisal Ratio': f"{appraisal_ratio:.2f}"
        })

    logging.info("Creating a copy of the CRSP data to calculate market cap percentage...")
    market_cap_data = ccm4.copy()

    logging.info("Calculating the total market cap for each date...")
    market_cap_data['total_market_cap'] = market_cap_data.groupby('jdate')['wt'].transform('sum')

    logging.info("Calculating the portfolio market cap for each date and factor portfolio...")
    market_cap_data['portfolio_market_cap'] = market_cap_data.groupby(['jdate', 'factor_portfolio'])['wt'].transform('sum')

    logging.info("Calculating the market cap percentage for each portfolio...")
    market_cap_data['market_cap_percentage'] = market_cap_data['portfolio_market_cap'] / market_cap_data['total_market_cap']

    logging.info("Integrating market cap into stats list...")
    for portfolio in stats_list:
        if portfolio['Portfolio'] != 'H-L':
            avg_market_cap_percentage = market_cap_data.loc[market_cap_data['factor_portfolio'] == portfolio['Portfolio'], 'market_cap_percentage'].mean()
            portfolio['Total Capitalization'] = f"{avg_market_cap_percentage * 100:.2f}%"
        else:
            portfolio['Total Capitalization'] = ""

    logging.info("Creating the DataFrame from the list of dictionaries...")
    stats_df = pd.DataFrame(stats_list)

    logging.info("Transposing the DataFrame...")
    stats_df = stats_df.set_index('Portfolio').transpose()

    logging.info("Reordering the columns...")
    columns = [str(i) for i in range(1, quantiles + 1)] + ['H-L']
    stats_df = stats_df.reindex(columns, axis=1)
    column_names = [str(i) for i in range(1, quantiles + 1)] + ['H-L']
    column_names[0] = 'Low'
    column_names[-2] = 'High'
    column_names[-1] = 'High-Low' if sign == 1 else 'Low-High'

    logging.info("Creating the LaTeX table preamble...")
    latex_content = [
        "\\begin{table*}[ht!]",
        "\\raggedright",
        "\\refstepcounter{table}",
        "\\label{tab: quantile_sort" + factor + "_with_" + str(quantiles) + "_quantiles}",
        "\\textbf{Table \\thetable} \\\\",
        "Portfolio sorts on " + latex_escape(factor) + " with " + str(quantiles) + " quantiles. \\\\",
        "\\hspace*{1em}" + latex_escape("This sample starts in July 1963, ends in December 2022, and includes all NYSE, AMEX, and NASDAQ common stocks for which we have market equity data for December of year t-1 and June of year t, and book equity data for t-1. The portfolios are constructed on book equity to market equity at the end of each June using quintile breakpoints.  The book equity used in June of year t is the book equity for the last fiscal year end in t-1.  Market equity is calculated at the end of December of year t-1.  More specific definitions can be found in the Appendix.  The data is measured monthly, with all statistics annualized.  1%, 5%, and 10% statistical significance are indicated with ***, **, and *, respectively.") + " \\\\",
        "\\vspace{0.5em}",
        "\\centering",
        "\\begin{adjustbox}{max width=\\textwidth}",
        "\\begin{tabular}{@{}l" + "c" * len(stats_df.columns) + "@{}}",
        "\\toprule",
        " & " + " & ".join(latex_escape(name) for name in column_names) + " \\\\",
        "\\midrule"
    ]

    logging.info("Adding the rows to the LaTeX table...")
    for index, row in stats_df.iterrows():
        if index in ["Excess t-stat", "Alpha t-stat", "Total t-stat"]:
            row_str = " & " + " & ".join(row) + " \\\\"
        else:
            row_str = latex_escape(index) + " & " + " & ".join(latex_escape(str(cell)) for cell in row) + " \\\\"
        latex_content.append(row_str)

    logging.info("Adding the table footer to the LaTeX table...")
    latex_content.extend([
        "\\bottomrule",
        "\\end{tabular}",
        "\\end{adjustbox}",
        "\\end{table*}"
    ])

    logging.info("Joining the content and writing it to a file...")
    latex_content = "\n".join(latex_content)
    with open(f'back_momentum_skewness/tables/quantile_sorts_{factor}_with_{quantiles}_quantiles.tex', 'w') as f:
        f.write(latex_content)


def perform_mom_quantile_sorts(quantiles: int,
                               lookback_period: int,
                               lag: int,
                               nyse_only: bool = True,
                               sign: int = 1,
                               logging_enabled: bool = True) -> None:
    """
    Perform quantile sorts on the momentum portfolios.

    Args:
        quantiles (int):
            The number of quantiles to use for portfolio formation.
        lookback_period (int):
            The number of months to look back for momentum calculation.
        lag (int):
            The number of months to lag the momentum calculation.
        nyse_only (bool):
            Whether to use only NYSE common stocks.
        sign (int):
            The sign of the factor (1 for positive, -1 for negative).
        logging_enabled (bool):
            Whether to enable logging.

    Returns:
        None
    """

    # Set up logging.
    setup_logging(logging_enabled)

    logging.info("Reading in the csv files...")
    crsp3 = pd.read_csv('data/processed_crsp_data.csv', usecols=['PERMNO', 'retadj', 'jdate', 'me', 'wt', 'SHRCD', 'EXCHCD', 'count'], parse_dates=['jdate'])

    logging.info("Calculating the momentum factor...")
    crsp3['MOMENTUM'] = crsp3.groupby('PERMNO')['retadj'].apply(lambda x: x.shift(lag + 1).rolling(window=lookback_period - lag, min_periods=lookback_period - lag).mean()).reset_index(level=0, drop=True)

    logging.info("Selecting the universe of stocks...")
    universe = crsp3[
        (crsp3['me'] > 0) &
        (crsp3['count'] >= 1) &
        ((crsp3['SHRCD'] == 10) | (crsp3['SHRCD'] == 11))
    ]

    # Filter the universe to include only NYSE common stocks if specified.
    if nyse_only:
        universe = universe[universe['EXCHCD'] == 1]

    logging.info("Removing NaN, inf, and -inf values from the momentum column...")
    universe = universe[~universe['MOMENTUM'].isnull()]
    universe = universe[~np.isinf(universe['MOMENTUM'])]
    universe = universe[~np.isneginf(universe['MOMENTUM'])]

    logging.info(f"Calculating the momentum quantile breakpoints...")
    percentiles = [i * 100 / quantiles for i in range(1, quantiles)]
    universe_mom = (
        universe.groupby(['jdate'])['MOMENTUM']
        .describe(percentiles=[p / 100 for p in percentiles])
        .reset_index()
    )
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
    
    logging.info("Dropping the columns that are no longer needed...")
    crsp5 = crsp5[['PERMNO', 'jdate', 'retadj', 'me', 'wt', 'MOMENTUM', 'factor_portfolio']]
    crsp5 = crsp5.dropna(subset=['MOMENTUM'])

    logging.info("Creating a dataframe for the value-weighted returns...")
    vwret = crsp5.groupby(['jdate', 'factor_portfolio']).apply(wavg, 'retadj', 'wt').to_frame().reset_index().rename(columns={0: 'vwret'})

    logging.info("Transposing the dataframes...")
    mom_factors = vwret.pivot(index='jdate', columns=['factor_portfolio'], values='vwret').reset_index()

    logging.info("Calculating the difference in returns between the high and low factor portfolios...")
    low_portfolio = '1' if sign == 1 else str(quantiles)
    high_portfolio = str(quantiles) if sign == 1 else '1'
    mom_factors['H-L'] = (mom_factors[high_portfolio] - mom_factors[low_portfolio])

    logging.info("Renaming the jdate column to date...")
    mom_factors = mom_factors.rename(columns={'jdate': 'date'})

    logging.info("Setting a date restriction...")
    mom_factors63 = mom_factors[
        (mom_factors['date'] >= '1963-07-01') &
        (mom_factors['date'] <= '2022-12-31')
    ]

    logging.info("Saving the dataframe to a CSV file...")
    filename = (
        f'back_momentum_skewness/data/processed_mom_'
        f'[{lookback_period}_{lag}]_with_{quantiles}_quantiles.csv'
    )
    mom_factors63.to_csv(filename, index=False)

    logging.info("Reading in the risk-free rate and market return data...")
    ff = pd.read_csv('data/raw_factors.csv')
    ff['date'] = pd.to_datetime(ff['date'], format='%Y%m') + MonthEnd(0)
    ff = ff[ff['date'] >= mom_factors63['date'].min()]
    ff = ff[ff['date'] <= mom_factors63['date'].max()]

    logging.info("Merging the data and risk-free rate/market return data...")
    merged_data = pd.merge(mom_factors63, ff[['date', 'RF', 'Mkt-RF']], on='date', how='inner')

    logging.info("Initializing an empty list to store dictionaries...")
    stats_list = []

    # Iterate over the factor portfolios (including H-L) to calculate the statistics.
    logging.info("Calculating the statistics for each factor portfolio...")
    for column in merged_data.columns[1:-2]:

        # Calculate the total returns (without subtracting the risk-free rate).
        total_returns = merged_data[column]

        # Calculate the mean, standard deviation, and number of observations for total returns.
        total_mean = total_returns.mean()
        total_std_dev = total_returns.std()
        n = len(total_returns)

        # Calculate the t-statistic for total returns.
        total_t_stat = total_mean / (total_std_dev / (n ** 0.5))

        # Subtract the risk-free rate from all the portfolios except H-L.
        if column == 'H-L':
            excess_returns = merged_data[column]
        else:
            excess_returns = merged_data[column] - (merged_data['RF'] / 100)

        # Calculate the mean and standard deviation of the excess returns.
        excess_mean = excess_returns.mean()
        excess_std_dev = excess_returns.std()

        # Calculate the t-statistic.
        t_stat = excess_mean / (excess_std_dev / (n ** 0.5))

        # Fit the CAPM model and calculate alpha, alpha t-statistic, and beta.
        X = sm.add_constant(merged_data['Mkt-RF'])
        model = sm.OLS(excess_returns, X).fit()
        alpha = model.params.iloc[0]
        alpha_t_stat = model.tvalues.iloc[0]
        beta = model.params.iloc[1]

        # Calculate the skewness, kurtosis, and Sharpe ratio.
        skew = excess_returns.skew()
        kurtosis = excess_returns.kurtosis()
        sharpe_ratio = excess_mean / excess_std_dev

        # Calculate the tracking error (standard deviation of the residuals).
        residuals = model.resid
        tracking_error = residuals.std()

        # Calculate Jensen's alpha (already calculated as `alpha`).
        jensens_alpha = alpha

        # Calculate the Appraisal Ratio.
        appraisal_ratio = jensens_alpha / tracking_error

        # Annualize the statistics using compound returns.
        total_mean = (1 + total_mean) ** 12 - 1
        excess_mean = (1 + excess_mean) ** 12 - 1
        excess_std_dev = excess_std_dev * (12 ** 0.5)
        sharpe_ratio = excess_mean / excess_std_dev
        jensens_alpha = (1 + jensens_alpha) ** 12 - 1
        tracking_error = tracking_error * (12 ** 0.5)
        appraisal_ratio = jensens_alpha / tracking_error

        # Append the statistics as a dictionary to the list
        stats_list.append({
            'Portfolio': column,
            'Total Return': add_significance_stars(total_mean * 100, total_t_stat),
            'Total t-stat': f"[{total_t_stat:.2f}]",
            'Excess Return': add_significance_stars(excess_mean * 100, t_stat),
            'Excess t-stat': f"[{t_stat:.2f}]",
            'Volatility': f"{excess_std_dev * 100:.2f}%",
            'Skew': f"{skew:.2f}",
            'Kurtosis': f"{kurtosis:.2f}",
            'Sharpe Ratio': f"{sharpe_ratio:.2f}",
            'CAPM Alpha': add_significance_stars(jensens_alpha * 100, alpha_t_stat),
            'Alpha t-stat': f"[{alpha_t_stat:.2f}]",
            'Market Beta': f"{beta * 100:.2f}",
            'Tracking Error': f"{tracking_error * 100:.2f}%",
            'Appraisal Ratio': f"{appraisal_ratio:.2f}"
        })

    logging.info("Creating a copy of the CRSP data to calculate market cap percentage...")
    market_cap_data = crsp5.copy()

    logging.info("Calculating the total market cap for each date...")
    market_cap_data['total_market_cap'] = market_cap_data.groupby('jdate')['wt'].transform('sum')

    logging.info("Calculating the portfolio market cap for each date and factor portfolio...")
    market_cap_data['portfolio_market_cap'] = market_cap_data.groupby(['jdate', 'factor_portfolio'])['wt'].transform('sum')

    logging.info("Calculating the market cap percentage for each portfolio...")
    market_cap_data['market_cap_percentage'] = market_cap_data['portfolio_market_cap'] / market_cap_data['total_market_cap']

    logging.info("Integrating market cap into stats list...")
    for portfolio in stats_list:
        if portfolio['Portfolio'] != 'H-L':
            avg_market_cap_percentage = market_cap_data.loc[market_cap_data['factor_portfolio'] == portfolio['Portfolio'], 'market_cap_percentage'].mean()
            portfolio['Total Capitalization'] = f"{avg_market_cap_percentage * 100:.2f}%"
        else:
            portfolio['Total Capitalization'] = ""

    logging.info("Creating the DataFrame from the list of dictionaries...")
    stats_df = pd.DataFrame(stats_list)

    logging.info("Transposing the DataFrame...")
    stats_df = stats_df.set_index('Portfolio').transpose()

    logging.info("Reordering the columns...")
    columns = [str(i) for i in range(1, quantiles + 1)] + ['H-L']
    stats_df = stats_df.reindex(columns, axis=1)
    column_names = [str(i) for i in range(1, quantiles + 1)] + ['H-L']
    column_names[0] = 'Low'
    column_names[-2] = 'High'
    column_names[-1] = 'High-Low' if sign == 1 else 'Low-High'

    logging.info("Creating the LaTeX table preamble...")
    latex_content = [
        "\\begin{table*}[ht!]",
        "\\raggedright",
        "\\refstepcounter{table}",
        "\\label{tab: quantile_sort_mom_" + f"[{lookback_period}_{lag}]" + "_with_" + str(quantiles) + "_quantiles}",
        "\\textbf{Table \\thetable} \\\\",
        "Portfolio sorts on " + latex_escape(f"[{lookback_period}_{lag}]") + " momentum with " + str(quantiles) + " quantiles. \\\\",
        "\\hspace*{1em}" + latex_escape("This sample starts in July 1963, ends in December 2022, and includes all NYSE, AMEX, and NASDAQ common stocks for which we have market equity data for December of year t-1 and June of year t, and book equity data for t-1. The portfolios are constructed on momentum calculated over the last 12 months, skipping the most recent month. The momentum is calculated as the average of the past 12 months' returns, excluding the most recent month. The data is measured monthly, with all statistics annualized.  1%, 5%, and 10% statistical significance are indicated with ***, **, and *, respectively.") + " \\\\",
        "\\vspace{0.5em}",
        "\\centering",
        "\\begin{adjustbox}{max width=\\textwidth}",
        "\\begin{tabular}{@{}l" + "c" * len(stats_df.columns) + "@{}}",
        "\\toprule",
        " & " + " & ".join(latex_escape(name) for name in column_names) + " \\\\",
        "\\midrule"
    ]

    logging.info("Adding the rows to the LaTeX table...")
    for index, row in stats_df.iterrows():
        if index in ["Excess t-stat", "Alpha t-stat", "Total t-stat"]:
            row_str = " & " + " & ".join(row) + " \\\\"
        else:
            row_str = latex_escape(index) + " & " + " & ".join(latex_escape(str(cell)) for cell in row) + " \\\\"
        latex_content.append(row_str)

    logging.info("Adding the table footer to the LaTeX table...")
    latex_content.extend([
        "\\bottomrule",
        "\\end{tabular}",
        "\\end{adjustbox}",
        "\\end{table*}"
    ])

    logging.info("Joining the content and writing it to a file...")
    latex_content = "\n".join(latex_content)
    with open(f'back_momentum_skewness/tables/quantile_sorts_mom_[{lookback_period}_{lag}]_with_{quantiles}_quantiles.tex', 'w') as f:
        f.write(latex_content)




