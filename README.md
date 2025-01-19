# GAMA - Analyse des Publications, Commentaires et Activité d'une Communauté Reddit

**GAMA** est un projet permettant d'extraire et d'analyser un ensemble de publications et de commentaires provenant de Reddit. Le projet utilise le module **Praw** pour l'extraction des posts et un modèle **LDA** (Latent Dirichlet Allocation) pour effectuer une analyse thématique des contenus. Une nouvelle fonctionnalité permet également d'analyser l'activité d'une communauté Reddit, en offrant des statistiques détaillées sur les publications et commentaires.

## Fonctionnalités
- Extraction des posts et commentaires à partir de Reddit via **Praw**.
- Prétraitement des textes (nettoyage, suppression des stopwords, lemmatisation).
- Analyse thématique des textes via un modèle **LDA** pour identifier les principaux sujets abordés dans les publications.
- Visualisation des résultats, incluant les mots-clés associés à chaque sujet et une heatmap des scores des mots-clés par sujet.
- Analyse de l'activité d'une communauté Reddit : statistiques sur les publications, la fréquence des commentaires et l'engagement dans le temps.
