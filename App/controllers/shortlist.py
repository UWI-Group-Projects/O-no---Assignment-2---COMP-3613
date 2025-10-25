from App.database import db
from .student import Student

def create_shortlist_entry(student_id, position_id):
    student = Student.query.get(student_id)
    if student:
        from App.models.shortlist import Shortlist
        new_entry = Shortlist(studentID=student_id, positionID=position_id)
        db.session.add(new_entry)
        db.session.commit()
        return new_entry
    return None
def view_shortlist_for_student(student_id):
    from App.models.shortlist import Shortlist
    entries = Shortlist.query.filter_by(studentID=student_id).all()
    return entries
def delete_shortlist_entry(student_id, position_id):
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
    return Student.query.filter_by(username=username).first()

