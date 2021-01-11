import pandas as pd
import mysql.connector

#File used for saving mySQL database as .csv file, so the movie recommendation system does not require connection to database

#Create a connection to database
connection = mysql.connector.connect(host='localhost',
                                 database='movierecommendationsystem',
                                 user='root',
                                 password='qwerty123!',
                                 use_pure=True)
    
#Recommendations are based upon description, actors, director and genre
query = "SELECT id, title, director, actors, genre, description, year FROM clean_movie_data;"

#Load data from sql into dateframe
movie_data = pd.read_sql(query, connection)
    
#Set id from database as index to the dateframe
movie_data = movie_data.set_index('id')

movie_data.to_csv("data_in_dataframe.csv", sep=",")


movie_data = pd.read_csv("../Data_as_dataframe/data_in_dataframe.csv")
print(movie_data.columns)
#movie_data = movie_data[["id", "title", "director", "actors", "genre", "description"]]
#print(movie_data.columns)

recommendation_df = movie_data["id"]
recommendation_df['title'] = movie_data["title"].str.lower() + " " + movie_data['year'].astype(str)
print(recommendation_df['title'])