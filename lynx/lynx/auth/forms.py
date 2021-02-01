"""Create form logic."""
from wtforms import Form, StringField, PasswordField, validators, SubmitField, BooleanField, DateField, HiddenField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Optional
import datetime

class SignupForm(Form):
    """User Signup Form."""
    firstName = StringField('First Name',[validators.Length(min=3, max=50), validators.DataRequired()])                     
    lastName = StringField('Last Name',[validators.Length(min=3, max=50), validators.DataRequired()])
    password = PasswordField('New Password', [ validators.DataRequired(),validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm Password', [ validators.DataRequired()])
    phone = StringField('Phone Number')
    language = SelectField('Language', [ validators.DataRequired()])
    email = StringField('Email', [validators.Length(min=6, max=120), validators.Email()])
    acceptTerms = BooleanField('Accept Terms and Conditions')
    submit = SubmitField('Register')

class LoginForm(Form):
    """User Login Form."""
    email = StringField('Email', [validators.Length(min=6, max=120), validators.Email()])
    password = PasswordField('Password', [validators.DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Log In')

class ForgotForm(Form):
    """Forgot Password Form."""
    email = StringField('Email', [validators.Length(min=6, max=120), validators.Email()])
    submit = SubmitField('Submit')

class ResetPasswordForm(Form):
    password = PasswordField('New Password', [ validators.DataRequired(),validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm New Password', [ validators.DataRequired()])
    submit = SubmitField('Request Password Reset')

# class UserForm(Form):
#     firstName = StringField('First Name',[validators.Length(min=3, max=50), validators.DataRequired()])                     
#     lastName = StringField('Last Name',[validators.Length(min=3, max=50), validators.DataRequired()])
#     phone = StringField('Phone Number')
#     language = StringField('Language')
#     email = StringField('Email', [validators.Length(min=6, max=120), validators.Email()])
#     memberStartDate =  StringField('Member Since')
#     memberExpireDate = StringField('Expiry Date')
#     dateJoined = StringField('Date Joined')
#     lastLogin = StringField('Last Login')
#     userRole = StringField('Role')
#     submit = SubmitField('Register')

class ProfileForm(Form):
    firstName = StringField('First Name',[validators.Length(min=3, max=50), validators.DataRequired()])                     
    lastName = StringField('Last Name',[validators.Length(min=3, max=50), validators.DataRequired()])
    phone = StringField('Phone Number')
    language = StringField('Language')
    # email = StringField('Email', [validators.Length(min=6, max=120), validators.Email()])
    user_id = HiddenField()
    submit = SubmitField('Update')

class PreferencesForm(Form):
    language = SelectField('Language', [ validators.DataRequired()])
    user_id = HiddenField()
    submit = SubmitField('Update')

class ChangePasswordForm(Form):
    currentpassword = PasswordField('Current Password', [ validators.DataRequired()])
    password = PasswordField('New Password', [ validators.DataRequired(),validators.EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Confirm New Password', [ validators.DataRequired()])
    submit = SubmitField('Change Password')

class UserInfoForm(Form):
    firstName = StringField('First Name',[validators.Length(min=3, max=50), validators.DataRequired()])                     
    lastName = StringField('Last Name',[validators.Length(min=3, max=50), validators.DataRequired()])
    email = StringField('Email', [validators.Length(min=6, max=120), validators.Email()])
    user_id = HiddenField()
    submit = SubmitField('Update')