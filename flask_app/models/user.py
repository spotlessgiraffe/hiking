from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models.hike import Hike
import re   # the regex module

# Create a regular expression object that we'll use later
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    db = "hiking_schema"
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.confirm_password = data['confirm_password']
        self.experience = data['experience']
        self.about_me = data['about_me']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        self.with_faves = []

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users;"
        results = connectToMySQL(cls.db).query_db(query)
        users = []

        for user in results:
            users.append(cls(user))
        
        return users

    @classmethod
    def get_by_id(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        user = cls(results[0])
        return user

    @classmethod
    def get_by_email(cls, data):
        query = "SELECT * FROM users WHERE email = %(email)s;"  # See if we can find a user with a matching email
        results = connectToMySQL(cls.db).query_db(query, data)

        # if there are no returned results, return false
        if len(results) < 1:
            return False
        # otherwise, return the results as an object; there should only be one entry in results if we found a match
        return cls(results[0])

    @classmethod
    def get_user_faves(cls, data):
        query = "SELECT * FROM users LEFT JOIN favorites ON users.id = favorites.user_id LEFT JOIN hikes ON hikes.id = favorites.hike_id WHERE users.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        user = cls(results[0])

        for row in results:
            if row["hikes.id"] is None:
                user.with_faves = []
            else: 
                hike_data = {
                    "id": row["hikes.id"],
                    "name": row["name"],
                    "description": row["description"],
                    "city": row["city"],
                    "state": row["state"],
                    "difficulty": row["difficulty"],
                    "created_at": row["hikes.created_at"],
                    "updated_at": row["hikes.updated_at"],
                    "user_id": row["hikes.user_id"]
                }

                user.with_faves.append(Hike(hike_data))
        
        return user

        """
        query = "SELECT * FROM users LEFT JOIN favorites ON users.id = favorites.user_id LEFT JOIN hikes ON hikes.id = favorites.hike_id WHERE users.id = %(id)s ORDER BY hikes.id DESC LIMIT 1;"
        results = connectToMySQL(cls.db).query_db(query, data)

        for row in results: 
            hike_data = {
                "name": name,
                "description": description,
                "city": city,
                "state": state,
                "difficulty": difficulty,
                "created_at": hikes.created_at,
                "updated_at": hikes.updated_at,
                "user_id": hikes.user_id
            }
            latest_fave = Hike(hike_data)
            
        return latest_fave
        """
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(password)s, NOW(), NOW());"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update_with_pw(cls, data):
        query = "UPDATE users SET about_me = %(about_me)s, experience = %(experience)s, password = %(password)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update_without_pw(cls, data):
        query = "UPDATE users SET about_me = %(about_me)s, experience = %(experience)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    # -- Validate user inputs on registration form --
    @staticmethod
    def validate_reg(user):
        users_db = User.get_all()    # Retrieve all the users from the database so that we can look if the entered email already exists
        is_valid = True
        # Validate first_name for letters only, at least 2 characters, and that it was submitted
        if not ((user['first_name'].isalpha()) and (len(user['first_name']) >= 2)):
            flash("'First Name' field is required and must be at least 2 alphabetic characters!", "register")
            is_valid = False
        # Validate last_name for letters only, at least 2 characters, and that it was submitted
        if not ((user['last_name'].isalpha()) and (len(user['last_name']) >= 2)):
            flash("'Last Name' field is required and must be at least 2 alphabetic characters!", "register")
            is_valid = False
        # Validate email matches regex format/pattern and that it was submitted
        if not EMAIL_REGEX.match(user['email']):
            flash("Invalid email address!", "register")
            is_valid = False
        # Validate entered email does not already exist in the database
        for user_db in users_db:
            if user['email'] == user_db.email:
                flash("Email already exists!", "register")
                is_valid = False
        # Validate entered password is at least 8 characters and that it was submitted
        # Bonus: Add an additional validation on passwords to have at least 1 number and 1 uppercase letter
        if not (any(x.isnumeric() for x in user['password']) and any(x.isupper() for x in user['password']) and (len(user['password']) >= 8)):
            flash("'Password' field is required. Password must have at least 1 number, 1 uppercase letter, and must be at least 8 characters!", "register")
            is_valid = False
        # Validate "Confirm Password" field matches "Password" field
        if user['confirm_password'] != user['password']:
            flash("Passwords don't match!", "register")
            is_valid = False
        return is_valid

    # -- Validate user inputs for "Edit Profile" form --
    @staticmethod
    def validate_profile(user):
        is_valid = True
        if user['about_me'] == "None":
            flash("'About Me' field is required!", "profile")
            is_valid = False
        if user['experience'] == "None":
            flash("'Experience' field is required!", "profile")
            is_valid = False
        if user['password'] != "":
            if not (any(x.isnumeric() for x in user['password']) and any(x.isupper() for x in user['password']) and (len(user['password']) >= 8)):
                flash("Password must have at least 1 number, 1 uppercase letter, and must be at least 8 characters!", "profile")
                is_valid = False
            
            if user['confirm_password'] != user['password']:
                flash("Passwords don't match!", "profile")
                is_valid = False
                
        return is_valid


"""
Sources:
1. https://stackoverflow.com/questions/17140408/if-statement-to-check-whether-a-string-has-a-capital-letter-a-lower-case-letter/17140466 [How to check if any letter is uppercase using any() and a "for" loop]
"""