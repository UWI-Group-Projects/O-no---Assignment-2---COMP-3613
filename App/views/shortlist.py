from flask import Blueprint, render_template, jsonify, request
from flask_login import current_user

from App.controllers.shortlist import get_shortlist_for_student, add_to_shortlist, remove_from_shortlist    
shortlist_views = Blueprint('shortlist_views', __name__, template_folder='../templates')    

# View shortlist for current student
@shortlist_views.route('/shortlist', methods=['GET'])   
def view_shortlist_page():   
    if not current_user.is_authenticated or current_user.role != 'student':
        return jsonify({"error": "unauthorized"}), 401
    shortlist = get_shortlist_for_student(current_user.id)
    return render_template('shortlist.html', shortlist=shortlist)

# Add to shortlist (Student only)
@shortlist_views.route('/shortlist', methods=['POST'])
def add_to_shortlist_api():   
    if not current_user.is_authenticated or current_user.role != 'student':
        return jsonify({"error": "unauthorized"}), 401
    data = request.json
    position_id = data.get('positionId')
    if add_to_shortlist(current_user.id, position_id):
        return jsonify({"message": "added to shortlist"}), 201
    return jsonify({"error": "failed to add"}), 400

# Remove from shortlist (Student only)
@shortlist_views.route('/shortlist/<int:positionId>', methods=['DELETE'])   
def remove_from_shortlist_api(positionId):   
    if not current_user.is_authenticated or current_user.role != 'student':
        return jsonify({"error": "unauthorized"}), 401
    if remove_from_shortlist(current_user.id, positionId):
        return jsonify({"message": "removed from shortlist"}), 200
    return jsonify({"error": "failed to remove"}), 400