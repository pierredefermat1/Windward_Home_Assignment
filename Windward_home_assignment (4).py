#!/usr/bin/env python
# coding: utf-8

# ## Windward home assignment
# <b> In this assignment I was asked to investigate meetings between tanker vessels in the Black Sea, occured in the past year using WindWard's 2 different datasets:</b>
# 
# 
# 1. current_benefitial_owners - a dataset contains info about the owners of tanker vessels that were involved in those meetings.
# 
# 
# 2. tanker_meetings_black_sea_last_year - a dataset contains info about the meetings, and vessels involved.
# 
# 
# In this project I used Pandas library for analyzing the given info. 

# <b> Loading the datasets & creating copies </b>

# In[1]:


import pandas as pd


# In[2]:


owners_data_origin = pd.read_csv('C:\\Users\\User\\Desktop\\Windward\\current_beneficial_owners_.csv')
past_year_meeting_origin = pd.read_csv('C:\\Users\\User\\Desktop\\Windward\\tanker_meetings_black_sea_last_year_.csv')


# In[3]:


owners_data = owners_data_origin.copy()
past_year_meeting = past_year_meeting_origin.copy()


# <b> Task a - understanding which subclasses combinations are most often occuring in those meetings  </b>

# In[4]:


vesells_type_comb = past_year_meeting.groupby(['Subclass'])
most_common_combs = vesells_type_comb['Second vessel subclass'].value_counts().sort_values(ascending=False).iloc[0:10]


# In[5]:


most_common_combs


# <b> Note </b>
# 
# 
# As seen above- there's an indication of duplication in our dataset. 
# It can be deduced from the exchange in the subclasses columns, and the same number of cases documented. hence, every meeting is probably being documented twice (one documentation for each vessel).
# 
# 
# Eitherway- the most common combinations are (descending):
# 1. Oil Products Tanker - Crude Oil Tanker (632 documentations)
# 2. Oil Products Tanker - Oil Products Tanker (338 documentations)
# 3. Oil/Chemicals Tanker - Crude Oil Tanker (280 documentations)
# 4. Oil/Chemicals Tanker - Oil Products Tanker (245 documentations)
# 5. Oil/Chemicals Tanker - Oil/Chemicals Tanker (220 documentations)
# 6. Oil Products Tanker - Crude/Oil Products Tanker (200 documentations)
# 
# 
# 
# 
# 
# 
# 
# 
# 
# <b> Task b - merging the two datasets and understanding which are the top 5 companies owns the vessels that were involved in those meetings </b>

# In[6]:


dataset = pd.merge(owners_data, past_year_meeting, on='vesselId', copy=False)
dataset


# In[7]:


task_b_data = dataset[['vesselId', 'name_lower', 'countryEnum', 'Subclass', 'Second vessel subclass']]
task_b_data = task_b_data.groupby(['name_lower', 'Subclass'])
suspicious_companies = task_b_data['Second vessel subclass'].value_counts().sort_values(ascending=False).iloc[0:6]


# In[8]:


suspicious_companies


# <b> Note </b>
# 
# 
# As seen above - I took the "top 6" companies owned vessels that were involved in most meetings based on task a analysis.
# It turned out that in 166 cases documented there wasnt any info on the company nor the country, therefore it cannot be treated as to one company responsible for all vessels documented. hence, to stay on the safe side- I took the 6th company owned the majority of involved vessels.
# 
# The companies were:
# 
# 1. yug rusi shipping- from Russia
# 2. sygnius ship management private limited - from India
# 3. volga-flot, ao - from Russia
# 4. sovcomflot - from Russia
# 5. rosneft jsc - from Russia
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# 
# <b> Task C- as discussed in task a, there are duplications in our dataset and I was asked to remove duplications of the same event documented. The problem was- there was no info on the starting/ending meeting dates, and I needed to think of another way to detect the same meeting. </b>
# 
# I was looking through the dataset features, trying to find conclusive proof of the existence of an identical meeting, and the best features I managed to find were coordinates (start/end langtitude/longtitude) of a documented meeting.
# The number of rows in the dataset decreased by 59 datapoints. The number of columns obviously stayed the same (32)

# In[9]:


task_c_data = dataset
task_c_data.drop_duplicates(subset=['Start Latitude', 'Start Longitude', 'End Latitude', 'End Longitude']
                           , keep='first')


# ## Mini Research
# 
# 
# In order to complete this task, I googled 'Tankers meetings in the Black Sea' and came across this [article](https://windward.ai/blog/high-sea-russian-oil-transfers-are-far-from-the-only-smuggling-method/) by Windward.
# In a brief- since the Russian invasion to Ukraine, the Russian are under global sanctions, in trade as well among other things.
# Trading with the Russians is a violation of those sanctions, and it appears that the Chinese are doing so in sophisticated ways, and no signs of breaching any sanctions.
# 
# 
# One particular operation pattern occurred in the above report was a chain of crude oil transported via several vessels, one that carrying it from Russia to another Russian vessel, and the later carries it to a meeting point with the Chinese vessel.
# 
# 
# In addition, I've managed to find info about tankers unloading process, which is usually done in ports in order to avoid pollution (in cases of leakage), and the whole procedure is taking up to 24 hours long.
# Using the information above, I've found a way to tag suspicious vessels in sanction breaching:
# 
# 
# * The last part of the carrying chain is a meeting between a Chinese tanker and a Russian tanker. Hence, we'd like to check any of these kind of meetings.
# 
# 
# * Any meeting that occurred more than 24 hours is a suspicious meeting.
# 

# In[10]:


dataset_copy = dataset

relevant_data = dataset_copy.loc[(dataset_copy['countryEnum']=='China') & (dataset_copy['Second vessel flag']=='Russia')]
relevant_data


# In[11]:


relevant_data = relevant_data.loc[(relevant_data['Activity Duration (hours)']>=24)]
relevant_data


# In[12]:


suspicious_chinese_companies = relevant_data['name_lower']
suspicious_chinese_companies = suspicious_chinese_companies.drop_duplicates(keep='first')

suspicious_chinese_vessels = relevant_data[['Vessel Name', 'vesselId']]
suspicious_russian_vessels = relevant_data[['Second vessel name', 'Second vesselId']]


# ### As seen above- we've managed to find 2 different Chinese companies, 3 different Chinese vessels, and  3 different Russian vessels that might be involved in dark activity.
