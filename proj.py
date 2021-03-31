import argparse
import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import seaborn as sns
import sqlite3


def load_data():
    """loads the required .csv files."""
    return pd.read_csv(r'C:\Users\Dell\OneDrive\Desktop\netflix_titles.csv')


def db_connection():
    """creates a connection to the database."""
    return sqlite3.connect("netflix.db")


def init_app():
    """initializes all the required variables"""
    df = load_data()
    con = db_connection()
    cur = con.cursor()
    df.to_sql('MyTable', con, if_exists='append', index=False)
    df = pd.read_sql_query("SELECT * from MyTable", con)
    df = df.drop_duplicates(['title', 'country', 'type', 'release_year'])
    df['date_added'] = pd.to_datetime(df['date_added'])
    for temp_ratings in df.index:
        if df.loc[temp_ratings, 'rating'] == 'UR':
            df.loc[temp_ratings, 'rating'] = 'NR'
    return df, con, cur


def ratings(df):
    """plots a graph that displays the comparison between different ratings
    and the individual data available for each rating."""
    plt.figure(figsize=(8, 6))
    df['rating'].value_counts(normalize=True).plot.bar()
    plt.title('Ratings')
    plt.xlabel('rating')
    plt.ylabel('relative frequency')
    plt.show()


def freq_tr(df):
    """plots a graph that displays the comparison between type of entry and the ratings they fall under."""
    plt.figure(figsize=(10, 8))
    sns.countplot(x='rating', hue='type', data=df)
    plt.title('comparing frequency between type and rating')
    plt.show()


def year_added(df):
    """sorts and displays the data acc. to the year they were added to Netflix."""
    df['year_added'] = df['date_added'].dt.year
    year_sort = df.groupby('year_added')['type'].value_counts(normalize=True) * 100
    print(year_sort)


def release_sort(df):
    """sorts and displays the data acc. to the year they were released to the public."""
    cf = df.groupby(['release_year', 'type'])['type'].value_counts().sort_values(ascending=False)
    print(cf)


def country_sort(df):
    """sorts and displays the data acc. to the country they were released in."""
    cf = df.groupby(['country', 'type'])['type'].value_counts().sort_values(ascending=False)
    print(cf)


def listed_sort(df):
    """sorts and displays the data acc. to the category they were listed in."""
    cf = df.groupby(['listed_in'])['type'].value_counts()
    print(cf)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-r', '--ratings', action='store', dest='ratings', help='Shows plot for ratings.', nargs='?',
                        const=1)
    parser.add_argument('-t', '--typeComparison', action='store', dest='frequency_tr', help='Shows comparison between '
                                                                                            'type and ratings.',
                        nargs='?', const=2)
    parser.add_argument('-y', '--yearAdded', action='store', dest='year_added', help='Shows frequency of Movies and '
                                                                                     'TV Shows released '
                                                                                     'in years.', nargs='?', const=3)
    parser.add_argument('-s', '--releaseSort', action='store', dest='release_sort', help='Shows count of Movies and TV '
                                                                                         'Shows sorted acc. '
                                                                                         'to release year.', nargs='?',
                        const=3)
    parser.add_argument('-c', '--countrySort', action='store', dest='country_sort', help='Shows count of Movies and '
                                                                                         'TV Shows '
                                                                                         'sorted acc. to countries.',
                        nargs='?', const=4)
    parser.add_argument('-l', '--listedSort', action='store', dest='listed_sort', help='Shows count of Movies '
                                                                                       'and TV Shows sorted acc. '
                                                                                       'to the category of listing.',
                        nargs='?', const=5)

    df, con, c = init_app()

    args = parser.parse_args()
    rating = args.ratings
    freq_trd = args.frequency_tr
    year = args.year_added
    release = args.release_sort
    country = args.country_sort
    listed = args.listed_sort

    if rating:
        ratings(df)
    elif freq_trd:
        freq_tr(df)
    elif year:
        year_added(df)
    elif release:
        release_sort(df)
    elif country:
        country_sort(df)
    elif listed:
        listed_sort(df)
