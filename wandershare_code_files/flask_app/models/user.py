import re
from flask_app import app
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
from flask import flash, session
from flask_app.config.mysqlconnection import connectToMySQL

class User:
    db = 'wandershare'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.wanderings = []

# CREATE
    @classmethod
    def create_user(cls, data):
        if not User.validate_user(data):
            return False
        data = cls.parse_registration_data(data)
        query = """
        INSERT INTO users (first_name, last_name, email, password, created_at, updated_at)
        VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW())
        ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        session['user_id'] = result
        return True

# READ
    @classmethod
    def get_user_by_username(cls, username):
        data = {'username' : username}
        query = """
        SELECT *
        FROM users
        WHERE username = %(username)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            result = cls(result[0])
        return result

    @classmethod
    def get_user_by_email(cls, email):
        data = {'email' : email}
        query = """
        SELECT *
        FROM users
        WHERE email = %(email)s
        ;"""
        result = connectToMySQL(cls.db).query_db(query, data)
        if result:
            result = cls(result[0])
        return result



# UPDATE


# DELETE


# VALIDATION
    @staticmethod
    def validate_user(data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        is_valid = True
        if len(data['first_name']) < 2:
            flash('First name must be at least 2 characters.')
            is_valid = False
        if len(data['last_name']) < 2:
            flash('Last name must be at least 2 characters.')
            is_valid = False
        if len(data['username']) < 8:
            flash('Username must be at least 8 characters.')
            is_valid = False
        if User.get_user_by_username(data['username']):
            flash('This username is already in use.')
            is_valid = False
        if not EMAIL_REGEX.match(data['email']):
            flash('Please use a valid email address.')
            is_valid = False
        if User.get_user_by_email(data['email']): 
            flash('User with this email already exists.')
            is_valid = False
        if len(data['password']) < 8:
            flash('Password must be at least 8 characters long.')
            is_valid = False
        if data['password'] != data['confirm_password']:
            flash('Passwords do not match.')
            is_valid = False
        return is_valid

    @staticmethod
    def parse_registration_data(data):
        parsed_data = {}
        parsed_data['first_name'] = data['first_name']
        parsed_data['last_name'] = data['last_name']
        parsed_data['email'] = data['email'].lower()
        parsed_data['password'] = bcrypt.generate_password_hash(data['password'])
        return parsed_data

# LOGIN
    @staticmethod
    def validate_login(data):
        this_user = User.get_user_by_email(data['email'])
        if this_user:
            if bcrypt.check_password_hash(this_user.password, data['password']):
                session['user_id'] = this_user.id
                return True
            flash('Your login failed!')
            return False
        flash('Your login failed!')
        return False

