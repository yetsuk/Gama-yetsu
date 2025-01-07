# --- Analyse Textuelle Reddit ---

# --- Accès code d'accès API
from dotenv import load_dotenv ## Accès au fichier .env
import os
# Chemin vers le fichier .env dans le dossier principal
from pathlib import Path
dotenv_path = Path(__file__).resolve().parent.parent / ".env"

# Charger les variables d'environnement
load_dotenv(dotenv_path=dotenv_path)


# --- Importation des Modules ---
import streamlit as st
## MAnipulation des données
import pandas as pd
import numpy as np

## Extractions des données
import praw

## Text Mining
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.neighbors import NearestNeighbors
from sklearn.cluster import DBSCAN
from collections import Counter
from sklearn.decomposition import PCA
from datetime import datetime


## Visualisation de données
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Nettoyage des donnéees
import spacy
from langdetect import detect, LangDetectException


st.title('Analyse textuelle Reddit')
st.write(''' 
         Cette page est un script réalisé avec Python qui a pour principe d'extraire puis analyser un corpus de texte issue de l'application
         Reddit. En premier lieu, le script propose de sélectionner le type d'élement que vous voulez extraire entre trois options: les posts de subreddit,
         les commentaires d'un même post, ou un ensemble de post trouvé à la suite d'une query. Dans le cas des publications des subreddits, le code propose
         une seconde option qui est la sélection entre les titres des publications et le contenu de la publication qui donne d'avantage d'information sur les 
         sujets abordés en son sein. 
         
         L'objectif principale est de réaliser une analyse thématique des publications Reddit afin d'en retenir les sujets qui peuvent abordés dans les conversations
         des membres du réseau. Cette analyse se fait uniquement avec Python et différents packages permettant l'analyse de donnée textuelle comme spacy et sklearn.
         Les résultats obtenus sont ensuite visualisé à l'aide plusieurs graphes qui seront affiché en fin de processus. ''')


# --- Ajout Instance de connexion Reddit --- 
try:
    reddit = praw.Reddit(client_id =  os.getenv('client_id'), 
                     client_secret = os.getenv('client_secret'),
                     user_agent = os.getenv('user_agent'))
    
except Exception as e:
    st.error("Erreur de connexion à l'API Reddit. Veuillez vérifier vos identifiants.")
    st.stop()




##################################################
# Définition des Fonctions pour analyse thématique
##################################################

# --- Choix des critères d'extraction ---
def choix_extraction():
    choix_extract = st.radio("Veuillez choisir le type d'extraction souhaitez",
                         ['Publication Subreddit', 'Commentaire', 'Query'])

    st.write(f'Vous avez choisis: {choix_extract}')


# Choix du corpus à analyser
def choix_corpus():
    list_corpus = ['Titre', 'Contenu de Publication']
    choix_corpus = st.radio('Veuillez choisir les corpus que vous souhaitez analyser', list_corpus )
    st.write(f'Vous avez choisis: {choix_corpus}')



# Choix source de recherche
def choix_source():
    list_source = ['Lien', 'N° Identification']
    choix_source = st.radio('Veuillez Choisir la source qui va vous servir de requête', list_source)
    st.write(f'Vous avez choisis: {choix_source}')
    return choix_source



# --- Extraction des publications Reddit ---
def extract_post(subreddit, choix_corpus):
    corpus = choix_corpus

    sub_posts = subreddit.top(limit = 10)

    # Création d'un dictionnaire pour stocker les publications
    post_dict = {'Post_ID' : [], 'Texte' : []}

    if corpus == 'Titre':
        for post in sub_posts:
            post_dict['Post_ID'].append(post.id)
            post_dict['Texte'].append(post.title)

            df_post = pd.DataFrame(post_dict)
        
        
    else:
        for post in sub_posts:
            post_dict['Post_ID'].append(post.id)
            post_dict['Texte'].append(post.selftext)
            df_post = pd.DataFrame(post_dict)

        # Affichage de la dataframe
        st.dataframe(df_post)

        return df_post



# Affichage des informations d'une communauté
def display_info(communaute):
    subreddit = reddit.subreddit(communaute)
    # Afficher les informations du subreddit
    st.write(f"Nom affiché : {subreddit.display_name}")
    st.write(f"Description : {subreddit.public_description}")
    st.write(f"Date de création : {datetime.fromtimestamp(subreddit.created_utc)}")
    st.write(f"Le subreddit '{subreddit.display_name}' compte actuellement : {subreddit.subscribers} abonnés.")



# Affhicher les informations d'une publication
def display_post_info(post):
    st.write(post.title)
    st.write(post.selftext)



# Nettoyage des liens
def from_link_get_id(link):
     #Tentative d'extraction des commentaires
    link = st.text_input("Veuillez écrire le lien du post")

    # Nettoyage du lien pour obtenir l'id du post
    if link:
        url = link.split('/')

        # Vérifiez que l'URL a au moins 7 segments
        if len(url) > 6:
            post_id = url[6]
            st.write(f"ID du post extrait : {post_id}")
        else:
            st.error("Lien invalide. Veuillez entrer un lien de post Reddit complet.")
            post_id = None




# Extraction des commentaires
def extract_comment(post):
    comments_dict = {}
    post.comments.replace_more(limit=5)
    all_comments = post.comments.list()

    for comment in all_comments:
        comments_dict[comment.id] = {
            'comment_author': comment.author.name if comment.author else '[deleted]',
            'comment_body': comment.body}

    # Création d'une Dataframe pour y ajouter les commentaires et les différentes caractéristiques associés
    comment_df = pd.DataFrame(comments_dict)
    comment_df = comment_df.transpose()

    return comment_df



# Extraction des posts depuis une query
def from_query_get_post(query):
            subreddit = reddit.subreddit("all")  # Recherche dans tout Reddit, ou spécifie un subreddit

            # Extraire les publications contenant le terme recherché
            post_dict = {'Titre': [], 'Texte': [], 'Score': [], "Nombre_Commentaire": [] }
            for submission in subreddit.search(query, limit=10):  # Ajuste le "limit" pour plus ou moins de résultats
                post_dict['Auteur'].append(submission.author)

                post_dict['Titre'].append(submission.title)



            comment_df = pd.DataFrame(post_dict)

            return comment_df    