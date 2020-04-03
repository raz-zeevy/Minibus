import pymongo
import os
import sys

is_prod = os.environ.get('IS_HEROKU', None)

if is_prod:
    MONGO_URI = os.environ.get('MONGO_URI', None)
elif not is_prod:
    sys.path.append('C:\\Users\\Raz_Z\\Projects\\Minibus-new')
    import env.config as config
    MONGO_URI = config.MONGO_URI

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
        request = Database.DATABASE[collection].insert_one(data)
        print(f"1 row was created : _id = {request}")
        return True

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

    @staticmethod
    def get_approved_phones():
        approved_phones = [row['phone_number'] for row in Database.find('approved_phones',{})]
        return approved_phones
    
    @staticmethod
    def delete_one(collection, query):
        request = Database.DATABASE[collection].delete_one(query)
        return request
    
    @staticmethod
    def insert_incremented(collection, data):
        data['_id'] = Database.find_one('sequences',{'_id' : collection})['next_sequence']
        request = Database.insert(collection, data)
        if request:
            Database.update_one('sequences',{'_id' : collection},{'next_sequence' : data['_id']+1})
            return True
        else:
            print('something might be wrong with the insert query')
            return False
    
if __name__ == '__main__':
    Database.initialize(MONGO_URI)
    data = {'phone_number' : '0544663407'}
    Database.insert_incremented('approved_phones',data)