import streamlit as st
from recommender import recommend
import requests

# ---------------- TMDB CONFIG ----------------
API_KEY = "your_tmdb_api_key"

def fetch_poster(title):
    try:
        url = f"https://api.themoviedb.org/3/search/tv?api_key={API_KEY}&query={title}&language=ko-KR"
        data = requests.get(url).json()

        if data['results']:
            for result in data['results']:
                # Prefer Korean shows
                if result.get('origin_country') == ['KR'] or result.get('original_language') == 'ko':
                    poster_path = result.get('poster_path')
                    if poster_path:
                        return f"https://image.tmdb.org/t/p/w500{poster_path}"

            # fallback (if no KR match)
            poster_path = data['results'][0].get('poster_path')
            if poster_path:
                return f"https://image.tmdb.org/t/p/w500{poster_path}"

    except:
        pass

    return "https://via.placeholder.com/300x450?text=No+Image"

# ---------------- UI ----------------
st.set_page_config(page_title="Drama Recommender", page_icon="🎬")

st.title("🎬 Drama Recommender")
st.write("Find Korean dramas based on your taste!")

# Sidebar filters
st.sidebar.header("Filters")
min_rating = st.sidebar.slider("Minimum Rating", 0, 10, 5)
genre = st.sidebar.text_input("Genre (optional)")
num_recommendations = st.sidebar.slider("Number of Recommendations", 1, 10, 5)

# Input
user_input = st.text_input("Enter a drama name")

if st.button("Recommend"):
    if user_input:
        results = recommend(user_input, min_rating, genre, num_recommendations)

        if not results:
            st.warning("No recommendations found")
        else:
            st.subheader("🎯 Recommendations")

            for idx, drama in enumerate(results):

                col1, col2 = st.columns([1, 2])

                # Poster
                with col1:
                    poster = fetch_poster(drama['title'])
                    st.image(poster, use_container_width=True)

                # Details
                with col2:
                    st.markdown(f"### {drama['title']}")
                    st.write(f"⭐ Rating: {drama['rating']}")
                    st.write(f"🎭 Genre: {drama['genres']}")

                    # Expandable synopsis
                    with st.expander("📖 Show Synopsis"):
                        st.write(drama.get('description', 'No synopsis available'))

                st.markdown("---")

    else:
        st.warning("Please enter a drama name")
