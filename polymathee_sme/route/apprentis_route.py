from flask import Blueprint, jsonify, request
from polymathee_sme import connect_mysql

apprentis = Blueprint("apprentis", __name__, url_prefix="/apprentis")


@apprentis.route("/most-common-specialties", methods=["GET"])
def get_most_common_specialties():
    """Analyse des spécialités les plus courantes par type de diplôme"""

    conn = connect_mysql.connect()
    query = """
    SELECT
    d.type_diplome,
    s.libelle_specialite,
    COUNT(f.numero_section) AS nombre_formations
    FROM Diplome d
    JOIN Formation f ON d.diplome = f.diplome
    JOIN Specialite s ON f.code_groupe_specialite = s.code_groupe_specialite
    GROUP BY d.type_diplome, s.libelle_specialite
    ORDER BY d.type_diplome, nombre_formations DESC
    """
    raw_result = connect_mysql.get_query(conn, query)

    # Conversion en liste de dictionnaires
    formatted_result = [
        {"type_diplome": row[0], "libelle_specialite": row[1], "nombre_formations": row[2]} for row in raw_result
    ]
    return jsonify(formatted_result)


@apprentis.route("/top-schools-by-diplomas", methods=["GET"])
def get_top_etablissements_formations():
    """
    Retourne les établissements offrant le plus de diplômes différents en 2024-2025.
    """

    conn = connect_mysql.connect()
    query = """
        SELECT
            e.nom_complet_cfa,
            COUNT(DISTINCT f.diplome) AS nb_diplomes_diff
        FROM Etablissement e
        JOIN Formation f ON e.id_etab = f.id_etab
        WHERE f.annee_scolaire = '2024-2025' 
        GROUP BY e.nom_complet_cfa
        ORDER BY nb_diplomes_diff DESC; 
    """
    select = connect_mysql.get_query(conn, query)
    result = [{"etablissement": row[0], "nombre_diplomes_differents": row[1]} for row in select]
    return jsonify(result)


@apprentis.route("/diplomes", methods=["GET"])
def get_diplomes():
    """
    Retourne la liste des diplomes
    """
    try:
        conn = connect_mysql.connect()
        query = "SELECT DISTINCT diplome FROM Diplome ORDER BY diplome;"
        select = connect_mysql.get_query(conn, query)
        result = [{"diplome": row[0]} for row in select]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@apprentis.route("/ville-jeunes", methods=["GET"])
def get_villes_by_diplome():
    diplome = request.args.get("diplome")
    annee = request.args.get("annee")

    if not diplome or not annee:
        return jsonify({"error": "Paramètres diplome et annee requis"}), 400

    try:
        query = """
            SELECT cj.libelle_ville_jeune AS ville, COUNT(*) AS nombre_jeunes
            FROM Diplome d
            JOIN Formation f ON d.diplome = f.diplome
            JOIN Inscrire i ON f.annee_scolaire = i.annee_scolaire AND f.numero_section = i.numero_section
            JOIN Jeune j ON i.annee_scolaire_1 = j.annee_scolaire AND i.num_section = j.num_section
            JOIN CommuneJeune cj ON j.annee_scolaire_2 = cj.annee_scolaire AND j.num_section_2 = cj.num_section
            WHERE d.diplome = %s AND f.annee_scolaire = %s
            GROUP BY cj.libelle_ville_jeune
            ORDER BY nombre_jeunes DESC
            LIMIT 10;
        """
        conn = connect_mysql.connect()
        values = (diplome, annee)
        select = connect_mysql.get_query(conn, query, values)
        result = [{"ville": row[0], "nombre_jeunes": row[1]} for row in select]
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
