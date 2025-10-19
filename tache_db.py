def creer_tache(conn, cursor, projet_id, type_tache, titre, description_resumee=None,
                date_heure=None, duree_minutes=None, echeance_absolue=None,
                tache_reference_id=None, lien_fichier_details=None, avancement=0):
    """Insère une nouvelle tâche dans la table taches

    Args:
        projet_id: ID du projet associé
        type_tache: Type de tâche ('cours', 'reunion', 'action')
        titre: Titre de la tâche (obligatoire)
        description_resumee: Description courte (optionnel)
        date_heure: Date et heure de début (optionnel)
        duree_minutes: Durée en minutes (optionnel, surtout pour cours/réunions)
        echeance_absolue: Deadline fixe (optionnel)
        tache_reference_id: ID d'une tâche de référence pour échéance relative (optionnel)
        lien_fichier_details: Lien vers fichier de détails (optionnel)
        avancement: Pourcentage d'avancement 0-100 (défaut: 0)
    """
    cursor.execute(
        """INSERT INTO taches (projet_id, type, titre, description_resumee, date_heure,
           duree_minutes, echeance_absolue, tache_reference_id, lien_fichier_details, avancement)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (projet_id, type_tache, titre, description_resumee, date_heure,
         duree_minutes, echeance_absolue, tache_reference_id, lien_fichier_details, avancement)
    )
    conn.commit()  # Validation de la transaction
    tache_id = cursor.lastrowid
    return tache_id

def lire_tache(conn, cursor, tache_id):
    """Récupère les informations d'une tâche à partir de son ID"""
    cursor.execute(
        "SELECT * FROM taches WHERE tache_id = ?",
        (tache_id,)
    )
    resultat = cursor.fetchone()

    if resultat:
        return dict(resultat)  # Convertit Row en dictionnaire
    return None

def modifier_tache(conn, cursor, tache_id, type_tache=None, titre=None, description_resumee=None,
                  date_heure=None, duree_minutes=None, echeance_absolue=None,
                  tache_reference_id=None, lien_fichier_details=None, avancement=None):
    """Met à jour les informations d'une tâche existante

    Seuls les paramètres fournis (non None) seront mis à jour.
    """
    # Construction dynamique de la requête selon les paramètres fournis
    updates = []
    params = []

    if type_tache is not None:
        updates.append("type = ?")
        params.append(type_tache)
    if titre is not None:
        updates.append("titre = ?")
        params.append(titre)
    if description_resumee is not None:
        updates.append("description_resumee = ?")
        params.append(description_resumee)
    if date_heure is not None:
        updates.append("date_heure = ?")
        params.append(date_heure)
    if duree_minutes is not None:
        updates.append("duree_minutes = ?")
        params.append(duree_minutes)
    if echeance_absolue is not None:
        updates.append("echeance_absolue = ?")
        params.append(echeance_absolue)
    if tache_reference_id is not None:
        updates.append("tache_reference_id = ?")
        params.append(tache_reference_id)
    if lien_fichier_details is not None:
        updates.append("lien_fichier_details = ?")
        params.append(lien_fichier_details)
    if avancement is not None:
        updates.append("avancement = ?")
        params.append(avancement)

    if not updates:
        return False

    params.append(tache_id)
    query = f"UPDATE taches SET {', '.join(updates)} WHERE tache_id = ?"

    cursor.execute(query, params)
    conn.commit()  # Validation de la transaction
    return cursor.rowcount > 0  # Retourne True si au moins une ligne modifiée

def supprimer_tache(conn, cursor, tache_id):
    """Supprime une tâche de la base de données"""
    cursor.execute(
        "DELETE FROM taches WHERE tache_id = ?",
        (tache_id,)
    )
    conn.commit()  # Validation de la transaction
    return cursor.rowcount > 0  # Retourne True si au moins une ligne supprimée

def lister_taches(conn, cursor, projet_id=None, type_tache=None):
    """Récupère toutes les tâches avec filtres optionnels

    Args:
        projet_id: Filtre par projet (optionnel)
        type_tache: Filtre par type ('cours', 'reunion', 'action') (optionnel)
    """
    query = "SELECT * FROM taches WHERE 1=1"
    params = []

    if projet_id is not None:
        query += " AND projet_id = ?"
        params.append(projet_id)

    if type_tache is not None:
        query += " AND type = ?"
        params.append(type_tache)

    query += " ORDER BY date_heure ASC, echeance_absolue ASC"

    cursor.execute(query, params)
    resultats = cursor.fetchall()
    return [dict(row) for row in resultats]

def lister_taches_a_venir(conn, cursor, limite=10):
    """Récupère les prochaines tâches à réaliser

    Retourne les tâches avec échéance proche, triées par date
    """
    cursor.execute(
        """SELECT * FROM taches
           WHERE (echeance_absolue IS NOT NULL AND echeance_absolue >= datetime('now'))
           OR (date_heure IS NOT NULL AND date_heure >= datetime('now'))
           ORDER BY
               CASE
                   WHEN echeance_absolue IS NOT NULL THEN echeance_absolue
                   ELSE date_heure
               END ASC
           LIMIT ?""",
        (limite,)
    )
    resultats = cursor.fetchall()
    return [dict(row) for row in resultats]
