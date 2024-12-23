import pandas as pd
import streamlit as st
import pickle
import requests

movies_dict = pickle.load(open('movies_dic.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movies = pd.DataFrame(movies_dict)
st.title("Movie :blue[Recommendation] :sunglasses:")

selected_movie_name = st.selectbox(
    "Search the movie",
    movies['title'].values
)


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(
        movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend_movies(movie):
    movies_list = []
    movies_poster = []
    movie_index = movies[movies['title'] == movie].index[0]
    similar_movies = sorted(list(enumerate(similarity[movie_index])), key=lambda x: x[1], reverse=True)[1:6]

    for i in similar_movies:
        movie_id = movies.iloc[i[0]].movie_id
        movies_list.append(movies.iloc[i[0]].title)
        movies_poster.append(fetch_poster(movie_id))
    return movies_list,movies_poster


if st.button('Recommend'):
    recommended_movie_names, recommended_movie_posters = recommend_movies(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])
