# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 13:28:38 2025

@author: User
"""
import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt

# 1. Fetch stock price data for both
tickers = ["PATH", "PLTR"]
start_date = "2024-01-01"
end_date = "2025-12-31"
data = yf.download(tickers, start=start_date, end=end_date, progress=False)['Adj Close']

# 2. Compute daily returns
returns = data.pct_change().dropna()

# 3. Compute rolling volatility (e.g., 30-day standard deviation) and annualized volatility
vol_window = 30
rolling_vol = returns.rolling(window=vol_window).std() * np.sqrt(252)

# 4. Compute overall volatility for each stock in the period
annual_vol = returns.std() * np.sqrt(252)
print("Annualized volatility for each stock:\n", annual_vol)

# 5. Plot rolling volatility
plt.figure(figsize=(12,6))
for ticker in tickers:
    plt.plot(rolling_vol.index, rolling_vol[ticker], label=f"{ticker} 30-day vol")
plt.legend()
plt.title("Rolling 30-day Annualized Volatility (2024-2025)")
plt.xlabel("Date")
plt.ylabel("Volatility")
plt.show()

# 6. Compare summary statistics
summary = pd.DataFrame({
    'MeanVol': rolling_vol.mean(),
    'MaxVol': rolling_vol.max(),
    'StdVol': rolling_vol.std()
})
print("Summary statistics of rolling volatility:\n", summary)

