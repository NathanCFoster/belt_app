from belt_app.config.mysqlconnection import connectToMySQL
from flask import flash
from belt_app.models.skeptics import Skeptic

class Sighting:
    def __init__(self, data):
        self.id = data['id']
        self.location = data['location']
        self.what_happened = data['what_happened']
        self.reported_at = data['reported_at']
        self.reported_by = data['reported_by']
        self.name_reported = data['name_reported']
        self.num_of_sas = data['num_of_sas']
        self.skeptics = Skeptic.findSkeptics(data["id"])
        
    @classmethod
    def findAll(cls):
        query = "SELECT * FROM sighting;"
        results = connectToMySQL("belt_schema").query_db(query)
        sightings = []
        if not results:
            return False
        for row in results:
            sightings.append(cls(row))
        return sightings

    @classmethod
    def newSighting(cls, data):
        query = f"""
        INSERT INTO sighting (location, what_happened, reported_at, reported_by, name_reported, num_of_sas)
        VALUES ('{data['location']}', '{data['what_happened']}', '{data['reported_at']}', '{data['reported_by']}', '{data['name_reported']}', '{data['num_of_sas']}')
        """
        sighting = connectToMySQL("belt_schema").query_db(query, data)
        if not sighting:
            return False
        return sighting

    @classmethod
    def findSighting(cls, id):
        query = f"SELECT * FROM sighting WHERE id = {id};"
        newSighting = connectToMySQL("belt_schema").query_db(query)
        if not newSighting:
            return False
        return cls(newSighting[0])

    @classmethod
    def findTime(cls, id):
        query = f"SELECT reported_at FROM sighting WHERE id = {id};"
        dateMade = connectToMySQL("belt_schema").query_db(query)
        if dateMade[0]['reported_at'] == None:
            return False
        newDate = dateMade[0]['reported_at'].strftime("%B %d, %y")
        return newDate

    @classmethod
    def updateSighting(cls, data, id):
        query = f""" UPDATE sighting
        SET location = '{data['location']}', what_happened = '{data['what_happened']}', reported_at = '{data['reported_at']}', num_of_sas = '{data['num_of_sas']}'
        WHERE id = {id}
        """
        updateSighting = connectToMySQL("belt_schema").query_db(query)
        return updateSighting

    @classmethod
    def deleteSighting(cls, id):
        query = f"DELETE FROM sighting WHERE id = {id}"
        deleteRecipe = connectToMySQL('belt_schema').query_db(query)
        return deleteRecipe

    @classmethod
    def userSighting(cls, user_id):
        query = f"""
        SELECT * FROM sighting
        WHERE reported_by = {user_id}
        """
        results = connectToMySQL('belt_schema').query_db(query)
        if not results:
            return False
        userSightings = []
        for row in results:
            userSightings.append(cls(row))
        return userSightings