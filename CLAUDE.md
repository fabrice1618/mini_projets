# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**Gestion de Projets** - A single-user project and task management application written in Python with SQLite database and AI integration.

### Core Requirements

- **Language**: Python
- **Database**: SQLite
- **AI Integration**: Required for task management features
- **User Model**: Single-user application

### Domain Model

**Projects**:
- Description
- Deadline (échéance)
- Can contain multiple tasks

**Tasks**:
- Type (action to perform OR appointment/meeting)
- Deadline
- Description
- Start date/time
- Progress/advancement status
- Collaborator assignment

### Main Features

1. **Project Management**: Create, read, update, delete projects
2. **Task Management**: Create, read, update, delete tasks within projects
3. **Upcoming Tasks View**: Display tasks that need to be completed soon
4. **AI-powered Task Management**: Leverage AI to help manage tasks

## Architecture Notes

The use case diagram (`gestion_projet.drawio`) shows:
- Primary actor: User
- Core use case: "Consulter les projets" (View projects) extends to:
  - Create, delete, modify projects
  - "Consulter les tâches" (View tasks) which further extends to:
    - Create, delete, modify tasks

When implementing, follow this hierarchy where task operations are accessed through project consultation.

## Development Guidelines

### Database Schema

Design SQLite schema with:
- `projets` table: id, description, echeance, ...
- `taches` table: id, projet_id (FK), type, echeance, description, date_heure_debut, avancement, collaborateur, ...
- Task types should be constrained to: "action" or "rendez-vous"

### AI Integration

The AI component should assist with task management. Consider what "gérer les tâches grâce à une IA" means in context - potentially:
- Task prioritization
- Deadline recommendations
- Task breakdown/suggestions
- Progress tracking assistance
