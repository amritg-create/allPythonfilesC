# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Module 5 (Programming): Functions ----

# Imports

import pandas as pd
import numpy as np
from pandas.core import groupby
from pandas.core.series import Series
import os
os.chdir('C:\\Users\\amrigupt\OneDrive - Cisco\\Desktop\\First Course Python Data Science Automation\\DS4B_101P_Course')

from my_pandas_extensions.database import collect_data


df = collect_data()

# 1.0 EXAMINING FUNCTIONS ----

# Pandas Series Function
# ?pd.Series.max
# ?np.max

#max is a method of the series class. 
#Methods are just functions that are part of a python class. 
#They are both made with "def" keyword which defines functions. 
#The only difference is when a class is made, the method is instantiated within the class. 
#Max is a method wihch is a function which is part of the series call. 

#?pd.Series.max

df.total_price #This total_price is a pandas series so it should work with .max function. 

pd.Series.max('A')

my_max = pd.Series.max #We are creating our own function. 
my_max(df.total_price)  #What is max of total price? 

type(my_max) #This is a function. 
type(df)


# Pandas Data Frame Function
# pd.DataFrame.aggregate

pd.DataFrame.aggregate(self = df[['total_price']], func = np.quantile, q = 0.5) #This gets us the median


#Df.aggregate (q=0.5) will get sent to np.quantile via kwargs. 


# 2.0 OUTLIER DETECTION FUNCTION ----
# - Works with a Pandas Series

x = df['total_price']

def detect_outliers(x, iqr_multiplier = 1.5, how = "both"): #This iqr multiplier creates a named argument. 
    """
    Used to detect outliers using 1.5 IQR Method. 

    Args:
        x (Pandas series): Should be a numeric pandas series. 
        iqr_multiplier (int, float, optional): A multiplier used to modify sensitivity. Must be positive. Lower values. Defaults to 1.5.
        how (str, optional): One of both upper or lower. Defaults to "both".

    Raises:
        Exception: _description_
        Exception: _description_
        Exception: _description_
        Exception: _description_

    Returns:
        [Pandas series]: Boolean series which flags outliers as True/False. 
    """
    
    #CHECKS
    if type(x) is not pd.Series:
        raise Exception("x must be a Pandas series")
    
    if not isinstance(iqr_multiplier, (float,int)):
        raise Exception("The IQR multiplier must be an int or float data type.")
    
    if iqr_multiplier <=0:
        raise Exception("IQR multiplier must be a positive value.")
    
    how_options = ['both', 'upper', 'lower']
    if how not in how_options:
        raise Exception(f"Invalid 'how'. Expected one of {how_options}")
    
    #IQR Logic
    
    q75 = np.quantile(x, 0.75)
    q25 = np.quantile(x,0.25)
    iqr = q75-q25
    
    lower_limit = q25-iqr_multiplier*iqr
    upper_limit = q75+iqr_multiplier*iqr
    
    outliers_upper = x >= upper_limit #This gives us boolean values. 
    outliers_lower = x <= lower_limit
    
    if how == "both":
        outliers = outliers_upper | outliers_lower #This will check both of these series and return true if either is true. 
    elif how == "lower":
        outliers = outliers_lower
    else:
        outliers = outliers_upper
        
    return outliers



detect_outliers(df['total_price'], iqr_multiplier= 0.5, how = "lower") #This returns just lower outliers.

df[detect_outliers(df['total_price'], iqr_multiplier= 0.1)] #This gives us values that are outliers. 


detect_outliers(df['total_price'], iqr_multiplier="abc") #This will throw an informative error message that we hve above. 
detect_outliers(df['total_price'], how="abc") #This gives us error. 

#Groupby Example- testing outliers witin groups. 

df.groupby("category_2").apply(lambda x:x[detect_outliers(x= x['total_price'], iqr_multiplier=1.5, how ='upper')])

# 3.0 EXTENDING A CLASS ----

pd.Series.detect_outliers = detect_outliers

df['total_price'].detect_outliers()