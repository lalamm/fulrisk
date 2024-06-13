import argparse
from performance.FakePerformance import FakePerformance
from report import STANDARD_REPORT, run_report

def main():
    """
    Main function for portfolio risk reporting.

    Parses command-line arguments to fetch portfolio and benchmark performance data,
    optionally including metadata, and runs a standard report.

    Command-line Arguments:
    -p, --portfolio   Name of the portfolio.
    -b, --benchmark   Name of the benchmark.
    -a, --about       About the portfolio (optional).

    Returns:
    None
    """
    parser = argparse.ArgumentParser(description='Portfolio risk reporting')
    parser.add_argument(
        '-p', '--portfolio',
        type=str,
        required=True,
        help='Name of the portfolio'
    )
    parser.add_argument(
        '-b', '--benchmark',
        type=str,
        required=True,
        help='Name of the benchmark'
    )
    parser.add_argument(
        '-a', '--about',
        type=str,
        help='About the portfolio'
    )
    args = parser.parse_args()

    portfolio_name = args.portfolio
    benchmark_name = args.benchmark

    perf = FakePerformance()
    por_perf = perf.fetch_portfolio_performance(portfolio_name)
    bench_perf = perf.fetch_portfolio_performance(benchmark_name)

    metadata = {}
    if args.about:
        metadata["about"] = args.about

    run_report(STANDARD_REPORT, por_perf, bench_perf, metadata)

if __name__ == "__main__":
    main()
