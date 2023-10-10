from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired, Email


class RegisterUserForm(FlaskForm):
    ''' Form for registering new notes app users '''

    username = StringField('User Name', validators=[InputRequired()])

    password = StringField('Password', validators=[InputRequired()])

    email = StringField('Email', validators=[InputRequired(), Email()])

    first_name = StringField('First Name', validators=[InputRequired()])

    last_name = StringField('Last Name', validators=[InputRequired()])



class LoginForm(FlaskForm):
    ''' Form for logging in to the notes app '''

    username = StringField('User Name', validators=[InputRequired()])

    password = StringField('Password', validators=[InputRequired()])



class CSRFProtectForm(FlaskForm):
    """ Form just for CSRF Protection """