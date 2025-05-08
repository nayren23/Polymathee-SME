"""Initialisation of the api"""

from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restful import Api
from flask_rq2 import RQ

from polymathee_sme.config import Config

app = Flask(__name__)
app.config.from_object(Config)
print(Config.FRONT_END_URL)
# cors = CORS(app, resources={r"*": {"origins": Config.FRONT_END_URL}}, supports_credentials=True)
CORS(app, resources={r"*": {"origins": "http://localhost:4200"}}, supports_credentials=True)
api = Api(app)
jwt = JWTManager(app)
rq = RQ(app)
