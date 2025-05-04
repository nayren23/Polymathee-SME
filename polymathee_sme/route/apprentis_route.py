from flask import Blueprint, request, jsonify
from polymathee_sme import connect_mysql

apprentis = Blueprint("apprentis", __name__, url_prefix="/apprentis")


@apprentis.route("/all", methods=["GET"])
def get_all_apprentis():
    conn = connect_mysql.connect()
    query = "SELECT * FROM apprentis LIMIT 100"
    result = connect_mysql.get_query(conn, query)
    return jsonify(result)


@apprentis.route("/stats/regions", methods=["GET"])
def get_stats_by_region():
    conn = connect_mysql.connect()
    query = """
    SELECT region, SUM(effectif) AS total_apprentis
    FROM apprentis
    GROUP BY region
    ORDER BY total_apprentis DESC
    """
    result = connect_mysql.get_query(conn, query)
    return jsonify(result)


@apprentis.route("/filter", methods=["GET"])
def filter_apprentis():
    region = request.args.get("region")
    annee = request.args.get("annee")
    conn = connect_mysql.connect()

    query = "SELECT * FROM apprentis WHERE 1=1"
    if region:
        query += f" AND region = '{region}'"
    if annee:
        query += f" AND annee = '{annee}'"

    result = connect_mysql.get_query(conn, query)
    return jsonify(result)
