import pickle
import streamlit as st
import requests

st.set_page_config(layout='wide')

st.markdown("""
    <style>
    /* Background and text styling */
    body {
        background-color: #1f1f1f;
        color: #e0e0e0;
    }
    .stApp {
        background-color: #121212;
    }
    /* Header styling */
    h1, h2, h3, h4, h5, h6 {
        color: #ffffff;
        font-family: 'Helvetica', sans-serif;
    }
    /* Recommendation card styling */
    .movie-container {
        display: flex;
        justify-content: space-between;
        padding: 10px;
    }
    .movie {
        text-align: center;
        margin: 10px;
        color: white;
    }
    img {
        border-radius: 8px;
    }
    </style>
    """, unsafe_allow_html=True)

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=6490bc6eafb034a5a6b7f697dd323a3e".format(movie_id)
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path')  # Use .get() to avoid KeyError if 'poster_path' is missing
    if poster_path:  # Check if the poster_path is not None
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    else:
        return None  # Handle cases where there's no poster available




def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]]['id']  # Access the column named 'id'
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters


st.header('Movie Recommender System')
movies = pickle.load(open('movies_pkl.pkl','rb'))
similarity = pickle.load(open('similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)  # Updated method
    with col1:
         st.image(recommended_movie_posters[0])
         st.text(recommended_movie_names[0])
       
    with col2:
        st.image(recommended_movie_posters[1])
        st.text(recommended_movie_names[1])
        
    with col3:
        st.image(recommended_movie_posters[2])
        st.text(recommended_movie_names[2])
        
    with col4:
        st.image(recommended_movie_posters[3])
        st.text(recommended_movie_names[3])
        
    with col5:
        st.image(recommended_movie_posters[4])
        st.text(recommended_movie_names[4])


st.markdown("""
    <hr>
    <div style="text-align: center; padding: 10px; color: #e0e0e0;">
        <p>🎥 Movie Recommender System | Built by Mueezuddin Ahmed</p>
    </div>
""", unsafe_allow_html=True)

