from functools import wraps

from flask import request, jsonify, session
from werkzeug.security import check_password_hash
import pymysql


# =========================================================
# DATABASE CONNECTION
# =========================================================

def get_db_connection():

    return pymysql.connect(
        host="localhost",
        user="root",
        password="mohi2411",
        database="student_db",
        cursorclass=pymysql.cursors.DictCursor
    )


# =========================================================
# BASIC AUTHENTICATION
# DEMO 2
# =========================================================

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


# =========================================================
# LOGIN REQUIRED
# DEMO 3 - GOOGLE AUTHENTICATION
# =========================================================

def login_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        # Check whether Google user is stored in session
        if "user" not in session:

            return jsonify({
                "error": "Login required"
            }), 401

        return f(*args, **kwargs)

    return decorated


# =========================================================
# ROLE BASED AUTHORIZATION
# DEMO 3
# =========================================================

def role_required(required_role):

    def decorator(f):

        @wraps(f)
        def decorated(*args, **kwargs):

            # First check authentication
            if "user" not in session:

                return jsonify({
                    "error": "Login required"
                }), 401

            # Get logged-in Google user's email
            email = session["user"].get("email")

            if not email:

                return jsonify({
                    "error": "User email not available"
                }), 401

            # Connect to MySQL
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute(
                """
                SELECT role
                FROM student
                WHERE email = %s
                """,
                (email,)
            )

            user = cursor.fetchone()

            cursor.close()
            conn.close()

            # User does not exist in student table
            if not user:

                return jsonify({
                    "error": "User not found"
                }), 403

            # Check user's role
            if user["role"] != required_role:

                return jsonify({
                    "error": "Access denied"
                }), 403

            # Role matches
            return f(*args, **kwargs)

        return decorated

    return decorator