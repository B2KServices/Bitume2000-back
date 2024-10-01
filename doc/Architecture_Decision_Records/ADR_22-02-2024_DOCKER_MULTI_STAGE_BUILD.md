## Problématique

Le projet tourne dans un conteneur Docker.

Il y a des différences entre l'environnement de développement et celui de production, résultant en deux Dockefiles
légèrement différents:

- l'utilisation du requirements.txt ou du requirements-dev.txt (par exemple, pytest n'est pas installé en production)
- l'entrypoint du Dockerfile :
    - En développement, on lance l'application avec `python main.py` et on veut pouvoir tester avec `pytest` si une
      variable d'environnement est configurée
    - En production, on lance l'application avec uwsgi

Afin de factoriser ces Dockerfiles on utilise la
syntaxe ['multi-stage build'](https://docs.docker.com/build/building/multi-stage/) de Docker:

```
FROM python:3.12-slim as base

... // instructions communes aux deux environnements


FROM base as dev

... // instructions de l'environnement de développement

ENTRYPOINT [ "bash", "-cl", "./envs/dev/back/back-start.sh" ]

FROM base as prod

... // instructions de l'environnement de production

ENTRYPOINT [ "bash", "-cl", "./envs/prod/back/back-start.sh" ]
```

Ce choix impacte la manière de build les images :

- Avec `docker build`, on ajoute l'option `--target dev`
- Avec docker-compose.yaml, on écrit :

```
    [service]:
        build:
            ...
            target: dev
```
