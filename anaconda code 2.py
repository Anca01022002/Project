# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 13:29:37 2025

@author: User
"""

# compare_path_pltr.py
import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt

# --- User-configurable period ---
start_date = "2024-01-01"
# yfinance's end date is exclusive; use next day to include 2025-11-13
end_date = "2025-11-14"

tickers = ["PATH", "PLTR"]

# Download Adjusted Close price
# group_by="column" ensures DataFrame columns for tickers
data = yf.download(tickers, start=start_date, end=end_date, progress=False)["Adj Close"]

# If yfinance returns a Series when only one ticker is requested, ensure DataFrame
if isinstance(data, pd.Series):
    data = data.to_frame()

# Drop rows where both are NaN (market closed)
data = data.dropna(how="all")

if data.empty:
    raise SystemError("No price data returned for the requested period. Check tickers and dates.")

# Align and forward-fill short gaps if needed (optional)
data = data.ffill().bfill()

# Determine first available trading day and last available day in the requested window
first_day = data.index.min()
last_day  = data.index.max()

# Get start and end prices for each ticker (first valid price in the period, last valid price)
start_prices = data.loc[first_day]
end_prices   = data.loc[last_day]

# Compute total percentage change: (end/start - 1) * 100
pct_change = ((end_prices / start_prices) - 1) * 100

# Print summary table
summary = pd.DataFrame({
    "start_date": [first_day.date(), first_day.date()],
    "end_date":   [last_day.date(), last_day.date()],
    "start_price": [start_prices["PATH"], start_prices["PLTR"]],
    "end_price":   [end_prices["PATH"], end_prices["PLTR"]],
    "pct_change":  [pct_change["PATH"], pct_change["PLTR"]],
}, index=["PATH (UiPath)", "PLTR (Palantir)"])

print("\n=== Summary: Price change from {} to {} ===\n".format(first_day.date(), last_day.date()))
print(summary.round(2))

# --- Plotting ---
plt.figure(figsize=(12, 5))
plt.plot(data.index, data["PATH"], label="PATH (Adj Close)")
plt.plot(data.index, data["PLTR"], label="PLTR (Adj Close)")
plt.title("Adjusted Close Price: PATH vs PLTR\n{} to {}".format(first_day.date(), last_day.date()))
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

# Normalize for relative-performance comparison (start at 100)
norm = data / data.iloc[0] * 100

plt.figure(figsize=(12, 5))
plt.plot(norm.index, norm["PATH"], label="PATH (Normalized, base=100)")
plt.plot(norm.index, norm["PLTR"], label="PLTR (Normalized, base=100)")
plt.title("Relative Performance (normalized to 100 at {})".format(first_day.date()))
plt.xlabel("Date")
plt.ylabel("Indexed value (100 = start)")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
