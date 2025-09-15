# --- Analyse Textuelle Reddit ---


# --- Import des modules nécessaire ---

import streamlit as st
import praw
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import LatentDirichletAllocation
import pyLDAvis
import pyLDAvis.lda_model
from datetime import datetime
import streamlit.components.v1 as components
import re
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import warnings



warnings.filterwarnings('ignore')




# --- Accès code d'accès API
from dotenv import load_dotenv ## Accès au fichier .env
import os
# Chemin vers le fichier .env dans le dossier principal
from pathlib import Path
dotenv_path = Path(__file__).resolve().parent.parent / ".env"

# Charger les variables d'environnement
load_dotenv(dotenv_path=dotenv_path)



st.set_page_config(page_title = "Analyse thématique")

st.title('Analyse textuelle Reddit')
st.write(''' 
         Désigner le subreddit de votre choix afin d'obtenir une liste de thèmes abordés par les membres
         de la communauté. Il vous suffit juste d'insérer le noms de la communauté, le programme s'occupera
         de l'extraction et de l'analyse des publications. ''')

# --- Initialisation des variables ---
if 'df_post' not in st.session_state:
    st.session_state.df_post = None


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





# --- Extraction des publications Reddit ---
def extract_post(communaute):

    subreddit = reddit.subreddit(communaute)

    sub_posts = subreddit.top(limit = 1500)

    # Création d'un dictionnaire pour stocker les publications
    post_dict = {'Post_ID' : [], 'text' : []}

    for post in sub_posts:
            post_dict['Post_ID'].append(post.id if post.id else "")
            post_dict['text'].append(post.title if post.title else "")
    

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




st.divider()

##################################
#   Construction de l'analyse    #
##################################

st.header('A vous de le tester !')



# Sélection et analyse du subreddit choisis

communaute = st.text_input("Insérez le noms du Subreddit à analyser", value ="")

if communaute and st.button('Validez'):

    st.success('Extraction des publications en cours')
    display_info(communaute)

    try:
        st.session_state.df_post = extract_post(communaute)
        st.success('Extraction des publications en cours')


    except Exception as e:
        st.error('Erreur lors de la récupération des informations du Subreddit. Veuillez vérifier le nom de la communauté ou réessayer plus tard')
        st.session_state.df_post = None

else:
    st.write('Appuyez sur le boutton pour valider !')        


st.divider() 
#########################
#    Analyse du texte   #
#########################


# Fonction de preprocessing

@st.cache_data
def preprocess_text(texts):
    """Préprocessing des textes pour l'analyse LDA"""
    try:
        nltk.download('punkt', quiet=True)
        nltk.download('stopwords', quiet=True)
        nltk.download('wordnet', quiet=True)
    except:
        pass
    
    # Mots vides français et anglais
    stop_words = set(stopwords.words('french') + stopwords.words('english'))
    stop_words.update(['le', 'de', 'un', 'à', 'être', 'et', 'en', 'avoir', 'que', 'pour'])
    
    lemmatizer = WordNetLemmatizer()
    processed_texts = []
    
    for text in texts:
        # Conversion en minuscules
        text = text.lower()
        # Suppression des caractères spéciaux et chiffres
        text = re.sub(r'[^a-zA-Zàâäéèêëïîôöùûüÿç\s]', '', text)
        # Tokenisation
        tokens = word_tokenize(text)
        # Suppression des mots vides et lemmatisation
        tokens = [lemmatizer.lemmatize(token) for token in tokens 
                 if token not in stop_words and len(token) > 2]
        processed_texts.append(' '.join(tokens))
    
    return processed_texts

if st.session_state.df_post is not None and not st.session_state.df_post.empty:
    # Paramètres LDA
    n_topics = st.sidebar.slider("Nombre de sujets", 2, 10, 5)
    max_features = st.sidebar.slider("Nombre maximum de mots", 100, 1000, 500)
    min_df = st.sidebar.slider("Fréquence minimale (min_df)", 1, 5, 2)
    
    # Bouton pour lancer l'analyse
    if st.sidebar.button("🚀 Lancer l'analyse LDA", type="primary"):
        
        with st.spinner("🔄 Préprocessing des textes..."):
            # Préprocessing
            processed_texts = preprocess_text(st.session_state.df_post['text'].tolist())
        
        with st.spinner("🔄 Entraînement du modèle LDA..."):
            # Vectorisation
            vectorizer = CountVectorizer(
                max_features=max_features,
                min_df=min_df,
                max_df=0.8,
                ngram_range=(1, 2)
            )
            
            doc_term_matrix = vectorizer.fit_transform(processed_texts)
            
            # Modèle LDA
            lda_model = LatentDirichletAllocation(
                n_components=n_topics,
                random_state=42,
                max_iter=10,
                learning_method='online'
            )
            
            lda_model.fit(doc_term_matrix)
        
        # Stockage des résultats dans session state
        st.session_state.lda_results = {
            'model': lda_model,
            'vectorizer': vectorizer,
            'doc_term_matrix': doc_term_matrix,
            'processed_texts': processed_texts,
            'original_df': st.session_state.df_post
        }
        
        st.success(" Analyse terminée!")

# Affichage des résultats
if 'lda_results' in st.session_state:
    results = st.session_state.lda_results
    
    # Onglets pour organiser l'affichage
    tab1, tab2, tab3, tab4 = st.tabs([" Visualisation Interactive", " Sujets Détaillés", " Documents par Sujet", " Métriques"])
    
    with tab1:
        st.subheader("Visualisation Interactive pyLDAvis")
        
        with st.spinner(" Génération de la visualisation..."):
            try:
                # Génération de la visualisation pyLDAvis
                vis = pyLDAvis.lda_model.prepare(
                    results['model'], 
                    results['doc_term_matrix'], 
                    results['vectorizer'],
                    mds='tsne'
                )
                
                # Conversion en HTML
                html_string = pyLDAvis.prepared_data_to_html(vis)
                
                # Affichage dans Streamlit
                components.html(html_string, width=1200, height=700, scrolling=True)
                
            except Exception as e:
                st.error(f"Erreur lors de la génération de la visualisation: {e}")
    
    with tab2:
        st.subheader(" Analyse des Sujets")
        
        # Extraction des mots-clés par sujet
        feature_names = results['vectorizer'].get_feature_names_out()
        
        for topic_idx, topic in enumerate(results['model'].components_):
            st.write(f"### Sujet {topic_idx + 1}")
            
            # Top mots pour ce sujet
            top_words_idx = topic.argsort()[-10:][::-1]
            top_words = [feature_names[i] for i in top_words_idx]
            top_weights = [topic[i] for i in top_words_idx]
            
            # Création d'un DataFrame pour l'affichage
            words_df = pd.DataFrame({
                'Mot': top_words,
                'Poids': [f"{w:.3f}" for w in top_weights]
            })
            
            col1, col2 = st.columns([2, 1])
            with col1:
                st.dataframe(words_df, use_container_width=True, hide_index=True)
            with col2:
                st.bar_chart(pd.Series(top_weights, index=top_words))
    
    with tab3:
        st.subheader(" Attribution des Documents aux Sujets")
        
        # Prédiction des sujets pour chaque document
        doc_topic_probs = results['model'].transform(results['doc_term_matrix'])
        
        # Création d'un DataFrame avec les résultats
        results_df = results['original_df'].copy()
        results_df['sujet_principal'] = doc_topic_probs.argmax(axis=1) + 1
        results_df['probabilite_max'] = doc_topic_probs.max(axis=1)
        
        # Ajout des probabilités pour tous les sujets
        for i in range(doc_topic_probs.shape[1]):
            results_df[f'prob_sujet_{i+1}'] = doc_topic_probs[:, i]
        
        st.dataframe(
            results_df[['text', 'sujet_principal', 'probabilite_max']].round(3),
            use_container_width=True,
            hide_index=True
        )
        
        # Distribution des documents par sujet
        st.subheader(" Distribution des Documents par Sujet")
        topic_counts = results_df['sujet_principal'].value_counts().sort_index()
        st.bar_chart(topic_counts)
    
    with tab4:
        st.subheader(" Métriques du Modèle")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Nombre de Sujets", n_topics)
        with col2:
            st.metric("Nombre de Documents", len(results['original_df']))
        with col3:
            st.metric("Vocabulaire", len(results['vectorizer'].get_feature_names_out()))
        
        # Calcul de la perplexité
        perplexity = results['model'].perplexity(results['doc_term_matrix'])
        log_likelihood = results['model'].score(results['doc_term_matrix'])
        
        col4, col5 = st.columns(2)
        with col4:
            st.metric("Perplexité", f"{perplexity:.2f}")
        with col5:
            st.metric("Log-vraisemblance", f"{log_likelihood:.2f}")
