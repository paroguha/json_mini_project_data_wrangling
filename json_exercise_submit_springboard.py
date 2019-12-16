
# coding: utf-8

# # JSON examples and exercise
# ****
# + get familiar with packages for dealing with JSON
# + study examples with JSON strings and files 
# + work on exercise to be completed and submitted 
# ****
# + reference: http://pandas-docs.github.io/pandas-docs-travis/io.html#json
# + data source: http://jsonstudio.com/resources/
# ****

# In[1]:


import pandas as pd


# ## imports for Python, Pandas

# In[2]:


import json
from pandas.io.json import json_normalize


# ## JSON example, with string
# 
# + demonstrates creation of normalized dataframes (tables) from nested json string
# + source: http://pandas-docs.github.io/pandas-docs-travis/io.html#normalization

# In[3]:


# define json string
data = [{'state': 'Florida', 
         'shortname': 'FL',
         'info': {'governor': 'Rick Scott'},
         'counties': [{'name': 'Dade', 'population': 12345},
                      {'name': 'Broward', 'population': 40000},
                      {'name': 'Palm Beach', 'population': 60000}]},
        {'state': 'Ohio',
         'shortname': 'OH',
         'info': {'governor': 'John Kasich'},
         'counties': [{'name': 'Summit', 'population': 1234},
                      {'name': 'Cuyahoga', 'population': 1337}]}]


# In[4]:


# use normalization to create tables from nested element
json_normalize(data, 'counties')


# In[5]:


# further populate tables created from nested element
json_normalize(data, 'counties', ['state', 'shortname', ['info', 'governor']])


# ****
# ## JSON example, with file
# 
# + demonstrates reading in a json file as a string and as a table
# + uses small sample file containing data about projects funded by the World Bank 
# + data source: http://jsonstudio.com/resources/

# In[10]:


# load json as string
json.load((open(r'C:\Users\paro\Desktop\data_wrangling_json\data\world_bank_projects_less.json')))


# In[12]:


# load as Pandas dataframe
sample_json_df = pd.read_json(r'C:\Users\paro\Desktop\data_wrangling_json\data\world_bank_projects_less.json')
sample_json_df


# ****
# ## JSON exercise
# 
# Using data in file 'data/world_bank_projects.json' and the techniques demonstrated above,
# 1. Find the 10 countries with most projects
# 2. Find the top 10 major project themes (using column 'mjtheme_namecode')
# 3. In 2. above you will notice that some entries have only the code and the name is missing. Create a dataframe with the missing names filled in.

# In[13]:


# loading the world_bank_json as string
json.load((open(r'C:\Users\paro\Desktop\data_wrangling_json\data\world_bank_projects.json')))


# In[14]:


# load as Pandas dataframe
WB_json_data = pd.read_json(r'C:\Users\paro\Desktop\data_wrangling_json\data\world_bank_projects.json')
WB_json_data


# In[16]:


WB_json_data.head(10)


# ## JSON exercise
# Using data in file 'data/world_bank_projects.json' and the techniques demonstrated above,
# 
# 1. Find the 10 countries with most projects
# 2. Find the top 10 major project themes (using column 'mjtheme_namecode')
# 3. In 2. above you will notice that some entries have only the code and the name is missing. Create a dataframe with the missing names filled in.

# In[17]:


WB_json_data.columns


# In[18]:


Countries_projects = WB_json_data[['countryname','countryshortname', 'project_name']]
Countries_projects.head()


# In[19]:


#1. Find the 10 countries with most projects
Countries_unique_projects = Countries_projects['countryname'].value_counts()
print('10 countries with most projects:')
Countries_unique_projects.head(10)


# In[20]:


# Find the top 10 major project themes (using column 'mjtheme_namecode')
# Create a themes dataframe and display it
themes = pd.DataFrame(columns=['code', 'name'])
for row in WB_json_data.mjtheme_namecode:
    themes = themes.append(json_normalize(row))
themes.reset_index(drop=True, inplace=True)

themes.head()


# In[21]:


# Find the top 10 major project themes
theme_counts = themes.name.value_counts()
print('Top 10 major project themes:')
theme_counts.head(10)


# In[23]:


# Find the top 10 major project themes
theme_code_counts = themes.code.value_counts()
print('Top 10 major project themes codes:')
theme_code_counts.head(10)


# In[22]:


# 3. In 2. above you will notice that some entries have only the code and the name is missing. 
# Create a dataframe with the missing names filled in.
# Mapping theme codes to theme names and displaying the dictionary
name_dict = {}

for row in themes.itertuples():
    if row[2] != '':
        name_dict[row[1]] = row[2]
        
name_dict


# In[24]:


# Fill in missing theme names using the name dictionary
for row in themes.itertuples():
    if row[2] == '':
        themes.set_value(row[0], 'name', name_dict[row[1]])
        
# Check to make sure there are no more missing entries
print('Number of missing name entries:', len(themes[themes['name'] == '']))


# In[25]:


# Display top 10 major project themes
print('Top 10 major project themes with the missing names filled in:')
themes.name.value_counts().head(10)

