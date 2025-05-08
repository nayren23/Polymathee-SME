"""MySQL database interactions"""

# !/usr/bin/python

from configparser import NoSectionError
import mysql.connector
from mysql.connector import Error
from polymathee_sme import app


def connect():
    """Connect to the MySQL database server"""
    conn = None
    try:
        # read connection parameters
        params = {}
        params["database"] = app.config["DB_NAME"]
        params["user"] = app.config["DB_USER"]
        params["password"] = app.config["DB_PWD"]
        params["host"] = app.config["DB_HOST"]
        params["port"] = app.config["DB_PORT"]

        # connect to the PostgreSQL server
        print("Connecting to the Mysql database...")
        conn = mysql.connector.connect(**params)

        # create a cursor
        cur = conn.cursor()

        # execute a statement
        print("Mysql database version:")
        cur.execute("SELECT version()")

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        cur.close()
    except (FileNotFoundError, NoSectionError, Error) as error:
        print("Database connection failed:", error)
        conn = None
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
        returning_value = cur.lastrowid

    # Commit the changes
    conn.commit()
    # Close communication with the PostgreSQL database server
    cur.close()
    return returning_value


def get_query(conn, query, params=None, return_dict=False):
    """Query data from db"""
    if conn is None:
        raise ValueError("No database connection available.")

    print(query)
    print("params", params)
    rows = None
    try:
        if return_dict:
            cur = conn.cursor(dictionary=True)
        else:
            cur = conn.cursor()

        cur.execute(query, params)
        rows = cur.fetchall()
        cur.close()
    except Error as error:
        print(error)
    return rows


if __name__ == "__main__":
    connect()
