"""
Configuration pour l'intégration Ollama
"""

# URL du serveur Ollama local
OLLAMA_HOST = "http://localhost:11434"

# Modèle à utiliser (Llama 3.2 recommandé pour function calling)
OLLAMA_MODEL = "llama3.2"

# Paramètres de génération
GENERATION_PARAMS = {
    "temperature": 0.1,  # Faible température pour plus de cohérence
    "top_p": 0.9,
    "top_k": 40,
}

# Options de timeout
TIMEOUT_SECONDS = 30

# Messages système pour guider l'IA
SYSTEM_MESSAGE = """Tu es un assistant IA pour la gestion de projets et tâches.
Tu dois aider l'utilisateur à gérer ses projets en utilisant les outils (tools) disponibles.

Règles importantes:
1. Utilise TOUJOURS un outil pour effectuer des actions sur la base de données
2. Sois précis dans l'extraction des paramètres depuis les demandes utilisateur
3. Pour les suppressions, demande toujours confirmation implicite
4. Si une information manque, demande-la à l'utilisateur
5. Réponds en français de manière claire et concise

Quand tu appelles un outil:
- Extrais correctement tous les paramètres nécessaires
- Utilise les valeurs par défaut appropriées
- Vérifie que les IDs sont des nombres entiers
"""
