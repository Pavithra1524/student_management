from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config import Config
from models import db, Student

app = Flask(__name__)
app.config.from_object(Config)

CORS(app)  # Enable CORS for frontend requests
db.init_app(app)

# Create Database Tables
with app.app_context():
    db.create_all()

# Add Student API
@app.route('/student/add/', methods=['POST'])
def add_student():
    data = request.json
    new_student = Student(name=data['name'], age=data['age'], email=data['email'])
    db.session.add(new_student)
    db.session.commit()
    return jsonify({"message": "Student added successfully"}), 201

# Get All Students API
@app.route('/student/lists/', methods=['GET'])
def get_students():
    students = Student.query.all()
    return jsonify([student.to_dict() for student in students])

# Get Student by ID API
@app.route('/student/get/<int:id>', methods=['GET'])
def get_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({"message": "Student not found"}), 404
    return jsonify(student.to_dict())

# Update Student API
@app.route('/student/update/<int:id>', methods=['PATCH'])
def update_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({"message": "Student not found"}), 404

    data = request.json
    student.name = data.get('name', student.name)
    student.age = data.get('age', student.age)
    student.email = data.get('email', student.email)
    db.session.commit()
    return jsonify({"message": "Student updated successfully"})

# Delete Student API
@app.route('/student/delete/<int:id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get(id)
    if not student:
        return jsonify({"message": "Student not found"}), 404

    db.session.delete(student)
    db.session.commit()
    return jsonify({"message": "Student deleted successfully"})


@app.route('/')
def home():
    return "Student Management API is running!"


if __name__ == '__main__':
    app.run(debug=True)
