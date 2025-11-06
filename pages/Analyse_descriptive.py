
# Accès API et page de l'application
import streamlit as st
import praw

# Manipulation de donnée
import pandas as pd
from datetime import datetime

# Visualisation de donnée
import matplotlib.pyplot as plt


st.set_page_config(page_title = 'Analyse Statistique')

st.title('Analyse statistique de subreddit')
st.write(''' Choisissez la communauté Reddit de votre choix et obtenait une analyse statistique de son activité.''')

# --- Initialisation de l'accès à l'API ---
try:
    reddit = praw.Reddit(client_id =  st.secrets['client_id'], 
                     client_secret = st.secrets['client_secret'],
                     user_agent = st.secrets['user_agent'])
    
except Exception as e:
    st.error("Erreur de connexion à l'API Reddit. Veuillez vérifier vos identifiants.")
    st.stop()


############################################################
#--- Définition des fonctions pour analyse descriptive ---
############################################################

# --- Affiche l'entête de la communauté
def show_subreddit_header(subreddit):
    # Afficher les informations du subreddit
    st.write(f"Nom affiché : {subreddit.display_name}")
    st.write(f"Description : {subreddit.public_description}")
    st.write(f"Date de création : {datetime.fromtimestamp(subreddit.created_utc)}")
    st.write(f"Le subreddit '{subreddit.display_name}' compte actuellement : {subreddit.subscribers} abonnés.")
        
# --- Extraction des posts ---
def extract_into_df(subreddit):
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
    top_posts = top_posts.dropna(subset = ['Auteur'])

    return top_posts



# --- Analyse statistique ---

def stats_analysis(top_posts):
        nb_publications = len(top_posts)
        nb_auteurs = top_posts['Auteur'].nunique()
        ratio_pub_auteur = round(nb_publications / nb_auteurs, 2)

        statistics = pd.DataFrame({
            'Statistiques': ['Nombre de publications', "Nombre d'auteurs", 'Ratio Publication / Auteur'],
            'Valeurs': [nb_publications, nb_auteurs, ratio_pub_auteur]
        })
        st.dataframe(statistics)



# --- Top 5 Auteurs ---
def print_top5(top_posts):
    top_auteurs = top_posts['Auteur'].value_counts().head(5).reset_index()
    top_auteurs.columns = ['Auteur', 'Nombre de publications']
    st.write('Voici les 5 membres ayant publié le plus')
    st.dataframe(top_auteurs)


# --- Description des variables Score et Total Comments ---
def describe_score_comments(top_posts):

    # Initialisation d'un dictionnaire pour stocker les statistiques
    stats = {
        "Statistiques": ["Moyenne", "Médiane", "Écart-type", "Minimum", "Maximum", 
                         "Premier quartile (Q1)", "Troisième quartile (Q3)"]
    }

    # Calcul des statistiques pour chaque variable et ajout au dictionnaire
    for var in ['Score', 'Total Comments']:
        stats[var] = [
            top_posts[var].mean().round(2), 
            top_posts[var].median(), 
            top_posts[var].std().round(2),
            top_posts[var].min(), 
            top_posts[var].max(),
            top_posts[var].quantile(0.25), 
            top_posts[var].quantile(0.75)
        ]

    # Conversion du dictionnaire en DataFrame
    combined_stats = pd.DataFrame(stats)

    # Affichage du tableau combiné
    st.dataframe(combined_stats)



# --- Rythme de publication dans le temps ---
def rythme_publication(top_posts):
    top_posts['Date'] = pd.to_datetime(top_posts['Date']).dt.to_period('M')
    df_count = top_posts.groupby('Date').size().reset_index(name='Nombre de posts')
    
    # Tracer l'évolution du nombre de posts au fil du temps
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df_count['Date'].astype(str), df_count['Nombre de posts'], marker='o', linewidth=2, markersize=6)
    ax.set_xlabel("Date", fontsize=12)
    ax.set_ylabel("Nombre de posts", fontsize=12)
    ax.set_title("Évolution du nombre de posts Reddit par mois", fontsize=14, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    # Améliorer la lisibilité de l'axe des abscisses
    n_ticks = len(df_count)
    if n_ticks > 12:
        # Si plus de 12 points, afficher seulement chaque 2ème ou 3ème tick
        step = max(1, n_ticks // 10)
        tick_positions = range(0, n_ticks, step)
        ax.set_xticks(tick_positions)
        ax.set_xticklabels([df_count['Date'].astype(str).iloc[i] for i in tick_positions])
    
    # Rotation et alignement des labels
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    
    # Afficher le plot
    st.pyplot(fig)


##############################
# --- Début de l'algorithme
##############################

# --- Accès information subreddit
subname = st.text_input('Saisir le nom de la communauté')



if subname:
    try:
        # Débute le code si subname existe
        communaute = reddit.subreddit(subname)

        st.title('Information générale du subreddit !')
        show_subreddit_header(communaute)

        # Extraction des posts Reddit
        post_reddit = extract_into_df(communaute)
        st.write('Publication Reddit extraites avec Succès')


        # --- Analyse Statistique ---
        st.header(f'Analyse Statistique de la communauté {communaute}')
        stats_analysis(post_reddit)

        # Top 5 Auteur
        st.header('Top 5 Auteur les plus actifs')
        print_top5(post_reddit)

        # Description Score / Commentaire
        st.header('Description du score et du nombre de commentaire')
        describe_score_comments(post_reddit)

        # Rythme de publication dans le temps
        st.header('Rythme de publication de la communauté')
        rythme_publication(post_reddit)


    except Exception as e:
         st.error("Erreur lors de la récupération des informations du subreddit. Veuillez vérifier le nom ou réessayer plus tard.")