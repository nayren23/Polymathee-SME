"""Configure database connection"""
# !/usr/bin/python
from ast import literal_eval
import dataclasses
import os
from configparser import ConfigParser, NoSectionError
from dotenv import load_dotenv


@dataclasses.dataclass
class Config:
    """Config variables"""

    PATH = os.path.dirname(__file__)
    load_dotenv()

    FRONT_END_URL = os.getenv("FRONT_END_URL")

    # DB config
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PWD = os.getenv("DB_PWD")
    DB_PORT = os.getenv("DB_PORT", "5432")

    # FLask configuration
    FLASK_DEBUG = literal_eval(os.getenv("FLASK_DEBUG"))
    FLASK_HOST = os.getenv("FLASK_HOST")
    FLASK_PORT = os.getenv("FLASK_PORT")

    # CERTS
    CERTIFICATE_CRT_FOLDER = os.getenv("CERTIFICATE_CRT_FOLDER")
    CERTIFICATE_KEY_FOLDER = os.getenv("CERTIFICATE_KEY_FOLDER")


class TestingConfig(Config):
    """Testing Config variables"""

    UNIVERSITY_EMAIL_DOMAIN = "university.com"
    TESTING = True
    DB_HOST = ""


def config(filename="config.ini", section="postgresql"):
    """Configure database connection"""
    parser = ConfigParser()
    file_path = os.path.join(os.path.dirname(__file__), filename)

    if not parser.read(file_path):
        raise FileNotFoundError(f"Configuration file '{filename}' not found.")

    if not parser.has_section(section):
        raise NoSectionError(section)

    return dict(parser.items(section))
