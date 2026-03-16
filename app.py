import streamlit as st
import pandas as pd
import pickle
import requests

# PAGE CONFIG
st.set_page_config(page_title="Netflix AI Recommender", layout="wide")

# ---------- BACKGROUND + CSS ----------
st.markdown("""
<style>

.stApp{
background-image: url("https://images.unsplash.com/photo-1489599849927-2ee91cede3ba");
background-size: cover;
background-position: center;
}

.title{
font-size:65px;
font-weight:bold;
text-align:center;
color:#E50914;
}

.movie-card{
background:rgba(0,0,0,0.75);
padding:12px;
border-radius:15px;
text-align:center;
transition:0.3s;
}

.movie-card:hover{
transform:scale(1.08);
box-shadow:0px 0px 15px #E50914;
}

.rating{
color:gold;
font-size:18px;
}

</style>
""", unsafe_allow_html=True)

st.markdown('<p class="title">🎬 Netflix AI Movie Recommender</p>', unsafe_allow_html=True)


# ---------- LOAD DATA ----------
import pickle

with open("movie_dict.pkl","rb") as f:
    movies_dict = pickle.load(f)
movies = pd.DataFrame(movies_dict)

similarity = pickle.load(open("similarity.pkl","rb"))

API_KEY = "YOUR_TMDB_API_KEY"


# ---------- POSTER FUNCTION ----------
def fetch_movie(movie_id):

    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={API_KEY}"

        data = requests.get(url).json()

        poster = data.get("poster_path")
        rating = data.get("vote_average")

        if poster:
            poster_url = "https://image.tmdb.org/t/p/w500/" + poster
        else:
            poster_url = "https://via.placeholder.com/500x750"

        return poster_url, rating

    except:
        return "https://via.placeholder.com/500x750", "N/A"


# ---------- RECOMMEND FUNCTION ----------
def recommend(movie):

    movie_index = movies[movies['title']==movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x:x[1]
    )[1:6]

    names=[]
    posters=[]
    ratings=[]

    for i in movies_list:

        movie_id = movies.iloc[i[0]].movie_id

        poster,rating = fetch_movie(movie_id)

        names.append(movies.iloc[i[0]].title)
        posters.append(poster)
        ratings.append(rating)

    return names,posters,ratings


# ---------- AI SEARCH ----------
search = st.text_input("🔎 Search Movie")

if search:

    results = movies[movies['title'].str.contains(search,case=False)]

    st.write("Search Results")

    cols = st.columns(5)

    for col,(i,row) in zip(cols,results.head(5).iterrows()):

        poster,_ = fetch_movie(row.movie_id)

        with col:

            st.image(poster)

            st.caption(row.title)


# ---------- MOVIE SELECT ----------
selected_movie = st.selectbox(
"🎥 Choose a movie",
movies['title'].values
)

if st.button("🍿 Recommend Movies"):

    names,posters,ratings = recommend(selected_movie)

    cols = st.columns(5)

    for col,name,poster,rating in zip(cols,names,posters,ratings):

        with col:

            st.markdown('<div class="movie-card">', unsafe_allow_html=True)

            st.image(poster)

            st.write(name)

            st.markdown(
                f'<p class="rating">⭐ {rating}</p>',
                unsafe_allow_html=True
            )

            st.markdown('</div>', unsafe_allow_html=True)


# ---------- TRENDING SECTION ----------
st.subheader("🔥 Trending Movies")

trend_cols = st.columns(6)

sample_movies = movies.sample(6)

for col,(i,row) in zip(trend_cols,sample_movies.iterrows()):

    poster,_ = fetch_movie(row.movie_id)

    with col:

        st.image(poster)

        st.caption(row.title)
import pickle

movies_dict = movies.to_dict()

pickle.dump(movies_dict, open("movie_dict.pkl", "wb"))
pickle.dump(similarity, open("similarity.pkl", "wb"))

print("Files created successfully")
