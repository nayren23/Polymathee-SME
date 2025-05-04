"""Rest API"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import os
from datetime import datetime

from flask import jsonify
from flask_jwt_extended import create_access_token, get_jwt, get_jwt_identity, set_access_cookies
from polymathee_sme import app
from polymathee_sme.route.user_route import user



@app.after_request
def reformat_jwt_response(response):
    """Reformat the response for jwt errors"""
    response_json = response.get_json()
    if response_json and "msg" in response_json:
        message = ""
        if not response_json["msg"].lower().startswith("token"):
            message = "TOKEN_"
        message += response_json["msg"].split(":")[0].replace(" ", "_").upper()

        response_json["message"] = message
        del response_json["msg"]
        response.data = json.dumps(response_json)
    return response


if __name__ == "__main__":
    currentPath = os.path.dirname(__file__)
    cert = os.path.join(currentPath, app.config["CERTIFICATE_CRT_FOLDER"])
    key = os.path.join(currentPath, app.config["CERTIFICATE_KEY_FOLDER"])
    context = (cert, key)  # certificate and key files
    
    app.register_blueprint(user)
    # Launch Flask server
    app.run(
        debug=app.config["FLASK_DEBUG"],
        host=app.config["FLASK_HOST"],
        port=app.config["FLASK_PORT"],
        ssl_context=context,
    )
