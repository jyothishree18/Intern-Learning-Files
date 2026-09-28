from functools import wraps
from flask import request, jsonify
from werkzeug.security import check_password_hash
import pymysql


def get_db_connection():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="mohi2411",
        database="student_db",
        cursorclass=pymysql.cursors.DictCursor
    )


def basic_auth(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        auth = request.authorization

        if not auth:
            return jsonify({
                "error": "Authentication required"
            }), 401

        # Use email as username
        email = auth.username
        password = auth.password

        conn = get_db_connection()

        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT *
            FROM student
            WHERE email = %s
            """,
            (email,)
        )

        student = cursor.fetchone()

        cursor.close()
        conn.close()

        if not student:
            return jsonify({
                "error": "Invalid email or password"
            }), 401

        # Compare entered password with stored hash
        if not check_password_hash(
            student["password"],
            password
        ):
            return jsonify({
                "error": "Invalid email or password"
            }), 401

        return f(*args, **kwargs)

    return decorated