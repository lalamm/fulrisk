from performance import BasePerformance  # Assuming BasePerformance is defined in performance module
import pandas as pd

class FakePerformance(BasePerformance):
    """
    A fake performance class inheriting from BasePerformance.

    This class reads portfolio performance data from a CSV file and provides a method to fetch performance data for a specific portfolio.

    Attributes:
    None

    Methods:
    fetch_portfolio_performance(por_name: str) -> pd.Series:
        Fetches performance data for the specified portfolio name.
    """

    def fetch_portfolio_performance(self, por_name: str) -> pd.Series:
        """
        Fetch portfolio performance data for the specified portfolio name.

        Parameters:
        por_name (str): Name of the portfolio to fetch performance data for.

        Returns:
        pd.Series: Series containing performance data for the specified portfolio.

        Raises:
        KeyError: If the specified portfolio name does not exist in the performance data.
        """
        perf = pd.read_csv("performance/perf.csv", index_col=0)
        try:
            return perf.loc[:, por_name]
        except KeyError as e:
            raise KeyError(f"Missing performance for {por_name}")
