from flask import Blueprint, render_template
from flask import Markup
from app.database_setup import Categories, SportsItem
from app import login_session
from app import session
from flask import jsonify

mod = Blueprint('endpoints', __name__)


@mod.route('/api/v1.0/catalog')
def showCatalog():
    CategorieList = []
    for category in session.query(Categories).all():
        categoryobj = category.serialize
        for item in session.query(SportsItem).filter_by(CategoryId=category.id):
            categoryobj['items'].append(item.serialize)

        CategorieList.append(categoryobj)
    return jsonify(Categories=CategorieList)


@mod.route('/api/v1.0/items/<int:id>')
def ShowItem(id):
    item = session.query(SportsItem).filter_by(id=id).one()
    return jsonify(Item=item.serialize)


@mod.route('/api/v1.0/category/<int:id>')
def ShowCaategory(id):
    items = []
    for item in session.query(SportsItem).filter_by(CategoryId=id):
        items.append(item.serialize)
    return jsonify(Items=items)
