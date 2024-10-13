FROM python:3.12-slim AS base

# Définition du répertoire de travail et de l'exposition du port
WORKDIR /code
EXPOSE 5001

# Mise à jour et installation des dépendances nécessaires
RUN apt-get update -y \
    && apt-get upgrade -y \
    && apt-get install -y gcc vim netcat-traditional postgresql-client \
    && apt-get clean all

# Création du groupe et de l'utilisateur
RUN addgroup --gid 1000 groupcontainer \
    && useradd -ms /bin/bash --uid 1000 --gid 1000 ifpen \
    && mkdir -p /code/app \
    && touch /code/app/uwsgi.pid \
    && chown -R ifpen:groupcontainer /code \
    && chmod -R 755 /code \
    && mkdir -p /code/app \
    && chown -R ifpen:groupcontainer /code/app \
    && chmod -R 755 /code/app

# Définition des variables d'environnement
COPY ./envs/shared/back/pip.conf /etc/pip.conf
ENV PYTHONPATH=/code/app
ENV EXPORT_PATH=/tmp/
COPY ./ /code

# Image de développement
FROM base AS dev
RUN pip install '.'
USER ifpen
ENTRYPOINT [ "bash", "-cl", "./envs/dev/back/back-start.sh" ]

# Image de production
FROM base AS prod
RUN pip install '.[production]'
USER ifpen
ENTRYPOINT [ "bash", "-cl", "./envs/prod/back/back-start.sh" ]
