from App.database import db

class Student(db.Model):
    __tablename__ = "student"

    studentID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    applications = db.relationship("InternshipPosition", backref="student", lazy=True)

    def __init__(self, name):
        self.name = name

    def to_json(self):
        return {
            "studentID": self.studentID,
            "name": self.name
        }