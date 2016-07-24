from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
app = Flask(__name__)

from database_setup import Restaurant, Base, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()



@app.route('/rest/<int:restaurant_id>/menu/JSON')
def restaurantMenuJSON(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id).all()
	return jsonify(MenuItems=[i.serialize for i in items])


@app.route('/rest/<int:restaurant_id>/menu/<int:menu_id>/JSON')
def restaurantItemMenuJSON(restaurant_id, menu_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	itemname = session.query(MenuItem).filter_by(id = menu_id).one()
	return jsonify(MenuItem=itemname.serialize)


@app.route('/')
@app.route('/rest')
def showRestaurants():
	restaurants = session.query(Restaurant).all()
	return render_template('restaurants.html', restaurants = restaurants)




@app.route('/rest/<int:restaurant_id>/')
def restaurantMenu(restaurant_id):
	restaurant = session.query(Restaurant).filter_by(id = restaurant_id).one()
	items = session.query(MenuItem).filter_by(restaurant_id = restaurant_id)
	return render_template('menu.html', restaurant = restaurant, items = items)


# Task 1: Create route for newMenuItem function here
@app.route('/rest/<int:restaurant_id>/new', methods = ['GET', 'POST'])
def newMenuItem(restaurant_id):
	if request.method == 'POST':
		newItem = MenuItem(name = request.form['name'], restaurant_id = restaurant_id)
		session.add(newItem)
		session.commit()
		flash("new menu item called %s has been created!" % request.form['name'])
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
		return render_template('newmenuitem.html', restaurant_id = restaurant_id)
    # return "page to create a new menu item. Task 1 complete!"


# Task 2: Create route for editMenuItem function here
@app.route('/rest/<int:restaurant_id>/<int:menu_id>/edit', methods = ['GET', 'POST'])
def editMenuItem(restaurant_id, menu_id):
    editItem = session.query(MenuItem).filter_by(id = menu_id).one()
    if request.method == 'POST':
    	if request.form['name']:
    		editItem.name = request.form['name']
    		session.add(editItem)
    		session.commit()
    		flash("menu item has been edited!")
    		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
    else:
    	return render_template('editmenuitem.html', restaurant_id=restaurant_id, menu_id=menu_id, i=editItem)


# return "page to edit a menu item. Task 2 complete!"

# Task 3: Create a route for deleteMenuItem function here
@app.route('/rest/<int:restaurant_id>/<int:menu_id>/delete', methods = ['GET', 'POST'])
def deleteMenuItem(restaurant_id, menu_id):
	deleteItem = session.query(MenuItem).filter_by(id = menu_id).one()
	if request.method == 'POST':
		session.delete(deleteItem)
		session.commit()
		flash("menu item has been Deleted!")
		return redirect(url_for('restaurantMenu', restaurant_id = restaurant_id))
	else:
		return render_template('deletemenuitem.html', restaurant_id=restaurant_id, item=deleteItem)


    # return "page to delete a menu item. Task 3 complete!"

if __name__ == '__main__':
	app.secret_key = 'super_secret_key'
	app.debug = True
	app.run(host = '0.0.0.0', port = 5000)
