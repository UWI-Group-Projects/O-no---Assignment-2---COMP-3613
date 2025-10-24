from App.database import db
from .internshipposition import InternshipPosition

class Employer(db.Model):
    __tablename__ = "employer"

    employerID = db.Column(db.Integer, primary_key=True)
    companyName = db.Column(db.String(120), nullable=False)

    positions = db.relationship("InternshipPosition", backref="employer", lazy=True)

    def __init__(self, companyName):
        self.companyName = companyName

    def to_json(self):
        return {
            "employerID": self.employerID,
            "companyName": self.companyName
        }
