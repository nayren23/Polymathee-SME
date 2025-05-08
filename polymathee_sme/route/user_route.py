"""User related endpoints"""

from flask import Blueprint, jsonify

from polymathee_sme import connect_mysql
from polymathee_sme.utils.exception.exceptions import ApiException

user = Blueprint("user", __name__, url_prefix="/user")


@user.route("/hello", methods=["GET"])
def register():
    """Hello World endpoint"""
    response = jsonify(message="HELLO_WORLD"), 200
    try:
        print("Hello World Route user")
    except ApiException as e:
        response = jsonify(message=e.message), e.status_code

    return response


@user.route("/test-db", methods=["GET"])
def test():
    """Test World endpoint"""
    conn = connect_mysql.connect()
    query = """
    SELECT *
    FROM formation
    """
    select = connect_mysql.get_query(conn, query)

    return select
