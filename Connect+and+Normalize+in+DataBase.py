
# coding: utf-8

# Connect and Normalize in DataBase

# In[67]:

import sqlite3
conn=sqlite3.connect('nominations.db')

q1=conn.execute("PRAGMA table_info(nominations)").fetchall()
query="select * from nominations limit 10"
q2=conn.execute(query).fetchall()
for item in q1:
    print(item)
for item2 in q2:
    print (item2)



# Creating the ceremonies table (Year-Host One to Many)

# In[68]:

create_ceremonies="create table ceremonies(id integer PRIMARY KEY,year integer,host text);"
conn.execute(create_ceremonies)


# Insert data into Ceremonies Table

# In[ ]:

years_hosts = [(2010, "Steve Martin"),
               (2009, "Hugh Jackman"),
               (2008, "Jon Stewart"),
               (2007, "Ellen DeGeneres"),
               (2006, "Jon Stewart"),
               (2005, "Chris Rock"),
               (2004, "Billy Crystal"),
               (2003, "Steve Martin"),
               (2002, "Whoopi Goldberg"),
               (2001, "Steve Martin"),
               (2000, "Billy Crystal"),
            ]
insert_query = "INSERT INTO ceremonies (year, host) VALUES (?,?);"
#insert muliple values into the table
conn.executemany(insert_query, years_hosts)


# In[ ]:

#Test the table
query="select host from ceremonies limit 10"
conn.execute(query).fetchall()
#conn.execute("pragma table_info(ceremonies)").fetchall()


# In[ ]:

# turn on foreign key constrains - prevent us from inserting rows 
#with nonexisting foreign key constraints
query="pragma foreign_keys=ON;"
conn.execute(query)


# In[ ]:

#set up one to many
query="create table nominations_two(id integer primary key,category text,nominee text,movie text,character text,won text,ceremony_id integer,foreign key(ceremony_id) references ceremony(id));"
conn.execute(query)


# In[71]:


nom_query ='''
select ceremonies.id as ceremony_id, nominations.category as category, 
nominations.nominee as nominee, nominations.movie as movie, 
nominations.characters as characters, nominations.won as won
from nominations
inner join ceremonies 
on nominations.year == ceremonies.year
;
'''
joined_nominations = conn.execute(nom_query).fetchall()

insert_nominations_two='''insert into nominations_two(ceremony_id,category,nominee,movie,character,won) values(?,?,?,?,?,?)
'''
conn.executemany(insert_nominations_two,joined_nominations_two)
print(conn.execute("select * from nominations_two limit 5").fetchall())


# In[73]:

#deleting and renaming tables (delete nominations and rename nominations two)
query1="drop table[nominations]"
conn.execute(query1)
query="alter table[nominations_two] rename to [nominations];"
conn.execute(query)


# In[77]:

#create muliple tables
create_movie='''create table movies(
id integer primary key,
movie text
)'''
conn.execute(create_movie)



# In[78]:

create_actors='''create table actors(
id integer primary key,
actor text
)'''
conn.execute(create_actors)


# In[82]:

create_movies_actors='''create table movies_actors(
id INTEGER PRIMARY KEY,
movie_id INTEGER REFERENCES movies(id), 
actor_id INTEGER REFERENCES actors(id)
)'''
conn.execute(create_movies_actors)

#populating a join table
pairs_query = "select movie,nominee from nominations;"
movie_actor_pairs = conn.execute(pairs_query).fetchall()

join_table_insert = "insert into movies_actors (movie_id, actor_id) values ((select id from movies where movie == ?),(select id from actors where actor == ?));"
conn.executemany(join_table_insert,movie_actor_pairs)

print(conn.execute("select * from movies_actors limit 5;").fetchall())


# In[ ]:



