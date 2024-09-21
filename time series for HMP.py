import os
#show current directory
print(os.getcwd()) 
from os import mkdir, getcwd
getcwd()

from statsmodels.tsa.statespace.sarimax import SARIMAX
import matplotlib.pyplot as plt
from statsmodels.tsa.api import ExponentialSmoothing
from ydata_profiling import ProfileReport, profile_report
import pandas as pd



df = pd.read_excel("C:/Users/amrigupt/Downloads/whole2024ChangeEvents.xlsx")
df
df.columns

#Pandas profiling using course



#Keeping only the columns we need

df2 = df[['CATEGORY_NAME', 'EVENT_OCCUR_DATE', 'EVENT_NAME']]
df2

# Convert 'Order_Date' to datetime and sort the dataframe by 'Order_Date'
df2['EVENT_OCCUR_DATE'] = pd.to_datetime(df2['EVENT_OCCUR_DATE'])
df2 = df2.sort_values(by='EVENT_OCCUR_DATE')

# Set 'Order_Date' as the index
df2.set_index('EVENT_OCCUR_DATE', inplace=True)

# Resample data to get monthly counts of events per hierarchy
monthly_events = df2.groupby('CATEGORY_NAME').resample('M').size().unstack(level=0, fill_value=0)

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
for CATEGORY_NAME in monthly_events.columns:
    data = monthly_events[CATEGORY_NAME]
    forecast = forecast_hierarchy(data, CATEGORY_NAME)
    forecasts[CATEGORY_NAME] = forecast


forecasts


    
    