# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# SQL DATABASES (Module 2): Working with SQLAlchemy ----

# IMPORTS ----

import pandas as pd
import sqlalchemy as sql

import os

os.mkdir("./00_database") #This makes a new directory for database. 

# CREATING A DATABASE ----

# Instatiate a database

engine = sql.create_engine("sqlite:///00_database/bike_orders_database.sqlite") #instantiates an engine from a SQL URL connection string.

#First two slashes above are required to connect to SQLite database. 
#Third slash is because we are connecting to a SQLite database at a file location. 

conn = engine.connect() #Connects your sql alchemy object to your database. This creates a connection object. 

#In memory versus out of memory databases is as follows. In memory DB doesnt permanently save a database to a file location. 

#out of memory or file database is good for storing data. 

# Read Excel Files

bikes_df = pd.read_excel("./00_data_raw/bikes.xlsx")
bikeshops_df = pd.read_excel("./00_data_raw/bikeshops.xlsx")
orderlines_df = pd.read_excel("./00_data_raw/orderlines.xlsx")

# Create Tables

#Next we will create tables in our bikes order database. 

bikes_df.to_sql("bikes", con=conn.connection)
pd.read_sql("select * FROM bikes", con = conn.connection) #We have added this table to our bike orders database. Let's do same thing for bike shops. 

bikeshops_df.to_sql("bikeshops", con=conn.connection)
pd.read_sql("select * FROM bikeshops", con=conn.connection)

#We see unnamed column is being generated in orderlines table. We can grab indices by their indice location using df.iloc. 

#We don't want 0 location so we put a 1 below. 

orderlines_df.iloc[: , 1:].to_sql("orderlines", con = conn.connection, if_exists = "replace") #This takes everything from 1 to the end.  
pd.read_sql("select * FROM orderlines", con = conn.connection)

# Close Connection

conn.close()

# RECONNECTING TO THE DATABASE 

# Connecting is the same as creating

engine = sql.create_engine("sqlite:///00_database/bike_orders_database.sqlite")

conn = engine.connect()

# GETTING DATA FROM THE DATABASE

# Get the table names

engine.table_names() #You can get table names. 

inspector = sql.inspect(conn) 

inspector.get_schema_names() #These are all schemas in database which refers to if your database has different configurations. 

inspector.get_table_names() #Returns the table names from an inspector object that is connected to your database. 

# Read the data and getting data out of your tables. 

table = inspector.get_table_names()
pd.read_sql(f"SELECT * FROM {table[0]}", con = conn.connection)

#Close Connection

conn.close()
