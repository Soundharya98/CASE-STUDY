#!/usr/bin/env python
# coding: utf-8

# # Churn case. Part 2. Analysis of LTV

# Lifetime value (LTV) is the total worth to a business of a customer over the while period of their relationship. It's an important metric as it costs less to keep existings customers than to acquire new ones, so the idea of increasing the value of your existig customers is a great way to drive growth. 

# In[1]:


import sqlite3
import pandas as pd


# In[2]:


conn = sqlite3.connect("churn.db")


# In[3]:


df = pd.read_sql("select * from churn_all", conn)


# In[4]:


df.head()


# ## 1. For those customers who unsubscribed the service, what was their average LTV? and how long did they usually stay in the service?

# In[5]:


## Extract those who unsubscribed the serviced (Churn = Yes)

churn_df = pd.read_sql("select * from churn_all where Churn = 'Yes'", conn)


# In[7]:


# Examine the distribution of TotalCharges
churn_df["TotalCharges"].describe()


# We can see that around 20% of the TotalCharges are very high, so let's divide the data to see each distribution.

# In[8]:


# Find the 80th percentile of the data in TotalCharges
churn_df.TotalCharges.quantile(0.8)


# In[9]:


pd.read_sql("select * from churn_all where TotalCharges <= 2840.41", conn)


# In[10]:


churn_df.query("TotalCharges <= 2840.41")


# In[11]:


# Divide the data by the 80th percentile of the data from the TotalCharges variable
total_charges_under80 = churn_df.query("TotalCharges <= 2840.41")
total_charges_above80 = churn_df.query("TotalCharges > 2840.41")


# In[12]:


# Show the distribution of people under the 80th percentile
total_charges_under80.TotalCharges.describe()


# In[13]:


# Show the distribution of people above the 80th percentile
total_charges_above80.TotalCharges.describe()


# In[14]:


# Show the distribution of the tenure of people under the 80th percentile
total_charges_under80.Tenure.describe()


# In[15]:


# Show the distribution of the tenure of people above the 80th percentile
total_charges_above80.Tenure.describe()


# The average LTV of the 80% of those who unsubscribed is \\$ 711, and their tenure is near 10 months. On the hand, the average LTV of the 20 % of those who unsubscribed is $ 4811, and their tenure is near 50 months.  

# ## 2. What kinds of services they subscribed when they were still a customer?

# ### PhoneService

# In[22]:


# under 80
pd.read_sql("select count(1) from churn_all where TotalCharges <= 2840.41 and Churn = 'Yes' group by PhoneService", conn)


# In[25]:


df["Gender"].value_counts() # example


# In[23]:


# under 80
total_charges_under80.PhoneService.value_counts()


# In[26]:


# Example of shape
df.shape


# In[27]:


# Under 80 (percentage)
total_charges_under80.PhoneService.value_counts() / total_charges_under80.shape[0]


# In[28]:


# Above 80 (percentage)
total_charges_above80.PhoneService.value_counts() / total_charges_above80.shape[0]


# For the top 20% (high LTV) only 2% of them didn't use the phone service. On the other hand, lower 80% (LTV) had around 11% of the people that didn't use the phone service. That is around 5 times more as the top 20%. Apparently if you are not subscribed to the phone service you are more likely to be in the bottom 80% of the LTV. We as a company can try to sell this service to more people.

# ### MutipleLines

# In[31]:


total_charges_under80_use_phone = total_charges_under80.query("PhoneService == 'Yes'")

total_charges_under80_use_phone.MultipleLines.value_counts() / total_charges_under80_use_phone.shape[0]


# In[32]:


total_charges_above80_use_phone = total_charges_above80.query("PhoneService == 'Yes'")

total_charges_above80_use_phone.MultipleLines.value_counts() / total_charges_above80_use_phone.shape[0]


# For the top 20% of LTV who used the phone service 84% of them used multiple lines, which is 2 times as much as the proportion of people in the low 80% LTV that is around 40%. Having multiple lines is going to get you closer to be in the top 20% of the LTV.

# ### InternetService

# In[33]:


# Under 80 (percentage)
total_charges_under80.InternetService.value_counts() / total_charges_under80.shape[0]


# In[34]:


# Above 80 (percentage)
total_charges_above80.InternetService.value_counts() / total_charges_above80.shape[0]


# All the people in the high 20% LTV used internet service. On the other hand 8% of the people in the low 80th percentile of the LTV did not have internet connection. Also, in the top 20% (high LTV) 90% of them had fiber optic, in comparison to only 64% in the low LTV. So as a company if we want to increase the LTV of customers, we should recommend using internet and Fiber Optic connection.

# ### Other services

# In[35]:


import numpy as np


# In[36]:


total_charges_under80_use_internet = total_charges_under80.query('InternetService!="No"')
proportion_internet_sub_service_under80 = np.array([total_charges_under80_use_internet.query('OnlineSecurity=="Yes"').shape[0]/total_charges_under80_use_internet.shape[0],
total_charges_under80_use_internet.query('TechSupport=="Yes"').shape[0]/total_charges_under80_use_internet.shape[0],
total_charges_under80_use_internet.query('OnlineBackup=="Yes"').shape[0]/total_charges_under80_use_internet.shape[0],
total_charges_under80_use_internet.query('DeviceProtection=="Yes"').shape[0]/total_charges_under80_use_internet.shape[0],
total_charges_under80_use_internet.query('StreamingTV=="Yes"').shape[0]/total_charges_under80_use_internet.shape[0],
total_charges_under80_use_internet.query('StreamingMovies=="Yes"').shape[0]/total_charges_under80_use_internet.shape[0]])


# In[37]:


proportion_internet_sub_service_under80


# In[38]:


total_charges_above80_use_internet = total_charges_above80.query('InternetService!="No"')
proportion_internet_sub_service_above80 = np.array([total_charges_above80_use_internet.query('OnlineSecurity=="Yes"').shape[0]/total_charges_above80_use_internet.shape[0],
total_charges_above80_use_internet.query('TechSupport=="Yes"').shape[0]/total_charges_above80_use_internet.shape[0],
total_charges_above80_use_internet.query('OnlineBackup=="Yes"').shape[0]/total_charges_above80_use_internet.shape[0],
total_charges_above80_use_internet.query('DeviceProtection=="Yes"').shape[0]/total_charges_above80_use_internet.shape[0],
total_charges_above80_use_internet.query('StreamingTV=="Yes"').shape[0]/total_charges_above80_use_internet.shape[0],
total_charges_above80_use_internet.query('StreamingMovies=="Yes"').shape[0]/total_charges_above80_use_internet.shape[0]])


# In[39]:


proportion_internet_sub_service_above80


# In the top 20% LTV, both streaming movies and streaming tv percentages are around 80%, in comparison in the low 80% LTV they are around 40%. Device protection and online backup for the top 20% LTV are around 55%, in comparison to only around 22% in the low LTV. As a company we would like to sell to customers streaming TV and movies and also online backup and device protection if we want to increase LTV.

# ## 3. For those who churned what is the proportion of each kind of contract?

# In[40]:


# Under 80 (percentage)
total_charges_under80.Contract.value_counts() / total_charges_under80.shape[0]


# In[41]:


# Above 80 (percentage)
total_charges_above80.Contract.value_counts() / total_charges_above80.shape[0]


# ## 4. For those who did not churn what is the proportion of each kind of contract?

# In[42]:


## Extract those who unsubscribed the services (Churn = Yes)

paying_df = pd.read_sql("select * from churn_all where Churn = 'No'", conn)


# In[43]:


paying_df.TotalCharges.describe()


# In[44]:


# Find the 80th percentile of the data in TotalCharges
paying_df.TotalCharges.quantile(0.8)


# In[45]:


# Divide the data by the 80th percentile of the data from the TotalCharges variable
paying_total_charges_under80 = paying_df.query("TotalCharges <= 4895.8")
paying_total_charges_above80 = paying_df.query("TotalCharges > 4895.8")


# In[46]:


# Under 80 (percentage)
paying_total_charges_under80.Contract.value_counts() / paying_total_charges_under80.shape[0]


# In[47]:


# Above 80 (percentage)
paying_total_charges_above80.Contract.value_counts() / paying_total_charges_above80.shape[0]


# - If we want to stop Churning we would like to sell contracts to people for at least one year, and much better for 2 years (Conjecture).
# - We have 57% of the people that stayed in the company in the top 20% LTV with 2 year contracts, and only 11% of the people in the top 20% had a 2 year contract and left the company.
# - 95% of the people that left the company and are in the low 80% have a month-to-month contract, in contrast to only 50% of the people in the low 80% that stayed in the company. We can say that having a month-to-month contract is one of the reasons that people are leaving the company (conjecture).
