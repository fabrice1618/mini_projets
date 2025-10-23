"""
Interface Kanban en lecture seule pour visualiser les projets et leurs tâches
Organisation: Une colonne par projet
Tri: Tâches triées par échéance absolue
Version NiceGUI
"""

from nicegui import ui
from datetime import datetime
from database import ouvrir_database
from projet_db import lister_projets
from tache_db import lister_taches
from ai_assistant import process_user_request


# Couleurs pour les types de tâches
TYPE_COLORS = {
    'cours': '#3B82F6',      # Bleu
    'reunion': '#8B5CF6',    # Violet
    'action': '#10B981'      # Vert
}

# Labels pour les types de tâches
TYPE_LABELS = {
    'cours': 'COURS',
    'reunion': 'RÉUNION',
    'action': 'ACTION'
}


def formater_echeance(echeance):
    """Formate l'échéance pour l'affichage"""
    if not echeance:
        return None

    try:
        dt = datetime.fromisoformat(echeance.replace('Z', '+00:00'))
        return dt.strftime('%d/%m/%Y %H:%M')
    except:
        return echeance


def formater_date_heure(date_heure):
    """Formate la date/heure pour l'affichage"""
    if not date_heure:
        return None

    try:
        dt = datetime.fromisoformat(date_heure.replace('Z', '+00:00'))
        return dt.strftime('%d/%m/%Y %H:%M')
    except:
        return date_heure


def get_echeance_color(echeance):
    """Détermine la couleur selon l'urgence de l'échéance"""
    if not echeance:
        return '#6B7280'  # Gris

    try:
        dt = datetime.fromisoformat(echeance.replace('Z', '+00:00'))
        now = datetime.now()
        delta = (dt - now).total_seconds() / 3600  # Heures restantes

        if delta < 0:
            return '#EF4444'  # Rouge - Dépassé
        elif delta < 24:
            return '#F59E0B'  # Orange - Urgent (< 24h)
        elif delta < 72:
            return '#FBBF24'  # Jaune - Proche (< 3j)
        else:
            return '#6B7280'  # Gris - Normal
    except:
        return '#6B7280'


def create_task_card(tache_data):
    """Crée une carte de tâche"""
    border_color = TYPE_COLORS.get(tache_data['type'], '#6B7280')

    with ui.card().classes('w-72 min-h-48 p-4').style(f'border-left: 4px solid {border_color}'):
        # Titre de la tâche
        ui.label(tache_data['titre']).classes('text-base font-bold mb-2 break-words')

        # Badge du type de tâche
        type_label = TYPE_LABELS.get(tache_data['type'], tache_data['type'].upper())
        type_color = TYPE_COLORS.get(tache_data['type'], '#6B7280')
        ui.badge(type_label).classes('mb-2').style(f'background-color: {type_color}; color: white;')

        # Échéance
        echeance_text = formater_echeance(tache_data.get('echeance_absolue'))
        if echeance_text:
            echeance_color = get_echeance_color(tache_data.get('echeance_absolue'))
            with ui.row().classes('items-center gap-1 mb-1'):
                ui.label('📅').classes('text-sm')
                ui.label(echeance_text).classes('text-sm').style(f'color: {echeance_color}')

        # Date/heure de début si disponible
        if tache_data.get('date_heure'):
            date_heure_text = formater_date_heure(tache_data['date_heure'])
            with ui.row().classes('items-center gap-1 mb-2'):
                ui.label('🕐').classes('text-xs')
                ui.label(date_heure_text).classes('text-xs')

        # Barre de progression
        avancement = tache_data.get('avancement', 0)
        with ui.row().classes('items-center gap-2 w-full mb-2'):
            ui.linear_progress(value=avancement / 100).classes('flex-grow')
            ui.label(f'{avancement}%').classes('text-xs')

        # Description résumée si disponible
        if tache_data.get('description_resumee'):
            desc = tache_data['description_resumee']
            desc_courte = desc[:100] + ('...' if len(desc) > 100 else '')
            ui.label(desc_courte).classes('text-xs text-gray-500 break-words')

        # Bouton menu (en bas de la carte)
        with ui.row().classes('justify-end mt-2'):
            ui.button('⋯').props('flat dense size=sm').classes('text-gray-500')


def create_project_column(projet_data, taches):
    """Crée une colonne de projet avec ses tâches"""
    with ui.card().classes('w-80 min-h-screen-75').style('background-color: #f3f4f6;'):
        # En-tête de la colonne
        with ui.card_section().classes('pb-2'):
            # Titre du projet
            ui.label(projet_data['titre']).classes('text-lg font-bold mb-2 break-words').style('color: #000000;')

            # Statut du projet
            statut_text = "OUVERT" if projet_data['statut'] == 'ouvert' else "FERMÉ"
            statut_color = "#10B981" if projet_data['statut'] == 'ouvert' else "#6B7280"
            ui.badge(statut_text).style(f'background-color: {statut_color}; color: white;')

            # Séparateur
            ui.separator().classes('my-2')

        # Zone scrollable pour les tâches
        with ui.scroll_area().classes('h-[600px]'):
            with ui.column().classes('gap-4 p-2'):
                if taches:
                    # Trier les tâches par échéance absolue
                    taches_triees = sorted(
                        taches,
                        key=lambda t: (
                            t['echeance_absolue'] is None,  # None en dernier
                            t['echeance_absolue'] or ''
                        )
                    )

                    for tache in taches_triees:
                        create_task_card(tache)
                else:
                    ui.label('Aucune tâche').classes('text-center text-gray-500 mt-8')


def refresh_kanban():
    """Rafraîchit l'affichage du Kanban"""
    ui.navigate.reload()


def load_kanban_data():
    """Charge et affiche les données du Kanban"""
    try:
        conn, cursor = ouvrir_database()

        # Récupérer tous les projets
        projets = lister_projets(conn, cursor)

        if not projets:
            with ui.column().classes('items-center justify-center h-96'):
                ui.label('Aucun projet trouvé.').classes('text-xl text-gray-500')
                ui.label('Utilisez les scripts CLI pour créer des projets et des tâches.').classes('text-sm text-gray-400')
            return

        # Créer les colonnes de projets
        with ui.row().classes('gap-4 p-4 overflow-x-auto').style('min-height: 700px;'):
            for projet in projets:
                # Récupérer les tâches de ce projet
                taches = lister_taches(conn, cursor, projet_id=projet['projet_id'])

                # Créer la colonne du projet
                create_project_column(projet, taches)

        conn.close()

    except Exception as e:
        with ui.column().classes('items-center justify-center h-96'):
            ui.label(f'Erreur lors du chargement des données:').classes('text-xl text-red-500')
            ui.label(str(e)).classes('text-sm text-red-400')


@ui.page('/')
def main_page():
    """Page principale de l'application Kanban"""
    # État du panneau IA
    panel_visible = {'value': False}
    ai_response = {'text': ''}

    def toggle_ai_panel():
        """Bascule l'affichage du panneau IA"""
        panel_visible['value'] = not panel_visible['value']
        ai_panel.set_visibility(panel_visible['value'])
        if panel_visible['value']:
            ai_panel.classes(remove='panel-hidden', add='panel-visible')
        else:
            ai_panel.classes(remove='panel-visible', add='panel-hidden')

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

    # En-tête
    with ui.header().classes('items-center justify-between').style('height: 80px; padding: 0 20px; background-color: #1f2937;'):
        with ui.row().classes('items-center gap-4'):
            ui.label('mini projets').classes('text-2xl font-bold').style('color: white;')
            ui.button(icon='chevron_right', on_click=toggle_ai_panel).props('outline').style('color: white; border-color: white; border-width: 2px;').tooltip('prompt IA')
        ui.button('Rafraîchir', on_click=refresh_kanban).props('outline').style('color: white; border-color: white;')

    # Panneau IA (initialement caché)
    with ui.column().classes('w-full panel-hidden').style(
        'background-color: #f9fafb; border-bottom: 1px solid #d1d5db; padding: 15px; '
        'overflow: hidden; max-height: 0; transition: max-height 0.3s ease-in-out;'
    ).bind_visibility_from(panel_visible, 'value') as ai_panel:

        # Zone de saisie du prompt avec bouton d'envoi
        with ui.row().classes('w-full items-end gap-2 mb-3'):
            prompt_input = ui.textarea(
                placeholder='Posez votre question ou donnez une instruction...'
            ).classes('flex-grow').style('min-height: 80px; background-color: white; border: 2px solid #3b82f6;')

            ui.button('Envoyer', on_click=send_prompt, icon='send').props('color=primary').classes('mb-1')

        ui.separator().classes('my-2')

        # Zone de réponse de l'IA
        with ui.scroll_area().classes('w-full').style('height: 200px; background-color: white; border: 1px solid #d1d5db; border-radius: 4px; padding: 10px;'):
            response_area = ui.label(ai_response.get('text', 'Les réponses de l\'IA apparaîtront ici...')).classes('text-sm whitespace-pre-wrap').style('color: #374151;')

    # Contenu principal
    with ui.column().classes('w-full'):
        load_kanban_data()

    # Styles CSS pour l'animation
    ui.add_head_html('''
        <style>
            .panel-hidden {
                max-height: 0 !important;
            }
            .panel-visible {
                max-height: 400px !important;
            }
        </style>
    ''')


def main():
    """Point d'entrée de l'application"""
    ui.run(
        title='mini projets',
        dark=False,
        reload=False,
        port=8080
    )


if __name__ == '__main__':
    main()
