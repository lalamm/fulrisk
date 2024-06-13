# Portfolio Risk Reporting

This project provides a tool for generating portfolio risk reports based on historical performance data. It allows users to specify a portfolio, benchmark, and optional metadata to generate a comprehensive report with visual plots and performance metrics.

## Requirements

- Python >= 3.10
- Required Python packages (see `requirements.txt`)

## Installation

1. Clone the repository:

2. Navigate to the project directory:
   ```
   cd portfolio-risk-reporting
   ```

3. Install the required Python packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

To generate a portfolio risk report, run the `main.py` script with the following command-line arguments:

```
python main.py -p PORTFOLIO_NAME -b BENCHMARK_NAME [-a ABOUT]
```

- `-p PORTFOLIO_NAME` (required): Name of the portfolio for which to generate the report.
- `-b BENCHMARK_NAME` (required): Name of the benchmark to compare against.
- `-a ABOUT` (optional): Additional information about the portfolio.

Example usage:
```
python main.py -p "Sverige" -b MXSE -a "En otroligt fin sverigefond med fokus på outperformance"
```

This command will generate a portfolio risk report for the "Sverige" portfolio, using the MXSE benchmark, and include the provided description.

## Project Structure

- `performance/`: Module for fetching portfolio performance data.
  - `__init__.py`: Defines the `BasePerformance` abstract base class.
  - `FakePerformance.py`: Implements a fake performance class for reading performance data from a CSV file.

- `risk/`: Module for calculating risk metrics.
  - `__init__.py`: Defines the `metrics` function for calculating average return, standard deviation, and Sharpe ratio.

- `report/`: Module for generating the portfolio risk report.
  - `__init__.py`: Defines functions for generating different sections of the report, such as title page, performance plots, and performance table.

- `main.py`: Main script for running the portfolio risk reporting tool.

- `requirements.txt`: Lists the required Python packages for running the project.

## Output

The generated portfolio risk report will be saved as `report.html` in the project directory. It includes the following sections:

- Title page: Displays the portfolio name, benchmark name (if provided), and the "about" information (if provided).
- Performance plot: Shows the cumulative returns of the portfolio over time.
- Active performance plot: Compares the performance of the portfolio against the benchmark (if provided).
- Performance table: Presents key performance metrics, such as returns, risk, Sharpe ratio, and tracking error (if benchmark is provided).


Example report
[Report](https://github.com/lalamm/fulrisk/blob/main/report.html)
