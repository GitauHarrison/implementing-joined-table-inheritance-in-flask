from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, SelectField
from wtforms.validators import DataRequired, Length, EqualTo, Email


class LoginForm(FlaskForm):
    """Login Form"""
    username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log In')


class RegistrationForm(FlaskForm):
    """Registration Form"""
    username = StringField('Username', validators=[DataRequired(), Length(1, 64)])
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField(
        'Confirm Password', validators=[DataRequired(), EqualTo('password')])
    identity = SelectField('Who are you?', choices=[('teacher', 'Teacher'), ('student', 'Student')])
    submit = SubmitField('Save')


class StudentForm(FlaskForm):
    age = StringField('Age', validators=[DataRequired()])
    submit = SubmitField('Update')


class TeacherForm(FlaskForm):
    course = StringField('Course', validators=[DataRequired()])
    submit = SubmitField('Update')
