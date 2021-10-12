#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
import numpy as np
from sklearn import metrics
import matplotlib.pyplot as plt
import seaborn as sns
get_ipython().run_line_magic('matplotlib', 'inline')


# In[5]:


#reading your dataset

data = pd.read_csv(r'\Users\HP\Downloads\NIGERIA_DEMOGRAPHICS_DATA.csv')
print(data.head())


# In[6]:


#Getting the summary of your dataset from the end

data.tail()


# In[7]:


#Dropping colums that would not be used in the analysis

to_drop = ['In a short sentence, describe your government',
...            'Are you a Nigerian?',
...            'Are you Happy with your job?',
...            'If there was one thing you really wanted to own, what would that be?',
...            'Do you think Nigeria can get better?',
...            'Please fill your email if you want to be notified once this research is completed.'
...              ]


# In[8]:


data.drop(columns=to_drop, inplace=True)
print(data.tail())


# In[9]:


data['Occupation'].is_unique


# In[10]:


#Getting the individual datatype of each column

data.dtypes


# In[11]:


data.get_dtype_counts()


# In[12]:


#renaming some columns

data = data.rename(columns = {'Age Group':'Age','Are you married?':'Marital_status','What is your steady/constant income range in a month?':'Income_range','How much do you think you earn from all other sources of income in a month':'Other_Income','On an average, how much do you think you spend in a month?':'Avg_Expense'})
print(data.tail())


# In[13]:


#checking the dataset for missing values in each column

print(data.isnull().sum())


# In[14]:


#Dropping empty rows

data = data.dropna()


# In[15]:


#recheckig the dataset for missing values

print(data.isnull().sum())


# In[16]:


data = data.reset_index(drop=True)


# In[17]:


print(data.info())


# In[50]:


data.describe()


# In[25]:


grouped = data.groupby("Income_range")
grouped


# In[26]:


grouped.groups


# In[27]:


grouped.size()


# In[72]:


data.groupby(['Income_range']).groups.keys()


# In[78]:


data['Income_range']= data['Income_range'].replace('Below 5000', 2500)
data['Income_range']= data['Income_range'].replace('11,000 – 20,000', 15500)
data['Income_range']= data['Income_range'].replace('110,000 – 200,000', 155000)
data['Income_range']= data['Income_range'].replace('201,000 – 300,000', 250500)
data['Income_range']= data['Income_range'].replace('21,000 – 50,000', 35500)
data['Income_range']= data['Income_range'].replace('301,000 – 500,000',400500)
data['Income_range']= data['Income_range'].replace('500,000 – above', 750000)
data['Income_range']= data['Income_range'].replace('5000 – 10,000', 7500)
data['Income_range']= data['Income_range'].replace('51,000 – 80,000',65500)
data['Income_range']= data['Income_range'].replace('81,000 – 100,000',90500)


# In[79]:


data['T_Income']= data['Income_range'] + data['Other_Income']


# In[80]:


data['Net_Income']= data['Income_range'] - data['Avg_Expense']


# In[29]:


grouped.agg(np.mean)


# In[33]:


grouped.agg([np.mean, np.sum, np.std]).head(10)


# In[41]:


p_index = grouped.agg(np.sum)
p_index['Avg_Expense'].plot(kind="bar")


# In[42]:


grouped = data.groupby("What part of your state do you live in?")["Income_range"]
grouped.apply(lambda x:x.value_counts())


# In[43]:


grouped = data.groupby("What part of your state do you live in?")["Avg_Expense"]
grouped.apply(lambda x:x.value_counts())


# In[44]:


grouped = data.groupby("What part of your state do you live in?")["What is your largest form of expense"]
grouped.apply(lambda x:x.value_counts())


# In[49]:


data.pivot_table(index='Income_range',values=
['Avg_Expense','Other_Income'],aggfunc=np.mean)


# In[51]:


data['Income_range'].value_counts().plot(kind="bar")


# In[56]:


def get_var_category(series):
    unique_count = series.nunique(dropna=False)
    total_count = len(series)
    if pd.api.types.is_numeric_dtype(series):
        return 'Numerical'
    elif pd.api.types.is_datetime64_dtype(series):
        return 'Date'
    elif unique_count==total_count:
        return 'Text (Unique)'
    else:
        return 'Categorical'
def print_categories(data):
    for column_name in data.columns:
        print(column_name, ": ", get_var_category(data[column_name]))


# In[57]:


print_categories(data)


# In[81]:


data['Net_Income'].value_counts()


# In[82]:


import seaborn as sns
sns.set(color_codes=True)
sns.set_palette(sns.color_palette("muted"))

sns.distplot(data["T_Income"].dropna())


# In[65]:


#checking the correlation of other income with that of expense
data[["Other_Income", "Avg_Expense"]].corr()


# In[89]:


#checking the correlation of total income with that of expense
data[["T_Income", "Avg_Expense"]].corr()


# In[83]:


#categorizing income range

data['NIncome'] = ['Very Low' if -2.147484e+09<net_income<10000
                        else 'Low' if 10000<net_income<50000
                      else 'Medium' if 50000<net_income<150000
                      else 'High' if 150000<net_income<300000
                      else 'Very High' if 300000<net_income<1000000
                      else 'Outlier' \
                      for net_income in list(data['Net_Income'].values)
                           ]


# In[84]:


print(data['NIncome'].tail())


# In[85]:


plt.rcParams['figure.figsize']=(10,5)
sns.countplot(data['NIncome'], palette = 'plasma_r')
plt.title('Net Income', fontsize = 30)
plt.show()


# In[87]:


#Getting the human need that people spend the most money on

data['What is your largest form of expense'].value_counts()


# In[88]:


data['Occupation'].value_counts()


# In[ ]:


#In conclusion, seeing the band of people in the very low income category, it can be concluded that nigeria is a poverty nation. In profering a solution, i believe subsidized basic amenities such as housing and transportation can be provided seeing the majority spend their monthly income on these amenities.

