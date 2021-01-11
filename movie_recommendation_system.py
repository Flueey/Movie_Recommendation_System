import pandas as pd
import mysql.connector
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.feature_extraction.text import CountVectorizer
import numpy as np
import re
import sys

pd.options.mode.chained_assignment = None

def significant_actors(actors_str):
    """Reduce the number of actors to the most important 5"""

    actors_lst = actors_str.split(', ')
    if len(actors_lst) <= 5:
        pass
    else:
        actors_lst = actors_lst[:5]
        
    new_actors_str = ', '.join(actors_lst)
    new_actors_str = lower_and_spaces(new_actors_str)
    return new_actors_str

def lower_and_spaces(string_of_things):
    """Turn strings in a list to lowercase and remove spaces between names"""

    string_of_things = string_of_things.replace(" ", "").lower()
    return string_of_things
    

def find_recommendations(recommendation_df, movie_data, title, director_influence, actors_influence, description_influence):
    """Find movie recommendations"""
    
    #Create similarity matrix
    count = CountVectorizer(min_df=0, stop_words='english')
    count_matrix = count.fit_transform(movie_data['metadata'])
    
    #Get the index of a looked-up movie
    title = title.lower()
    try:
        idx = recommendation_df[recommendation_df['title'] == f'{title}'].index[0]
    except IndexError:
        print("Could not find movie \"{}\" in the database".format(title))
        sys.exit()
    
    #Reduce size of matrix
    count_matrix = count_matrix.astype(np.float32)
    #Reduce index by 1 since they are not even
    cosine_sim = cosine_similarity(count_matrix, count_matrix[idx-1])
    
    #Enumerate returns true indexes of the movies
    scores = list(enumerate(cosine_sim))
    
    #Order results by highest similarity and choose best 100
    scores = sorted(scores, key=lambda x: x[1], reverse = True)
    scores = scores[1:100]
    
    #Find movie titles based on indexes and append them to list
    #Enumerate reversed order so the most recommended movie has the
    #highest score (index)
    movie_indexes = [i[0] for i in scores]
    recommendations = []
    for i in movie_indexes:
        recommendations.append(recommendation_df['title'].iloc[i])
    recommendations = list(enumerate(recommendations))

    return recommendations
    


def prepare_data(flag, movie_name,director_influence=3, actors_influence=2, description_influence=2,genre_influence=2):
        
    #If we want to connect to database
    if flag == 0:
        #Create a connection to database
        connection = mysql.connector.connect(host='localhost',
                                     database='movierecommendationsystem',
                                     user='root',
                                     password='qwerty123!',
                                     use_pure=True)
    
        #Recommendations are based upon description, actors, director and genre
        query = "SELECT id, title, director, actors, genre, description FROM clean_movie_data;"
    
        #Load data from sql into dateframe
        movie_data = pd.read_sql(query, connection)
        
        #Construct a dateframe with indexes, titles and years, which will be sent into function find_recommendations() later
        #The titles are turned to lowercase, so it is easier to give input
        #Production year is added to differentiate between movies with the same title
        query = """SELECT id, CONCAT(LOWER(title)," ", `year`) as title FROM clean_movie_data"""
        recommendation_df = pd.read_sql(query, connection)

    
    #If we want to work with csv
    elif flag == 1:
        #Read CSV file that was prepared in order to demonstrate how programme works without having to connect to database
        movie_data_csv = pd.read_csv("../Data_as_dataframe/data_in_dataframe.csv")
        
        #Recommendations are based upon description, actors, director and genre
        movie_data = movie_data_csv[["id", "title", "director", "actors", "genre", "description"]]
        
        #Construct a dateframe with indexes, titles and years, which will be sent into function find_recommendations() later
        #The titles are turned to lowercase, so it is easier to give input
        #Production year is added to differentiate between movies with the same title
        recommendation_df = movie_data_csv[["id", "title", "year"]]
        recommendation_df['title'] = recommendation_df["title"].str.lower() + " " + recommendation_df["year"].astype(str)

    #Set id from database or csv as index to the dateframes
    movie_data = movie_data.set_index('id')
    recommendation_df = recommendation_df.set_index('id')
    
    #Reduce a number of actors so that only the most important are taken into consideration
    #Splitting string and taking only the first 5 actors
    #Also changing the actors into a string with no spaces and all in lowercase
    movie_data['actors'] = movie_data['actors'].apply(significant_actors)

    #Change everything left to lowercase and remove spaces between names
    movie_data['director'] = movie_data['director'].apply(lower_and_spaces)
    movie_data['genre'] = movie_data['genre'].apply(lambda x: x.lower())
    movie_data['description'] = movie_data['description'].apply(lambda x: x.lower())

    #Increase the influence of director upon the final result (by multiplying its occurance)
    movie_data['director'] = movie_data['director'].apply(lambda x: (x*director_influence))
    movie_data['description'] = movie_data['description'].apply(lambda x: (x*actors_influence))
    movie_data['actors'] = movie_data['actors'].apply(lambda x: (x*description_influence))
    movie_data['genre'] = movie_data['genre'].apply(lambda x: (x*genre_influence))

    #Combine all metadata into single series
    movie_data['metadata'] = movie_data['director'] + movie_data['actors'] + movie_data['description'] + movie_data['genre']

    
    #Calculate recommendations for movie that were inputed
    movies = find_recommendations(recommendation_df, movie_data, movie_name, director_influence, actors_influence, description_influence)
    for i in range(10):
        print(movies[i])
    

def make_recommendations():
    
    #Pattern that will be used to check if given title is correct
    pattern = re.compile(".*\s\d{4}")
    title = []

    
    print("Welcome to my movie system recommendation!")
    print("The recommendation system takes a movie title (and year) as arguments and tries to find a movie, which is similiar.")
    movie_title = input("Please insert movie title in english and year of production in a following format: *movie year_of_production*: ")
    title = pattern.findall(movie_title)
    while len(title) != 1:
        print("\nGiven title includes an error!")
        movie_title = input("Please insert movie title in english and year of production in a following format: *movie year_of_production*: ")
        title = pattern.findall(movie_title)
    flag = int(input("Do you want to connect to .csv file or database? .csv file is recommended, since database requires having mySQL and running previous files. Type in 0 for .csv file or type 1 for database: "))
    print(flag)
    while (flag != 1) and (flag != 0):
        flag = int(input("Please provide either 0 for connection to .csv file oraz 1 for connection to database: "))
    print("\nThe recommendations are calculated based on 4 criteria: director, 5 most known actors, genre and imdb description of the movie.")
    print("You can choose if you want to increase the influence of any criteria.")
    print("It is recommended to start with default settings and try to change them based on the feeling you got from the results.")
    print("Default settings are: directors' influence multiplied by 3, actors' by 2 and descriptions' by 2.\n")
    decision = input("Do you want to change them (yes/no)?")
    if decision == "no":
        prepare_data(flag,movie_title)
    else:
        while True:
            try:
                director_influence = int(input("Please provide a multiplier for director: "))
                actors_influence = int(input("Please provide a multiplier for actors: "))
                description_influence = int(input("Please provide a multiplier for description: "))
                genre_influence = int(input("Please provide a multiplier for genre: "))
                prepare_data(flag,movie_title, director_influence, actors_influence, description_influence,genre_influence)
                break
            except ValueError:
                print("Not a valid value, plesae try again")

make_recommendations()




