from flask import Flask, render_template, request, redirect,jsonify, url_for, flash
app = Flask(__name__)
from flask import Markup
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from database_setup import Categories,SportsItem,engine
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

#Connect to Database and create database session
DBSession = sessionmaker(bind= engine)
session = DBSession()

CLIENT_ID = json.loads(open('client_secrets.json','r').read())['web']['client_id']


@app.route('/login')
def ShowLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html',STATE = state)

@app.route('/gconnect',methods=['POST'])
def gconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state tokens'),401)
        response.headers['Content-Type'] = 'application/json'
        return response
    code = request.data
    try:
        oauth_flow = flow_from_clientsecrets('client_secrets.json',scope='')
        oauth_flow.redirect_uri = 'postmessage'
        credentials = oauth_flow.step2_exchange(code)
    except FlowExchangeError:
        response = make_response(json.dumps('Failed to upgrade the athorization code'),401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = credentials.access_token
    url = ('https://www.googleapis.com/oauth2/v1/tokeninfo?access_token=%s'
           % access_token)
    h = httplib2.Http()
    result = json.loads(h.request(url, 'GET')[1])
    # If there was an error in the access token info, abort.
    if result.get('error') is not None:
        response = make_response(json.dumps(result.get('error')), 500)
        response.headers['Content-Type'] = 'application/json'
        return response
    # Verify that the access token is used for the intended user.
    gplus_id = credentials.id_token['sub']
    if result['user_id'] != gplus_id:
        response = make_response(
            json.dumps("Token's user ID doesn't match given user ID."), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
        
    stored_access_token = login_session.get('access_token')
    stored_gplus_id = login_session.get('gplus_id')
    if stored_access_token is not None and gplus_id == stored_gplus_id:
        response = make_response(json.dumps('Current user is already connected.'),
                                 200)
        response.headers['Content-Type'] = 'application/json'
        return response

     # Store the access token in the session for later use.
    login_session['access_token'] = credentials.access_token
    login_session['gplus_id'] = gplus_id

    # Get user info
    userinfo_url = "https://www.googleapis.com/oauth2/v1/userinfo"
    params = {'access_token': credentials.access_token, 'alt': 'json'}
    answer = requests.get(userinfo_url, params=params)

    data = answer.json()

    login_session['username'] = data['name']
    login_session['picture'] = data['picture']
    login_session['email'] = data['email']

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

@app.route('/gdisconect')
def gdisconnect():
    if credentials is None:
        response = make_response(json.dumps('current user not connected'),401)
        response.headers['Content-Type'] = 'application/json'
        return response

    access_token = credentials.access_token
    if access_token is None:
        print 'Access Token is None'
        response = make_response(json.dumps('Current user not connected.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    print 'In gdisconnect access token is %s', access_token
    print 'User name is: '
    print login_session['username']
    url = 'https://accounts.google.com/o/oauth2/revoke?token=%s' % login_session['access_token']
    h = httplib2.Http()
    result = h.request(url, 'GET')[0]
    print 'result is '
    print result
    if result['status'] == '200':
        del login_session['access_token']
        del login_session['gplus_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        response = make_response(json.dumps('Successfully disconnected.'), 200)
        response.headers['Content-Type'] = 'application/json'
        return response
    else:
        response = make_response(json.dumps('Failed to revoke token for given user.', 400))
        response.headers['Content-Type'] = 'application/json'
        return response




@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    if request.args.get('state') != login_session['state']:
        response = make_response(json.dumps('Invalid state parameter.'), 401)
        response.headers['Content-Type'] = 'application/json'
        return response
    access_token = request.data
    print "access token received %s " % access_token


    app_id = json.loads(open('fb_client_secrets.json', 'r').read())[
        'web']['app_id']
    app_secret = json.loads(
        open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (
        app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]


    # Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    '''
        Due to the formatting for the result from the server token exchange we have to
        split the token first on commas and select the first index which gives us the key : value
        for the server access token then we split it on colons to pull out the actual token value
        and replace the remaining quotes with nothing so that it can be used directly in the graph
        api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')

    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    # print "url sent for API access:%s"% url
    # print "API JSON result: %s" % result
    data = json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]

    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    # Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]

    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']

    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '

    flash("Now logged in as %s" % login_session['username'])
    return output


@app.route('/fbdisconnect')
def fbdisconnect():
    facebook_id = login_session['facebook_id']
    # The access token must me included to successfully logout
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"

# Disconnect based on provider
@app.route('/disconnect')
def disconnect():
    if 'provider' in login_session:
        if login_session['provider'] == 'google':
            gdisconnect()
            del login_session['gplus_id']
            del login_session['access_token']
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('home'))
    else:
        flash("You were not logged in")
        return redirect(url_for('home'))


@app.route('/')
def home():
    categories = ""
    recententries = ""
    for category in session.query(Categories):
        categories += '<a class="list-group-item" href="/categories/'+ str(category.id) +'"'+ '>'+ category.name +'</a></li>'
    
    markedupCategories = Markup(categories)
    items =  session.query(SportsItem).order_by(SportsItem.id.desc()).limit(10)
    return render_template('home.html',CATEGORIES = markedupCategories,ITEMS = items) 
    
@app.route('/categories/<int:id>')
def showcategory(id):
    categories = ""
    for category in session.query(Categories):
        if(category.id == id):
            categories += '<a class="list-group-item active" href="/categories/'+ str(category.id) +'"'+ '>'+ category.name +'</a></li>'
        else:
            categories += '<a class="list-group-item" href="/categories/'+ str(category.id) +'"'+ '>'+ category.name +'</a></li>'
    markedupCategories = Markup(categories)
    items = []
    for item in session.query(SportsItem).filter_by(CategoryId = id):
        items.append(item)
    return render_template('category.html',CATEGORIES = markedupCategories,ITEMS = items) 

@app.route('/items/<int:id>')
def ShowItem(id):
    item = session.query(SportsItem).filter_by(id = id).one()
    return render_template('item.html',ITEMNAME =  item.name,DESCRIPTION = item.info,ITEMID=item.id)

@app.route('/edititem/<int:id>',methods=['GET','POST'])
def profile(id):
    if 'username' not in login_session:
        return redirect('/login')
    item = session.query(SportsItem).filter_by(id = id).one()
    categoryoptions = ""
    for catgory in session.query(Categories):
        if(item.CategoryId == catgory.id):
            categoryoptions += '<option value="' + str(catgory.id) + '" selected>'+ catgory.name +'</option>'
        else:
            categoryoptions += '<option value="' + str(catgory.id) + '">'+ catgory.name +'</option>'
    markedupOptions = Markup(categoryoptions) 
    if(request.method == 'GET'):
        csrftoken = generateToken()
        return render_template('edititem.html',OPTIONS = markedupOptions,ITEMNAME =  item.name,DESCRIPTION = item.info,CATEGORY = item.CategoryId,CSRFTOKEN = csrftoken)
    if(request.method == 'POST'):
        if('csrftoken' not in login_session or request.form['csrftoken'] != login_session['csrftoken']):
            abort(400)
        item.name = request.form['itemname']
        item.info = request.form['description']
        item.CategoryId = request.form['categories']
        session.commit()
        csrftoken = generateToken()
        return render_template('edititem.html',OPTIONS = markedupOptions,MESSAGE = "Updated",ITEMNAME =  item.name,DESCRIPTION = item.info,CATEGORY = item.CategoryId,CSRFTOKEN = csrftoken)

@app.route('/additem',methods=['GET','POST'])
def additem():
    if 'username' not in login_session:
        return redirect('/login') 
    if(request.method == 'GET'):
        categoryoptions = ""
        for catgory in session.query(Categories):
            categoryoptions += '<option value="' + str(catgory.id) + '">'+ catgory.name +'</option>'
        markedupOptions = Markup(categoryoptions)
        csrftoken = generateToken()
        return render_template("additem.html",OPTIONS = markedupOptions,CSRFTOKEN = csrftoken)
    if(request.method == 'POST'):
        if('csrftoken' not in login_session or request.form['csrftoken'] != login_session['csrftoken']):
            abort(400)
        item = SportsItem(name = request.form['itemname'],info = request.form['description'],CategoryId = request.form['categories'])
        session.add(item)
        session.commit()
        categoryoptions = ""
        for catgory in session.query(Categories):
            categoryoptions += '<option value="' + str(catgory.id) + '">'+ catgory.name +'</option>'
        markedupOptions = Markup(categoryoptions)
        csrftoken = generateToken()
        return render_template("additem.html",OPTIONS = markedupOptions,MESSAGE = "Added " +request.form['itemname'],CSRFTOKEN = csrftoken)

@app.route('/deleteitem/<int:id>',methods=['GET','POST'])
def deleteItem(id):
    if 'username' not in login_session:
        return redirect('/login')
    if(request.method == 'GET'):
        item = session.query(SportsItem).filter_by(id = id).one()
        csrftoken = generateToken()
        return render_template('deleteitem.html',CSRFTOKEN = csrftoken,ITEMNAME = item.name)
    if(request.method == 'POST'):
        if('csrftoken' not in login_session or request.form['csrftoken'] != login_session['csrftoken']):
            abort(400)
        item = session.query(SportsItem).filter_by(id = id).one()
        session.delete(item)
        session.commit()
        del login_session['csrftoken']
        return redirect('/')


def generateToken():
    token = ''.join(random.choice(string.ascii_uppercase + string.digits)
                for x in xrange(32))
    login_session['csrftoken'] = token
    return token

if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 5000)
