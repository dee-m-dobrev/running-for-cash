from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import PickleType
from app import db


class User(db.Model):
	__tablename__ = 'users'
	email = db.Column(db.String(120), primary_key=True)
	pwdhash = db.Column(db.String(54))
	wallet = db.Column(db.String(120))
	movestoken = db.Column(PickleType)
	quest = db.Column(PickleType)
	coins = db.Column(db.Integer)
	lastreward = db.Column(db.Integer)
	quest_progress = db.Column(db.Integer)
	quest_complete = db.Column(db.Boolean)
	difficulty = db.Column(db.String(120))
	week = db.Column(db.String(120))


	def __init__(self, email, password, wallet):
		self.email = email.lower()
		self.set_password(password)
		self.wallet = wallet.lower()
		self.movestoken = None
		self.quest = {"number": "01", "activity": "walking", "duration": "15", "distance": "0", "reward": "15"}
		self.coins = 0
		self.lastreward = 0
		self.quest_progress = 0
		self.quest_complete = False
		self.difficulty = "beginner"
		self.week = '01'

	def set_password(self, password):
		self.pwdhash = generate_password_hash(password)

	def check_password(self, password):
		return check_password_hash(self.pwdhash, password)