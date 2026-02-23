import streamlit as st
from dotenv import load_dotenv

from domain.recommendation import recomendation
from infra.dataset_loader import load_dataset
from infra.resource_loader import load_encoder, load_maps, load_model
from services.tmdb_service import get_movie
from theme.style import inject_css

load_dotenv()

# ============================================================
# TRADUÇÃO DE GÊNEROS
# ============================================================

GENEROS_PT = {
    "Action": "Ação",
    "Adventure": "Aventura",
    "Animation": "Animação",
    "Biography": "Biografia",
    "Comedy": "Comédia",
    "Crime": "Crime",
    "Drama": "Drama",
    "Family": "Família",
    "Fantasy": "Fantasia",
    "Film-Noir": "Film Noir",
    "History": "História",
    "Horror": "Terror",
    "Music": "Música",
    "Musical": "Musical",
    "Mystery": "Mistério",
    "Romance": "Romance",
    "Sci-Fi": "Ficção Científica",
    "Sport": "Esporte",
    "Thriller": "Thriller",
    "War": "Guerra",
    "Western": "Faroeste"
}

def main():
    """Main function to render the Streamlit app interface and handle user interactions"""
    st.set_page_config(
        page_title="MapTheSoul",
        page_icon="🎬",
        layout="wide",
        initial_sidebar_state="collapsed"
    )

    inject_css()

    model = load_model()
    encoder = load_encoder()
    maps = load_maps()
    df = load_dataset()

    # HEADER
    st.markdown('<h1 class="main-title">MAP THE SOUL</h1>', unsafe_allow_html=True)
    st.markdown('<p class="main-subtitle">find the film that speaks to your soul</p>', unsafe_allow_html=True)
    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # PAINEL DE CONTROLES NA PÁGINA PRINCIPAL
    st.markdown('<p class="section-label">✦ &nbsp; map your moment &nbsp; ✦</p>', unsafe_allow_html=True)
    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        genero_pt = st.selectbox(
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
    genero = [k for k, v in GENEROS_PT.items() if v == genero_pt][0]

    st.markdown("<br>", unsafe_allow_html=True)

    col_btn = st.columns([3, 2, 3])
    with col_btn[1]:
        buscar = st.button("✦  revelar filmes  ✦", use_container_width=True)

    if buscar:
        st.session_state["buscar"] = True
        st.session_state["genero"] = genero
        st.session_state["genero_pt"] = genero_pt
        st.session_state["duracao"] = duracao
        st.session_state["decada"] = decada
        st.session_state["nota_minima"] = nota_minima

    st.markdown('<hr class="divider">', unsafe_allow_html=True)

    # RESULTADOS
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
                    if poster:
                        st.image(poster, width=180)
                    st.markdown(
                        f'<div class="filme-card">'
                        f'<p class="filme-titulo">{filme["Series_Title"]}</p>'
                        f'<p class="filme-meta">⭐ {filme["IMDB_Rating"]} &nbsp;·&nbsp; {st.session_state["genero_pt"]} &nbsp;·&nbsp; {filme["Runtime"]} min &nbsp;·&nbsp; {filme["Released_Year"]}</p>'
                        f'<p class="filme-sinopse">{sinopse}</p>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
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