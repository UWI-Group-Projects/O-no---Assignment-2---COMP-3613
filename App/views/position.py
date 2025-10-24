from flask import Blueprint, request, jsonify
from flask_jwt_extended import current_user, jwt_required
from App.controllers.auth import employer_required, staff_required, student_required
from App.controllers.employer import create_position, accept_student, reject_student, view_shortlist_for_position
from App.controllers.staff import add_student_to_position
from App.controllers.student import view_shortlist_positions, view_employer_response

position_views = Blueprint('position_views', __name__)

# Create internship position (Employer only)
@position_views.route('/positions', methods=['POST'])
@jwt_required()
@employer_required
def create_position_api():
    data = request.json
    pos = create_position(current_user.id, data['title'], data.get('description'))
    if pos:
        return jsonify({"message": "position created"}), 201
    return jsonify({"error": "invalid employer"}), 400


# Add student to shortlist (Staff)
@position_views.route('/positions/<int:positionId>/shortlist', methods=['POST'])
@jwt_required()
@staff_required
def shortlist_student_api(positionId):
    data = request.json
    if add_student_to_position(current_user, data['studentId'], positionId):
        return jsonify({"message": "student added to shortlist"}), 201
    return jsonify({"error": "failed"}), 400


# Employer review (accept/reject)
@position_views.route('/positions/<int:positionId>/review', methods=['POST'])
@jwt_required()
@employer_required
def review_student_api(positionId):
    data = request.json
    student_id = data["studentId"]
    decision = data["decision"].lower()

    if decision == "accept":
        success = accept_student(current_user.id, positionId, student_id)
        msg = "student accepted"
    else:
        success = reject_student(current_user.id, positionId, student_id)
        msg = "student rejected"

    if success:
        return jsonify({"message": msg}), 200
    return jsonify({"error": "failed"}), 400


# View shortlisted positions (Student only)
@position_views.route('/students/<int:studentId>/shortlist', methods=['GET'])
@jwt_required()
@student_required
def view_shortlist_api(studentId):
    apps = view_shortlist_positions(studentId)
    if not apps:
        return jsonify([]), 200

    results = []
    for app in apps:
        status = view_employer_response(studentId, app["positionID"])
        app["status"] = status
        results.append(app)

    return jsonify(results), 200
