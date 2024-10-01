## Système de Pooling de Connexion avec SQLAlchemy

Notre application utilise SQLAlchemy pour la gestion des connexions à la base de données, avec un système de pooling de
connexion pour optimiser à la fois les performances et la gestion des ressources.

### Paramètres de Pooling

- **`pool_size=10`** : Garde 10 connexions ouvertes en permanence.
    - *Exemple d'utilisation* : Dans un scénario où la majorité de nos requêtes sont légères et constantes, maintenir 10
      connexions ouvertes évite les délais d'ouverture de nouvelles connexions.
- **`max_overflow=20`** : Permet jusqu'à 30 connexions (10 + 20) lors de pics de demandes.
    - *Exemple d'utilisation* : Lors d'une augmentation soudaine des requêtes, comme pendant une campagne
      promotionnelle, le système peut ouvrir temporairement jusqu'à 30 connexions pour gérer la charge.
- **`pool_recycle=1800`** (30 minutes) : Recycle les connexions pour prévenir des déconnexions dues à des timeouts.
    - *Exemple d'utilisation* : Ceci est particulièrement utile pour éviter les déconnexions lors des périodes de faible
      activité, comme la nuit.
- **`pool_pre_ping=True`** : Vérifie la validité de la connexion avant son utilisation.
    - *Exemple d'utilisation* : Avant de réaliser une transaction importante, le système s'assure que la connexion est
      toujours valide, augmentant ainsi la fiabilité de l'opération.

Ces paramètres assurent une gestion efficace et flexible des connexions, adaptée aux divers scénarios d'utilisation de
notre application.
