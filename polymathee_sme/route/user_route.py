"""User related endpoints"""
from flask import Blueprint, jsonify, make_response, request, send_file
from flask_jwt_extended.exceptions import NoAuthorizationError

from polymathee_sme import app, connect_mysql
from polymathee_sme import app
from polymathee_sme.utils.exception.exceptions import ApiException
from polymathee_sme.utils.exception.user_exceptions import EmailAlreadyVerifiedException
from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    get_jwt_identity,
    jwt_required,
    set_access_cookies,
    set_refresh_cookies,
    unset_jwt_cookies,
    verify_jwt_in_request,
)

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
    FROM utilisateur
    """
    select = connect_mysql.get_query(conn, query)

    return select
