# Plan d'implémentation - Intégration IA avec Ollama

## Vue d'ensemble

Ce document détaille l'implémentation de l'intégration IA dans l'application de gestion de projets en utilisant Ollama et le function calling.

### Architecture de l'intégration

```
┌─────────────────────────────────────────────────────────────────────┐
│                   Application (kanban_view_nice.py)                 │
│                                                                      │
│  Utilisateur → Panneau IA → ai_assistant.py → Ollama (Llama 3.2)   │
│                                     ↓                                │
│                              execute_tool_call()                     │
│                                     ↓                                │
│                    ┌────────────────┴────────────────┐              │
│                    ↓                                 ↓              │
│              projet_db.py                       tache_db.py         │
│                    ↓                                 ↓              │
│                         database.db (SQLite)                         │
└─────────────────────────────────────────────────────────────────────┘
```

### Flux de traitement d'une requête

1. **Utilisateur** saisit un prompt : "Crée un projet 'Stage entreprise'"
2. **ai_assistant.process_user_request()** envoie le prompt + liste des tools à Ollama
3. **Ollama** analyse et retourne un appel de fonction structuré
4. **ai_assistant.execute_tool_call()** exécute la fonction correspondante
5. **Résultat** affiché dans le panneau IA et interface rafraîchie

---

## Fichiers à créer

### 1. `ai_config.py` - Configuration Ollama

**Objectif**: Centraliser la configuration du service Ollama

```python
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
```

**Emplacement**: `/home/fab/projet/BACHINGE24_annee2/mini_projets/ai_config.py`

---

### 2. `ai_tools.py` - Définition des tools

**Objectif**: Définir tous les outils (tools) disponibles pour Ollama avec leurs schémas JSON

```python
"""
Définition des tools disponibles pour l'IA (function calling)
Chaque tool correspond à une opération CRUD sur projets ou tâches
"""

# Liste complète des tools avec leurs schémas JSON pour Ollama
TOOLS = [
    # ==================== PROJETS ====================
    {
        "type": "function",
        "function": {
            "name": "creer_projet",
            "description": "Crée un nouveau projet dans la base de données",
            "parameters": {
                "type": "object",
                "properties": {
                    "titre": {
                        "type": "string",
                        "description": "Titre du projet (obligatoire)"
                    },
                    "description": {
                        "type": "string",
                        "description": "Description détaillée du projet (optionnel)"
                    },
                    "statut": {
                        "type": "string",
                        "enum": ["ouvert", "ferme"],
                        "description": "Statut du projet (défaut: 'ouvert')"
                    }
                },
                "required": ["titre"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "lire_projet",
            "description": "Récupère les informations détaillées d'un projet spécifique",
            "parameters": {
                "type": "object",
                "properties": {
                    "projet_id": {
                        "type": "integer",
                        "description": "ID du projet à consulter"
                    }
                },
                "required": ["projet_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "modifier_projet",
            "description": "Modifie un projet existant (titre, description ou statut)",
            "parameters": {
                "type": "object",
                "properties": {
                    "projet_id": {
                        "type": "integer",
                        "description": "ID du projet à modifier"
                    },
                    "titre": {
                        "type": "string",
                        "description": "Nouveau titre du projet (optionnel)"
                    },
                    "description": {
                        "type": "string",
                        "description": "Nouvelle description (optionnel)"
                    },
                    "statut": {
                        "type": "string",
                        "enum": ["ouvert", "ferme"],
                        "description": "Nouveau statut (optionnel)"
                    }
                },
                "required": ["projet_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "supprimer_projet",
            "description": "Supprime un projet de la base de données (ATTENTION: action irréversible)",
            "parameters": {
                "type": "object",
                "properties": {
                    "projet_id": {
                        "type": "integer",
                        "description": "ID du projet à supprimer"
                    }
                },
                "required": ["projet_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "lister_projets",
            "description": "Liste tous les projets ou filtre par statut (ouvert/fermé)",
            "parameters": {
                "type": "object",
                "properties": {
                    "statut": {
                        "type": "string",
                        "enum": ["ouvert", "ferme"],
                        "description": "Filtre par statut (optionnel, si absent retourne tous les projets)"
                    }
                },
                "required": []
            }
        }
    },

    # ==================== TÂCHES ====================
    {
        "type": "function",
        "function": {
            "name": "creer_tache",
            "description": "Crée une nouvelle tâche dans un projet",
            "parameters": {
                "type": "object",
                "properties": {
                    "projet_id": {
                        "type": "integer",
                        "description": "ID du projet parent"
                    },
                    "type_tache": {
                        "type": "string",
                        "enum": ["cours", "reunion", "action"],
                        "description": "Type de tâche: cours, reunion ou action"
                    },
                    "titre": {
                        "type": "string",
                        "description": "Titre de la tâche"
                    },
                    "description_resumee": {
                        "type": "string",
                        "description": "Description courte de la tâche (optionnel)"
                    },
                    "date_heure": {
                        "type": "string",
                        "description": "Date et heure de début au format ISO (YYYY-MM-DD HH:MM:SS) (optionnel)"
                    },
                    "duree_minutes": {
                        "type": "integer",
                        "description": "Durée en minutes (optionnel, surtout pour cours/réunions)"
                    },
                    "echeance_absolue": {
                        "type": "string",
                        "description": "Échéance absolue au format ISO (YYYY-MM-DD HH:MM:SS) (optionnel)"
                    },
                    "avancement": {
                        "type": "integer",
                        "description": "Pourcentage d'avancement 0-100 (défaut: 0)"
                    }
                },
                "required": ["projet_id", "type_tache", "titre"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "lire_tache",
            "description": "Récupère les informations détaillées d'une tâche spécifique",
            "parameters": {
                "type": "object",
                "properties": {
                    "tache_id": {
                        "type": "integer",
                        "description": "ID de la tâche à consulter"
                    }
                },
                "required": ["tache_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "modifier_tache",
            "description": "Modifie une tâche existante (tous les champs sont optionnels)",
            "parameters": {
                "type": "object",
                "properties": {
                    "tache_id": {
                        "type": "integer",
                        "description": "ID de la tâche à modifier"
                    },
                    "type_tache": {
                        "type": "string",
                        "enum": ["cours", "reunion", "action"],
                        "description": "Nouveau type de tâche (optionnel)"
                    },
                    "titre": {
                        "type": "string",
                        "description": "Nouveau titre (optionnel)"
                    },
                    "description_resumee": {
                        "type": "string",
                        "description": "Nouvelle description (optionnel)"
                    },
                    "date_heure": {
                        "type": "string",
                        "description": "Nouvelle date/heure au format ISO (optionnel)"
                    },
                    "duree_minutes": {
                        "type": "integer",
                        "description": "Nouvelle durée en minutes (optionnel)"
                    },
                    "echeance_absolue": {
                        "type": "string",
                        "description": "Nouvelle échéance au format ISO (optionnel)"
                    },
                    "avancement": {
                        "type": "integer",
                        "description": "Nouveau pourcentage d'avancement 0-100 (optionnel)"
                    }
                },
                "required": ["tache_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "supprimer_tache",
            "description": "Supprime une tâche de la base de données (ATTENTION: action irréversible)",
            "parameters": {
                "type": "object",
                "properties": {
                    "tache_id": {
                        "type": "integer",
                        "description": "ID de la tâche à supprimer"
                    }
                },
                "required": ["tache_id"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "lister_taches",
            "description": "Liste les tâches avec filtres optionnels par projet et/ou type",
            "parameters": {
                "type": "object",
                "properties": {
                    "projet_id": {
                        "type": "integer",
                        "description": "Filtre par projet (optionnel)"
                    },
                    "type_tache": {
                        "type": "string",
                        "enum": ["cours", "reunion", "action"],
                        "description": "Filtre par type (optionnel)"
                    }
                },
                "required": []
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "lister_taches_a_venir",
            "description": "Liste les prochaines tâches à réaliser (triées par échéance)",
            "parameters": {
                "type": "object",
                "properties": {
                    "limite": {
                        "type": "integer",
                        "description": "Nombre maximum de tâches à retourner (défaut: 10)"
                    }
                },
                "required": []
            }
        }
    }
]


def get_tool_by_name(tool_name):
    """Retourne le schéma d'un tool par son nom"""
    for tool in TOOLS:
        if tool["function"]["name"] == tool_name:
            return tool
    return None


def get_all_tool_names():
    """Retourne la liste de tous les noms de tools disponibles"""
    return [tool["function"]["name"] for tool in TOOLS]
```

**Emplacement**: `/home/fab/projet/BACHINGE24_annee2/mini_projets/ai_tools.py`

---

### 3. `ai_assistant.py` - Module principal

**Objectif**: Orchestrer les interactions avec Ollama et exécuter les function calls

```python
"""
Module principal d'interaction avec l'IA Ollama
Gère le function calling et l'exécution des tools
"""

import json
import ollama
from datetime import datetime

# Imports locaux
from ai_config import (
    OLLAMA_MODEL,
    OLLAMA_HOST,
    GENERATION_PARAMS,
    TIMEOUT_SECONDS,
    SYSTEM_MESSAGE
)
from ai_tools import TOOLS, get_tool_by_name, get_all_tool_names
from database import ouvrir_database
import projet_db
import tache_db


class AIAssistantError(Exception):
    """Exception personnalisée pour les erreurs de l'assistant IA"""
    pass


def execute_tool_call(tool_name, arguments):
    """
    Exécute un appel de fonction (tool call) en mappant vers les fonctions DB

    Args:
        tool_name (str): Nom du tool à exécuter
        arguments (dict): Arguments pour le tool

    Returns:
        dict: Résultat de l'exécution avec 'success', 'message', et optionnellement 'data'
    """
    try:
        # Ouvrir la connexion DB
        conn, cursor = ouvrir_database()

        result = {
            "success": False,
            "message": "",
            "data": None,
            "modified": False  # Indique si la DB a été modifiée
        }

        # ==================== PROJETS ====================

        if tool_name == "creer_projet":
            projet_id = projet_db.creer_projet(
                conn, cursor,
                titre=arguments.get("titre"),
                description=arguments.get("description"),
                statut=arguments.get("statut", "ouvert")
            )
            result["success"] = True
            result["message"] = f"✅ Projet '{arguments.get('titre')}' créé avec succès (ID: {projet_id})"
            result["data"] = {"projet_id": projet_id}
            result["modified"] = True

        elif tool_name == "lire_projet":
            projet = projet_db.lire_projet(conn, cursor, arguments.get("projet_id"))
            if projet:
                result["success"] = True
                result["message"] = f"📋 Projet trouvé: {projet['titre']}"
                result["data"] = projet
            else:
                result["success"] = False
                result["message"] = f"❌ Projet ID {arguments.get('projet_id')} non trouvé"

        elif tool_name == "modifier_projet":
            success = projet_db.modifier_projet(
                conn, cursor,
                projet_id=arguments.get("projet_id"),
                titre=arguments.get("titre"),
                description=arguments.get("description"),
                statut=arguments.get("statut")
            )
            if success:
                result["success"] = True
                result["message"] = f"✅ Projet ID {arguments.get('projet_id')} modifié avec succès"
                result["modified"] = True
            else:
                result["success"] = False
                result["message"] = f"❌ Impossible de modifier le projet ID {arguments.get('projet_id')}"

        elif tool_name == "supprimer_projet":
            success = projet_db.supprimer_projet(conn, cursor, arguments.get("projet_id"))
            if success:
                result["success"] = True
                result["message"] = f"🗑️ Projet ID {arguments.get('projet_id')} supprimé"
                result["modified"] = True
            else:
                result["success"] = False
                result["message"] = f"❌ Impossible de supprimer le projet ID {arguments.get('projet_id')}"

        elif tool_name == "lister_projets":
            projets = projet_db.lister_projets(
                conn, cursor,
                statut=arguments.get("statut")
            )
            result["success"] = True
            if projets:
                result["message"] = f"📋 {len(projets)} projet(s) trouvé(s)"
                result["data"] = projets
            else:
                result["message"] = "Aucun projet trouvé"
                result["data"] = []

        # ==================== TÂCHES ====================

        elif tool_name == "creer_tache":
            tache_id = tache_db.creer_tache(
                conn, cursor,
                projet_id=arguments.get("projet_id"),
                type_tache=arguments.get("type_tache"),
                titre=arguments.get("titre"),
                description_resumee=arguments.get("description_resumee"),
                date_heure=arguments.get("date_heure"),
                duree_minutes=arguments.get("duree_minutes"),
                echeance_absolue=arguments.get("echeance_absolue"),
                avancement=arguments.get("avancement", 0)
            )
            result["success"] = True
            result["message"] = f"✅ Tâche '{arguments.get('titre')}' créée avec succès (ID: {tache_id})"
            result["data"] = {"tache_id": tache_id}
            result["modified"] = True

        elif tool_name == "lire_tache":
            tache = tache_db.lire_tache(conn, cursor, arguments.get("tache_id"))
            if tache:
                result["success"] = True
                result["message"] = f"📋 Tâche trouvée: {tache['titre']}"
                result["data"] = tache
            else:
                result["success"] = False
                result["message"] = f"❌ Tâche ID {arguments.get('tache_id')} non trouvée"

        elif tool_name == "modifier_tache":
            success = tache_db.modifier_tache(
                conn, cursor,
                tache_id=arguments.get("tache_id"),
                type_tache=arguments.get("type_tache"),
                titre=arguments.get("titre"),
                description_resumee=arguments.get("description_resumee"),
                date_heure=arguments.get("date_heure"),
                duree_minutes=arguments.get("duree_minutes"),
                echeance_absolue=arguments.get("echeance_absolue"),
                avancement=arguments.get("avancement")
            )
            if success:
                result["success"] = True
                result["message"] = f"✅ Tâche ID {arguments.get('tache_id')} modifiée avec succès"
                result["modified"] = True
            else:
                result["success"] = False
                result["message"] = f"❌ Impossible de modifier la tâche ID {arguments.get('tache_id')}"

        elif tool_name == "supprimer_tache":
            success = tache_db.supprimer_tache(conn, cursor, arguments.get("tache_id"))
            if success:
                result["success"] = True
                result["message"] = f"🗑️ Tâche ID {arguments.get('tache_id')} supprimée"
                result["modified"] = True
            else:
                result["success"] = False
                result["message"] = f"❌ Impossible de supprimer la tâche ID {arguments.get('tache_id')}"

        elif tool_name == "lister_taches":
            taches = tache_db.lister_taches(
                conn, cursor,
                projet_id=arguments.get("projet_id"),
                type_tache=arguments.get("type_tache")
            )
            result["success"] = True
            if taches:
                result["message"] = f"📋 {len(taches)} tâche(s) trouvée(s)"
                result["data"] = taches
            else:
                result["message"] = "Aucune tâche trouvée"
                result["data"] = []

        elif tool_name == "lister_taches_a_venir":
            limite = arguments.get("limite", 10)
            taches = tache_db.lister_taches_a_venir(conn, cursor, limite=limite)
            result["success"] = True
            if taches:
                result["message"] = f"📋 {len(taches)} tâche(s) à venir"
                result["data"] = taches
            else:
                result["message"] = "Aucune tâche à venir"
                result["data"] = []

        else:
            raise AIAssistantError(f"Tool inconnu: {tool_name}")

        # Fermer la connexion
        conn.close()

        return result

    except Exception as e:
        return {
            "success": False,
            "message": f"❌ Erreur lors de l'exécution de {tool_name}: {str(e)}",
            "data": None,
            "modified": False
        }


def format_result_for_display(result):
    """
    Formate le résultat pour affichage dans l'interface

    Args:
        result (dict): Résultat de execute_tool_call

    Returns:
        str: Message formaté pour l'utilisateur
    """
    message = result["message"]

    # Ajouter les données si disponibles
    if result.get("data"):
        data = result["data"]

        # Formater les projets
        if isinstance(data, list) and len(data) > 0 and "projet_id" in data[0]:
            message += "\n\n**Projets:**\n"
            for projet in data[:5]:  # Limiter à 5 pour l'affichage
                message += f"  • [{projet['projet_id']}] {projet['titre']} - {projet['statut']}\n"
            if len(data) > 5:
                message += f"  ... et {len(data) - 5} autre(s)\n"

        # Formater les tâches
        elif isinstance(data, list) and len(data) > 0 and "tache_id" in data[0]:
            message += "\n\n**Tâches:**\n"
            for tache in data[:5]:  # Limiter à 5 pour l'affichage
                echeance = tache.get('echeance_absolue', 'Non définie')
                message += f"  • [{tache['tache_id']}] {tache['titre']} ({tache['type']}) - {tache['avancement']}%\n"
                if echeance != 'Non définie':
                    message += f"    Échéance: {echeance}\n"
            if len(data) > 5:
                message += f"  ... et {len(data) - 5} autre(s)\n"

        # Formater un projet unique
        elif isinstance(data, dict) and "projet_id" in data:
            message += f"\n\n**Détails:**\n"
            message += f"  • Titre: {data['titre']}\n"
            message += f"  • Statut: {data['statut']}\n"
            if data.get('description'):
                message += f"  • Description: {data['description']}\n"

        # Formater une tâche unique
        elif isinstance(data, dict) and "tache_id" in data:
            message += f"\n\n**Détails:**\n"
            message += f"  • Titre: {data['titre']}\n"
            message += f"  • Type: {data['type']}\n"
            message += f"  • Avancement: {data['avancement']}%\n"
            if data.get('echeance_absolue'):
                message += f"  • Échéance: {data['echeance_absolue']}\n"
            if data.get('description_resumee'):
                message += f"  • Description: {data['description_resumee']}\n"

    return message


def process_user_request(user_prompt):
    """
    Point d'entrée principal pour traiter une requête utilisateur

    Args:
        user_prompt (str): Prompt de l'utilisateur

    Returns:
        dict: Résultat avec 'message' (str) et 'modified' (bool)
    """
    try:
        # Préparer les messages pour Ollama
        messages = [
            {
                "role": "system",
                "content": SYSTEM_MESSAGE
            },
            {
                "role": "user",
                "content": user_prompt
            }
        ]

        # Appeler Ollama avec les tools
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=messages,
            tools=TOOLS,
            options={
                "temperature": GENERATION_PARAMS["temperature"],
                "top_p": GENERATION_PARAMS["top_p"],
                "top_k": GENERATION_PARAMS["top_k"],
            }
        )

        # Vérifier si l'IA a décidé d'appeler un tool
        if response.get("message") and response["message"].get("tool_calls"):
            tool_calls = response["message"]["tool_calls"]

            # Traiter chaque tool call (normalement il y en a un seul)
            results = []
            modified = False

            for tool_call in tool_calls:
                tool_name = tool_call["function"]["name"]
                arguments = tool_call["function"]["arguments"]

                # Exécuter le tool
                result = execute_tool_call(tool_name, arguments)
                results.append(result)

                if result["modified"]:
                    modified = True

            # Formater le résultat final
            if len(results) == 1:
                final_message = format_result_for_display(results[0])
            else:
                final_message = "\n\n".join([format_result_for_display(r) for r in results])

            return {
                "message": final_message,
                "modified": modified
            }

        # Si pas de tool call, retourner la réponse textuelle de l'IA
        else:
            ai_message = response["message"]["content"]
            return {
                "message": f"💬 {ai_message}",
                "modified": False
            }

    except Exception as e:
        return {
            "message": f"❌ Erreur lors du traitement de la requête: {str(e)}",
            "modified": False
        }


def test_connection():
    """
    Test de connexion à Ollama

    Returns:
        bool: True si la connexion fonctionne
    """
    try:
        # Tester avec un simple prompt
        response = ollama.chat(
            model=OLLAMA_MODEL,
            messages=[{"role": "user", "content": "Dis bonjour"}]
        )
        return True
    except Exception as e:
        print(f"Erreur de connexion à Ollama: {e}")
        return False


# Pour les tests en ligne de commande
if __name__ == "__main__":
    print("=== Test de l'assistant IA ===\n")

    # Test de connexion
    print("1. Test de connexion à Ollama...")
    if test_connection():
        print("   ✅ Connexion OK\n")
    else:
        print("   ❌ Connexion échouée\n")
        exit(1)

    # Test d'un prompt simple
    print("2. Test de création de projet...")
    result = process_user_request("Crée un projet 'Test IA' avec la description 'Projet de test'")
    print(f"   {result['message']}\n")

    print("3. Test de listing des projets...")
    result = process_user_request("Montre-moi tous les projets")
    print(f"   {result['message']}\n")
```

**Emplacement**: `/home/fab/projet/BACHINGE24_annee2/mini_projets/ai_assistant.py`

---

## Modifications des fichiers existants

### 1. `kanban_view_nice.py` - Intégration du panneau IA

**Localisation**: Fonction `send_prompt()` (ligne 208-216)

**Modification à effectuer**:

```python
# AVANT (lignes 208-216)
def send_prompt():
    """Envoie le prompt à l'IA (placeholder pour l'instant)"""
    user_prompt = prompt_input.value
    if user_prompt.strip():
        # Placeholder - à remplacer par l'appel réel à l'IA
        ai_response['text'] += f"\n\n> Vous: {user_prompt}\n\nIA: Réponse simulée pour '{user_prompt}'\n"
        response_area.set_text(ai_response['text'])
        prompt_input.value = ''

# APRÈS
def send_prompt():
    """Envoie le prompt à l'IA"""
    user_prompt = prompt_input.value
    if user_prompt.strip():
        # Importer le module AI assistant
        from ai_assistant import process_user_request

        # Appeler l'IA
        result = process_user_request(user_prompt)

        # Afficher le résultat
        ai_response['text'] += f"\n\n> Vous: {user_prompt}\n\n{result['message']}\n"
        response_area.set_text(ai_response['text'])

        # Rafraîchir l'affichage si modification de la DB
        if result['modified']:
            refresh_kanban()

        prompt_input.value = ''
```

**Alternative (import en haut du fichier)**:

```python
# En haut du fichier kanban_view_nice.py, après les autres imports
from ai_assistant import process_user_request

# Puis dans send_prompt():
def send_prompt():
    """Envoie le prompt à l'IA"""
    user_prompt = prompt_input.value
    if user_prompt.strip():
        # Appeler l'IA
        result = process_user_request(user_prompt)

        # Afficher le résultat
        ai_response['text'] += f"\n\n> Vous: {user_prompt}\n\n{result['message']}\n"
        response_area.set_text(ai_response['text'])

        # Rafraîchir l'affichage si modification de la DB
        if result['modified']:
            refresh_kanban()

        prompt_input.value = ''
```

---

### 2. `requirements.txt` - Ajout de la dépendance

**Ajouter cette ligne**:

```
ollama>=0.1.0
```

**Fichier complet (probable)**:

```
nicegui>=1.4.0
ollama>=0.1.0
```

---

## Installation et configuration

### 1. Vérifier qu'Ollama fonctionne

```bash
# Test de connexion
curl http://localhost:11434

# Devrait retourner: "Ollama is running"

# Vérifier le modèle
ollama list

# Devrait afficher llama3.2
```

### 2. Installer la dépendance Python

```bash
# Activer l'environnement virtuel (si utilisé)
source venv/bin/activate

# Installer ollama
pip install ollama

# Ou depuis requirements.txt
pip install -r requirements.txt
```

### 3. Tester l'assistant en mode CLI

```bash
# Test de l'assistant
python ai_assistant.py
```

**Sortie attendue**:

```
=== Test de l'assistant IA ===

1. Test de connexion à Ollama...
   ✅ Connexion OK

2. Test de création de projet...
   ✅ Projet 'Test IA' créé avec succès (ID: X)

3. Test de listing des projets...
   📋 X projet(s) trouvé(s)

   **Projets:**
     • [1] Projet existant - ouvert
     • [X] Test IA - ouvert
```

---

## Exemples de prompts utilisateur

### Projets

#### Création
- "Crée un projet 'Stage entreprise'"
- "Ajoute un nouveau projet 'Mémoire de fin d'études' avec la description 'Recherche sur l'IA'"
- "Créer un projet fermé appelé 'Archives 2024'"

#### Consultation
- "Montre-moi tous les projets"
- "Liste les projets ouverts"
- "Affiche les détails du projet 3"
- "Quels sont mes projets fermés ?"

#### Modification
- "Change le titre du projet 1 en 'Nouveau titre'"
- "Modifie la description du projet 2"
- "Ferme le projet 5"
- "Passe le projet 'Stage' en statut fermé"

#### Suppression
- "Supprime le projet 10"
- "Efface le projet 'Test'"

### Tâches

#### Création
- "Ajoute une action 'Rédiger introduction' dans le projet 1"
- "Crée une réunion 'Point hebdomadaire' le 25 octobre 2025 à 14h dans le projet 2"
- "Nouvelle tâche de type cours 'Cours IA' le 30 octobre à 10h pour 2 heures dans le projet 1"
- "Ajoute une action 'Finaliser rapport' avec échéance au 15 novembre 2025 dans le projet 3"

#### Consultation
- "Liste toutes les tâches du projet 1"
- "Montre-moi les réunions"
- "Affiche les 5 prochaines tâches à venir"
- "Quelles sont mes tâches en retard ?"
- "Détails de la tâche 7"

#### Modification
- "Passe la tâche 5 à 75% d'avancement"
- "Change l'échéance de la tâche 3 au 20 novembre 2025"
- "Modifie le titre de la tâche 8 en 'Nouveau titre'"
- "Met la tâche 2 à 100%"

#### Suppression
- "Supprime la tâche 12"
- "Efface la tâche 'Test'"

### Recherches et requêtes complexes

- "Montre-moi toutes les tâches urgentes"
- "Liste les actions du projet 'Stage'"
- "Quelles tâches sont à moins de 50% d'avancement ?"
- "Affiche les prochaines réunions de la semaine"
- "Combien de projets ouverts j'ai ?"

---

## Tests de validation

### Phase 1: Tests de base

```bash
# 1. Test de connexion Ollama
curl http://localhost:11434

# 2. Test du module AI assistant
python ai_assistant.py

# 3. Lancer l'application
python kanban_view_nice.py
```

### Phase 2: Tests fonctionnels dans l'interface

**Test Projets**:
1. ✅ Créer un projet via prompt
2. ✅ Lister tous les projets
3. ✅ Modifier un projet
4. ✅ Supprimer un projet

**Test Tâches**:
1. ✅ Créer une action
2. ✅ Créer une réunion avec date/heure
3. ✅ Modifier l'avancement d'une tâche
4. ✅ Lister les tâches d'un projet
5. ✅ Supprimer une tâche

**Test Interface**:
1. ✅ Le panneau IA s'ouvre/ferme correctement
2. ✅ Les réponses s'affichent dans la zone de texte
3. ✅ L'interface se rafraîchit après modifications
4. ✅ Les erreurs sont affichées clairement

### Phase 3: Tests de robustesse

**Gestion d'erreurs**:
- Prompt avec ID inexistant
- Prompt ambigu ou incomplet
- Requête sans les informations nécessaires

**Exemples de prompts à tester**:
```
"Supprime le projet 999"  → Devrait retourner une erreur
"Modifie le projet"        → IA devrait demander quel projet
"Crée une tâche"          → IA devrait demander dans quel projet
```

---

## Dépannage

### Problème: "Ollama is not running"

**Solution**:
```bash
sudo systemctl start ollama
# ou
sudo systemctl restart ollama
```

### Problème: "Model not found"

**Solution**:
```bash
ollama pull llama3.2
```

### Problème: "Module 'ollama' not found"

**Solution**:
```bash
pip install ollama
```

### Problème: Réponses lentes

**Causes possibles**:
- RAM insuffisante → Utiliser `llama3.2:1b` (plus léger)
- Modèle non chargé en cache → La première requête est toujours plus lente

**Solution**:
```bash
# Précharger le modèle
ollama run llama3.2
# Tapez /bye pour quitter mais le modèle reste en mémoire
```

### Problème: L'IA ne comprend pas certaines requêtes

**Solutions**:
1. Être plus explicite dans le prompt
2. Utiliser des verbes d'action clairs: "crée", "liste", "modifie", "supprime"
3. Spécifier les IDs quand nécessaire
4. Ajuster `SYSTEM_MESSAGE` dans `ai_config.py` pour mieux guider l'IA

---

## Améliorations futures (optionnelles)

### 1. Historique des conversations

Ajouter un système de mémorisation des échanges pour permettre des requêtes contextuelles:
- "Ajoute une tâche dans ce projet" (en référence au dernier projet mentionné)

### 2. Confirmations pour actions critiques

Implémenter une confirmation utilisateur avant suppression:
```python
# Dans send_prompt()
if "supprimer" in result.get("action_type", ""):
    # Afficher un dialogue de confirmation
    pass
```

### 3. Templates de prompts

Ajouter des boutons avec des prompts pré-remplis:
- "Mes tâches urgentes"
- "Créer un nouveau projet"
- "Vue d'ensemble"

### 4. Export et rapports

Ajouter un tool pour générer des rapports:
```python
"generer_rapport_projet": Génère un rapport détaillé d'un projet
```

### 5. Recherche sémantique

Implémenter une recherche intelligente dans les descriptions:
```python
"rechercher": Recherche dans tous les titres et descriptions
```

---

## Ressources

### Documentation officielle
- **Ollama**: https://ollama.com
- **Ollama Python**: https://github.com/ollama/ollama-python
- **Llama 3.2**: https://ollama.com/library/llama3.2

### Tutoriels
- Function calling avec Ollama: https://github.com/ollama/ollama/blob/main/docs/api.md#tools
- NiceGUI documentation: https://nicegui.io

### Aide
Pour toute question ou problème, consulter:
- Issues Ollama: https://github.com/ollama/ollama/issues
- Documentation du projet dans `CLAUDE.md`
- Spécifications dans `spec_integration_ia.md`

---

## Checklist d'implémentation

**Préparation** (Fait ✅):
- [x] Ollama installé
- [x] Modèle llama3.2 téléchargé
- [x] Client Python ollama installé

**Implémentation**:
- [ ] Créer `ai_config.py`
- [ ] Créer `ai_tools.py`
- [ ] Créer `ai_assistant.py`
- [ ] Modifier `kanban_view_nice.py` (fonction `send_prompt`)
- [ ] Ajouter `ollama>=0.1.0` à `requirements.txt`

**Tests**:
- [ ] Tester `ai_assistant.py` en CLI
- [ ] Tester création de projets via IA
- [ ] Tester création de tâches via IA
- [ ] Tester modifications via IA
- [ ] Tester suppressions via IA
- [ ] Tester recherches et listings
- [ ] Valider le rafraîchissement de l'interface

**Documentation**:
- [ ] Créer `AI_EXAMPLES.md` avec exemples de prompts
- [ ] Mettre à jour `README.md` avec section IA
- [ ] Documenter les prompts qui fonctionnent bien

---

## Conclusion

Cette implémentation fournit une intégration complète de l'IA dans votre application de gestion de projets. Les 3 nouveaux fichiers (`ai_config.py`, `ai_tools.py`, `ai_assistant.py`) encapsulent toute la logique IA, rendant le système:

- **Modulaire**: Chaque composant a une responsabilité claire
- **Maintenable**: Code bien structuré et commenté
- **Extensible**: Facile d'ajouter de nouveaux tools
- **Robuste**: Gestion d'erreurs complète
- **Pédagogique**: Code clair pour apprentissage étudiant

L'intégration dans `kanban_view_nice.py` est minimale (quelques lignes), préservant la structure existante de votre application.

**Prochaines étapes**: Suivre la checklist d'implémentation ci-dessus dans l'ordre.
