# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Module 4 (Time Series): Profiling Data ----


# IMPORTS


import pandas as pd
from ydata_profiling import ProfileReport, profile_report

from my_pandas_extensions.database import collect_data #This is database module. 

df = collect_data() #Allows you to import data from database. 
df #This is dataframe loaded in. 

# PANDAS PROFILING

# Get a Profile


profile = ProfileReport(df = df) #Save as profile. 

profile #We just made an object of the Profile Report class. This is called instantiation. 
#Our report is an object that has combined the dataframe that is and input which gets processed and turned into a ProfileReport object. 

#High cardinality is a term which means having many values that are very infrequent. 

# Sampling - Big Datasets

df.profile_report()

df.sample(frac = 0.5).profile.report()




# Pandas Helper
# ?pd.DataFrame.profile_report


# Saving Output

df.profile_report().to_file("04_time_series/profile_report.html")


# VSCode Extension - Browser Preview




# %%
