from performance import BasePerformance
import pandas as pd

class FakePerformance(BasePerformance):
    def fetch_portfolio_performance(self, por_name) -> pd.Series:
        perf = pd.read_csv("performance/perf.csv",index_col=0)
        try:
            return perf.loc[:,por_name]
        except KeyError as e:
            raise KeyError(f"Missing performance for {por_name}")
