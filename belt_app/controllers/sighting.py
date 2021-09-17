import re
from flask import request, render_template, redirect, flash
from flask.globals import session
from belt_app.models.user import User
from belt_app.models.sighting import Sighting
from belt_app.models.skeptics import Skeptic
from belt_app import app

@app.route("/all_sightings")
def allSightings():
    return render_template("sightings.html", user=User.currentUser(session['user_id']), sightings=Sighting.findAll())

@app.route("/report_sighting")
def reportSighting():
    return render_template("reportsighting.html", user=User.currentUser(session['user_id']))

@app.route("/newSighting", methods=['post'])
def newSighting():
    curUser = User.currentUser(session['user_id'])
    data = {
        'location' : request.form['location'],
        'what_happened' : request.form['what_happened'],
        'reported_at' : request.form['reported_at'],
        'name_reported' : f'{curUser.first_name} {curUser.last_name}',
        'reported_by' : session['user_id'],
        'num_of_sas' : request.form['num_of_sas']
    }
    newSighting = Sighting.newSighting(data)
    return redirect("/")

@app.route("/view/<id>")
def viewSighting(id):
    believed = False
    skeptics = Skeptic.skepticNames(id)
    if skeptics != False:
        for row in Skeptic.skepticNames(id):
            if session['user_id'] == row['user_id']:
                believed = True
    
    return render_template("viewSighting.html", user=User.currentUser(session['user_id']), 
    sighting=Sighting.findSighting(id), 
    time=Sighting.findTime(id), 
    skeptics=skeptics,
    believed=believed)

@app.route("/edit/<id>")
def editSighting(id):
    return render_template("updateSighting.html", user=User.currentUser(session['user_id']), sighting=Sighting.findSighting(id))

@app.route("/updateSighting/<id>", methods=['post'])
def updateSighting(id):
    data = {
        **request.form
    }
    Sighting.updateSighting(data, id)
    return redirect(f"/view/{id}")

@app.route('/delete/<id>')
def deleteSighting(id):
    Sighting.deleteSighting(id)
    return redirect("/")

@app.route("/skeptic/<id>")
def skeptic(id):
    data = {
        'user_id' : session['user_id'],
        'sighting_id' : id
    }
    newSkeptic = Skeptic.addSketpic(data)
    return redirect(f"/view/{id}")


@app.route("/believe/<id>")
def believe(id):
    data = {
        'user_id' : session['user_id'],
        'sighting_id' : id
    }
    Skeptic.believe(data)
    return redirect(f"/view/{id}")
