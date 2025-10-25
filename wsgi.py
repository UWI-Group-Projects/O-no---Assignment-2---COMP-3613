import click, pytest, sys
from flask.cli import AppGroup, with_appcontext

from App.database import db, get_migrate
from App.models import User, Employer, Staff, Student, InternshipPosition
from App.main import create_app

# Import controllers
from App.controllers.user import (
    create_staff, create_employer, create_student,
    get_all_employers, get_all_employers_json, get_employer_by_id, get_employer_by_username, delete_employer,
    get_all_students, get_all_students_json, get_student_by_id,
    get_all_staff, get_all_staff_json, get_staff_by_id
)
from App.controllers.employer import create_position, accept_student, reject_student, view_shortlist_for_position
from App.controllers.staff import add_student_to_position
from App.controllers.student import view_shortlist_positions, view_employer_response

app = create_app()
migrate = get_migrate(app)

"""
INITIALIZATION
"""
@app.cli.command("init", help="Creates and initializes database")
def init():
    db.drop_all()
    db.create_all()

    # Create base data
    admin = User(username="admin", password="adminpass")
    staff1 = create_staff("alice", "alicepass")
    staff2 = create_staff("bob", "bobpass")
    employer1 = create_employer("SquigglyWiggly")
    employer2 = create_employer("AwHellNahCorporation")
    student1 = create_student("John Doe")
    student2 = create_student("Jane Smith")

    db.session.add_all([admin, employer1, employer2, student1, student2])
    db.session.commit()

    print(" Database initialized successfully.")


"""
EMPLOYER COMMANDS
"""
@app.cli.command("create-position", help="Employer creates internship position")
def create_position_command():
    employers = get_all_employers()
    print("Employers:")
    for e in employers:
        print(f"  {e.employerID}: {e.companyName}")

    employer_id = int(input("Employer ID: "))
    title = input("Position title: ")
    description = input("Description: ")

    pos = create_position(employer_id, title, description)
    if pos:
        print(f" Created position: {pos.title}")
    else:
        print("Invalid employer ID")


@app.cli.command("review-student", help="Employer reviews a shortlisted student")
def review_student_command():
    employer_id = int(input("Employer ID: "))
    position_id = int(input("Position ID: "))
    student_id = int(input("Student ID: "))
    decision = input("Decision (accept/reject): ").lower()

    if decision == "accept":
        result = accept_student(employer_id, position_id, student_id)
    else:
        result = reject_student(employer_id, position_id, student_id)

    print(" Updated" if result else " Failed")


"""
STAFF COMMANDS
"""
@app.cli.command("add-student", help="Staff shortlists a student for a position")
def add_student_command():
    students = get_all_students()
    print("Students:")
    for s in students:
        print(f"  {s.studentID}: {s.name}")

    student_id = int(input("Student ID: "))
    position_id = int(input("Position ID: "))

    if add_student_to_position(None, student_id, position_id):
        print(" Student shortlisted")
    else:
        print(" Failed to shortlist student")


"""
STUDENT COMMANDS
"""
@app.cli.command("view-shortlist", help="Student views applications and employer responses")
def view_shortlist_command():
    students = get_all_students()
    print("Students:")
    for s in students:
        print(f"  {s.studentID}: {s.name}")

    student_id = int(input("Student ID: "))
    apps = view_shortlist_positions(student_id)

    if not apps:
        print("No shortlisted positions.")
        return

    for app_item in apps:
        response = view_employer_response(student_id, app_item["positionID"])
        print(f"{app_item['title']} → Status: {response or 'Pending'}")


"""
USER MANAGEMENT COMMANDS
"""
user_cli = AppGroup("user", help="User management commands")

@user_cli.command("create", help="Create a new user by role")
@click.argument("role")
@click.argument("username")
@click.argument("password", required=False)
def create_user_cmd(role, username, password):
    role = role.lower()
    if role == "staff":
        user = create_staff(username, password)
    elif role == "employer":
        user = create_employer(username)
    elif role == "student":
        user = create_student(username)
    else:
        print(" Invalid role. Use: staff | employer | student")
        return
    print(f" Created {role}: {username}")


@user_cli.command("list", help="List all users by role")
@click.argument("role", default="all")
@click.argument("format", default="string")
def list_user_cmd(role, format):
    role = role.lower()

    if role == "employer":
        data = get_all_employers_json() if format == "json" else get_all_employers()
    elif role == "staff":
        data = get_all_staff_json() if format == "json" else get_all_staff()
    elif role == "student":
        data = get_all_students_json() if format == "json" else get_all_students()
    else:
        print(" Invalid role. Use: employer | staff | student")
        return

    print(data)

app.cli.add_command(user_cli)


"""
TEST COMMANDS
"""
test = AppGroup("test", help="Testing commands")

@test.command("user")
@click.argument("type", default="all")
def user_tests(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    sys.exit(pytest.main(["-k", "App"]))

app.cli.add_command(test)
