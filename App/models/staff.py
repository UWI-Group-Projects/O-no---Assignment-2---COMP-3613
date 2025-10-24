from werkzeug.security import generate_password_hash, check_password_hash
from App.database import db

class Staff(db.Model):
    __tablename__ = "staff"

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

    def to_json(self):
        return {
            "staffID": self.staffID,
            "username": self.username
        }
