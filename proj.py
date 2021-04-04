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
    temp_df = load_data()
    temp_con = db_connection()
    temp_cur = temp_con.cursor()
    temp_df.to_sql('MyTable', temp_con, if_exists='append', index=False)
    temp_df = pd.read_sql_query("SELECT * from MyTable", temp_con)
    temp_df = temp_df.drop_duplicates(['title', 'country', 'type', 'release_year'])
    temp_df['date_added'] = pd.to_datetime(temp_df['date_added'])
    for temp_ratings in temp_df.index:
        if temp_df.loc[temp_ratings, 'rating'] == 'UR':
            temp_df.loc[temp_ratings, 'rating'] = 'NR'
    return temp_df, temp_con, temp_cur


def ratings():
    """plots a graph that displays the comparison between different ratings
    and the individual data available for each rating."""
    plt.figure(figsize=(8, 6))
    DF['rating'].value_counts(normalize=True).plot.bar()
    plt.title('Ratings')
    plt.xlabel('rating')
    plt.ylabel('relative frequency')
    plt.show()


def freq_tr():
    """plots a graph that displays the comparison between type of entry and the ratings they fall under."""
    plt.figure(figsize=(10, 8))
    sns.countplot(x='rating', hue='type', data=DF)
    plt.title('comparing frequency between type and rating')
    plt.show()


def year_added():
    """sorts and displays the data acc. to the year they were added to Netflix."""
    DF['year_added'] = DF['date_added'].dt.year
    year_sort = DF.groupby('year_added')['type'].value_counts(normalize=True) * 100
    print(year_sort)


def release_sort():
    """sorts and displays the data acc. to the year they were released to the public."""
    cf = DF.groupby(['release_year', 'type'])['type'].value_counts().sort_values(ascending=False)
    print(cf)


def country_sort():
    """sorts and displays the data acc. to the country they were released in."""
    cf = DF.groupby(['country', 'type'])['type'].value_counts().sort_values(ascending=False)
    print(cf)


def listed_sort():
    """sorts and displays the data acc. to the category they were listed in."""
    cf = DF.groupby(['listed_in'])['type'].value_counts()
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

    DF, con, c = init_app()

    args = parser.parse_args()
    rating = args.ratings
    freq_trd = args.frequency_tr
    year = args.year_added
    release = args.release_sort
    country = args.country_sort
    listed = args.listed_sort

    if rating:
        ratings()
    elif freq_trd:
        freq_tr()
    elif year:
        year_added()
    elif release:
        release_sort()
    elif country:
        country_sort()
    elif listed:
        listed_sort()
