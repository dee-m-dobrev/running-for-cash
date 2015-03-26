import requests
from app import models, db


users = models.User.query.all()
for user in users:
    if user.movestoken is not None:
    	payload = {'grant_type': 'refresh_token',
    			'refresh_token': user.movestoken['refresh_token'],
    			'client_id': '68D1ogxT33tbs850i2nITH1F7fqe4WU3',
    			'client_secret': 'eZXD8kDor6WR8BVz2h07M8ZWv5BKr9u5CkRqe32TQ2R7u1eAov70uuwp3shsQTm6'}
    	r = requests.post('https://api.moves-app.com/oauth/v1/access_token', params=payload)
    	if 'access_token' in r.json().keys():
            user.movestoken = r.json()
        else:
            user.movestoken = None
db.session.commit()