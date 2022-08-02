#!/usr/bin/env python
# coding: utf-8

# # Sorting and tagging customers depending on their LTV

# ## Sorting

# In[1]:


## Bubble sort

def my_sort(xs, f=lambda x: x):
    for i in range(len(xs) - 1):
        for j in range(i, len(xs)):
            if f(xs[i]) < f(xs[j]):
                xs[i], xs[j] = xs[j], xs[i]
    return xs


# In[2]:


my_sort([-1,2,5,-5,6])


# In[3]:


## Bubble sort for dictionaries
def my_sort_dict(xs, f=lambda x:x[1]):
    xs = [(k,v) for k,v in xs.items()]
    return {k: v for (k,v) in my_sort(xs,f)}


# In[4]:


test_dict = {"Customer1": 5000,
 "Customer2": 2500,
 "Customer3": 8000}


# In[5]:


my_sort_dict(test_dict)


# ## Apply to our dataset

# In[6]:


import pandas as pd
import sqlite3


# In[7]:


conn = sqlite3.connect("churn.db")


# In[8]:


LTV = pd.read_sql("select CustomerID, TotalCharges from churn_all", conn).set_index("CustomerID").T.to_dict("records")[0]


# In[9]:


LTV


# In[10]:


my_sort_dict(LTV)


# ## Tagging our customers

# In[11]:


def create_segment(df, LTV_col, target_col, LTV_value, upper_segment="High", lower_segment="Low"):
    df[target_col] = df[LTV_col].map(lambda x: upper_segment if x > LTV_value else lower_segment)
    return df


# In[12]:


df = pd.read_sql("select * from churn_all", conn)


# In[13]:


LTV_Value = df.TotalCharges.quantile(0.80)


# In[14]:


LTV_Value


# In[15]:


churn_tagged = create_segment(df, "TotalCharges", "LTV_Segment", LTV_Value)


# In[16]:


churn_tagged.head()


# In[17]:


churn_tagged["LTV_Segment"].value_counts()


# ## Creating the LTV_Analysis class

# In[18]:


class LTV_Analysis:
    
    def __init__(self):
        pass
    
    ## Bubble sort

    def my_sort(self,xs, f=lambda x: x):
        for i in range(len(xs) - 1):
            for j in range(i, len(xs)):
                if f(xs[i]) < f(xs[j]):
                    xs[i], xs[j] = xs[j], xs[i]
        return xs
    
    ## Bubble sort for dictionaries
    
    def my_sort_dict(self, xs, f=lambda x:x[1]):
        xs = [(k,v) for k,v in xs.items()]
        return {k: v for (k,v) in my_sort(xs,f)}
    
    ## Segmetation function
    
    def create_segment(self, df, LTV_col, target_col, LTV_value, upper_segment="High", lower_segment="Low"):
        df[target_col] = df[LTV_col].map(lambda x: upper_segment if x > LTV_value else lower_segment)
        return df


# In[19]:


l = LTV_Analysis()


# In[20]:


l.my_sort_dict(LTV)


# In[21]:


l.create_segment(df, "TotalCharges", "LTV_Segment", LTV_Value)


# In[ ]:




