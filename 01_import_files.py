# DS4B 101-P: PYTHON FOR BUSINESS ANALYSIS ----
# Module 2 (Pandas Import): Importing Files ----

# IMPORTS ----

import pandas as pd



# 1.0 FILES ----

# - Pickle ----

#Used to store python/pandas objects. 

#You want to save format as pickle file most of the time. 

pickle_df = pd.read_pickle("00_data_wrangled/bike_orderlines_wrangled_df.pkl")
pickle_df.info()

#Pickle file will save in save format as original file unlike CSV. For datetime, for example, it's saved as datetime whereas for CSV, it's saved as an object. 

# - CSV ----

#CSV is relatively fast to load in Python compared to Excel. 

#Therefore, we will want to use parse_dates to preserve same format for order date as original object. 

csv_df = pd.read_csv("00_data_wrangled/bike_orderlines_wrangled_df.csv", parse_dates= ['order_date']) #We parse column here to be specified as order date. 
csv_df.info()

# - Excel ----

excel_df = pd.read_excel("00_data_wrangled/bike_orderlines_wrangled_df.xlsx")
excel_df.info()

