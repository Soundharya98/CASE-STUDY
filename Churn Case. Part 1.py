#!/usr/bin/env python
# coding: utf-8

# # Churn case. Part 1.

# In[1]:


import pandas as pd


# ## Reading all CSV files with Pandas

# In[11]:


customer = pd.read_csv("customer.csv")
customer.head()


# In[12]:


cust_loc = pd.read_csv("cust_loc.csv")
cust_loc.head()


# In[13]:


cust_services = pd.read_csv("cust_services.csv")
cust_services.head()


# In[14]:


cust_account = pd.read_csv("cust_account.csv")
cust_account.head()


# In[10]:


cust_account.dtypes


# In[15]:


cust_churn = pd.read_csv("cust_churn.csv")
cust_churn.head()


# ## Create database and tables

# In[2]:


import sqlite3


# In[3]:


conn = sqlite3.connect("churn.db")
cur = conn.cursor()


# In[11]:


# Create customer table
customer.to_sql("customer", conn, if_exists="replace", index=False)


# In[12]:


# Create customer location table
cust_loc.to_sql("cust_loc", conn, if_exists="replace", index=False)


# In[13]:


# Create customer services table
cust_services.to_sql("cust_services", conn, if_exists="replace", index=False)


# In[14]:


# Create customer accountcust_account table
cust_account.to_sql("cust_account", conn, if_exists="replace", index=False)


# In[15]:


# Create customer churn table
cust_churn.to_sql("cust_churn", conn, if_exists="replace", index=False)


# ## Information about our tables

# In[4]:


def table_info(conn,cursor):
    """
    prints out all of the columns of every table in the DB
    
    conn: database connection object
    cursor: cursor object
    """
    
    tables = cur.execute("SELECT name FROM sqlite_master WHERE type='table';").fetchall()
    for table_name in tables:
        table_name = table_name[0]
        table = pd.read_sql_query("SELECT * from {} LIMIT 0".format(table_name), conn)
        print(table_name)
        for col in table.columns:
            print("\t "+ col)
            print()


# In[5]:


table_info(conn,cur)


# ## Join all tables

# In[6]:


cur.execute(
"""
ALTER TABLE cust_loc
RENAME COLUMN Cust_ID TO CustomerID;
""")


# In[7]:


table_info(conn,cur)


# In[9]:


cur.execute(
"""
SELECT 
*
FROM customer
INNER JOIN cust_loc
USING (CustomerID)
""")
cur.fetchone()


# In[17]:


cust_loc = cust_loc.rename(columns={"Cust_ID": "CustomerID"})


# In[18]:


cust_loc.head()


# In[19]:


pd.concat([customer,cust_loc], join="inner", axis=1)


# In[20]:


# Rename remaining columns from tables
cust_services = cust_services.rename(columns={"Cust_ID": "CustomerID"})
cust_account = cust_account.rename(columns={"Account_id": "CustomerID"})
cust_churn = cust_churn.rename(columns={"Id": "CustomerID"})


# In[21]:


dfs_to_join = [customer, cust_loc, cust_services, cust_account, cust_churn]


# In[27]:


customer.loc[customer["Gender"] == "Male",]


# In[29]:


churn_all = pd.concat(dfs_to_join, join="inner", axis=1)


# In[34]:


churn_all = churn_all.loc[:, ~churn_all.columns.duplicated()]


# In[36]:


churn_all.head()


# In[37]:


churn_all.dtypes


# In[38]:


churn_all["TotalCharges"] = pd.to_numeric(churn_all["TotalCharges"], errors="coerce")


# In[39]:


churn_all.dtypes


# In[40]:


# Missing values
churn_all.isnull().sum(axis=0)


# In[41]:


# Drop the missing values
churn_all = churn_all.dropna()


# In[42]:


churn_all.isnull().sum(axis=0)


# In[44]:


churn_all.dtypes


# In[45]:


churn_all.to_sql("churn_all", conn, if_exists="replace", index=False)


# In[46]:


cur.execute("PRAGMA table_info('churn_all')").fetchall()


# In[47]:


pd.read_sql("select * from churn_all", conn)


# ## See all tables

# In[48]:


cur.execute("select name from sqlite_master where type='table'")
cur.fetchall()

