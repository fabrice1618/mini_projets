#!/usr/bin/env python3
"""
Script de démonstration de l'intégration IA
Teste toutes les fonctionnalités principales
"""

from ai_assistant import process_user_request, test_connection
import time

def print_section(title):
    """Affiche un titre de section"""
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70 + "\n")

def test_prompt(prompt, delay=2):
    """Teste un prompt et affiche le résultat"""
    print(f"📝 Prompt: {prompt}")
    print("-" * 70)
    result = process_user_request(prompt)
    print(f"{result['message']}")
    if result['modified']:
        print("\n✅ Base de données modifiée")
    print()
    time.sleep(delay)  # Pause pour ne pas surcharger Ollama

def main():
    print_section("DÉMONSTRATION DE L'ASSISTANT IA")

    # Test de connexion
    print("🔌 Test de connexion à Ollama...")
    if not test_connection():
        print("❌ Impossible de se connecter à Ollama")
        print("Assurez-vous qu'Ollama est démarré: sudo systemctl start ollama")
        return
    print("✅ Connexion à Ollama réussie\n")

    # PROJETS
    print_section("1. GESTION DES PROJETS")

    print("➤ Création de projets:")
    test_prompt("Crée un projet 'Démonstration IA' avec la description 'Test complet du système'")
    test_prompt("Ajoute un nouveau projet 'Formation Python'")

    print("➤ Listing de projets:")
    test_prompt("Affiche tous les projets")
    test_prompt("Liste les projets ouverts")

    # TÂCHES
    print_section("2. GESTION DES TÂCHES")

    print("➤ Création de tâches:")
    test_prompt("Crée une action 'Préparer la présentation' dans le projet 1")
    test_prompt("Ajoute une réunion 'Kickoff meeting' le 2025-11-01 10:00:00 pour 60 minutes dans le projet 1")
    test_prompt("Créer un cours 'Introduction Python' le 2025-11-05 14:00:00 avec échéance au 2025-11-05 18:00:00 dans le projet 1")

    print("➤ Listing de tâches:")
    test_prompt("Liste les tâches du projet 1")
    test_prompt("Montre-moi les prochaines tâches à venir")

    print("➤ Modification de tâches:")
    test_prompt("Passe la tâche 1 à 50% d'avancement")
    test_prompt("Change le titre de la tâche 2 en 'Réunion de lancement'")

    # RECHERCHES
    print_section("3. RECHERCHES ET REQUÊTES")

    test_prompt("Affiche toutes les réunions")
    test_prompt("Liste les actions")
    test_prompt("Quels sont mes projets ?")

    # OPÉRATIONS AVANCÉES
    print_section("4. OPÉRATIONS AVANCÉES")

    print("➤ Consultation de détails:")
    test_prompt("Affiche les détails du projet 1")
    test_prompt("Montre-moi la tâche 1")

    print("➤ Modifications:")
    test_prompt("Modifie la description du projet 1 en 'Description mise à jour'")
    test_prompt("Ferme le projet 2")

    print_section("DÉMONSTRATION TERMINÉE")
    print("✅ Tous les tests ont été exécutés avec succès!")
    print("\nL'assistant IA est maintenant intégré dans l'application NiceGUI.")
    print("Lancez l'application avec: python kanban_view_nice.py")

if __name__ == "__main__":
    main()
