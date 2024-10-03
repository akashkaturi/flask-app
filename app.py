from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

# Initialize app
app = Flask(__name__)

# uncomment the next line for MySQL Configuration
# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')
# uncomment the next line for sqlite db
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize Database
db = SQLAlchemy(app)

# Initialize Marshmallow
ma = Marshmallow(app)

# Student Model
class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    major = db.Column(db.String(100), nullable=False)

    def __init__(self, name, age, major):
        self.name = name
        self.age = age
        self.major = major

# Student Schema
class StudentSchema(ma.Schema):
    class Meta:
        fields = ('id', 'name', 'age', 'major')

# Initialize schema
student_schema = StudentSchema()
students_schema = StudentSchema(many=True)

# Create a Student (POST)
@app.route('/student', methods=['POST'])
def add_student():
    name = request.json['name']
    age = request.json['age']
    major = request.json['major']

    new_student = Student(name, age, major)
    db.session.add(new_student)
    db.session.commit()

    return student_schema.jsonify(new_student)

# Get All Students (GET)
@app.route('/students', methods=['GET'])
def get_students():
    all_students = Student.query.all()
    result = students_schema.dump(all_students)
    return jsonify(result)

# Get Single Student (GET)
@app.route('/student/<id>', methods=['GET'])
def get_student(id):
    student = Student.query.get(id)
    return student_schema.jsonify(student)

# Update a Student (PUT)
@app.route('/student/<id>', methods=['PUT'])
def update_student(id):
    student = Student.query.get(id)

    name = request.json['name']
    age = request.json['age']
    major = request.json['major']

    student.name = name
    student.age = age
    student.major = major

    db.session.commit()

    return student_schema.jsonify(student)

# Delete Student (DELETE)
@app.route('/student/<id>', methods=['DELETE'])
def delete_student(id):
    student = Student.query.get(id)
    db.session.delete(student)
    db.session.commit()

    return student_schema.jsonify(student)

# Run Server
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)
