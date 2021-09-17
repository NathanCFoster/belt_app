from belt_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash

email_regex = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
password_regex = re.compile(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[A-Za-z\d]{8,}$")

class User:
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at'] 
        self.updated_at = data['updated_at']
        self.sightings = []


    @staticmethod
    def validateUser(form):
        isValid = True
        if len(form['first_name']) < 2:
            flash('First Name must be 2 characters', 'register')
            isValid = False
        if len(form['last_name']) <2:
            flash('Last Name must be 2 characters long', 'register')
            isValid = False
        if not password_regex.match(form["password"]):
            flash('Password must be 8 characters, have one uppercase letter, one lowercase letter, and one number', 'register')
            isValid = False
        if not email_regex.match(form['email']):
            flash('Must be a valid email', 'register')
            isValid = False
        if form['password'] != form['confirmedPass']: 
            flash("Password must be the same", 'register')
        return isValid


    @classmethod
    def newUser(cls, data):
        query ="INSERT INTO user (first_name, last_name, email, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s)"
        newUser = connectToMySQL("belt_schema").query_db(query, data)
        return newUser
    
    @classmethod
    def showUsers(cls):
        query = "SELECT * FROM user"
        allUsers = connectToMySQL("belt_schema").query_db(query)
        users = []
        for row in allUsers:
            users.append(cls(row))
        
        return users

    @classmethod
    def findUser(cls, data):
        query = "SELECT * FROM user WHERE email = %(email)s;"
        user = connectToMySQL("belt_schema").query_db(query, data)
        if not user:
            return False
        return cls(user[0])
    
    @classmethod
    def currentUser(cls, id):
        query = "SELECT * FROM user WHERE id = %s" %(id) 
        currentUser = connectToMySQL("belt_schema").query_db(query)
        if not currentUser:
            return False
        return cls(currentUser[0])
