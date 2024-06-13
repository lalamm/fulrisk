from abc import ABC, abstractmethod
import pandas as pd

class BasePerformance(ABC):
    @abstractmethod
    def fetch_portfolio_performance(self,por_name) -> pd.Series:
        pass
