import sqlite3

def ouvrir_database(nom_fichier='database.db'):
    """Ouvre une connexion à la base de données SQLite"""
    conn = sqlite3.connect(nom_fichier)
    conn.row_factory = sqlite3.Row  # Pour accéder aux colonnes par leur nom
    cursor = conn.cursor()
    return conn, cursor
