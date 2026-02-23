import streamlit as st

def render_header(title, subtitle) -> None:
    """Render the main header of the app with the given title and subtitle"""
    st.markdown(f'<h1 class="main-title">{title}</h1>', unsafe_allow_html=True)
    st.markdown(f'<p class="main-subtitle">{subtitle}</p>', unsafe_allow_html=True)
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

def render_movie_card(movie, poster, summary, genre_pt) -> None:
    """Render a movie card with the given movie details, poster, summary, and genre in Portuguese"""
    with st.container():
        col1, col2 = st.columns([1, 2])
        with col1:
            if poster:
                st.image(poster, use_container_width=True)
        with col2:
            st.markdown(
                f'<div class="filme-card">'
                f'<p class="filme-titulo">{movie["Series_Title"]}</p>'
                f'<p class="filme-meta">⭐ {movie["IMDB_Rating"]} &nbsp;·&nbsp; {genre_pt} &nbsp;·&nbsp; {movie["Runtime"]} min &nbsp;·&nbsp; {movie["Released_Year"]}</p>'
                f'<p class="filme-sinopse">{summary}</p>'
                f'</div>',
                unsafe_allow_html=True
            )