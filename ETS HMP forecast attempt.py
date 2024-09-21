from sktime.forecasting.ets import AutoETS
from tqdm import tqdm

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

#Keeping only the columns we need

df2 = df[['CATEGORY_NAME', 'EVENT_OCCUR_DATE', 'EVENT_NAME']]
df2.columns

# Assuming 'df2' is your DataFrame
# Convert EVENT_OCCUR_DATE to datetime
df2['EVENT_OCCUR_DATE'] = pd.to_datetime(df2['EVENT_OCCUR_DATE'])

# Group by CATEGORY_NAME and month, count events
df2['month'] = df2['EVENT_OCCUR_DATE'].dt.to_period('M')
grouped = df2.groupby(['CATEGORY_NAME', 'month']).size().reset_index(name='count')
grouped


# Create a DataFrame for each CATEGORY_NAME and forecast using ETS
forecast_results = {}

for category in grouped['CATEGORY_NAME'].unique():
    category_data = grouped[grouped['CATEGORY_NAME'] == category].set_index('month')
    category_data = category_data.asfreq('M').fillna(0)  # Ensure monthly frequency and fill missing data
    
    # Non-seasonal ETS model
    model = ExponentialSmoothing(category_data['count'], 
                                 trend='additive', 
                                 seasonal=None)
    fit = model.fit()
    forecast = fit.forecast(12)
    forecast_results[category] = forecast

# Display forecast results
for category, forecast in forecast_results.items():
    print(f"Forecast for {category}:")
    print(forecast)
    print("\n")


forecast_results.items()

forecast.tail()