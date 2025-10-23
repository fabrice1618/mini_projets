# 🚀 Démarrage Rapide - Assistant IA

## En 3 étapes

### 1️⃣ Vérifier qu'Ollama fonctionne

```bash
# Vérifier le service
sudo systemctl status ollama

# Si nécessaire, démarrer
sudo systemctl start ollama

# Tester
curl http://localhost:11434
# Devrait afficher: "Ollama is running"
```

### 2️⃣ Lancer l'application

```bash
python kanban_view_nice.py
```

L'application s'ouvre sur http://localhost:8080

### 3️⃣ Utiliser l'IA

1. Cliquez sur le bouton `►` dans l'en-tête
2. Le panneau IA s'ouvre
3. Tapez votre commande, par exemple:
   ```
   Crée un projet 'Mon nouveau projet'
   ```
4. Cliquez "Envoyer"
5. L'IA exécute l'action et affiche le résultat
6. L'interface se rafraîchit automatiquement

---

## 📝 Commandes de base

### Projets
```
Crée un projet 'Nom du projet'
Affiche les projets
Liste les projets ouverts
Modifie le projet 1 avec le titre 'Nouveau titre'
Ferme le projet 2
Supprime le projet 3
```

### Tâches
```
Ajoute une action 'Titre de la tâche' dans le projet 1
Crée une réunion 'Meeting' le 2025-11-15 10:00:00 dans le projet 1
Liste les tâches du projet 1
Passe la tâche 5 à 75% d'avancement
Montre les prochaines tâches à venir
Affiche toutes les réunions
```

---

## 🎬 Démonstration complète

Pour voir toutes les fonctionnalités:

```bash
python demo_ai.py
```

Ce script teste automatiquement toutes les opérations CRUD.

⏱️ **Durée**: ~5 minutes (pauses entre les requêtes pour ne pas surcharger Ollama)

---

## 📚 Documentation complète

- **Exemples détaillés**: `AI_EXAMPLES.md` - 50+ exemples de prompts
- **Guide complet**: `AI_INTEGRATION_COMPLETE.md` - Architecture et troubleshooting
- **Plan d'implémentation**: `implement_ia.md` - Détails techniques

---

## ⚠️ Problèmes courants

### "Erreur de connexion à Ollama"
```bash
sudo systemctl start ollama
```

### L'IA ne répond pas correctement
Reformulez de manière plus directe:
- ❌ "Pourrais-tu me montrer les projets ?"
- ✅ "Affiche les projets"

### Réponses lentes
Normal pour la première requête (chargement du modèle).
Les suivantes sont plus rapides.

---

## 📁 Fichiers créés

```
✅ ai_config.py          - Configuration
✅ ai_tools.py           - Définition des 12 outils
✅ ai_assistant.py       - Module principal
✅ kanban_view_nice.py   - Interface (modifiée)
✅ demo_ai.py            - Script de démonstration
```

---

## ✨ C'est tout !

Vous êtes prêt à utiliser l'assistant IA.

**Bon usage ! 🎉**
