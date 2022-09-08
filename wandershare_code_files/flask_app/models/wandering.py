from flask import flash
from flask_app.models import user
from flask_app.config.mysqlconnection import connectToMySQL

class Wandering:
    db = 'wandershare'
    def __init__(self, data):
        self.id = data['id']
        self.location = data['location']
        self.duration = data['duration']
        self.rating = data['rating']
        self.details = data['details']
        self.image = data['image']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None
    
#CREATE
    @classmethod
    def create_wandering(cls, data):
        if not cls.validate_wandering(data):
            return False
        query = """
        INSERT INTO wanderings (location, duration, rating, details, image, user_id)
        VALUES (%(location)s, %(duration)s, %(rating)s, %(details)s, %(image)s, %(user_id)s)
        ;"""
        return connectToMySQL(cls.db).query_db(query, data)

#READ
    @classmethod
    def get_all_wanderings(cls):
        query = """
        SELECT *
        FROM wanderings
        JOIN users
        ON users.id = wanderings.user_id
        ;"""
        result = connectToMySQL(cls.db).query_db(query)
        all_wanderings = []
        for row in result:
            this_wandering = cls(row)
            user_data = {
                'id' : row['users.id'],
                'first_name' : row['first_name'],
                'last_name' : row['last_name'],
                'username' : row['username'],
                'email' : row['email'],
                'password' : row['password'],
                'created_at' : row['users.created_at'],
                'updated_at' : row['users.updated_at']
            }
            all_users = user.User(user_data) 
            this_wandering.user = all_users
            all_wanderings.append(this_wandering)
        return all_wanderings
    
    @classmethod
    def get_wandering_with_user_by_id(cls, id):
        data = {'id' : id}
        query = """
        SELECT *
        FROM wanderings
        LEFT JOIN users
        ON users.id = wanderings.user_id
        WHERE wanderings.id = %(id)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            this_wandering = cls(result[0])
            user_data = {
                'id' : result[0]['users.id'],
                'first_name' : result[0]['first_name'],
                'last_name' : result[0]['last_name'],
                'username' : result[0]['username'],
                'email' : result[0]['email'],
                'password' : result[0]['password'],
                'created_at' : result[0]['users.created_at'],
                'updated_at' : result[0]['users.updated_at']
            }
            this_wandering.user = user.User(user_data)
            return this_wandering
        return False

    @classmethod
    def get_wandering_by_id(cls, id):
        data = {'id' : id}
        query = """
        SELECT *
        FROM wanderings
        WHERE id = %(id)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            result = cls(result[0])
        return result

    # @classmethod
    # def get_avg_rating_by_id(cls, id):
    #     query = """
    #     SELECT ROUND(AVG('rating'), 2)
    #     AS 'avg' 
    #     COUNT('user_id')
    #     AS 'num'
    #     FROM wanderings
    #     WHERE id = %(id)s
    #     ;"""

#UPDATE


#DELETE
