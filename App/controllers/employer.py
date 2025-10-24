from App.database import db
from App.models.internshipposition import InternshipPosition
from App.models.employer import Employer

def create_position(employer_id, title, description=None):
    # validate employer exists
    employer = Employer.query.get(employer_id)
    if not employer:
        return None
    pos = InternshipPosition(title=title, description=description, employerID=employer.employerID)
    db.session.add(pos)
    db.session.commit()
    return pos

def accept_student(employer_id, position_id, student_id):
    pos = InternshipPosition.query.filter_by(positionID=position_id, employerID=employer_id).first()
    if pos and pos.studentID == student_id:
        pos.set_status("Accepted")
        db.session.commit()
        return True
    return False

def reject_student(employer_id, position_id, student_id):
    pos = InternshipPosition.query.filter_by(positionID=position_id, employerID=employer_id).first()
    if pos and pos.studentID == student_id:
        pos.set_status("Rejected")
        db.session.commit()
        return True
    return False

def view_shortlist_for_position(employer_id, position_id):
    pos = InternshipPosition.query.filter_by(positionID=position_id, employerID=employer_id).first()
    if pos and pos.student:
        return [pos.student.to_json()]
    return []