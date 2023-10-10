"""Flask app for Notes"""
import os
from flask import Flask, request, jsonify, render_template, redirect, flash
from models import db, connect_db, User
from forms import RegisterUserForm


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

        new_user = User(
            username=username,
            password=password,
            email=email,
            first_name=first_name,
            last_name=last_name
        )

        db.session.add(new_user)
        db.session.commit()

        flash(f'Successfully added {new_user.name}')
        return redirect(f'/users/{new_user.username}')

    else:
        return render_template('register.html', form=form)