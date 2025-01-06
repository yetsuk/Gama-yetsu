import streamlit as st
import praw

# Manipulation de donnée
import numpy as np
import pandas as pd
from datetime import datetime
import spacy
from langdetect import detect, LangDetectException

# Visualisation de donnée
import statsmodels as stats
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import plotly.express as px

# --- Accès code d'accès API
from dotenv import load_dotenv ## Accès au fichier .env
import os
# Chemin vers le fichier .env dans le dossier principal
from pathlib import Path
dotenv_path = Path(__file__).resolve().parent.parent / ".env"

# Charger les variables d'environnement
load_dotenv(dotenv_path=dotenv_path)



st.title('Analyse statistique des subreddit')
st.write(''' Cette page est un script permettant d'analyser les statistiques concernant une communauté Reddit (autrement dit subreddit) 
            en particulier. Tout d'abord elle extrait l'ensemble des posts de ce subreddit afin de les implanter dans une dataframe comportant plusieurs variables:

- l'auteur du post
- le titre du post
- le texte que le post contient
- le nombre de commentaire
- le score du post aussi appelé karma
- la date de publication

L'algorithme renvoit alors une analyse globale du subreddit. ''')

# --- Initialisation de l'accès à l'API ---
try:
    reddit = praw.Reddit(client_id =  os.getenv('clien_id'), 
                     client_secret = os.getenv('client_secret'),
                     user_agent = os.getenv('user_agent'))
    
except Exception as e:
    st.error("Erreur de connexion à l'API Reddit. Veuillez vérifier vos identifiants.")
    st.stop()

# --- Début de l'algorithme ---

# Sélection du subreddit
communaute = st.text_input("Veuillez écrire le nom du subreddit (sans le 'r/')")


# --- Extractions des posts ---

# Vérification si un nom de subreddit a été saisi
if communaute:
    try:
        subreddit = reddit.subreddit(communaute)

        # Afficher les informations du subreddit
        st.write(f"Nom affiché : {subreddit.display_name}")
        st.write(f"Description : {subreddit.public_description}")
        st.write(f"Date de création : {datetime.fromtimestamp(subreddit.created_utc)}")
        st.write(f"Le subreddit '{subreddit.display_name}' compte actuellement : {subreddit.subscribers} abonnés.")
        
        # --- Extraction des posts ---
        posts = subreddit.top(limit=None)  
        posts_dict = {
            'Auteur': [], "Title": [], "Post Text": [], "ID": [],
            "Score": [], "Total Comments": [], "Post URL": [], "Date": []
        }

        # Extraction des informations de chaque post
        for post in posts:
            posts_dict['Auteur'].append(post.author.name if post.author else "N/A")
            posts_dict["Title"].append(post.title)
            posts_dict["ID"].append(post.id)
            posts_dict["Post Text"].append(post.selftext)
            posts_dict["Score"].append(post.score)
            posts_dict["Total Comments"].append(post.num_comments)
            posts_dict["Post URL"].append(post.url)
            posts_dict["Date"].append(datetime.fromtimestamp(post.created_utc))

        top_posts = pd.DataFrame(posts_dict)
        top_posts = top_posts.drop_na(subset = ['Auteur'])
        st.write("Données des posts récupérées avec succès !")

        # --- Analyse statistique ---
        st.header('Informations principales')
        nb_publications = len(top_posts)
        nb_auteurs = top_posts['Auteur'].nunique()
        ratio_pub_auteur = round(nb_publications / nb_auteurs, 2)

        stat_post = pd.DataFrame({
            'Statistiques': ['Nombre de publications', "Nombre d'auteurs", 'Ratio Publication / Auteur'],
            'Valeurs': [nb_publications, nb_auteurs, ratio_pub_auteur]
        })

        st.write(f'Voici les statistiques principales du subreddit {communaute}')
        st.dataframe(stat_post)

        # --- Top 5 Auteurs ---
        top_auteurs = top_posts['Auteur'].value_counts().head(5).reset_index()
        top_auteurs.columns = ['Auteur', 'Nombre de publications']
        st.write('Voici les 5 membres ayant publié le plus')
        st.dataframe(top_auteurs)

        # --- Description des variables Score et Total Comments ---
        st.header('Description des variables Score et Commentaires')
        for var in ['Score', 'Total Comments']:
            stat_df = pd.DataFrame({
                "Statistiques": ["Moyenne", "Médiane", "Écart-type", "Minimum", "Maximum", "Premier quartile (Q1)", "Troisième quartile (Q3)"],
                "Valeurs": [
                    top_posts[var].mean().round(2), top_posts[var].median(), top_posts[var].std().round(2),
                    top_posts[var].min(), top_posts[var].max(),
                    top_posts[var].quantile(0.25), top_posts[var].quantile(0.75)
                ]
            })
            st.write(f'Description de la variable {var}')
            st.dataframe(stat_df)

        # --- Rythme de publication dans le temps ---
        top_posts['Date'] = pd.to_datetime(top_posts['Date']).dt.to_period('M')
        df_count = top_posts.groupby('Date').size().reset_index(name='Nombre de posts')

        # Tracer l'évolution du nombre de posts au fil du temps
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(df_count['Date'].astype(str), df_count['Nombre de posts'], marker='o')
        ax.set_xlabel("Date")
        ax.set_ylabel("Nombre de posts")
        ax.set_title("Évolution du nombre de posts Reddit par mois")
        ax.grid(True)
        plt.xticks(rotation=45)
        plt.tight_layout()

        # Afficher le plot
        st.write('Nombre de post publié par mois')
        st.pyplot(fig)

    except Exception as e:
        st.error("Erreur lors de la récupération des informations du subreddit. Veuillez vérifier le nom ou réessayer plus tard.")