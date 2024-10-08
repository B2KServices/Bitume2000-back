# Bitume 2000 API

<img src="doc/assets/b2k_logo.svg" width="150" alt="logo">

GeneePortail-back est un projet de backend développé avec [Python](https://www.python.org/)
et [Flask](https://flask.palletsprojects.com/en/2.3.x/).

## Gestion de version Git

- Respect du [Git Flow](https://www.atlassian.com/fr/git/tutorials/comparing-workflows/gitflow-workflow) :
    - Une branche "develop" commune aux développements en cours
        - Chaque branche de dev part de la branche "develop"
    - Une branche "main" de production

- Déploiement des versions de développement et de production :
    - Chaque merge request finalisée sur la branche `develop` redéploie automatiquement le projet dans l'environnement
      de test avec la version 0.0.0.
    - Chaque nouveau tag créé sur master sur gitlab redéploie automatiquement le projet dans l'environnement de
      production, avec comme version le nouveau tag.

- Gestion des commits
    - Commits "utiles" uniquement (pas de succession de commits "Fix TU")
    - Messages de commit en français

## Style

- Suivi des règles du PEP8
    - La longueur des lignes a été augmenté à 140 caractères pour encourager les noms de méthode explicites
- Le code est inspecté par [ruff](https://github.com/astral-sh/ruff) avant chaque commit par le pre-commit pour garantir
  le respect des règles de style

### pre-commit

Pre-commit nous permet de vérifier que le code est bien formaté à chaque commit, et qu'il passera notamment la CI de
formattage. <br>
Sa configuration est faite dans le fichier `.pre-commit.yaml`
Il est nécessaire de l'installer, une premiere fois, pour le projet.

D'abord, installez le package python en local

`pip install pre-commit`

Ensuite,

```bash
pre-commit install
```

Afin de vous assurer que vous passez bien le pre-commit, vous pouvez executer la commande suivante :

```bash
pre-commit run --all-files
```

### Règles plus précises

- Ce qui est en lien avec le métier en français, le reste en anglais
- Attention à l'abus de commentaires : Python est très expressif et un bon code avec de
  méthodes explicites se comprend de lui même la plupart du temps
- Attention a ne pas dupliquer du code, pensez à réutiliser ou factoriser
    - Make it Work, Make it Right, Make it Fast
- Prendre le temps de tout nommer correctement
- Pas de `except` global ou de `except Exception`
- Pas de fonction trop longue (~30 Lignes)
- Pas de fichier trop long (~300 Lignes)
- Pour les chaînes de caractères comportant des variables : utiliser les fstring plutôt que % ou format :

```python
exemple = f'le texte avec {une_variable} en utilisant les f-string'
```

- Les chaînes en dur doivent être extraites dans des constantes si elles sont réutilisées
- Les noms de variables doivent être pertinents et explicites
- Attention au code mort !

## Process de dev

- Pour les chantiers moyens à gros, réalisation d'un DCT avant de débuter les développements
- Lorsqu'un choix technique doit être réalisé (ex.: choix d'une librairie plutôt qu'une autre), écriture d'un
  ADR (Architecture Decision Record)
- La fonctionnalité doit être testée en local par le développeur
- Si la méthode d'installation et/ou d'exploitation est modifiée suite à un chantier, rédiger
  une nouvelle version des manuels adéquats

## Configuration du projet Python (`pyproject.toml`)

Ce fichier est la pierre angulaire de la configuration de votre package Python.

### Section projet

```toml
[project]
name = "package_name"
version = "0.1.0"
description = "DESCRIPTION"
requires-python = ">=3.12"
authors = [
    { name = "AUTHOR", email = "author@example.com" }
]
maintainers = [
    { name = "AUTHOR", email = "author@example.com" },
]
dependencies = [
    "flask",
    # ajouter les dépendances nécessaires
]
classifiers = [
    "Programming Language :: Python :: 3.12",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
]
[project.optional-dependencies]
production = [
    'uwsgi'
]
```

### Configuration de setuptools

```toml
[tool.setuptools]
py-modules = []
```

### Outils et linting avec Ruff

```toml
[tool.ruff]
line-length = 140

[tool.ruff.lint]
extend-select = [
    "UP",
    "E501",
    "I",
    "B",
    "F",
    "E",
    "N",
    "A",
    "PL"
]

[tool.ruff.lint.pydocstyle]
convention = "numpy"

[tool.ruff.format]
quote-style = "single"
indent-style = "space"
docstring-code-format = true
```

Cette documentation reflète la configuration actuelle de votre fichier `pyproject.toml`, en se concentrant sur les
aspects spécifiques de votre projet tels que la gestion des paquets, la compatibilité Python, et l'intégration d'outils
de linting et de formatage. Assurez-vous d'ajuster les champs `name`, `version`, `authors`, `description`, etc., selon
les besoins spécifiques de votre projet.

## Description des ci-gitlab

### CI/CD: GITLAB

- ``pytest`` : Lance les tests unitaires, normalement définis dans le dossier ``tests``.
- ``replace_name_python``: Remplace les noms par défauts des quickstarts par les bons noms (ex : ``quickstart-backend``
  devient ``mon_projet-backend``).
- ``delete_pipelines`` : Supprime les pipelines intermédiaires pour ne laisser que les deux dernières.
- ``ruff_guardian`` : Vérifie que le code est bien formaté.
- ``pages`` : Génère et publie la documentation sur GitLab Pages.
- ``cleanup`` : Supprime les builds des dockers effectués dans les précédents jobs.
- ``trivy`` : Scan toutes les librairies utilisées pour connaitre leurs vulnérabilités.
- ``harbor | external_harbor``: Déploie les dockers sur harbor. Le job ``harbor`` est éxécuté si c'est un déploiement *
  *On Premise** et le job ``external_harbor`` est éxécuté si c'est un déploiement **On Cloud**.

## Création d'une release

### Manuellement

Dans votre virtualenv Python,

Installez l'utilitaire bump-my-version

```shell
pip install --upgrade bump-my-version
```

L'utilitaire bump-my-version permet de versionner le projet de manière efficace en intégrant la possibilité de rajouter
un pre-release.

Pour avoir un aperçu des changements de version disponibles pour le projet, faites la commande suivante :

```shell
bump-my-version show-bump
```

Exemple, pour un projet dont la version actuelle est 0.1.0 :

```bash
bump-my-version show-bump
```

```
0.1.0 ── bump ─┬─ major ─ 1.0.0
               ├─ minor ─ 0.2.0
               ├─ patch ─ 0.1.1
               ├─ pre_l ─ 0.1.0-rc0
               ╰─ pre_n ─ 0.1.0-dev1
```

Ceci indique que si vous changez de version majeure, le projet passe en 1.0.0, ou si vous changez de version mineure,
le projet passe en 0.2.0, etc.

Pour upgrade la version de votre projet en fonction du mot clé associé, faites à la racine de votre projet :

```bash
bump-my-version bump <major|minor|patch|pre_l|pre_n>
```

Par exemple :

```bash
bump-my-version bump minor
```

### Dans le pipeline Gitlab

Afin de créer un release, créez un nouveau tag sur la branche master avec pour titre la nouvelle version. </br>
La CI Gitlab va ensuite automatiquement build le package et le redéployer sur le Nexus.

> **NOTE :** les tags doivent suivre le format de versioning de python ``X.Y.Z`` (ex: ``1.2.3``) <br>
> X pour la version majeure, Y pour la version mineure et Z pour la version patch

## Gestion des dépendances

Pour ajouter une dépendance au projet, modifiez le fichier `pyproject.toml` :

- Si la dépendance est nécessaire au fonctionnement nominal de l'application, ajoutez-la dans la
  section `[project] > dependencies`.
- Si la dépendance est nécessaire uniquement pour la version de production, ajoutez-la dans la
  section `[project.optional-dependencies] > production`.

Les Dockerfiles se chargent de l'installation des dépendances en fonction de l'environnement (développement ou
production), simplifiant ainsi le processus de gestion des dépendances.
Les dockers se chargent aussi d'ajouter les dépendances venant des nexus interne et externe.
Si vous voulez les ajouters en local il est conseillé d'ajouter la configuration suivante
dans `~/.config/pip/pip.conf` :

```ini
[global]
index = https://pypi.org/simple
index-url = https://pypi.org/simple
extra-index-url = https://nexus.fastit.dev/repository/fast-it/simple
                  https://nexus.ifpen.fr/repository/fast-it/simple
retries = 1
```

---

## Workflow des controllers

### Création

Pour rappel, on désigne par 'controller' une collection de routes d'API pour une ressource donnée (e.g. les CRUD d'une
entité, des fonctionnalités qui appartiennent au même groupe logique).\
Pour une ressource ou groupe de ressources [R], la localisation du/des controller dans la base de code
est `data/[R]/controllers/[classname]_controller.py`.

- Créez un `flask.Blueprint`, c'est cet objet qui représente les controllers dans Flask
- Ensuite, vous pouvez définir une route comme ceci :

```python
from flask_apispec import doc
from setup import docs
from flask import Blueprint

NAME = 'abc'
abc_blueprint = Blueprint(f"{NAME}_blueprint", __name__)


@abc_blueprint.get(f"/{NAME}/<uuid:id_abc>")
def get_abc(id_abd):
    ...
    return response, code

```

- **Enregistrez** le blueprint à l'application avec `app.register_blueprint(...)` dans shared/__init__.py

> ** INFO ** : Il est important respecter une règle quand on enregistre un nouveau blueprint dans setup/__init__.py

- (Routes PUT, POST, PATCH) Recupérez le __payload__ de la requete avec `flask.request.get_json()`
- (Recommandé) Validez les données avec un [schema marshamallow](#schemas)
- Conernant la __logique métier__, privilégiez la création d'un [service](#services) pour encapsuler les détails
  d'implémentation
  plutôt que de mettre ce code dans les endpoints de vos controllers

## swagger

pour mettre en place le swagger il vous suffit d'importer le ``SwaggerInterface au debut de votre projet``

```python
from managers.swagger_manager import SwaggerInterface

docs: SwaggerInterface = SwaggerInterface(
    document_options=False,
    title="Quick Start API",
    version="0.0.0",
    openapi_version="3.0.2",
    swagger_ui=True,
    components={"securitySchemes": {"ApiKeyAuth": {"type": "apiKey", "in": "header", "name": "Authorization"}}},
    security_definitions={"ApiKeyAuth": {"type": "apiKey", "name": "Authorization", "in": "header"}},
    security=[{"ApiKeyAuth": []}],
    info={
        "description": "how to use the API with the authorization: \n"
                       "1.	Enter your credentials: Provide your username and password in the authentication route below. \n"
                       "2.	Retrieve the key: Upon successful authentication, you will receive an authentication key. \n"
                       "3.	Authorize: Add the returned key by clicking on the “Authorize” button."
    },
)
```

sans oublier de l'initier a l'application

```python
docs.init_app(app)
```

une fois cela fait vous pouvez ajouter des routes en les enregistrant dans le swagger

```python
docs.register_function(get_abc)
```

et vous pouvez aussi ajouter des informations sur les routes

```python
from flask_apispec import doc
from setup import docs
from flask import Blueprint
from managers.swagger_manager.doc_decorator import swagger

NAME = 'abc'
abc_blueprint = Blueprint(f"{NAME}_blueprint", __name__)


@swagger(
    responses={
        200: {"description": "Success", "content": TestSchema},
        400: {"description": "Bad Request", "content": fields.String()},
    },
    body={"description": "body description", "content": TestSchema}
)
@abc_blueprint.get(f"/{NAME}/<uuid:id_abc>")
def get_abc(id_abd):
    ...
    return response, code


@swagger(
    is_file=True,
    body={"description": "body description", "content": fields.field(type="file")}
)
@abc_blueprint.post(f"/{NAME}/<uuid:id_abc>")
def post_file(id_abd):
    ...
    return response, code
```

> le ``is_file`` est a mettre a ``True`` si vous voulez que le swagger affiche un input de type file

## SQLAlchemy

SQLAlchemy est un ORM (Object-Relational Mapping) qui permet de manipuler des bases de données relationnelles en
utilisant des objets Python.\
Il est utilisé dans le projet pour interagir avec la base de données PostgreSQL.

### Création d'une table avec SQLAlchemy

les tables SQL sont lié aux classes Python, celles si sont définies dans le
dossier `app/data/[resource]/models/[classname]_model.py` et en dev, elles sont automatiquement créées dans la base de
données.

```python
class HelloWorldModel(db.Model):  # db est l'instance de SQLAlchemy initialisée dans setup/__init__.py
    __tablename__ = "hello_world"
    id_hello_world = Column(
        UUID, primary_key=True, unique=True, server_default=sqlalchemy.text("gen_random_uuid()"), nullable=False
    )
    name = Column(String())
```

en cas de mise en production, le projet ne touche pas à la structure de la base de données, il est donc nécessaire de
créer les tables manuellement.

### Ajouter des données dans une table SQLAlchemy :

une fois que le projet est lancé et que les tables sont crées dans la base de données PostgreSQL, il est possible
d'ajouter des données en utilisant la class `SQLAlchemyRegistry`

pour l'initialiser il faut :

```
registry = SQLAlchemyRegistry(HelloWorldModel)
```

une fois initialisé, l'objet est directement lié à la table `HelloWorldModel` et permet d'ajouter des données en
utilisant la méthode `create_one` :

```python
registry.create_one(ObjectData)
```

la récuprer avec la méthode `get_one_or_fail` :

```python
registry.get_one_or_fail(ObjectData)
```

> **NOTE**  avec un schema marshmallow_sqlalchemy expliqué ci-dessous, il est possible de transformer le JSON en objet
> compatible avec la table SQLAlchemy (registry)

## Schemas

Les schemas marshamallow remplissent deux roles simultanément :

- __Serialisation__ / __Deserialisation__ des donnees
- __Validation__ des donnees

### Sérialisation / Déserialisation

__Données Sérialisées__ = Représentation des données reçues et envoyées à l'extérieur (__Dictionnaires Python__)\
NB : C'est Flask qui se charge de transformer les dictionnaires en représentation json, en appliquant `json.dumps()` aux
retours des fonctions d'endpoints

__Données Désérialisées__ = Représentation des données dans le serveur (__Dictionnaires ou Objets Python__)

La sérialisation/déserialisation est utile notamment :

- Lorsque l'on utilise un ORM comme SQLAlchemy, il est souvent possible d'étendre Marshmallow pour pouvoir déserialiser
  directement vers des entités
- Lorsque l'on souhaite découpler le format des données entre la représentation en Base de Données et dans les JSON des
  requêtes API

### Validation

La __validation des données__ consiste à vérifier que lors d'une requête :

- Tous les champs attendus sont présents
- Chaque valeur correspond bien au type attendu pour le champ correspondant
- Les valeurs sont cohérentes et sont valides en fonction de la nature du champ associé (par exemple, le formatage d'une
  adresse mail)

La validation est optionnelle, mais très recommandée, car elle permet :

- De sécuriser ses routes en prévenant des failles potentielles
- De faciliter le développement pour les clients l'API en détectant certaines erreurs de logique

### Vocabulaire

Dans marshmallow '__load__' = __deserialize__ et '__dump__' = __serialize__:

__[payload: JSON]__ ----load--->  __[instance: Object]__\
__[payload: JSON]__ <---dump----  __[instance: Object]__

### Definir un schema

- Un schema __marshmallow__ 'pur'

```python3
class Album:
    title: str
    release_date: datetime.date


class AlbumSchema(Schema):
    title = fields.Str()
    release_date = fields.Date()
```

- Un schema __marshmallow_sqlalchemy__

```python3
class AlbumModel:
    title: Column(String(255))
    release_date: Column(Date())


class AlbumSchema(SQLAlchemySchema):
    class Meta:
        model = AlbumModel
        load_instance = True  # Optional: deserialize to model instances
        include_fk = True  # Optional: To include foreign fields
        include_relationships = True  # Optional: To include relationships (become a fields.Related not fields.Nested)

    title = auto_field()
    release_date = auto_field()


# Ou avec SQLAlchemyAutoSchema

class AlbumSchema(SQLAlchemySchema):
    class Meta:
        model = AlbumModel
        load_instance = True  # Optional: deserialize to model instances
        include_fk = True  # Optional: To include foreign fields
        include_relationships = True  # Optional: To include relationships (become a fields.Related not fields.Nested)
```

Note: SQLAlchemySchema n'inclut pas les `sqlalchemy.relationship()`, juste les `sqlalchemy.Column()`

Regarder aussi:

- [marshmallow.fields.Nested()](https://marshmallow.readthedocs.io/en/stable/nesting.html)
- [read_only et dump_only](https://marshmallow.readthedocs.io/en/stable/quickstart.html#read-only-and-write-only-fields)
- [data_key](https://marshmallow.readthedocs.io/en/stable/quickstart.html#specifying-serialization-deserialization-keys)
  pour changer le nom d'un field du dictionnaire en un autre nom dans l'objet

## Classes utilitaires

### Services

Les services (`app/data/[resource]/service`) sont des classes utilitaires regroupant la logique métier propre a une
ressource\
Leur role est d'encapsuler cette logique, de rendre le comportement des routes API plus lisible et plus facile a
maintenir

### Managers

Les managers (`app/managers`) sont des classes utilitaires associés à un module indépendant de l'application (ex.
authentification)\
Typiquement les managers peuvent aussi provenir de leur propre package python, et sont a priori optionels\
Plus exactement, les managers sont les classes qui exposent la logique de leur module

### Utils

Les utils (`app/utils`) sont un ensemble de classes et fonctions utilitaires, utiles pour tous les projets

## Gestion des erreurs

### Erreurs personnalisées

Il est recommandé de créer une classe d'erreur pour chaque type d'erreur de l'application,
en héritant (directement ou pas) de la même classe mère : `BaseCustomError` située à
`app/errors/base_custom_error.py`.

Par exemple :

```python
class IncorrectEmail(BaseCustomError):
    def __init__(self, email: str):
        message = f"L'email fournit '{email}' n'a pas un format correct."
        super().__init__(message)
```

### Gestionnaires d'erreur ('*error handler*')

Les gestionnaires d'erreur sont des middlewares configurés pour intercepter les
erreurs qui pourraient se produire durant l'exécution de n'importe quel controller,
permettant d'envoyer une réponse avec le message et le code d'erreur.\
NB: Flask met en place un gestionnaire d'erreur par défaut pour toutes les erreurs
non-interceptées, et il retourne alors un code d'erreur 500

Les gestionnaires d'erreur de l'application sont configurés dans `app/setup/app_error_handlers/app_error_handlers.py`

Par exemple :

```python
@app.errorhandler(BaseCustomError)
def handle_custom_error(error):
    self.request_console_logger.error(error)
    return DefaultResponse.error(message=str(error)), 400
```

Ce bout de code permet d'assurer que, sauf règle plus précise, les erreurs de
l'application renvoient par défaut un code d'erreur de 400 avec comme payload
`{status: "error", message: [MESSAGE_D_ERREUR]}`

### Codes d'erreur

Les codes d'erreurs prévus par le quick-start sont les suivants :

- `200`: Succès (code de succès par défaut)
- `201`: Succès de création
- `400`: Erreur (code d'erreur par défaut)
- `401`: Non connecté (n'a pas de token ou token invalide)
- `403`: Non autorisé (n'a pas les permissions necessaires)
- `404`: URL ou ressource non trouvée
- `500`: Erreur imprévue
- `501`: Non implémenté

## Mettre à jour la doc

La doc se met a jour automatiquement avec les CI/CD de gitlab, elle est automatiquement générée avec Sphinx et hébergée
sur les pages Gitlab.
vous pouvez ajouter des documents a la racine et modifier le fichier `index.rst` pour les inclure dans la doc.
> Cependant, il est recommandé de ne pas modifier la ligne `module` dans le fichier `index.rst` car elle permet
> d'acceder a la documentation auto générée des modules


La documentation auto-générée va aller chercher les fonctions du code et les docstrings associées pour les afficher dans
la doc.

pour tester votre documentation en local, il suffit de lancer la commande suivante :

```shell
docker exec -it quick_start sphinx-apidoc -f -o sphinx app 
docker exec -it quick_start sphinx-build -b html ./sphinx ./public  
```