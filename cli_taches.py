from database import ouvrir_database
from tache_db import *

def afficher_menu():
    print("\n=== GESTION DES TÂCHES ===")
    print("1. Lister toutes les tâches")
    print("2. Lister les tâches d'un projet")
    print("3. Lister les tâches par type")
    print("4. Voir les tâches à venir")
    print("5. Créer une nouvelle tâche")
    print("6. Modifier une tâche")
    print("7. Modifier l'avancement d'une tâche")
    print("8. Supprimer une tâche")
    print("9. Quitter")
    print("==========================")

def afficher_tache(tache):
    """Affiche les informations d'une tâche de manière formatée"""
    print(f"\nID: {tache['tache_id']} | Projet ID: {tache['projet_id']} | Type: {tache['type']}")
    print(f"Titre: {tache['titre']}")
    if tache['description_resumee']:
        print(f"Description: {tache['description_resumee']}")
    if tache['date_heure']:
        print(f"Date/Heure: {tache['date_heure']}", end="")
        if tache['duree_minutes']:
            print(f" (Durée: {tache['duree_minutes']} min)")
        else:
            print()
    if tache['echeance_absolue']:
        print(f"Échéance: {tache['echeance_absolue']}")
    if tache['tache_reference_id']:
        print(f"Échéance relative à la tâche ID: {tache['tache_reference_id']}")
    if tache['lien_fichier_details']:
        print(f"Fichier détails: {tache['lien_fichier_details']}")
    print(f"Avancement: {tache['avancement']}%")
    print(f"Date de création: {tache['date_creation']}")
    print("-" * 60)

def main():
    # Ouvrir la connexion à la base de données
    conn, cursor = ouvrir_database()

    while True:
        afficher_menu()
        choix = input("\nVotre choix : ")

        if choix == "1":
            # Lister toutes les tâches
            taches = lister_taches(conn, cursor)
            if taches:
                print(f"\n{len(taches)} tâche(s) trouvée(s):")
                for tache in taches:
                    afficher_tache(tache)
            else:
                print("Aucune tâche trouvée.")

        elif choix == "2":
            # Lister les tâches d'un projet
            projet_id = int(input("ID du projet : "))
            taches = lister_taches(conn, cursor, projet_id=projet_id)
            if taches:
                print(f"\n{len(taches)} tâche(s) pour le projet {projet_id}:")
                for tache in taches:
                    afficher_tache(tache)
            else:
                print("Aucune tâche trouvée pour ce projet.")

        elif choix == "3":
            # Lister les tâches par type
            print("\nTypes disponibles: cours, reunion, action")
            type_tache = input("Type de tâche : ")
            if type_tache not in ['cours', 'reunion', 'action']:
                print("Type invalide !")
                continue
            taches = lister_taches(conn, cursor, type_tache=type_tache)
            if taches:
                print(f"\n{len(taches)} tâche(s) de type '{type_tache}':")
                for tache in taches:
                    afficher_tache(tache)
            else:
                print(f"Aucune tâche de type '{type_tache}' trouvée.")

        elif choix == "4":
            # Voir les tâches à venir
            limite = input("Nombre de tâches à afficher (défaut: 10) : ")
            limite = int(limite) if limite.strip() else 10
            taches = lister_taches_a_venir(conn, cursor, limite=limite)
            if taches:
                print(f"\n{len(taches)} tâche(s) à venir:")
                for tache in taches:
                    afficher_tache(tache)
            else:
                print("Aucune tâche à venir trouvée.")

        elif choix == "5":
            # Créer une tâche
            print("\n--- Création d'une nouvelle tâche ---")
            projet_id = int(input("ID du projet : "))
            print("Types disponibles: cours, reunion, action")
            type_tache = input("Type de tâche : ")
            if type_tache not in ['cours', 'reunion', 'action']:
                print("Type invalide !")
                continue

            titre = input("Titre de la tâche (obligatoire) : ")
            if not titre.strip():
                print("Erreur : le titre est obligatoire.")
                continue

            description_resumee = input("Description résumée (optionnel) : ")
            description_resumee = description_resumee if description_resumee.strip() else None

            date_heure = input("Date et heure (AAAA-MM-JJ HH:MM, optionnel) : ")
            date_heure = date_heure if date_heure.strip() else None

            duree_minutes = input("Durée en minutes (optionnel) : ")
            duree_minutes = int(duree_minutes) if duree_minutes.strip() else None

            echeance_absolue = input("Échéance absolue (AAAA-MM-JJ HH:MM, optionnel) : ")
            echeance_absolue = echeance_absolue if echeance_absolue.strip() else None

            tache_reference_id = input("ID tâche de référence pour échéance relative (optionnel) : ")
            tache_reference_id = int(tache_reference_id) if tache_reference_id.strip() else None

            lien_fichier_details = input("Lien vers fichier de détails (optionnel) : ")
            lien_fichier_details = lien_fichier_details if lien_fichier_details.strip() else None

            avancement = input("Avancement 0-100 (défaut: 0) : ")
            avancement = int(avancement) if avancement.strip() else 0

            tache_id = creer_tache(conn, cursor, projet_id, type_tache, titre,
                                   description_resumee, date_heure, duree_minutes,
                                   echeance_absolue, tache_reference_id,
                                   lien_fichier_details, avancement)
            print(f"Tâche créée avec succès ! ID: {tache_id}")

        elif choix == "6":
            # Modifier une tâche
            print("\n--- Modification d'une tâche ---")
            tache_id = int(input("ID de la tâche à modifier : "))

            # Vérifier si la tâche existe
            tache = lire_tache(conn, cursor, tache_id)
            if not tache:
                print("Erreur : tâche non trouvée.")
                continue

            print(f"\nTâche actuelle:")
            afficher_tache(tache)

            print("\nLaissez vide pour conserver la valeur actuelle.")
            print("Types disponibles: cours, reunion, action")
            type_tache = input(f"Nouveau type [{tache['type']}] : ")
            if type_tache.strip() and type_tache not in ['cours', 'reunion', 'action']:
                print("Type invalide !")
                continue

            titre = input(f"Nouveau titre [{tache['titre']}] : ")
            description_resumee = input(f"Nouvelle description [{tache['description_resumee']}] : ")
            date_heure = input(f"Nouvelle date/heure [{tache['date_heure']}] : ")
            duree_minutes = input(f"Nouvelle durée minutes [{tache['duree_minutes']}] : ")
            echeance_absolue = input(f"Nouvelle échéance [{tache['echeance_absolue']}] : ")
            tache_reference_id = input(f"Nouveau ID tâche référence [{tache['tache_reference_id']}] : ")
            lien_fichier_details = input(f"Nouveau lien fichier [{tache['lien_fichier_details']}] : ")
            avancement = input(f"Nouvel avancement [{tache['avancement']}] : ")

            # Ne mettre à jour que les champs remplis
            type_tache = type_tache if type_tache.strip() else None
            titre = titre if titre.strip() else None
            description_resumee = description_resumee if description_resumee.strip() else None
            date_heure = date_heure if date_heure.strip() else None
            duree_minutes = int(duree_minutes) if duree_minutes.strip() else None
            echeance_absolue = echeance_absolue if echeance_absolue.strip() else None
            tache_reference_id = int(tache_reference_id) if tache_reference_id.strip() else None
            lien_fichier_details = lien_fichier_details if lien_fichier_details.strip() else None
            avancement = int(avancement) if avancement.strip() else None

            if modifier_tache(conn, cursor, tache_id, type_tache, titre, description_resumee,
                            date_heure, duree_minutes, echeance_absolue, tache_reference_id,
                            lien_fichier_details, avancement):
                print("Tâche modifiée avec succès !")
            else:
                print("Aucune modification effectuée.")

        elif choix == "7":
            # Modifier l'avancement d'une tâche
            print("\n--- Modification de l'avancement ---")
            tache_id = int(input("ID de la tâche : "))
            tache = lire_tache(conn, cursor, tache_id)
            if not tache:
                print("Erreur : tâche non trouvée.")
                continue

            print(f"Tâche: {tache['titre']}")
            print(f"Avancement actuel: {tache['avancement']}%")
            nouvel_avancement = int(input("Nouvel avancement (0-100) : "))

            if 0 <= nouvel_avancement <= 100:
                if modifier_tache(conn, cursor, tache_id, avancement=nouvel_avancement):
                    print(f"Avancement mis à jour : {nouvel_avancement}%")
                else:
                    print("Erreur lors de la mise à jour.")
            else:
                print("Erreur : l'avancement doit être entre 0 et 100.")

        elif choix == "8":
            # Supprimer une tâche
            print("\n--- Suppression d'une tâche ---")
            tache_id = int(input("ID de la tâche à supprimer : "))

            # Vérifier si la tâche existe
            tache = lire_tache(conn, cursor, tache_id)
            if not tache:
                print("Erreur : tâche non trouvée.")
                continue

            afficher_tache(tache)
            confirmation = input("\nÊtes-vous sûr de vouloir supprimer cette tâche ? (o/n) : ")

            if confirmation.lower() == 'o':
                if supprimer_tache(conn, cursor, tache_id):
                    print("Tâche supprimée avec succès !")
                else:
                    print("Erreur lors de la suppression.")

        elif choix == "9":
            print("Au revoir !")
            break

        else:
            print("Choix invalide !")

    # Fermer la connexion à la base de données
    conn.close()

if __name__ == "__main__":
    main()
