from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, validators, PasswordField, RadioField
from models import User


class ContactForm(Form):
	name = StringField("Name",  [validators.DataRequired("Please enter your name.")])
	email = StringField("Email",  [validators.DataRequired("Please enter your email address."), validators.Email("Please enter your email address.")])
	subject = StringField("Subject",  [validators.DataRequired("Please enter a subject.")])
	message = TextAreaField("Message",  [validators.DataRequired("Please enter a message.")])


class SignupForm(Form):
	email = StringField("Email",  [validators.DataRequired("Please enter your email address."), validators.Email("Please enter your email address.")])
	password = PasswordField('Password', [validators.DataRequired("Please enter a password.")])
	wallet = StringField("Wallet Address",  [validators.DataRequired("Please enter your wallet address.")])

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		if not Form.validate(self):
			return False
		user = User.query.filter_by(email=self.email.data.lower()).first()
		if user:
			self.email.errors.append("The email is already taken.")
			return False
		else:
			return True


class SigninForm(Form):
	email = StringField("Email", [validators.DataRequired("Please enter your email address."), validators.Email("Please enter your email address.")])
	password = PasswordField('Password', [validators.DataRequired("Please enter a password.")])

	def __init__(self, *args, **kwargs):
		Form.__init__(self, *args, **kwargs)

	def validate(self):
		if not Form.validate(self):
			return False
		user = User.query.filter_by(email=self.email.data).first()
		if user and user.check_password(self.password.data):
			return True
		else:
			self.email.errors.append("Invalid email or password.")
			return False


class DifficultyForm(Form):
	difficulty_beg = RadioField('Difficulty', choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], default='beginner')
	difficulty_int = RadioField('Difficulty', choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], default='intermediate')
	difficulty_adv = RadioField('Difficulty', choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced')], default='advanced')