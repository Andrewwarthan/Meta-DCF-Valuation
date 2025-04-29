import pandas as pd
import numpy as np
import yfinance as yf
import plotly.graph_objs as go
from dash import Dash, dcc, html, Input, Output

# === Load Meta FCF Data ===
df = pd.read_csv("meta_fcf_data.csv")
df = df.sort_values("Year")

# === Dash App Setup ===
app = Dash(__name__)
app.title = "Meta DCF Valuation"

app.layout = html.Div([
    html.H1("Meta Platforms DCF Valuation Tool"),
    html.Div([
        html.Label("Growth Rate (%):"),
        dcc.Slider(id='growth-rate', min=0.05, max=0.20, step=0.01, value=0.12,
                   marks={i: f"{int(i*100)}%" for i in [0.05, 0.10, 0.15, 0.20]}),
        html.Br(),
        html.Label("WACC (%):"),
        dcc.Slider(id='wacc', min=0.05, max=0.12, step=0.005, value=0.08,
                   marks={i: f"{int(i*100)}%" for i in [0.05, 0.08, 0.10, 0.12]}),
        html.Br(),
        html.Label("Terminal Growth Rate (%):"),
        dcc.Slider(id='terminal-growth', min=0.01, max=0.04, step=0.0025, value=0.025,
                   marks={i: f"{int(i*100)}%" for i in [0.01, 0.025, 0.04]}),
    ], style={'width': '48%', 'display': 'inline-block', 'padding': '20px'}),

    html.Div(id='valuation-output', style={'margin': '40px 0'}),
    dcc.Graph(id='fcf-graph')
])

@app.callback(
    [Output('valuation-output', 'children'),
     Output('fcf-graph', 'figure')],
    [Input('growth-rate', 'value'),
     Input('wacc', 'value'),
     Input('terminal-growth', 'value')]
)
def update_dcf(growth_rate, wacc, terminal_growth):
    last_fcf = df["FCF"].iloc[-1]
    forecast_years = 5

    forecasted_fcf = [last_fcf * (1 + growth_rate) ** i for i in range(1, forecast_years + 1)]
    discount_factors = [(1 / (1 + wacc) ** i) for i in range(1, forecast_years + 1)]
    discounted_fcf = [fcf * df for fcf, df in zip(forecasted_fcf, discount_factors)]

    terminal_value = forecasted_fcf[-1] * (1 + terminal_growth) / (wacc - terminal_growth)
    discounted_terminal_value = terminal_value / ((1 + wacc) ** forecast_years)

    enterprise_value = sum(discounted_fcf) + discounted_terminal_value
    net_debt = -3000  # Meta has net cash (in millions)
    equity_value = enterprise_value - net_debt
    equity_value_dollars = equity_value * 1_000_000
    shares_outstanding = 2_550_000_000  # Meta shares
    implied_share_price = equity_value_dollars / shares_outstanding

    ticker = yf.Ticker("META")
    current_price = ticker.history(period="1d")["Close"].iloc[-1]
    diff = current_price - implied_share_price
    pct_diff = (diff / implied_share_price) * 100

    output_text = html.Div([
        html.H4("DCF Valuation Summary"),
        html.P(f"Enterprise Value: ${enterprise_value:,.2f}M"),
        html.P(f"Equity Value: ${equity_value:,.2f}M"),
        html.P(f"Implied Share Price: ${implied_share_price:.2f}"),
        html.P(f"Current Market Price: ${current_price:.2f}"),
        html.P(f"Difference: ${diff:.2f} ({pct_diff:.2f}%)"),
        html.P("→ The market price is {} the DCF-implied value.".format(
            "above" if diff > 0 else "below"))
    ])

    historical_years = list(df["Year"])
    historical_fcf = list(df["FCF"])
    forecast_years_labels = [df["Year"].iloc[-1] + i for i in range(1, 6)]

    figure = {
        'data': [
            go.Scatter(x=historical_years, y=historical_fcf, mode='lines+markers', name='Historical FCF', line=dict(color='blue')),
            go.Scatter(x=forecast_years_labels, y=forecasted_fcf, mode='lines+markers', name='Forecasted FCF', line=dict(color='red', dash='dash'))
        ],
        'layout': go.Layout(
            title='Historical and Forecasted Free Cash Flow',
            xaxis={'title': 'Year'},
            yaxis={'title': 'Free Cash Flow (in millions)'},
            hovermode='closest'
        )
    }

    return output_text, figure

if __name__ == '__main__':
    app.run(debug=True)
