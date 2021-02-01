from wtforms import Form, StringField, TextAreaField, BooleanField, SubmitField, validators, ValidationError

class ContactForm(Form):
    inputName = StringField('Name', [validators.Length(min=4, max=50), validators.DataRequired()])
    inputEmail = StringField('Email', [validators.Length(min=6, max=120), validators.Email()])
    inputMessage = TextAreaField('Message', [validators.Length(min=1, max=500), validators.DataRequired()])