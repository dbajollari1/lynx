"""Create form logic."""
from wtforms import Form, StringField, validators, SubmitField, BooleanField, DateField, HiddenField, DecimalField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Optional

class SendForm(Form):                    
    amt = DecimalField('Amount', [validators.DataRequired()])
    fromemail = StringField('From Email', [validators.Length(min=6, max=120), validators.Email()])
    toemail = StringField('To Email', [validators.Length(min=6, max=120), validators.Email()])
    tokenSymbol = StringField('Token', [validators.Length(min=3, max=4)])
    submit = SubmitField('Send')

class InvestForm(Form):
    Token = SelectField('Token', [ validators.DataRequired()])
    Amount = DecimalField('Amount', [ validators.DataRequired()])
    submit = SubmitField('Trade')