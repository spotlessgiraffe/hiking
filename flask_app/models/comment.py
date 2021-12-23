from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user

class Comment:
    db = "hiking_schema"
    def __init__(self, data):
        self.id = data['id']
        self.message = data['message']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.hike_id = data['hike_id']

        # list to contain comment with associated user
        self.with_user = []

    @classmethod
    def save(cls, data):
        query = "INSERT INTO comments (message, created_at, updated_at, user_id, hike_id) VALUES (%(message)s, NOW(), NOW(), %(user_id)s, %(hike_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM comments;"
        results = connectToMySQL(cls.db).query_db(query)
        return results
    
    # Display comments with the associated user
    @classmethod 
    def get_with_user(cls, data):
        query = "SELECT * FROM comments JOIN users ON users.id = comments.user_id WHERE comments.hike_id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)

        # Initialize the process of creating a Comment object first so that we can start to add to its attribute
        comment = cls(results[0])
        
        # Go through each comment object and parse user data to create User objects
        # Append User objects as an attribute to the Comment object
        for row in results:
            user_data = {
                "id": row["users.id"],
                "first_name": row["first_name"],
                "last_name": row["last_name"],
                "email": row["email"],
                "password": row["password"],
                "confirm_password": row["confirm_password"],
                "experience": row["experience"],
                "about_me": row["about_me"],
                "created_at": row["users.created_at"],
                "updated_at": row["users.updated_at"]
            }

            # Create User object using parsed data
            comment.with_user.append(user.User(user_data))   # Creates a list of User objects associated with each comment; can now access as an attribute

        return comment  # Returns Comment object

    @classmethod
    def get_latest(cls):
        query = "SELECT * FROM comments ORDER BY id DESC LIMIT 1;"
        results = connectToMySQL(cls.db).query_db(query)
        latest_comment = cls(results[0])
        return latest_comment

    # Validate user input on Comments form
    @staticmethod
    def validate_comment(comment):
        is_valid = True
        if len(comment['message']) == 0:
            flash("Comment must contain at least 3 characters!", "comment")
            is_valid = False
        
        return is_valid