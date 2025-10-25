from flask import Blueprint, render_template, jsonify, request
from flask_login import current_user

employer_views = Blueprint('employer_views', __name__, template_folder='../templates')
# View employer dashboard
@employer_views.route('/employer/dashboard', methods=['GET'])
def employer_dashboard():
    if not current_user.is_authenticated or current_user.role != 'employer':
        return jsonify({"error": "unauthorized"}), 401
    return render_template('employer_dashboard.html')
# Post a new internship position
@employer_views.route('/employer/post_position', methods=['POST'])
def post_internship_position():
    if not current_user.is_authenticated or current_user.role != 'employer':
        return jsonify({"error": "unauthorized"}), 401
    data = request.json
    title = data.get('title')
    description = data.get('description')
    # Here you would normally save the position to the database
    return jsonify({"message": "position posted", "title": title}), 201
# View all posted positions by the employer
@employer_views.route('/employer/positions', methods=['GET'])
def view_posted_positions():
    if not current_user.is_authenticated or current_user.role != 'employer':
        return jsonify({"error": "unauthorized"}), 401
    # Here you would normally fetch positions from the database
    positions = [
        {"id": 1, "title": "Software Intern", "description": "Work on cool projects."},
        {"id": 2, "title": "Data Analyst Intern", "description": "Analyze data trends."}
    ]
    return jsonify({"positions": positions}), 200
# View applicants for a specific position   
@employer_views.route('/employer/positions/<int:position_id>/applicants', methods=['GET'])
def view_applicants(position_id):   
    if not current_user.is_authenticated or current_user.role != 'employer':
        return jsonify({"error": "unauthorized"}), 401
    # Here you would normally fetch applicants from the database
    applicants = [
        {"student_id": 1, "name": "Alice"},
        {"student_id": 2, "name": "Bob"}
    ]
    return jsonify({"position_id": position_id, "applicants": applicants}), 200
# Make decision on an applicant
@employer_views.route('/employer/positions/<int:position_id>/applicants/<int:student_id>/decision', methods=['POST'])
def decide_applicant(position_id, student_id):   
    if not current_user.is_authenticated or current_user.role != 'employer':
        return jsonify({"error": "unauthorized"}), 401
    data = request.json
    decision = data.get('decision')  # 'accept' or 'reject'
    # Here you would normally update the applicant's status in the database
    return jsonify({"message": f"applicant {student_id} has been {decision}ed for position {position_id}"}), 200
