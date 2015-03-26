from app import models

users = models.User.query.all()
for user in users:
    print user.email, "-", user.coins, "-", user.wallet