import pymongo
from app.config import MONGO_URI, MONGO_DATABASE

class MongoDB:
    def __init__(self, uri, db_name=None):
        self.uri = uri
        self.db_name = db_name
        self.client = None
        self.db = None
        self.connect()

    def connect(self):
        self.client = pymongo.MongoClient(self.uri)
        if self.db_name:
            self.db = self.client[self.db_name]

    def set_database(self, db_name):
        self.db_name = db_name
        self.connect()

    def __getattr__(self, name):
        if self.db:
            return getattr(self.db, name)
        else:
            raise ValueError("No database selected. Use set_database() to select a database.")

    def close_connection(self):
        if self.client:
            self.client.close()

# Example usage:
mongo = MongoDB(MONGO_URI)
mongo.set_database(MONGO_DATABASE)