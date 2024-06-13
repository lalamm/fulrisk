import base64
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from risk import BDAYS, metrics

def title_page(portfolio, benchmark, metadata):
    """
    Generates the title page of the report.

    Parameters:
    - portfolio: The portfolio data.
    - benchmark: The benchmark data.
    - metadata: Dictionary containing metadata information.

    Returns:
    - HTML string of the title page.
    """
    benchmark_name = f" vs {benchmark.name}" if benchmark is not None else ""
    about = f"<p>{metadata.get('about', '')}</p>"

    return f"<h1>Portfolio report for {portfolio.name}{benchmark_name}</h1>{about}"

def generate_plot(data, title, xlabel, ylabel):
    """
    Generates a plot and encodes it as a base64 string.

    Parameters:
    - data: The data to plot.
    - title: The title of the plot.
    - xlabel: The label for the x-axis.
    - ylabel: The label for the y-axis.

    Returns:
    - HTML string with the base64-encoded plot image.
    """
    fig, ax = plt.subplots(figsize=(8, 6))
    data.plot(ax=ax)

    ax.set_title(title)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)

    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)
    plot_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    plt.close(fig)

    return f'<img src="data:image/png;base64,{plot_base64}">'

def active_performance_plot(portfolio, benchmark, metadata):
    """
    Generates the active performance plot.

    Parameters:
    - portfolio: The portfolio data.
    - benchmark: The benchmark data.
    - metadata: Dictionary containing metadata information.

    Returns:
    - HTML string with the active performance plot.
    """
    active_returns = (portfolio - benchmark).add(1).cumprod()
    active_returns = active_returns / active_returns.iloc[0] * 100

    return generate_plot(active_returns, f'{portfolio.name} vs {benchmark.name}', 'Date', 'Returns')

def performance_plot(portfolio, benchmark, metadata):
    """
    Generates the performance plot.

    Parameters:
    - portfolio: The portfolio data.
    - benchmark: The benchmark data.
    - metadata: Dictionary containing metadata information.

    Returns:
    - HTML string with the performance plot.
    """
    cumulative_returns = portfolio.add(1).cumprod()
    cumulative_returns = cumulative_returns / cumulative_returns.iloc[0] * 100

    return generate_plot(cumulative_returns, f'{portfolio.name}', 'Date', 'Returns')

def performance_table(portfolio, benchmark, metadata):
    """
    Generates the performance table.

    Parameters:
    - portfolio: The portfolio data.
    - benchmark: The benchmark data.
    - metadata: Dictionary containing metadata information.

    Returns:
    - HTML string with the performance table.
    """
    data = {portfolio.name: metrics(portfolio)}
    if benchmark is not None:
        data[benchmark.name] = metrics(benchmark)

    df = pd.DataFrame.from_dict(data)
    original_indices = df.index
    df.loc['Performance (%)'] = (df.loc['avg_return'] * BDAYS).apply(lambda x: f"{(x*100):.2f}%")
    df.loc['Risk (%)'] = (df.loc['avg_std'] * np.sqrt(BDAYS)).apply(lambda x: f"{(x*100):.2f}%")
    df.loc['Sharpe'] = df.loc['avg_sharpe'] * np.sqrt(BDAYS)

    if benchmark is not None:
        excess_returns = portfolio - benchmark
        te = excess_returns.std() * np.sqrt(252)
        df.loc["TE (%)", portfolio.name] = f'{te*100:.2f}'
        df.loc["TE (%)",benchmark.name] = "-"
    df.drop(index=original_indices,inplace=True)
    table_html = df.to_html(index=True)
    return table_html

STANDARD_REPORT = [title_page, performance_plot, active_performance_plot, performance_table]

def run_report(report, portfolio, benchmark=None, metadata={}):
    """
    Runs the report generation process.

    Parameters:
    - report: List of report generation functions.
    - portfolio: The portfolio data.
    - benchmark: The benchmark data.
    - metadata: Dictionary containing metadata information.
    """
    html = ""
    for page in report:
        html += page(portfolio, benchmark, metadata)

    with open("report.html", "w") as text_file:
        text_file.write(html)
