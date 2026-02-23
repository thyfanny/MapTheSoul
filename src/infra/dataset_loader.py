import streamlit as st
import pandas as pd

@st.cache_data
def load_dataset():
    """Load and preprocess the movie dataset"""
    df = pd.read_csv("data/imdb_top_1000.csv")
    df.dropna(subset=["Genre", "IMDB_Rating", "Runtime", "Meta_score", "No_of_Votes", "Released_Year"], inplace=True)
    df["Runtime"] = df["Runtime"].apply(lambda x: int(x.replace(" min", "").strip()))
    df["Released_Year"] = pd.to_numeric(df["Released_Year"], errors="coerce")
    df.dropna(inplace=True)
    df["Released_Year"] = df["Released_Year"].astype(int)
    return df