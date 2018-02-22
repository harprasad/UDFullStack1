from flask import Blueprint,render_template
from flask import Markup
from database_setup import Categories, SportsItem
from app import login_session
from app import session


mod = Blueprint('home',__name__)

@mod.route('/')
def home():
    categories = ""
    recententries = ""
    for category in session.query(Categories):
        categories += '<a class="list-group-item" href="/categories/' + \
            str(category.id) + '"' + '>' + category.name + '</a></li>'

    markedupCategories = Markup(categories)
    items = session.query(SportsItem).order_by(SportsItem.id.desc()).limit(10)
    return render_template('home.html', CATEGORIES=markedupCategories, ITEMS=items, SESSION=login_session)
