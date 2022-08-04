#!/usr/bin/env python
# coding: utf-8

# # INTRODUCTION TO SQLITE AND ITS USAGE WITH PYTHON

# In[1]:


import sqlite3


# ## Create a connection , a table and add data 

# In[2]:


# Create connection (db)

conn = sqlite3.connect ('Example2.db')


# In[3]:


# Create a cursor

cur = conn.cursor ()


# In[4]:


# Create table

cur.execute("CREATE TABLE customer (First_Name TEXT, Last_Name TEXT, Age INTEGER, Income REAL)")


# In[5]:


# Insert a row in the table

cur.execute("INSERT INTO customer VALUES ('Soundharya', 'K', '23', '28000')")


# In[6]:


# Save results

conn.commit()


# ## Connect to an existing database

# In[8]:


conn = sqlite3.connect ('Example2.db')
cur = conn.cursor ()


# In[10]:


# Run simple query
cur.execute("SELECT * FROM customer")
cur.fetchone()


# In[11]:


for row in cur.execute("SELECT * FROM customer"):
    print(row)


# ## Add several rows

# In[12]:


customer_list = [
    ("Sri", "Ambani", 58, 90000.0),
    ("Sandeep","Desai", 20, 25000),
    ("Kajal", "Agarwal", 35, 98845.5)
]


# In[14]:


cur.executemany("INSERT INTO customer VALUES (?,?,?,?)", customer_list)


# In[15]:


for row in cur.execute("SELECT * FROM customer"):
    print(row)


# In[16]:


conn.commit()


# In[17]:


conn.close()


# ## Run queries

# In[19]:


conn = sqlite3.connect ('Example2.db')
cur = conn.cursor ()


# In[20]:


cur.execute("SELECT * FROM customer WHERE First_Name = 'Soundharya'")
cur.fetchall()


# In[22]:


cur.execute("SELECT * FROM customer WHERE Last_Name = 'Desai'")
cur.fetchall()


# In[23]:


cur.execute("SELECT * FROM customer WHERE Last_Name = 'jhons'")
cur.fetchall()


# In[24]:


cur.execute("SELECT * FROM customer ORDER BY Last_Name")
cur.fetchall()


# In[25]:


cur.execute("SELECT SUM(Income) FROM customer")
cur.fetchone()


# In[29]:


conn.commit()


# In[26]:


conn.close()


# In[ ]:





# In[27]:


conn.commit()


# In[30]:


conn = sqlite3.connect ('Example2.db')
cur = conn.cursor ()


# In[31]:


conn.commit()


# In[32]:


conn.close()


# In[33]:


conn.commit()

