from flask import Blueprint,render_template
from flask import Markup,redirect,request
import random
import string
from database_setup import Categories, SportsItem
from app import login_session
from app import session
from app import generateToken
from app import login_required

mod = Blueprint('additem',__name__)

@mod.route('/additem', methods=['GET', 'POST'])
'''A function to allow logged in users to add items'''
@login_required
def additem():
    if(request.method == 'GET'):
        categoryoptions = ""
        for catgory in session.query(Categories):
            categoryoptions += '<option value="' + \
                str(catgory.id) + '">' + catgory.name + '</option>'
        markedupOptions = Markup(categoryoptions)
        csrftoken = generateToken()
        return render_template("additem.html", OPTIONS=markedupOptions, CSRFTOKEN=csrftoken)
    if(request.method == 'POST'):
        if('csrftoken' not in login_session or request.form['csrftoken'] != login_session['csrftoken']):
            abort(400)
        item = SportsItem(
            name=request.form['itemname'], info=request.form['description'], CategoryId=request.form['categories'])
        session.add(item)
        session.commit()
        categoryoptions = ""
        for catgory in session.query(Categories):
            categoryoptions += '<option value="' + \
                str(catgory.id) + '">' + catgory.name + '</option>'
        markedupOptions = Markup(categoryoptions)
        csrftoken = generateToken()
        return render_template("additem.html", OPTIONS=markedupOptions, MESSAGE="Added " + request.form['itemname'], CSRFTOKEN=csrftoken)
