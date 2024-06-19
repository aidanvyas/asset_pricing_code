from quantile_sorts import perform_ff_quantile_sorts

if __name__ == "__main__":

    # Quintile sorts for the Fama-French factors.
    perform_ff_quantile_sorts(quantiles=5, factor='me', nyse_only=False, sign=-1, logging_enabled=True)
    perform_ff_quantile_sorts(quantiles=5, factor='BE_ME', nyse_only=False, sign=1, logging_enabled=True)
    perform_ff_quantile_sorts(quantiles=5, factor='OP_BE', nyse_only=False, sign=1, logging_enabled=True)
    perform_ff_quantile_sorts(quantiles=5, factor='AT_GR1', nyse_only=False, sign=-1, logging_enabled=True)
