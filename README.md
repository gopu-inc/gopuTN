<img width="1024" height="1024" alt="IMG_6950" src="https://github.com/user-attachments/assets/8087e0a0-04c6-438f-ae26-07ef51237db2" />
# gotn 🐨 - Le lient CLI pour gopHub


<p align="center">
  <!-- Version PyPI -->
  <a href="https://pypi.org/project/gotn/"><img alt="PyPI Version" src="https://img.shields.io/pypi/v/gotn.svg">
  </a>
<a href="https://github.com/gopu-inc/gopuTN/actions/workflows/ci.yml">
  <img alt="Build Status" src="https://github.com/gopu-inc/gopuTN/actions/workflows/ci.yml/badge.svg?branch=main">
</a>
<a href="https://codecov.io/gh/gopu-inc/gopuTN">
  <img alt="Coverage" src="https://codecov.io/gh/gopu-inc/gopuTN/branch/main/graph/badge.svg">
</a>
<a href="https://github.com/gopu-inc/gopuTN/blob/main/LICENSE">
  <img alt="License" src="https://img.shields.io/github/license/gopu-inc/gopuTN.svg">
</a>
  
<a href="https://github.com/psf/black">
  <img alt="Code style: black" src="https://img.shields.io/badge/code%20style-black-000000.svg">
</a>
<a href="https://hub.docker.com/r/ceoseshell/gotn">
  <img alt="Docker Version" src="https://img.shields.io/docker/v/ceoseshell/gotn?sort=semver">
</a>
<!-- Docker Version avec logo -->
<a href="https://hub.docker.com/r/ceoseshell/gotn">
  <img alt="Docker Version" src="https://img.shields.io/docker/v/ceoseshell/gotn?sort=semver&logo=docker&logoColor=white">
</a>
<!-- Docker Pulls avec logo -->
<a href="https://hub.docker.com/r/ceoseshell/gotn">
  <img alt="Docker Pulls" src="https://img.shields.io/docker/pulls/ceoseshell/gotn?logo=docker&logoColor=white">
</a>
<!-- Docker Size avec logo -->
<a href="https://hub.docker.com/r/ceoseshell/gotn">
  <img alt="Docker Size" src="https://img.shields.io/docker/image-size/ceoseshell/gotn/latest?logo=docker&logoColor=white">
</a>
<a href="https://hub.docker.com/r/ceoseshell/gotn">
  <img alt="Docker Pulls" src="https://img.shields.io/docker/pulls/ceoseshell/gotn?logo=docker&logoColor=white">
</a>
<a href="https://pypi.org/project/gotn/">
  <img alt="PyPI Downloads" src="https://img.shields.io/pypi/dm/gotn?logo=pypi&logoColor=white">
</a>
<a href="https://ghcr.io/gopu-inc/gotn">
  <img alt="GHCR Downloads" src="https://img.shields.io/badge/dynamic/json?url=https://ghcr.io/v2/gopu-inc/gotn/tags/list&label=GHCR%20Downloads&query=$.tags.length&logo=github&logoColor=white&color=blue">
</a>





<p align="center">
  <i>"Votre terminal, votre hub, votre écosystème. Centralisez, partagez et exécutez vos "gotn" avec une simplicité déconcertante."</i>
</p>

---
![gotn Banner](https://copilot.microsoft.com/th/id/BCO.4641e553-2a04-4ae2-b1ab-b243bb3bd887.png)
## 📋 Sommaire

- [🎯 Introduction : La Vision de gopHub](#-introduction--la-vision-de-gophub)
- [⚡ Fonctionnalités Principales](#-fonctionnalités-principales)
- [🛠️ Installation](#️-installation)
- [🚀 Usage Détaillé avec Exemples](#-usage-détaillé-avec-exemples)
  - [Authentification](#authentification)
  - [Gestion des Gops](#gestion-des-gops)
  - [Interaction et Exécution](#interaction-et-exécution)
  - [Gestion de l'Environnement](#gestion-de-lenvironnement)
  - [Maintenance](#maintenance)
- [📂 Structure du Projet](#-structure-du-projet)
- [🔑 Authentification : Sécurisée et Transparente](#-authentification--sécurisée-et-transparente)
- [🐨 Intégration avec gopHub API et ChromaDB](#-intégration-avec-gophub-api-et-chromadb)
- [🌐 WebSocket Shell : Le Terminal Interactif](#-websocket-shell--le-terminal-interactif)
- [🧪 Tests : Notre Gage de Qualité](#-tests--notre-gage-de-qualité)
- [🐳 Utilisation avec Docker](#-utilisation-avec-docker)
- [📦 Publication sur PyPI](#-publication-sur-pypi)
- [🤝 Contribution : Rejoignez l'Aventure gopuTN](#-contribution--rejoignez-laventure-goputn)
- [📜 Licence](#-licence)
- [✨ Roadmap et Idées Futures](#-roadmap-et-idées-futures)

---

## 🎯 Introduction : La Vision de gopHub

**gotn** (prononcé "go-ten") est bien plus qu'un simple client en ligne de commande. C'est votre porte d'entrée vers l'écosystème **gopHub**, une plateforme centralisée conçue pour héberger, partager et exécuter des scripts, des extraits de code, des notebooks ou des configurations complexes, que nous appelons affectueusement des **"gops"**.

Notre vision est de briser les silos entre les développeurs, les Ops et les data scientists. Fini le temps où les scripts utiles se perdaient dans des dépôts Git oubliés ou des dossiers locaux désorganisés. Avec **gopHub**, chaque "gop" devient une ressource découvrable, versionnée, documentée et exécutable instantanément depuis n'importe quel terminal grâce à `gotn`.

Le branding **gopuTN** 🐨 (un clin d'œil à nos origines et à notre sympathique mascotte) incarne notre engagement envers une communauté open-source collaborative, inclusive et innovante. Nous croyons en la puissance de l'outillage intelligent pour simplifier les workflows complexes et permettre à chacun de se concentrer sur ce qui compte vraiment : créer de la valeur. `gotn` est l'incarnation de cette philosophie, offrant une expérience utilisateur fluide et puissante directement depuis l'endroit que les développeurs aiment le plus : le terminal.

## ⚡ Fonctionnalités Principales

`gotn` est une véritable boîte à outils pour interagir avec l'écosystème gopHub.

| Commande        | Description                                                                                                   |
|-----------------|---------------------------------------------------------------------------------------------------------------|
| `login`         | S'authentifier auprès de gopHub et sauvegarder le token d'accès.                                               |
| `register`      | Créer un nouveau compte sur la plateforme gopHub.                                                             |
| `list`          | Lister les "gops" disponibles (les vôtres ou ceux de la communauté).                                          |
| `search`        | Rechercher des "gops" par nom, tags, ou via une recherche sémantique avancée.                                   |
| `readme`        | Afficher le README d'un "gop" directement dans le terminal, formaté en Markdown.                               |
| `stats`         | Consulter les statistiques d'utilisation d'un "gop" (nombre d'exécutions, etc.).                                |
| `assoc`         | Associer un répertoire local à un "gop" existant sur gopHub.                                                    |
| `send`          | Envoyer (créer ou mettre à jour) un "gop" depuis un répertoire local vers gopHub.                               |
| `init`          | Initialiser une nouvelle structure de "gop" dans un répertoire local.                                          |
| `exec`          | Exécuter un "gop" distant avec des paramètres spécifiques, sans le télécharger localement.                      |
| `env`           | Gérer les variables d'environnement secrètes pour un "gop".                                                   |
| `shell`         | Démarrer une session shell interactive et sécurisée avec un "gop" via WebSocket.                              |
| `update`        | Mettre à jour `gotn` vers la dernière version disponible sur PyPI.                                            |
| `delete`        | Supprimer un "gop" de la plateforme gopHub (nécessite les droits).                                             |
| `pull`          | Télécharger la dernière version d'un "gop" dans un répertoire local.                                          |
| `const`         | Définir des constantes (variables non secrètes) pour un "gop".                                                |
| `let`           | (Alias pour `const`) Définir des constantes pour un "gop".                                                    |

## 🛠️ Installation

Vous avez plusieurs moyens d'installer `gotn` pour qu'il s'intègre parfaitement à votre workflow.

### 1. Via `pip` (Recommandé)

Le moyen le plus simple et le plus rapide est d'utiliser `pip`, le gestionnaire de paquets Python.

```bash
pip install gotn
```

### 2. Via Docker

Pour une installation isolée et portable, vous pouvez utiliser notre image Docker officielle disponible sur Docker Hub.

```bash
# Pull de l'image
docker pull goputn/gotn:latest

# Exécuter une commande
docker run --rm -it -v ~/.gotnrc:/root/.gotnrc goputn/gotn:latest list --mine
```
*Note : Le montage du volume `~/.gotnrc` est crucial pour conserver votre authentification entre les exécutions.*

### 3. Depuis la Source

Pour les développeurs souhaitant contribuer ou utiliser la version de développement :

```bash
# 1. Clonez le dépôt
git clone https://github.com/gopuTN/gotn.git
cd gotn

# 2. Créez un environnement virtuel (recommandé)
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate

# 3. Installez en mode éditable
pip install -e .
```

---

## 🚀 Usage Détaillé avec Exemples

Voici comment utiliser `gotn` au quotidien.

### Authentification

Commencez par vous connecter à votre compte gopHub.

**`register`**: Crée un nouveau compte.
```bash
gotn register nouveau-dev nouveau.dev@email.com"m
# Vous serez invité à entrer un mot de passe de manière sécurisée.
```

**`login`**: Connecte votre CLI à gopHub.
```bash
gotn login mail mot_de_passe
# Saisissez votre nom d'utilisateur et votre mot de passe.
# Un token JWT sera généré et stocké dans ~/.gotnrc
```

### Gestion des Gops

Créez, trouvez et partagez vos "gops".

**`init`**: Initialise un nouveau projet "gop" localement.
```bash
mkdir my-awesome-gop && cd my-awesome-gop
gotn init my-awesome-gop 1.2.0 app.py app.gopuTN README.md --description Un gop qui fait des choses incroyables. --tags manger meij
# Crée une structure de base : gotn.json, README.md, src/
```

**`send`**: Publie ou met à jour votre "gop" sur la plateforme.
```bash
# Depuis le répertoire de votre gop
gotn send --tags Première version, ajout de la logique principale.
```

**`list`**: Affiche les "gops" disponibles.
```bash
# Lister vos propres gops
gotn list --mine

# Lister les 10 gops les plus populaires
gotn list --sort popularity --limit 10
```

**`search`**: Trouve des "gops" spécifiques.
```bash
# Recherche par mots-clés dans les noms et descriptions
gotn search "analyse de logs"

# Recherche sémantique pour trouver des concepts similaires
gotn search --semantic "script pour visualiser des données financières"

# Recherche par tags
gotn search --tags "database,backup,python"
```

**`pull`**: Récupère un "gop" depuis la plateforme.
```bash
gotn pull community/daily-report-generator
# Le gop sera téléchargé dans un nouveau dossier ./daily-report-generator
```

**`delete`**: Supprime un de vos "gops".
```bash
gotn delete my-old-gop --confirm
```

### Interaction et Exécution

Utilisez la puissance des "gops" directement depuis votre terminal.

**`readme`**: Affiche la documentation d'un "gop".```bash
gotn readme community/aws-s3-manager
# Le README s'affichera joliment formaté dans votre terminal.
```

**`stats`**: Consulte les métriques d'un "gop".```bash
gotn stats community/aws-s3-manager
# Affiche le nombre d'exécutions, les contributeurs, la date de dernière mise à jour, etc.
```

**`exec`**: Exécute un "gop" à distance.
```bash
# Exécution simple
gotn exec community/image-resizer --source "input.jpg" --output "output.png" --width 800

# Exécution avec lecture de la sortie standard
gotn exec community/json-formatter < data.json
```

**`shell`**: Ouvre un shell interactif avec le "gop".
```bash
gotn shell community/database-explorer
# >>> Connexion WebSocket établie avec database-explorer...
# >>> Entrez 'help' pour la liste des commandes.
# db-explorer> show tables;
```

### Gestion de l'Environnement

Configurez vos "gops" de manière sécurisée.

**`env`**: Gère les secrets.
```bash
# Ajouter une variable secrète
gotn env set my-prod-db/api-key
# Vous serez invité à saisir la valeur de manière sécurisée.

# Lister les variables d'environnement
gotn env list my-prod-db
```

**`const` / `let`**: Gère les variables non-secrètes.```bash
# Définir une constante
gotn const set my-prod-db/DB_HOST "db.prod.example.com"

# Lister les constantes
gotn const list my-prod-db
```

### Maintenance

**`update`**: Gardez votre client à jour.
```bash
gotn update
# Vérifie la version sur PyPI et se met à jour si nécessaire.
```

---

## 📂 Structure du Projet

Le projet est structuré pour être modulaire et facilement maintenable.

```
gotn/
├── .github/                # Workflows CI/CD pour GitHub Actions
│   └── workflows/
│       ├── ci.yml          # Tests et linting
│       └── publish.yml     # Publication sur PyPI
├── gotn/
│   ├── api/                # Modules pour interagir avec l'API gopHub
│   ├── commands/           # Logique pour chaque sous-commande CLI (login, list, etc.)
│   ├── core/               # Classes principales, gestion de la configuration
│   ├── shell/              # Logique du client WebSocket
│   ├── __main__.py         # Point d'entrée pour le package
│   └── cli.py              # Définition du groupe de commandes avec Click
├── scripts/                # Scripts d'aide (build, release, etc.)
├── tests/
│   ├── cli/                # Tests d'intégration pour les commandes CLI
│   └── unit/               # Tests unitaires pour la logique métier
├── .dockerignore
├── .gitignore
├── Dockerfile              # Définit l'image Docker pour gotn
├── docker-compose.yml      # Pour l'environnement de développement local
├── LICENSE
├── README.md               # Ce fichier !
└── setup.py                # Configuration du package PyPI
```

---

## 🔑 Authentification : Sécurisée et Transparente

La sécurité est notre priorité. `gotn` utilise une authentification basée sur les **JSON Web Tokens (JWT)**.

1.  Lorsque vous exécutez `gotn login`, le client envoie vos identifiants (nom d'utilisateur/mot de passe) de manière sécurisée (via HTTPS) à l'API de gopHub.
2.  Si les identifiants sont valides, le serveur génère un JWT signé qui contient votre identité et des permissions. Ce token a une durée de vie limitée.
3.  Le client `gotn` reçoit ce token et le stocke localement dans le fichier `~/.gotnrc`. Ce fichier est configuré avec des permissions restrictives pour protéger son contenu.
4.  Pour toutes les commandes suivantes nécessitant une authentification (`send`, `exec`, `env`, etc.), `gotn` attache automatiquement le JWT dans l'en-tête `Authorization: Bearer <token>` de la requête HTTP.
5.  Le serveur gopHub valide la signature et l'expiration du token avant d'autoriser l'opération.

Ce mécanisme garantit que vos identifiants ne transitent sur le réseau qu'une seule fois, lors de la connexion initiale.

---

## 🐨 Intégration avec gopHub API et ChromaDB

`gotn` est le client officiel de l'**API REST de gopHub**. Chaque commande correspond à un ou plusieurs points de terminaison de l'API.

L'une des fonctionnalités les plus puissantes de gopHub est sa capacité de recherche sémantique, rendue possible par **ChromaDB**.

-   **Comment ça marche ?**
    1.  Lorsque vous `send` un "gop", le backend de gopHub ne se contente pas de stocker vos fichiers. Il analyse le contenu de votre `README.md`, votre description et vos métadonnées.
    2.  Ce contenu textuel est transformé en vecteurs numériques (embeddings) à l'aide d'un modèle de langage avancé.
    3.  Ces vecteurs sont stockés et indexés dans une base de données vectorielle, **ChromaDB**.
    4.  Lorsque vous lancez une commande `gotn search --semantic "mon besoin"`, votre requête est également transformée en vecteur.
    5.  ChromaDB effectue alors une recherche de similarité cosinus pour trouver les "gops" dont les vecteurs sont les plus proches de celui de votre requête, vous retournant ainsi les résultats les plus pertinents, même si les mots-clés ne correspondent pas exactement.

---

## 🌐 WebSocket Shell : Le Terminal Interactif

La commande `gotn shell <gop-name>` offre une expérience unique : une session interactive en temps réel avec un "gop" hébergé sur nos serveurs.

-   **Technologie sous-jacente** : Cette fonctionnalité repose sur les **WebSockets**, un protocole de communication qui permet une connexion bidirectionnelle et persistante entre le client (`gotn`) et le serveur (l'environnement d'exécution du "gop").
-   **Cas d'usage** : C'est idéal pour les "gops" conçus comme des outils interactifs : clients de bases de données, explorateurs d'API, outils de débogage, etc. Vous pouvez envoyer des commandes, recevoir des réponses instantanées et maintenir un état tout au long de la session, le tout sans latence perceptible.

---

## 🧪 Tests : Notre Gage de Qualité

Nous nous engageons à fournir un outil fiable et robuste. Pour ce faire, nous avons une suite de tests complète.

**Pour exécuter les tests :**

1.  Assurez-vous d'avoir installé le projet depuis la source avec les dépendances de développement :
    ```bash
    pip install -e ".[dev]"
    ```
2.  Lancez la suite de tests avec `pytest`:
    ```bash
    # Exécuter tous les tests (unitaires et CLI)
    pytest

    # Exécuter uniquement les tests unitaires
    pytest tests/unit

    # Exécuter les tests avec le rapport de couverture
    pytest --cov=gotn
    ```

---

## 🐳 Utilisation avec Docker

Le `Dockerfile` est conçu pour créer une image légère et optimisée de `gotn`. Le `docker-compose.yml` est parfait pour un environnement de développement local, permettant de simuler l'écosystème complet (par exemple, en liant `gotn` à une instance locale de l'API gopHub).

**Construire l'image localement :**
```bash
docker build -t gotn-local .
```

**Lancer une commande avec l'image locale :**
```bash
docker run --rm -it gotn-local --version
```

---

## 📦 Publication sur PyPI

Le processus de publication est automatisé via un workflow GitHub Actions (`.github/workflows/publish.yml`).

1.  Un mainteneur crée une nouvelle "release" sur GitHub avec un tag (ex: `v1.2.3`).
2.  L'action se déclenche, installe les dépendances, construit le package (`sdist` et `wheel`).
3.  Elle utilise `twine` pour uploader le package sur PyPI en utilisant un token d'API stocké dans les secrets du dépôt.

Ce processus garantit des publications fiables et sécurisées.

---

## 🤝 Contribution : Rejoignez l'Aventure gopuTN

Nous sommes ravis de l'intérêt que vous portez à `gotn` ! Les contributions sont le cœur de l'open-source.

1.  **Forkez le dépôt** sur GitHub.
2.  **Créez une branche** pour votre fonctionnalité (`git checkout -b feature/nom-feature`).
3.  **Codez !** Assurez-vous de suivre le style de code (nous utilisons `black` et `flake8`).
4.  **Ajoutez des tests** pour vos nouvelles fonctionnalités. C'est non négociable.
5.  **Assurez-vous que tous les tests passent** (`pytest`).
6.  **Ouvrez une Pull Request** vers notre branche `main`.
7.  **Décrivez clairement** vos changements dans la PR.

N'hésitez pas à ouvrir une "issue" pour discuter d'un bug ou d'une nouvelle idée avant de commencer à travailler.

---

## 📜 Licence

Ce projet est sous licence MIT. Pour plus de détails, consultez le fichier [LICENSE](LICENSE).

---

## ✨ Roadmap et Idées Futures

Nous avons de grandes ambitions pour `gotn` et l'écosystème gopHub !

-   **[ ] Intégration d'un TUI (Text User Interface)** : Une interface plus riche dans le terminal pour naviguer et gérer les "gops" (avec des bibliothèques comme `rich` ou `textual`).
-   **[ ] Système de Plugins** : Permettre à la communauté de développer des extensions pour `gotn` (nouveaux types d'authentification, formats de sortie, etc.).
-   **[ ] Gestion des Équipes et Organisations** : Introduire des permissions granulaires pour les "gops" au sein d'une organisation.
-   **[ ] Marché Privé de "gops"** : Permettre aux entreprises d'héberger leur propre instance de gopHub pour leurs "gops" internes.
-   **[ ] Amélioration des `stats`** : Fournir des graphiques et des analyses plus poussées sur l'utilisation des "gops".
-   **[ ] Support du Versioning Sémantique** : Permettre d'exécuter ou de télécharger une version spécifique d'un "gop" (ex: `gotn exec mon-gop@1.2.3`).

---
<p align="center">
  Fait avec ❤️ par la communauté gopuTN 🐨
</p>
```
