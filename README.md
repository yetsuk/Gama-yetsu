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


# Installation

## Prérequis

- Python 3.7 ou plus récent
- Un compte Reddit
- Git (optionnel)

## Installation

### 1. Cloner le dépôt

```bash
git clone https://github.com/yetsuk/Gama-yetsu.git
cd Gama-yetsu
```

### 2. Créer un environnement virtuel (recommandé)

<details>
<summary><strong>🔧 Avec environnement virtuel (recommandé)</strong></summary>

```bash
python -m venv reddit_env
source reddit_env/bin/activate  # Sur Linux/Mac
# ou
reddit_env\Scripts\activate     # Sur Windows
```

**Avantages :** Isolation des dépendances, évite les conflits entre projets
</details>

<details>
<summary><strong>⚡ Sans environnement virtuel (plus simple)</strong></summary>

Vous pouvez passer directement à l'étape suivante si vous préférez installer les dépendances globalement.

**Note :** Cette approche peut créer des conflits si vous travaillez sur plusieurs projets Python.
</details>

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

## Configuration

### 1. Créer une application Reddit

1. Connectez-vous sur [Reddit](https://www.reddit.com)
2. Allez sur https://www.reddit.com/prefs/apps
3. Cliquez sur "Create App" ou "Create Another App"
4. Remplissez le formulaire :
   - **Nom** : Nom de votre application
   - **Type** : Sélectionnez "script"
   - **Description** : Description de votre application (optionnel)
   - **About URL** : Laissez vide ou ajoutez une URL (optionnel)
   - **Redirect URI** : Entrez `http://localhost:8080`
5. Cliquez sur "Create app"

### 2. Récupérer les identifiants

Après la création, notez :
- **Client ID** : sous le nom de votre app (chaîne de 14 caractères)
- **Client Secret** : le "secret" affiché

### 3. Créer le fichier .env

Créez un fichier `.env` à la racine du projet et ajoutez vos identifiants :

```env
REDDIT_CLIENT_ID=votre_client_id_ici
REDDIT_CLIENT_SECRET=votre_client_secret_ici
REDDIT_USERNAME=votre_nom_utilisateur_reddit
REDDIT_PASSWORD=votre_mot_de_passe_reddit
REDDIT_USER_AGENT=VotreApp/1.0 by votre_nom_utilisateur
```

> ⚠️ **Important** : Ne jamais commiter le fichier `.env` dans votre dépôt Git. Assurez-vous qu'il est dans votre `.gitignore`.

### 4. Configurer .gitignore

Ajoutez ces lignes à votre fichier `.gitignore` :

```gitignore
.env
__pycache__/
*.pyc
reddit_env/
.venv/
```

  
## Ressources utiles

- [Documentation PRAW](https://praw.readthedocs.io/)
- [API Reddit](https://www.reddit.com/dev/api/)
- [Règles de l'API Reddit](https://github.com/reddit-archive/reddit/wiki/API)

---

⭐ Si ce projet vous aide, n'hésitez pas à lui donner une étoile !

