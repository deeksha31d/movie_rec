# -*- coding: utf-8 -*-
"""
@author: Deeksha Dewangan
"""
import json
import requests
import pickle
import gzip
import streamlit as st
from streamlit_lottie import st_lottie
import requests
import pandas as pd


#%%
def get_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def Recommender(movie):
    index = movies_list[movies_list['title'] == movie].index[0]
    Distances = similarity_score[index]
    Movie_list = sorted(list(enumerate(Distances)),reverse=True,key = lambda x: x[1])
    Movies_recommended =[]
    Movies_poster = []
    for i in Movie_list[1:7]:
        index = i[0]
        movie_id = movies_list.iloc[index].movie_id
        movie_name = movies_list.iloc[index].title
        Movies_recommended.append(movie_name)
        Movies_poster.append(get_poster(movie_id))
    return Movies_recommended, Movies_poster
        
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()
#%%
st.header('Movies for you')
#%%

movies_list = pd.read_csv('Processed_movie_data.csv')
with gzip.open('Similarity_score.pklz', 'rb') as ifp:
    similarity_score = pickle.load(ifp)

movie_list = movies_list['title'].values

selected_movie = st.selectbox(
    "What you have watched recently?",
    movie_list
)
lottie_movie = load_lottieurl("https://assets9.lottiefiles.com/private_files/lf30_bb9bkg1h.json")
 
st_lottie(lottie_movie, height=300, key="coding")

if st.button('Recommend Me'):
    recommended_movie_names,recommended_movie_posters = Recommender(selected_movie)
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
  