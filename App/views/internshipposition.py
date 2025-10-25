from flask import Blueprint, render_template, jsonify, request
from flask_login import current_user
from App.controllers.shortlist import get_shortlist_for_student, add_to_shortlist, remove_from_shortlist    
position_views = Blueprint('position_views', __name__, template_folder='../templates')
# View internship positions for current student
@position_views.route('/positions', methods=['GET'])
def view_positions_page():   
    if not current_user.is_authenticated or current_user.role != 'student':
        return jsonify({"error": "unauthorized"}), 401
    # For simplicity, we will just render a template without actual positions
    return render_template('positions.html')
# Add to positions (Student only)
@position_views.route('/positions', methods=['POST'])
def add_position_api():   
    if not current_user.is_authenticated or current_user.role != 'student':
        return jsonify({"error": "unauthorized"}), 401
    data = request.json
    position_id = data.get('positionId')
    if add_to_shortlist(current_user.id, position_id):
        return jsonify({"message": "added to positions"}), 201
    return jsonify({"error": "failed to add"}), 400

