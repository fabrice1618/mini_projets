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
            # Vérifier si c'est un projet complet ou juste un ID
            if "titre" in data:
                message += f"\n\n**Détails:**\n"
                message += f"  • Titre: {data['titre']}\n"
                message += f"  • Statut: {data['statut']}\n"
                if data.get('description'):
                    message += f"  • Description: {data['description']}\n"
            # Sinon c'est juste un retour de création avec l'ID

        # Formater une tâche unique
        elif isinstance(data, dict) and "tache_id" in data:
            # Vérifier si c'est une tâche complète ou juste un ID
            if "titre" in data:
                message += f"\n\n**Détails:**\n"
                message += f"  • Titre: {data['titre']}\n"
                message += f"  • Type: {data['type']}\n"
                message += f"  • Avancement: {data['avancement']}%\n"
                if data.get('echeance_absolue'):
                    message += f"  • Échéance: {data['echeance_absolue']}\n"
                if data.get('description_resumee'):
                    message += f"  • Description: {data['description_resumee']}\n"
            # Sinon c'est juste un retour de création avec l'ID

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
                # Gérer les différents formats possibles de tool_call
                if hasattr(tool_call, 'function'):
                    # Format objet
                    tool_name = tool_call.function.name
                    arguments = tool_call.function.arguments
                elif isinstance(tool_call, dict):
                    # Format dict
                    tool_name = tool_call["function"]["name"]
                    arguments = tool_call["function"]["arguments"]
                else:
                    # Format inconnu, essayer d'extraire
                    tool_name = str(tool_call.get("function", {}).get("name", ""))
                    arguments = tool_call.get("function", {}).get("arguments", {})

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
        import traceback
        error_details = traceback.format_exc()
        return {
            "message": f"❌ Erreur lors du traitement de la requête: {str(e)}\n\nDétails:\n{error_details}",
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
