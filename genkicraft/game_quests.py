import json
import requests
from datetime import datetime, timedelta
from app import models, db


users = models.User.query.all()
for user in users:
	if user.quest is not None:
		if user.quest_complete is False and user.movestoken is not None:
			date = (datetime.now() - timedelta(days=1)).strftime('%Y%m%d') # get yesterday's date
			payload = {'access_token': user.movestoken['access_token']}
			r = requests.get('https://api.moves-app.com/api/1.1/user/summary/daily/' + date, params=payload)
			if r.text != "expired_access_token" and r.json()[0]['summary'] is not None:
				activity = None
				for value in r.json()[0]['summary']:
					if value['activity'] == user.quest['activity']:
						activity = value
				if activity is not None:
					if int(user.quest['distance'])*1609 <= int(activity['distance']) and int(user.quest['duration'])*60 <= int(activity['duration']):
						user.coins += int(user.quest['reward'])
						user.lastreward = int(user.quest['reward'])
						user.quest_complete = True

		if user.quest_complete is True:
			week_file = '/week_' + user.week + '.json'
			path = '/home/deemdobrev/genkicraft/app/quests/' + user.difficulty + week_file
			json_data = open(path)
			quests = json.load(json_data)
			json_data.close()
			if (int(user.quest['number']) + 1) <= len(quests.items()):
				next_quest_number = '0%d' % (int(user.quest['number']) + 1)
				user.quest = quests[next_quest_number]
			else:
				user.quest = None

		user.quest_progress = 0
		user.quest_complete = False
db.session.commit()