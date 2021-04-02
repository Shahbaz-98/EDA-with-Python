import argparse
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns
import sqlite3


CON = ""
C = ""
DF = ""


def load_data():
    return pd.read_csv(r'C:\Users\Dell\OneDrive\Desktop\netflix_titles.csv')


def db_connection():
    return sqlite3.connect("netflix.db")


def init_app():
    global DF
    DF = load_data()
    global CON
    CON = db_connection()
    global C
    C = CON.cursor()
    DF.to_sql('MyTable', CON, if_exists='append', index=False)
    DF = pd.read_sql_query("SELECT * from MyTable", CON)
    DF = DF.drop_duplicates(['title', 'country', 'type', 'release_year'])
    DF['date_added'] = pd.to_datetime(DF['date_added'])
    for ratings in DF.index:
        if DF.loc[ratings, 'rating'] == 'UR':
            DF.loc[ratings, 'rating'] = 'NR'


init_app()


def release_sort_func():
    return DF.groupby(['release_year', 'type'])['type'].value_counts().sort_values(ascending=False)


def country_sort_func():
    return DF.groupby(['country', 'type'])['type'].value_counts().sort_values(ascending=False)


def listed_sort_func():
    return DF.groupby(['listed_in'])['type'].value_counts()


def ratings():
    plt.figure(figsize=(8, 6))
    DF['rating'].value_counts(normalize=True).plot.bar()
    plt.title('Ratings')
    plt.xlabel('rating')
    plt.ylabel('relative frequency')
    plt.show()


def freq_tr():
    plt.figure(figsize=(10, 8))
    sns.countplot(x='rating', hue='type', data=DF)
    plt.title('comparing frequency between type and rating')
    plt.show()


def year_added():
    DF['year_added'] = DF['date_added'].dt.year
    year_sort = DF.groupby('year_added')['type'].value_counts(normalize=True) * 100
    print(year_sort)


def release_sort():
    cf = release_sort_func()
    print(cf)


def country_sort():
    cf = country_sort_func()
    print(cf)


def listed_sort():
    cf = listed_sort_func()
    print(cf)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--ratings', action='store', dest='ratings', help='Shows plot for ratings.', nargs='?'
                        , const=1)
    parser.add_argument('-t', '--typeComparison', action='store', dest='frequencyTR', help='Shows comparison between '
                                                                                           'type and ratings.', nargs='?'
                        , const=2)
    parser.add_argument('-y', '--yearAdded', action='store', dest='yearAdded', help='Shows frequency of Movies and '
                                                                                    'TV Shows released in years.', nargs='?'
                        , const=3)
    parser.add_argument('-s', '--releaseSort', action='store', dest='releaseSort', help='Shows count of Movies and TV '
                                                                                        'Shows sorted acc. '
                                                                                        'to release year.', nargs='?'
                        , const=3)
    parser.add_argument('-c', '--countrySort', action='store', dest='countrySort', help='Shows count of Movies and '
                                                                                        'TV Shows sorted '
                                                                                        'acc. to countries.', nargs='?'
                        , const=4)
    parser.add_argument('-l', '--listedSort', action='store', dest='listedSort', help='Shows count of Movies and '
                                                                                      'TV Shows sorted acc. '
                                                                                      'to the category of listing.',
                        nargs='?', const=5)

    args = parser.parse_args()
    rating = args.ratings
    freqTRD = args.frequencyTR
    year = args.yearAdded
    release = args.releaseSort
    country = args.countrySort
    listed = args.listedSort

    if rating:
        ratings()
    elif freqTRD:
        freq_tr()
    elif year:
        year_added()
    elif release:
        release_sort()
    elif country:
        country_sort()
    elif listed:
        listed_sort()

