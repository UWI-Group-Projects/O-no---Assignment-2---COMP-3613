import os, tempfile, pytest, logging, unittest
from werkzeug.security import check_password_hash, generate_password_hash

from App.main import create_app
from App.database import db, create_db
from App.models import User, Employer, Staff, Student, InternshipPosition
from App.controllers import (
    create_user,
    get_all_users_json,
    login,
    get_user,
    get_user_by_username,
    update_user)

LOGGER = logging.getLogger(__name__)


class UserUnitTests(unittest.TestCase):

    def test_new_user(self):
        user = User("bob", "bobpass")
        assert user.username == "bob"


    def test_get_json(self):
        user = User("bob", "bobpass")
        user_json = user.get_json()
        self.assertDictEqual(user_json, {"id":None, "username":"bob"})
    
    def test_hashed_password(self):
        password = "mypass"
        hashed = generate_password_hash(password, method='sha256')
        user = User("bob", password)
        assert user.password != password

    def test_check_password(self):
        password = "mypass"
        user = User("bob", password)
        assert user.check_password(password)



@pytest.fixture(autouse=True, scope="module")
def empty_db():
    app = create_app({'TESTING': True, 'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db'})
    create_db()
    yield app.test_client()
    db.drop_all()


def test_authenticate():
    user = create_user("bob", "bobpass")
    assert login("bob", "bobpass") != None

class UsersIntegrationTests(unittest.TestCase):

    def test_create_user(self):
        user = create_user("rick", "bobpass")
        assert user.username == "rick"

    def test_get_all_users_json(self):
        users_json = get_all_users_json()
        self.assertListEqual([{"id":1, "username":"bob"}, {"id":2, "username":"rick"}], users_json)


    def test_update_user(self):
        update_user(1, "ronnie")
        user = get_user(1)
        assert user.username == "ronnie"

def test_create_internship():
    employer = Employer(companyName="TestCorp")
    db.session.add(employer)
    db.session.commit()

    position = employer.create_position("Software Intern", "Desc")
    assert position.title == "Software Intern"
    assert position.employerID == employer.employerID
    assert position.status == "Pending"

def test_empty_title_disallowed():
    employer = Employer(companyName="TestCorp")
    db.session.add(employer)
    db.session.commit()
    
    import pytest
    with pytest.raises(Exception):
        employer.create_position("", "Desc")

def test_add_student_to_shortlist():
    employer = Employer(companyName="TestCorp")
    staff = Staff(username="staff1", password="pass")
    student = Student(name="John Test")
    db.session.add_all([employer, staff, student])
    db.session.commit()

    position = employer.create_position("Data Intern", "Desc")
    result = staff.add_student_to_position(student.studentID, position.positionID)
    assert result is True
    assert position.studentID == student.studentID

def test_dusplicate_student_not_added():
    employer = Employer(companyName="TestCorp")
    staff = Staff(username="staff1", password="pass")
    student = Student(name="John Test")
    db.session.add_all([employer, staff, student])
    db.session.commit()

    position = employer.create_position("Data Intern", "Desc")
    staff.add_student_to_position(student.studentID, position.positionID)
    staff.add_student_to_position(student.studentID, position.positionID)
    assert position.studentID == student.studentID

def test_accept_student():
    employer = Employer(companyName="TestCorp")
    staff = Staff(username="staff1", password="pass")
    student = Student(name="John Test")
    db.session.add_all([employer, staff, student])
    db.session.commit()

    position = employer.create_position("Web Intern", "Desc")
    staff.add_student_to_position(student.studentID, position.positionID)
    result = employer.accept_student(position.positionID, student.studentID)
    assert result is True
    assert position.status == "Accepted"

def test_reject_student():
    employer = Employer(companyName="TestCorp")
    staff = Staff(username="staff1", password="pass")
    student = Student(name="John Test")
    db.session.add_all([employer, staff, student])
    db.session.commit()

    position = employer.create_position("Web Intern", "Desc")
    staff.add_student_to_position(student.studentID, position.positionID)
    result = employer.reject_student(position.positionID, student.studentID)
    assert result is True
    assert position.status == "Rejected"

def test_integration_accept_flow():
    employer = Employer(companyName="TestCorp")
    staff = Staff(username="staff1", password="pass")
    student = Student(name="John Test")
    db.session.add_all([employer, staff, student])
    db.session.commit()

    position = employer.create_position("Full Stack Intern", "Desc")
    staff.add_student_to_position(student.studentID, position.positionID)
    assert position.studentID == student.studentID
    employer.accept_student(position.positionID, student.studentID)
    assert position.status == "Accepted"
    positions = student.view_shortlist_positions()
    assert len(positions) == 1
    assert positions[0]['positionID'] == position.positionID

def test_integration_reject_flow():
    employer = Employer(companyName="TestCorp")
    staff = Staff(username="staff1", password="pass")
    student = Student(name="John Test")
    db.session.add_all([employer, staff, student])
    db.session.commit()

    position = employer.create_position("Data Analyst Intern", "Desc")
    staff.add_student_to_position(student.studentID, position.positionID)
    assert position.studentID == student.studentID
    employer.reject_student(position.positionID, student.studentID)
    assert position.status == "Rejected"
    status = student.view_employer_response(position.positionID)
    assert status == "Rejected"
