"""
Interface Kanban en lecture seule pour visualiser les projets et leurs tâches
Organisation: Une colonne par projet
Tri: Tâches triées par échéance absolue
"""

import customtkinter as ctk
from datetime import datetime
from database import ouvrir_database
from projet_db import lister_projets
from tache_db import lister_taches


class TaskCard(ctk.CTkFrame):
    """Carte représentant une tâche dans le Kanban"""

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

    def __init__(self, master, tache_data, **kwargs):
        super().__init__(master, **kwargs)
        self.tache = tache_data

        # Configuration du style de la carte
        self.configure(
            fg_color=("white", "gray17"),
            corner_radius=8,
            border_width=2,
            border_color=self.TYPE_COLORS.get(tache_data['type'], 'gray')
        )

        # Padding interne
        self.grid_columnconfigure(0, weight=1)

        # Titre de la tâche
        titre_label = ctk.CTkLabel(
            self,
            text=tache_data['titre'],
            font=ctk.CTkFont(size=13, weight="bold"),
            anchor="w",
            wraplength=250
        )
        titre_label.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))

        # Badge du type de tâche
        type_badge = ctk.CTkLabel(
            self,
            text=self.TYPE_LABELS.get(tache_data['type'], tache_data['type'].upper()),
            font=ctk.CTkFont(size=10, weight="bold"),
            fg_color=self.TYPE_COLORS.get(tache_data['type'], 'gray'),
            corner_radius=4,
            width=80,
            height=22,
            text_color="white"
        )
        type_badge.grid(row=1, column=0, sticky="w", padx=10, pady=5)

        # Échéance
        echeance_text = self._formater_echeance(tache_data.get('echeance_absolue'))
        if echeance_text:
            echeance_color = self._get_echeance_color(tache_data.get('echeance_absolue'))
            echeance_label = ctk.CTkLabel(
                self,
                text=f"📅 {echeance_text}",
                font=ctk.CTkFont(size=11),
                text_color=echeance_color,
                anchor="w"
            )
            echeance_label.grid(row=2, column=0, sticky="w", padx=10, pady=2)

        # Date/heure de début si disponible
        if tache_data.get('date_heure'):
            date_heure_text = self._formater_date_heure(tache_data['date_heure'])
            date_label = ctk.CTkLabel(
                self,
                text=f"🕐 {date_heure_text}",
                font=ctk.CTkFont(size=10),
                anchor="w"
            )
            date_label.grid(row=3, column=0, sticky="w", padx=10, pady=2)

        # Barre de progression
        avancement = tache_data.get('avancement', 0)
        progress_frame = ctk.CTkFrame(self, fg_color="transparent")
        progress_frame.grid(row=4, column=0, sticky="ew", padx=10, pady=(5, 5))
        progress_frame.grid_columnconfigure(0, weight=1)

        progress_bar = ctk.CTkProgressBar(
            progress_frame,
            height=8,
            corner_radius=4
        )
        progress_bar.grid(row=0, column=0, sticky="ew", pady=2)
        progress_bar.set(avancement / 100)

        progress_label = ctk.CTkLabel(
            progress_frame,
            text=f"{avancement}%",
            font=ctk.CTkFont(size=10),
            width=40
        )
        progress_label.grid(row=0, column=1, padx=(5, 0))

        # Description résumée si disponible
        if tache_data.get('description_resumee'):
            desc_label = ctk.CTkLabel(
                self,
                text=tache_data['description_resumee'][:100] + ('...' if len(tache_data['description_resumee']) > 100 else ''),
                font=ctk.CTkFont(size=10),
                anchor="w",
                wraplength=250,
                text_color=("gray50", "gray60")
            )
            desc_label.grid(row=5, column=0, sticky="ew", padx=10, pady=(0, 5))

        # Bouton menu (en bas de la carte)
        menu_btn = ctk.CTkButton(
            self,
            text="⋯",
            font=ctk.CTkFont(size=18),
            width=40,
            height=28,
            fg_color="transparent",
            hover_color=("gray80", "gray25"),
            text_color=("gray60", "gray50"),
            corner_radius=4
        )
        menu_btn.grid(row=6, column=0, sticky="e", padx=10, pady=(5, 10))

    def _formater_echeance(self, echeance):
        """Formate l'échéance pour l'affichage"""
        if not echeance:
            return None

        try:
            dt = datetime.fromisoformat(echeance.replace('Z', '+00:00'))
            return dt.strftime('%d/%m/%Y %H:%M')
        except:
            return echeance

    def _formater_date_heure(self, date_heure):
        """Formate la date/heure pour l'affichage"""
        if not date_heure:
            return None

        try:
            dt = datetime.fromisoformat(date_heure.replace('Z', '+00:00'))
            return dt.strftime('%d/%m/%Y %H:%M')
        except:
            return date_heure

    def _get_echeance_color(self, echeance):
        """Détermine la couleur selon l'urgence de l'échéance"""
        if not echeance:
            return ("gray50", "gray60")

        try:
            dt = datetime.fromisoformat(echeance.replace('Z', '+00:00'))
            now = datetime.now()
            delta = (dt - now).total_seconds() / 3600  # Heures restantes

            if delta < 0:
                return "#EF4444"  # Rouge - Dépassé
            elif delta < 24:
                return "#F59E0B"  # Orange - Urgent (< 24h)
            elif delta < 72:
                return "#FBBF24"  # Jaune - Proche (< 3j)
            else:
                return ("gray50", "gray60")  # Normal
        except:
            return ("gray50", "gray60")


class ProjectColumn(ctk.CTkScrollableFrame):
    """Colonne représentant un projet avec ses tâches"""

    def __init__(self, master, projet_data, **kwargs):
        super().__init__(master, **kwargs)

        self.projet = projet_data
        self.configure(
            fg_color=("gray92", "gray13"),
            corner_radius=10
        )

        # En-tête de la colonne
        header_frame = ctk.CTkFrame(self, fg_color="transparent")
        header_frame.pack(fill="x", padx=5, pady=(5, 10))

        # Titre du projet
        titre_label = ctk.CTkLabel(
            header_frame,
            text=projet_data['titre'],
            font=ctk.CTkFont(size=16, weight="bold"),
            anchor="w",
            wraplength=270
        )
        titre_label.pack(fill="x", padx=5)

        # Statut du projet
        statut_text = "SAUF OUVERT" if projet_data['statut'] == 'ouvert' else "SAUF FERMÉ"
        statut_color = "#10B981" if projet_data['statut'] == 'ouvert' else "#6B7280"
        statut_badge = ctk.CTkLabel(
            header_frame,
            text=statut_text,
            font=ctk.CTkFont(size=10, weight="bold"),
            fg_color=statut_color,
            corner_radius=4,
            height=22,
            text_color="white",
            padx=8
        )
        statut_badge.pack(anchor="w", padx=5, pady=(5, 0))

        # Séparateur
        separator = ctk.CTkFrame(self, height=2, fg_color=("gray70", "gray30"))
        separator.pack(fill="x", padx=5, pady=5)

    def add_task_card(self, tache_data):
        """Ajoute une carte de tâche à la colonne"""
        card = TaskCard(self, tache_data)
        card.pack(fill="x", padx=5, pady=5)


class KanbanApp(ctk.CTk):
    """Application principale Kanban"""

    def __init__(self):
        super().__init__()

        # Configuration de la fenêtre
        self.title("Gestion de Projets - Vue Kanban")
        self.geometry("1400x800")

        # Thème
        ctk.set_appearance_mode("dark")  # "light" ou "dark"
        ctk.set_default_color_theme("blue")

        # En-tête
        self._create_header()

        # Zone de contenu principale (scrollable horizontalement)
        self._create_main_content()

        # Chargement des données
        self._load_data()

    def _create_header(self):
        """Crée l'en-tête de l'application"""
        header_frame = ctk.CTkFrame(self, height=80, corner_radius=0)
        header_frame.pack(fill="x", side="top")
        header_frame.pack_propagate(False)

        title_label = ctk.CTkLabel(
            header_frame,
            text="Vue Kanban - Projets et Tâches",
            font=ctk.CTkFont(size=24, weight="bold")
        )
        title_label.pack(side="left", padx=20, pady=20)

        # Bouton pour rafraîchir
        refresh_btn = ctk.CTkButton(
            header_frame,
            text="Rafraîchir",
            command=self._refresh_data,
            width=120,
            height=35
        )
        refresh_btn.pack(side="right", padx=20, pady=20)

    def _create_main_content(self):
        """Crée la zone de contenu principale avec défilement horizontal"""
        # Frame conteneur
        self.main_container = ctk.CTkFrame(self, fg_color="transparent")
        self.main_container.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame interne pour les colonnes (utilise pack au lieu de canvas)
        self.columns_frame = ctk.CTkFrame(self.main_container, fg_color="transparent")
        self.columns_frame.pack(fill="both", expand=True)

        # Stocker le nombre de colonnes
        self.num_columns = 0


    def _load_data(self):
        """Charge les données depuis la base de données"""
        try:
            conn, cursor = ouvrir_database()

            # Récupérer tous les projets
            projets = lister_projets(conn, cursor)

            if not projets:
                # Afficher un message si aucun projet
                no_data_label = ctk.CTkLabel(
                    self.columns_frame,
                    text="Aucun projet trouvé.\nUtilisez les scripts CLI pour créer des projets et des tâches.",
                    font=ctk.CTkFont(size=14),
                    text_color=("gray50", "gray60")
                )
                no_data_label.pack(padx=50, pady=100)
                return

            # Stocker le nombre de colonnes
            self.num_columns = len(projets)

            # Configurer le grid pour que les colonnes se répartissent équitablement
            self.columns_frame.grid_rowconfigure(0, weight=1)
            for idx in range(self.num_columns):
                self.columns_frame.grid_columnconfigure(idx, weight=1, uniform="column")

            # Créer une colonne pour chaque projet
            for idx, projet in enumerate(projets):
                # Créer la colonne du projet
                column = ProjectColumn(self.columns_frame, projet)
                column.grid(row=0, column=idx, padx=10, pady=10, sticky="nsew")

                # Récupérer les tâches de ce projet
                taches = lister_taches(conn, cursor, projet_id=projet['projet_id'])

                # Trier les tâches par échéance absolue
                taches_triees = sorted(
                    taches,
                    key=lambda t: (
                        t['echeance_absolue'] is None,  # None en dernier
                        t['echeance_absolue'] or ''
                    )
                )

                # Ajouter les cartes de tâches
                if taches_triees:
                    for tache in taches_triees:
                        column.add_task_card(tache)
                else:
                    # Message si aucune tâche
                    no_task_label = ctk.CTkLabel(
                        column,
                        text="Aucune tâche",
                        font=ctk.CTkFont(size=12),
                        text_color=("gray50", "gray60")
                    )
                    no_task_label.pack(padx=10, pady=20)

            conn.close()

        except Exception as e:
            error_label = ctk.CTkLabel(
                self.columns_frame,
                text=f"Erreur lors du chargement des données:\n{str(e)}",
                font=ctk.CTkFont(size=14),
                text_color="red"
            )
            error_label.pack(padx=50, pady=100)

    def _refresh_data(self):
        """Rafraîchit l'affichage des données"""
        # Détruire toutes les colonnes existantes
        for widget in self.columns_frame.winfo_children():
            widget.destroy()

        # Réinitialiser le nombre de colonnes
        self.num_columns = 0

        # Recharger les données
        self._load_data()


def main():
    """Point d'entrée de l'application"""
    app = KanbanApp()
    app.mainloop()


if __name__ == "__main__":
    main()
