# --- Analyse Textuelle Reddit ---


# --- Import des modules nécessaire ---

import pandas as pd
import gensim
import gensim.corpora as corpora
import spacy
import nltk
from nltk.corpus import stopwords
import re
from datetime import datetime

from langdetect import detect 

import pyLDAvis
import pyLDAvis.gensim_models

import streamlit as st
import praw

import matplotlib.pyplot as plt
import seaborn as sns





# --- Accès code d'accès API
from dotenv import load_dotenv ## Accès au fichier .env
import os
# Chemin vers le fichier .env dans le dossier principal
from pathlib import Path
dotenv_path = Path(__file__).resolve().parent.parent / ".env"

# Charger les variables d'environnement
load_dotenv(dotenv_path=dotenv_path)





st.title('Analyse textuelle Reddit')
st.write(''' 
         Désigner le subreddit de votre choix afin d'obtenir une liste de thèmes abordés par les membres
         de la communauté. Il vous suffit juste d'insérer le noms de la communauté, le programme s'occupera
         de l'extraction et de l'analyse des publications. ''')


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


# Choix du corpus à analyser
def choix_corpus():
    list_corpus = ['Titre', 'Contenu de Publication']
    choix_corpus = st.radio('Veuillez choisir les corpus que vous souhaitez analyser', list_corpus )
    st.write(f'Vous avez choisis: {choix_corpus}')

""
# --- Extraction des publications Reddit ---
def extract_post(communaute, choix_corpus):

    subreddit = reddit.subreddit(communaute)

    corpus = choix_corpus

    sub_posts = subreddit.top(limit = 10)

    # Création d'un dictionnaire pour stocker les publications
    post_dict = {'Post_ID' : [], 'Texte' : []}

    if corpus == 'Titre':
        for post in sub_posts:
            post_dict['Post_ID'].append(post.id if post.id else "")
            post_dict['Texte'].append(post.title if post.title else "")

           
    else:
        for post in sub_posts:
            post_dict['Post_ID'].append(post.id if post.id else "")
            post_dict['Texte'].append(post.selftext if post.selftext else "")

    df_post = pd.DataFrame(post_dict)

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


st.divider()

##################################
#   Construction de l'analyse    #
##################################

st.header('A vous de le tester !')

# --- Choix objet d'analyse ---

choix_extract = st.radio("Veuillez choisir le type d'extraction souhaitez !",
                         ['Publication Subreddit', 'Commentaire', 'Query'])


# Initialisation variable publication

st.write(f'Vous avez choisis: {choix_extract}')
st.divider()


if choix_extract == 'Publication Subreddit':
    ## Sélection du type de corpus souhaiter    
    choix_corpus = st.radio('Veuillez choisir les textes à analyser !', ['Titre', 'Contenu de publication'])

    st.write(f"Vous avez choisi d'analyser les {choix_corpus}")

    st.divider()

     # Extraction des publications de subreddit
    communaute = st.text_input('Veullez écrire le noms du subreddit sans le "r/" !')
    st.divider()

    # Ajout du bouton de validation
    if st.button('Validez'):

        if communaute:

            st.success('Analyse en cours')
            st.subheader(communaute)
            # Retourne des informations sur la communauté
            display_info(communaute)
            try:
                df_post = extract_post(communaute, choix_corpus)

            except Exception as e:
                st.error("Erreur lors de la récupération des informations du subreddit. Veuillez vérifier le nom ou réessayer plus tard.")

        
    else:
        st.write('Veuillez cliquer sur le bouton pour valider !')



st.divider() 
#########################
#    Analyse du texte   #
#########################

# Variable texte à analyser
# Détection de la langue basée sur une concaténation des textes
# Variable texte à analyser
# Détection de la langue basée sur une concaténation des textes
if not df_post.empty:
    # Concaténer tous les textes pour détecter la langue principale
    concatenated_text = " ".join(df_post['Texte'].dropna().astype(str))
    lang = detect(concatenated_text)

    # Charger les stopwords et le modèle Spacy correspondant
    if lang == 'fr':
        stop_words = stopwords.words('french')
        nlp = spacy.load('fr_core_news_sm')  # Assurez-vous que ce modèle est installé
    else:
        stop_words = stopwords.words('english')
        nlp = spacy.load('en_core_web_sm')  # Assurez-vous que ce modèle est installé

    # Fonction de preprocessing
    def preprocess_text(text):
        text = re.sub(r'\s+', ' ', text)  # Supprime les espaces multiples
        text = re.sub(r'\S*@\S*\s?', '', text)  # Supprime les emails
        text = re.sub(r"'", '', text)  # Supprime les apostrophes
        text = re.sub(r'[^\w\sÀ-ÿ]', ' ', text)  # Garde les caractères alphabétiques (incl. accents)
        text = text.lower()  # Convertit en minuscule
        return text.strip()

    # Appliquer le preprocessing
    df_post['cleaned_text'] = df_post['Texte'].apply(preprocess_text)  # Correction de la colonne utilisée

    # Tokenization et retrait des stopwords
    def tokenize(text):
        tokens = gensim.utils.simple_preprocess(text, deacc=True)
        tokens = [token for token in tokens if token not in stop_words]
        return tokens

    df_post['tokens'] = df_post['cleaned_text'].apply(tokenize)

    # Lemmatization des tokens
    def lemmatize(tokens):
        doc = nlp(" ".join(tokens))
        return [token.lemma_ for token in doc]

    df_post['lemmas'] = df_post['tokens'].apply(lemmatize)

    # Création dictionnaire et corpus
    id2word = corpora.Dictionary(df_post['lemmas'])
    texts = df_post['lemmas']
    corpus = [id2word.doc2bow(text) for text in texts]

    # Paramètres ajustables dans Streamlit
    num_topics = st.slider("Nombre de thèmes à identifier :", min_value=2, max_value=10, value=3)
    passes = st.slider("Nombre de passes pour LDA :", min_value=1, max_value=20, value=10)
    chunksize = st.slider("Taille des chunks pour LDA :", min_value=50, max_value=200, value=100)

    # Fonction pour afficher les top mots-clés par sujet
    def plot_top_keywords(lda_model, num_words=10):
        topics = []
        for topic_id, topic_words in lda_model.show_topics(num_topics=-1, num_words=num_words, formatted=False):
            words = ", ".join([word for word, _ in topic_words])
            topics.append([f"Topic {topic_id}", words])
    
        df_topics = pd.DataFrame(topics, columns=["Topic", "Keywords"])
        return df_topics

    # Initialisation de la session d'état pour `lda_model`
    if 'lda_model' not in st.session_state:
        st.session_state.lda_model = None

    # Si le modèle LDA n'est pas encore créé, créer un modèle
    if st.button('Créer le modèle LDA') and st.session_state.lda_model is None:
        try:
            st.session_state.lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                                   id2word=id2word,
                                                   num_topics=num_topics,
                                                   random_state=100,
                                                   update_every=1,
                                                   chunksize=chunksize,
                                                   passes=passes,
                                                   alpha='auto',
                                                   per_word_topics=True)
            st.success("Le modèle LDA a été créé avec succès.")
            
            # Affichage des résultats (exemple avec les mots-clés)
            df_topics = plot_top_keywords(st.session_state.lda_model, num_words=10)
            st.write(df_topics)
        except Exception as e:
            st.error(f"Erreur lors de l'entraînement du modèle LDA : {e}")

    # Vérification si le modèle LDA est déjà disponible dans la session
    if st.session_state.lda_model:
        st.write("Le modèle LDA est déjà disponible dans la session.")

        # Visualisation dans Streamlit si le modèle LDA existe
        if st.button("Afficher les mots-clés des sujets"):
            df_topics = plot_top_keywords(st.session_state.lda_model, num_words=10)
            st.write(df_topics)

            # Heatmap pour montrer les scores
            st.subheader("Visualisation des poids des mots par sujet")
            plt.figure(figsize=(10, 6))
            sns.heatmap(pd.DataFrame(st.session_state.lda_model.get_topics()), annot=True, cmap="coolwarm")
            st.pyplot(plt)