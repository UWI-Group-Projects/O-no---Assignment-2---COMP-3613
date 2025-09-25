from App.database import db
from .internshipposition import InternshipPosition
from .student import Student

class Employer(db.Model):
    employerID = db.Column(db.Integer, primary_key=True)
    companyName = db.Column(db.String(120), nullable=False)

    positions = db.relationship("InternshipPosition", backref="employer", lazy=True)

    def __init__(self, companyName):
        self.companyName = companyName

    def create_position(self, title, desc):
        new_position = InternshipPosition(title=title, employerID=self.employerID)
        db.session.add(new_position)
        db.session.commit()
        return new_position
    
    def accept_student(self, positionID, studentID):
        position = InternshipPosition.query.filter_by(positionID=positionID, employerID=self.employerID).first()
        if position and position.studentID == studentID:
            position.set_status("Accepted")
            db.session.commit()
            return True
        return False
    
    def reject_student(self, positionID, studentID):
        position = InternshipPosition.query.filter_by(positionID=positionID, employerID=self.employerID).first()
        if position and position.studentID == studentID:
            position.set_status("Rejected")
            db.session.commit()
            return True
        return False

    def view_shortlist(self, positionID):
        position = InternshipPosition.query.filter_by(positionID=positionID, employerID=self.employerID).first()
        if position and position.student:
            return [position.student.get_json()]
        return []
