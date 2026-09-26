from functools import wraps
from flask import request, jsonify
from werkzeug.security import check_password_hash
import sqlite3


def get_db_connection():
    conn = sqlite3.connect("students.db")
    conn.row_factory = sqlite3.Row
    return conn


def basic_auth(f):
    @wraps(f)
    def decorated(*args, **kwargs):

        auth = request.authorization

        if not auth:
            return jsonify({"error": "Authentication required"}), 401

        username = auth.username
        password = auth.password

        conn = get_db_connection()

        user = conn.execute(
            "SELECT * FROM users WHERE username = ?",
            (username,)
        ).fetchone()

        conn.close()

        if not user:
            return jsonify({"error": "Invalid username or password"}), 401

        if not check_password_hash(user["password"], password):
            return jsonify({"error": "Invalid username or password"}), 401

        return f(*args, **kwargs)

    return decorated