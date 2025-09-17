# GAMA - Analyse de l'activité et des publications d'une communauté

**GAMA** est un projet permettant d'analyser l'activité d'une communauté Reddit, aussi appelé Subreddit. Le projet permet de réaliser deux types d'analyses (une analyse statistique et une analyses thématique) à partir de donnée axtraite à l'aide du module **Praw** qui donne à accès à l'API de Reddit.

# Fonctionnement des analyses

## Analyse statistique
  Le programme extrait l'ensemble des publications d'un subreddit, ainsi qu'une partie de leurs informations: 
  - Auteur
  - Date de publications
  - Score

  Suite à cela, l'algorithme renvoie une série d'analyse statistique permettant de rendre de l'activité de l'application:
  - Nom et description du Subreddit
  - Nombre d'abonnée et de score
  - Liste des 5 auteurs les plus actifs
  - Analyse descriptive des publications (nombre de commentaire et score)
  - Graphe du nombre de poste publié par mois

## Analyse thématique

L'algortithme extrait les 1500 posts les plus populaire (limite en lien au restriction API) après avoir insérer le nom du subreddit choisis. Suite à l'extraction, l'algortihme vous demande les métriques que vous souhaitez utiliser pour l'analyse **LDA** qui se décrit comme *une technique de modélisation thématique permettant de découvrir les sujets centraux et leurs distributions dans un ensemble de documents* [voir plus](https://www.ibm.com/fr-fr/think/topics/latent-dirichlet-allocation).

A la fin de l'analyse l'algorithme affiche une visualisation interactive donnant accès aux différents thèmes abordés et mots clés associé, une analyse des sujets, la distributions des termes au sein des différents sujets et un descriptif des métrique du modèle.


