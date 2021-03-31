import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import matplotlib.pyplot as plt
import seaborn as sns
import os
import sqlite3
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('-r', '--ratings', action='store', dest='ratings', help='Shows plot for ratings.')
parser.add_argument('-t', '--typeComparisson', action='store', dest='frequencyTR', help='Shows comparisson between type and ratings.')
parser.add_argument('-y', '--yearAdded', action='store', dest='yearAdded', help='Shows frequency of Movies and TV Shows released in years.')
parser.add_argument('-s', '--releaseSort', action='store', dest='releaseSort', help='Shows count of Movies and TV Shows sorted acc. to release year.')
parser.add_argument('-c', '--countrySort', action='store', dest='countrySort', help='Shows count of Movies and TV Shows sorted acc. to countries.')
parser.add_argument('-l', '--listedSort', action='store', dest='listedSort', help='Shows count of Movies and TV Shows sorted acc. to the year of listing.')

args = parser.parse_args()
rating = args.ratings
freqTRD = args.frequencyTR
year = args.yearAdded
release = args.releaseSort
country = args.countrySort
listed = args.listedSort

if(rating):
  ratings()
elif (freqTRD):
  freqTR()
elif (year):
    yearAdded()
elif(release):
    releaseSort()
elif(country):
    countrySort()
elif(listed):
    listedSort()

df = pd.read_csv(r'C:\Users\Dell\Downloads\archive\netflix_titles.csv')
con = sqlite3.connect("netflix.db")
c=con.cursor()
df = pd.read_sql_query("SELECT * from MyTable", con)
df=df.drop_duplicates(['title','country','type','release_year'])
df['date_added'] = pd.to_datetime(df['date_added'])

for i in df.index:
    if df.loc[i,'rating']=='UR':
        df.loc[i,'rating']='NR'

releaseSort = pd.read_sql('''select release_year,type,count(type) as count from MyTable group by release_year order by count DESC''', con)
releaseSort.to_sql("releaseSort",con, if_exists = "replace")

countrySort = pd.read_sql('''select country, type, count(type) as count from MyTable group by country order by count DESC''',con)
countrySort.to_sql("countrySort",con,if_exists = "append")

listedSort = pd.read_sql('''select listed_in, type, count(type) as count from MyTable group by listed_in''',con)
listedSort.to_sql("listedSort",con,if_exists = "append")

def ratings():
  plt.figure(figsize=(8,6))
  df['rating'].value_counts(normalize=True).plot.bar()
  plt.title('Ratings')
  plt.xlabel('rating')
  plt.ylabel('relative frequency')
  plt.show()

def freqTR():
  plt.figure(figsize=(10,8))
  sns.countplot(x='rating',hue='type',data=df)
  plt.title('comparing frequency between type and rating')
  plt.show()

def yearAdded():
  df['year_added']=df['date_added'].dt.year
  yearSort = df.groupby('year_added')['type'].value_counts(normalize=True)*100

def releaseSort():
    df = pd.read_sql_query("SELECT * from releaseSort", con)
    df.head()

def countrySort():
    df = pd.read_sql_query("SELECT * from countrySort", con)
    df.head()

def listedSort():
    df = pd.read_sql_query("SELECT * from listedSort", con)
    df.head()
