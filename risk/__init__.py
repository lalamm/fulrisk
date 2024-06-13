BDAYS = 252
def metrics(returns):
    avg_return = returns.mean()
    avg_std = returns.std()
    return {
        "avg_return" : avg_return,
        "avg_std" : avg_std,
        "avg_sharpe": avg_return/avg_std
    }
