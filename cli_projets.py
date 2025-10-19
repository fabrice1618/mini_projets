from database import ouvrir_database
from projet_db import *

def afficher_menu():
    print("\n=== GESTION DES PROJETS ===")
    print("1. Lister tous les projets")
    print("2. Lister les projets ouverts")
    print("3. Lister les projets fermés")
    print("4. Créer un nouveau projet")
    print("5. Modifier un projet")
    print("6. Changer le statut d'un projet")
    print("7. Supprimer un projet")
    print("8. Quitter")
    print("===========================")

def afficher_projet(projet):
    """Affiche les informations d'un projet de manière formatée"""
    print(f"\nID: {projet['projet_id']}")
    print(f"Titre: {projet['titre']}")
    if projet['description']:
        print(f"Description: {projet['description']}")
    print(f"Statut: {projet['statut']}")
    print(f"Date de création: {projet['date_creation']}")
    print("-" * 50)

def main():
    # Ouvrir la connexion à la base de données
    conn, cursor = ouvrir_database()

    while True:
        afficher_menu()
        choix = input("\nVotre choix : ")

        if choix == "1":
            # Lister tous les projets
            projets = lister_projets(conn, cursor)
            if projets:
                print(f"\n{len(projets)} projet(s) trouvé(s):")
                for projet in projets:
                    afficher_projet(projet)
            else:
                print("Aucun projet trouvé.")

        elif choix == "2":
            # Lister les projets ouverts
            projets = lister_projets(conn, cursor, statut='ouvert')
            if projets:
                print(f"\n{len(projets)} projet(s) ouvert(s):")
                for projet in projets:
                    afficher_projet(projet)
            else:
                print("Aucun projet ouvert trouvé.")

        elif choix == "3":
            # Lister les projets fermés
            projets = lister_projets(conn, cursor, statut='ferme')
            if projets:
                print(f"\n{len(projets)} projet(s) fermé(s):")
                for projet in projets:
                    afficher_projet(projet)
            else:
                print("Aucun projet fermé trouvé.")

        elif choix == "4":
            # Créer un projet
            print("\n--- Création d'un nouveau projet ---")
            titre = input("Titre du projet (obligatoire) : ")
            if not titre.strip():
                print("Erreur : le titre est obligatoire.")
                continue
            description = input("Description (optionnel, Entrée pour ignorer) : ")
            description = description if description.strip() else None
            statut = input("Statut (ouvert/ferme, défaut: ouvert) : ") or 'ouvert'
            if statut not in ['ouvert', 'ferme']:
                print("Erreur : le statut doit être 'ouvert' ou 'ferme'.")
                continue

            projet_id = creer_projet(conn, cursor, titre, description, statut)
            print(f"Projet créé avec succès ! ID: {projet_id}")

        elif choix == "5":
            # Modifier un projet
            print("\n--- Modification d'un projet ---")
            projet_id = int(input("ID du projet à modifier : "))

            # Vérifier si le projet existe
            projet = lire_projet(conn, cursor, projet_id)
            if not projet:
                print("Erreur : projet non trouvé.")
                continue

            print(f"\nProjet actuel:")
            afficher_projet(projet)

            print("\nLaissez vide pour conserver la valeur actuelle.")
            titre = input(f"Nouveau titre [{projet['titre']}] : ")
            description = input(f"Nouvelle description [{projet['description']}] : ")
            statut = input(f"Nouveau statut [{projet['statut']}] : ")

            # Ne mettre à jour que les champs remplis
            titre = titre if titre.strip() else None
            description = description if description.strip() else None
            statut = statut if statut.strip() else None

            if statut and statut not in ['ouvert', 'ferme']:
                print("Erreur : le statut doit être 'ouvert' ou 'ferme'.")
                continue

            if modifier_projet(conn, cursor, projet_id, titre, description, statut):
                print("Projet modifié avec succès !")
            else:
                print("Aucune modification effectuée.")

        elif choix == "6":
            # Changer le statut d'un projet
            print("\n--- Changement de statut ---")
            projet_id = int(input("ID du projet : "))
            projet = lire_projet(conn, cursor, projet_id)
            if not projet:
                print("Erreur : projet non trouvé.")
                continue

            statut_actuel = projet['statut']
            nouveau_statut = 'ferme' if statut_actuel == 'ouvert' else 'ouvert'
            print(f"Statut actuel : {statut_actuel}")
            print(f"Nouveau statut : {nouveau_statut}")
            confirmation = input("Confirmer le changement ? (o/n) : ")

            if confirmation.lower() == 'o':
                if modifier_projet(conn, cursor, projet_id, statut=nouveau_statut):
                    print(f"Statut changé avec succès : {nouveau_statut}")
                else:
                    print("Erreur lors du changement de statut.")

        elif choix == "7":
            # Supprimer un projet
            print("\n--- Suppression d'un projet ---")
            projet_id = int(input("ID du projet à supprimer : "))

            # Vérifier si le projet existe
            projet = lire_projet(conn, cursor, projet_id)
            if not projet:
                print("Erreur : projet non trouvé.")
                continue

            afficher_projet(projet)
            confirmation = input("\nÊtes-vous sûr de vouloir supprimer ce projet ? (o/n) : ")

            if confirmation.lower() == 'o':
                if supprimer_projet(conn, cursor, projet_id):
                    print("Projet supprimé avec succès !")
                else:
                    print("Erreur lors de la suppression.")

        elif choix == "8":
            print("Au revoir !")
            break

        else:
            print("Choix invalide !")

    # Fermer la connexion à la base de données
    conn.close()

if __name__ == "__main__":
    main()
