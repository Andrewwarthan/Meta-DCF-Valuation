# Meta Platforms DCF Valuation Dashboard

This project is a Python-based interactive web application that performs a Discounted Cash Flow (DCF) analysis for Meta Platforms (META). It was built using Dash, Plotly, and yfinance.

## 📊 Features

- Adjustable inputs: Growth rate, WACC, terminal growth
- Real-time DCF valuation calculation
- Automatically fetches Meta's current stock price
- Forecasted vs historical Free Cash Flow chart
- Responsive, web-based interface using Dash

## 🧮 Key Assumptions (Base Case)
- Growth Rate: 12%
- WACC: 8%
- Terminal Growth Rate: 2.5%
- Net Cash: $3B
- Shares Outstanding: 2.55B

## 📁 Files
- `app.py` — Main Dash application
- `meta_fcf_data.csv` — Historical Free Cash Flow inputs
- `requirements.txt` — Python dependencies
- `README.md` — This file

## ▶️ How to Run

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/meta-dcf-app.git
   cd meta-dcf-app
