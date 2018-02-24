from flask import Blueprint, render_template
from flask import Markup, redirect, request, flash
import random
import string
from app.database_setup import User, Categories, SportsItem
from app import login_session
from app import session
from app import generateToken
from app import login_required
from app import getUserInfo
mod = Blueprint('additem', __name__)


@mod.route('/additem', methods=['GET', 'POST'])
@login_required
def additem():
    '''A function to allow logged in users to add items'''
    if(request.method == 'GET'):
        categoryoptions = ""
        for catgory in session.query(Categories):
            categoryoptions += '<option value="' + \
                str(catgory.id) + '">' + catgory.name + '</option>'
        markedupOptions = Markup(categoryoptions)
        csrftoken = generateToken()
        print csrftoken
        return render_template(
            "additem.html",
            OPTIONS=markedupOptions,
            CSRFTOKEN=csrftoken
        )

    if(request.method == 'POST'):
        if('csrftoken' not in login_session or request.form['csrftoken'] != login_session['csrftoken']):
            abort(400)
        print request.form
        category = session.query(Categories).filter_by(
            id=request.form['categories']).one()
        user = getUserInfo(login_session['user_id'])
        item = SportsItem(
            name=request.form['itemname'],
            info=request.form['description'],
            CategoryId=request.form['categories'],
            category=category,
            userId=login_session['user_id'],
            user=user
        )
        session.add(item)
        session.commit()
        categoryoptions = ""
        for catgory in session.query(Categories):
            categoryoptions += '<option value="' + \
                str(catgory.id) + '">' + catgory.name + '</option>'
        markedupOptions = Markup(categoryoptions)
        csrftoken = generateToken()
        return render_template(
            "additem.html",
            OPTIONS=markedupOptions,
            MESSAGE="Added " + request.form['itemname'],
            CSRFTOKEN=csrftoken,
        )
