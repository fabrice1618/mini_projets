def creer_projet(conn, cursor, titre, description=None, statut='ouvert'):
    """Crée un nouveau projet dans la base de données"""
    cursor.execute(
        "INSERT INTO projets (titre, description, statut) VALUES (?, ?, ?)",
        (titre, description, statut)
    )
    conn.commit()  # Validation de la transaction
    projet_id = cursor.lastrowid
    return projet_id

def lire_projet(conn, cursor, projet_id):
    """Récupère les informations d'un projet"""
    cursor.execute(
        "SELECT * FROM projets WHERE projet_id = ?",
        (projet_id,)
    )
    resultat = cursor.fetchone()

    if resultat:
        return dict(resultat)  # Convertit Row en dictionnaire
    return None

def modifier_projet(conn, cursor, projet_id, titre=None, description=None, statut=None):
    """Modifie un projet existant"""
    # Construction dynamique de la requête selon les paramètres fournis
    updates = []
    params = []

    if titre is not None:
        updates.append("titre = ?")
        params.append(titre)
    if description is not None:
        updates.append("description = ?")
        params.append(description)
    if statut is not None:
        updates.append("statut = ?")
        params.append(statut)

    if not updates:
        return False

    params.append(projet_id)
    query = f"UPDATE projets SET {', '.join(updates)} WHERE projet_id = ?"

    cursor.execute(query, params)
    conn.commit()  # Validation de la transaction
    return cursor.rowcount > 0  # Retourne True si au moins une ligne modifiée

def supprimer_projet(conn, cursor, projet_id):
    """Supprime un projet"""
    cursor.execute(
        "DELETE FROM projets WHERE projet_id = ?",
        (projet_id,)
    )
    conn.commit()  # Validation de la transaction
    return cursor.rowcount > 0  # Retourne True si au moins une ligne supprimée

def lister_projets(conn, cursor, statut=None):
    """Liste tous les projets (ou filtre par statut si fourni)"""
    if statut is None:
        cursor.execute("SELECT * FROM projets ORDER BY date_creation DESC")
    else:
        cursor.execute("SELECT * FROM projets WHERE statut = ? ORDER BY date_creation DESC", (statut,))
    resultats = cursor.fetchall()
    return [dict(row) for row in resultats]
