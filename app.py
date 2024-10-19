import pickle
import streamlit as st
import pandas as pd
import requests
from requests.exceptions import RequestException
import time


# Set page configuration
st.set_page_config(
    page_title="Movie Recommendation System",
    page_icon="popcorn.png"  
)

# TMDb API key
api_key = "c695019c63e1d6ecca032da1828fac58"

# Function to fetch the poster URL and TMDb movie page URL
def fetch_poster_and_link(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c695019c63e1d6ecca032da1828fac58&language=en-US"
    retries = 3
    for _ in range(retries):
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()  # Check if the request was successful
            data = response.json()
            poster_path = data.get("poster_path")
            if poster_path:
                # Construct the poster URL
                poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
                # Construct the TMDb movie page URL
                movie_link = f"https://www.themoviedb.org/movie/{movie_id}"
                return poster_url, movie_link
            return None, None
        except RequestException as e:
            print(f"Error fetching poster and link: {e}")
            time.sleep(2)  # Wait before retrying
    return None, None

# Function to recommend movies
def recomended(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movie_names = []
    recommended_movie_posters = []
    recommended_movie_links = []
    
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        poster_url, movie_link = fetch_poster_and_link(movie_id)
        recommended_movie_posters.append(poster_url)
        recommended_movie_links.append(movie_link)
    
    return recommended_movie_names, recommended_movie_posters, recommended_movie_links

# Load the movie data and similarity matrix
movies = pickle.load(open('movie.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Streamlit interface
st.title('Movie Recommendation System')

movies_list = movies['title'].values
option = st.selectbox(
    "Type or select a movie from the dropdown",
    movies_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters, recommended_movie_links = recomended(option)
    cols = st.columns(len(recommended_movie_names))  # Create columns based on number of recommendations
    
    for idx, (name, poster, link) in enumerate(zip(recommended_movie_names, recommended_movie_posters, recommended_movie_links)):
        with cols[idx]:
            st.text(name)
            if poster and link:
                # Display the poster as a clickable image that redirects to the TMDb movie page
                st.markdown(f"<a href='{link}' target='_blank'><img src='{poster}' alt='{name}' style='width:100%;'></a>", unsafe_allow_html=True)


#design footer
st.markdown(
    """
    <style>
    .footer { 
        #link{
        text-decoration: none;
        }
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #f1f1f1;
        color: black;
        text-align: center;
        padding: 10px;
        font-size: 14px;d
        box-shadow: 0px -1px 5px rgba(0, 0, 0, 0.1);
    }
    </style>
    <div class="footer">
        <p> <a id ="link" href = "https://www.linkedin.com/in/karan-datascientist/">Developed by Karan </a></p>
    </div>
    """,
    unsafe_allow_html=True
)
