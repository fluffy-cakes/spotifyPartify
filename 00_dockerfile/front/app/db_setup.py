from main import app, db, User
import json

users = open("./users.json")
data  = json.load(users)

db.create_all(app=app)

with app.app_context():
    for x in data['users']:
        db.session.add(User(username=x))
        db.session.commit()


exit()

# Commands to test from terminal:
# sqlite3 db.sqlite3
# select * from user;
# .exit
