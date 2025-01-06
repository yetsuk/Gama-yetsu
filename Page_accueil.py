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
    Programme d'extraction et d'analyse de post Reddit. L'objectif étant de mieux comprendre les thèmes abordés au sein d'un subreddit ou
    au cours d'une échange dans les commentaires d'un post. Les méthodes utilisés dans le programme s'inspire des méthodes utilisés lors de la production de mon mémoire de fin d'étude en 
    Data Science et Société Numérique. Le programme que je réalise se compose de deux parties distinctes:

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
            <p> Analyse de l'activité d'un subreddit (autrement appelé communauté) en relevant diverse information: nombre de post, nombre de commentaire,
            score de la publication, etc. A cela s'ajoute des informations sur les auteurs de post afin de rendre compte des individus pouvant être influant dans le
            réseau.</p>

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
            <p> Analyse des thèmes abordés au sein d'un subredit, des commentaires ou au sujet d'un élément recherchés comme une simple query.
            Permet d'obtenir plus d'information sur les sujets abordés et les éléments de langages utilisés.</p>

        </div>
        """,
        unsafe_allow_html=True
    )