from flask import flash, session
from flask_app.models import user
import os
from flask_app.config.mysqlconnection import connectToMySQL

class Wandering:
    db = 'wandershare'
    def __init__(self, data):
        self.id = data['id']
        self.location = data['location']
        self.start_date = data['start_date']
        self.end_date = data['end_date']
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
        query = """
        INSERT INTO wanderings (location, start_date, end_date, rating, details, image, user_id)
        VALUES (%(location)s, %(start_date)s, %(end_date)s, %(rating)s, %(details)s, %(image)s, %(user_id)s)
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

#UPDATE
    @classmethod
    def edit_wandering(cls, data):
        if not Wandering.validate_wandering(data, "edit"):
            return False
        one_wandering = Wandering.get_wandering_by_id(data['id'])
        if one_wandering.image != data['image']:
            os.remove(f'/Users/heathermehr/projects_algos/core_assignments/Wandershare/wandershare_code_files/flask_app/{one_wandering.image}')
        query = """
        UPDATE wanderings
        SET location = %(location)s,
        start_date = %(start_date)s,
        end_date = %(end_date)s,
        rating = %(rating)s,
        details = %(details)s,
        image = %(image)s
        WHERE id = %(id)s
        ;"""
        connectToMySQL(cls.db).query_db(query, data)
        return True

#DELETE
    @classmethod
    def delete_wandering_by_id(cls, id):
        one_wandering = Wandering.get_wandering_by_id(id)
        if one_wandering.user_id != session['user_id']:
            return False
        data = {'id' : id}
        query = """
        DELETE FROM wanderings
        WHERE id = %(id)s
        ;"""
        connectToMySQL(cls.db).query_db(query, data)
        os.remove(f'/Users/heathermehr/projects_algos/core_assignments/Wandershare/wandershare_code_files/flask_app/{one_wandering.image}')
        return True

#VALIDATE
    @staticmethod
    def validate_wandering(form, file):
        print(form)
        print(file)
        is_valid = True
        if len(form['location']) < 2:
            flash('Wandering location should be at least two characters long.')
            is_valid = False
        if len(form['start_date']) < 10:
            flash('Please enter a start date.')
            is_valid = False
        if form['end_date'] == "":
            flash('Please enter an end date.')
            is_valid = False
        if not form.get('rating'):
            flash('Please enter a rating.')
            is_valid = False
        if len(form['details']) < 20:
            flash('Please write a more detailed description of your trip.')
            is_valid = False
        print(form)
        return is_valid