from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user, wandering

# CREATE
@app.route('/register', methods = ['POST'])
def register_user():
    if user.User.create_user(request.form):
        return redirect('/dashboard')
    return redirect('/user/register')

# READ
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/user/register')
def register():
    return render_template('register.html')

@app.route('/user/<int:id>/wanderings')
def user_dashboard(id):
    if not 'user_id' in session:
        return redirect('/')
    this_user = user.User.get_user_wanderings()
    return render_template('user_dashboard.html', this_user = this_user)

# UPDATE


# DELETE


# LOGIN
@app.route('/login', methods = ['POST'])
def log_reg():
    if user.User.validate_login(request.form):
        return redirect('/dashboard')
    return redirect('/')

# LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
