from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user, wandering

# CREATE


# READ
@app.route('/')
def index():
    return render_template('index.html')

# UPDATE


# DELETE


# LOGIN
@app.route('/login', methods = ['POST'])
def log_reg():
    if user.User.validate_login(request.form):
        return redirect('/user/dashboard')
    return redirect('/')

# LOGOUT
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')
