# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Module 3 (Pandas Core): Data Structures ----

# IMPORTS ----

import pandas as pd
import numpy as np

from my_pandas_extensions.database import collect_data

df = collect_data() #This should pull in our SQL data set. 

# 1.0 HOW PYTHON WORKS - OBJECTS

# Objects

#Everyhing in Python is an object. Frame is a submodule to core. Data frame is the class of object. 

type(df)

# Objects have classes

type(df).mro() #There is inheritance structure. It inherits from data frame class, the base pandas object, etc. that are in output. 

#In Python, objects get methods and attributes from the classes that they inherit it from. 

# Objects have attributes

#Attributes is metadata that exists for an object. 

df.shape #Shape is attribute of an object that returns number of rows and columns for an object. 

# Objects have methods

#A method is a function that can be applied to that object class. 

#Query is an example of a method. 

df.query("model == 'Jekyl'") #This tells you if there is anything in the model column that is "Jekyl"


# 2.0 KEY DATA STRUCTURES FOR ANALYSIS

# - PANDAS DATA FRAME

df

#Dataframe has column and index attributes. It is key structure that holds columns of panda series. 

# - PANDAS SERIES

df['order_date'].dt.year #This can be done for a series but not a year. 

#A series that is of the datetime64 has an attribute called dt. From that attribute, we can grab the year out. 

#Dataframes have series and each series have their own methods which differ from pandas dataframe. 

# - NUMPY ARRAY

#Pandas series are built on top of numpy arrays. 

#The series adds an index and metadata like series name. 

df['order_date'].values #This is an attribute. It pulls out an attribute. 

#Data Types

type(df['price'].values).mro() #This inherits object. 

#Numpy holds information and holds data as different data types. 

# 3.0 DATA STRUCTURES - PYTHON

# Dictionaries

d = {'a':1} #This is of class dictionary when you do type below. 
type(d)

d.keys() #a is the key. 

# Lists

#Lists are commonly used for iteration. 

l = [1, "A", [2, "B"]]

#You commonly access lists by their index position. 

l[1]

list(d.values())[0] #You can coerce the above dictionary into a list. 


# Tuples

#This is an immutable list. 

#They are used in pandas for storing data frame shape and multi-index column names. 

type(df.shape) #This is tuple data type. 

type(df.shape).mro() #This is a tuple and object. 

t = (10,20)

# Base Data Types

df.total_price #Int64 is extension of int class where it specifies how many bytes its supposed to take. 

# Casting- this is converting one data type to another. 

model = 'Jekyll Carbon 2'
price = 6070

f"The first model is : {model}" #We can then form a sentence with model from above. 

#The below will not work. 

price + "some text"

#Therefore you should do below:

str(price) + " some text"

int("50%".replace('%', "")) #This casts this value to an integer. 

#range() makes a range object that defines how to generate a sequence of numbers. 

type(range(1,50)).mro() #Range is a generator. It provides a specification for how to generate a sequence. 

#This is a memory saving strategy that only creates the range when you need it. 

r = list(range(1,50)) #This generates the numbers in that range. This is calling casting to a list. 

np.array(r)

pd.Series(r)

pd.Series(r).to_frame() #Converts to a dataframe which is a higher level object. A series is also a higher level object than a list. 

# Converting column data types from one data type to another. 

df['order_date'].astype('str') #pandas series have methods to change. This converts it to object class. 

#s.astype above converts a series from one data type to another. 

df['order_date'].astype('str').str.replace('-', '/') #This converts format of order date column to another format. 




