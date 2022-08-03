#!/usr/bin/env python
# coding: utf-8

# # Introduction to PANDAS with SQLite

# In[1]:


import pandas as pd
import sqlite3
import warnings
warnings.filterwarnings("ignore")


# ## Create a connection

# In[2]:


conn = sqlite3.connect("Example2.db")
cur = conn.cursor()


# In[3]:


cur.execute("SELECT * FROM customer")
cur.fetchall()


# ## Creation of a Dataframe(PANDAS)

# In[4]:


df = pd.read_sql_query("SELECT * FROM customer", conn)


# In[5]:


df


# ## Run queries for PANDAS

# In[6]:


pd.read_sql("SELECT * FROM customer", conn)


# In[7]:


pd.read_sql("SELECT * FROM customer WHERE Age = 35", conn)


# In[8]:


pd.read_sql("SELECT First_Name, Income FROM customer", conn)


# In[9]:


pd.read_sql("SELECT First_Name, Income FROM customer")


# In[10]:


pd.read_sql("SELECT First_Name, Income FROM customer ORDER BY First_Name", conn)


# ## Read CSV files from PANDAS

# In[11]:


pd.read_csv("Sample.csv")


# In[12]:


sample_df = pd.read_csv("Sample.csv")


# In[13]:


type(sample_df)


# In[14]:


sample_df.head(3)


# ## Creating a table in Sqlite from a CSV file with PANDAS

# In[15]:


sample_df = pd.read_csv("Sample.csv")


# In[16]:


sample_df.to_sql("sample_table", conn, if_exists = "replace", index = False )


# In[17]:


pd.read_sql("SELECT * FROM sample_table", conn)


# In[20]:


sample_df.columns


# ## Function to get all the tables information

# In[18]:


conn = sqlite3.connect("Example2.db")
cur = conn.cursor()


# In[21]:


def table_info(conn, cursor):
    """
    prints out all of the columns of every table in the DB
    
    conn: database connection object
    cursor: cursor object
    """
    
    tables = cur.execute("SELECT Name FROM sqlite_master WHERE type = 'table'; ").fetchall()
    for table_name in tables:
        table_name = table_name[0]
        table = pd.read_sql_query("SELECT * FROM {} LIMIT 0".format(table_name), conn)
        print(table_name)
        for col in table.columns:
            print("\t "+ col)
            print()


# In[22]:


table_info(conn, cur)


# ## See the table schema with SQLite

# In[23]:


cur.execute("PRAGMA table_info('customer')").fetchall()

Every row includes:

- index of the column
- Column Name 
- Data type 
- Whether or not the column can be NULL
- The default value for the column
- The primary key in the result is 0 for columns that are not the primary key
# In[24]:


conn.commit()


# In[25]:


conn.close()


# In[ ]:




