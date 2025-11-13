# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 13:26:19 2025

@author: User
"""

import pandas as pd
import numpy as np
import yfinance as yf
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Fetch stock price data for PATH
ticker = "PATH"
start_date = "2024-01-01"
end_date = "2025-12-31"
df_price = yf.download(ticker, start=start_date, end=end_date, progress=False)

# 2. Compute e.g. annual or quarterly return  
# Here: compute yearly return based on closing price at year-end
df_price['Year'] = df_price.index.year
yearly_close = df_price.groupby('Year')['Close'].last()
yearly_return = yearly_close.pct_change().dropna()
print("Yearly return for", ticker, "\n", yearly_return)

# 3. Revenue growth data (you will supply manually or via API)
# Based on public data: PATH revenue for FY 2024 ~ $1.31B; FY 2025 ~ $1.43B → growth ~9.3% :contentReference[oaicite:1]{index=1}
revenue = {
    2024: 1.31,
    2025: 1.43
}
rev_growth = { year: (revenue[year] / revenue.get(year-1, np.nan) - 1)
              for year in revenue.keys() if (year-1) in revenue }
print("Revenue growth:", rev_growth)

# 4. Combine into DataFrame
df = pd.DataFrame({
    'Return': yearly_return,
    'RevGrowth': pd.Series(rev_growth)
}).dropna()
print(df)

# 5. Compute correlation
corr = df.corr().loc['Return','RevGrowth']
print(f"Correlation between revenue growth and stock return: {corr:.4f}")

# 6. Plot scatter
sns.regplot(x='RevGrowth', y='Return', data=df)
plt.title(f"{ticker}: Revenue Growth vs Stock Return")
plt.xlabel("Revenue Growth")
plt.ylabel("Stock Annual Return")
plt.show()
