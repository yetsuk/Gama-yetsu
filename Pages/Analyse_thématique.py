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

# --- Processus d'extraction ---

choix_extract = st.radio("Veuillez choisir le type d'extraction souhaitez",
                         ['Publication Subreddit', 'Commentaire', 'Query'])

st.write(f'Vous avez choisis: {choix_extract}')

# --- Création méthode d'extraction par catégorie ---

# Analyse Publication Subreddit
if choix_extract == 'Publication Subreddit':
        
    ## Sélection du type de corpus souhaiter    
    choix_corpus = st.radio('Veuillez choisir les textes à analyser', ['Titre', 'Contenu de publication'])

    st.write(f"Vous avez choisi d'analyser les {choix_corpus}")

     # Extraction des publications de subreddit
    communaute = st.text_input('Veullez écrire le noms du subreddit sans le "r/" ')

    if communaute:
        try:
            subreddit = reddit.subreddit(communaute)

            # Afficher les informations du subreddit
            st.write(f"Nom affiché : {subreddit.display_name}")
            st.write(f"Description : {subreddit.public_description}")
            st.write(f"Date de création : {datetime.fromtimestamp(subreddit.created_utc)}")
            st.write(f"Le subreddit '{subreddit.display_name}' compte actuellement : {subreddit.subscribers} abonnés.")


            sub_posts = subreddit.top(limit = 10)

            # Création d'un dictionnaire pour stocker les publications
            post_dict = {'Post_ID' : [], 'Texte' : []}

            if choix_corpus == 'Titre':

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

        except Exception as e:
            st.error("Erreur lors de la récupération des informations du subreddit. Veuillez vérifier le nom ou réessayer plus tard.")


elif choix_extract == 'Commentaire':
    choix_recherche = st.radio("Faire la recherche à partir d'un:", ['Lien', 'Identifiant de post'])
    st.write(f'Vous avez choisi {choix_recherche}')

    # SI UTILISATEUR UTILISE UN ID

    if choix_recherche == 'Identifiant du post':
        
        #Tentative d'extraction des commentaires
        post_id = st.text_input("Veuillez écrire l'ID du post")

        comments_dict = {}
        # Identifiant du post Reddit que vous voulez extraire
    
        # Récupération du post
        try:
            post = reddit.submission(id=post_id)

            # Affiché le post et son contenu pour que l'utilisateur puisse vérifier qu'il s'agit bien de le publication souhaité
            st.write(post.Title)
            st.write(post.selftext)

            # Extraction des commentaires
            post.comments.replace_more(limit=5)
            all_comments = post.comments.list()

            for comment in all_comments:
                comments_dict[comment.id] = {
                    'comment_author': comment.author.name if comment.author else '[deleted]',
                    'comment_body': comment.body}

            # Création d'une Dataframe pour y ajouter les commentaires et les différentes caractéristiques associés
            comment_df = pd.DataFrame(comments_dict)
            comment_df = comment_df.transpose()

        except Exception as e:
            st.error("Erreur lors de la récupération des informations du subreddit. Veuillez vérifier le nom ou réessayer plus tard.")

    else: 

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


        

            comments_dict = {}
            # Identifiant du post Reddit que vous voulez extraire
    
            # Récupération du post
            try:
                post = reddit.submission(id=post_id)

                # Affiché le post et son contenu pour que l'utilisateur puisse vérifier qu'il s'agit bien de le publication souhaité
                st.write(post.Title)
                st.write(post.selftext)

                # Extraction des commentaires
                post.comments.replace_more(limit=5)
                all_comments = post.comments.list()

                for comment in all_comments:
                    comments_dict[comment.id] = {
                        'comment_author': comment.author.name if comment.author else '[deleted]',
                        'comment_body': comment.body}

                # Création d'une Dataframe pour y ajouter les commentaires et les différentes caractéristiques associés
                comment_df = pd.DataFrame(comments_dict)
                comment_df = comment_df.transpose()

            except Exception as e:
                st.error("Erreur lors de la récupération des informations du subreddit. Veuillez vérifier le nom ou réessayer plus tard.")

else:
    try: 
        ### Extraction depuis une query

        def from_query_get_post(query):
            subreddit = reddit.subreddit("all")  # Recherche dans tout Reddit, ou spécifie un subreddit

            # Extraire les publications contenant le terme recherché
            post_dict = {'Titre': [], 'Texte': [], 'Score': [], "Nombre_Commentaire": [] }
            for submission in subreddit.search(query, limit=10):  # Ajuste le "limit" pour plus ou moins de résultats
                post_dict['Auteur'].append(submission.author)

                post_dict['Titre'].append(submission.title)



            comment_df = pd.DataFrame(post_dict)

            return comment_df    
        
        # Création de la fonction input
        query = st.text_input('Ajouter un terme à ajouter')

        if query:
            comment_df = from_query_get_post(query)
    
    except Exception as e:
        st.error("Erreur lors de la récupération des informations du subreddit. Veuillez vérifier le nom ou réessayer plus tard.")
