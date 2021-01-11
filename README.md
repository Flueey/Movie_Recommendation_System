# Movie Recommendation System
Programme written in python, which inputs data from IMDB .csv file to a database created in MySQL. It selects proper data and creates table with data that will be used in the system. Based on given title it downloads it’s metadata from database and compares it with other movies. It calculates the similarity between the given movie and the rest of the movies after it changes the metadata into vectors. Programme lets the users choose whether they are interested more in director, actors, description or genre similarity. It returns the list of 10 movies that are most similar to given title. User has an option to work with database (read further for more information) or with .csv file. Both return the same results.

# Instructions on how to run a programme
For users who just want to find movie recommendations, all they need to run is movie_recommendation_system.py file. There are detailed instructions provided after running the programme. Programme asks for movie title and year of production.

If someone wants to start from the stratch e.g. upload the data into sql, clean the data and then work out the recommendations based on connection to database:
First you need to run the data_into_sql.py, then clean_data.py (both are in Data_with_SQL folder) and finally you can run programme with flag set to 1 (which means connection to database)

# Upcoming changes
This code still requires a lot of error handling. This will be added in the near future. So far only the most obvious of errors are handled. 
