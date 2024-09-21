# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# JUMPSTART (Module 1): First Sales Analysis with Python ----

# Important VSCode Set Up:
#   1. Select a Python Interpreter: ds4b_101p
#   2. Delete terminals to start a fresh Python Terminal session

#Check current working directory

import os
#show current directory
print(os.getcwd()) 
from os import mkdir, getcwd
getcwd()

# 1.0 Load Libraries ----

## Load libraries

# Core Python Data Analysis

#%%

import pandas as pd
import numpy as np
np.sum([1,2,3])
import matplotlib.pyplot as plt
bikes_df = pd.read_excel("00_data_raw/bikes.xlsx")
bikes_df

bikeshops_df = pd.read_excel("00_data_raw/bikeshops.xlsx")
bikeshops_df

orderlines_df = pd.read_excel(
    io= "00_data_raw/orderlines.xlsx", 
    converters = {'order.date': str} #Convert order.date to string. Specify you want it to be a specific type of data type. Provide it a dictionary. 
    )

orderlines_df.info()

#%%

# Plotting
from plotnine import (
    ggplot, aes, 
    geom_col, geom_line, geom_smooth,
    facet_wrap, 
    scale_y_continuous, scale_x_datetime,
    labs,
    theme, theme_minimal, theme_matplotlib,
    expand_limits,
    element_text
)

from mizani.breaks import date_breaks
from mizani.formatters import date_format, currency_format


# Misc
import os
from os import mkdir, getcwd
from rich import pretty
pretty.install()
getcwd()



# 2.0 Importing Data Files ----

# help(pd.read_excel)
# - Use "q" to quit

bikes_df = pd.read_excel("00_data_raw/bikes.xlsx")
bikes_df

bikeshops_df = pd.read_excel("00_data_raw/bikeshops.xlsx")
bikeshops_df

orderlines_df = pd.read_excel(
    io= "00_data_raw/orderlines.xlsx", 
    converters = {'order.date': str} #Convert order_date to string. 
    )

orderlines_df.info()

# 3.0 Examining Data ----

bikes_df
orderlines_df #product id in orderlines is the same as bike ID in bikes_df.  
bikeshops_df #Bikeshop ID in bikeshops_df is the same as customer.ID in orderlines df. 

#Examining frequency counts

s = bikes_df['description'] #Using bracket notation with single string returns a pandas series. Pandas series contains contents of description column. 
freq_count_series = s.value_counts() #How many of each entity in the description column? 
freq_count_series.nlargest() #This grabs 5 largest values. 

#Below is method chaining so we join the above together

bikes_df['description'].value_counts().nlargest()

#Both data frames and series have plot methods:

top5_bikes_series = bikes_df['description'].value_counts().nlargest()

#Let's now make the above a horizontal plot/bar chart:

fig = top5_bikes_series.plot(kind = "barh")
fig.invert_yaxis() #This inverts the axis
plt.show()

# 4.0 Joining Data ----

#We will first drop the unnecessary columns and then do merging with the other tables. 

orderlines_df = pd.DataFrame(orderlines_df)

bike_orderlines_joined_df = orderlines_df \
    .drop(columns='Unnamed: 0', axis=1) \
    .merge(
        right = bikes_df,
        how='left',
        left_on='product.id',
        right_on='bike.id'
    ) \
    .merge(
        right=bikeshops_df,
        how = 'left',
        left_on='customer.id',
        right_on='bikeshop.id'
    )

bike_orderlines_joined_df

# 5.0 Wrangling Data ----

# * No copy

df = bike_orderlines_joined_df



# * Copy

df2 = bike_orderlines_joined_df.copy() #Makes a copy of the data frame. 

df

# * Handle Dates

df['order.date']

df['order.date'] = pd.to_datetime(df['order.date']) #This will take that dataframe column and overrite it with series. Conversion of column to datetime. 
df.info()

# * Show Effect: Copy vs No Copy

bike_orderlines_joined_df.info()

# * Text Columns

#Some of these text columns need to be split up. 

# * Splitting Description into category_1, category_2, and frame_material

df.T #This transposes the table. 

#"Mountain - Over Mountain - Carbon" is an example description.

"Mountain - Over Mountain - Carbon".split(" - ") #This splits it up into a list of 3 different items. 

temp_df = df['description'].str.split(pat = ' - ', expand = True) #This returns a 3 column dataframe. How do we add that back to df?

df['category.1'] = temp_df[0]
df['category.1']

df['category.2'] = temp_df[1]
df['category.2']

df['frame.material'] = temp_df[2]
df['frame.material']

df #We have now added the above 3 columns that were separated to original data frame. 

# * Splitting Location into City and State

temp_df = df['location'].str.split(pat = ', ', n=1, expand = True)

df['city'] = temp_df[0]
df['state'] = temp_df[1]
df

# * Price Extended

df.T
df['total.price'] = df['quantity'] * df['price'] #This is total price or revenue column. 

df.sort_values('total.price', ascending=False) #This sorts total price column. 

# * Reorganizing

df.columns #This is an attribute of the DataFrame class.

#We are deciding to keep anything related to order like order line or order date. 

cols_to_keep_list = ['order.id', 
'order.line', 
'order.date', 
#'customer.id', 
#'product.id',
#'quantity', 
#'bike.id', 
'model', 
#'description', 
'quantity',
'price', 
'total.price',
#'bikeshop.id',
'bikeshop.name', 
'location', 
'category.1', 
'category.2',
'frame.material', 
'city', 
'state']

df = df[cols_to_keep_list]

# * Renaming columns- let's have underscores instead of dots in our column names. 

#Str.replace is a built in function that modifies a string by replacing patterns of text with a replacement. 

df['order.date']

df.columns = df.columns.str.replace(".", "_") #This replaces all column names with _ instead of .
df.columns

df
bike_orderlines_joined_df

bike_orderlines_wrangled_df = df
bike_orderlines_wrangled_df #This is the final one after all the data transformations. 

# 6.0 Visualizing a Time Series ----

#Now is a good time for us to save our work. 

mkdir("00_data_wrangled")

bike_orderlines_wrangled_df.to_pickle("00_data_wrangled/bike_orderlines_wrangled_df.pkl") 

df = pd.read_pickle("00_data_wrangled/bike_orderlines_wrangled_df.pkl") #DF is now same thing as bike orderlines wrangled. 

#The above writes our data frame or python object to binary file. You can then load this file and it gets returned in the same format that you saved it in. 

# 6.1 Total Sales by Month ----

df = pd.DataFrame(df)
df['order_date'] #This has datetime properties. 

order_date_series = df['order_date']

#The first thing we will do is take data frame and calculate total sales by month so we will have to use datetime time seris component. 

#We will subselect therefore 2 columns. This is order_date and total price. 

#df[[order_date]] is a list and returns a one column dataframe. 

#df.set_index converts column to an index. Datetime index is required for df.resample() method shown below. 

#df.resample() method returns resampling object that internally groups data based on frequency "rule". 

df[['order_date', 'total_price']].set_index('order_date') #This returns two column dataframe and we will use this to aggregate total prices. 

#Above we are using order_date as index. 

df[['order_date', 'total_price']].set_index('order_date').resample(rule = 'YS').sum() #We now have the total prices by year. 

df[['order_date', 'total_price']].set_index('order_date').resample(rule = 'MS').sum() #We now have the sales by month start. 

sales_by_month_df = df[['order_date', 'total_price']].set_index('order_date').resample(rule = 'MS').aggregate(np.sum).reset_index() #We now have two column data frame. 

sales_by_month_df

# Quick Plot ----

#We can do plot of sales by month. 

sales_by_month_df.plot(x = 'order_date', y = 'total_price')
plt.show()


# Report Plot ----

#Below is a bar chart. 

ggplot(mapping = aes(x= 'order_date', y= 'total_price'),data = sales_by_month_df) + \
    geom_col
    
#Below is a geom smoother:

ggplot(mapping = aes(x= 'order_date', y= 'total_price'),data = sales_by_month_df) + \
    geom_line() + \
    geom_smooth(method = "loess", se = False, color = "blue", span = 0.3)


# 6.2 Sales by Year and Category 2 ----

# ** Step 1 - Manipulate ----

df #We want to analyze category 2. Category 2 contains more depth to the features such as Over Mountain.

#We will use list approach below with 2 brackets to it on a weekly basis. 

#We are using function for total price below to aggregate total price by category. 

sales_by_month_cat_2 = df[['category_2', 'order_date', 'total_price']] \
    .set_index('order_date') \
    .groupby('category_2') \
    .resample('W') \
    .agg(func = {'total_price': np.sum}) \
    .reset_index()

sales_by_month_cat_2

# Step 2 - Visualize ----

# Simple Plot

#Below we get category_2 as columns, index as order date and the total price on a weekly basis of each category_2. 
#This fills in missing values with 0 with fill.na(0).

sales_by_month_cat_2 \
    .pivot(
        index = 'order_date',
        columns = 'category_2',
        values = 'total_price'
    ) \
    .fillna(0) \
    .plot()

plt.show()

#Below is a line chart with subplots on a 3x3 grid. 

sales_by_month_cat_2 \
    .pivot(
        index = 'order_date',
        columns = 'category_2',
        values = 'total_price'
    ) \
    .fillna(0) \
    .plot(kind="line", subplots=True, layout = (3,3))
plt.show()

# Reporting Plot (might be good for HMP). This is a faceted 3x3 plot with a linear trendline with sales by month and date breaks of 2 years. 


ggplot(
    mapping = aes(x = 'order_date', y='total_price'), 
    data= sales_by_month_cat_2
) + \
    geom_line(color = "#2c3e50") + \
    geom_smooth(method = "lm", se = False, color = "blue") + \
    facet_wrap(
        facets= "category_2", 
        ncol=3, 
        scales = "free_y"
    ) + \
    scale_y_continuous(labels = 'usd', size = 2) + \
    scale_x_datetime(
        breaks= date_breaks("2 years"),
        labels = date_format(fmt = "%Y-%m")
    ) + \
    labs(title = "Revenue by Week", x = "", y = "Revenue") + \
    theme_minimal() + \
    theme(
        subplots_adjust = {"wspace": 0.35},
        axis_text_y = element_text(size = 6),
        axis_text_x = element_text(size = 6)
        ) 
    
# 7.0 Writing Files ----

# Pickle ----

#Use pickle to save/load in the identical format you've been working in. 

df.to_pickle("00_data_wrangled/bike_orderlines_wrangled_df.pkl")

# CSV ----

df.to_csv("00_data_wrangled/bike_orderlines_wrangled_df.csv")


# Excel ----

df.to_excel("00_data_wrangled/bike_orderlines_wrangled_df.xlsx")


# WHERE WE'RE GOING
# - Building a forecast system
# - Create a database to host our raw data
# - Develop Modular Functions to:
#   - Collect data
#   - Summarize data and prepare for forecast
#   - Run Automatic Forecasting for One or More Time Series
#   - Store Forecast in Database
#   - Retrieve Forecasts and Report using Templates


