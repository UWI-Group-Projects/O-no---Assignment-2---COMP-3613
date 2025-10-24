from App.database import db
from App.models.internshipposition import InternshipPosition
from App.models.student import Student

def add_student_to_position(staff_user, student_id, position_id):
    # keep staff_user argument so we can check permission in future
    pos = InternshipPosition.query.filter_by(positionID=position_id).first()
    student = Student.query.get(student_id)
    if pos and student:
        pos.assign_student(student.studentID)
        db.session.commit()
        return True
    return False