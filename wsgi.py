import click, pytest, sys
from flask.cli import with_appcontext, AppGroup

from App.database import db, get_migrate
from App.models import (User, Employer, Staff, Student, InternshipPosition)
from App.main import create_app
from App.controllers import ( create_user, get_all_users_json, get_all_users, initialize )


# This commands file allow you to create convenient CLI commands for testing controllers

app = create_app()
migrate = get_migrate(app)

# This command creates and initializes the database
@app.cli.command("init", help="Creates and initializes the database")
def init():
    initialize()

    admin = User(username="admin", password="adminpass")
    rob = User(username="rob", password="robpass")
    sally = User(username="sally", password="sallypass")

    employer1 = Employer(companyName="SquigglyWiggly")
    employer2 = Employer(companyName="AwHellNahCorporation")

    staff1 = Staff(username="alice", password="alicepass")
    staff2 = Staff(username="bob", password="bobpass")

    student1 = Student(name="John Doe")
    student2 = Student(name="Jane Smith")

    pos1 = InternshipPosition(title="Software Intern", employerID=1)
    pos2 = InternshipPosition(title="Data Analyst Intern", employerID=2)

    db.session.add_all([
        admin, rob, sally,
        employer1, employer2,
        staff1, staff2,
        student1, student2,
        pos1, pos2
    ])
    db.session.commit()
    print('database intialized')

# for internshiop  (Employer) create internship position
@app.cli.command("create-position", help="Employer creates an internship position")
def create_position_command():
    employers = Employer.query.all()
    print("Employers:", employers)

    employer_id = input("Enter the employer id creating this position: ")
    title = input("Enter the title of the internship position: ")
    description = input("Enter a description: ")

    employer = Employer.query.get(employer_id)
    if employer:
        position = InternshipPosition(title=title, status="open", employerID=employer.employerID)
        db.session.add(position)
        db.session.commit()
        print(f"Internship '{title}' created successfully for employer {employer.companyName}")
    else:
        print("Invalid employer ID.")


# staff command where (Staff) Add student to an internship positions shortlist
@app.cli.command("add-student", help="Staff adds a student to an internship position")
def add_student_command():

    students = Student.query.all()
    print("Students:", students)
    positions = InternshipPosition.query.all()
    print("Positions:", positions)

    student_id = input("Enter the student id to add: ")
    position_id = input("Enter the internship position id: ")

    student = Student.query.get(student_id)
    position = InternshipPosition.query.get(position_id)

    if student and position:
        position.studentID = student.studentID
        db.session.commit()
        print(f"Student '{student.name}' added to internship '{position.title}' shortlist.")
    else:
        print("Invalid student ID or position ID.")

# employer reject/accept (Employer) accept/reject student from shortlist
@app.cli.command("review-student", help="Employer accepts or rejects a student from a shortlist")
def review_student_command():

    positions = InternshipPosition.query.all()
    print("Positions:", positions)

    position_id = input("Enter the internship position id: ")
    position = InternshipPosition.query.get(position_id)

    if position and position.studentID:
        decision = input("Enter decision (accept/reject): ").lower()
        if decision in ["accepted", "rejected"]:
            position.status = decision
            db.session.commit()
            print(f"Student {position.studentID} has been {decision}ed for position '{position.title}'.")
        else:
            print("Invalid decision. Please enter 'accept' or 'reject'.")
    else:
        print("No student assigned to this position or invalid position ID.")

# for student view (Student) view shortlisted positions and employer response
@app.cli.command("view-shortlist", help="Student views their shortlisted positions and employer response")
def view_shortlist_command():
    
    students = Student.query.all()
    print("Students:", students)

    student_id = input("Enter the student id: ")
    student = Student.query.get(student_id)

    if student:
        positions = InternshipPosition.query.filter_by(studentID=student.studentID).all()

        if positions:
            for pos in positions:
                print(f"Position: {pos.title}, Status: {pos.status}")
        else:
            print("No positions found for this student.")
    else:
        print("Invalid student ID.")

'''
User Commands
'''

# Commands can be organized using groups

# create a group, it would be the first argument of the comand
# eg : flask user <command>
user_cli = AppGroup('user', help='User object commands') 

# Then define the command and any parameters and annotate it with the group (@)
@user_cli.command("create", help="Creates a user")
@click.argument("username", default="rob")
@click.argument("password", default="robpass")
def create_user_command(username, password):
    create_user(username, password)
    print(f'{username} created!')

# this command will be : flask user create bob bobpass

@user_cli.command("list", help="Lists users in the database")
@click.argument("format", default="string")
def list_user_command(format):
    if format == 'string':
        print(get_all_users())
    else:
        print(get_all_users_json())

app.cli.add_command(user_cli) # add the group to the cli

'''
Test Commands
'''

test = AppGroup('test', help='Testing commands') 

@test.command("user", help="Run User tests")
@click.argument("type", default="all")
def user_tests_command(type):
    if type == "unit":
        sys.exit(pytest.main(["-k", "UserUnitTests"]))
    elif type == "int":
        sys.exit(pytest.main(["-k", "UserIntegrationTests"]))
    else:
        sys.exit(pytest.main(["-k", "App"]))
    

app.cli.add_command(test)