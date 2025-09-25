from App.database import db
from .internshipposition import InternshipPosition

class Student(db.Model):
    studentID = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)

    applications = db.relationship("InternshipPosition", backref="student", lazy=True)

    def __init__(self, name):
        self.name = name

    def view_shortlist_positions(self):
        return [app.get_json() for app in self.applications]
    
    def view_employer_response(self, positionID):
        position = InternshipPosition.query.filter_by(positionID=positionID, studentID=self.studentID).first()
        return position.status if position else "Not Found"
