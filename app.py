from flask_sqlalchemy import SQLAlchemy
from flask import Flask
# from flask import request
from flask_cors import CORS
import json

app = Flask (__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///university.sqlite3'
CORS(app)

db = SQLAlchemy(app)
class students(db.Model):
   id = db.Column('student_id', db.Integer, primary_key = True)
   name = db.Column(db.String(100))
   age =db.Column(db.Integer)

   
   def __init__(self, name,age):
        self.name = name
        self.age = age
        
  
@app.route('/')
def show_all():
    res=[]
    for student in students.query.all():
        res.append({"id":student.id,"name":student.name,"age":student.age})
    return  (json.dumps(res))
   
 
@app.route('/new_student', methods = ['GET', 'POST'])
def new_student():
    request_data = request.get_json()
    name= request_data["name"]
    age = request_data["age"]
 
    newStudent= students(name,age)
    db.session.add (newStudent)
    db.session.commit()
    return "a new student add"

@app.route("/delete_student/<id>", methods=["DELETE"])
def delete_student(id):
    student = students.query.get(id)
    if student:
        db.session.delete(student)
        db.session.commit()
    return "student delete"

@app.route("/students/<int:student_id>", methods=["GET","PUT"])
def update_student(student_id):
    student = students.query.get(student_id)
    if student:
        student.name = request.json.get("name", student.name)
        student.age= request.json.get("age", student.age)
        stu_upd={"id":student.id,"name":student.name,"age":student.age}
        db.session.commit()
        return (json.dumps(stu_upd))
    else:
        return "error Student not found."



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)