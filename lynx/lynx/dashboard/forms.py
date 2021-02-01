"""Create form logic."""
from wtforms import Form, StringField, validators, SubmitField, BooleanField, DateField, HiddenField, DecimalField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo, Length, Optional

