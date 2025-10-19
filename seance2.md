# Séance 2 : Fonctions CRUD et Interface CLI

## Objectifs de la séance

Dans cette séance, vous allez créer les fonctions de base pour manipuler vos données (projets et tâches) dans la base de données SQLite, puis les utiliser dans des scripts simples en ligne de commande.

## Rappel : Qu'est-ce qu'une fonction ?

Une fonction est un bloc de code réutilisable qui effectue une tâche précise. En Python :

```python
def nom_fonction(parametre1, parametre2):
    # Code à exécuter
    resultat = parametre1 + parametre2
    return resultat
```

**Pourquoi utiliser des fonctions ?**
- Éviter de répéter le même code plusieurs fois
- Rendre le code plus lisible et organisé
- Faciliter les tests et la maintenance

## Partie 1 : Fonctions CRUD pour la base de données

### Qu'est-ce que CRUD ?

CRUD signifie :
- **C**reate (Créer) : ajouter de nouvelles données
- **R**ead (Lire) : récupérer/consulter des données
- **U**pdate (Modifier) : mettre à jour des données existantes
- **D**elete (Supprimer) : effacer des données

### Tâche 1.0 : Créer la base de données et les tables

Avant d'écrire les fonctions CRUD, vous devez créer la structure de la base de données.

#### Créer le fichier `create_database.py`

Ce script crée le fichier de base de données SQLite.

```python
import sqlite3

def creer_database(nom_fichier='gestion_projets.db'):
    """Crée le fichier de base de données SQLite"""
    conn = sqlite3.connect(nom_fichier)
    print(f"Base de données '{nom_fichier}' créée avec succès !")
    conn.close()

if __name__ == "__main__":
    creer_database()
```

#### Créer le fichier `create_tables.py`

Ce script crée les tables `projets` et `taches` dans la base de données.

```python
import sqlite3

def creer_tables(nom_fichier='gestion_projets.db'):
    """Crée les tables projets et taches dans la base de données"""
    conn = sqlite3.connect(nom_fichier)
    cursor = conn.cursor()

    # Création de la table projets
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT NOT NULL,
            echeance DATE NOT NULL
        )
    ''')

    # Création de la table taches
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS taches (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            projet_id INTEGER NOT NULL,
            type_tache TEXT NOT NULL CHECK(type_tache IN ('action', 'rendez-vous')),
            description TEXT NOT NULL,
            echeance DATE NOT NULL,
            date_heure_debut DATETIME,
            avancement INTEGER DEFAULT 0,
            collaborateur TEXT,
            FOREIGN KEY (projet_id) REFERENCES projets(id) ON DELETE CASCADE
        )
    ''')

    conn.commit()
    conn.close()
    print("Tables 'projets' et 'taches' créées avec succès !")

if __name__ == "__main__":
    creer_tables()
```

**À exécuter une seule fois au début :**
1. `python create_database.py` - Crée le fichier de base de données
2. `python create_tables.py` - Crée les tables dans la base de données

### Tâche 1.1 : Créer les fonctions utilitaires pour la base de données

Créez un fichier `database.py` avec une fonction pour ouvrir la connexion :

**`ouvrir_database(nom_fichier='gestion_projets.db')`**
   - Ouvre une connexion à la base de données SQLite
   - Paramètre : nom du fichier de base de données (par défaut : 'gestion_projets.db')
   - Retourne : un tuple (connexion, cursor)
   - Exemple : `conn, cursor = ouvrir_database()`

**Pourquoi cette fonction ?**
- Éviter de répéter le code de connexion dans chaque script
- Centraliser la configuration de la base de données
- Faciliter l'accès aux colonnes par leur nom avec `row_factory`

**Exemple de structure :**

```python
import sqlite3

def ouvrir_database(nom_fichier='gestion_projets.db'):
    """Ouvre une connexion à la base de données SQLite"""
    conn = sqlite3.connect(nom_fichier)
    conn.row_factory = sqlite3.Row  # Pour accéder aux colonnes par leur nom
    cursor = conn.cursor()
    return conn, cursor
```

### Tâche 1.2 : Créer le fichier de fonctions pour les projets

Créez un fichier `projet_db.py` avec les fonctions suivantes :

**Attention :**
- Toutes ces fonctions doivent recevoir `conn` et `cursor` comme premiers paramètres
- Chaque fonction qui modifie la base (création, modification, suppression) doit faire un `conn.commit()` pour valider les changements

1. **`creer_projet(conn, cursor, description, echeance)`**
   - Insère un nouveau projet dans la table `projets`
   - Retourne l'ID du projet créé

2. **`lire_projet(conn, cursor, projet_id)`**
   - Récupère les informations d'un projet à partir de son ID
   - Retourne un dictionnaire ou None si le projet n'existe pas

3. **`modifier_projet(conn, cursor, projet_id, description, echeance)`**
   - Met à jour les informations d'un projet existant
   - Retourne True si réussi, False sinon

4. **`supprimer_projet(conn, cursor, projet_id)`**
   - Supprime un projet de la base de données
   - Retourne True si réussi, False sinon

5. **`lister_projets(conn, cursor)`**
   - Récupère tous les projets
   - Retourne une liste de projets

### Tâche 1.3 : Créer le fichier de fonctions pour les tâches

Créez un fichier `tache_db.py` avec les fonctions suivantes :

**Attention :**
- Toutes ces fonctions doivent recevoir `conn` et `cursor` comme premiers paramètres
- Chaque fonction qui modifie la base (création, modification, suppression) doit faire un `conn.commit()` pour valider les changements

1. **`creer_tache(conn, cursor, projet_id, type_tache, description, echeance, date_heure_debut, avancement, collaborateur)`**
   - Insère une nouvelle tâche dans la table `taches`
   - Retourne l'ID de la tâche créée

2. **`lire_tache(conn, cursor, tache_id)`**
   - Récupère les informations d'une tâche à partir de son ID
   - Retourne un dictionnaire ou None si la tâche n'existe pas

3. **`modifier_tache(conn, cursor, tache_id, type_tache, description, echeance, date_heure_debut, avancement, collaborateur)`**
   - Met à jour les informations d'une tâche existante
   - Retourne True si réussi, False sinon

4. **`supprimer_tache(conn, cursor, tache_id)`**
   - Supprime une tâche de la base de données
   - Retourne True si réussi, False sinon

5. **`lister_taches(conn, cursor, projet_id=None)`**
   - Récupère toutes les tâches (ou seulement celles d'un projet si projet_id est fourni)
   - Retourne une liste de tâches

### Exemple de structure d'une fonction CRUD

**Important :** Les fonctions CRUD reçoivent la connexion (`conn`) et le curseur (`cursor`) en paramètres. Chaque fonction qui modifie la base de données doit faire un `conn.commit()` pour valider les changements de manière atomique.

```python
def creer_projet(conn, cursor, description, echeance):
    """Crée un nouveau projet dans la base de données"""
    cursor.execute(
        "INSERT INTO projets (description, echeance) VALUES (?, ?)",
        (description, echeance)
    )
    conn.commit()  # Validation de la transaction
    projet_id = cursor.lastrowid
    return projet_id

def lire_projet(conn, cursor, projet_id):
    """Récupère les informations d'un projet"""
    cursor.execute(
        "SELECT * FROM projets WHERE id = ?",
        (projet_id,)
    )
    resultat = cursor.fetchone()

    if resultat:
        return dict(resultat)  # Convertit Row en dictionnaire
    return None

def modifier_projet(conn, cursor, projet_id, description, echeance):
    """Modifie un projet existant"""
    cursor.execute(
        "UPDATE projets SET description = ?, echeance = ? WHERE id = ?",
        (description, echeance, projet_id)
    )
    conn.commit()  # Validation de la transaction
    return cursor.rowcount > 0  # Retourne True si au moins une ligne modifiée

def supprimer_projet(conn, cursor, projet_id):
    """Supprime un projet"""
    cursor.execute(
        "DELETE FROM projets WHERE id = ?",
        (projet_id,)
    )
    conn.commit()  # Validation de la transaction
    return cursor.rowcount > 0  # Retourne True si au moins une ligne supprimée

def lister_projets(conn, cursor):
    """Liste tous les projets"""
    cursor.execute("SELECT * FROM projets")
    resultats = cursor.fetchall()
    return [dict(row) for row in resultats]
```

**Pourquoi cette approche ?**
- Chaque fonction est **atomique** : elle valide sa propre modification immédiatement
- Si une erreur se produit, seule l'opération en cours est annulée
- Plus simple à comprendre et à déboguer pour les débutants

## Partie 2 : Scripts de vérification

### Tâche 2.1 : Créer un script de test

Créez un fichier `test_fonctions.py` qui :

1. Crée un nouveau projet
2. Affiche les informations du projet créé
3. Modifie le projet
4. Crée plusieurs tâches pour ce projet
5. Liste toutes les tâches du projet
6. Supprime une tâche
7. Vérifie que la suppression a fonctionné

**Exemple de structure :**

```python
from database import ouvrir_database, fermer_database
from projet_db import *
from tache_db import *

# Ouverture de la connexion à la base de données
conn, cursor = ouvrir_database()

# Test création projet
print("=== Test création de projet ===")
projet_id = creer_projet(conn, cursor, "Mon premier projet", "2025-12-31")
print(f"Projet créé avec l'ID : {projet_id}")

# Test lecture projet
print("\n=== Test lecture de projet ===")
projet = lire_projet(conn, cursor, projet_id)
print(f"Projet trouvé : {projet}")

# Test modification projet
print("\n=== Test modification de projet ===")
succes = modifier_projet(conn, cursor, projet_id, "Projet modifié", "2026-01-15")
print(f"Modification réussie : {succes}")

# Test création de tâches
print("\n=== Test création de tâches ===")
tache_id1 = creer_tache(conn, cursor, projet_id, "action", "Tâche 1", "2025-11-01", "2025-10-15 09:00", 0, "Alice")
tache_id2 = creer_tache(conn, cursor, projet_id, "rendez-vous", "Réunion", "2025-10-20", "2025-10-20 14:00", 0, "Bob")
print(f"Tâches créées avec les IDs : {tache_id1}, {tache_id2}")

# Test liste des tâches du projet
print("\n=== Test liste des tâches ===")
taches = lister_taches(conn, cursor, projet_id)
for tache in taches:
    print(f"Tâche {tache['id']}: {tache['description']} - {tache['type_tache']}")

# Test suppression d'une tâche
print("\n=== Test suppression de tâche ===")
succes = supprimer_tache(conn, cursor, tache_id2)
print(f"Suppression réussie : {succes}")

# Vérification de la suppression
print("\n=== Vérification après suppression ===")
taches = lister_taches(conn, cursor, projet_id)
print(f"Nombre de tâches restantes : {len(taches)}")

# Fermeture de la connexion
conn.close()
print("\n=== Tests terminés ===")
```

**Important :**
- Ouvrez la connexion au début du script avec `ouvrir_database()`
- Fermez la connexion à la fin avec `conn.close()`
- Pas besoin de `commit()` final car chaque fonction CRUD fait déjà son propre commit

## Partie 3 : Interface en ligne de commande (CLI)

### Tâche 3.1 : Créer un menu pour gérer les projets

Créez un fichier `cli_projets.py` qui affiche un menu permettant de :

1. Lister tous les projets
2. Créer un nouveau projet
3. Modifier un projet
4. Supprimer un projet
5. Quitter

**Exemple de structure :**

```python
from database import ouvrir_database, fermer_database
from projet_db import *

def afficher_menu():
    print("\n=== GESTION DES PROJETS ===")
    print("1. Lister tous les projets")
    print("2. Créer un nouveau projet")
    print("3. Modifier un projet")
    print("4. Supprimer un projet")
    print("5. Quitter")
    print("===========================")

def main():
    # Ouvrir la connexion à la base de données
    conn, cursor = ouvrir_database()

    while True:
        afficher_menu()
        choix = input("\nVotre choix : ")

        if choix == "1":
            # Code pour lister les projets
            projets = lister_projets(conn, cursor)
            if projets:
                for projet in projets:
                    print(f"ID: {projet['id']}, Description: {projet['description']}, Échéance: {projet['echeance']}")
            else:
                print("Aucun projet trouvé.")

        elif choix == "2":
            # Code pour créer un projet
            description = input("Description du projet : ")
            echeance = input("Échéance (AAAA-MM-JJ) : ")
            projet_id = creer_projet(conn, cursor, description, echeance)
            print(f"Projet créé avec succès ! ID: {projet_id}")

        elif choix == "3":
            # Code pour modifier un projet
            projet_id = int(input("ID du projet à modifier : "))
            description = input("Nouvelle description : ")
            echeance = input("Nouvelle échéance (AAAA-MM-JJ) : ")
            if modifier_projet(conn, cursor, projet_id, description, echeance):
                print("Projet modifié avec succès !")
            else:
                print("Erreur : projet non trouvé.")

        elif choix == "4":
            # Code pour supprimer un projet
            projet_id = int(input("ID du projet à supprimer : "))
            if supprimer_projet(conn, cursor, projet_id):
                print("Projet supprimé avec succès !")
            else:
                print("Erreur : projet non trouvé.")

        elif choix == "5":
            print("Au revoir !")
            break

        else:
            print("Choix invalide !")

    # Fermer la connexion à la base de données
    conn.close()

if __name__ == "__main__":
    main()
```

**Important :**
- La connexion est ouverte une seule fois au début du programme
- La connexion est fermée à la fin du programme, pas à chaque opération
- Chaque fonction CRUD fait son propre `commit()` donc les données sont bien sauvegardées

### Tâche 3.2 : Créer un menu pour gérer les tâches

Créez un fichier `cli_taches.py` similaire pour gérer les tâches avec les options :

1. Lister toutes les tâches
2. Lister les tâches d'un projet
3. Créer une nouvelle tâche
4. Modifier une tâche
5. Supprimer une tâche
6. Quitter

## Ressources utiles

- Cours Python (partie 4) : https://github.com/fabrice1618/intro_python/blob/main/intro-python-part4-csv_sql.ipynb
- Documentation SQLite en Python : https://docs.python.org/fr/3/library/sqlite3.html

## Critères de réussite

À la fin de cette séance, vous devez avoir :

- ✅ Un fichier `create_database.py` pour créer la base de données
- ✅ Un fichier `create_tables.py` pour créer les tables
- ✅ Un fichier de base de données `gestion_projets.db` créé et avec ses tables
- ✅ Un fichier `database.py` avec la fonction `ouvrir_database()`
- ✅ Un fichier `projet_db.py` avec toutes les fonctions CRUD pour les projets (avec `commit()`)
- ✅ Un fichier `tache_db.py` avec toutes les fonctions CRUD pour les tâches (avec `commit()`)
- ✅ Un script `test_fonctions.py` qui vérifie que vos fonctions fonctionnent correctement
- ✅ Un script `cli_projets.py` avec un menu fonctionnel pour gérer les projets
- ✅ Un script `cli_taches.py` avec un menu fonctionnel pour gérer les tâches
- ✅ Tous vos scripts s'exécutent sans erreur

## Conseils

- **Commencez par créer la base de données** : exécutez d'abord `create_database.py` puis `create_tables.py`
- Testez chaque fonction au fur et à mesure que vous les écrivez
- **N'oubliez pas le `conn.commit()`** dans les fonctions qui modifient la base (créer, modifier, supprimer)
- Utilisez des `print()` pour déboguer et voir ce qui se passe
- Pensez à gérer les cas d'erreur (par exemple, si un utilisateur entre un ID qui n'existe pas)
