from flask import Blueprint, render_template
from flask import Markup, redirect, request, flash
import random
import string
from flask import url_for
from app.database_setup import User, Categories, SportsItem
from app import login_session
from app import session
from app import generateToken
from app import login_required

mod = Blueprint('deleteitem', __name__)


@mod.route('/deleteitem/<int:id>', methods=['GET', 'POST'])
@login_required
def deleteItem(id):
    '''Deletes a specific item from database. Only logged in users can delete their own items'''
    item = session.query(SportsItem).filter_by(id=id).one()
    if(item.userId != login_session["user_id"]):
        flash('Only Item Creators can edit or delete their items')
        print url_for('item.ShowItem', id=id)
        return redirect(url_for('item.ShowItem', id=id))

    if(request.method == 'GET'):
        csrftoken = generateToken()
        return render_template('deleteitem.html', CSRFTOKEN=csrftoken, ITEMNAME=item.name)
    if(request.method == 'POST'):
        if('csrftoken' not in login_session or request.form['csrftoken'] != login_session['csrftoken']):
            abort(400)
        session.delete(item)
        session.commit()
        del login_session['csrftoken']
        return redirect('/')
