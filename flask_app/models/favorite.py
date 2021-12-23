from flask_app.config.mysqlconnection import connectToMySQL

class Favorite:
    db = "hiking_schema"
    def __init__(self, data):
        self.id = data['id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.hike_id = data['hike_id']
    
    @classmethod
    def add_to_favorite(cls, data):
        query = "INSERT INTO favorites (user_id, hike_id, created_at, updated_at) VALUES (%(user_id)s, %(hike_id)s, NOW(), NOW());"
        return connectToMySQL(cls.db).query_db(query, data)