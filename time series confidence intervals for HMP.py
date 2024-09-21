import numpy as np
import pandas as pd
from tqdm import tqdm
from pmdarima import AutoARIMA
import matplotlib.pyplot as plt


# Load data from the first sheet
df = pd.read_excel("C:/Users/amrigupt/Downloads/whole2024ChangeEvents.xlsx")

# Convert 'Order_Date' to datetime and sort the dataframe by 'Order_Date'
df['EVENT_OCCUR_DATE'] = pd.to_datetime(df['EVENT_OCCUR_DATE'])
df = df.sort_values(by='EVENT_OCCUR_DATE')

# Set 'Order_Date' as the index
df.set_index('EVENT_OCCUR_DATE', inplace=True)

# Resample data to get monthly counts of events per CATEGORY_NAME
monthly_events = df.groupby('CATEGORY_NAME').resample('M').size().unstack(level=0, fill_value=0)

# Check for and handle missing values in the dataset
monthly_events = monthly_events.fillna(0)

# For Loop
# We will store results as dictionary.
model_results_list = []

for col in tqdm(monthly_events.columns):
    # Series Extraction
    y = monthly_events[col]
    
    # Debug: Print column name and check if series is empty
    print(f"Processing column: {col}")
    if y.empty or y.sum() == 0:
        print(f"No data available for category: {col}")
        continue
    
    # Ensure the index is datetime with a specified frequency
    y.index = pd.to_datetime(y.index)
    y = y.asfreq('M')
    
    # Plot the time series data
    plt.figure(figsize=(10, 6))
    plt.plot(y, label='Observed')
    plt.title(f'Time Series for {col}')
    plt.legend()
    plt.show()
    
    # Modeling with AutoARIMA
    forecaster = AutoARIMA(sp=12, suppress_warnings=True)
    
    # Fit model with error handling
    try:
        forecaster.fit(y)
    except ValueError as e:
        print(f"Error fitting model for category {col}: {e}")
        continue
    
    h = 12
    
    # Predictions and Confidence Intervals
    try:
        predictions, conf_int_df = forecaster.predict(fh=h, return_conf_int=True, alpha=0.05)
    except ValueError as e:
        print(f"Error predicting for category {col}: {e}")
        continue
    
    # Handle length mismatch
    if len(predictions) < h:
        predictions = np.append(predictions, [np.nan] * (h - len(predictions)))
    if len(conf_int_df) < h:
        conf_int_df = np.vstack([conf_int_df, [[np.nan, np.nan]] * (h - len(conf_int_df))])
    
    # Combine predictions and confidence intervals into a DataFrame
    forecast_index = pd.date_range(start=y.index[-1] + pd.DateOffset(months=1), periods=h, freq='M')
    forecast_df = pd.DataFrame({
        "prediction": predictions,
        "ci_low": conf_int_df[:, 0],
        "ci_hi": conf_int_df[:, 1],
        "CATEGORY_NAME": col
    }, index=forecast_index)
    
    # Append to list
    model_results_list.append(forecast_df)

# Combine all results into a single DataFrame
if model_results_list:
    model_results_df = pd.concat(model_results_list, axis=0)
    print("Model results combined successfully.")
else:
    print("No valid forecasts were produced.")

# Save the combined DataFrame to a new Excel file
output_file_path = '/mnt/data/forecast_results.xlsx'
model_results_df.to_excel(output_file_path, sheet_name='Forecasts')

print(f"Forecast results saved to {output_file_path}")

# Display the DataFrame in Jupyter Notebook
model_results_df.head()

model_results_list

