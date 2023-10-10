"""Flask app for Notes"""
import os
from flask import Flask, request, render_template, redirect, flash, session
from models import db, connect_db, User
from forms import RegisterUserForm, LoginForm, CSRFProtectForm


app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", "postgresql:///notes")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


@app.get('/')
def homepage():
    ''' redirect user to /register '''

    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def register():
    ''' shows and handles user registration form '''

    form = RegisterUserForm()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user =User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)
        db.session.commit()

        session['user_id'] = new_user.id

        flash(f'Successfully added {new_user.username}')
        return redirect(f'/users/{new_user.username}')

    else:
        return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    ''' show and handle the user login form '''

    form = LoginForm()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        user =  User.authenticate(username, password)

        if user:
            session['user_id'] = user.id
            return redirect(f'/users/{user.username}')

        else:
            # why is this in square brackets?
            form.username.errors = ['Incorrect username or password']

    return render_template('login.html', form=form)



@app.get('/users/<username>')
def show_user(username):
    # are we supposed to do anything with username here?
    ''' display information about a particular user '''

    form = CSRFProtectForm()

    if 'user_id' not in session:
        flash('You must logged in to view this page')
        return redirect('/')

    else:
        user = User.query.get(session['user_id'])
        return render_template('profile.html', user=user, form=form)



@app.post("/logout")
def logout():
    """Logs user out and redirects to homepage."""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        # Remove "user_id" if present, but no errors if it wasn't
        session.pop("user_id", None)

    return redirect("/")
