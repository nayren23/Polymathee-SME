"""Rest API"""

# !/usr/bin/env python
# -*- coding: utf-8 -*-

from polymathee_sme import app
from polymathee_sme.route.apprentis_route import apprentis

if __name__ == "__main__":
    app.register_blueprint(apprentis)

    # Launch Flask server
    app.run(
        debug=app.config["FLASK_DEBUG"],
        host=app.config["FLASK_HOST"],
        port=app.config["FLASK_PORT"],
    )
