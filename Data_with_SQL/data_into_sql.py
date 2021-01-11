#Data was obtained via Kaggle website
#https://www.kaggle.com/stefanoleone992/imdb-extensive-dataset

#Import data into SQL

import pandas as pd
from sqlalchemy import create_engine

df_movies = pd.read_csv('../Data/IMDb_movies.csv')
engine = create_engine("mysql+pymysql://{user}:{pw}@localhost/{db}".format
                       (user="root",pw="qwerty123!",db="MovieRecommendationSystem"))
try:
    df_movies.to_sql('movie_dataset', con = engine, if_exists = 'replace',chunksize = 1000)
except:
    print('Something went wrong')
else:
    print('Data uploaded successfully')


#Add a primary key, change its type and column name
query = """ALTER TABLE `movierecommendationsystem`.`movie_dataset` 
               # CHANGE COLUMN `index` `id` INT NOT NULL ,
                #ADD PRIMARY KEY (`id`),
                #ADD UNIQUE INDEX `id_UNIQUE` (`id` ASC) VISIBLE"""
engine.execute(query)
