from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required
from models import User
from werkzeug.security import check_password_hash

# Create the blueprint
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            username = request.form['username']
            password = request.form['password']
            
            # Debug print
            print(f"Login attempt: {username}")
            
            user = User.query.filter_by(username=username).first()
            
            if user and user.password == password:
                login_user(user)
                print(f"Login successful for {username}")
                return redirect(url_for('main.dashboard'))
            else:
                if user:
                    print(f"Password incorrect for {username}")
                else:
                    print(f"No user found with username: {username}")
                flash('Invalid username or password')
        except Exception as e:
            print(f"Login error: {str(e)}")
            flash(f'Login error: {str(e)}')
    
    return render_template('login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))