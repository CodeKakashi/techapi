import json
from flask_restful import Resource
from pymongo.errors import BulkWriteError
from app.config import G_DATA_STATIC_PATH
from app.db import mongo

mdb = mongo.db



collectionsTobeGenerated = [
    'district',
    "aboutus"
]

class GenerateStatic(Resource):
    def get(self):
        updatedCollections = []
        duplicates = {}

        for c in collectionsTobeGenerated:
            try:
                print('--------->', f'{G_DATA_STATIC_PATH}/{c}.json')
                with open(f'{G_DATA_STATIC_PATH}/{c}.json', 'r') as file:
                    staticList = json.load(file)

                    # Clear existing documents in the collection
                    mdb[c].delete_many({})

                    # Insert new documents
                    mdb[c].insert_many(staticList)
                
                updatedCollections.append(c)

            except BulkWriteError as bwe:
                # Handle duplicate key errors
                for error in bwe.details['writeErrors']:
                    duplicates.setdefault(c, []).append(error['op']['_id'])

                continue
        
        return {
            'status': 1,
            'updatedCollections': updatedCollections,
            'duplicates': duplicates,
        }

