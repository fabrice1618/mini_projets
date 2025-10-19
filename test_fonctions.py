from database import ouvrir_database
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
