from flask import render_template, request, redirect, flash, session, abort
from sqlalchemy.sql import text
from app import app
from db import db
from restaurants import search_restaurants, delete_restaurant, get_all_restaurants, add_restaurant
from reviews import get_reviews, add_review
import users

'''
Flaw no.5 fix

from logging import getLogger, ERROR

logger = getLogger('login_activity')
logger.setLevel(ERROR)

def log_access_control_failure(username):
    logger.error(f'Access control failure for user: {username}')

'''
@app.route("/")
def index():
    return render_template("home.html")

@app.route("/new")
def new():
    restaurants = get_all_restaurants()
    return render_template("new.html", restaurants=restaurants)

@app.route("/restaurants")
def restaurants():
    username = session['username']
    restaurants = get_all_restaurants()
    is_admin = users.admins(username)
    return render_template("restaurants.html", count=len(restaurants), restaurants=restaurants, is_admin = is_admin) 
 

@app.route("/review")
def reviews():
    restaurants_all = get_reviews()
    return render_template("reviews.html", count=len(restaurants_all), restaurants=restaurants_all) 

@app.route("/add_review", methods=["POST"])
def reviews_to_db():
    restaurant_id = request.form.get('restaurant_id')
    stars = request.form.get('stars')
    comment = request.form.get('comment')

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    if not stars:
        return redirect(request.referrer)
    
    add_review(restaurant_id, stars, comment)
    return redirect('/review')

@app.route("/send", methods=["POST"])
def send():
    name = request.form["name"]
    address = request.form["address"]
    city = request.form["city"]
    categories = request.form.get('categories')

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    if add_restaurant(name, address, city, categories):
        return redirect("/restaurants")
    else:
        message = "Restaurant with name {} already exists".format(name)
        return render_template("new.html", message=message)

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]

    if users.login(username,password) == False:
        flash('Invalid username or password')
        return redirect('/')
    
    else:
        return redirect("/restaurants")
    
    '''
    Flow no.5 fix

    logger.error('Login attempt initiated')

    username = request.form["username"]
    password = request.form["password"]

    if users.login(username,password) == False:
        # Logging failed login attempt
        logger.error(f'Failed login attempt for user: {username}')
        log_access_control_failure(username)

        flash('Invalid username or password')
        return redirect('/')
    
    else:
        # Logging successful login
        logger.error(f'User {username} successfully logged in')

        return redirect("/restaurants")'''

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/create_account", methods=["POST"])
def craete_account():
    username = request.form["username"]
    password = request.form["password"]

    if not username or not password:
        flash('Väärä käyttäjä tai salasana')
        return redirect('/')

    if len(username) < 4:
        flash('Käyttäjänimen täytyy olla vähintään 4 merkkiä')
        return redirect('/')
    
    if len(password) < 6:
        flash('Salasanan täytyy olla vähintään 6 merkkiä')
        return redirect('/')
    
    users.create_account(username,password)

    return redirect('/restaurants')

@app.route("/search", methods=["POST"])
def search():
    substring = request.form.get('name')
    filtered_restaurants = search_restaurants(substring)

    html_response = f"<html><body>Count: {len(filtered_restaurants)}<br>Restaurants: {filtered_restaurants}</body></html>"
    
    return html_response

    '''
    Flaw no.4 fix
    return render_template('filtered.html', count=len(filtered_restaurants), restaurants=filtered_restaurants)
    '''

@app.route("/delete", methods=["POST"])
def delete():

    '''
    #Flaw no.2 fix

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    '''

    '''
    #Flaw no.1 fix

    username = session.get('username')
    if not users.admins(username):
        abort(401)  # Unauthorized access

    '''
    restaurant_id = request.form.get('restaurant_id')
    delete_restaurant(restaurant_id)
    return redirect("/restaurants")
