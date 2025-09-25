![Tests](https://github.com/uwidcit/flaskmvc/actions/workflows/dev.yml/badge.svg)

# Flask MVC Template
A template for flask applications structured in the Model View Controller pattern [Demo](https://dcit-flaskmvc.herokuapp.com/). [Postman Collection](https://documenter.getpostman.com/view/583570/2s83zcTnEJ)


# Dependencies
* Python3/pip3
* Packages listed in requirements.txt

# Installing Dependencies
```bash
$ pip install -r requirements.txt
```

# Configuration Management
...

# Initializing the Database
When connecting the project to a fresh empty database ensure the appropriate configuration is set then file then run the following command:

```bash
$ flask init
```

---

# Custom CLI Commands

The following CLI commands were implemented in **wsgi.py** to simulate the interactions between Employers, Staff, and Students.

### 1. Initialize Database
Populate database with sample data:
```bash
$ flask init
```

### 2. Create Internship Position (Employer)
Allows an employer to create an internship position.
```bash
$ flask create-position
```
➡ Prompts: employer id, title, description.

### 3. Add Student to Position (Staff)
Staff can add a student to an internship position’s shortlist.
```bash
$ flask add-student
```
➡ Prompts: student id, position id.

### 4. Review Student (Employer)
Employer accepts or rejects a student from the shortlist.
```bash
$ flask review-student
```
➡ Prompts: position id, decision (`accept` or `reject`).

### 5. View Shortlist (Student)
Student views their shortlisted positions and employer responses.
```bash
$ flask view-shortlist
```
➡ Prompts: student id.

---

# User Commands

User commands are grouped under `flask user ...`

### Create User
```bash
$ flask user create <username> <password>
```

### List Users
```bash
$ flask user list string
$ flask user list json
```

---

# Testing Commands

Run tests using the `test` group.

### Run all user tests
```bash
$ flask test user
```

### Run unit or integration tests only
```bash
$ flask test user unit
$ flask test user int
```

Or run all tests:
```bash
$ pytest
```

---

# Running the Project
_For development:_
```bash
$ flask run
```

_For production (Gunicorn):_
```bash
$ gunicorn wsgi:app
```
