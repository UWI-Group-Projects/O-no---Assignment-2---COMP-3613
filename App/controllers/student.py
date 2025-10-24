from App.models.internshipposition import InternshipPosition
from App.models.student import Student

def view_shortlist_positions(student_id):
    student = Student.query.get(student_id)
    if not student: return []
    return [app.to_json() for app in student.applications]

def view_employer_response(student_id, position_id):
    pos = InternshipPosition.query.filter_by(positionID=position_id, studentID=student_id).first()
    return pos.status if pos else None