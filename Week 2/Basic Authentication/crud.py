from flask import request, jsonify
from auth import basic_auth
from werkzeug.security import generate_password_hash


def register_routes(app, db):

    # Student table
    class Student(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(100), nullable=False)
        age = db.Column(db.Integer, nullable=False)
        department = db.Column(db.String(100), nullable=False)
        email = db.Column(db.String(100), unique=True, nullable=False)
        phone = db.Column(db.String(15), nullable=False)
        password = db.Column(db.String(255), nullable=False)

    # GET all students
    @app.route("/students", methods=["GET"])
    @basic_auth
    def get_students():
        """
        Get all students
        ---
        tags:
          - Students
        responses:
          200:
            description: List of all students
        """

        students = Student.query.all()
        result = []

        for student in students:
            result.append({
                "id": student.id,
                "name": student.name,
                "age": student.age,
                "department": student.department,
                "email": student.email,
                "phone": student.phone
            })

        return jsonify(result)

    # GET student by ID
    @app.route("/students/<int:id>", methods=["GET"])
    @basic_auth
    def get_student(id):
        """
        Get a student by ID
        ---
        tags:
          - Students
        parameters:
          - name: id
            in: path
            required: true
            type: integer
        responses:
          200:
            description: Student details
          404:
            description: Student not found
        """

        student = db.session.get(Student, id)

        if not student:
            return jsonify({
                "message": "Student not found"
            }), 404

        return jsonify({
            "id": student.id,
            "name": student.name,
            "age": student.age,
            "department": student.department,
            "email": student.email,
            "phone": student.phone
        })

    # POST - Add student
    @app.route("/students", methods=["POST"])
    @basic_auth
    def add_student():
        """
        Add a new student
        ---
        tags:
          - Students
        parameters:
          - in: body
            name: body
            required: true
            schema:
              type: object
              required:
                - name
                - age
                - department
                - email
                - phone
                - password
              properties:
                name:
                  type: string
                age:
                  type: integer
                department:
                  type: string
                email:
                  type: string
                phone:
                  type: string
                password:
                  type: string
        responses:
          201:
            description: Student added successfully
        """

        data = request.get_json()

        # Check required fields
        required_fields = [
            "name",
            "age",
            "department",
            "email",
            "phone",
            "password"
        ]

        for field in required_fields:
            if field not in data:
                return jsonify({
                    "error": f"{field} is required"
                }), 400

        # Hash password before storing
        hashed_password = generate_password_hash(data["password"])

        student = Student(
            id=data.get("id"),
            name=data["name"],
            age=data["age"],
            department=data["department"],
            email=data["email"],
            phone=data["phone"],
            password=hashed_password
        )

        db.session.add(student)
        db.session.commit()

        return jsonify({
            "message": "Student added successfully",
            "id": student.id
        }), 201

    # PUT - Update student
    @app.route("/students/<int:id>", methods=["PUT"])
    @basic_auth
    def update_student(id):
        """
        Update a student
        ---
        tags:
          - Students
        parameters:
          - name: id
            in: path
            required: true
            type: integer
          - in: body
            name: body
            required: true
            schema:
              type: object
              properties:
                name:
                  type: string
                age:
                  type: integer
                department:
                  type: string
                email:
                  type: string
                phone:
                  type: string
                password:
                  type: string
        responses:
          200:
            description: Student updated successfully
          404:
            description: Student not found
        """

        student = db.session.get(Student, id)

        if not student:
            return jsonify({
                "message": "Student not found"
            }), 404

        data = request.get_json()

        if "name" in data:
            student.name = data["name"]

        if "age" in data:
            student.age = data["age"]

        if "department" in data:
            student.department = data["department"]

        if "email" in data:
            student.email = data["email"]

        if "phone" in data:
            student.phone = data["phone"]

        # Hash new password if provided
        if "password" in data:
            student.password = generate_password_hash(
                data["password"]
            )

        db.session.commit()

        return jsonify({
            "message": "Student updated successfully"
        })

    # DELETE - Delete student
    @app.route("/students/<int:id>", methods=["DELETE"])
    @basic_auth
    def delete_student(id):
        """
        Delete a student
        ---
        tags:
          - Students
        parameters:
          - name: id
            in: path
            required: true
            type: integer
        responses:
          200:
            description: Student deleted successfully
          404:
            description: Student not found
        """

        student = db.session.get(Student, id)

        if not student:
            return jsonify({
                "message": "Student not found"
            }), 404

        db.session.delete(student)
        db.session.commit()

        return jsonify({
            "message": "Student deleted successfully"
        })