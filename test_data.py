"""
Script pour créer des données de test dans la base de données
Utilise les fonctions CRUD existantes pour alimenter la base
"""

from database import ouvrir_database
from projet_db import *
from tache_db import *
from datetime import datetime, timedelta

def clear_database(conn, cursor):
    """Supprime toutes les données existantes"""
    print("\n=== Nettoyage de la base de données ===")
    cursor.execute("DELETE FROM taches")
    cursor.execute("DELETE FROM projets")
    conn.commit()
    print("Base de données nettoyée.")

def create_test_projets(conn, cursor):
    """Crée des projets de test"""
    print("\n=== Création des projets de test ===")

    projets_data = [
        {
            'titre': 'Cours Python - Licence 3',
            'description': 'Enseignement de Python niveau avancé pour étudiants L3 informatique',
            'statut': 'ouvert'
        },
        {
            'titre': 'Cours Base de Données - Master 1',
            'description': 'Conception et gestion de bases de données relationnelles',
            'statut': 'ouvert'
        },
        {
            'titre': 'Projet Recherche IA',
            'description': 'Recherche sur les algorithmes d\'apprentissage automatique',
            'statut': 'ouvert'
        },
        {
            'titre': 'Organisation Conférence 2024',
            'description': 'Préparation de la conférence annuelle du département',
            'statut': 'ouvert'
        },
        {
            'titre': 'Cours Web - Archives 2024',
            'description': 'Ancien cours de développement web',
            'statut': 'ferme'
        }
    ]

    projet_ids = []
    for projet in projets_data:
        projet_id = creer_projet(
            conn, cursor,
            projet['titre'],
            projet['description'],
            projet['statut']
        )
        projet_ids.append(projet_id)
        print(f"✓ Projet créé : {projet['titre']} (ID: {projet_id})")

    return projet_ids

def create_test_taches(conn, cursor, projet_ids):
    """Crée des tâches de test pour les projets"""
    print("\n=== Création des tâches de test ===")

    # Date de référence : aujourd'hui
    today = datetime.now()

    # Projet 1 : Cours Python - Licence 3
    print(f"\nTâches pour le projet ID {projet_ids[0]} (Cours Python):")

    # Cours planifiés
    cours1_id = creer_tache(
        conn, cursor,
        projet_id=projet_ids[0],
        type_tache='cours',
        titre='Introduction à Python',
        description_resumee='Variables, types de données, structures de contrôle',
        date_heure=(today + timedelta(days=1)).strftime('%Y-%m-%d 09:00'),
        duree_minutes=120,
        avancement=100
    )
    print(f"  ✓ Cours créé : Introduction à Python (ID: {cours1_id})")

    cours2_id = creer_tache(
        conn, cursor,
        projet_id=projet_ids[0],
        type_tache='cours',
        titre='POO en Python',
        description_resumee='Classes, objets, héritage, polymorphisme',
        date_heure=(today + timedelta(days=8)).strftime('%Y-%m-%d 09:00'),
        duree_minutes=120,
        avancement=0
    )
    print(f"  ✓ Cours créé : POO en Python (ID: {cours2_id})")

    cours3_id = creer_tache(
        conn, cursor,
        projet_id=projet_ids[0],
        type_tache='cours',
        titre='Gestion des fichiers et exceptions',
        description_resumee='Manipulation de fichiers, gestion d\'erreurs',
        date_heure=(today + timedelta(days=15)).strftime('%Y-%m-%d 09:00'),
        duree_minutes=120,
        avancement=0
    )
    print(f"  ✓ Cours créé : Gestion des fichiers (ID: {cours3_id})")

    # Actions liées aux cours
    tache1_id = creer_tache(
        conn, cursor,
        projet_id=projet_ids[0],
        type_tache='action',
        titre='Préparer slides POO',
        description_resumee='Créer les supports de cours sur la POO',
        echeance_absolue=(today + timedelta(days=6)).strftime('%Y-%m-%d 18:00'),
        tache_reference_id=cours2_id,  # Échéance relative au cours POO
        lien_fichier_details='/cours/python/slides_poo.md',
        avancement=30
    )
    print(f"  ✓ Action créée : Préparer slides POO (ID: {tache1_id})")

    tache2_id = creer_tache(
        conn, cursor,
        projet_id=projet_ids[0],
        type_tache='action',
        titre='Corriger TP 1',
        description_resumee='Corriger les travaux pratiques du premier cours',
        echeance_absolue=(today + timedelta(days=5)).strftime('%Y-%m-%d 18:00'),
        avancement=0
    )
    print(f"  ✓ Action créée : Corriger TP 1 (ID: {tache2_id})")

    # Projet 2 : Cours Base de Données - Master 1
    print(f"\nTâches pour le projet ID {projet_ids[1]} (Cours BDD):")

    cours_bdd1 = creer_tache(
        conn, cursor,
        projet_id=projet_ids[1],
        type_tache='cours',
        titre='Modèle relationnel',
        description_resumee='Algèbre relationnelle, normalisation',
        date_heure=(today + timedelta(days=2)).strftime('%Y-%m-%d 14:00'),
        duree_minutes=180,
        avancement=50
    )
    print(f"  ✓ Cours créé : Modèle relationnel (ID: {cours_bdd1})")

    cours_bdd2 = creer_tache(
        conn, cursor,
        projet_id=projet_ids[1],
        type_tache='cours',
        titre='SQL avancé',
        description_resumee='Jointures, sous-requêtes, fonctions d\'agrégation',
        date_heure=(today + timedelta(days=9)).strftime('%Y-%m-%d 14:00'),
        duree_minutes=180,
        avancement=0
    )
    print(f"  ✓ Cours créé : SQL avancé (ID: {cours_bdd2})")

    reunion_bdd = creer_tache(
        conn, cursor,
        projet_id=projet_ids[1],
        type_tache='reunion',
        titre='Réunion coordination Master',
        description_resumee='Point avec les autres enseignants du Master',
        date_heure=(today + timedelta(days=4)).strftime('%Y-%m-%d 16:00'),
        duree_minutes=60,
        avancement=0
    )
    print(f"  ✓ Réunion créée : Coordination Master (ID: {reunion_bdd})")

    action_bdd = creer_tache(
        conn, cursor,
        projet_id=projet_ids[1],
        type_tache='action',
        titre='Créer base de données exemple',
        description_resumee='Préparer une BDD exemple pour les TPs',
        echeance_absolue=(today + timedelta(days=7)).strftime('%Y-%m-%d 18:00'),
        tache_reference_id=cours_bdd2,
        lien_fichier_details='/cours/bdd/exemple_entreprise.sql',
        avancement=60
    )
    print(f"  ✓ Action créée : Créer base exemple (ID: {action_bdd})")

    # Projet 3 : Projet Recherche IA
    print(f"\nTâches pour le projet ID {projet_ids[2]} (Recherche IA):")

    reunion_ia1 = creer_tache(
        conn, cursor,
        projet_id=projet_ids[2],
        type_tache='reunion',
        titre='Réunion équipe recherche',
        description_resumee='Point mensuel sur l\'avancement des travaux',
        date_heure=(today + timedelta(days=3)).strftime('%Y-%m-%d 10:00'),
        duree_minutes=90,
        avancement=0
    )
    print(f"  ✓ Réunion créée : Équipe recherche (ID: {reunion_ia1})")

    action_ia1 = creer_tache(
        conn, cursor,
        projet_id=projet_ids[2],
        type_tache='action',
        titre='Rédiger article CNN',
        description_resumee='Article sur les réseaux de neurones convolutifs',
        echeance_absolue=(today + timedelta(days=30)).strftime('%Y-%m-%d 23:59'),
        lien_fichier_details='/recherche/papers/cnn_2024.tex',
        avancement=45
    )
    print(f"  ✓ Action créée : Rédiger article (ID: {action_ia1})")

    action_ia2 = creer_tache(
        conn, cursor,
        projet_id=projet_ids[2],
        type_tache='action',
        titre='Analyser résultats expériences',
        description_resumee='Traiter les données des dernières expériences',
        echeance_absolue=(today + timedelta(days=10)).strftime('%Y-%m-%d 18:00'),
        avancement=20
    )
    print(f"  ✓ Action créée : Analyser résultats (ID: {action_ia2})")

    action_ia3 = creer_tache(
        conn, cursor,
        projet_id=projet_ids[2],
        type_tache='action',
        titre='Préparer présentation conférence',
        description_resumee='Slides pour la conférence ICML',
        echeance_absolue=(today + timedelta(days=45)).strftime('%Y-%m-%d 18:00'),
        lien_fichier_details='/recherche/presentations/icml_2024.pptx',
        avancement=0
    )
    print(f"  ✓ Action créée : Présentation conférence (ID: {action_ia3})")

    # Projet 4 : Organisation Conférence
    print(f"\nTâches pour le projet ID {projet_ids[3]} (Conférence):")

    reunion_conf1 = creer_tache(
        conn, cursor,
        projet_id=projet_ids[3],
        type_tache='reunion',
        titre='Comité d\'organisation',
        description_resumee='Réunion du comité pour préparer la conférence',
        date_heure=(today + timedelta(days=7)).strftime('%Y-%m-%d 15:00'),
        duree_minutes=120,
        avancement=0
    )
    print(f"  ✓ Réunion créée : Comité organisation (ID: {reunion_conf1})")

    action_conf1 = creer_tache(
        conn, cursor,
        projet_id=projet_ids[3],
        type_tache='action',
        titre='Contacter intervenants',
        description_resumee='Envoyer invitations aux conférenciers',
        echeance_absolue=(today + timedelta(days=14)).strftime('%Y-%m-%d 18:00'),
        avancement=70
    )
    print(f"  ✓ Action créée : Contacter intervenants (ID: {action_conf1})")

    action_conf2 = creer_tache(
        conn, cursor,
        projet_id=projet_ids[3],
        type_tache='action',
        titre='Réserver salles',
        description_resumee='Réservation des amphithéâtres pour la conférence',
        echeance_absolue=(today + timedelta(days=21)).strftime('%Y-%m-%d 17:00'),
        avancement=100
    )
    print(f"  ✓ Action créée : Réserver salles (ID: {action_conf2})")

    action_conf3 = creer_tache(
        conn, cursor,
        projet_id=projet_ids[3],
        type_tache='action',
        titre='Créer site web conférence',
        description_resumee='Développer le site de la conférence avec programme',
        echeance_absolue=(today + timedelta(days=28)).strftime('%Y-%m-%d 18:00'),
        lien_fichier_details='/web/conference2024/',
        avancement=35
    )
    print(f"  ✓ Action créée : Site web (ID: {action_conf3})")

    # Projet 5 : Cours Web - Archives (fermé)
    print(f"\nTâches pour le projet ID {projet_ids[4]} (Archives - projet fermé):")

    cours_web = creer_tache(
        conn, cursor,
        projet_id=projet_ids[4],
        type_tache='cours',
        titre='HTML/CSS avancé',
        description_resumee='Dernier cours de l\'année 2024',
        date_heure=(today - timedelta(days=30)).strftime('%Y-%m-%d 10:00'),
        duree_minutes=120,
        avancement=100
    )
    print(f"  ✓ Cours créé : HTML/CSS (ID: {cours_web})")

    action_web = creer_tache(
        conn, cursor,
        projet_id=projet_ids[4],
        type_tache='action',
        titre='Archiver supports de cours',
        description_resumee='Sauvegarder tous les supports dans l\'archive',
        echeance_absolue=(today - timedelta(days=5)).strftime('%Y-%m-%d 18:00'),
        avancement=100
    )
    print(f"  ✓ Action créée : Archiver supports (ID: {action_web})")

def display_summary(conn, cursor):
    """Affiche un résumé des données créées"""
    print("\n" + "="*60)
    print("=== RÉSUMÉ DES DONNÉES CRÉÉES ===")
    print("="*60)

    # Comptage des projets
    projets = lister_projets(conn, cursor)
    projets_ouverts = lister_projets(conn, cursor, statut='ouvert')
    projets_fermes = lister_projets(conn, cursor, statut='ferme')

    print(f"\nPROJETS:")
    print(f"  - Total: {len(projets)}")
    print(f"  - Ouverts: {len(projets_ouverts)}")
    print(f"  - Fermés: {len(projets_fermes)}")

    # Comptage des tâches
    taches = lister_taches(conn, cursor)
    taches_cours = lister_taches(conn, cursor, type_tache='cours')
    taches_reunion = lister_taches(conn, cursor, type_tache='reunion')
    taches_action = lister_taches(conn, cursor, type_tache='action')

    print(f"\nTÂCHES:")
    print(f"  - Total: {len(taches)}")
    print(f"  - Cours: {len(taches_cours)}")
    print(f"  - Réunions: {len(taches_reunion)}")
    print(f"  - Actions: {len(taches_action)}")

    # Tâches à venir
    taches_a_venir = lister_taches_a_venir(conn, cursor, limite=5)
    print(f"\nPROCHAINES TÂCHES À VENIR: {len(taches_a_venir)}")
    for tache in taches_a_venir:
        date_affichage = tache['echeance_absolue'] or tache['date_heure']
        print(f"  - {tache['titre']} ({tache['type']}) - {date_affichage}")

    # Avancement moyen
    if taches:
        avancement_moyen = sum(t['avancement'] for t in taches) / len(taches)
        print(f"\nAVANCEMENT MOYEN: {avancement_moyen:.1f}%")

    print("\n" + "="*60)

def main():
    """Fonction principale"""
    print("="*60)
    print("CRÉATION DE DONNÉES DE TEST")
    print("="*60)

    # Ouverture de la connexion
    conn, cursor = ouvrir_database()

    try:
        # Demander confirmation avant de nettoyer
        print("\nATTENTION : Ce script va supprimer toutes les données existantes !")
        confirmation = input("Voulez-vous continuer ? (o/n) : ")

        if confirmation.lower() != 'o':
            print("Opération annulée.")
            return

        # Nettoyage de la base
        clear_database(conn, cursor)

        # Création des données
        projet_ids = create_test_projets(conn, cursor)
        create_test_taches(conn, cursor, projet_ids)

        # Affichage du résumé
        display_summary(conn, cursor)

        print("\n✓ Données de test créées avec succès !")
        print("\nVous pouvez maintenant tester les scripts CLI :")
        print("  - python cli_projets.py")
        print("  - python cli_taches.py")

    except Exception as e:
        print(f"\n✗ Erreur lors de la création des données : {e}")
        import traceback
        traceback.print_exc()

    finally:
        # Fermeture de la connexion
        conn.close()
        print("\nConnexion à la base de données fermée.")

if __name__ == "__main__":
    main()
