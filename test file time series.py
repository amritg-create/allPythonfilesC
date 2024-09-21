df = pd.read_excel("C:/Users/amrigupt/Downloads/testfilefortimeseries.xlsx")
df

#Test File for Time Series

import pandas as pd
from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt

# Load the uploaded Excel file
file_path = "C:/Users/amrigupt/Downloads/testfilefortimeseries.xlsx"
xls = pd.ExcelFile(file_path)

# Load data from the first sheet
df = pd.read_excel(file_path, sheet_name='Sheet1')

# Convert 'Order_Date' to datetime and sort the dataframe by 'Order_Date'
df['Order_Date'] = pd.to_datetime(df['Order_Date'])
df = df.sort_values(by='Order_Date')

# Set 'Order_Date' as the index
df.set_index('Order_Date', inplace=True)

# Resample data to get monthly counts of events per hierarchy
monthly_events = df.groupby('Hierarchy').resample('M').size().unstack(level=0, fill_value=0)

# Function to forecast next 12 months for a given hierarchy
def forecast_hierarchy(data, hierarchy_name):
    # Fit the SARIMAX model
    model = SARIMAX(data, order=(1, 1, 1), seasonal_order=(1, 1, 1, 12))
    model_fit = model.fit(disp=False)
    
    # Forecast the next 12 months
    forecast = model_fit.get_forecast(steps=12)
    forecast_index = pd.date_range(start=data.index[-1] + pd.DateOffset(months=1), periods=12, freq='M')
    forecast_series = pd.Series(forecast.predicted_mean, index=forecast_index)
    
    # Ensure non-negative values
    forecast_series = forecast_series.apply(lambda x: max(0, x))
    
    # Plot the historical data and forecast
    plt.figure(figsize=(10, 6))
    plt.plot(data, label='Historical')
    plt.plot(forecast_series, label='Forecast', linestyle='--')
    plt.title(f'Event Count Forecast for {hierarchy_name}')
    plt.xlabel('Date')
    plt.ylabel('Event Count')
    plt.legend()
    plt.show()
    
    return forecast_series

# Forecasting for each hierarchy
forecasts = {}
for hierarchy in monthly_events.columns:
    data = monthly_events[hierarchy]
    forecast = forecast_hierarchy(data, hierarchy)
    forecasts[hierarchy] = forecast


forecasts
