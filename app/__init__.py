from flask import Flask,redirect,flash
from flask import session as login_session
from functools import wraps
from sqlalchemy.orm import sessionmaker
from database_setup import engine
import random
import string


DBSession = sessionmaker(bind=engine)
session = DBSession()

def generateToken():
    """Generates a random token and stores in login_seesion mainly used as csrf token"""
    token = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['csrftoken'] = token
    return token

def login_required(function):
    @wraps(function)
    def wrapper( *args, **kwargs ):
        if 'username' in login_session:
            function()
        else:
            flash('A user must be logged in to add update or delete item.')
            return redirect('/login')
    return wrapper

app = Flask(__name__)
app.secret_key = 'super_secret_key'

from app.site.home import mod
from app.site.categories import mod
from app.site.item import mod
from app.site.edititem import mod
from app.site.additem import mod
from app.site.login import mod
from app.site.deleteitem import mod
from app.api.endpoints import mod

app.register_blueprint(site.home.mod)
app.register_blueprint(site.categories.mod)
app.register_blueprint(site.item.mod)
app.register_blueprint(site.edititem.mod)
app.register_blueprint(site.additem.mod)
app.register_blueprint(site.login.mod)
app.register_blueprint(site.deleteitem.mod)

app.register_blueprint(api.endpoints.mod,uri_prefix = '/api')