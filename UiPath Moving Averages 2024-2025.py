# -*- coding: utf-8 -*-
"""
Created on Tue Nov 11 08:00:28 2025

@author: Denisa
"""

# -*- coding: utf-8 -*-
"""
UiPath Stock Price Analysis - 2024
@author: Denisa
"""

import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from statsmodels.tsa.stattools import adfuller

# 1. Download UiPath stock data for 2024
data = yf.download("PATH", period="2y")

# 2. Display the first few rows
print(data.head())

# 3. Plot closing price
plt.figure(figsize=(10,5))
plt.plot(data['Close'], label='UiPath Closing Price')
plt.title("UiPath Stock Price in 2024")
plt.xlabel("Date")
plt.ylabel("Price (USD)")
plt.legend()
plt.grid(True)
plt.show()

# 4. Check for stationarity (Augmented Dickey-Fuller Test)
result = adfuller(data['Close'].dropna())
print("ADF Statistic:", result[0])
print("p-value:", result[1])
if result[1] < 0.05:
    print("✅ Series is stationary.")
else:
    print("❌ Series is NOT stationary (has a stochastic trend).")

# 5. Plot moving averages for trend visualization
data['MA20'] = data['Close'].rolling(20).mean()
data['MA50'] = data['Close'].rolling(50).mean()

plt.figure(figsize=(10,5))
plt.plot(data['Close'], label='Close', color='blue')
plt.plot(data['MA20'], label='20-day MA', color='red')
plt.plot(data['MA50'], label='50-day MA', color='green')
plt.title("UiPath Moving Averages (2024)")
plt.legend()
plt.grid(True)
plt.show()
