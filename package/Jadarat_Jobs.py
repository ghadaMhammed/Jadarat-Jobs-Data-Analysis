#!/usr/bin/env python
# coding: utf-8

# In[434]:

# In[435]:


#Import all relevant libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import zscore
from ydata_profiling import ProfileReport
from ipyvizzu import Chart, Data, Config, Style
from bidi.algorithm import get_display  # Fixes Arabic display
import arabic_reshaper  # Reshapes Arabic characters for display
 

# ## Loading the data
# We can now load the dataset into pandas using the read_csv() function. This converts the CSV file into a Pandas dataframe.

# In[436]:


#Read in the csv file and convert to a Pandas dataframe
import kagglehub
import os
if __name__ == "__main__":
 # Download latest version
 path = kagglehub.dataset_download("moayadalkhozayem/job-postings-in-saudi-arabia")
 file = os.listdir(path)


# In[437]:


df = pd.read_csv(path + "/" + file[0])


# ### Viewing the dataframe
# We can get a quick sense of the size of our dataset by using the shape method. This returns a tuple with the number of rows and columns in the dataset.

# In[438]:


df.head()


# In[439]:


df.info()


# In[440]:


df.describe(exclude="number")


# ## 1. Data Profiling:
# Data profiling is a comprehensive process of examining the data available in an existing dataset and collecting statistics and information about that data. 

# In[441]:


# Generate a profile report using ydata_profiling
profile = ProfileReport(df, title="Pandas Profiling Report", explorative=True)

# Display the report
profile.to_notebook_iframe()


# #### 1. Reliability:
# Evaluate the data's source and collection process to determine its trustworthiness.

# In[442]:


# the data shows no source or collection process


# #### 2. Timeliness: 
# Ensure the data is up-to-date and reflective of the current situation or the period of interest for the analysis.

# In[443]:


# the data updated since 2023


# #### 3. Consistency: 
# 
# Confirm that the data is consistent within the dataset and across multiple data sources. For example, the same data point should not have different values in different places.
# 

# In[444]:


# since its one dataset, no need to check consistency


# #### 4. Relevance: 
# 

# In[445]:


# eco_activity
# job_desc
# job_tasks
# comp_no
# all these variables are inrelevant to this study, therefore, we will drop them
df.drop(columns=["eco_activity","job_desc", "job_tasks", "comp_no"], inplace=True)


# #### 5. Uniqueness: 
# Check for and remove duplicate records to prevent skewed analysis results.
# 

# In[446]:


# check duplicates
df.duplicated().sum()


# In[447]:


# show duplicates rows
df[df.duplicated()]


# In[448]:


# Since job post ids are unique, we consider them as unique except the "صيدلي" job, we will remove the duplication


# #### 6. Completeness: 
# Ensure that no critical data is missing. This might mean checking for null values or required fields that are empty.
# 
# We will start by checking the dataset for missing or null values. For this, we can use the isna() method which returns a dataframe of boolean values indicating if a field is null or not. To group all missing values by column, we can include the sum() method.

# In[449]:


#Display number missing values per column
df.isnull().sum()


# In[450]:


# go to clean them 


# #### 7. Check Accuracy:
# 
# Verify that the data is correct and precise. This could involve comparing data samples with known sources or using validation rules.
# 
# **The process includes:**
# 1. Validating the appropriateness of data types for the dataset.
# 2. Identifying outliers  using established validation  rule

# In[451]:


# check columns types 
df.dtypes


# In[452]:


# job_date should be date


# In[453]:


# go to clean them 


# ## 2. Data Cleaning: 
# 
# Preliminary findings from data profiling can lead to cleaning the data by:
# - Handling missing values
# - Correcting errors.
# - Dealing with outliers.
# 
# -------------------
# 
# 

# ### Handling missing values:

# In[454]:


df['qualif'].fillna("no qualif", inplace=True)


# In[455]:


df['comp_size'].fillna("no comp_size", inplace=True)


# In[456]:


# we will remove duplication of row that have job post id = 20202026399061
df[df['job_post_id'] == 20202026399061]


# In[457]:


df[df['job_post_id'] == 20202026399061].drop_duplicates(subset='job_post_id', keep="first")


# In[458]:


# go back to 6th dimention --> Completeness


# ### Correcting errors
# 
# -------------------

# In[459]:


df['job_date'].unique()


# In[460]:


# drop rows that have date == Publish date
df = df[df['job_date'] != 'Publish date']


# In[461]:


get_ipython().system('pip install hijri-converter')


# In[462]:


from hijri_converter import Hijri

# Function to convert Hijri to Gregorian
def hijri_to_gregorian(hijri_str):
    day, month, year = map(int, hijri_str.split('/'))
    hijri_date = Hijri(year, month, day)
    return hijri_date.to_gregorian()


# In[463]:


# since we need to change type of job_date to date, only gregorian date is needed, we can use hijri_to_gregorian function
df['job_date_gregorian'] = df['job_date'].apply(hijri_to_gregorian)

# drop job_date column
df.drop(columns=['job_date'], inplace=True)


# In[464]:


df.head(2)


# In[465]:


# we will change position to int
df['available_positions'] = df['positions'].map(lambda x: x.split('/')[1])

# change type to int
df['available_positions'] = df['available_positions'].astype(int)


# In[466]:


# drop positions column
df.drop(columns=['positions'], inplace=True)


# In[467]:


df.head(2)


# In[468]:


df['exper'].unique()


# In[469]:


# change exper to int
df['exper'] =df['exper'].map(lambda x: x.split('Y')[0])

# change type to int
df['exper'] = df['exper'].astype(int)


# In[470]:


df.head(2)


# In[471]:


df['benefits'].unique()


# In[472]:


# extract salary from benefits list
salary = df['benefits'].map(lambda x: x.split(',')[1].split(']')[0].split('\'')[1])

# change salary type to int
df['salary'] = salary.astype(float)


# In[473]:


df.head(2)


# In[474]:


# change type to datetime
df['job_date_gregorian'] = pd.to_datetime(df['job_date_gregorian'])


# In[475]:


# go back to 7th dimension Accuracy 


# ### Dealing with outliers:

# In[476]:


df.describe(include='number')


# In[477]:


# detect outliers using zscore
# first select numeric columns
numric_df = df.select_dtypes(include=['number'])
zscore = numric_df.apply(zscore)


# In[478]:


# show zscore
abs(zscore)


# In[479]:


# set a threshold for zscore
threshold = 3 # common value
outliers = df[(abs(zscore) > threshold).any(axis=1)]
# show outlers calculated by zscore
outliers


# In[480]:


# drop rows that is equal to outliers
df = df[~df.isin(outliers)].dropna()


# In[481]:


x = df[df['exper'] == 0].sort_values(by='salary', ascending=False).head()


# In[482]:


# as you can see above there is unreasonable row that require a CEO with no experience, 
# we need to drop that row
df = df[~df.isin(x)].dropna()


# ## Q1: What proportion of job postings is attributed to each region within the kingdom?

# In[483]:


# What proportion of job postings is attributed to each region within the kingdom?
job_region_prop = (df['region'].value_counts()/df.shape[0]*100).round()
# exclude 0 values
job_region_prop = job_region_prop[job_region_prop != 0]


# In[484]:


# craeate a dataframe that have region and number of posts
region_df = pd.DataFrame({
    'Region' : job_region_prop.index,
    'Number of posts' : job_region_prop.values
})


# In[485]:


region_df


# In[486]:


# plot it using bar chart
region_data = Data()
region_data.add_df(region_df)
region_chart = Chart()
region_chart.animate(region_data)
region_chart.animate(
Config.column(
{

"x":"Region",
"y":"Number of posts",
"label":"عدد الوظائف",
"title":"عدد الوظائف المعلنة حسب المنطقة"
})
)


# ## Q2: Is there a gender preference indicated in the job postings?

# In[487]:


# Is there a gender preference indicated in the job postings?
gender_pref =  df['gender'].value_counts()


# In[488]:


# create a dataframe that have gender and number of posts
gender_pref_df = pd.DataFrame({
    'Gender' : gender_pref.index,
    'Number of posts' : gender_pref.values
})


# In[489]:


# plot it using bar chart
gender_pref_data = Data()
gender_pref_data.add_df(gender_pref_df)
gender_pref_chart = Chart()
gender_pref_chart.animate(gender_pref_data)
gender_pref_chart.animate(
Config.column(
{

"x":"Gender",
"y":"Number of posts",
"label":"عدد الوظائف",
"title":"عدد الوظائف المعلنة حسب الجنس"
})
)


# ## Q3: What is the expected salary range for fresh graduates? 

# In[490]:


# show avarage salary for fresh graduates each job title
avg_salary_fresh_grad = (df[df['exper'] == 0].groupby('job_title')['salary'].mean()).round()

# create a dataframe that have job title and average salary
avg_salary_fresh_grad_df = pd.DataFrame({
    'job_title' : avg_salary_fresh_grad.index,
    'salary' : avg_salary_fresh_grad.values
})


# In[491]:


# sort salary in ascending order
avg_salary_fresh_grad_df = avg_salary_fresh_grad_df.sort_values(by='salary', ascending=False)


# In[492]:


avg_salary_fresh_grad_df


# In[493]:


df['comp_type'].unique()


# In[494]:


# What is the expected salary range for fresh graduates? 
# plot range of salary using bar chart
plt.figure(figsize=(10, 5))

#histogram
sns.histplot(avg_salary_fresh_grad_df['salary'], kde=True)

# Apply Arabic reshaping and BiDi to labels to visiualize it correctly in seaborn
xlbl = get_display( arabic_reshaper.reshape('الراتب'))
ylbl = get_display( arabic_reshaper.reshape('عدد الوظائف بهذا الراتب'))

plt.xlabel(xlbl)
plt.ylabel(ylbl)

# Apply Arabic reshaping and BiDi to title to visiualize it correctly in seaborn
title = get_display(arabic_reshaper.reshape('النطاق المتوقع للراتب لحديثي التخرج') )
plt.title(title)

plt.show()



# ## Q4: # Are job opportunities predominantly targeted at individuals with experience, or is there room for fresh graduates as well?

# In[495]:


# Are job opportunities predominantly targeted at individuals with experience, or is there room for fresh graduates as well?
job_opportunities = df['exper'].value_counts()

job_opportunities_df = pd.DataFrame({
    'Experience' : job_opportunities.index.astype(str),
    'Number of posts' : job_opportunities.values
})


# In[496]:


job_opportunities_df.dtypes


# In[497]:


# plot it using bar

job_opportunities_data = Data()
job_opportunities_data.add_df(job_opportunities_df)
job_opportunities_chart = Chart()
job_opportunities_chart.animate(job_opportunities_data)
job_opportunities_chart.animate(
Config.column(
{

"x":"Experience",
"y":"Number of posts",
"title":"عدد الوظائف حسب سنوات الخبرة"
})
)


# ## Q5: Number of jobs per over time 

# In[498]:


df


# In[499]:


# number of jobs per over time
df_over_time = df['job_date_gregorian'].value_counts()
df_over_time_df = pd.DataFrame({
    'date' : df_over_time.index,
    'Number of posts' : df_over_time.values
})


# In[500]:


# convert date to datetime and keep only year and month
df_over_time_df['date'] = pd.to_datetime(df_over_time_df['date']).dt.strftime('%Y-%m')


# In[501]:


# sort date in from oldest to newest
df_over_time_df = df_over_time_df.sort_values(by='date', ascending=True)


# In[502]:


df_over_time_df


# In[503]:


# plot it using line chart

df_over_time_data = Data()
df_over_time_data.add_df(df_over_time_df)
df_over_time_chart = Chart()
df_over_time_chart.animate(df_over_time_data)
df_over_time_chart.animate(
Config.line(
{

"x":"date",
"y":"Number of posts",
"title":"عدد الوظائف حسب التاريخ"
})
)


# ## Q6: How many jobs with no experience is posted for each company type

# In[504]:


# How many jobs with no experience is posted for each company type?
no_exp = df[df['exper'] == 0]
no_exp_comp_type = no_exp['comp_type'].value_counts()
no_exp_comp_type_df = pd.DataFrame({
    'Company Type' : no_exp_comp_type.index,
    'Number of posts' : no_exp_comp_type.values
})


# In[505]:


# Apply Arabic reshaping
#no_exp_comp_type_df['Company Type'] = no_exp_comp_type_df['Company Type'].apply(lambda x: get_display(arabic_reshaper.reshape(x)))


# In[506]:


# plot it using bar chart using seaborn, show percentage in each bar
sns.barplot(x='Company Type', y='Number of posts', data=no_exp_comp_type_df)
# Apply Arabic reshaping and BiDi to labels to visiualize it correctly in seaborn
xlbl2 = get_display( arabic_reshaper.reshape('نوع الجهة'))
ylbl2 = get_display( arabic_reshaper.reshape('عدد الوظائف'))

plt.xlabel(xlbl2)
plt.ylabel(ylbl2)

# Apply Arabic reshaping and BiDi to title to visiualize it correctly in seaborn
title2 = get_display(arabic_reshaper.reshape('عدد وظائف التي لا تتطلب خبرة حسب نوع الجهة') )
plt.title(title2)
plt.show()


# In[ ]: