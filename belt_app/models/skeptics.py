from belt_app.config.mysqlconnection import connectToMySQL


class Skeptic:
    def __init__(self, data):
        self.user_id = data['user_id']
        self.sighting_id = data['sighting_id']
    
    @classmethod
    def addSketpic(cls, data):
        query = """
        INSERT INTO skeptic (user_id, sighting_id)
        VALUES (%(user_id)s, %(sighting_id)s)
        """
        results = connectToMySQL("belt_schema").query_db(query, data)
        if not results:
            return False
        return cls(results[0])

    @classmethod
    def findSkeptics(cls, id):
        query = f"""
        SELECT count(user_id) as skeptics
        FROM skeptic
        WHERE sighting_id = {id};
        """
        results = connectToMySQL("belt_schema").query_db(query)
        if not results:
            return False
        return results[0]
    
    @classmethod
    def skepticNames(cls, id):
        query = f"""
        select user_id, user.first_name, user.last_name
        from skeptic
        left join user
        on skeptic.user_id = user.id
        where sighting_id = {id}
        """
        results = connectToMySQL("belt_schema").query_db(query)
        if not results:
            return False
        return results

    @classmethod
    def believe(cls, data):
        query = """
        DELETE FROM skeptic
        WHERE user_id = %(user_id)s
        and sighting_id = %(sighting_id)s;
        """
        delete = connectToMySQL("belt_schema").query_db(query, data)
        if not delete:
            return False
        return delete