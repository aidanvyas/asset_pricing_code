import time
import logging
import pandas as pd
import numpy as np
from pandas.tseries.offsets import MonthEnd
from scipy import stats
import statsmodels.api as sm

def setup_logging(logging_enabled: bool = True):
    """
    Helper function to setup logging.

    This function configures the logging settings for the application. It sets
    the logging level to INFO and specifies the log message format. If logging
    is not enabled, it disables all logging messages.

    Args:
        logging_enabled (bool): Whether to enable logging. Defaults to True.

    Returns:
        None
    """
    if logging_enabled:
        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s - %(levelname)s - %(message)s')
    else:
        logging.disable(logging.CRITICAL)


def quantile_bucket(row: pd.Series,
                    factor: str,
                    quantiles: int) -> str:
    """
    Helper function to assign a stock to the correct factor bucket.

    Args:
        row (pd.Series): The row of the DataFrame.
        factor (str): The factor to use for the bucketing.
        quantiles (int): The number of quantiles to use.

    Returns:
        str: The bucket to assign the stock to.
    """
    for i in range(1, quantiles):
        if row[factor] <= row[f'{i * 100 // quantiles}%']:
            return str(i)
    return str(quantiles)


def wavg(group: pd.DataFrame,
         avg_name: str,
         weight_name: str) -> float:
    """
    Helper function to calculate value-weighted returns.

    Args:
        group (pd.DataFrame): The group to calculate the value-weighted returns for.
        avg_name (str): The name of the average column.
        weight_name (str): The name of the weight column.

    Returns:
        float: The value-weighted return.
    """
    average_column = group[avg_name]
    weight_column = group[weight_name]
    try:
        return (average_column * weight_column).sum() / weight_column.sum()
    except ZeroDivisionError:
        return np.nan


def calculate_corner_returns(quantiles: int,
                             lookback_period: int,
                             lag: int,
                             logging_enabled: bool = True):
    """
    This function calculates the corner returns for the momentum portfolios.

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

    # Create a dataframe for the value-weighted returns.
    vwret = crsp5.groupby(['jdate', 'factor_portfolio', 'past_portfolio']).apply(wavg, 'retadj', 'wt').to_frame().reset_index().rename(columns={0: 'vwret'})
    logging.info("Created a dataframe for the value-weighted returns.")

    # Create a column that represents the combined past and current momentum portfolio that the stock is in.
    vwret['past_current_portfolio'] = vwret['past_portfolio'].astype(int) * 10 + vwret['factor_portfolio'].astype(int)
    logging.info("Created a column that represents the combined past and current momentum portfolio.")

    # Tranpose the dataframes such that the rows are dates and the columns are portfolio returns.
    mom_portfolios = vwret.pivot(index='jdate', columns=['past_current_portfolio'], values='vwret').reset_index()
    logging.info("Transposed the dataframes.")

    # Set a date restriction from July 1963 to December 2022.
    mom_portfolios63 = mom_portfolios[(mom_portfolios['jdate'] >= '1963-07-01') & (mom_portfolios['jdate'] <= '2022-12-31')]
    logging.info("Set a date restriction.")

    # Calculate the average returns across all time for each portfolio.
    avg_returns = mom_portfolios63.mean(numeric_only=True) * 100

    # Prepare the LaTeX table content.
    latex_content = [
        "\\begin{table*}[ht!]",
        "\\centering",
        "\\caption{Average Returns for Momentum Portfolios (\\%) with Lookback Period of " + str(lookback_period) + " Months and Lag of " + str(lag) + " Month}",
        "\\label{tab:average_returns}",
        "\\begin{tabular}{c" + "c" * quantiles + "}",
        "\\toprule",
        "Past & \\multicolumn{" + str(quantiles) + "}{c}{Current Momentum Portfolio} \\\\",
        "Portfolio & " + " & ".join([str(i) for i in range(1, quantiles+1)]) + " \\\\",
        "\\midrule"
    ]

    # Populate the table rows with average returns.
    for past_portfolio in range(1, quantiles + 1):
        row_str = str(past_portfolio) + " & " + " & ".join([f"{avg_returns[past_portfolio * 10 + current_portfolio]:.2f}" 
                                                            for current_portfolio in range(1, quantiles + 1)]) + " \\\\"
        latex_content.append(row_str)

    # Complete the LaTeX table.
    latex_content.extend([
        "\\bottomrule",
        "\\end{tabular}",
        "\\end{table*}"
    ])

    # Join the content and write it to a file.
    latex_content = "\n".join(latex_content)
    file_name = f"back_momentum_skewness/tables/transition_returns_[{lookback_period}, {lag}]_with_{quantiles}_quantiles.tex"
    with open(file_name, 'w') as f:
        f.write(latex_content)
    logging.info(f"Saved the LaTeX table to '{file_name}'.")


def run_tests():
    """
    This function runs the tests for the momentum portfolios.
    """

    # # Create and verify the momentum portfolios (quantiles=10, lookback_period=12, lag=1, nyse_only=True).
    # start_time = time.time()
    # perform_quantile_sorts(quantiles=10, lookback_period=12, lag=1, nyse_only=True, logging_enabled=True)
    # verify_decile_sort('raw_mom_deciles', 'processed_mom_[12, 1]_with_10_quantiles')
    # elapsed_time = time.time() - start_time
    # print(f"Performed and verified decile sorts for momentum portfolios in {elapsed_time:.2f} seconds.")

    # # Create and verify the short-term reversal portfolios (quantiles=10, lookback_period=1, lag=0, nyse_only=True).
    # start_time = time.time()
    # perform_quantile_sorts(quantiles=10, lookback_period=1, lag=0, nyse_only=True, logging_enabled=True)
    # verify_decile_sort('raw_str_deciles', 'processed_mom_[1, 0]_with_10_quantiles')
    # elapsed_time = time.time() - start_time
    # print(f"Performed and verified decile sorts for short-term reversal portfolios in {elapsed_time:.2f} seconds.")

    # # Create and verify the long-term reversal portfolios (quantiles=10, lookback_period=60, lag=12, nyse_only=True).
    # start_time = time.time()
    # perform_quantile_sorts(quantiles=10, lookback_period=60, lag=12, nyse_only=True, logging_enabled=True)
    # verify_decile_sort('raw_ltr_deciles', 'processed_mom_[60, 12]_with_10_quantiles')
    # elapsed_time = time.time() - start_time
    # print(f"Performed and verified decile sorts for long-term reversal portfolios in {elapsed_time:.2f} seconds.")

    # Replicate the summary statistics for the momentum portfolios.
    # start_time = time.time()
    # perform_quantile_sorts(quantiles=5, lookback_period=3, lag=1, nyse_only=False, logging_enabled=True)
    # output_summary_statistics(quantiles=5, lookback_period=3, lag=1, logging_enabled=True)
    # perform_quantile_sorts(quantiles=5, lookback_period=6, lag=1, nyse_only=False, logging_enabled=True)
    # output_summary_statistics(quantiles=5, lookback_period=6, lag=1, logging_enabled=True)
    # perform_quantile_sorts(quantiles=5, lookback_period=9, lag=1, nyse_only=False, logging_enabled=True)
    # output_summary_statistics(quantiles=5, lookback_period=9, lag=1, logging_enabled=True)
    # perform_quantile_sorts(quantiles=5, lookback_period=12, lag=1, nyse_only=False, logging_enabled=True)
    # output_summary_statistics(quantiles=5, lookback_period=12, lag=1, logging_enabled=True)
    # elapsed_time = time.time() - start_time
    # print(f"Replicated quintile sorts for momentum portfolios and outputted summary statistics in {elapsed_time:.2f} seconds.")

    # # Calculate the transition probabilities and returns for the momentum portfolios.
    # start_time = time.time()
    # create_transition_table(quantiles=5, lookback_period=3, lag=1, nyse_only=False, logging_enabled=True)
    # calculate_transition_probabilities(quantiles=5, lookback_period=3, lag=1, logging_enabled=True)
    # calculate_corner_returns(quantiles=5, lookback_period=3, lag=1, logging_enabled=True)
    # create_transition_table(quantiles=5, lookback_period=6, lag=1, nyse_only=False, logging_enabled=True)
    # calculate_transition_probabilities(quantiles=5, lookback_period=6, lag=1, logging_enabled=True)
    # calculate_corner_returns(quantiles=5, lookback_period=6, lag=1, logging_enabled=True)
    # create_transition_table(quantiles=5, lookback_period=9, lag=1, nyse_only=False, logging_enabled=True)
    # calculate_transition_probabilities(quantiles=5, lookback_period=9, lag=1, logging_enabled=True)
    # calculate_corner_returns(quantiles=5, lookback_period=9, lag=1, logging_enabled=True)
    # create_transition_table(quantiles=5, lookback_period=12, lag=1, nyse_only=False, logging_enabled=True)
    # calculate_transition_probabilities(quantiles=5, lookback_period=12, lag=1, logging_enabled=True)
    # calculate_corner_returns(quantiles=5, lookback_period=12, lag=1, logging_enabled=True)
    # elapsed_time = time.time() - start_time
    # print(f"Calculated the transition probabilities in {elapsed_time:.2f} seconds.")

run_tests()