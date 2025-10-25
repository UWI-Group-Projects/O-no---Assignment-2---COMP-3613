import click, pytest, sys
from flask.cli import AppGroup, with_appcontext

from App.database import db, get_migrate
from App.models import User, Employer, Staff, Student, InternshipPosition
from App.main import create_app

# Import controllers
from App.controllers.user import create_user, get_all_users, get_all_users_json
from App.controllers.employer import create_position, accept_student, reject_student, view_shortlist_for_position
from App.controllers.staff import add_student_to_position
from App.controllers.student import view_shortlist_positions, view_employer_response

app = create_app()
migrate = get_migrate(app)

@app.cli.command("init", help="Creates and initializes database")
def init():
    db.drop_all()
    db.create_all()

    admin = User(username="admin", password="adminpass")
    staff1 = Staff(username="alice", password="alicepass")
    staff2 = Staff(username="bob", password="bobpass")

    employer1 = Employer(companyName="SquigglyWiggly")
    employer2 = Employer(companyName="AwHellNahCorporation")

    student1 = Student(name="John Doe")
    student2 = Student(name="Jane Smith")

    db.session.add_all([admin, staff1, staff2, employer1, employer2, student1, student2])
    db.session.commit()

    print(" Database initialized")

# Employer creates position
@app.cli.command("create-position", help="Creates internship position")
def create_position_command():
    employers = Employer.query.all()
    print("Employers:", employers)

    employer_id = int(input("Employer ID: "))
    title = input("Position title: ")
    description = input("Description: ")

    pos = create_position(employer_id, title, description)
    if pos:
        print(f" Created: {pos.title}")
    else:
        print(" Invalid employer ID")

# Staff adds student to position
@app.cli.command("add-student", help="Shortlist a student")
def add_student_command():
    student_id = int(input("Student ID: "))
    position_id = int(input("Position ID: "))

    # Staff authentication skipped in CLI → pass None
    if add_student_to_position(None, student_id, position_id):
        print(" Student shortlisted")
    else:
        print(" Failed to shortlist student")

# Employer reviews student
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

# Student views positions + employer response
@app.cli.command("view-shortlist", help="Student views applications")
def view_shortlist_command():
    student_id = int(input("Student ID: "))
    apps = view_shortlist_positions(student_id)

    if not apps:
        print(" No shortlisted positions")
        return

    for app in apps:
        response = view_employer_response(student_id, app["positionID"])
        print(f"{app['title']} → Status: {response or 'Pending'}")

"""
USER COMMANDS
"""
user_cli = AppGroup("user", help="User commands")

@user_cli.command("create", help="Create a new user")
@click.argument("username")
@click.argument("password")
def create_user_cmd(username, password):
    user = create_user(username, password)
    print(f"User {user.username} created")

@user_cli.command("list", help="List all users")
@click.argument("format", default="string")
def list_user_cmd(format):
    if format == "string":
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli)

"""
TEST COMMANDS
"""
test = AppGroup("test", help="Testing")

@test.command("user")
@click.argument("type", default="all")
def user_tests(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    sys.exit(pytest.main(["-k", "App"]))

app.cli.add_command(test)