# ============================================================
# MapTheSoul - Estilização CSS
# ============================================================

import streamlit as st

def inject_css():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Cormorant+Garamond:ital,wght@0,300;0,400;0,600;1,300;1,400&family=Josefin+Sans:wght@100;300;400&display=swap');

    html, body, [class*="css"] {
        font-family: 'Josefin Sans', sans-serif;
        background-color: #0a0a0a;
        color: #e8d5a3;
    }

    .stApp {
        background: radial-gradient(ellipse at top, #1a1200 0%, #0a0a0a 60%);
        min-height: 100vh;
    }

    .main-title {
        font-family: 'Cormorant Garamond', serif;
        font-size: 4.5rem;
        font-weight: 300;
        letter-spacing: 0.3em;
        color: #c9a84c;
        text-align: center;
        margin-bottom: 0;
        text-shadow: 0 0 40px rgba(201, 168, 76, 0.3);
    }

    .main-subtitle {
        font-family: 'Josefin Sans', sans-serif;
        font-size: 0.85rem;
        font-weight: 100;
        letter-spacing: 0.5em;
        color: #8a7a5a;
        text-align: center;
        text-transform: uppercase;
        margin-top: 0.2rem;
        margin-bottom: 2rem;
    }

    .section-label {
        font-size: 0.75rem;
        font-weight: 100;
        letter-spacing: 0.5em;
        color: #6a5a3a;
        text-transform: uppercase;
        text-align: center;
    }

    .divider {
        border: none;
        border-top: 1px solid #2a2010;
        margin: 1.5rem 0;
    }

    /* SELECTBOX */
    [data-testid="stSelectbox"] > div > div {
        background-color: #111000 !important;
        border: 1px solid #3a2e10 !important;
        color: #e8d5a3 !important;
        border-radius: 0 !important;
    }

    /* SLIDER */
    [data-testid="stSlider"] * {
        color: #c9a84c !important;
    }

    /* BOTÃO */
    .stButton > button {
        background: linear-gradient(135deg, #c9a84c 0%, #8a6a20 100%);
        color: #0a0a0a !important;
        border: none;
        border-radius: 0;
        font-family: 'Josefin Sans', sans-serif;
        font-weight: 400;
        letter-spacing: 0.4em;
        text-transform: uppercase;
        font-size: 0.8rem;
        padding: 0.8rem 1rem;
        width: 100%;
        transition: all 0.3s ease;
    }

    .stButton > button:hover {
        background: linear-gradient(135deg, #e8c870 0%, #c9a84c 100%);
        transform: translateY(-1px);
        box-shadow: 0 8px 25px rgba(201, 168, 76, 0.3);
    }

    /* CARDS DE FILME */
    .filme-card {
        background: linear-gradient(145deg, #111000, #0d0c00);
        border: 1px solid #2a2010;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        position: relative;
        transition: border-color 0.3s ease;
    }

    .filme-card:hover {
        border-color: #c9a84c;
    }

    .filme-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        width: 3px;
        height: 100%;
        background: linear-gradient(180deg, #c9a84c, #8a6a20);
    }

    .filme-titulo {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.6rem;
        font-weight: 400;
        color: #c9a84c;
        letter-spacing: 0.05em;
        margin-bottom: 0.3rem;
    }

    .filme-meta {
        font-size: 0.7rem;
        font-weight: 100;
        letter-spacing: 0.3em;
        color: #6a5a3a;
        text-transform: uppercase;
        margin-bottom: 1rem;
    }

    .filme-sinopse {
        font-size: 0.9rem;
        font-weight: 300;
        color: #a09070;
        line-height: 1.7;
        font-style: italic;
    }

    /* WELCOME */
    .welcome-text {
        font-family: 'Cormorant Garamond', serif;
        font-size: 1.2rem;
        font-weight: 300;
        font-style: italic;
        color: #6a5a3a;
        text-align: center;
        letter-spacing: 0.1em;
        line-height: 2;
    }

    .step-item {
        font-size: 0.8rem;
        font-weight: 100;
        letter-spacing: 0.3em;
        color: #8a7a5a;
        text-transform: uppercase;
        text-align: center;
        margin: 0.5rem 0;
    }

    .step-number {
        color: #c9a84c;
        font-family: 'Cormorant Garamond', serif;
        font-size: 1rem;
    }

    /* LABELS */
    label {
        font-size: 0.75rem !important;
        font-weight: 300 !important;
        letter-spacing: 0.3em !important;
        text-transform: uppercase !important;
        color: #8a7a5a !important;
    }

    /* SCROLLBAR */
    ::-webkit-scrollbar { width: 4px; }
    ::-webkit-scrollbar-track { background: #0a0a0a; }
    ::-webkit-scrollbar-thumb { background: #3a2e10; }
    ::-webkit-scrollbar-thumb:hover { background: #c9a84c; }

    /* ESCONDE ELEMENTOS DO STREAMLIT */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    [data-testid="stSidebar"] {display: none !important;}
    </style>
    """, unsafe_allow_html=True)