import json
import time
import requests
from flask import render_template, request, flash, session, url_for, redirect
from flask.ext.mail import Message
from forms import *
from models import *
from app import app, mail


@app.route('/', methods=['GET', 'POST'])
def home():
	return render_template('home.html')


@app.route('/about', methods=['GET', 'POST'])
def about():
	return render_template('about.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
	form = ContactForm()

	if request.method == 'POST':
		if not form.validate():
			flash('All fields are required.')
			return render_template('contact.html', form=form)
		else:
			msg = Message(form.subject.data, sender='contact@example.com', recipients=['dobromir.m.dobrev@gmail.com'])
			msg.body = """
			From: %s <%s>
			%s
			""" % (form.name.data, form.email.data, form.message.data)
			mail.send(msg)
			return render_template('contact.html', success=True)

	elif request.method == 'GET':
		return render_template('contact.html', form=form)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
	form = SignupForm()

	if 'email' in session:
		return redirect(url_for('profile'))

	if request.method == 'POST':
		if not form.validate():
			return render_template('signup.html', form=form)
		else:
			newuser = User(form.email.data, form.password.data, form.wallet.data)
			db.session.add(newuser)
			db.session.commit()

			session['email'] = newuser.email
			return redirect(url_for('profile'))

	elif request.method == 'GET':
		return render_template('signup.html', form=form)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
	if 'email' not in session:
		return redirect(url_for('signin'))

	user = User.query.filter_by(email=session['email']).first()
	if user is None:
		return redirect(url_for('signout'))

	if user.movestoken is not None and user.quest is not None and user.quest_complete is False:
		date = time.strftime('%Y%m%d')
		payload = {'access_token': user.movestoken['access_token']}
		r = requests.get('https://api.moves-app.com/api/1.1/user/summary/daily/' + date, params=payload)
		if r.text == "expired_access_token":
		    user.movestoken = None
		elif r.json()[0]['summary'] is not None:
			activity = None
			for value in r.json()[0]['summary']:
				if value['activity'] == user.quest['activity']:
					activity = value
			if activity is not None:
				completion = False
				if user.quest['duration'] == 0:
					user.quest_progress = int(activity['distance'])/1609
					if user.quest_progress >= int(user.quest['distance']):
						completion = True
				else:
					user.quest_progress = int(activity['duration'])/60
					if user.quest_progress >= int(user.quest['duration']):
						completion = True
				if completion is True:
					user.coins += int(user.quest['reward'])
					user.lastreward = int(user.quest['reward'])
					user.quest_complete = True
		db.session.commit()

	return render_template('profile.html', user=user)


@app.route('/authorization', methods=['GET', 'POST'])
def authorization():
	code = request.args.get('code')
	payload = {'grant_type': 'authorization_code',
        	'code': code,
        	'client_id': '68D1ogxT33tbs850i2nITH1F7fqe4WU3',
        	'client_secret': 'eZXD8kDor6WR8BVz2h07M8ZWv5BKr9u5CkRqe32TQ2R7u1eAov70uuwp3shsQTm6',
        	'redirect_uri': 'https://deemdobrev.pythonanywhere.com/authorization'}
	r = requests.post('https://api.moves-app.com/oauth/v1/access_token', params=payload)
	user = User.query.filter_by(email=session['email']).first()
	if 'error' not in r.json().keys():
	    user.movestoken = r.json()
    	db.session.commit()
	return redirect(url_for('profile'))


@app.route('/signin', methods=['GET', 'POST'])
def signin():
	form = SigninForm()

	if 'email' in session:
		return redirect(url_for('profile'))

	if request.method == 'POST':
		if not form.validate():
			return render_template('signin.html', form=form)
		else:
			session['email'] = form.email.data
			return redirect(url_for('profile'))

	elif request.method == 'GET':
		return render_template('signin.html', form=form)


@app.route('/signout', methods=['GET', 'POST'])
def signout():
	if 'email' not in session:
		return redirect(url_for('signin'))

	session.pop('email', None)
	return redirect(url_for('home'))


@app.route('/difficulty', methods=['GET','POST'])
def difficulty():
	form = DifficultyForm()
	user = User.query.filter_by(email=session['email']).first()
	if user.difficulty == 'beginner':
		response = form.difficulty_beg.data
	if user.difficulty == 'intermediate':
		response = form.difficulty_int.data
	if user.difficulty == 'advanced':
		response = form.difficulty_adv.data

	if request.method == 'POST':
		if user.difficulty != response:
			week_file = '/week_' + user.week + '.json'
			path = '/home/deemdobrev/genkicraft/app/quests/' + response + week_file
			json_data = open(path)
			quests = json.load(json_data)
			json_data.close()

			user.difficulty = response
			user.quest = quests['01']
			user.coins = 0
			user.lastreward = 0
			user.quest_progress = 0
			user.quest_complete = False
			db.session.commit()
		return redirect(url_for('profile'))

	elif request.method == 'GET':
		return render_template('difficulty.html', form=form, user=user)