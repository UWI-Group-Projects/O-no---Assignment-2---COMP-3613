from flask_jwt_extended import create_access_token, jwt_required, JWTManager, get_jwt_identity, verify_jwt_in_request
from flask_jwt_extended import current_user
from functools import wraps
from flask import jsonify
from App.controllers.user import create_employer, create_staff, create_student
from flask_login import login_user, current_user

from App.models import User, Staff, Employer, Student
from App.database import db

def login(username, password):
    staff = Staff.query.filter_by(username=username).first()
    if staff and staff.check_password(password):
        return staff
    student = Student.query.filter_by(username=username).first()
    if student and student.check_password(password):
        return student
    
    employer = Employer.query.filter_by(username=username).first()
    if employer and employer.check_password(password):
        return employer 
    
    return None

def login_student(username, password):
    student = Student.query.filter_by(username=username).first()
    if student and student.check_password(password):
        login_user(student)
        return student
    return None

def login_staff(username, password):
    staff = Staff.query.filter_by(username=username).first()
    if staff and staff.check_password(password):
        login_user(staff)
        return staff
    return None

def login_employer(username, password):
    employer = Employer.query.filter_by(username=username).first()
    if employer and employer.check_password(password):
        login_user(employer)
        return employer
    return None

def initialize():
    db.drop_all()
    db.create_all()
    bob = create_staff('bob', 'bobpass')
    db.session.add(bob)
    db.session.commit()
    student1 = create_student('student1', 'student1pass')
    db.session.add(student1)
    db.session.commit()
    employer1 = create_employer('employer1', 'employer1pass', 'TechCorp')
    db.session.add(employer1) 


def staff_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not isinstance(current_user, Staff):
            return "Unauthorized", 401
        return func(*args, **kwargs)
    return wrapper

def employer_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not isinstance(current_user, Employer):
            return "Unauthorized", 401
        return func(*args, **kwargs)
    return wrapper

def student_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not isinstance(current_user, Student):
            return "Unauthorized", 401
        return func(*args, **kwargs)
    return wrapper