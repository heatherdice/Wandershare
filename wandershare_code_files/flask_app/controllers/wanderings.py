from flask_app import app
from flask import render_template, redirect, request, session
from flask_app.models import user, wandering

# CREATE


# READ
@app.route('/dashboard')
def dashboard():
    if not 'user_id' in session:
        return redirect('/')
    all_wanderings = wandering.Wandering.get_all_wanderings()
    return render_template('dashboard.html', all_wanderings = all_wanderings)

@app.route('/wandering/new')
def new_wandering_page():
    if not 'user_id' in session:
        return redirect('/')
    this_user = user.User.get_logged_in_user()
    return render_template('new_wandering.html', this_user = this_user)

# UPDATE

# DELETE

