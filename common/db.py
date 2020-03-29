import pymongo
import os

class Database(object):
    DATABASE = None

    @staticmethod
    def initialize(URI):
        Database.URI = URI
        client = pymongo.MongoClient(Database.URI)
        Database.DATABASE = client['minibus']

    @staticmethod
    def create_collection():
        Database.DATABASE.createCollection('profiles')

    @staticmethod
    def insert(collection, data):
        request = Database.DATABASE[collection].insert(data)
        if isinstance(request, str):
            print(f"1 row was created : _id = {request}")
        else:
            print(f"{len(request)} row was created : _id's = {request}")

    @staticmethod
    def find(collection, query):
        request =  Database.DATABASE[collection].find(query)
        return request

    @staticmethod
    def find_one(collection, query):
        request = Database.DATABASE[collection].find_one(query)
        return request

    @staticmethod
    def update_one(collection, query, new_values):
        Database.DATABASE[collection].update_one(query,{ "$set" : new_values})
        print(f"'{list(new_values.keys())[0]}' of '{list(query.values())[0]}' --> {list(new_values.values())[0]}")

    @staticmethod
    def update(collection, query, new_values):
        ids =  Database.DATABASE[collection].find(query,{'_id' : 1})
        for id in ids:
            Database.update_one(collection, {'_id' : id}, new_values)
        print(f"{ids.count()} rows: '{list(new_values.keys())[0]}' --> {list(new_values.values())[0]}")

    @staticmethod
    def get_all_profiles():
        profiles_data = [row for row in Database.find('profiles',{})]
        return profiles_data

if __name__ == '__main__':
    pass