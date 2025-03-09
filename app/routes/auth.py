from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from flask_login import login_user, logout_user, login_required, current_user
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Login route"""
    # If user is already logged in, redirect to main page
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.get_by_username(username)
        if user and user.check_password(password):
            # Remember user preference (if checkbox selected)
            remember = 'remember' in request.form
            login_user(user, remember=remember)
            
            # Get next page from request args
            next_page = request.args.get('next')
            
            # Redirect to next page or main index
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(next_page or url_for('main.index'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    """Logout route"""
    # Clear the session and logout user
    session = {}
    logout_user()
    flash('You have been logged out successfully', 'info')
    return redirect(url_for('auth.login'))