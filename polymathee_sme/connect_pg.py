"""Postgresql databse interactions"""
# !/usr/bin/python

from configparser import NoSectionError
import psycopg2
import psycopg2.extras
from uniride_sme import app


def connect():
    """Connect to the PostgreSQL database server"""
    conn = None
    try:
        # read connection parameters
        params = {}
        params["dbname"] = app.config["DB_NAME"]
        params["user"] = app.config["DB_USER"]
        params["password"] = app.config["DB_PWD"]
        params["host"] = app.config["DB_HOST"]
        params["port"] = app.config["DB_PORT"]

        # connect to the PostgreSQL server
        print("Connecting to the PostgreSQL database...")
        conn = psycopg2.connect(**params)

        conn.set_client_encoding("UTF8")

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print("PostgreSQL database version:")
        cur.execute("SELECT version()")

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        cur.close()
    except (FileNotFoundError, NoSectionError, psycopg2.DatabaseError) as error:
        print(error)
    return conn


def disconnect(conn):
    """Close the connexion"""
    conn.close()
    print("Database connection closed.")


def execute_command(conn, query, params=None):
    """Execute a SQL command"""
    cur = conn.cursor()

    returning_value = None

    print(query)
    print("params", params)
    cur.execute(query, params)
    if "returning" in query.lower():
        returning_value = cur.fetchone()[0]

    # Close communication with the PostgreSQL database server
    cur.close()
    # Commit the changes
    conn.commit()
    return returning_value


def get_query(conn, query, params=None, return_dict=False):
    """Query data from db"""
    print(query)
    print("params", params)
    try:
        rows = None
        if return_dict:
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        else:
            cur = conn.cursor()
        cur.execute(query, params)
        rows = cur.fetchall()
        cur.close()
    except psycopg2.DatabaseError as error:
        print(error)
    return rows


if __name__ == "__main__":
    connect()
