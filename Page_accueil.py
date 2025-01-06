import streamlit as st

st.set_page_config(
        page_title='Projet: Gama - Yetsu',
        layout="wide"
    )



# --- Titre de le Page ---

# Centrer le header
st.markdown(
    """
    <h1 style='text-align: center;'>Projet - GAMA</h1>
    """,
    unsafe_allow_html=True
)

# --- Sous-titre de la Page ---

st.markdown(
    """
    <h3 style='text-align: center; color: grey;'>Extraction et Analyse de publication Reddit</h3>
    """,
    unsafe_allow_html=True
)

