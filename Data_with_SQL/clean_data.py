import mysql.connector as mysql
import csv

#File used for deleting rows with missing data and choosing only the movies, which are above average

movies_dataset = mysql.connect(host='localhost', user='root',
                               passwd='qwerty123!', database='movierecommendationsystem',
                               use_pure=True)
cursor = movies_dataset.cursor()
#Select rows where there is no missing data, high average rating and enough
#votes to consider the rating significant
#In case there are new movies in database, which haven't got the chance to
#get enough votes, there is an additional OR clause that includes them if
#they have been recognized by the critics and have metascore higher than 60 and votes higher than 2000
cursor.execute("""SELECT title, actors, description, director, genre, votes, avg_vote, year
    FROM movie_dataset WHERE (actors IS NOT NULL)
    AND (description IS NOT NULL) AND (director IS NOT NULL)
    AND (genre IS NOT NULL) AND ((votes > 10000
    AND avg_vote > (SELECT AVG(avg_vote) FROM movie_dataset)) OR (metascore > 60 AND votes > 1500)) ;""")
valid_data = cursor.fetchall()


#Create a table where the significant data will be stored
cursor.execute("""CREATE TABLE clean_movie_data (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(200),
    director VARCHAR(100),
    actors VARCHAR(500),
    description VARCHAR(500),
    genre VARCHAR(100),
    avg_vote FLOAT(2,1),
    votes INT,
    year INT);""")

#Populate table with data
insert_query = """INSERT INTO clean_movie_data (title, actors, description,
        director, genre, votes, avg_vote, year) values (%s, %s, %s, %s, %s, %s, %s, %s)"""

try:
    for row in valid_data:
        cursor.execute(insert_query, row)
except:
    print('Something went wrong')
else:
    movies_dataset.commit()
    print('Data uploaded successfully')
