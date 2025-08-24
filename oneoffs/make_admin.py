import os
import sys
from os.path import dirname, abspath

root_dir = dirname(dirname(abspath(__file__)))
sys.path.append(root_dir)

from app import app, db
from app.models import User
import sqlalchemy as sa


app.app_context().push()

print('*-- GRANT ADMINISTRATOR RIGHTS TO USER --*')
username_to_update = str(input('Username: ')).strip()

user = User.query.filter_by(username=username_to_update).first()
if user:
    print(f"Found account: {user}")
    user.is_admin = True
    db.session.commit()
    print(f"{username_to_update} is now admin.")
else:
    print(f"User {username_to_update} not found.")

print('Done.')