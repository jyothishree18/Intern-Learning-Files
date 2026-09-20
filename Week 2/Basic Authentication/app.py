from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from auth import basic_auth
app = Flask(__name__)

# Database configuration
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///students.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Student table
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    department = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    phone = db.Column(db.String(15), nullable=False)


# Create database
with app.app_context():
    db.create_all()

import crud

crud.register_routes(app, db, Student)

if __name__ == "__main__":
    app.run(debug=True)