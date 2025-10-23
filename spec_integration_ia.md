# Spécifications : Intégration IA pour la gestion de projets et tâches

## Contexte

Permettre aux utilisateurs de gérer leurs projets et tâches via des commandes en langage naturel. L'IA interprète les demandes et exécute les modifications dans la base de données via un système de function calling.

## Solution recommandée pour étudiants (gratuite)

### Approche : Function Calling avec Ollama

Cette solution utilise le **function calling** (appel de fonctions), une technique où l'IA peut décider d'appeler des fonctions Python pour effectuer des actions concrètes (comme modifier la base de données).

#### Schéma de l'architecture

```
┌────────────────────────────────────────────────────────────────────┐
│                    Application NiceGUI (kanban_view_nice.py)        │
│                                                                     │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Interface utilisateur (Panneau prompt IA)                    │  │
│  │  - L'utilisateur saisit : "Crée un projet 'Stage entreprise'" │  │
│  └────────────────────────┬─────────────────────────────────────┘  │
│                           │                                         │
│                           ▼                                         │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  ai_assistant.py                                              │  │
│  │  ┌────────────────────────────────────────────────────────┐  │  │
│  │  │ 1. process_user_request(prompt)                         │  │  │
│  │  │    - Reçoit le prompt de l'utilisateur                  │  │  │
│  │  │    - Envoie à Ollama avec liste des tools disponibles   │  │  │
│  │  └────────────────────────────────────────────────────────┘  │  │
│  │                           │                                   │  │
│  │                           ▼                                   │  │
│  │  ┌────────────────────────────────────────────────────────┐  │  │
│  │  │ Ollama (LLM local - Llama 3.2)                          │  │  │
│  │  │ - Comprend : "je dois créer un projet"                  │  │  │
│  │  │ - Décide d'appeler : creer_projet("Stage entreprise")   │  │  │
│  │  │ - Retourne : {"tool": "creer_projet",                   │  │  │
│  │  │               "args": {"titre": "Stage entreprise"}}    │  │  │
│  │  └────────────────────────────────────────────────────────┘  │  │
│  │                           │                                   │  │
│  │                           ▼                                   │  │
│  │  ┌────────────────────────────────────────────────────────┐  │  │
│  │  │ 2. execute_tool_call(tool_name, arguments)              │  │  │
│  │  │    - Reçoit la décision de l'IA                         │  │  │
│  │  │    - Appelle la fonction Python correspondante          │  │  │
│  │  └────────────────────────────────────────────────────────┘  │  │
│  └──────────────────────────┬───────────────────────────────────┘  │
│                             │                                       │
│                             ▼                                       │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Fonctions de base de données (projet_db.py, tache_db.py)    │  │
│  │  - creer_projet(conn, cursor, titre, ...)                    │  │
│  │  - modifier_projet(conn, cursor, projet_id, ...)             │  │
│  │  - creer_tache(conn, cursor, projet_id, ...)                 │  │
│  │  - lister_projets(conn, cursor, statut)                      │  │
│  │  - etc.                                                       │  │
│  └────────────────────────┬─────────────────────────────────────┘  │
│                           │                                         │
│                           ▼                                         │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │  Base de données SQLite (database.db)                         │  │
│  │  - Table: projets                                             │  │
│  │  - Table: taches                                              │  │
│  └──────────────────────────────────────────────────────────────┘  │
└────────────────────────────────────────────────────────────────────┘
```

#### Flux de fonctionnement détaillé

1. **L'utilisateur écrit** : "Crée un projet 'Stage entreprise' avec échéance au 15 juin"

2. **ai_assistant.py reçoit le prompt** et envoie à Ollama :
   ```python
   # Ollama reçoit :
   # - Le prompt utilisateur
   # - La liste des tools disponibles avec leurs descriptions :
   {
     "name": "creer_projet",
     "description": "Crée un nouveau projet",
     "parameters": {
       "titre": "string (requis)",
       "description": "string (optionnel)",
       "statut": "string (défaut: 'ouvert')"
     }
   }
   ```

3. **Ollama analyse et décide** :
   - Comprend qu'il faut créer un projet
   - Extrait les informations : titre="Stage entreprise", échéance="2025-06-15"
   - Retourne un appel de fonction structuré

4. **ai_assistant.py exécute la fonction** :
   ```python
   conn, cursor = ouvrir_database()
   projet_id = creer_projet(conn, cursor,
                           titre="Stage entreprise",
                           description="Échéance: 15 juin")
   ```

5. **Résultat affiché** : "✅ Projet 'Stage entreprise' créé avec succès (ID: 5)"

#### Notre approche (Function Calling) :
- ✅ Tout intégré dans une seule application Python
- ✅ Pas de serveur séparé à gérer
- ✅ Code simple et lisible pour l'apprentissage
- ✅ Même résultat fonctionnel pour l'utilisateur

### Technologie : Ollama avec Llama 3.2

**Ollama** est un outil qui permet d'exécuter des modèles d'IA localement sur votre ordinateur.

**Avantages pour les étudiants** :
- ✅ **100% gratuit** : Aucun coût API, aucun abonnement
- ✅ **Installation simple** : Une seule commande `curl -fsSL https://ollama.com/install.sh | sh`
- ✅ **Fonctionne hors ligne** : Pas besoin de connexion internet après installation
- ✅ **Performant** : Llama 3.2 excellent pour les tâches structurées comme le function calling
- ✅ **Pédagogique** : Comprendre comment fonctionne une IA localement
- ✅ **Pas de données envoyées sur internet** : Confidentialité garantie

**Llama 3.2** est le modèle recommandé car :
- Optimisé pour le function calling
- Taille raisonnable (quelques GB)
- Bonnes performances même sur ordinateurs moyens
- Gratuit et open-source

## Configuration nécessaire

### Configuration matérielle minimale

Pour faire fonctionner Ollama avec Llama 3.2, voici les besoins en ressources :

#### Espace disque
- **Ollama** : ~500 MB
- **Llama 3.2 (3B)** : ~2 GB (modèle léger, recommandé pour débuter)
- **Llama 3.2 (1B)** : ~1 GB (encore plus léger, pour machines limitées)
- **Total recommandé** : Au moins **5 GB d'espace libre** (pour l'installation et la marge de manœuvre)

#### Mémoire RAM
- **Minimum** : 8 GB de RAM
- **Recommandé** : 16 GB de RAM pour de meilleures performances
- Le modèle Llama 3.2 (3B) utilise environ 3-4 GB de RAM pendant l'exécution

#### Processeur
- **Compatible avec** : x86_64 (Intel/AMD), ARM64 (Apple Silicon, ARM Linux)
- **Recommandé** : Processeur multi-cœurs moderne (4 cœurs ou plus)
- **Note** : GPU optionnel mais améliore les performances (NVIDIA CUDA, AMD ROCm, Apple Metal)

### Installation par système d'exploitation

#### 🐧 Linux

**Prérequis** :
- Distribution moderne (Ubuntu 20.04+, Debian 11+, Fedora 37+, etc.)
- `curl` installé

**Installation** :
```bash
# Installation d'Ollama en une commande
curl -fsSL https://ollama.com/install.sh | sh

# Vérifier l'installation
ollama --version

# Télécharger le modèle Llama 3.2 (3B)
ollama pull llama3.2

# Ou pour la version plus légère (1B)
ollama pull llama3.2:1b

# Tester le modèle
ollama run llama3.2
```

**Démarrage automatique** :
```bash
# Ollama démarre automatiquement comme service systemd
# Pour vérifier le statut :
sudo systemctl status ollama

# Pour redémarrer le service :
sudo systemctl restart ollama
```

**Emplacement des modèles** :
- Modèles stockés dans : `~/.ollama/models/`

---

#### 🍎 macOS

**Prérequis** :
- macOS 11 Big Sur ou plus récent
- Architecture Intel ou Apple Silicon (M1/M2/M3)

**Installation** :
```bash
# Méthode 1 : Via curl (similaire à Linux)
curl -fsSL https://ollama.com/install.sh | sh

# Méthode 2 : Télécharger l'application depuis le site
# Rendez-vous sur https://ollama.com/download
# Téléchargez Ollama.app et glissez-le dans Applications

# Vérifier l'installation
ollama --version

# Télécharger Llama 3.2
ollama pull llama3.2

# Tester
ollama run llama3.2
```

**Notes pour Apple Silicon (M1/M2/M3)** :
- Excellentes performances grâce à l'accélération Metal
- Llama 3.2 fonctionne très bien même sur Mac Mini M1 avec 8 GB RAM

**Emplacement des modèles** :
- Modèles stockés dans : `~/.ollama/models/`

**Interface graphique** :
- Ollama tourne en arrière-plan (icône dans la barre de menu)
- Clic sur l'icône pour voir le statut et les modèles installés

---

#### 🪟 Windows

**Prérequis** :
- Windows 10/11 (64-bit)
- WSL2 recommandé mais pas obligatoire (version native disponible)

**Installation (version native Windows)** :
```powershell
# Télécharger l'installeur depuis https://ollama.com/download
# Exécuter OllamaSetup.exe

# Ou via PowerShell (si disponible) :
# Télécharger et installer automatiquement
winget install Ollama.Ollama

# Vérifier l'installation
ollama --version

# Télécharger Llama 3.2
ollama pull llama3.2

# Tester
ollama run llama3.2
```

**Installation via WSL2 (méthode alternative)** :
```bash
# Dans WSL2 Ubuntu/Debian
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2
```

**Emplacement des modèles (Windows natif)** :
- Modèles stockés dans : `C:\Users\VotreNom\.ollama\models\`

**Notes Windows** :
- Service Ollama démarre automatiquement au démarrage de Windows
- Accessible via `http://localhost:11434`

---

### Installation du client Python

Après avoir installé Ollama, installer le client Python :

```bash
# Activer votre environnement virtuel (recommandé)
python -m venv venv

# Linux/macOS
source venv/bin/activate

# Windows
venv\Scripts\activate

# Installer le client Ollama Python
pip install ollama

# Vérifier l'installation
python -c "import ollama; print('✓ Client Ollama Python installé avec succès')"

# Ou vérifier la version avec pip
pip show ollama | grep Version
```

### Vérification de l'installation complète

Test rapide pour vérifier que tout fonctionne :

```bash
# 1. Vérifier qu'Ollama tourne
curl http://localhost:11434

# Devrait retourner : "Ollama is running"

# 2. Lister les modèles installés
ollama list

# Devrait afficher llama3.2

# 3. Test Python
python << EOF
import ollama
response = ollama.chat(model='llama3.2', messages=[
    {'role': 'user', 'content': 'Dis bonjour en français'}
])
print(response['message']['content'])
EOF
```

### Résolution de problèmes courants

#### Problème : "Ollama is not running"
**Solution** :
```bash
# Linux
sudo systemctl start ollama

# macOS
# Lancer Ollama.app depuis Applications

# Windows
# Lancer "Ollama" depuis le menu Démarrer
```

#### Problème : Pas assez de RAM
**Solution** :
- Utiliser le modèle plus léger : `ollama pull llama3.2:1b`
- Fermer les applications gourmandes en mémoire
- Vérifier les processus avec `htop` (Linux/macOS) ou Gestionnaire des tâches (Windows)

#### Problème : Téléchargement lent
**Solution** :
- Le premier téléchargement peut prendre 10-30 minutes selon votre connexion
- Llama 3.2 (3B) fait ~2 GB
- Laisser le téléchargement se terminer complètement

### Alternatives pour machines très limitées

Si votre ordinateur ne répond pas aux exigences :

1. **Utiliser un modèle plus petit** :
   ```bash
   ollama pull llama3.2:1b  # Seulement 1 GB
   ```

2. **Services cloud gratuits** (pour tests uniquement) :
   - Google Colab (GPU gratuit limité)
   - Hugging Face Spaces
   - Note : Ces solutions nécessitent une connexion internet

## Capacités de l'IA

L'IA pourra effectuer les opérations suivantes :

### 1. CRUD Projets
- Créer un nouveau projet
- Lire/consulter les informations d'un projet
- Modifier un projet existant (titre, description, statut)
- Supprimer un projet

### 2. CRUD Tâches
- Créer une nouvelle tâche dans un projet
- Lire/consulter les informations d'une tâche
- Modifier une tâche existante (tous les champs)
- Supprimer une tâche

### 3. Requêtes intelligentes
- Rechercher des projets/tâches selon des critères complexes en langage naturel
- Filtrer par dates, statuts, types, etc.
- Identifier les tâches urgentes, en retard, à venir

### 4. Suggestions
- Proposer des optimisations de planning
- Suggérer la priorisation de tâches
- Aider à la décomposition de tâches complexes
- Identifier les conflits d'échéances

## Architecture technique

### 1. Dépendances
```
ollama>=0.1.0  # Client Python pour Ollama
```

### 2. Modules à créer

#### `ai_config.py`
Configuration centralisée pour Ollama :
- URL du serveur Ollama (défaut: http://localhost:11434)
- Modèle à utiliser (défaut: llama3.2)
- Paramètres de génération (temperature, etc.)

#### `ai_assistant.py`
Module principal d'interaction avec l'IA :

**Fonctions principales** :
- `define_tools()` : Définit les outils disponibles pour l'IA
- `execute_tool_call(tool_name, arguments)` : Exécute un appel de fonction
- `process_user_request(prompt)` : Point d'entrée principal

**Tools disponibles** (mapping vers fonctions existantes) :
- `creer_projet(titre, description, statut)`
- `modifier_projet(projet_id, titre, description, statut)`
- `supprimer_projet(projet_id)`
- `lister_projets(statut)`
- `creer_tache(projet_id, type, titre, ...)`
- `modifier_tache(tache_id, ...)`
- `supprimer_tache(tache_id)`
- `lister_taches(projet_id, type)`
- `rechercher_projets_taches(criteres)` : Nouvelle fonction de recherche intelligente

### 3. Intégration dans l'interface

#### Modifications de `kanban_view_nice.py`

**Dans la fonction `send_prompt()`** :
```python
def send_prompt():
    user_prompt = prompt_input.value
    if user_prompt.strip():
        # Appeler l'IA
        result = ai_assistant.process_user_request(user_prompt)

        # Afficher le résultat
        ai_response['text'] += f"\n\n> Vous: {user_prompt}\n\n{result['message']}\n"
        response_area.set_text(ai_response['text'])

        # Rafraîchir l'affichage si modification
        if result['modified']:
            refresh_kanban()

        prompt_input.value = ''
```

**Gestion des erreurs** :
- Messages clairs en cas d'erreur
- Suggestions de correction si commande mal formulée
- Confirmation pour les opérations de suppression

## Exemples d'utilisation

### Création de projets
```
"Crée un projet 'Stage entreprise' avec échéance au 15 juin"
"Ajoute un nouveau projet 'Mémoire de fin d'études'"
```

### Gestion de tâches
```
"Ajoute une tâche 'Rédiger introduction' dans le projet Mémoire"
"Passe la tâche 'Recherche bibliographique' à 75% d'avancement"
"Liste toutes les tâches urgentes (échéance < 48h)"
```

### Modifications
```
"Change le titre du projet 1 en 'Projet de recherche'"
"Déplace l'échéance de la tâche 5 au 20 mai"
"Marque le projet 'Stage' comme fermé"
```

### Recherches intelligentes
```
"Montre-moi tous les projets ouverts"
"Quelles sont mes tâches en retard ?"
"Liste les réunions de cette semaine"
"Quelles tâches sont à moins de 30% d'avancement ?"
```

### Suggestions
```
"Aide-moi à organiser mes tâches par priorité"
"Décompose la tâche 'Rédiger le rapport' en sous-tâches"
"Y a-t-il des conflits d'échéances dans mes projets ?"
```

## Plan d'implémentation

### Phase 1 : Configuration et setup
1. Installer Ollama sur le système
2. Ajouter la dépendance `ollama` à requirements.txt
3. Créer `ai_config.py` avec la configuration
4. Documenter l'installation pour les étudiants

### Phase 2 : Module AI Assistant
1. Créer `ai_assistant.py`
2. Définir tous les tools avec leurs schémas JSON
3. Implémenter `define_tools()` : mapping vers projet_db/tache_db
4. Implémenter `execute_tool_call()` : exécution sécurisée
5. Implémenter `process_user_request()` : orchestration complète
6. Ajouter la fonction `rechercher_projets_taches()` pour recherches complexes

### Phase 3 : Intégration interface
1. Modifier `send_prompt()` dans kanban_view_nice.py
2. Ajouter la gestion des erreurs avec messages clairs
3. Implémenter le rafraîchissement automatique après modification
4. Améliorer l'affichage des réponses (formatting, couleurs)

### Phase 4 : Tests et documentation
1. Tester toutes les opérations CRUD via prompts
2. Tester les recherches intelligentes
3. Valider les suggestions
4. Créer `AI_EXAMPLES.md` avec exemples de prompts
5. Rédiger documentation pour étudiants (README_IA.md)

### Phase 5 : Optimisations
1. Ajouter un historique des conversations
2. Implémenter des confirmations pour actions critiques
3. Ajouter des raccourcis/templates de prompts
4. Optimiser les performances

## Avantages pédagogiques

Cette approche est idéale pour des étudiants car :

1. **Compréhensible** : Pas de concepts complexes, juste du Python et du JSON
2. **Gratuite** : Pas de frais cachés, fonctionne complètement hors ligne
3. **Modulaire** : Chaque composant est indépendant et testable
4. **Réutilisable** : Le code existant est préservé et enrichi
5. **Évolutive** : Facile d'ajouter de nouveaux tools ou capacités
6. **Pratique** : Montre concrètement comment une IA interagit avec une base de données

## Sécurité et bonnes pratiques

- Validation des entrées avant exécution
- Confirmation requise pour suppressions
- Logs des actions effectuées par l'IA
- Gestion propre des erreurs de connexion DB
- Limitation des requêtes complexes pour éviter surcharge

## Ressources pour les étudiants

### Documentation Ollama
- Site officiel : https://ollama.com
- Documentation API : https://github.com/ollama/ollama/blob/main/docs/api.md
- Modèles disponibles : https://ollama.com/library

### Tutoriels recommandés
- "Getting Started with Ollama and Python"
- "Function Calling with Local LLMs"
- "Building AI Assistants with Ollama"
