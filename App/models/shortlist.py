from App.database import db
from .student import Student
class Shortlist(db.Model):
    __tablename__ = "shortlist"

    shortlistID = db.Column(db.Integer, primary_key=True)
    studentID = db.Column(db.Integer, db.ForeignKey("student.studentID"), nullable=False)
    positionID = db.Column(db.Integer, db.ForeignKey("internshipposition.positionID"), nullable=False)

    def __init__(self, studentID, positionID):
        self.studentID = studentID
        self.positionID = positionID

    def to_json(self):
        return {
            "shortlistID": self.shortlistID,
            "studentID": self.studentID,
            "positionID": self.positionID
        }