# DS4B 101-P: PYTHON FOR BUSINESS ANALYSIS ----
# Module 4 (Time Series): Working with Time Series Data ----

# IMPORTS

#%%

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from my_pandas_extensions.database import collect_data

# DATA

#%%

df = collect_data()

# 1.0 DATE BASICS

df['order_date'] #This is datetime 64. 

# Conversion

type("2011-01-07")

pd.to_datetime("2011-01-07") #This is a timestamp. It gets converted to timestamp from string. 

pd.to_datetime("2011-01-07").to_period(freq="W") #This is a weekly time period. 

# Accessing elements

df.order_date

# Months

#You can use accessors to access months and other time elements per below. 

df.order_date.dt.month #this gives us month of year. 
df.order_date.dt.month_name() #This gives us name of month. 

# Days

df.order_date.dt.day 
df.order_date.dt.day_name()

# DATE MATH

import datetime 
today = datetime.date.today() #This gives us today's date. 

today + pd.Timedelta(" 1 day") #This gives us the day for tomorrow. 

pd.to_datetime(today + pd.Timedelta(" 1 day")) #This is a datetime object. 

df.order_date + pd.Timedelta("1Y")

#Duration

today = datetime.date.today()
one_year_from_today = today + pd.Timedelta(days=365)

one_year_from_today-today #This is time delta of 365 days. 

(one_year_from_today-today)/pd.Timedelta(days=7) #This is dividing by one week to get number of weeks. 


# DATE SEQUENCES

pd.date_range(start = pd.to_datetime("2011-01"), periods = 10) #There should be 10 time periods. 

pd.date_range(start = pd.to_datetime("2011-01"), periods = 10, freq="2D") #This is time period of every 2 days for 10 periods. 

 
# PERIODS
# - Periods represent timestamps that fall within an interval using a frequency.
# - IMPORTANT: {sktime} requires periods to model univariate time series

# Convert to Time Stamp

df['order_date'].dt.to_period(freq='W') #Label is lumped in the same week. 


df['order_date'].dt.to_period(freq='D')


df['order_date'].dt.to_period(freq='M')


df['order_date'].dt.to_period(freq='Q')

# Get the Frequency

#Conversion to a timestamp

df['order_date'].dt.to_period(freq='M').dt.to_timestamp() #This changes it to a datetime64. 

# TIME-BASED GROUPING (RESAMPLING)
# - The beginning of our Summarize by Time Function

# Using kind = "timestamp"

df[['order_date', 'total_price']].set_index('order_date').resample("M").sum() #This will total up our price by month. 

#Single Time series using kind = "timestamp"

bike_sales_m_df = df[['order_date', 'total_price']].set_index('order_date').resample("MS", kind = "timestamp").sum() #This gives us by month start. 

bike_sales_m_df

# Using kind = "period"

df[['category_2', 'order_date', 'total_price']].set_index('order_date') #Set date column to index which is required for resample. 

df[['category_2', 'order_date', 'total_price']].set_index('order_date').groupby('category_2')

df[['category_2', 'order_date', 'total_price']].set_index('order_date').groupby('category_2').resample('M', kind = 'period')


df[['category_2', 'order_date', 'total_price']].set_index('order_date').resample('M', kind = 'period').agg(np.sum)

#We need a wide data frame and do that per below. 

df[['category_2', 'order_date', 'total_price']].set_index('order_date').groupby('category_2').resample('M', kind = 'period').agg(np.sum).unstack('category_2')
 
df[['category_2', 'order_date', 'total_price']].set_index('order_date').groupby('category_2').resample('M', kind = 'period').agg(np.sum).unstack('category_2').reset_index().assign(order_date = lambda x:x['order_date'].dt.to_period().set_index('order_date'))

df['order_date']=pd.to_datetime(df['order_date'])

#Grouped time series using kind = "period". 

bike_sales_cat2_m_wide_df = (
    df[['category_2', 'order_date', 'total_price']]
    .set_index('order_date')
    .groupby('category_2')
    .resample('M', kind='period')
    .agg(np.sum)
    .unstack('category_2')
    .reset_index()
)

bike_sales_cat2_m_wide_df
 
 
# MEASURING CHANGE

# Difference between previous timestamp from Previous Timestamp

#  - Single (No Groups)

bike_sales_m_df.assign(total_price_lag1 = lambda x: x['total_price'].shift(1)) #Previous total price value is being put in there. 

#Let us now get change from month to month. 

bike_sales_m_df.assign(total_price_lag1 = lambda x: x['total_price'].shift(1)).assign(diff = lambda x: x.total_price-x.total_price_lag1)

#We can now get plot:

bike_sales_m_df.assign(total_price_lag1 = lambda x: x['total_price'].shift(1)).assign(diff = lambda x: x.total_price-x.total_price_lag1).plot(y='diff')

#We can also use apply function:

bike_sales_m_df.apply(lambda x: x-x.shift(1)) #This creates the difference. 


#  - Multiple Groups: Key is to use wide format with apply

bike_sales_cat2_m_wide_df.apply(lambda x: x-x.shift(1))

#  - Difference from First Timestamp

bike_sales_m_df #We are trying to key in on first value which is 1-1-2011. 

bike_sales_m_df.apply(lambda x:(x-x[0])) #This subtracts all subsequent values from first value. 

# CUMULATIVE CALCULATIONS

bike_sales_m_df.resample('YS').sum() #Now we have how much revenue is generated per year. 

bike_sales_m_df.resample('YS').sum().cumsum() #This gives the cumulative values. So 2011+2012 would be 2012 one. 

bike_sales_m_df.resample('YS').sum().cumsum().reset_index().assign(order_date = lambda x: x.order_date.dt.to_period()).set_index('order_date').plot(kind = "bar")


# ROLLING CALCULATIONS

# Single

#Rolling mean is used to smooth out an average. 

bike_sales_m_df.assign(total_price_roll12 = lambda x: x['total_price'].rolling(window = 12)).mean()

# Groups - Can't use assign(), we'll use merging


