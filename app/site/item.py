from flask import Blueprint,render_template
from flask import Markup
from database_setup import Categories, SportsItem
from app import login_session
from app import session

mod = Blueprint('item',__name__)


@mod.route('/items/<int:id>')
def ShowItem(id):
    item = session.query(SportsItem).filter_by(id=id).one()
    return render_template('item.html', ITEMNAME=item.name, DESCRIPTION=item.info, ITEMID=item.id, SESSION=login_session)

