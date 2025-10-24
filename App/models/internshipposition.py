from App.database import db

class InternshipPosition(db.Model):
    __tablename__ = "internshipposition"

    positionID = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default="Pending")

    employerID = db.Column(db.Integer, db.ForeignKey("employer.employerID"), nullable=False)
    studentID = db.Column(db.Integer, db.ForeignKey("student.studentID"), nullable=True)

    def __init__(self, title, employerID, description=None, studentID=None, status="Pending"):
        self.title = title
        self.employerID = employerID
        self.description = description
        self.studentID = studentID
        self.status = status

    def set_status(self, status):
        self.status = status

    def assign_student(self, student_id):
        self.studentID = student_id

    def to_json(self):
        return {
            "positionID": self.positionID,
            "title": self.title,
            "description": self.description,
            "status": self.status,
            "employerID": self.employerID,
            "studentID": self.studentID
        }