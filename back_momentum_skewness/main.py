from quantile_sorts import perform_ff_quantile_sorts, perform_mom_quantile_sorts
import time

if __name__ == "__main__":

    # Quintile sorts for the Fama-French factors.
    perform_ff_quantile_sorts(quantiles=5, factor='me', nyse_only=False, sign=-1, logging_enabled=True)
    perform_ff_quantile_sorts(quantiles=5, factor='BE_ME', nyse_only=False, sign=1, logging_enabled=True)
    perform_ff_quantile_sorts(quantiles=5, factor='OP_BE', nyse_only=True, sign=1, logging_enabled=True)
    perform_ff_quantile_sorts(quantiles=5, factor='AT_GR1', nyse_only=False, sign=-1, logging_enabled=True)

    # Quintile sorts for the momentum portfolios.
    start_time = time.time()
    perform_mom_quantile_sorts(quantiles=5, lookback_period=3, lag=1, nyse_only=False, sign=1, logging_enabled=True)
    perform_mom_quantile_sorts(quantiles=5, lookback_period=6, lag=1, nyse_only=False, sign=1, logging_enabled=True)
    perform_mom_quantile_sorts(quantiles=5, lookback_period=9, lag=1, nyse_only=False, sign=1, logging_enabled=True)
    perform_mom_quantile_sorts(quantiles=5, lookback_period=12, lag=1, nyse_only=False, sign=1, logging_enabled=True)
    perform_mom_quantile_sorts(quantiles=5, lookback_period=1, lag=0, nyse_only=False, sign=-1, logging_enabled=True)
    elapsed_time = time.time() - start_time
    print(f"Performed quintile sorts for momentum portfolios in {elapsed_time:.2f} seconds.")

