import os
import jwt
from datetime import datetime, timedelta, timezone

from flask import Flask, jsonify, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flasgger import Swagger
from authlib.integrations.flask_client import OAuth
from dotenv import load_dotenv


# ---------------- LOAD .ENV ----------------

load_dotenv(
    os.path.join(
        os.path.dirname(__file__),
        ".env"
    ),
    override=True
)


# ---------------- FLASK APP ----------------

app = Flask(__name__)

app.config["SECRET_KEY"] = os.getenv(
    "SECRET_KEY",
    "student-management-secret"
)

# ---------------- JWT CONFIGURATION ----------------

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = "HS256"


# ---------------- GOOGLE OAUTH ----------------

oauth = OAuth(app)

google = oauth.register(
    name="google",
#------------CLIENT ID------------------
   client_id=os.getenv("GOOGLE_CLIENT_ID"),

#------------CLIENT SECRET---------------
client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url=(
        "https://accounts.google.com/.well-known/openid-configuration"
    ),

    client_kwargs={
        "scope": "openid email profile"
    }
)


# ---------------- SWAGGER ----------------

swagger = Swagger(
    app,
    template={
        "swagger": "2.0",

        "securityDefinitions": {
            "basicAuth": {
                "type": "basic",
                "description": "Basic Authentication"
            },

            "BearerAuth": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Enter: Bearer <JWT token>"
            }
        },

        "security": [
            {
                "basicAuth": []
            }
        ]
    }
)


# ---------------- DATABASE ----------------

app.config["SQLALCHEMY_DATABASE_URI"] = (
    f"mysql+pymysql://{os.getenv('DB_USER')}:"
    f"{os.getenv('DB_PASSWORD')}@"
    f"{os.getenv('DB_HOST')}/"
    f"{os.getenv('DB_NAME')}"
)

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# ---------------- CREATE DATABASE TABLES ----------------

with app.app_context():
    db.create_all()


# ---------------- CRUD ----------------

import crud

crud.register_routes(app, db)


# =========================================================
# JWT AUTHENTICATION
# =========================================================

from functools import wraps
from flask import request


def jwt_required(f):

    @wraps(f)
    def decorated(*args, **kwargs):

        auth_header = request.headers.get("Authorization")

        # Check whether Authorization header exists
        if not auth_header:
            return jsonify({
                "error": "JWT token required"
            }), 401

        try:
            # Expected format:
            # Authorization: Bearer <token>

            parts = auth_header.split(" ")

            if len(parts) != 2 or parts[0].lower() != "bearer":
                return jsonify({
                    "error": "Invalid Authorization header format"
                }), 401

            token = parts[1]

            # Decode and verify JWT
            payload = jwt.decode(
                token,
                JWT_SECRET,
                algorithms=[JWT_ALGORITHM]
            )

            # Store decoded user information
            request.user = payload

        except jwt.ExpiredSignatureError:

            return jsonify({
                "error": "JWT token has expired"
            }), 401

        except jwt.InvalidTokenError:

            return jsonify({
                "error": "Invalid JWT token"
            }), 401

        return f(*args, **kwargs)

    return decorated


# =========================================================
# GOOGLE LOGIN
# =========================================================

@app.route("/login/google")
def google_login():

    redirect_uri = url_for(
        "google_callback",
        _external=True
    )

    return google.authorize_redirect(
        redirect_uri
    )


# =========================================================
# GOOGLE CALLBACK + JWT GENERATION
# =========================================================

@app.route("/auth/google/callback")
def google_callback():

    token = google.authorize_access_token()

    user = token.get("userinfo")

    if not user:

        return jsonify({
            "error": "Unable to get Google user information"
        }), 400

    # Store user in Flask session
    session["user"] = {
        "email": user.get("email"),
        "name": user.get("name"),
        "google_id": user.get("sub")
    }

    # ---------------- CREATE JWT ----------------

    payload = {
        "email": user.get("email"),
        "name": user.get("name"),

        # JWT expires after 1 hour
        "exp": datetime.now(timezone.utc) + timedelta(hours=1)
    }

    access_token = jwt.encode(
        payload,
        JWT_SECRET,
        algorithm=JWT_ALGORITHM
    )

    return jsonify({
        "message": "Google login successful",

        # JWT token
        "access_token": access_token,

        "user": session["user"]
    })


# =========================================================
# PROTECTED TEST ROUTE
# =========================================================

@app.route("/protected")
@jwt_required
def protected():

    return jsonify({
        "message": "JWT authentication successful",
        "user": request.user
    })


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return jsonify({
        "message": "Logged out successfully"
    })


# =========================================================
# DEBUG GOOGLE
# =========================================================

@app.route("/debug/google")
def debug_google():

    return {
        "client_id": google.client_id
    }


# =========================================================
# RUN APP
# =========================================================

if __name__ == "__main__":
    app.run(debug=True)