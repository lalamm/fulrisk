import base64
from io import BytesIO
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from risk import BDAYS, metrics

def title_page(portfolio,benchmark,metadata):
    benchmark_name = f" vs {benchmark.name}" if benchmark is not None else ""
    about = f"<p>{metadata['about']}</p>" if 'about' in metadata else ""

    return f"<h1>Portfolio report for {portfolio.name}{benchmark_name}</h1>{about}"

def active_performance_plot(portfolio,benchmark,metadata):
    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot the Pandas series
    simple_returns = ((portfolio - benchmark)+1).cumprod().apply(np.exp)

    # Set the initial value to 100
    simple_returns = (simple_returns / simple_returns.iloc[0] * 100).plot(ax=ax)

        # Set plot title and axis labels
    ax.set_title(f'{portfolio.name} vs {benchmark.name}')
    ax.set_xlabel('Date')
    ax.set_ylabel('Returns')

    # Save the plot to a BytesIO object
    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)

    # Encode the plot as a Base64 string
    plot_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Create the HTML string with the Base64-encoded plot
    return f"""
        <img src="data:image/png;base64,{plot_base64}">
    """
def performance_plot(portfolio,benchmark,metadata):
    fig, ax = plt.subplots(figsize=(8, 6))

    # Plot the Pandas series
    # Plot the Pandas series
    simple_returns = (portfolio+1).cumprod().apply(np.exp)

    # Set the initial value to 100
    simple_returns = (simple_returns / simple_returns.iloc[0] * 100).plot(ax=ax)

        # Set plot title and axis labels
    ax.set_title(f'{portfolio.name}')
    ax.set_xlabel('Date')
    ax.set_ylabel('Returns')

    # Save the plot to a BytesIO object
    buffer = BytesIO()
    fig.savefig(buffer, format='png')
    buffer.seek(0)

    # Encode the plot as a Base64 string
    plot_base64 = base64.b64encode(buffer.getvalue()).decode('utf-8')

    # Create the HTML string with the Base64-encoded plot
    return f"""
     <img src="data:image/png;base64,{plot_base64}">
    """

def performance_table(portfolio, benchmark,metadata):
    data = {portfolio.name : metrics(portfolio)}
    if benchmark is not None:
        data[benchmark.name] = metrics(benchmark)

    df = pd.DataFrame.from_dict(data)
    orig_indices = df.index
    df.loc['Performance (%)'] = (df.loc['avg_return'] * BDAYS).apply(lambda x: f"{(x*100):.2f}%")
    df.loc['Risk (%)'] = (df.loc['avg_std'] * np.sqrt(BDAYS)).apply(lambda x: f"{(x*100):.2f}%")
    df.loc['Sharpe'] = df.loc['avg_sharpe'] * np.sqrt(BDAYS)
    if benchmark is not None:
        excess_returns = portfolio-benchmark
        te = excess_returns.std()*np.sqrt(252)
        df.loc["TE (%)",portfolio.name] = '{0:.2f}'.format(te*100)
        pass
    df.drop(index=orig_indices,inplace=True)
    table_html = df.to_html(index=True)
    return table_html

STANDARD_REPORT = [title_page,performance_plot,active_performance_plot,performance_table]
def run_report(report,portfolio,benchmark=None,metadata={}):
    html = ""
    for page in report:
        html+=page(portfolio,benchmark,metadata)

    with open("report.html", "w") as text_file:
        text_file.write(html)
