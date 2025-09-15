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


# --- Présentation du Projet ---

st.markdown(
    '''
    <div style= 'text-align: center; font-size: 18px; line-height: 1.6;'>
    Application d'extraction et d'analyse de publication Reddit utilisant python et praw pour accéder à l'API de Reddit.
    Possible de réaliser deux types d'analyses.

    </div>
    ''',
    unsafe_allow_html=True)

# Ajouter un grand espace
st.markdown("<div style='margin-top: 65px;'></div>", unsafe_allow_html=True)

# --- Présentation des deux parties du Projets ---

# Création de deux colonnes
col1, col2, col3 = st.columns([1,0.4,1])

# Premiere analyse
with col1:
    st.markdown(
        """
        <div style="text-align: center; font-size: 18px; line-height: 1.6; margin: 10px 0;">
            <h3>Analyse Descriptive</h3>
            <p> Analyse descriptive de l'activité du Subreddit (nombre de post, nombre d'auteur, auteur les plus influents...).</p>

        </div>
        """,
        unsafe_allow_html=True)

# Ligne de séparation
with col2:
    st.markdown(
        """
        <div style="border-left: 2px solid red; height: 100%; margin: auto;"></div>
        """,
        unsafe_allow_html=True
    )

# Deuxième analyse
with col3:
    st.markdown(
        """
        <div style="text-align: center; font-size: 18px; line-height: 1.6; margin: 10px 0;">
            <h3>Analyse Textuelle</h3>
            <p> Analyse des publications visibles au sein d'une communauté permettant d'identifié les thèmes abordés.</p>

        </div>
        """,
        unsafe_allow_html=True
    )