from flask import Flask
from flask import session as login_session
from sqlalchemy.orm import sessionmaker
from database_setup import engine
import random
import string

DBSession = sessionmaker(bind=engine)
session = DBSession()

def generateToken():
    token = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['csrftoken'] = token
    return token

app = Flask(__name__)
app.secret_key = 'super_secret_key'

from app.site.home import mod
from app.site.categories import mod
from app.site.item import mod
from app.site.edititem import mod
app.register_blueprint(site.home.mod)
app.register_blueprint(site.categories.mod)
app.register_blueprint(site.item.mod)
app.register_blueprint(site.edititem.mod)