from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user, wandering
import os
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '/Users/heathermehr/projects_algos/core_assignments/Wandershare/wandershare_code_files/flask_app/static/images'
ALLOWED_EXTENSIONS = set(['pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# CREATE
def allowed_file(filename):
    return '.' in filename and \
    filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/wanderings/add', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        wandering.Wandering.validate_wandering(request.form, request.files)
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            user_id = session['user_id']
            data = {
                'location' : request.form['location'],
                'start_date' : request.form['start_date'],
                'end_date' : request.form['end_date'],
                'rating' : request.form['rating'],
                'details' : request.form['details'],
                'image' : f'/static/images/{filename}',
                'user_id' : user_id
            }
            new_wandering = wandering.Wandering.create_wandering(data)
            if not new_wandering:
                return redirect('/wandering/new')
            return redirect(f'/user/{user_id}/wanderings')
        flash('Not an allowed file type.')
        return redirect('/wandering/new')
    return redirect('/')

# READ
@app.route('/dashboard')
def dashboard():
    if not 'user_id' in session:
        return redirect('/')
    all_wanderings = wandering.Wandering.get_all_wanderings()
    return render_template('dashboard.html', all_wanderings = all_wanderings)

@app.route('/wandering/<int:id>')
def one_wandering_page(id):
    if not 'user_id' in session:
        return redirect('/')
    this_wandering = wandering.Wandering.get_wandering_with_user_by_id(id)
    # this_user = user.User.get_user_by_id()
    return render_template('view_wandering.html', this_wandering = this_wandering)

@app.route('/wandering/new')
def new_wandering_page():
    if not 'user_id' in session:
        return redirect('/')
    this_user = user.User.get_logged_in_user()
    return render_template('new_wandering.html', this_user = this_user)

@app.route('/wandering/<int:id>/edit')
def edit_wandering_page(id):
    if not 'user_id' in session:
        return redirect('/')
    this_wandering = wandering.Wandering.get_wandering_by_id(id)
    this_user = user.User.get_logged_in_user()
    return render_template('edit_wandering.html', this_wandering = this_wandering, this_user = this_user)

# UPDATE
@app.route('/wandering/edit/<int:id>', methods = ['POST'])
def edit_wandering_form(id):
    if not 'user_id' in session:
        return redirect('/')
    one_wandering = wandering.Wandering.get_wandering_by_id(id)
    if one_wandering.user_id != session['user_id']:
        return redirect('/dashboard')
    data = request.form.to_dict()
    file = request.files['file']
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        data['image'] = f'/static/images/{filename}'
    elif not file:
        data['image'] = one_wandering.image
    if wandering.Wandering.edit_wandering(data):
        return redirect(f'/wandering/{id}')
    return redirect(f'/wandering/{id}/edit')

# DELETE
@app.route('/wandering/delete/<int:id>')
def delete_wandering(id):
    if not 'user_id' in session:
        return redirect('/')
    if wandering.Wandering.delete_wandering_by_id(id):
        return redirect('/dashboard')
    return redirect(f'/user/{id}/wanderings')

