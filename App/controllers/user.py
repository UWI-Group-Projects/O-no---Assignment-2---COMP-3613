from App.models import User
from App.database import db
from App.models.student import Student


def create_staff(username, password):
    newuser = Staff(username=username, password=password)
    try:
        db.session.add(newuser)
        db.session.commit()
        return newuser
    except:
        return None

def create_employer(username, password):
    newuser = Employer(username=username, password=password)
    try:
        db.session.add(newuser)
        db.session.commit()
        return newuser
    except:
        return None 

def create_student(username, password):
    newuser = Student(username=username, password=password)
    try:
        db.session.add(newuser)
        db.session.commit()
        return newuser
    except:
        return None 
    
def get_all_employers():
    return Employer.query.all()
def get_all_employers_json():
    employer_list = Employer.query.all()
    return [employer.get_json() for employer in employer_list]

def get_employer_by_id(employer_id):
    return Employer.query.get(employer_id)
def get_employer_by_username(username):
    return Employer.query.filter_by(username=username).first()
def delete_employer(employer_id):
    employer = Employer.query.get(employer_id)
    if not employer:
        return False
    try:
        db.session.delete(employer)
        db.session.commit()
        return True
    except:
        return False

def get_all_students():
    return Student.query.all()
def get_all_students_json():
    student_list = Student.query.all()
    return [student.get_json() for student in student_list]
def get_student_by_id(student_id):
    return Student.query.get(student_id)
def get_student_by_username(username):
    return Student.query.filter_by(username=username).first()
def delete_student(student_id):
    student = Student.query.get(student_id)
    if not student:
        return False
    try:
        db.session.delete(student)
        db.session.commit()
        return True
    except:
        return False
        
def get_all_staff():
    return Staff.query.all()
def get_all_staff_json():
    staff_list = Staff.query.all()
    return [staff.get_json() for staff in staff_list]   
def get_staff_by_id(staff_id):
    return Staff.query.get(staff_id)
def get_staff_by_username(username):
    return Staff.query.filter_by(username=username).first()
def delete_staff(staff_id):
    staff = Staff.query.get(staff_id)
    if not staff:
        return False
    try:
        db.session.delete(staff)
        db.session.commit()
        return True
    except:
        return False
from App.models.employer import Employer
from App.models.staff import Staff
from flask_login import login_user, current_user
from functools import wraps
def staff_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not isinstance(current_user, Staff):
            return "Unauthorized", 401
        return func(*args, **kwargs)
    return wrapper
def initialize():
    db.drop_all()
    db.create_all()
    bob = create_staff('bob', 'bobpass')
    alice = create_staff('alice', 'alicepass')
    return [bob, alice]
    db.session.commit()
    return [bob, alice]

