from flask import render_template, request, redirect, url_for, jsonify, flash
from flask_httpauth import HTTPBasicAuth

from . import main
from .. import db
from ..models import Restaurant, MenuItem

auth = HTTPBasicAuth()


@main.route('/')
@main.route('/restaurants/')
@auth.login_required
def display_restaurants():
    """
    Display a list of all restaurants
    :return: restaurants page
    """
    restaurants = db.session.query(Restaurant).all()
    return render_template('restaurants.html', restaurants=restaurants)


@main.route('/restaurant/new/', methods=['GET', 'POST'])
def create_restaurant():
    """
    Create a new restaurant
    :return: create restaurant page
    """
    if request.method == 'POST':
        # request.form stores form data!
        restaurant = Restaurant(name=request.form['restaurant_name'])
        db.session.add(restaurant)
        db.session.commit()
        flash('New Restaurant Created')
        return redirect(url_for('display_restaurants'))
    else:
        return render_template('create_restaurant.html')


@main.route('/restaurant/<int:restaurant_id>/edit/', methods=['GET', 'POST'])
def edit_restaurant(restaurant_id):
    """
    Rename restaurant
    :param restaurant_id: id of restaurant
    :return: edit restaurant page
    """
    if request.method == 'POST':
        # update syntax is weird!
        db.session.query(Restaurant).filter_by(id=restaurant_id).update({Restaurant.name: request.form['edit']})
        db.session.commit()
        flash('Restaurant Succesfully Edited')
        return redirect(url_for('display_restaurants'))
    else:
        restaurant = db.session.query(Restaurant).filter_by(id=restaurant_id).first()
        return render_template('edit_restaurant.html', restaurant=restaurant)


@main.route('/restaurant/<int:restaurant_id>/delete/', methods=['GET', 'POST'])
def delete_restaurant(restaurant_id):
    """
    delete restaurant
    :param restaurant_id: id of restaurant
    :return: delete restaurant page
    """
    if request.method == 'POST':
        db.session.query(Restaurant).filter_by(id=restaurant_id).delete()
        db.session.commit()
        flash('Restaurant Successfully Deleted')
        return redirect(url_for('display_restaurants'))
    else:
        restaurant = db.session.query(Restaurant).filter_by(id=restaurant_id).first()
        return render_template('delete_restaurant.html', restaurant=restaurant)


@main.route('/restaurant/<int:restaurant_id>/')
@main.route('/restaurant/<int:restaurant_id>/menu/')
def display_restaurant_menu(restaurant_id):
    """
    Display a restaurant menu with menu items sorted by course
    :param restaurant_id:  restaurant id
    :return: restaurant menu page
    """
    menu_items = db.session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return render_template('menu.html', menu_items=menu_items, restaurant_id=restaurant_id)


@main.route('/restaurant/<int:restaurant_id>/menu/new/', methods=['GET', 'POST'])
def create_menu_item(restaurant_id):
    """
    Create menu item
    :param restaurant_id: restaurant id
    :return: create restaurant page
    """
    if request.method == 'POST':
        menu_item = MenuItem(name=request.form['menu_item_name'],
                             course=request.form['menu_item_course'],
                             price=request.form['menu_item_price'],
                             description=request.form['menu_item_description'],
                             restaurant_id=restaurant_id,)
        db.session.add(menu_item)
        db.session.commit()
        flash('Menu Item Created')
        return redirect(url_for('display_restaurant_menu', restaurant_id=restaurant_id))
    else:
        return render_template('create_menu_item.html', restaurant_id=restaurant_id)


@main.route('/restaurant/<int:restaurant_id>/menu/<int:menu_item_id>/edit/', methods=['GET', 'POST'])
def edit_menu_item(restaurant_id, menu_item_id):
    """
    Rename a menu item
    :param restaurant_id: restaurant id
    :param menu_item_id: menu item id
    :return: edit menu item page
    """
    if request.method == 'POST':
        db.session.query(MenuItem).filter_by(id=menu_item_id).update({MenuItem.name: request.form['menu_item_name']})
        db.session.commit()
        flash('Menu Item Successfully Edited')
        return redirect(url_for('display_restaurant_menu', restaurant_id=restaurant_id))
    else:
        menu_item = db.session.query(MenuItem).filter_by(id=menu_item_id).first()
        return render_template('edit_menu_item.html', restaurant_id=restaurant_id, menu_item=menu_item)


@main.route('/restaurant/<int:restaurant_id>/menu/<int:menu_item_id>/delete/', methods=['GET', 'POST'])
def delete_menu_item(restaurant_id, menu_item_id):
    """
    Delete menu item
    :param restaurant_id: restaurant id
    :param menu_item_id: menu item id
    :return: delete menu item page
    """
    if request.method == 'POST':
        db.session.query(MenuItem).filter_by(id=menu_item_id).delete()
        db.session.commit()
        flash('Menu Item Successfully Deleted')
        return redirect(url_for('display_restaurant_menu', restaurant_id=restaurant_id))
    else:
        menu_item = db.session.query(MenuItem).filter_by(id=menu_item_id).first()
        return render_template('delete_menu_item.html', restaurant_id=restaurant_id, menu_item=menu_item)


@main.route('/restaurants/JSON')
def restaurants_json():
    """
    jsonify restaurants
    :return: restaurants in JSON format
    """
    restaurants = db.session.query(Restaurant).all()
    return jsonify(restaurants=[restaurant.serialize for restaurant in restaurants])


@main.route('/restaurant/<int:restaurant_id>/menu/JSON')
def restaurant_menu_json(restaurant_id):
    """
    jsonify restaurant menu
    :param restaurant_id: restaurant id
    :return: restaurant menu in JSON format
    """
    menu_items = db.session.query(MenuItem).filter_by(restaurant_id=restaurant_id).all()
    return jsonify(menu_items=[menu_item.serialize for menu_item in menu_items])


@main.route('/restaurant/<int:restaurant_id>/menu/<int:menu_item_id>/JSON')
def restaurant_menu_item_json(restaurant_id, menu_item_id):
    """
    jsonify menu item
    :param restaurant_id: restaurant id
    :param menu_item_id: menu item id
    :return: menu item in JSON format
    """
    menu_item = db.session.query(MenuItem).filter_by(id=menu_item_id).first()
    if menu_item:
        return jsonify(menu_item=menu_item.serialize)
    else:
        return "Menu item does not exist. JSON not available"