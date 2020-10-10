import datetime
import pandas as pd
import yfinance as yf

import helpers
from config import deposits

sorted_deposits = sorted(deposits, key=lambda tup: helpers.date_to_timestamp(tup[0]))

startDate = sorted_deposits[0][0]
endDate = helpers.shift_date_string(sorted_deposits[-1][0], 7) # pad end date 

#define the ticker symbol
tickerSymbol = 'VOO'

#get data on this ticker
tickerData = yf.Ticker(tickerSymbol)

#get the historical prices for this ticker
tickerDf = tickerData.history(period='1d', start=startDate, end=endDate)

# Initialize variables
total_deposits = sum([pair[1] for pair in deposits])
curr_deposits = 0
curr_close = 0

for date_string, amt in sorted_deposits:
    try:
        dailyTicker = tickerDf.loc[date_string]
    except KeyError:
        new_date = helpers.sanitize_dates(date_string)
        dailyTicker = tickerDf.loc[new_date]

    # calculate change of previous deposits 
    if curr_close:
        curr_deposits = curr_deposits *  dailyTicker.Close / curr_close
    curr_close = dailyTicker.Close
   
    # add in new deposit
    curr_deposits += amt



end_date = datetime.datetime.strptime(endDate, "%Y-%m-%d")
start_date = datetime.datetime.strptime(startDate, "%Y-%m-%d")
year_diff = end_date.year - start_date.year

print(f"Backtesting ticker {tickerSymbol}")
print(f"Net deposits: {total_deposits:.2f}")
print(f"Account value: {curr_deposits:.2f}")
print(f"Current Annualized ROI: {(curr_deposits / total_deposits - 1) * 100 / year_diff:.3f}%")
