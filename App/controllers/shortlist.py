from App.database import db

def add_to_shortlist(student_id, position_id):
    from App.models.shortlist import Shortlist
    from .student import Student
    student = Student.query.get(student_id)
    if student:
        new_entry = Shortlist(studentID=student_id, positionID=position_id)
        db.session.add(new_entry)
        db.session.commit()
        return new_entry
    return None

def get_shortlist_for_student(student_id):
    from App.models.shortlist import Shortlist
    entries = Shortlist.query.filter_by(studentID=student_id).all()
    return entries

def remove_from_shortlist(student_id, position_id):
    from App.models.shortlist import Shortlist
    entry = Shortlist.query.filter_by(studentID=student_id, positionID=position_id).first()
    if entry:
        try:
            db.session.delete(entry)
            db.session.commit()
            return True
        except:
            return False
    return False


