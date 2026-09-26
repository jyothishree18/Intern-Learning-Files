from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from auth import basic_auth
from flasgger import Swagger
app = Flask(__name__)
swagger = Swagger(app, template={
    "swagger": "2.0",
    "securityDefinitions": {
        "basicAuth": {
            "type": "basic",
            "description": "Basic Authentication"
        }
    },
    "security": [
        {
            "basicAuth": []
        }
    ]
})
# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Create database
with app.app_context():
    db.create_all()

import crud

crud.register_routes(app, db)

if __name__ == "__main__":
    app.run(debug=True)