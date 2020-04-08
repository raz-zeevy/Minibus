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
        request = Database.DATABASE[collection].update_one(query,{ "$set" : new_values})
        print(f"'{list(new_values.keys())[0]}' of '{list(query.values())[0]}' --> {list(new_values.values())[0]}")
        return request 
    
    @staticmethod
    def update(collection, query, new_values):
        ids =  Database.DATABASE[collection].find(query,{'_id' : 1})
        for id in ids:
            id = id['_id']
            request = Database.update_one(collection, {'_id' : id}, new_values)
        print(f"{ids.count()} rows: '{list(new_values.keys())[0]}' --> {list(new_values.values())[0]}")

    @staticmethod
    def load_search_data():
        data =  Database.DATABASE['profiles'].find({},{'_id' : 1, 'full_name' : 1,
                                                      'image_location' : 1,
                                                      'date_of_birth' : 1,'residence':1,
                                                      'phone_number' : 1, 'hashtags':1})
        return [row for row in data]

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
    
    def search_text(collection, query, ids_only=True):
        res = Database.DATABASE[collection].find({ '$text' : { '$search' : query}})
        return set([item['_id'] for item in res])
    
if __name__ == '__main__':
    Database.initialize(MONGO_URI)
    Database.update('profiles',{'image_location' : 'https://minibus-photos.s3.us-east-2.amazonaws.com/images/female-profile-image.png'},
                                {'image_location' : 'https://minibus-photos.s3.us-east-2.amazonaws.com/female-profile-image.png'})
    # data = {'phone_number' : '0544663407'}
    # Database.insert_incremented('approved_phones',data)