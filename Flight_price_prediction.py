#!/usr/bin/env python
# coding: utf-8

# In[71]:


# Dataset taken from Kaggle


# In[72]:


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns


# In[73]:


df_train = pd.read_excel('E:/KaggleCompetitions/FlightPricePredictions/Data_Train.xlsx')
df_train.head()


# In[74]:


df_train.info()


# In[75]:


# There are almost all the object datatypes excluding price. Now, we can check for datetime columns: Date_of_Journey, 
# Arrival_Time, Dep_Time


# In[76]:


df_train[['Date_of_Journey', 'Arrival_Time', 'Dep_Time']].head()


# In[77]:


# Separating date, month and year into different columns from Date_of_Journey to check behaviour at different 
# months and same date, etc different combinations.


# In[78]:


list_date = ['Date_of_Journey', 'Arrival_Time', 'Dep_Time']


# In[79]:


for i in list_date:
    df_train[i] = pd.to_datetime(df_train[i])
df_train.columns


# In[80]:


df_train['journey_day']=df_train['Date_of_Journey'].dt.day
df_train['journey_month']=df_train['Date_of_Journey'].dt.month
df_train['journey_year']=df_train['Date_of_Journey'].dt.year

df_train[['journey_day', 'journey_month', 'journey_year']].head()


# In[81]:


df_train['journey_year'].value_counts()


# In[82]:


df_train['journey_month'].value_counts()


# In[83]:


df_train['journey_day'].value_counts()


# In[84]:


# Range of time period of data, we have
print(df_train['Date_of_Journey'].max())
print(df_train['Date_of_Journey'].min())


# In[85]:


#checking null values in all the columns


# In[86]:


df_train.isnull().sum()


# In[87]:


# Extraction of hour and seconds from timestamp columns


# In[88]:


list_time = ['Dep_Time', 'Arrival_Time']
for i in list_time:
#     try:
    df_train[i + '_hour'] = df_train[i].dt.hour
    df_train[i + '_hour'] = df_train[i].dt.minute
    #df_train = df_train.drop(i, axis = 1, inplace = True)
#     except:
#         pass


# In[89]:


df_train.head()


# EDA

# In[90]:


# Analyse if duration impacts price (target)


# In[91]:


df_train['Duration'].max()


# In[92]:


df_train['Duration'].value_counts()


# In[93]:


# df_train['Duration_mins'] = int(str(df_train['Duration']).split('h')[0])*60+int(str(df_train['Duration']).split('h')[-1].replace(' ','').replace('m', ''))


# In[94]:


list2 = []
for i in range(len(df_train['Duration'])):
    print(i)
    try:
#         print(int(str(df_train['Duration'][i]).split('h')[-1].replace(' ','').replace('m', '')))
        list2.append(int(str(df_train['Duration'][i]).split('h')[0])*60 + int(str(df_train['Duration'][i]).split('h')[-1].replace(' ','').replace('m', '')))
    except:
        if 'm' not in df_train['Duration'][i]:
            list2.append(int(str(df_train['Duration'][i]).split('h')[0])*60)
        elif 'h' not in df_train['Duration'][i]:
            list2.append(int(str(df_train['Duration'][i]).split('m')[0]))
        else:
            list2.append('')


# In[95]:


len(list2)


# In[96]:


len(df_train)


# In[97]:


df_train['Duration_mins'] = list2
df_train.head()


# In[98]:


#count of flights fly at early morning, morning, noon, evening, night, late night 


# In[99]:


list3=[]
def departuretimezone(i):
#     for i in df_train[z]:
    if 4<i<8:
        return('early morning')
    elif 8<i<12:
        return('morning')
    elif 12<i<116:
        return('noon')
    elif 16<i<20:
        return('evening')
    elif 20<i<24:
        return('night')
    else:
        return('late night')


# In[100]:


df_train['Dep_Time_hour'].apply(departuretimezone).value_counts().plot(kind = 'bar')


# In[101]:


df_train['Arrival_Time_hour'].apply(departuretimezone).value_counts().plot(kind = 'bar')


# In[102]:


# Hence, there are no flights departing or landing at evening and in night time.
# Most busy or peak time of the flights in noon time and least at morning.


# In[103]:


# if Duration affecting/effecting Price(Target)
sns.lmplot(x = 'Duration_mins', y = 'Price', data = df_train)


# In[104]:


df_train['Destination'].value_counts().plot()


# In[105]:


sns.countplot(df_train['Destination'])


# In[106]:


# Hence, most busy destination airport is Cochin.


# In[107]:


df_train['Source'].value_counts().plot(kind = 'pie')


# In[108]:


# Hence, most busy source airport is Delhi.


# In[109]:


# Count of different airlines having destination at Cochin airport?
df_train[df_train['Destination'] == 'Cochin'].groupby('Airline').size().sort_values(ascending = False)


# In[110]:


# Count of different airlines having Source at Delhi airport?
df_train[df_train['Source'] == 'Delhi'].groupby('Airline').size().sort_values(ascending = False)


# In[111]:


# Different routes for Source airport at Delhi
df_train[df_train['Source'] == 'Delhi'].groupby('Route').size().sort_values(ascending = False)


# In[112]:


# Different routes for Destination airport at Cochin
df_train[df_train['Destination'] == 'Cochin'].groupby('Route').size().sort_values(ascending = False)


# In[113]:


df_train['Airline'].value_counts().sort_values(ascending = False)


# In[114]:


# Maximum fly is of Jet Airways airline.


# In[115]:


# Jet airways have different routs
df_train[df_train['Airline'] == 'Jet Airways'].groupby('Route').size().sort_values(ascending = False)


# In[116]:


# Airline VS Price
plt.figure(figsize=(16,10))
sns.boxplot(x = 'Price', y = 'Airline', data = df_train)
plt.xticks(rotation = 90, fontsize = 18)
plt.xticks(fontsize = 15)


# In[117]:


# Airline VS Price
plt.figure(figsize=(16,10))
sns.violinplot(x = 'Price', y = 'Airline', data = df_train)
plt.xticks(rotation = 90, fontsize = 18)
plt.xticks(fontsize = 15)


# # Feature Engineering

# In[118]:


df_train.head()


# In[119]:


(df_train['Additional_Info'].value_counts()/len(df_train)) *100


# In[120]:


# 78.11 % of records in data are without Additional info. Rest of most flights don't have the meals included.


# In[121]:


# check for the datatypes
for i in df_train.columns:
    print(i + ' :  ', df_train[i].dtype)


# In[122]:


df_train['Source'].value_counts()


# In[123]:


df_train['Destination'].value_counts()


# In[124]:


(df_train['Total_Stops'].value_counts()/len(df_train)) *100


# In[125]:


# There are 52.65% flights having 1 stop and 32.67% are non-stop flights.


# In[126]:


df_train.groupby(['Airline'])['Price'].mean()


# In[127]:


df_train.groupby(['Airline'])['Price'].std()


# In[128]:


list1 = df_train.groupby(['Airline'])['Price'].std().sort_values().index
list1


# In[129]:


# COnverting Airlines from cat to continuous variables
dict2 = {m:n for m,n in enumerate(list1,0)}
list2 = df_train['Airline'].map(dict2)
list2


# In[130]:


df_train['Airline'].value_counts


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




