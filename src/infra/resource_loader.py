import streamlit as st
import pickle

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