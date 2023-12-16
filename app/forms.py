from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField,SubmitField,FloatField
from wtforms.validators import DataRequired, Email

class RegistrationForm(FlaskForm):
    id=StringField('ID',validators=[DataRequired()])
    username=StringField('Username',validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Register')

class LoginForm(FlaskForm):
    username=StringField('Username',validators=[DataRequired()])
    password=PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class Dashboard(FlaskForm):
    submit=SubmitField('Logout')

class DataForm(FlaskForm):
    id=StringField('ID',validators=[DataRequired()])
    name=StringField('Name',validators=[DataRequired()])
    account_number=StringField('Account Number', validators=[DataRequired()])
    balance=FloatField('Balance', validators=[DataRequired()])
    user_id=StringField('USER_ID',validators=[DataRequired()])
    submit=SubmitField('Submit')

class DepositForm(FlaskForm):
    amount=FloatField("amount",validators=[DataRequired()])
    submit=SubmitField('Submit')

class WithdrawForm(FlaskForm):
    amount=FloatField("amount",validators=[DataRequired()])
    submit=SubmitField('Submit')

