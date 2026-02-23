import streamlit as st
import pickle


@st.cache_resource
def load(path: str) -> object:
    """Generic function to load a pickled resource from the specified path"""
    with open(path, "rb") as f:
        return pickle.load(f)