from app import app
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, IntegerField, TextAreaField, BooleanField
from wtforms.validators import InputRequired, EqualTo, NumberRange, Optional
from datetime import datetime

def validDate(form,field):
	try:
		date = datetime.strptime(field.data, '%m/%d/%Y')
	except:
		raise ValueError('Invalid date format')

class LoginForm(FlaskForm):
	username = StringField('Username', validators=[InputRequired(message='A username is required')])
	password = PasswordField('Password', validators=[InputRequired(message='Enter your password')])

class SignUpForm(FlaskForm):
	username = StringField('Username',validators=[InputRequired(message='A username is required')])
	password = PasswordField('Password', [InputRequired(), EqualTo('confirm', message='Passwords must match')])
	confirm = PasswordField('RepeatPassword')

class AddDriverForm(FlaskForm):
	name = StringField('Name',validators=[InputRequired(message='Driver name is required')])
	alias = StringField('Alias')
	vehicle = StringField('Vehicle')
	forklift = BooleanField('Forklift')
	percentage = IntegerField('Percentage',validators=[NumberRange(min=0, max=100, message='Percentage must be between 0 - 100')])

class EditDriverForm(FlaskForm):
	id = StringField('Id',validators=[InputRequired(message='Driver ID is required')])
	name = StringField('Name',validators=[InputRequired(message='Driver name is required')])
	alias = StringField('Alias')
	vehicle = StringField('Vehicle')
	forklift = BooleanField('Forklift')
	percentage = IntegerField('Percentage',validators=[NumberRange(min=0, max=100, message='Percentage must be between 0 - 100')])

class NewEquipmentForm(FlaskForm):
	id = StringField('Id',validators=[InputRequired(message='Vehicle ID is required')])
	mileage = IntegerField('Mileage',validators=[InputRequired(message='Vehicle mileage is required')])
	notes = TextAreaField('Notes')

class EditLoadForm(FlaskForm):
	id = StringField('Id',validators=[InputRequired(message='Load ID is required')])
	driver = StringField('Driver')
	vehicle = StringField('Vehicle')
	hand_tag = StringField('Hand Tag')
	origin = StringField('Origin')
	customer = StringField('Customer')
	po_num = StringField('P.O. Number')
	destination = StringField('Destination')
	date = StringField('Date', validators=[Optional(),validDate])
	forklift = IntegerField('Forklift',validators=[Optional(),NumberRange(min=0, message='Forklift Cost must be positive')])
	amount_billed = IntegerField('Amount Billed',validators=[Optional(),NumberRange(min=0, message='Amount Billed must be positive')])
	amount_paid = IntegerField('Amount Paid',validators=[Optional(),NumberRange(min=0, message='Amount Paid must be positive')])
	subhaul = BooleanField('Subhaul')
	preload = BooleanField('Preload')
	other = TextAreaField('Other')