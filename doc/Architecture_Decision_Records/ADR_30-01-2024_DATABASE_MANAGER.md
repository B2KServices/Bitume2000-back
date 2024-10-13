## Problématiques

- Rendre extensible le support de nouveaux types de bases de données.
- Rendre extensible le support d'un nombre arbitraire de bases de données.

## Remarques

Pour chaque projet backend, il faut définir au moins deux bases de données:

- Au moins une base de données pour la logique de l'application: soit Postgres, soit MongoDB
- Une base MongoDB pour les logs

Les bibliothèques retenues pour interragir avec ces deux dialectes sont SQLAlchemy (pour Postgres) et PyMongo (pour
MongoDB).\
Nous avons décidés d'utiliser les bibliothèques Flask-SQLAlchemy et Flask-PyMongo pour gérer l'interaction avec Flask:
notablement, les requêtes ont accès à des connexions correspondant à leur durrée de vie.

Il y a une très grande similarité entre ces bases de donneées en termes de configuration :

- Flask-XXX expose un manager de connexion (les objets `SQLAlchemy` et `PyMongo`) à initialiser dans une variable
  globale (appelée typiquement `db` et `mongo`)
- Au moment de l'initialisation de l'application Flask, il faut connecter ce manager à l'objet Flask (couramment
  appelé `app`)
- Il faut alors spécifier l'URI de connexion à la base de données, sous cette
  forme: `dialect://user:password@host:port/database`
- *Note:* Pour Flask-SQLAlchemy, il ne semble être possible de connecter qu'une base de donneées, en se basant su le
  fait que la configuraion de l'URI se fait vie une variable de configuration unique, SQLALCHEMY_DATABASE_URI.

## Solution proposée

Centraliser la définition de chaque base de données à l'aide d'un manager: le `DatabaseManager`\
Sa responsabilité est de :

- récupérer dans l'environnement la configuration de connexion a chaque base de données (user, password, host, port,
  database)
- créer les objets `SQLAlchemy` et `PyMongo` correspondant à chaque base de données
- initialiser l'application Flask avec ces objets:

```python
database_manager = DatabaseManager()
db = database_manager.add_postgres_database('POSTGRES_DB')
mongo_logs = database_manager.add_mongo_database('MONGO_LOGS')

# ...

database_manager.init_app(app)
```

équivaut à

```python
mongo_logs = PyMongo()
db = SQLAlchemy()

# ...

app.config["SQLALCHEMY_DATABASE_URI"] = f"postgres://{POSTGRES_DB_USER}:{POSTGRES_DB_PASSWORD}@{POSTGRES_DB_HOST}:{POSTGRES_DB_PORT}/{POSTGRES_DB_DATABASE}"
db.init_app(app)
mongo_logs.init_app(app, uri=f"mongodb://{MONGO_LOGS_USER}:{MONGO_LOGS_PASSWORD}@{MONGO_LOGS_HOST}:{MONGO_LOGS_PORT}/{MONGO_LOGS_DATABASE}")
```