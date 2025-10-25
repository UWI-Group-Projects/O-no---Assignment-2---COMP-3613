from flask import Blueprint, render_template, jsonify, request
from flask_login import current_user

student_views = Blueprint('student_views', __name__, template_folder='../templates')

# view shortlist for current student
@student_views.route('/student/shortlist', methods=['GET'])
def view_student_shortlist_page():
    if not current_user.is_authenticated or current_user.role != 'student':
        return jsonify({"error": "unauthorized"}), 401
    # Here you would normally fetch the student's shortlist from the database
    shortlist = []  # Placeholder for actual shortlist data
    return render_template('student_shortlist.html', shortlist=shortlist)

# view employer responses for current student
@student_views.route('/student/responses', methods=['GET'])
def view_student_responses_page():
    if not current_user.is_authenticated or current_user.role != 'student':
        return jsonify({"error": "unauthorized"}), 401
    # Here you would normally fetch the student's employer responses from the database
    responses = []  # Placeholder for actual responses data
    return render_template('student_responses.html', responses=responses)
