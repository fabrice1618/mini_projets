import sqlite3

def creer_tables(nom_fichier='database.db'):
    """Crée les tables projets et taches dans la base de données"""
    conn = sqlite3.connect(nom_fichier)
    cursor = conn.cursor()

    # Création de la table projets
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS projets (
            projet_id INTEGER PRIMARY KEY AUTOINCREMENT,
            titre TEXT NOT NULL,
            description TEXT,
            statut TEXT NOT NULL DEFAULT 'ouvert' CHECK(statut IN ('ouvert', 'ferme')),
            date_creation DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # Création de la table taches
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS taches (
            tache_id INTEGER PRIMARY KEY AUTOINCREMENT,
            projet_id INTEGER NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('cours', 'reunion', 'action')),
            titre TEXT NOT NULL,
            description_resumee TEXT,
            date_heure DATETIME,
            duree_minutes INTEGER,
            echeance_absolue DATETIME,
            tache_reference_id INTEGER,
            lien_fichier_details TEXT,
            avancement INTEGER DEFAULT 0 CHECK(avancement >= 0 AND avancement <= 100),
            date_creation DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (projet_id) REFERENCES projets(id) ON DELETE CASCADE,
            FOREIGN KEY (tache_reference_id) REFERENCES taches(id) ON DELETE SET NULL
        )
    ''')

    conn.commit()
    conn.close()
    print("Tables 'projets' et 'taches' créées avec succès !")

if __name__ == "__main__":
    creer_tables()
