"""
Test spécifique pour le listing de projets
"""

from ai_assistant import process_user_request

prompts = [
    "Liste tous les projets",
    "Montre-moi tous les projets",
    "Affiche les projets",
    "Quels sont mes projets ?",
    "Liste les projets ouverts"
]

for prompt in prompts:
    print(f"\nPrompt: {prompt}")
    print("-" * 60)
    result = process_user_request(prompt)
    print(f"{result['message']}\n")
