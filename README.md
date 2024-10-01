# STARTER-BACK

<img src="./doc/assets/genee.png" alt="Image 1" width="150px" style="margin: 20px">

Starter-KIT est un projet de backend développé avec [Python](https://www.python.org/)
et [Flask](https://flask.palletsprojects.com/en/2.3.x/).

## Dépendances Principales

- [Flask](https://flask.palletsprojects.com/en/2.3.x/) : Une micro framework pour Python.
- [SQLAlchemy](https://www.sqlalchemy.org/) : Un SQL toolkit et ORM pour Python.
- [Marshmallow](https://marshmallow.readthedocs.io/en/stable/) : Une bibliothèque pour la conversion des types de
  données, la validation et la désérialisation.
- [Docker](https://www.docker.com/) : Une plateforme de conteneurisation.
- [Docker Compose](https://docs.docker.com/compose/) : Un outil pour définir et gérer des applications multi-conteneurs
  avec Docker.

## Structure du Projet

```markdown
.
├── app
│   │ └── Contient toute la logique de l'application
│   ├── data
│   │    │ └── Contient le code de logique de l'application
│   │    └── fonctionalités
│   │         │ └── remplace 'fonctionalités' par le nom de la fonctionalité, chaque fonctionalité est un module de l'application
│   │         ├── controllers
│   │         │   └── Contient les points d'accès API pour le module
│   │         ├── models
│   │         │   └── Contient les modèles de données SQLAlchemy associés au module
│   │         ├── schemas
│   │         │   └── Contient les schémas utilisés pour la validation des données entrantes pour le module
│   │         └── services
│   │             └── Contient les fonctions utilitaires pour le module 
│   ├── errors
│   │   └── Contient les erreurs personnalisées de l'application
│   ├── shared
│   │   └── __init__.py
│   │        └── Logique d'initialisation de l'application, modules partagés (fonctions utilitaires, services)
│   ├── config.py
│   │   └── Contient la configuration des variables d'environnement de l'application
│   └── main.py
│       └──Point d'entrée de l'application, il démarre le projet
├── doc
│   └── Décisions d'architecture (ARDs), guides, accumulation du savoir
├── envs
│   │ └── Environnements Docker de développement et de production
│   ├── dev
│   │   └── Contient les fichiers de configuration pour l'environnement de développement
│   ├── prod
│   │   └── Contient les fichiers de configuration pour l'environnement de production
│   └── shared
│       └── Contient les fichiers de configuration partagés entre les environnements
├── scripts
│   └── Utilitaires de lancement de l'application et liés aux tests
├── pyproject.toml
│   └── Fichier de configuration de python pour le projet (dépendances, outils, ...)
├── README.md
│   └── Fichier de documentation du projet
├── .gitignore
│   └── Fichier de configuration de git pour le projet (fichiers à ignorer)
└── migrations
```

## Installation

### Prérequis

Pour exécuter cette application, vous devez avoir Docker et Docker Compose installés sur votre système.

#### Installation de Docker

##### Sur Linux

1. Mettez à jour l'index du paquet `apt` :
   ```sh
   sudo apt-get update
   ```
2. Installez les paquets permettant à `apt` d'utiliser un dépôt sur HTTPS :
   ```sh
   sudo apt-get install apt-transport-https ca-certificates curl software-properties-common
   ```
3. Ajoutez la clé GPG officielle de Docker :
   ```sh
   curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
   ```
4. Ajoutez le dépôt Docker à vos sources `APT` :
   ```sh
   sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable"
   ```
5. Mettez à jour l'index du paquet `apt` et installez Docker CE :
   ```sh
   sudo apt-get update
   sudo apt-get install docker-ce
   ```

##### Sur Mac

1. Téléchargez Docker Desktop pour Mac
   depuis [Docker Hub](https://hub.docker.com/editions/community/docker-ce-desktop-mac/).
2. Ouvrez le fichier `.dmg` téléchargé et glissez l'icône de Docker dans votre dossier `Applications`.
3. Ouvrez Docker Desktop depuis vos `Applications`.

#### Installation de Docker Compose

##### Sur Linux

1. Téléchargez la version actuelle de Docker Compose :
   ```sh
   sudo curl -L "https://github.com/docker/compose/releases/download/1.29.2/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
   ```
2. Appliquez les permissions d'exécution au binaire :
   ```sh
   sudo chmod +x /usr/local/bin/docker-compose
   ```

##### Sur Mac

Docker Compose est déjà inclus dans Docker Desktop pour Mac, donc aucune étape supplémentaire n'est nécessaire.

### Lancement de l'application

Ouvrez une invite de commande ou un terminal.

Accédez au répertoire "dev" situé dans le répertoire "envs" de l'application. Utilisez la commande suivante pour vous
déplacer vers ce répertoire :

```sh
cd /envs/dev
```

Une fois dans le répertoire "dev", exécutez la commande suivante pour démarrer l'application à l'aide de Docker
Compose :

```sh
docker-compose up
```

Une fois l'application démarrée, vous pouvez accéder à celle-ci en faisant vos requêtes
à `http://localhost:5001/api/endpoint`.

## Variables d'Environnement

Le projet utilise la variable d'environnement suivante :

- `MIGRATIONS` : Cette variable détermine si des migrations doivent être effectuées sur la base de données. Mettez-la
  à `1` pour activer les migrations

et à `0` pour les désactiver.

### Lancement de l'application

Ouvrez une invite de commande ou un terminal.

- lancer les docker

```shell
docker-compose -f envs/dev/docker-compose.yml up 
```

sans oublier le .env prévu pour ``envs/dev/back/.env``

# Configuration de Pycharm

Pycharm est l'IDE Python de jetbrains, pour avoir acces au programme par l'IDE sans erreurs demande quelques
modification

> **NOTE**: cette configuration a été faites avec la nouvelle UI de Pycharm elle peut ne pas fonctionner sur l'ancienne

### Selection de l'interpreteur python du service docker (permet d'avoir la complétion sans avoir à installer les dépendences sur l'hôte)

- Cliquer sur le bouton de l'interpréteur en bas a droite (là où il y a probablement écrit ``Python 3.X`` avec la
  version de python installée sur l'hôte)
- ``Add New Interpreter``, puis choisir ``On Docker Compose...``
- Dans le champ ``Configuration files`` sélectionner le fichier suivant: ``envs/dev/docker-compose.yml``
- Dans le champ ``Service``, choisir le nom du service qui contient flask, i.e. ``flask`` (le champ devrait avoir des
  valeurs disponibles apres avoir fini l'étape précédente)
- Appuyer sur ``Next``, attendre la fin de commande lancée par l'IDE puis ``Next``
- Appuyer sur ``Create`` dans la dernière fenêtre
- Si en bas a gauche il y a ecrit ``Remote Python 3.X Docker Compose (flask)``, vous avez tout pour commencer !

### Mise en place de la visualisation de la base de donnée

Cliquez sur le logo qui ressemble a une pile de disque sur le coté droit.\
Si vous ne le voyez pas, assurez vous que le plugin ``Database tools and SQL`` soit bien installé.\
Une fois le menu ouvert, cliquez sur ``+ > Data Source > PostgreSQL``\
Mettez les informations suivantes :

- ``port: 5432``
- ``host: localhost``
- ``connect with user and password``
    - user: ``postgres``
    - password: ``postgres``

> **NOTE**: assurez vous bien pendant la connexion avec le docker postgres que le docker soit lancé

Une fois connecté vous verrez a droite ``postgres@localhost`` et plus a droite un petit bouton avec écrit quelque choise
du genre ``1 of 4`` ou bien ``4``, cliquez dessus.\
Cochez ``db_dev`` et ``All schemas`` dans le menu déroulant de ``db_dev``\
Vous pouvez maintenant accéder à toutes vos table dans ``postgres@localhost > db_dev > public > tables``

# Explication des scripts

- ``tester.sh`` permet de tester l'applicatopm
    - les arguments :
        - -d permet de définir si les dockers sont dépendant du programme,
          si utilisé les dockers se lanceront par le testers et vous n'aurez que le retour du tester en lui meme
        - sinon doit etre rattaché au docker-compose deja lancé
- ``application_restart.sh`` permet quand les dockers sont lancés, a l'interruption de ceux-ci par le billet du
  raccourcis ctrl-c ce relance tout seul en nettoyant la base de donnée

# Mise en place du format par lint

``black`` permet de formatter le code. Pour le relier à la fonction ``format code`` de l'IDE:

- S'assurer que Black est bien installé : ``python3 -m pip install Black``
- Aller dans ``Settings... > Tools > Black`` et activer ``on code reformat``