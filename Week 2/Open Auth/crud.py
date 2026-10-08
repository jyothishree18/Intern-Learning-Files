from flask import request, jsonify

from auth import login_required, role_required

from werkzeug.security import generate_password_hash


def register_routes(app, db):

    # =========================================================
    # STUDENT TABLE
    # =========================================================

    class Student(db.Model):

        id = db.Column(
            db.Integer,
            primary_key=True
        )

        name = db.Column(
            db.String(100),
            nullable=False
        )

        age = db.Column(
            db.Integer,
            nullable=False
        )

        department = db.Column(
            db.String(100),
            nullable=False
        )

        email = db.Column(
            db.String(100),
            unique=True,
            nullable=False
        )

        phone = db.Column(
            db.String(15),
            nullable=False
        )

        password = db.Column(
            db.String(255),
            nullable=False
        )

        # Role for authorization
        role = db.Column(
            db.String(20),
            nullable=False,
            default="student"
        )


    # =========================================================
    # GET ALL STUDENTS
    # Any authenticated Google user can access
    # =========================================================

    @app.route("/students", methods=["GET"])
    @login_required
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
                "phone": student.phone,
                "role": student.role
            })

        return jsonify(result)


    # =========================================================
    # GET STUDENT BY ID
    # Any authenticated Google user can access
    # =========================================================

    @app.route("/students/<int:id>", methods=["GET"])
    @login_required
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

        student = db.session.get(
            Student,
            id
        )

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
            "phone": student.phone,
            "role": student.role

        })


    # =========================================================
    # POST - ADD STUDENT
    # ADMIN ONLY
    # =========================================================

    @app.route("/students", methods=["POST"])
    @role_required("admin")
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

                role:
                  type: string

        responses:
          201:
            description: Student added successfully

          403:
            description: Access denied
        """

        data = request.get_json()

        if not data:

            return jsonify({
                "error": "Request body is required"
            }), 400


        # -----------------------------------------------------
        # Check required fields
        # -----------------------------------------------------

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


        # -----------------------------------------------------
        # Check whether email already exists
        # -----------------------------------------------------

        existing_student = Student.query.filter_by(
            email=data["email"]
        ).first()

        if existing_student:

            return jsonify({
                "error": "Email already exists"
            }), 409


        # -----------------------------------------------------
        # Hash password
        # -----------------------------------------------------

        hashed_password = generate_password_hash(
            data["password"]
        )


        # -----------------------------------------------------
        # Create student
        # -----------------------------------------------------

        student = Student(

            id=data.get("id"),

            name=data["name"],

            age=data["age"],

            department=data["department"],

            email=data["email"],

            phone=data["phone"],

            password=hashed_password,

            role=data.get(
                "role",
                "student"
            )
        )


        db.session.add(student)

        db.session.commit()


        return jsonify({

            "message": "Student added successfully",

            "id": student.id,

            "role": student.role

        }), 201

    # PUT - UPDATE STUDENT
    # ADMIN ONLY
    @app.route("/students/<int:id>", methods=["PUT"])
    @role_required("admin")
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

                role:
                  type: string

        responses:

          200:
            description: Student updated successfully

          404:
            description: Student not found

          403:
            description: Access denied
        """

        student = db.session.get(
            Student,
            id
        )

        if not student:

            return jsonify({
                "message": "Student not found"
            }), 404


        data = request.get_json()

        if not data:

            return jsonify({
                "error": "Request body is required"
            }), 400


        # -----------------------------------------------------
        # Update fields
        # -----------------------------------------------------

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


        # -----------------------------------------------------
        # Update password
        # -----------------------------------------------------

        if "password" in data:

            student.password = generate_password_hash(
                data["password"]
            )


        # -----------------------------------------------------
        # Update role
        # -----------------------------------------------------

        if "role" in data:

            if data["role"] not in [
                "admin",
                "student"
            ]:

                return jsonify({
                    "error": "Role must be admin or student"
                }), 400

            student.role = data["role"]


        db.session.commit()


        return jsonify({

            "message": "Student updated successfully",

            "role": student.role

        })


    # =========================================================
    # DELETE STUDENT
    # ADMIN ONLY
    # =========================================================

    @app.route("/students/<int:id>", methods=["DELETE"])
    @role_required("admin")
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

          403:
            description: Access denied
        """

        student = db.session.get(
            Student,
            id
        )

        if not student:

            return jsonify({
                "message": "Student not found"
            }), 404

        db.session.delete(student)
        db.session.commit()
        return jsonify({
            "message": "Student deleted successfully"
        })