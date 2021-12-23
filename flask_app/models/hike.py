from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app.models import user
from flask_app.models import comment

class Hike:
    db = "hiking_schema"
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.city = data['city']
        self.state = data['state']
        self.difficulty = data['difficulty']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']

        self.with_user = []     # list of User instances
        self.with_comments = []     # list of Comment instances

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM hikes WHERE id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        hike = cls(results[0])
        return hike

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM hikes;"
        results = connectToMySQL(cls.db).query_db(query)
        hikes = []

        for hike in results:
            hikes.append(cls(hike))
        
        return hikes

    @classmethod
    def sort_by_filter(cls, data):
        query = "SELECT * FROM hikes WHERE state = %(state)s OR city = %(city)s OR difficulty = %(difficulty)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        filtered_hikes = []

        for hike in results:
            filtered_hikes.append(cls(hike))
        
        return filtered_hikes

    @classmethod
    def get_with_user(cls, data):
        query = "SELECT * FROM hikes JOIN users ON users.id = hikes.user_id WHERE hikes.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)

        hike = cls(results[0])

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

            hike.with_user.append(user.User(user_data))  # List of User objects associated with each hike post
        return hike     # Returns an object

    @classmethod
    def get_latest(cls):
        query = "SELECT * FROM hikes ORDER BY id DESC LIMIT 1;"
        results = connectToMySQL(cls.db).query_db(query)
        latest_hike = cls(results[0])
        return latest_hike

    # Display comments with the associated user
    @classmethod 
    def get_with_comments(cls, data):
        query = "SELECT * FROM hikes LEFT JOIN comments ON hikes.id = comments.hike_id WHERE hikes.id = %(id)s;"
        results = connectToMySQL(cls.db).query_db(query, data)
        print(results)

        # Initialize the process of creating a Comment object first so that we can start to add to its attribute
        hike = cls(results[0])
        
        # Go through each comment object and parse user data to create User objects
        # Append User objects as an attribute to the Comment object
        for row in results:
            if row["comments.id"] is None:
                hike.with_comments = []
            else: 
                comment_data = {
                    "id": row["comments.id"],
                    "message": row["message"],
                    "created_at": row["comments.created_at"],
                    "updated_at": row["comments.updated_at"],
                    "user_id": row["comments.user_id"],
                    "hike_id": row["hike_id"]
                }

                # Create User object using parsed data
                hike.with_comments.append(comment.Comment(comment_data))   # Creates a list of User objects associated with each comment; can now access as an attribute

        return hike  # Returns Comment object

    @classmethod
    def save(cls, data):
        query = "INSERT INTO hikes (name, description, city, state, difficulty, created_at, updated_at, user_id) VALUES (%(name)s, %(description)s, %(city)s, %(state)s, %(difficulty)s, NOW(), NOW(), %(user_id)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def update(cls, data):
        query = "UPDATE hikes SET name = %(name)s, description = %(description)s, city = %(city)s, state = %(state)s, difficulty = %(difficulty)s, updated_at = NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def delete(cls, data):
        query = "DELETE FROM hikes WHERE id = %(id)s;"
        return connectToMySQL(cls.db).query_db(query, data)

    # Validate user inputs on "Create a Hike" and "Edit a Hike" form
    @staticmethod
    def validate_hike(hike):
        is_valid = True
        if (len(hike["name"]) == 0) or (len(hike["name"]) < 3):
            flash("Name of hike is required and must be at least 3 characters long", "hiking")
            is_valid = False
        if (len(hike["description"]) == 0) or (len(hike["description"]) < 3):
            flash("Description is required and must be at least 3 characters long", "hiking")
            is_valid = False
        if (len(hike["city"]) == 0) or (len(hike["city"]) < 3): 
            flash("City is required and must be at least 3 characters long", "hiking")
            is_valid = False
        if len(hike["state"]) != 2:
            flash("State must be 2 characters", "hiking")
            is_valid = False
        if (len(hike["difficulty"]) == 0):
            flash("Difficulty level must be selected", "hiking")
            is_valid = False
        return is_valid
