from flask import Blueprint, render_template, jsonify, request, flash, send_from_directory, flash, redirect, url_for
from flask_jwt_extended import jwt_required, current_user, unset_jwt_cookies, set_access_cookies
from flask_login import login_user, logout_user, current_user

from.index import index_views

from App.controllers import (
    login,login_staff, login_student, login_employer

)

auth_views = Blueprint('auth_views', __name__, template_folder='../templates')




@auth_views.route('/login', methods=['GET'])
def login_page():
    return render_template('login.html')

@auth_views.route('/login', methods=['POST'])
def login_action():
    username = request.form.get('username')
    password = request.form.get('password')
    role = request.form.get('role')
    user = None
    if role == 'student':
        user = login_student(username, password)
    elif role == 'staff':
        user = login_staff(username, password)
    elif role == 'employer':
        user = login_employer(username, password)
    if user:
        return redirect('/')
    flash('Invalid username/password')
    return redirect('/login')

@auth_views.route('/logout', methods=['GET'])
def logout_action():
    logout_user()
    return redirect('/')