from flask import Blueprint, render_template
from flask import Markup
from app import login_session
from app import session
from app.database_setup import Categories, SportsItem

mod = Blueprint('categories', __name__)


@mod.route('/categories/<int:id>')
def showcategory(id):
    '''Displays items belonging to a specific category'''
    categories = ""
    for category in session.query(Categories):
        if(category.id == id):
            categories += '<a class="list-group-item active" href="/categories/' + \
                str(category.id) + '"' + '>' + category.name + '</a></li>'
        else:
            categories += '<a class="list-group-item" href="/categories/' + \
                str(category.id) + '"' + '>' + category.name + '</a></li>'
    markedupCategories = Markup(categories)
    items = []
    for item in session.query(SportsItem).filter_by(CategoryId=id):
        items.append(item)
    return render_template(
        'category.html',
        CATEGORIES=markedupCategories,
        ITEMS=items,
        SESSION=login_session
    )
