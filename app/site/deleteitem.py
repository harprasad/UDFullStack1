from flask import Blueprint,render_template
from flask import Markup,redirect,request
import random
import string
from database_setup import Categories, SportsItem
from app import login_session
from app import session
from app import generateToken
from app import login_required

mod = Blueprint('deleteitem',__name__)

@mod.route('/deleteitem/<int:id>', methods=['GET', 'POST'])
@login_required
def deleteItem(id):
    '''Deletes a specific item from database. Only logged in users can delete their own items'''
    if(request.method == 'GET'):
        item = session.query(SportsItem).filter_by(id=id).one()
        csrftoken = generateToken()
        return render_template('deleteitem.html', CSRFTOKEN=csrftoken, ITEMNAME=item.name)
    if(request.method == 'POST'):
        if('csrftoken' not in login_session or request.form['csrftoken'] != login_session['csrftoken']):
            abort(400)
        item = session.query(SportsItem).filter_by(id=id).one()
        session.delete(item)
        session.commit()
        del login_session['csrftoken']
        return redirect('/')