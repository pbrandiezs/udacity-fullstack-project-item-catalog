#!/usr/bin/env python

# Program: application.py 
# Author: Perry Brandiezs
# Date: May 1, 2019

# See the README.md at vagrant/catalog/README.md
# See the expected output document at vagrant/catalog/Expected_Output.docx


# This program demonstrates CRUD operations using an Item Catalog.

#   Create: Ability to create an airplane item
#   Read:   Ability to read an inventory list showing category name, item name, item description.  Ability to show item detail, login required.
#   Update: Ability to edit item detail, login required.
#   Delete: Ability to delete an item, login required and must be item creator.

# This program demonstrates OAuth2 authentication and authorization using a third party provider.
#   Login / Logout using Facebook is provided, link can be found at the top-right of the main screen.
#   Login required to display item detail, update an item, or delete an item.
#   Must also be the item creator to delete.

# This program demonstrates API endpoints.
#   Display all items
#   Display specific item detail
#   Display all users


from flask import Flask, render_template, request, redirect,jsonify, url_for, flash
from sqlalchemy import create_engine, asc
from sqlalchemy.orm import sessionmaker
from models import Base, User, ItemCatalog, Category
from flask import session as login_session
import random
import string
from oauth2client.client import flow_from_clientsecrets
from oauth2client.client import FlowExchangeError
import httplib2
import json
from flask import make_response
import requests

app = Flask(__name__)

#Connect to Database and create database session
engine = create_engine('sqlite:///ItemCatalog.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

# Create anti-forgery state token
@app.route('/login')
def showLogin():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits)
                    for x in xrange(32))
    login_session['state'] = state
    return render_template('login.html', STATE=state)


# User Helper Functions

def createUser(login_session):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    newUser = User(username=login_session['username'], email=login_session[
                   'email'], picture=login_session['picture'])
    session.add(newUser)
    session.commit()
    user = session.query(User).filter_by(email=login_session['email']).one()
    return user.id


def getUserInfo(user_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    user = session.query(User).filter_by(id=user_id).one()
    return user


def getUserID(email):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    try:
        user = session.query(User).filter_by(email=email).one()
        return user.id
    except:
        return None

# Facebook OAuth2 login
@app.route('/fbconnect', methods=['POST'])
def fbconnect():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if request.args.get('state') != login_session['state']:
      response = make_response(json.dumps('Invalid state parameter.'), 401)
      response.headers['Content-Type'] = 'application/json'
      return response
    access_token = request.data
    #Exchange token for long-lived server-side token
    app_id = json.loads(open('fb_client_secrets.json', 'r').read())['web']['app_id']
    app_secret = json.loads(open('fb_client_secrets.json', 'r').read())['web']['app_secret']
    url = 'https://graph.facebook.com/oauth/access_token?grant_type=fb_exchange_token&client_id=%s&client_secret=%s&fb_exchange_token=%s' % (app_id, app_secret, access_token)
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]

    #Use token to get user info from API
    userinfo_url = "https://graph.facebook.com/v2.8/me"
    '''
        Due to the formatting for the result from the server token exchange we have to
        split the token first on commas and select the first index which gives us the key : value
        for the server access token then we split it on colons to pull out the actual token value
        and replace the remaining quotes with nothing so that it can be used directly in the graph
        api calls
    '''
    token = result.split(',')[0].split(':')[1].replace('"', '')
    url = 'https://graph.facebook.com/v2.8/me?access_token=%s&fields=name,id,email' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data=json.loads(result)
    login_session['provider'] = 'facebook'
    login_session['username'] = data["name"]
    login_session['email'] = data["email"]
    login_session['facebook_id'] = data["id"]
    
    # The token must be stored in the login_session in order to properly logout
    login_session['access_token'] = token

    #Get user picture
    url = 'https://graph.facebook.com/v2.8/me/picture?access_token=%s&redirect=0&height=200&width=200' % token
    h = httplib2.Http()
    result = h.request(url, 'GET')[1]
    data = json.loads(result)

    login_session['picture'] = data["data"]["url"]
    # see if user exists
    user_id = getUserID(login_session['email'])
    if not user_id:
        user_id = createUser(login_session)
    login_session['user_id'] = user_id

    output = ''
    output += '<h1>Welcome, '
    output += login_session['username']
    output += '!</h1>'
    output += '<img src="'
    output += login_session['picture']
    output += ' " style = "width: 300px; height: 300px;border-radius: 150px;-webkit-border-radius: 150px;-moz-border-radius: 150px;"> '
    flash("you are now logged in as %s" % login_session['username'])
    print "done!"
    return output

# Facebook OAuth2 logout
@app.route('/fbdisconnect')
def fbdisconnect():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    facebook_id = login_session['facebook_id']
    access_token = login_session['access_token']
    url = 'https://graph.facebook.com/%s/permissions?access_token=%s' % (facebook_id,access_token)
    h = httplib2.Http()
    result = h.request(url, 'DELETE')[1]
    return "you have been logged out"

@app.route('/disconnect')
def disconnect():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if 'provider' in login_session:
        if login_session['provider'] == 'facebook':
            fbdisconnect()
            del login_session['facebook_id']
        del login_session['username']
        del login_session['email']
        del login_session['picture']
        del login_session['user_id']
        del login_session['provider']
        flash("You have successfully been logged out.")
        return redirect(url_for('showItemCatalog'))
    else:
        flash("You were not logged in to begin with!")
        redirect(url_for('showItemCatalog'))


# Show all Catalog Items
# This is an example of CRUD: Read
@app.route('/')
@app.route('/items/')
def showItemCatalog():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    # items = session.query(ItemCatalog).order_by(asc(ItemCatalog.category_name), asc(ItemCatalog.item_name))
    items = session.query(ItemCatalog)
    # check if logged in
    if 'username' not in login_session:
        # not logged in, display public items
        return render_template('publicitems.html', items = items)
    else:
        # logged in, display items (including creator)
        return render_template('items.html', items = items)

# Create a new item
# This is an example of CRUD: Create
@app.route('/item/new/', methods=['GET','POST'])
def newItem():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    if 'username' not in login_session:
        return redirect('/login')
    if request.method == 'POST':
        newItem = ItemCatalog(category_name = request.form['category_name'],
        item_name = request.form['item_name'],
        item_description = request.form['item_description'],
        user_id=login_session['user_id'])
        session.add(newItem)
        flash('New Item %s Successfully Created' % newItem.item_name)
        session.commit()
        return redirect(url_for('showItemCatalog'))
    else:
        return render_template('newItem.html')

# Edit a item
# This is an example of CRUD: Update
@app.route('/item/<int:id>/edit/', methods = ['GET', 'POST'])
def editItem(id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    editedItem = session.query(ItemCatalog).filter_by(id = id).one()
    if 'username' not in login_session:
        # not logged in, display public items
        flash("Login required to edit!")
        return redirect(url_for('showItemCatalog'))
    if request.method == 'POST':
        if request.form['item_name'] and request.form['category_name'] and request.form['item_description']:
            editedItem.category_name = request.form['category_name']
            editedItem.item_name = request.form['item_name']
            editedItem.item_description = request.form['item_description']
            session.add(editedItem)
            session.commit()
            return redirect(url_for('showItemCatalog'))
    else:
        return render_template('editItem.html', item = editedItem)


# Delete an item
# This is an example of CRUD: Delete
@app.route('/item/<int:id>/delete/', methods = ['GET','POST'])
def deleteItem(id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    itemToDelete = session.query(ItemCatalog).filter_by(id = id).one()
    # check if logged in
    if 'username' not in login_session:
        # not logged in, display public items
        flash("Login required to delete!")
        return redirect(url_for('showItemCatalog'))
    if itemToDelete.user_id != login_session['user_id']:
        # return "<script>function myFunction() {alert('You are not authorized to delete this item.  Please create your own item in order to delete.');}</script><body onload='myFunction()''>"
        flash("Not authorized to delete this item!  Create your own item to delete.")
        return redirect(url_for('showItemCatalog'))
    if request.method == 'POST':
        session.delete(itemToDelete)
        flash('%s Successfully Deleted' % itemToDelete.item_name)
        session.commit()
        return redirect(url_for('showItemCatalog'))
    else:
        return render_template('deleteItem.html', item = itemToDelete)



# Show an item
# An example of CRUD: Read
@app.route('/item/<int:item_id>/')
def showItem(item_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    item = session.query(ItemCatalog).filter_by(id = item_id).one()
    creator = getUserInfo(item.user_id)
    items = session.query(ItemCatalog).filter_by(id = ItemCatalog.id).all()
    username = session.query(User.username).filter_by(id = creator.id).one()
    #Check if logged in
    if 'username' not in login_session:
        flash('Must log in to view item detail!')
        return render_template('publicitems.html', items = items)
    else:
        return render_template('item.html', item = item, username = username[0])

# JSON endpoint to show all items
@app.route('/items/JSON')
def itemsJSON():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    items = session.query(ItemCatalog).all()
    return jsonify(items = [item.serialize for item in items])

# JSON endpoint to show a specific item
@app.route('/item/<int:item_id>/JSON')
def itemJSON(item_id):
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    item = session.query(ItemCatalog).filter_by(id = item_id).one()
    creator = getUserInfo(item.user_id)
    items = session.query(ItemCatalog).filter_by(id = ItemCatalog.id).all()
    username = session.query(User.username).filter_by(id = creator.id).one()
    #Check if logged in
    if 'username' not in login_session:
        #not logged in
        return jsonify({"item": [
            {
                "category_id": item.category_id,
                "id": item.id,
                "item_description": item.item_description,
                "item_name": item.item_name,
            }]
        })
    else:
        # logged in, include creator with the result
        return jsonify({"item": [
            {
                "category_id": item.category_id,
                "id": item.id,
                "item_description": item.item_description,
                "item_name": item.item_name,
                "creator": username[0]
            }]
        })

# JSON endpoint to show all users
@app.route('/users/JSON')
def usersJSON():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    users = session.query(User).all()
    return jsonify(users = [user.serialize for user in users])

# JSON endpoint to show all categories
@app.route('/categories/JSON')
def categoriesJSON():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    categories = session.query(Category).all()
    return jsonify(categories = [category.serialize for category in categories])

# Main run web server using port 8000
if __name__ == '__main__':
  app.secret_key = 'super_secret_key'
  app.debug = True
  app.run(host = '0.0.0.0', port = 8000)
