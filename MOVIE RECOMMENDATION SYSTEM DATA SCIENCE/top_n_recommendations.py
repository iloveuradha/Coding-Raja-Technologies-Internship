# top_n_recommendations.py

import pandas as pd
from surprise import Dataset, Reader
from surprise.model_selection import train_test_split
from surprise import KNNBasic

ratings = pd.read_csv(r'ml-latest-small\ratings.csv')
movies = pd.read_csv(r'ml-latest-small\movies.csv')  

user_item_matrix = ratings.pivot_table(index='userId', columns='movieId', values='rating')

user_item_matrix = user_item_matrix.fillna(0)

reader = Reader(rating_scale=(0.5, 5))
data = Dataset.load_from_df(ratings[['userId', 'movieId', 'rating']], reader)

trainset, testset = train_test_split(data, test_size=0.2)

model = KNNBasic(sim_options={'user_based': False})
model.fit(trainset)

def get_top_n_movie_recommendations(movie_name, n=5):
    movie_id = get_movie_id(movie_name)
    if movie_id is not None:
        recommendations = model.get_neighbors(movie_id, k=n)
        movie_names = [get_movie_name(movie_id) for movie_id in recommendations]
        return movie_names
    else:
        return ['Movie not found']


def get_movie_name_suggestions(term):
    
    movies = pd.read_csv(r'ml-latest-small\movies.csv')
    suggestions = movies[movies['title'].str.contains(term, case=False)]['title'].tolist()
    return suggestions

def get_movie_id(movie_name):
    movie_id_series = movies[movies['title'] == movie_name]['movieId']
    if not movie_id_series.empty:
        return movie_id_series.iloc[0]
    else:
        return None


def get_movie_name(movie_id):
    movie_names = dict(zip(movies['movieId'], movies['title']))
    return movie_names.get(movie_id, 'Unknown')


