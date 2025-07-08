from pymongo import MongoClient
import os
from datetime import datetime

class DurationUserModel:
    def __init__(self):
        mongo_url = os.getenv('MONGODB_URL', '##### ADD-YOUR-MONGODB-URL-HERE #####')
        try:
            self.client = MongoClient(mongo_url, serverSelectionTimeoutMS=5000)
            self.client.admin.command('ping')
            self.db = self.client['user_duration_tracker']
            self.collection = self.db['users']
            self.connected = True
        except Exception as e:
            print(f"MongoDB connection failed: {e}")
            self.connected = False
            self.client = None
            self.db = None
            self.collection = None
    
    def create_user(self, name, user_id, duration, end_time):
        """Create a new user entry"""
        if not self.connected:
            raise Exception("MongoDB not connected")
        
        user_data = {
            'name': name,
            'user_id': user_id,
            'duration': duration,
            'end_time': end_time,
            'created_at': datetime.now()
        }
        result = self.collection.insert_one(user_data)
        return str(result.inserted_id)
    
    def get_all_users(self):
        """Get all users"""
        if not self.connected:
            raise Exception("MongoDB not connected")
        
        users = list(self.collection.find({}, {'_id': 0}))
        return users
    
    def update_user(self, user_id, duration, end_time):
        """Update user duration and end time"""
        if not self.connected:
            raise Exception("MongoDB not connected")
        
        result = self.collection.update_one(
            {'user_id': user_id},
            {'$set': {'duration': duration, 'end_time': end_time}}
        )
        return result.modified_count > 0
    
    def delete_user(self, user_id):
        """Delete a user by user_id"""
        if not self.connected:
            raise Exception("MongoDB not connected")
        
        result = self.collection.delete_one({'user_id': user_id})
        return result.deleted_count > 0
    
    def close_connection(self):
        """Close MongoDB connection"""
        if self.client:
            self.client.close()

