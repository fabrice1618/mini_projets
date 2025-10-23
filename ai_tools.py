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
