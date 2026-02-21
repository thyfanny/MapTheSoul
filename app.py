# ============================================================
# MapTheSoul
# ============================================================

import streamlit as st
import pandas as pd
import pickle
import requests
import os
from dotenv import load_dotenv
from style import inject_css

load_dotenv()
TMDB_API_KEY = os.getenv("TMDB_API_KEY")

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

# ============================================================
# CARREGAMENTO DE RECURSOS
# ============================================================

@st.cache_resource
def load_model():
    with open("data/model.pkl", "rb") as f:
        return pickle.load(f)

@st.cache_resource
def load_encoder():
    with open("data/label_encoder.pkl", "rb") as f:
        return pickle.load(f)

@st.cache_resource
def load_maps():
    with open("data/maps.pkl", "rb") as f:
        return pickle.load(f)

@st.cache_data
def load_dataset():
    df = pd.read_csv("data/imdb_top_1000.csv")
    df.dropna(subset=["Genre", "IMDB_Rating", "Runtime", "Meta_score", "No_of_Votes", "Released_Year"], inplace=True)
    df["Runtime"] = df["Runtime"].apply(lambda x: int(x.replace(" min", "").strip()))
    df["Released_Year"] = pd.to_numeric(df["Released_Year"], errors="coerce")
    df.dropna(inplace=True)
    df["Released_Year"] = df["Released_Year"].astype(int)
    return df

# ============================================================
# TMDB
# ============================================================

def buscar_filme_tmdb(titulo):
    url = "https://api.themoviedb.org/3/search/movie"
    params = {"api_key": TMDB_API_KEY, "query": titulo, "language": "pt-BR"}
    try:
        response = requests.get(url, params=params)
        data = response.json()
        if data["results"]:
            filme = data["results"][0]
            poster = f"https://image.tmdb.org/t/p/w500{filme['poster_path']}" if filme.get("poster_path") else None
            sinopse = filme.get("overview", "Sinopse não disponível.")
            return poster, sinopse
    except:
        pass
    return None, "Sinopse não disponível."

# ============================================================
# RECOMENDAÇÃO
# ============================================================

def recomendar_filmes(genero, duracao, decada, nota_minima, model, encoder, maps, df):
    """Filtra e classifica filmes com base nas preferências do usuário"""

    # Filtra filmes que contenham o gênero escolhido em qualquer posição
    df_filtrado = df[df["Genre"].apply(lambda x: genero in [g.strip() for g in x.split(",")])].copy()

    min_dur, max_dur = maps["duracao"][duracao]
    df_filtrado = df_filtrado[
        (df_filtrado["Runtime"] >= min_dur) &
        (df_filtrado["Runtime"] <= max_dur)
    ]

    if maps["decada"][decada] is not None:
        min_ano, max_ano = maps["decada"][decada]
        df_filtrado = df_filtrado[
            (df_filtrado["Released_Year"] >= min_ano) &
            (df_filtrado["Released_Year"] <= max_ano)
        ]

    df_filtrado = df_filtrado[df_filtrado["IMDB_Rating"] >= nota_minima]

    if df_filtrado.empty:
        return pd.DataFrame()

    df_filtrado["Genre_encoded"] = encoder.transform([genero] * len(df_filtrado))

    features = ["Genre_encoded", "Runtime", "Meta_score", "No_of_Votes"]
    df_filtrado["Recomendado"] = model.predict(df_filtrado[features])

    recomendados = df_filtrado[df_filtrado["Recomendado"] == 1][
        ["Series_Title", "Genre", "IMDB_Rating", "Runtime", "Released_Year"]
    ].copy()

    return recomendados.sample(frac=1).head(10)

# ============================================================
# INTERFACE PRINCIPAL
# ============================================================

def main():
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
            recomendados = recomendar_filmes(
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
                poster, sinopse = buscar_filme_tmdb(filme["Series_Title"])
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