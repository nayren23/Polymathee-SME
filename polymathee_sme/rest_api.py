"""Rest API"""
# !/usr/bin/env python
# -*- coding: utf-8 -*-
import os

from polymathee_sme import app
from polymathee_sme.route.user_route import user
from polymathee_sme.route.apprentis_route import apprentis


if __name__ == "__main__":
    currentPath = os.path.dirname(__file__)
    cert = os.path.join(currentPath, app.config["CERTIFICATE_CRT_FOLDER"])
    key = os.path.join(currentPath, app.config["CERTIFICATE_KEY_FOLDER"])
    context = (cert, key)  # certificate and key files

    app.register_blueprint(user)
    app.register_blueprint(apprentis)

    # Launch Flask server
    app.run(
        debug=app.config["FLASK_DEBUG"],
        host=app.config["FLASK_HOST"],
        port=app.config["FLASK_PORT"],
        ssl_context=context,
    )
