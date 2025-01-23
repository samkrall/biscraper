from flask_wtf import FlaskForm
from wtforms import EmailField, SubmitField
from wtforms.validators import DataRequired, Email

# forms as a class, in version 0.1, the only form we need is for email signup
# Only validator is data required and that its an email.
class EmailForm(FlaskForm):
    email = EmailField('Email',
                         validators=[DataRequired(), Email()])
    submit = SubmitField('Sign Up!')
