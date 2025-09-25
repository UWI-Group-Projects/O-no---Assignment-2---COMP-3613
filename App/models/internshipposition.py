from App.database import db

class InternshipPosition(db.Model):
    positionID = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    status = db.Column(db.String(50), default="Pending")

    employerID = db.Column(db.Integer, db.ForeignKey("employer.employerID"), nullable=False)
    studentID = db.Column(db.Integer, db.ForeignKey("student.studentID"), nullable=True) 

    def __init__(self, title, employerID, studentID=None, status="Pending"):
        self.title = title
        self.employerID = employerID
        self.studentID = studentID
        self.status = status

    def set_status(self, status):
        self.status = status
