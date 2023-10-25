- ![Static Badge](https://img.shields.io/badge/P12%20D%C3%A9veloppez%20une%20architecture%20backend%20s%C3%A9curis%C3%A9e%20avec%20Python%20et%20SQL-blue?label=Projet)
- ![Static Badge](https://img.shields.io/badge/Ciran_G%C3%9CRB%C3%9CZ-darkgreen?label=Auteur)
- ![Static Badge](https://img.shields.io/badge/Octobre_2023-orange?label=Date)
- ![Static Badge](https://img.shields.io/badge/Python-blue?label=Language) [![Code style: black](https://img.shields.io/badge/Code%20style-Black-000000.svg)](https://github.com/psf/black)


# EpicEvents CRM Software: Logiciel CRM interne (English version down below)

EpicEvents CRM Software est un logiciel à exécuter localement. Il s'agit d'un outil permettant de collecter et de traiter les données des clients et de leurs événements, tout en facilitant la communication entre les différents pôles de l'entreprise EpicEvents. Cette application est implémentée sous la forme d'un CLI (Command-Line Interface). Elle permet la lecture, la création, la mise à jour de collaborateurs, clients, contrats et évènements.

## Pré-requis

Ce logiciel ayant été développé en utilisant le SGBD PostgreSQL, son installation est obligatoire. L'installation de l'interface pgAdmin4 est vivement recommandée pour faciliter la gestion de vos bases de données.

Pour plus d'informations concernant l'installation de PostgreSQL, veuillez consulter la documentation officielle en [suivant ce lien](https://www.postgresql.org/docs/current/).

## Installation

Ce logiciel peut être installé en suivant les étapes décrites ci-dessous.

1. Clonez ce dépôt de code à l'aide de la commande `$ git clone https://github.com/CeeG33/oc-cg-p12` (vous pouvez également télécharger le code [en tant qu'archive zip](https://github.com/CeeG33/oc-cg-p12/archive/refs/heads/main.zip).
2. Rendez vous depuis un terminal à la racine du répertoire oc-cg-p12 avec la commande `$ cd oc-cg-p12`
3. Créez un environnement virtuel pour le projet avec `$ python -m venv env` sous Windows ou `$ python3 -m venv env` sous MacOS ou Linux.
4. Activez l'environnement virtuel avec `$ env\Scripts\activate` sous Windows ou `$ source env/bin/activate` sous MacOS ou Linux.
5. Installez les dépendances du projet avec la commande `$ pip install -r requirements.txt`
6. Créez un fichier nommé `.env` à la racine du répertoire oc-cg-p12 et renseignez-y les variables d'environnements. Pour plus d'explications concernant les variables d'environnements, veuillez consulter le chapitre dédié ci-après.
7. Créez les tables initiales de la base de données avec `$ python epicevents/create_db.py`
8. Vous pouvez désormais accéder au programme à l'aide de la commande suivante `$ python -m epicevents`.

Les étapes 1 à 3 et 5 à 7 ne sont requises que pour l'installation initiale. Pour les lancements ultérieurs du logiciel, il suffit seulement d'exécuter les étapes 4 et 8 à partir du répertoire racine du projet.

Toutes les commandes permises dans le logiciel sont documentées. Ainsi, vous pouvez visualiser la documentation directement depuis votre terminal avec la commande `--help`.
Voici quelques exemples:

```
$ python -m epicevents --help
$ python -m epicevents collaborators --help
$ python -m epicevents collaborators create --help
```


## Variables d'environnement

Il est primordial de renseigner les variables d'environnement pour que le logiciel fonctionne. Celles-ci sont à définir par vous-même. Voici les variables d'environnement attendues ainsi que leur utilisation:

```
-DB_NAME >> Nom de la base de données allant être utilisée par le logiciel (exemple : epiceventsdb)
-DB_USER >> Nom de l'utilisateur de la base de données (exemple : utilisateur1)
-DB_PASSWORD >> Mot de passe de l'utilisateur de la base de données (exemple : motdepasse)
-SECRET_KEY >> Clé d’encodage des mots de passe utilisateurs. (exemple : epiceventssecret)
-ADMIN_EMAIL >> Email du compte administrateur qui sera automatiquement créé en tant que premier utilisateur du logiciel (exemple : administrateur@epicevents.com)
-ADMIN_PASSWORD >> Mot de passe du compte administrateur qui sera automatiquement créé en tant que premier utilisateur du logiciel (exemple : adminpass)
-DSN >> Lien de journalisation généré par Sentry.
-TOKEN >> Token d’identification de l'utilisateur du logiciel - DOIT être laissé vide.

```

Un modèle de fichier .env est déjà présent dans le répertoire (>> `.env_template`). Vous pouvez le copier et le renommer en .env afin d'y renseigner les variables d'environnement.


__________________________________________

