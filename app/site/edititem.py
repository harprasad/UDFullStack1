from flask import Blueprint, render_template
from flask import Markup, redirect, request, flash
from flask import url_for
import random
import string
from app.database_setup import User, Categories, SportsItem
from app import login_session
from app import session
from app import generateToken
from app import login_required


mod = Blueprint('edititem', __name__)


@mod.route('/edititem/<int:id>', methods=['GET', 'POST'])
@login_required
def profile(id):
    item = session.query(SportsItem).filter_by(id=id).one()
    if(item.userId != login_session["user_id"]):
        flash('Only Item Creators can edit or delete their items')
        return redirect(url_for('item.ShowItem', id=id))
    categoryoptions = ""
    for catgory in session.query(Categories):
        if(item.CategoryId == catgory.id):
            categoryoptions += '<option value="' + \
                str(catgory.id) + '" selected>' + catgory.name + '</option>'
        else:
            categoryoptions += '<option value="' + \
                str(catgory.id) + '">' + catgory.name + '</option>'
    markedupOptions = Markup(categoryoptions)
    if(request.method == 'GET'):
        csrftoken = generateToken()
        return render_template(
            'edititem.html',
            OPTIONS=markedupOptions,
            ITEMNAME=item.name,
            DESCRIPTION=item.info,
            CATEGORY=item.CategoryId,
            CSRFTOKEN=csrftoken
        )
    if(request.method == 'POST'):
        if('csrftoken' not in login_session or request.form['csrftoken'] != login_session['csrftoken']):
            abort(400)
        category = session.query(Categories).filter_by(
            id=request.form['categories']).one()
        item.name = request.form['itemname']
        item.info = request.form['description']
        item.CategoryId = request.form['categories']
        item.category = category
        session.commit()
        csrftoken = generateToken()
        return render_template(
            'edititem.html',
            OPTIONS=markedupOptions,
            MESSAGE="Updated",
            ITEMNAME=item.name,
            DESCRIPTION=item.info,
            CATEGORY=item.CategoryId,
            CSRFTOKEN=csrftoken
        )
