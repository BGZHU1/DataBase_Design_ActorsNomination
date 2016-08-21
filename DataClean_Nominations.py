
# coding: utf-8

# In[82]:

import pandas as pd
dataFrame=pd.read_csv("academy_awards.csv",encoding="ISO-8859-1")


# Get a feel of the data: esp. the value in unmaned column, 
# weather or not there are some valuable values

# In[83]:

dataFrame.head(15)


# In[84]:

counts=[]
for col in dataFrame.columns:
    count=dataFrame[col].value_counts()
    print(count)
    print("end here")
    print("--------------")
    


# Clean up the Year Column

# In[85]:

dataFrame["Year"]=dataFrame["Year"].astype("str")
dataFrame["Year"]=dataFrame["Year"].str[0:4]
dataFrame["Year"]=dataFrame["Year"].astype("int64")
later_than_2000=dataFrame[dataFrame["Year"]>2000]
award_categories = ["Actor -- Leading Role","Actor -- Supporting Role", "Actress -- Leading Role", "Actress -- Supporting Role"]
nominations = later_than_2000[later_than_2000["Category"].isin(award_categories)]
print(nominations)


# Clean up the Won

# In[86]:

Won=dataFrame["Won?"]
#print(Won.value_counts())
replace_dict={"YES":1,"NO":0}
dataFrame["Won?"]=Won.map(replace_dict)
print(dataFrame["Won?"].value_counts())


# In[87]:

dataFrame["Won"]=dataFrame["Won?"]
#print(dataFrame["Won"].value_counts(dropna=False))
#dataFrame["Won"]=dataFrame["Won"].astype("int64")


# In[88]:

list={"Won?",
"Unnamed: 5",
"Unnamed: 6",
"Unnamed: 7",
"Unnamed: 8",
"Unnamed: 9",
"Unnamed: 10"}
final_nominations=dataFrame.drop(list,axis=1)
print(final_nominations.head(6))


# Clean up the additional info - splite the info

# In[89]:

additional_info_one=dataFrame["Additional Info"].str.rstrip("'}")
additional_info_two=additional_info_one.str.split("{'")
print(additional_info_two)


# In[90]:

movie_names=additional_info_two.str[0]
characters=additional_info_two.str[1]
final_nominations["Movie"]=movie_names
final_nominations["Characters"]=characters
final_nominations.drop("Additional Info",axis=1)


# Connect to DataBase

# In[92]:

import sqlite3
conn=sqlite3.connect("nominations.db")
final_nominations.to_sql("nominations",conn,index=False)


# Test by query the data

# In[104]:

query_one="pragma table_info(nominations);"
query_two="select * from nominations limit 10;"
print(conn.execute(query_one).fetchall())
print(conn.execute(query_two).fetchall())
conn.close()


# In[ ]:



