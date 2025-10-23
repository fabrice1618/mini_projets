"""
Test complet du workflow AI assistant
"""

from ai_assistant import process_user_request

print("=== Test workflow complet ===\n")

# Test 1: Créer un projet via prompt naturel
print("Test 1: Créer un projet")
print("-" * 50)
result = process_user_request("Crée un projet 'Mon Nouveau Projet' avec la description 'Test workflow complet'")
print(f"Message:\n{result['message']}\n")
print(f"Modified: {result['modified']}\n")

# Test 2: Lister les projets
print("Test 2: Lister les projets")
print("-" * 50)
result = process_user_request("Montre-moi tous les projets")
print(f"Message:\n{result['message']}\n")
print(f"Modified: {result['modified']}\n")

# Test 3: Créer une tâche
print("Test 3: Créer une tâche")
print("-" * 50)
result = process_user_request("Ajoute une action 'Tâche de test' dans le projet 1")
print(f"Message:\n{result['message']}\n")
print(f"Modified: {result['modified']}\n")
