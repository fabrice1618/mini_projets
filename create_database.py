import sqlite3

def creer_database(nom_fichier='database.db'):
    """Crée le fichier de base de données SQLite"""
    conn = sqlite3.connect(nom_fichier)
    print(f"Base de données '{nom_fichier}' créée avec succès !")
    conn.close()

if __name__ == "__main__":
    creer_database()
