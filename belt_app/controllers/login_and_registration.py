from flask import request, render_template, redirect, flash
from flask.globals import session
from belt_app.models.user import User
from belt_app.models.sighting import Sighting
from belt_app import app
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route("/")
def createPage():
    if 'user_id' not in session:
        return render_template("index.html")
    else:
        return render_template("landingpage.html", user = User.currentUser(session['user_id']), sightings=Sighting.userSighting(session['user_id']))

@app.route("/submitUser", methods=['post'])
def submitUser():
    if not User.validateUser(request.form):
        return redirect("/")
    pwHash = bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name' : request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': pwHash
    }
    newUser = User.newUser(data)
    print("hello")
    return redirect("/")


@app.route("/loginUser", methods=['post'])
def loginUser():
    valid = True
    data = {
        'email' : request.form['email'],
    }
    user = User.findUser(data)
    if not user:
        flash("We don't have that email in our database", 'login')
        return redirect("/")
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Incorrect password", 'login')
        return redirect("/")
    
    session['user_id'] = user.id
    return redirect("/")

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")

@app.route('/users')
def users():
    return render_template("users.html", users = User.showUsers())