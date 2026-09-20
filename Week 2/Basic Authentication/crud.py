from flask import request, jsonify
from auth import basic_auth

def register_routes(app, db, Student):

    # GET all students
    @app.route("/students", methods=["GET"])
    @basic_auth
    def get_students():
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
        student = db.session.get(Student, id)

        if not student:
            return jsonify({"message": "Student not found"}), 404

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
        data = request.get_json()

        student = Student(
            id=data.get("id"),
            name=data["name"],
            age=data["age"],
            department=data["department"],
            email=data["email"],
            phone=data["phone"]
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
        student = db.session.get(Student, id)

        if not student:
            return jsonify({"message": "Student not found"}), 404

        data = request.get_json()

        student.name = data["name"]
        student.age = data["age"]
        student.department = data["department"]
        student.email = data["email"]
        student.phone = data["phone"]

        db.session.commit()

        return jsonify({
            "message": "Student updated successfully"
        })


    # DELETE - Delete student
    @app.route("/students/<int:id>", methods=["DELETE"])
    @basic_auth
    def delete_student(id):
        student = db.session.get(Student, id)

        if not student:
            return jsonify({"message": "Student not found"}), 404

        db.session.delete(student)
        db.session.commit()

        return jsonify({
            "message": "Student deleted successfully"
        })