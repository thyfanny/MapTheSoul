from src.config.constants import APP_SUBTITLE, APP_TITLE, GENEROS_PT
from src.ui.components import render_header, render_movie_card
import streamlit as st
from dotenv import load_dotenv

from src.infra.resource_loader import load
from src.services.tmdb_service import get_movie
from src.theme.style import inject_css
from src.infra.dataset_loader import load_dataset
from src.domain.recommendation import recomendation


load_dotenv()

@st.cache_resource
def load_assets():
    """Load all necessary assets for the app, including the model, label encoder, maps, and dataset"""
    return load("models/model.pkl"), load("models/label_encoder.pkl"), \
           load("models/maps.pkl"), load_dataset()

def main():
    """Main function to render the Streamlit app interface and handle user interactions"""
    st.set_page_config(page_title="MapTheSoul", page_icon="🎬", layout="wide")
    inject_css()

    model, encoder, maps, df = load_assets()

    render_header(APP_TITLE, APP_SUBTITLE)
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        genre_pt = st.selectbox(
            "qual gênero você prefere?",
            [GENEROS_PT[g] for g in maps["generos"]]
        )

    with col2:
        duracao = st.selectbox(
            "quanto tempo você tem?",
            list(maps["duracao"].keys())
        )

    with col3:
        decada = st.selectbox(
            "prefere filmes de qual época?",
            list(maps["decada"].keys())
        )

    with col4:
        nota_minima = st.slider(
            "nota mínima no imdb",
            min_value=7.0,
            max_value=10.0,
            value=7.5,
            step=0.1
        )

    # Converte gênero de volta para inglês
    genero = [k for k, v in GENEROS_PT.items() if v == genre_pt][0]

    st.markdown("<br>", unsafe_allow_html=True)

    col_btn = st.columns([3, 2, 3])
    with col_btn[1]:
        buscar = st.button("✦  revelar filmes  ✦", use_container_width=True)

    if buscar:
        st.session_state["buscar"] = True
        st.session_state["genero"] = genero
        st.session_state["genero_pt"] = genre_pt
        st.session_state["duracao"] = duracao
        st.session_state["decada"] = decada
        st.session_state["nota_minima"] = nota_minima

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # SEARCH
    if st.session_state.get("buscar"):
        with st.spinner("mapeando sua alma cinematográfica..."):
            recomendados = recomendation(
                st.session_state["genero"],
                st.session_state["duracao"],
                st.session_state["decada"],
                st.session_state["nota_minima"],
                model, encoder, maps, df
            )

        if recomendados.empty:
            st.warning("nenhum filme encontrado. tente ajustar suas preferências.")
        else:
            st.markdown(f'<p class="step-item">✦ {len(recomendados)} filmes encontrados para a sua alma ✦</p>', unsafe_allow_html=True)
            st.markdown("<br>", unsafe_allow_html=True)

            cols = st.columns(2)
            for i, (_, filme) in enumerate(recomendados.iterrows()):
                poster, sinopse = get_movie(filme["Series_Title"])
                with cols[i % 2]:
                    render_movie_card(filme, poster, sinopse, genre_pt)
    else:
        st.markdown("<br><br>", unsafe_allow_html=True)
        st.markdown("""
        <p class="welcome-text">
            every soul has a story.<br>
            every story has a film.<br>
            <br>
            map yours.
        </p>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()