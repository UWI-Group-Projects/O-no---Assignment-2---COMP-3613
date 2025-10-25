from App.database import db
from App.models.internshipposition import InternshipPosition
from employer import Employer

def create_position(employer_id, title, description=None):
    # validate employer exists
    employer = Employer.query.get(employer_id)
    if not employer:
        return None
    pos = InternshipPosition(title=title, description=description, employerID=employer.employerID)
    db.session.add(pos)
    db.session.commit()
    return pos

