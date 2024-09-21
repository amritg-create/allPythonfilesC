# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----

# Module 6 (Sktime): Introduction to Forecasting ----

# Imports

import pandas as pd
import pandas as pd 
pd.__version__
import numpy as np

from my_pandas_extensions.database import collect_data

df = collect_data()

from my_pandas_extensions.timeseries import summarize_by_time

# Sktime Imports

from sktime.forecasting.arima import AutoARIMA

#Progress Bars

from tqdm import tqdm #This adds a progress bar. 

# 1.0 DATA SUMMARIZATIONS ----

#We need data in the right format. Forecast has to be arranged by a time series. 

bike_sales_m_df = df \
    .summarize_by_time(
        date_column = 'order_date',
        value_column = 'total_price',
        rule = "M",
        kind = 'timestamp'
    )
    
bike_sales_m_df

bike_sales_cat2_m_df = df \
    .summarize_by_time(
        date_column = 'order_date',
        value_column = 'total_price',
        groups = ['category_2'],
        rule = 'M'
    )
    
bike_sales_cat2_m_df


# 2.0 SINGLE TIME SERIES FORECAST ----

bike_sales_m_df.plot() #This produces our time series. 

#ARIMA is autoregressive integrated moving average. 

#Forecasting takes the historical demand data and predicts the next "h" observations into the future. 

bike_sales_m_df

y = bike_sales_m_df['total_price'] #This is a pandas series. 
y

#Dataset currently is a monthly time series. AutoARIMA is not good at figuring out seasonality. It however wont know if dataset is seasonal. 

#We therefore add SP argument below. We will give it a value of 12 so every 12 observations is a cycle. This is monthly data set. 

forecaster = AutoARIMA(sp=12)

forecaster.fit(y) #The fit method trains the forecaster object to learn from the data (y). 

forecaster.predict(fh = np.arange(1,13)) #This gives forecaster for the next 12 observations. 

#You can also do forecasting for the next 24 periods by doing the following. 

#Predictions

h=24
forecaster.predict(fh = np.arange(1,h+1)) #FH is forecaster horizon. 

#AutoARIMA CONFIDENCE INTERVALS

#These confidence intervals measure how confident we are in the estimate. 

#These are "prediction estimates" based on in-sample estimates. 

#These are not out of sample (gold standard) for confidence/accuracy measurement. 

#Sktime has methods to do out of sample, which requires a second round of training to get accuracy metrics like RMSE, MAE, etc. 

forecaster.predict(fh = np.arange(1,h+1), return_pred_int = True) #This produces a tuple. We have our predictions and lower and upper bound. 

#We can control upper and lower bound with the alpha argument. 

forecaster.predict(fh = np.arange(1,h+1), return_pred_int = True, alpha = 0.2) #This gives us 80% confidence range. 

#We can now save this as a predictions tuple. 

predictions_ci_tuple = forecaster.predict(fh = np.arange(1,h+1), return_pred_int = True, alpha = 0.95)
predictions_ci_tuple
type(predictions_ci_tuple) 

predictions_ci_tuple[0] #This gives us predictions. 

predictions_ci_tuple[1] #This gives us the upper and lower bounds. 

#We can also save this in another way per below. Predictions series is first element and confidence interval is second element. 

#Confidence Intervals

predictions, conf_int_df = forecaster.predict(fh = np.arange(1,h+1), return_pred_int = True, alpha = 0.05)

conf_int_df

#FORECAST VISUALIZATION

from sktime.utils.plotting import plot_series

plot_series(y) #This plots our series for us. 

plot_series(y, predictions, conf_int_df['lower'], conf_int_df['upper'], labels = ['actual', 'predictions', 'ci_lower', 'ci_upper']) #We now have confidence intervals. 


# 3.0 MULTIPLE TIME SERIES FORCAST (LOOP) ----

bike_sales_cat2_m_df.head()
bike_sales_m_df.head()

df = bike_sales_cat2_m_df

df.columns

df.columns[0]

df[df.columns[0]] #This is total price for cross country race and is series. 

#For Loop

#We will print each of the column names. 

#We will store results as dictionary. 

model_results_dict = {}

for col in tqdm(df.columns):
    
    #Series Extraction
    
    y= df[col]
    
    # Ensure the index is datetime with a specified frequency
    y.index = pd.to_datetime(y.index)
    y = y.asfreq('M') 
    
    #Modeling 
    
    forecaster = AutoARIMA(sp=12, suppress_warnings=True)
    
    forecaster.fit(y)
    
    h=12
    
    #Predictions and Confidence Intervals
    
    predictions, conf_int_df = forecaster.predict(fh=np.arange(1,h+1), return_pred_int= True, alpha = 0.05)
    
    #Combine into Data Frame
    
    ret = pd.concat([y, predictions, conf_int_df], axis = 1) #joining the data, predictions and confidence interval lower and upper bounds. 
    ret.columns= ["value", "prediction", "ci_low", "ci_hi"] #Naming the columns of the data frame. 
    
    #Update dictionary 
    
    model_results_dict[col] = ret
    
    model_results_dict  
    
model_results_df = pd.concat(model_results_dict, axis = 0)

#Visualize

model_results_dict[('total_price','Cross Country Race')].plot()

model_results_dict[list(model_results_dict.keys())[4]].plot()



