"""Flask app for Notes"""
import os
from flask import Flask, render_template, redirect, flash, session
from werkzeug.exceptions import Unauthorized
from models import db, connect_db, User
from forms import RegisterUserForm, LoginForm, CSRFProtectForm


app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    "DATABASE_URL", "postgresql:///notes")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)


USER_SESSION_KEY = 'username'


@app.get('/')
def homepage():
    ''' redirect user to /register '''

    return redirect('/register')


@app.route('/register', methods=['GET', 'POST'])
def register():
    ''' shows or handles user registration form '''

    # why can't use if session[USER_SESSION_KEY]
    if USER_SESSION_KEY in session:
        return redirect(f'/users/{session[USER_SESSION_KEY]}')

    form = RegisterUserForm()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username, password, email, first_name, last_name)

        db.session.add(new_user)
        db.session.commit()

        session[USER_SESSION_KEY] = new_user.username

        flash(f'Successfully added {new_user.username}')
        return redirect(f'/users/{new_user.username}')

    else:
        return render_template('register.html', form=form)



@app.route('/login', methods=['GET', 'POST'])
def login():
    ''' show or handle the user login form '''

    # why can't use if session[USER_SESSION_KEY]
    if USER_SESSION_KEY in session:
        return redirect(f'/users/{session[USER_SESSION_KEY]}')

    form = LoginForm()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        user =  User.authenticate(username, password)

        if user:
            session[USER_SESSION_KEY] = user.username
            return redirect(f'/users/{user.username}')

        else:
            form.username.errors = ['Incorrect username or password']

    return render_template('login.html', form=form)



@app.get('/users/<username>')
def show_user(username):
    ''' display information about a particular user '''

    if USER_SESSION_KEY not in session or session[USER_SESSION_KEY] != username:
        raise Unauthorized()

    else:

        form = CSRFProtectForm()
        user = User.query.get_or_404(username)

        return render_template('profile.html', user=user, form=form)



@app.post("/logout")
def logout():
    """Logs user out and redirects to homepage."""

    form = CSRFProtectForm()

    if form.validate_on_submit():
        session.pop(USER_SESSION_KEY)

    return redirect("/")


@app.post('/users/<username>/delete')
def delete_user(username):
    ''' handles delete user button '''

    form = CSRFProtectForm()

    if form.validate_on_submit():

        user = User.query.get_or_404(username)

        for note in user.notes:
            db.session.delete(note)

        db.session.delete(user)
        db.session.commit()

        flash(f'Successfully deleted {username}')
        return redirect('/')

    else:
        raise Unauthorized()
