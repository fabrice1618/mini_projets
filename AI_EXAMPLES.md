# Exemples de prompts pour l'assistant IA

Ce document liste des exemples de prompts testés et validés pour interagir avec l'assistant IA.

---

## 📋 Projets

### Création de projets

| Prompt | Résultat attendu |
|--------|------------------|
| `Crée un projet 'Stage entreprise'` | Nouveau projet créé avec ID |
| `Ajoute un nouveau projet 'Mémoire de fin d'études'` | Nouveau projet créé |
| `Crée un projet 'Recherche IA' avec la description 'Projet sur l'apprentissage automatique'` | Projet avec description |
| `Créer un projet fermé appelé 'Archives 2024'` | Projet avec statut fermé |

### Consultation de projets

| Prompt | Résultat attendu |
|--------|------------------|
| `Affiche les projets` | ✅ Liste tous les projets |
| `Quels sont mes projets ?` | ✅ Liste tous les projets |
| `Liste les projets ouverts` | ✅ Filtre par statut ouvert |
| `Liste les projets fermés` | ✅ Filtre par statut fermé |
| `Affiche les détails du projet 1` | Détails complets du projet |
| `Montre-moi le projet 3` | Détails du projet 3 |

⚠️ **Prompts moins fiables**:
- `Montre-moi tous les projets` (parfois répond textuellement)
- `Liste tous les projets` (parfois répond textuellement)

### Modification de projets

| Prompt | Résultat attendu |
|--------|------------------|
| `Change le titre du projet 1 en 'Nouveau titre'` | Titre mis à jour |
| `Modifie la description du projet 2 en 'Nouvelle description'` | Description mise à jour |
| `Ferme le projet 5` | Statut changé à 'fermé' |
| `Passe le projet 3 en statut ouvert` | Statut changé à 'ouvert' |
| `Modifie le projet 4 avec le titre 'Formation Python' et le statut fermé` | Titre et statut mis à jour |

### Suppression de projets

| Prompt | Résultat attendu |
|--------|------------------|
| `Supprime le projet 10` | Projet supprimé |
| `Efface le projet 15` | Projet supprimé |

---

## ✅ Tâches

### Création de tâches

#### Actions
| Prompt | Résultat attendu |
|--------|------------------|
| `Ajoute une action 'Rédiger introduction' dans le projet 1` | Action créée |
| `Crée une action 'Finaliser rapport' avec échéance au 2025-11-15 18:00:00 dans le projet 2` | Action avec échéance |
| `Créer une action 'Préparer présentation' à 50% d'avancement dans le projet 1` | Action avec avancement initial |

#### Réunions
| Prompt | Résultat attendu |
|--------|------------------|
| `Ajoute une réunion 'Point hebdomadaire' le 2025-11-01 14:00:00 dans le projet 1` | Réunion créée |
| `Crée une réunion 'Kickoff meeting' le 2025-11-05 10:00:00 pour 120 minutes dans le projet 2` | Réunion avec durée |
| `Créer une réunion 'Soutenance' le 2025-12-01 09:00:00 avec échéance au 2025-12-01 11:00:00 dans le projet 3` | Réunion avec date et échéance |

#### Cours
| Prompt | Résultat attendu |
|--------|------------------|
| `Ajoute un cours 'Introduction Python' le 2025-11-10 14:00:00 dans le projet 1` | Cours créé |
| `Crée un cours 'Base de données avancées' le 2025-11-15 08:00:00 pour 180 minutes dans le projet 2` | Cours avec durée |

### Consultation de tâches

| Prompt | Résultat attendu |
|--------|------------------|
| `Liste les tâches du projet 1` | Toutes les tâches du projet 1 |
| `Affiche les tâches du projet 2` | Toutes les tâches du projet 2 |
| `Montre-moi les prochaines tâches à venir` | ✅ 10 prochaines tâches (par défaut) |
| `Liste les 5 prochaines tâches` | 5 prochaines tâches |
| `Affiche toutes les réunions` | ✅ Filtre par type 'reunion' |
| `Liste toutes les actions` | ✅ Filtre par type 'action' |
| `Montre les cours` | ✅ Filtre par type 'cours' |
| `Affiche la tâche 5` | Détails de la tâche 5 |
| `Détails de la tâche 12` | Détails complets |

### Modification de tâches

| Prompt | Résultat attendu |
|--------|------------------|
| `Passe la tâche 5 à 75% d'avancement` | Avancement mis à jour |
| `Change l'échéance de la tâche 3 au 2025-11-20 18:00:00` | Échéance mise à jour |
| `Modifie le titre de la tâche 8 en 'Nouveau titre'` | Titre mis à jour |
| `Met la tâche 2 à 100%` | Avancement à 100% |
| `Change le type de la tâche 7 en reunion` | Type mis à jour |
| `Modifie la tâche 10 avec 30% d'avancement et échéance au 2025-12-01 12:00:00` | Plusieurs champs mis à jour |

### Suppression de tâches

| Prompt | Résultat attendu |
|--------|------------------|
| `Supprime la tâche 12` | Tâche supprimée |
| `Efface la tâche 20` | Tâche supprimée |

---

## 🔍 Recherches et requêtes complexes

### Recherches par statut/type

| Prompt | Résultat attendu |
|--------|------------------|
| `Affiche tous les projets ouverts` | ✅ Projets avec statut 'ouvert' |
| `Liste tous les projets fermés` | ✅ Projets avec statut 'fermé' |
| `Montre toutes les actions` | ✅ Tâches de type 'action' |
| `Affiche toutes les réunions` | ✅ Tâches de type 'reunion' |
| `Liste tous les cours` | ✅ Tâches de type 'cours' |

### Tâches à venir

| Prompt | Résultat attendu |
|--------|------------------|
| `Quelles sont mes prochaines tâches ?` | ✅ Liste des tâches à venir |
| `Montre les tâches à venir` | ✅ Liste triée par échéance |
| `Affiche les 10 prochaines échéances` | 10 tâches à venir |

### Questions générales

| Prompt | Résultat attendu |
|--------|------------------|
| `Combien j'ai de projets ?` | Compte des projets |
| `Quels sont mes projets ?` | ✅ Liste des projets |
| `Que dois-je faire cette semaine ?` | Tâches à venir |

---

## 💡 Astuces pour de meilleurs résultats

### ✅ Prompts qui fonctionnent bien

1. **Soyez direct et explicite**:
   - ✅ "Crée un projet 'Test'"
   - ✅ "Liste les projets"
   - ✅ "Affiche les tâches du projet 1"

2. **Utilisez des verbes d'action clairs**:
   - ✅ Crée, Ajoute, Créer
   - ✅ Liste, Affiche, Montre
   - ✅ Modifie, Change, Met à jour
   - ✅ Supprime, Efface

3. **Spécifiez les IDs quand nécessaire**:
   - ✅ "Modifie le projet 5"
   - ✅ "Supprime la tâche 12"

4. **Format de dates ISO recommandé**:
   - ✅ "2025-11-15 18:00:00"
   - ✅ "le 2025-11-15 à 18:00:00"

### ⚠️ Prompts moins fiables

1. **Trop vagues**:
   - ❌ "Fais quelque chose"
   - ❌ "Aide-moi"
   - ⚠️ "Montre-moi tout"

2. **Langage conversationnel**:
   - ⚠️ "Pourrais-tu me montrer les projets ?"
   - ⚠️ "J'aimerais voir mes tâches"
   - ✅ Mieux: "Affiche les projets" / "Liste les tâches"

3. **Références ambiguës**:
   - ❌ "Modifie ce projet" (quel projet ?)
   - ❌ "Supprime ça" (supprimer quoi ?)

---

## 🎯 Exemples d'utilisation réelle

### Scénario 1: Démarrer un nouveau projet de recherche

```
1. "Crée un projet 'Recherche Machine Learning' avec la description 'Projet de recherche sur les réseaux de neurones'"
2. "Ajoute une action 'Revue de littérature' dans le projet 1"
3. "Crée une action 'Collecte de données' avec échéance au 2025-12-01 18:00:00 dans le projet 1"
4. "Ajoute une réunion 'Point superviseur' le 2025-11-15 10:00:00 pour 60 minutes dans le projet 1"
5. "Liste les tâches du projet 1"
```

### Scénario 2: Organiser un cours

```
1. "Crée un projet 'Cours Python L3'"
2. "Ajoute un cours 'Introduction Python' le 2025-11-20 14:00:00 pour 120 minutes dans le projet 1"
3. "Crée un cours 'Fonctions et modules' le 2025-11-27 14:00:00 pour 120 minutes dans le projet 1"
4. "Ajoute une action 'Préparer exercices' avec échéance au 2025-11-19 18:00:00 dans le projet 1"
5. "Liste tous les cours"
```

### Scénario 3: Suivi de projet

```
1. "Affiche les projets ouverts"
2. "Liste les tâches du projet 2"
3. "Passe la tâche 5 à 50% d'avancement"
4. "Change l'échéance de la tâche 7 au 2025-12-10 12:00:00"
5. "Montre les prochaines tâches à venir"
```

### Scénario 4: Nettoyage et archivage

```
1. "Affiche tous les projets"
2. "Ferme le projet 3"
3. "Supprime la tâche 15"
4. "Liste les projets fermés"
```

---

## 📊 Statistiques de fiabilité

Basé sur les tests effectués:

| Type d'opération | Fiabilité | Note |
|-----------------|-----------|------|
| Création projet | 95% | ✅ Très fiable |
| Création tâche | 90% | ✅ Très fiable |
| Listing avec filtres | 85% | ✅ Fiable |
| Modification | 90% | ✅ Très fiable |
| Suppression | 90% | ✅ Très fiable |
| Listing général | 70% | ⚠️ Variable selon le prompt |
| Consultation détails | 85% | ✅ Fiable |

**Note**: Les variations de fiabilité dépendent principalement de la formulation du prompt. Les prompts directs et explicites ont une fiabilité proche de 100%.

---

## 🐛 Comportements observés

### Normal
- La première requête est plus lente (chargement du modèle)
- Certains prompts génèrent une réponse textuelle au lieu d'un tool call
- L'IA peut demander des clarifications si le prompt est ambigu

### À améliorer
- Les prompts avec "tous" ou "tout" sont parfois interprétés textuellement
- Les formulations conversationnelles sont moins fiables
- Les dates en langage naturel ("demain", "la semaine prochaine") ne fonctionnent pas encore

---

## 🚀 Pour aller plus loin

### Personnalisation du message système

Éditez `ai_config.py` pour adapter le comportement de l'IA:
```python
SYSTEM_MESSAGE = """Tu es un assistant IA pour la gestion de projets...
[Ajoutez vos propres instructions ici]
"""
```

### Ajout de nouveaux outils

1. Définir le tool dans `ai_tools.py`
2. Implémenter la fonction dans `projet_db.py` ou `tache_db.py`
3. Ajouter le mapping dans `execute_tool_call()` de `ai_assistant.py`

---

📅 Dernière mise à jour: 23 octobre 2025
🎯 Version: 1.0
🤖 Modèle: Llama 3.2 via Ollama
