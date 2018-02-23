from flask import Flask, render_template, request, redirect
from flask import jsonify, url_for, flash
from flask import Markup
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Categories, SportsItem, engine
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests
from sqlalchemy import desc
from flask import abort


app = Flask(__name__)

from site.home import mod

app.register_blueprint(site.home.mod)

#Connect to Database and create database session
DBSession = sessionmaker(bind=engine)
session = DBSession()














def generateToken():
    token = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['csrftoken'] = token
    return token

#API codes starts here




if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host='0.0.0.0', port=5000)
