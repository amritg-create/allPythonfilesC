# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Module 7 (Plotnine): Plot Anatomy ----

# Imports

import pandas as pd
import numpy as np

from my_pandas_extensions.database import collect_data
from my_pandas_extensions.timeseries import summarize_by_time
from my_pandas_extensions.forecasting import arima_forecast

from plotnine import *
import plotnine

from plotnine.ggplot import ggplot
from plotnine.geoms import geom_col

ggplot 

# Data

df = collect_data()

# VISUALIZATION ----

# Step 1: Data Summarization

bike_sales_y_df = df.summarize_by_time(date_column = 'order_date', value_column = 'total_price', rule= 'Y', kind = 'timestamp')

#We can now reset the index:

bike_sales_y_df = df.summarize_by_time(date_column = 'order_date', value_column = 'total_price', rule= 'Y', kind = 'timestamp').reset_index()
bike_sales_y_df


# Step 2: Plot ----
# - Canvas: Set up column mappings
# - Geometries: Add geoms
# - Format: Add scales, labs, theme

(ggplot(mapping=aes(x='order_date', y= 'total_price'), data = bike_sales_y_df))

#Geometries

+geom_col()




# Saving a plot ----


# What is a plotnine plot? ----

