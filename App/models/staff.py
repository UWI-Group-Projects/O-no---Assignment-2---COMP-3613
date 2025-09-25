from werkzeug.security import check_password_hash, generate_password_hash
from App.database import db
from .internshipposition import InternshipPosition

class Staff(db.Model):
    staffID = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)

    def __init__(self, username, password):
        self.username = username
        self.set_password(password)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def add_student_to_position(self, studentID, positionID):
        position = InternshipPosition.query.filter_by(positionID=positionID).first()
        if position:
            position.studentID = studentID
            db.session.commit()
            return True
        return False

    def get_json(self):
        return {
            "staffID": self.staffID,
            "username": self.username
        }
