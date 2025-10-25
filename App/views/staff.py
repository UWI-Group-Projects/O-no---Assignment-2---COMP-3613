from flask import Blueprint, render_template, jsonify, request
from flask_login import current_user

staff_views = Blueprint('staff_views', __name__, template_folder='../templates')
# View staff dashboard
@staff_views.route('/staff/dashboard', methods=['GET'])
def staff_dashboard():
    if not current_user.is_authenticated or current_user.role != 'staff':
        return jsonify({"error": "unauthorized"}), 401
    return render_template('staff_dashboard.html')


# Add student to shortlist (Staff only)
@staff_views.route('/staff/shortlist', methods=['POST'])
def add_student_to_shortlist():
    if not current_user.is_authenticated or current_user.role != 'staff':
        return jsonify({"error": "unauthorized"}), 401
    data = request.json
    student_id = data.get('studentId')
    position_id = data.get('positionId')
    # Here you would normally add the student to the shortlist in the database
    return jsonify({"message": f"student {student_id} added to shortlist for position {position_id}"}), 201

