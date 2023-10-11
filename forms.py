from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length


class RegisterUserForm(FlaskForm):
    ''' Form for registering new notes app users '''

    username = StringField('User Name', validators=[InputRequired(), Length(min=2, max=20)])

    password = PasswordField('Password', validators=[InputRequired(), Length(min=4, max=100)])

    email = StringField('Email', validators=[InputRequired(), Email(), Length(max=50)])

    first_name = StringField('First Name', validators=[InputRequired(), Length(max=30)])

    last_name = StringField('Last Name', validators=[InputRequired(), Length(max=30)])



class LoginForm(FlaskForm):
    ''' Form for logging in to the notes app '''

    username = StringField('User Name', validators=[InputRequired()])

    password = PasswordField('Password', validators=[InputRequired()])


# name can be anything, hidden field is there with all FlaskForms
class CSRFProtectForm(FlaskForm):
    """ Form just for CSRF Protection """