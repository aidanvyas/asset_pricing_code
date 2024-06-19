# Standard library imports.
import time

# Local application/library specific imports.
import logging
from quantile_sorts import perform_ff_quantile_sorts, perform_mom_quantile_sorts
from transitions import create_original_mom_transition_table, calculate_mom_transition_probabilities, create_ff_transition_tables, calculate_ff_transition_probabilities, create_ff_multiyear_transition_tables, create_ff_returns_transition_tables, calculate_ff_returns_transition_probabilities

if __name__ == "__main__":

    # Quintile sorts for the Fama-French factors.
    perform_ff_quantile_sorts(quantiles=5, factor='me', nyse_only=False, sign=-1, logging_enabled=True)
    perform_ff_quantile_sorts(quantiles=5, factor='BE_ME', nyse_only=False, sign=1, logging_enabled=True)
    perform_ff_quantile_sorts(quantiles=5, factor='OP_BE', nyse_only=False, sign=1, logging_enabled=True)
    perform_ff_quantile_sorts(quantiles=5, factor='AT_GR1', nyse_only=False, sign=-1, logging_enabled=True)
    print(f"Performed quantile sorts on Fam-French factors.")

    # Quintile sorts for momentum portfolios.
    # start_time = time.time()
    # perform_mom_quantile_sorts(quantiles=5, lookback_period=12, lag=1, nyse_only=False, sign=1, logging_enabled=False)
    # perform_mom_quantile_sorts(quantiles=5, lookback_period=9, lag=1, nyse_only=False, sign=1, logging_enabled=False)
    # perform_mom_quantile_sorts(quantiles=5, lookback_period=6, lag=1, nyse_only=False, sign=1, logging_enabled=False)
    # perform_mom_quantile_sorts(quantiles=5, lookback_period=3, lag=1, nyse_only=False, sign=1, logging_enabled=False)
    # perform_mom_quantile_sorts(quantiles=5, lookback_period=1, lag=0, nyse_only=False, sign=-1, logging_enabled=False)
    # elapsed_time = time.time() - start_time
    # print(f"Performed quantile sorts on momentum in {elapsed_time:.2f} seconds.")

    # Transition probabilities for momentum portfolios.
    # start_time = time.time()
    # create_original_mom_transition_table(quantiles=5, lookback_period=12, lag=0, nyse_only=False, logging_enabled=True)
    # calculate_mom_transition_probabilities(quantiles=5, lookback_period=12, lag=0, logging_enabled=True)
    # create_original_mom_transition_table(quantiles=5, lookback_period=9, lag=0, nyse_only=False, logging_enabled=True)
    # calculate_mom_transition_probabilities(quantiles=5, lookback_period=9, lag=0, logging_enabled=True)
    # create_original_mom_transition_table(quantiles=5, lookback_period=6, lag=0, nyse_only=False, logging_enabled=True)
    # calculate_mom_transition_probabilities(quantiles=5, lookback_period=6, lag=0, logging_enabled=True)
    # create_original_mom_transition_table(quantiles=5, lookback_period=3, lag=0, nyse_only=False, logging_enabled=True)
    # calculate_mom_transition_probabilities(quantiles=5, lookback_period=3, lag=0, logging_enabled=True)
    # # create_original_mom_transition_table(quantiles=5, lookback_period=1, lag=0, nyse_only=False, logging_enabled=True)
    # # calculate_mom_transition_probabilities(quantiles=5, lookback_period=1, lag=0, logging_enabled=True)
    # elapsed_time = time.time() - start_time
    # print(f"Performed and calculated transition probabilities for momentum in {elapsed_time:.2f} seconds.")

    # Transition probabilities for Fama-French factors.
    # start_time = time.time()
    # create_ff_transition_tables(quantiles=5, factor='me', nyse_only=False, logging_enabled=True)
    # calculate_ff_transition_probabilities(quantiles=5, factor='me', logging_enabled=True)
    # create_ff_transition_tables(quantiles=5, factor='BE_ME', nyse_only=False, logging_enabled=True)
    # calculate_ff_transition_probabilities(quantiles=5, factor='BE_ME', logging_enabled=True)
    # create_ff_transition_tables(quantiles=5, factor='OP_BE', nyse_only=False, logging_enabled=True)
    # calculate_ff_transition_probabilities(quantiles=5, factor='OP_BE', logging_enabled=True)
    # create_ff_transition_tables(quantiles=5, factor='AT_GR1', nyse_only=False, logging_enabled=True)
    # calculate_ff_transition_probabilities(quantiles=5, factor='AT_GR1', logging_enabled=True)
    # elapsed_time = time.time() - start_time
    # print(f"Performed and calculated transition probabilities for Fama-French factors in {elapsed_time:.2f} seconds.")

    # Transition probabilites for returns.
    # start_time = time.time()
    # create_ff_returns_transition_tables(quantiles=5, factor='me', nyse_only=False, logging_enabled=True)
    # calculate_ff_returns_transition_probabilities(quantiles=5, factor='me', logging_enabled=True)
    # create_ff_returns_transition_tables(quantiles=5, factor='BE_ME', nyse_only=False, logging_enabled=True)
    # calculate_ff_returns_transition_probabilities(quantiles=5, factor='BE_ME', logging_enabled=True)
    # create_ff_returns_transition_tables(quantiles=5, factor='OP_BE', nyse_only=False, logging_enabled=True)
    # calculate_ff_returns_transition_probabilities(quantiles=5, factor='OP_BE', logging_enabled=True)
    # create_ff_returns_transition_tables(quantiles=5, factor='AT_GR1', nyse_only=False, logging_enabled=True)
    # calculate_ff_returns_transition_probabilities(quantiles=5, factor='AT_GR1', logging_enabled=True)
    # elapsed_time = time.time() - start_time
    # print(f"Performed and calculated transition probabilities for returns in {elapsed_time:.2f} seconds.")