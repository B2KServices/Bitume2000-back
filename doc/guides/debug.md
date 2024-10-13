## Introduction

Actuellement, nous ne savons pas comment faire marcher le debugger fournit avec Pycharm.

La solution trouvée consiste a utiliser le module `debugpy` en mode 'attach', \
i.e. le debugger ne lance pas le programme, mais se connecte au programme en \
cours d'éxécution.

Cette solution fonctionne avec **VSCode**, en conjonction avec l'extension \
'**Remote SSH**' afin de pouvoir debugger aussi a l'intérieur du code des modules \
importés.

## Conditions Préliminaires

Il faut:

- Avoir installé l'extension 'Remote SSH' dans VSCode
- Avoir mappé, dans docker-compose.yml, le port 22 du docker flask sur un port \
  de l'hote pour le ssh
- Avoir ajouté `debugpy` dans les dépendences optionnelles du projet
- Avoir introduit ces lignes dans le script app/main.py:
  ```python
  import debugpy

  debugpy.listen(("0.0.0.0", 5678))
  debugpy.wait_for_client()
  ```
- Avoir retiré le mode debug de Flask: app.run(..., debug=~~True~~)

## Étapes

Voici la marche a suivre:

- Mettre la valeur `DEBUG=1` dans le fichier envs/dev/back/.env

- Lancer les dockers normalement\
  Ces lignes devraient s'afficher dans les logs de Docker:
  ```
  quick_start_back      | 0.00s - Debugger warning: It seems that frozen modules are being used, which may
  quick_start_back      | 0.00s - make the debugger miss breakpoints. Please pass -Xfrozen_modules=off
  quick_start_back      | 0.00s - to python to disable frozen modules.
  quick_start_back      | 0.00s - Note: Debugging will proceed. Set PYDEVD_DISABLE_FILE_VALIDATION=1 to disable this validation.
  ```

- Dans VSCode, ouvrir la 'Command Palette' (Ctrl Shift P) et executer la commande \
  `Remote-SSH: Connect to Host...`

- (Selement la premiere fois)
    - `Add New SSH Host...`
    - Entrer la commande `ssh -p XXX root@localhost` (le port XXX étant \
      actuellement le port mappé avec le port 22 du service Docker 'flask')

- Dans la nouvelle fenetre VSCode, le mot de passe de root@localhost demandé est `root`

- Ouvrir l'Explorer (1ere icone en haut a gauche), cliquer sur `Open Folder`, \
  choisir le dossier du projet dans le docker (`/code`)

- Ouvrir les extensions et installer l'extension Python sur le remote (VSCode \
  le suggere également avec une notification popup)\
  Éventuellement, activer l'extension si ce n'est pas fait automatiquement

- Placer les breakpoints aux endroits souhaités

- Ouvrir le panneau 'Run and Debug' de VSCode

- (Seulement la première fois)
    - Cliquer sur `create a launch.json file`
    - sélectionner `Python > Remote Attach`
    - Entrer `localhost` pour l'host
    - Entrer `5678` pour le port
    - Dans le launch.json généré changer `"justMyCode": true` en `"justMyCode": false`

- Lancer le debuggage (l'attache au process) depuis l'onglet `Run and Debug` \
  ou bien en appuyant sur F5
