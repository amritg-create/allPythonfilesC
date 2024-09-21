# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# Week 2 (Data Wrangling): Data Wrangling ----

# IMPORTS

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from my_pandas_extensions.database import collect_data #Grab from database submodule. 

# DATA

df = collect_data()

# 1.0 SELECTING COLUMNS

# Select by name

['order_date', 'order_id', 'order_line'] #Let's say i just want these 3 columns. 

df[['order_date', 'order_id', 'order_line']]


# Select by position or location

df.iloc[:,0:3] #This gives you the specific columns. 

df.iloc[:, -3:] #This gives you the last three columns. 

# Select by text matching

#Easiest way to do by text match is through filter function. This is used to filter based on column or row index using text patterns. 

df.filter(regex = "(^model)|(^cat)", axis = 1) #This is what we call regex pattern where we take columns that have "model" or the word "cat" in them. 

#For above, the ^ means "starts with". The term $ means "ends with". 

df.filter(regex = "price$", axis = 1) #This grabs any column that ends in price. 

# Rearranging columns

#We want to have model as the first column. 

l = df.columns.tolist() #This converts a column or row index to a list, which is iterable. 

l.remove('model') #This removes the model column from the list. 

df[['model', *l]] #The asterisk function converts a nested list to an unnested list. 

df #The idea here is that we now have model as the first column. 

#The above takes columns which is an index object and casts it to a list. 

#What if we want to rearrange multiple columns? LETS GO OVER THAT BELOW.

#Single approach for rearranging multiple columns.

l = df.columns.to_list()
l

l.remove('model')
l.remove('category_1')
l.remove('category_2')
l

#We now make a list of the ones we want to keep after we take out the above. 

df[['model', 'category_1', 'category_2', *l]]

#METHOD 2- REARRANGING MULTIPLE COLUMNS THROUGH LIST COMPREHENSION

l = df.columns.tolist()

cols_to_front = ['model', 'category_1', 'category_2', *l] #These are columns we want to keep and move to the front. 

cols_to_front

l2 = [col for col in l if col not in cols_to_front] #This negates cols_to_front. 

df[[*cols_to_front, *l2]]


# Select by data types

#Up until now, we have used column names to rearrange. Other ways we can do it is by rearranging data frames by taking chunks of data frame out. 

#we can do this via select data types via select_dtypes. 

df.info()

df.select_dtypes(include=object) #selects columns and subsets by data type. This one includes all columns that are of class object. 

df1 = df.select_dtypes(include=object) #You can give it a string or list and it either takes include or exclude. 

#Let's say we wanted to move all string object columns to the front. 

df2 = df.select_dtypes(exclude=object) #This includes all of the non-string columns. 
df2

#pd.concat combines multiple data frames contained in a list. 

pd.concat([df1, df2], axis = 1) #Axis = 1 is for column. Df1 is things in front and df2 is things in back. 

#Another way of moving these columns to front is as follows. 

df[['model', 'category_1', 'category_2']]

df.drop(['model', 'category_1', 'category_2'], axis = 1)

#Use the below three lines of code to move things to the front. 

df1 = df[['model', 'category_1', 'category_2']]
df2 = df.drop(['model', 'category_1', 'category_2'], axis = 1)
pd.concat([df1, df2], axis = 1)

# Dropping Columns (De-selecting)

# 2.0 ARRANGING ROWS ----

df.sort_values('total_price') #It goes from lowest to largest

df.sort_values('total_price', ascending = False)

df.sort_values('order_date')

#We can also do the same thing with pandas series. 

df['price'].sort_values()


# 3.0 FILTERING  ----

# Simpler Filters

#Row filtering with boolean series involves key concept being that we need to create a "boolean series"
#This is a pandas series that consists of only true or false values. We use this to subset or data frame rowwise. 

#Let's take all rows with a date greater than or equal to 2015. 

df.order_date #We need to convert this to true/false wehre it's true if we want a year greater than or equal to 2015. 

df.order_date >= pd.to_datetime("2015-01-01") #we get true or falses with this. 

df[df.order_date >= pd.to_datetime("2015-01-01")] #We have just created a rowwise filter using a boolean series. 

#let's say we want to hone in on specific model that appears in specifc rows: 

df[df.model == 'Trigger Carbon 1'] #We get everything with Trigger Carbon 1. 

#Let's say we want all rows that starts with Trigger Carbon 1:

df[df.model.str.startswith("Trigger")]

#Let's say we want all rows that contain "Carbon":

df[df.model.str.contains("Carbon")] #These are all the models which contain carbon. 

# Query

#df.query() is a string based rowwise filtering method.

price_threshold = 5000

df.query("price >= @price_threshold") #This gives where price is greater than or equal to price threshold. You always need @ symbol for variable. 

#What if we wanted to do multiple queries like this? 

price_threshold_1 = 9000
price_threshold_2 = 1000

df.query("(price >= @price_threshold_1) | price <= @price_threshold_2")

#How do you do this without the @ symbol? 

df.query(f"price >= {price_threshold_1}") #This does the same thing as the aobve but without the @symbol. 

# Filtering Items in a List

#Another common scenario is when you have items in a list. 

df['category_2'].unique() #These are unique ones for category 2. 

#Let's say we want to filter data frame using subset of these. 

df[df['category_2'].isin(['Triathalon', 'Over Mountain'])] #This gives you all rows which have Triathalon or Over Mountain. 

df[~df['category_2'].isin(['Triathalon', 'Over Mountain'])] #This gives you everything that is not Triathalon or Over Mountain using the tilda sign. 

# Slicing

df[:5] #This grabs the first 5 rows. 


df.tail(5) #This gives us the last 5 rows of the data frame. 

# Index Slicing- tihs takes a look at indices and you can slice based on that. 

df.iloc[0:5] #This also grabs the first five rows. 

df.iloc[0:5, [1,3,5]] #Let's say we want columns 1, 3 and 5 and the first 5 rows. 

#[loc] is used for row and column selection with names. 
#iloc is used for index positoins. 

df.iloc[0:5, :] #This gives you all columns and rows 0-5. 

df.iloc[:, [1,3,5]] #This gives you all rows and columns 1, 3 and 5. 

# Unique / Distinct Values- Let's say you want unique combinations of rows within dataframes. 

df[['model', 'category_1', 'category_2', 'frame_material']] #you now have 15644 rows but some are duplicates. 

df[['model', 'category_1', 'category_2', 'frame_material']].drop_duplicates() #This drops duplicates. 


# Top / Bottom- let's say we want largest orders. 

df.nlargest(n= 20, columns= 'total_price') #This gives you rows with 20 highest total prices. 

#You can do same thing with series as well. 

df['total_price'].nlargest(n=20)

df.nsmallest(n=20, columns = 'total_price') #Do this one for HMP

df['total_price'].nsmallest(n=20) 


# Sampling Rows

df.sample(n=10, random_state = 123) #This sample will always return the same 10 rows. 

#Sometimes we dont know how may we need but we have a fraction we want. Then we do this:

df.sample(frac = 0.10, random_state = 123) #This returns roughly 10% of our data. 


# 4.0 ADDING CALCULATED COLUMNS (MUTATING) ----


# Method 1 - Series Notations

df2 = df.copy() #Makes a copy of the main dataframe so we don't accidentally overwrite it. 

df2['new_col'] = df2['price'] * df2['quantity']
df2

df2['new_col_2'] = df['model'].str.lower() #This is the model column but everything is in lower case. 
df2

# Method 2 - assign (Great for method chaining)

#df.assign supports method chaining. We just need to follow lambda function syntax. 

#Let's make the column lowercase. 

df.assign(frame_material = lambda x: x['frame_material'].str.lower()) #x is same thing as df here. We are then adding lambda x, lambda is anonymous function. 

#We can also make new columns via this approach:

df.assign(frame_material_lower = lambda x: x['frame_material'].str.lower()) #This creates a new column. 

#How might we use assign in progression as we use method chains?

df[['model', 'price']].drop_duplicates().set_index('model') #This sets index as being model and price is our column. 

hist = df[['model', 'price']].drop_duplicates().set_index('model').plot(kind = 'hist') #We see this histogram is pretty skewed. 

#One way to compensate for this skew (has outliers) is via log transformation. 

df[['model', 'price']].drop_duplicates().assign(price = lambda x: np.log(x['price'])).set_index('model').plot(kind = 'hist') #This is log transformation. 

# Adding Flags (True/False)

"Supersix Evo".lower().find("supersix") >= 0 #This means that it finds the term "supersix" and therefore gives True as output.   

"Beast of the East".lower().find("supersix") #This gives -1 which means it's not present. 

df.assign(flag_supersix = lambda x: x['model'].str.lower().str.contains("supersix")) #This adds true or false column at the end. 

df['model'].str.lower().str.contains("supersix")


# Binning- this is a great way to convert numeric data to groups based on their values. 

pd.cut(df.price, bins = 3, labels = ['low', 'medium', 'high']).astype(str) #This creates 3 bins based on price. 

df[['model', 'price']].drop_duplicates().assign(price_group = lambda x: pd.cut(x.price, bins = 3)) #We now have our groupings. 

#Visualizing above binning strategy

df[['model', 'price']].drop_duplicates().assign(price_group = lambda x: pd.cut(x.price, bins = 3)).pivot(index = 'model', columns = 'price_group', values = 'price').style.background_gradient(cmap = 'blues')

#Quantile Binning- should be used 99% of the time. 

pd.qcut(df.price, q = [0, 0.33, 0.66, 1], labels = ['low', 'medium', 'high'])

#Let's now create a visualization for quantile cutting like we have done above for the non-quantile binning:

df[['model', 'price']].drop_duplicates().assign(price_group = lambda x: pd.qcut(x.price, q = 3)).pivot(index = 'model', columns = 'price_group', values = 'price').style.background_gradient(cmap = 'blues')

# 5.0 GROUPING  ----

# 5.1 Aggregations (No Grouping)

df[['total_price']].sum().to_frame() #This returns the sum of total price as a dataframe. 

df.select_dtypes(exclude = ['object']) #We get only numeric columns when we do this. 

df.select_dtypes(exclude = ['object']).drop('order_date', axis = 1) #We have just numeric columns now. 

df.select_dtypes(exclude = ['object']).drop('order_date', axis = 1).sum() #This gives us summary metrics. 

#With df.agg function, we can specifically target columns and apply more than one aggregating function. 

df.agg([np.sum, np.mean, np.std])

df.agg({'quantity': np.sum, 'total_price': [np.sum, np.mean]}) #This gives sum of quantity and total_price columns. 

# Common Summaries

df['model'].value_counts()

df[['model', 'category_1']].value_counts() #This is a data frame that gives you back the number with two columns. Use for HMP. 

df.nunique() #This gives you number of unique values for each line item. 

df.isna().sum() #Missing data- This returns a data frame that has true and false for every cell in data frame. You stack with sum function and for each column that's false, it tallies up 0s and 1s. 

# 5.2 Groupby + Agg

df.groupby(['city', 'state']).sum()

df.groupby(['city', 'state']).agg(dict(total_price = np.sum, quantity = np.sum))

# Get the sum and median by groups

df[['category_1', 'category_2', 'total_price']] #We have just columns that I want to aggregate by. 

df[['category_1', 'category_2', 'total_price']].groupby(['category_1', 'category_2'])

df[['category_1', 'category_2', 'total_price']].groupby(['category_1', 'category_2']).agg([np.sum, np.median]) #This is summarization (sum and median). 

summary_df_1 = df[['category_1', 'category_2', 'total_price']].groupby(['category_1', 'category_2']).agg([np.sum, np.median]).reset_index()


# Apply Summary Functions to Specific Columns

df[['category_1', 'category_2', 'total_price', 'quantity']]

df[['category_1', 'category_2', 'total_price', 'quantity']].groupby(['category_1', 'category_2']) #Group by category 1 and category 2. 

df[['category_1', 'category_2', 'total_price', 'quantity']].groupby(['category_1', 'category_2']).agg({'quantity': np.sum, 'total_price': np.sum})

summary_df_2 = df[['category_1', 'category_2', 'total_price', 'quantity']].groupby(['category_1', 'category_2']).agg({'quantity': np.sum, 'total_price': np.sum}).reset_index()

summary_df_2

# Detecting NA

summary_df_1.columns

#Let's say we want to see if there are missing values in here:

summary_df_1.isna().sum() #This gives you sum of missing values. 


# 5.3 Groupby + Transform (Apply)
# - Note: Groupby + Assign does not work. No assign method for groups.

df[['category_2', 'order_date', 'total_price', 'quantity']]

#Let's now create a summary data frame of the above by weekly frequency. 

df[['category_2', 'order_date', 'total_price', 'quantity']].set_index('order_date')

#Now let's add a group by variable and resample order date by weekly. 

df[['category_2', 'order_date', 'total_price', 'quantity']].set_index('order_date').groupby('category_2').resample("W")

#Now lets do aggregation. 

summary_df_3 = df[['category_2', 'order_date', 'total_price', 'quantity']].set_index('order_date').groupby('category_2').resample("W").agg(np.sum).reset_index() #This aggregates by week. 

df[['category_2', 'order_date', 'total_price', 'quantity']].set_index('order_date').groupby('category_2').resample("W").agg(np.sum).reset_index()

summary_df_3 #This is a time series. 

summary_df_3.set_index('order_date').groupby('category_2').apply(lambda x: (x.total_price.mean())/ x.total_price.std()) #This is called centering when we remove average. 

summary_df_3.set_index(['order_date', 'category_2']).groupby('category_2').apply(lambda x: (x-x.mean()/x.std())) #We get scaling for total price and quantity by category_2. 
                                                                                 
summary_df_3.set_index(['order_date', 'category_2']).groupby('category_2').apply(lambda x: (x-x.mean()/x.std() )).reset_index()                                                                                 

# 5.4 Groupby + Filter (Apply)

df.tail(5)

summary_df_3.groupby('category_2').tail(5) #This gives us last 5 observations by group. 

summary_df_3.groupby('category_2').apply(lambda x: x.iloc[10:20]) #This is 10-20 for each of the indices. 

# 6.0 RENAMING Columns ----

# Single Index

summary_df_2 #Let's say we wanted to replace all the underscores in here. 

summary_df_2.rename(columns = dict(category_1 = "Category 1")) #This allows us to rename a column. 

summary_df_2.columns.str.replace("_", " ").str.title() #This gives us a capital letter and the title case for column names. 

summary_df_2.rename(columns = lambda x: x.replace("_", " ").title()) #This gives us a more professional looking table. 

# Targeting specific columns

summary_df_2 #Let's suppose total price to be something else like revenue. 

summary_df_2.rename(columns = {'total_price': 'Revenue'}) #We just renamed total_price column to Revenue. 

# - Mult-Index

summary_df_1.columns #We might want to flatten these columns as it's multi-indice. 

"_".join(('category_1',       '')) #This will join the first piece and last piece. 

["_".join (col) for col in summary_df_1.columns.to_list()] #This joins the columns together. 

summary_df_1.set_axis(["A", "B", "C", "D"], axis = 1) #This renames the columns to A, B, C and D. 

# 7.0 RESHAPING (MELT & PIVOT_TABLE) ----

# Aggregate Revenue by Bikeshop by Category 1 

df[['bikeshop_name', 'category_1', 'total_price']].groupby(['bikeshop_name', 'category_1']).sum() #This gives sum of total_price by bikeshop name and category.

df[['bikeshop_name', 'category_1', 'total_price']].groupby(['bikeshop_name', 'category_1']).sum().reset_index()

df[['bikeshop_name', 'category_1', 'total_price']].groupby(['bikeshop_name', 'category_1']).sum().reset_index().sort_values('total_price', ascending= False)

bikeshop_revenue_df = df[['bikeshop_name', 'category_1', 'total_price']].groupby(['bikeshop_name', 'category_1']).sum().reset_index().sort_values('total_price', ascending= False).rename(columns = lambda x: x.replace('_', ' ').title())

bikeshop_revenue_df

# 7.1 Pivot & Melt 

# Pivot (Pivot Wider)

#Wide format is good for reporting. 

bikeshop_revenue_df.pivot(index = ['Bikeshop Name'], columns = 'Category 1', values = ['Total Price']) #I have made wider the table. 

bikeshop_revenue_df.pivot(index = ['Bikeshop Name'], columns = 'Category 1', values = ['Total Price']).reset_index() #This gives us initial columns back. 

#If we want to get rid of multilevel index as that doesnt look good for report, we can do below:

bikeshop_revenue_wide_df = bikeshop_revenue_df.pivot(index = ['Bikeshop Name'], columns = 'Category 1', values = ['Total Price']).reset_index().set_axis(["Bikeshop Name", "Mountain", "Road"], axis = 1)

#Now i might want to do formatting:

bikeshop_revenue_wide_df.plot(x = "Bikeshop Name", y = ["Mountain, Road"], kind = "barh")

#Let's sort values now. 

bikeshop_revenue_wide_df.sort_values("Mountain", ascending=False) #We get a table that has the highest at the top. 

#Now lets format this:

bikeshop_revenue_wide_df.sort_values("Mountain", ascending=False).style.highlight_max() #This highlights the maximum values. 

from mizani.formatters import dollar_format

bikeshop_revenue_wide_df.sort_values("Mountain", ascending=False).style.highlight_max().format({"Mountain" : lambda x: "$" + str(x)})

# Melt (Pivoting Longer)

from plotnine import (ggplot, aes, geom_col, facet_wrap, theme_minimal, coord_flip)

ggplot(mapping = aes(x= "Bikeshop Name", y = "Revenue", fill = "Category_1"), data = bikeshop_revenue_wide_df) + geom_col() + coord_flip() + facet_wrap("Category_1")+theme_minimal

# 7.2 Pivot Table (Pivot + Summarization, Excel Pivot Table) GRAPHING FOR HMP

df #This is our raw data. 

#df.pivot_table() converts raw data into summarized tables by combining pivoting and aggregation into 1 function. 

#Let's take an example of one pivot table. 

df.pivot_table(columns=None, values = 'total_price', index = 'category_1', aggfunc= np.sum)

#We can do another pivot table:

df.pivot_table(columns='frame_material', values = 'total_price', index = 'category_1', aggfunc= np.sum) #Frame material is the column here. 

df.pivot_table(columns=None, values = 'total_price', index = ['category_1', 'frame_material'], aggfunc= np.sum) 

df.assign(year = lambda x: x.order_date.dt.year) #This gives another column for year on the right. 

df.assign(year = lambda x: x.order_date.dt.year).pivot_table(index = "year", aggfunc=np.sum['category_1', "category_2"])

# 7.3 Stack & Unstack ----



# Unstack - Pivots Wider 1 Level (Pivot)

# Stack - Pivots Longer 1 Level (Melt)


# 8.0 JOINING DATA ----

orderlines_df = pd.read_excel("00_data_raw/orderlines.xlsx")

bikes_df = pd.read_excel("00_data_raw/bikes.xlsx")

# Merge (Joining)

#bike ID from bikes_df matches product ID from orderlines_df. 

pd.merge(left = orderlines_df, right = bikes_df, left_on = "product.id", right_on = "bike.id")

# Concatenate (Binding)

#Concatenating or binding is the equivalent of pasting two data frames together. The data frames can be joined row-wise or column-wise. 

#The best practice is to have them have the same index structure (either same columns or same rows depending on the bind). 

# Rows

df_1 = df.head(5) #This gives us the first 5 rows. 
df_2 = df.tail(5)

pd.concat([df1, df2],axis = 0)

# Rows 

df_1 = df.iloc[:,5]
df_2 = df.iloc[:,-5:] #These are last 5 columns. 

pd.concat([df_1, df_2], axis = 1) #These are the 10 columns. 

#MAKE SURE YOUR DATA HAS THE SAME ROW INDEX IF JOINING COLUMN WISE. MAKE SURE IT HAS SAME COLUMN INDEX IF JOINING ROW WISE. 

# 9.0 SPLITTING (SEPARATING) COLUMNS AND COMBINING (UNITING) COLUMNS

#Splitting text columns into multiple columns using delimiters. 

# Separate

#let's separate year month and day. 

df['order_date'].astype('str') #Use the astype method to coerce the order date from datetime object to a string.

df['order_date'].astype('str').str.split("-", expand = True)  #Splits a pandas series using a text delimiter. Here we now have year, month and day. 

df['order_date'].astype('str').str.split("-", expand = True).set_axis(["year", "month", "day"], axis = 1) #This gives year, month and day column names. 

#We can now get this into original data frame:

df_2 = df['order_date'].astype('str').str.split("-", expand = True).set_axis(["year", "month", "day"], axis = 1)

#Then do the below

df[["year", "month", "day"]] = df_2

df_2

# Combine

df_2['year'] + "-" + df_2['month'] + "-" + df_2['day'] #We have now recombined it into year-month-day format. 



# 10.0 APPLY 
# - Apply functions across rows 

sales_cat_2_daily_df= df[['category_2', 'order_date', 'total_price']].set_index('order_date').groupby('category_2').resample('D').sum()
sales_cat_2_daily_df

sales_cat_2_daily_df.apply(np.mean)

sales_cat_2_daily_df.groupby('category_2').apply(lambda x: np.repeat( np.mean(x), len(x) )) #We should get the mean by group. 

#Grouped Transform

sales_cat_2_daily_df.groupby('category_2').transform(np.mean)


# 11.0 PIPE 
# - Functional programming helper for "data" functions

data = df

def add_column(data, **kwargs): #User will enter kwargs as key-value pairs to add new columns. 
    
    data_copy = data.copy() #This will make a copy of initial dataframe. 
    
    #print(kwargs)
    
    data_copy[list(kwargs.keys())] = pd.DataFrame(kwargs)
    
    return data_copy 

add_column(df, total_price_2 = df.total_price *2)

#The problem however with above is we cannot method chain with our handy new function. 

#This means we need to save an intermediate data frame before we can apply our function, which slows down our productivity. 

df.pipe(add_column, category_2_lower = df['category_2'].str.lower())

#Challenge Problem 1

df.columns
summary_stuff = df[['bikeshop_name', 'order_date', 'total_price']]
summary_stuff = summary_stuff.set_axis(["id", "date", "value"], axis = 1)
summary_stuff.columns
summary_stuff.set_index('date').groupby('id').resample('YS').agg(np.sum).reset_index
summary_stuff

#Part 2 Challenge Problem 1

summary_stuff['date']
summary_stuff_1 = summary_stuff.assign(date = lambda x: x['date'].dt.year).pivot(index = 'id', columns = 'date', values = 'value')

