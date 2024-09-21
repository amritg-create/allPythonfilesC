# DS4B 101-P: PYTHON FOR DATA SCIENCE AUTOMATION ----
# SQL DATABASES (Module 2): Working with SQLAlchemy ----

#We are going to create a function. This will be collect data function. 

#We want to automate some of the process for importing data from SQL database. 

#In our sales analysis, we did some ETL or some data wrangling or data transformation.  

# IMPORTS ----

import sqlalchemy as sql
import pandas as pd

# FUNCTION DEFINITION ----

def my_function (a=1):
    b = 1
    return a+b

my_function() #This returns 2 for above function. 

my_function(a=2)

def collect_data(conn_string = "sqlite:///00_database/bike_orders_database.sqlite"):
    """
    Collects and combines the bike orders data. 

    Args:
        conn_string (str, optional): SQL Alchemy connection string to find database. Defaults to "sqlite:///00_database/bike_orders_database.sqlite".
    Returns:
        DataFrame: A pandas dataframe that combines data from tables:
        -orderlines: Transactions data. 
        -bikes: Products data. 
        -bikeshops: Customers data. 
    """
    
    # Body
    
    # 1.0 Connect to database
    
    engine = sql.create_engine(conn_string)
    
    conn = engine.connect()
    
    table_names = ['bikes', 'bikeshops', 'orderlines']
    
    data_dict = {} #A dictionary is a key-value pair in Python. The data with table name can be stored as key-value pair. 
    for table in table_names:
        data_dict[table] = pd.read_sql(f"SELECT * FROM {table}", con = conn.connection) \
            .drop("index", axis=1)
    
    conn.close()
        
    #2.0 Combining data
    
    data_dict['bikes'] #We want to drop index column. We do this above. 
    data_dict['orderlines']
    
    joined_df = pd.DataFrame(data_dict['orderlines']) \
        .merge(
            right = data_dict['bikes'],
            how = 'left',
            left_on = 'product.id', 
            right_on = 'bike.id'
        ) \
        .merge(
            right = data_dict['bikeshops'],
            how = 'left',
            left_on = 'customer.id', 
            right_on = 'bikeshop.id'
        )
        
    #3.0 Cleaning the data (Wrangle data and get it transformed it in right format)
    
    joined_df.info() #We need to convert order_date from object to datetime. 
    
    df = joined_df
    
    df['order.date'] = pd.to_datetime(df['order.date']) #Converts it from object to datetime. 
    
    temp_df = df['description'].str.split(" - ", expand= True)
    df['category.1'] = temp_df[0]
    df['category.2'] = temp_df[1]
    df['frame_material'] = temp_df[2]
    
    temp_df = df['location'].str.split(", ", expand= True)
    df['city'] = temp_df[0]
    df['state'] = temp_df[1]
    
    df['total.price'] = df['quantity'] * df['price']
    
    df.columns
    
    cols_to_keep_list = ['order.id', 'order.line', 'order.date',
       'quantity', 'price', 'total.price', 'model',
       'category.1', 'category.2',
       'frame_material', 'bikeshop.name', 'city', 'state']
    
    df = df[cols_to_keep_list] #Put above columns in df frame. 
    
    df.columns = df.columns.str.replace(".", "_") #This replaces dots in column names with underscores. 
    
    #df.info()
    
    return df

collect_data() #This runs function above. 

