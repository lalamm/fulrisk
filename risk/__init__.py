BDAYS = 252

def metrics(returns):
    """
    Calculate average return, standard deviation of returns, and Sharpe ratio.

    Parameters:
    returns (pandas.Series): Time series of returns data.

    Returns:
    dict: A dictionary containing the calculated metrics:
        - 'avg_return': Average return of the input returns data.
        - 'avg_std': Standard deviation of the input returns data.
        - 'avg_sharpe': Sharpe ratio calculated as average return divided by standard deviation.
    """
    avg_return = returns.mean()
    avg_std = returns.std()
    avg_sharpe = avg_return / avg_std if avg_std != 0 else 0.0  # Handle division by zero gracefully
    return {
        "avg_return": avg_return,
        "avg_std": avg_std,
        "avg_sharpe": avg_sharpe
    }
