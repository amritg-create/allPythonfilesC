# BUSINESS SCIENCE UNIVERSITY

# COURSE: DS4B 201-P PYTHON MACHINE LEARNING
# MODULE 0: MACHINE LEARNING & API'S JUMPSTART 
# PART 1: PYCARET
# ----

# GOAL: Make an introductory ML lead scoring model
#  that can be used in an API

# LIBRARIES

import os
import pandas as pd
import sqlalchemy as sql
import pycaret.classification as clf


# 1.0 READ DATA ----

# Connect to SQL Database ----

engine = sql.create_engine("sqlite:///00_database/crm_database.sqlite")

conn = engine.connect()

sql.inspect(engine).get_table_names() #Get names of tables in the database. 

# * Subscribers ---

subscribers_df = pd.read_sql(sql = "SELECT * FROM Subscribers", con = conn) #This pulls the subscribers table from the database. 

# * Transactions

transactions_df = pd.read_sql(sql = "SELECT * FROM Transactions", con=conn) #This pulls in all the transactions. We are interested in if user has made purchase. 


# *Close Connection ----

conn.close()

# 2.0 SIMPLIFIED DATA PREP ----

#Let's join subscribers data frame with transactions and get it in right format for machine learning. 

subscribers_df #We are juts going to use the member rating and country code for now. 

#We also need to join subscribers df with whoever made a transaction. 

subscribers_joined_df = subscribers_df

emails_made_purchase = transactions_df['user_email'].unique() #This removes all the duplicates. 

subscribers_joined_df['user_email'].isin(emails_made_purchase) #This should give a bunch of trues and falses. 

subscribers_joined_df['made_purchase']= subscribers_joined_df['user_email'].isin(emails_made_purchase).astype('int') #this now makes it ones and zeros. 

subscribers_joined_df

# 3.0 QUICKSTART MACHINE LEARNING WITH PYCARET ----

#Goal- Make a probability score for how likely someone is to make a purchase. 

# * Subset the data ----

df = subscribers_joined_df[['member_rating', 'country_code', 'made_purchase']] #These are all predictive features. 

# * Setup the Classifier ----

#clf.setup() #Used to initialize the machine learning environment and set up the experiment. It prepares the dataset for training and testing by performing feature preprocessing. 

clf_1 = clf.setup(data=df, target = 'made_purchase', train_size = 0.8, session_id = 123)

clf_1

# * Make A Machine Learning Model ----

xgb_model = clf.create_model(estimator = 'xgboost')
xgb_model




# * Finalize the model ----


# * Predict -----


# * Save the Model ----



# * Load the model -----



# CONCLUSIONS:
# * Insane that we did all of this in 90 lines of code
# * And the model was better than random guessing...
# * But, there are questions that come to mind...

# KEY QUESTIONS:
# * SHOULD WE EVEN TAKE ON THIS PROJECT? (COST/BENEFIT)
# * MACHINE LEARNING MODEL - IS IT GOOD?
# * WHAT CAN WE DO TO IMPROVE THE MODEL?
# * WHAT ARE THE KEY FEATURES IN THE MODEL?
# * CAN WE EXPLAIN WHY CUSTOMERS ARE BUYING / NOT BUYING?
# * CAN THE COMPANY MAKE A RETURN ON INVESTMENT FROM THIS MODEL?


