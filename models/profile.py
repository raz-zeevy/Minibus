import datetime
import sys, os
from common.db import Database
import random
from flask import session

is_prod = os.environ.get('IS_HEROKU', None)

if is_prod:
    MONGO_URI = os.environ.get('MONGO_URI', None)
elif not is_prod:
    sys.path.append('C:\\Users\\Raz_Z\\Projects\\Minibus-new')
    import env.config as config
    MONGO_URI = config.MONGO_URI

default_image_locations = {'male' : 'images/male-profile-image.png',
                               'female' : 'images/female-profile-image.png',
                               'no-gender' : 'images/no-gender-profile-image.jpg',
                                '' : 'images/no-gender-profile-image.jpg'}

class Profile():
    def __init__(self, full_name, email, password='123',
                 phone_number=None ,date_of_birth=None, residence=None,
                 gender='male',
                 pre_army=None, inst_army=None, army=None, more_frames = None,
                 inst_education=None, education=None, inst_job=None, job=None,
                 education_work_more=None,
                 hobbies=None,
                 interes=None, hashtags=None, ready_to_asist=None, ways_to_asist=None,
                  _id=None, image_location=None,
                 creation_date = datetime.datetime.now()):
        self._id = full_name + str(random.randint(100,999)) if _id is None else _id
        self.full_name = str(full_name)
        self.email = email.lower()
        self.password = str(password)
        self.phone_number = str(phone_number)
        self.date_of_birth = date_of_birth
        self.residence = residence
        self.gender = gender
        self.pre_army = pre_army
        self.inst_army = inst_army
        self.army = army
        self.more_frames = more_frames
        self.inst_education = inst_education
        self.education = education
        self.inst_job = inst_job
        self.job = job
        self.education_work_more = education_work_more
        self.hobbies = hobbies
        self.interes = interes
        self.hashtags = hashtags
        self.ready_to_asist = ready_to_asist
        self.ways_to_asist = ways_to_asist
        self.image_location = default_image_locations[gender] if image_location in [None,'']  else image_location
        self.creation_date = creation_date

    def __repr__(self):
        return f"{self._id}-{self.full_name}"

    def json(self):
        json = self.__dict__.copy() 
        del json['password']
        json['creation_date'] = self.creation_date.strftime("%m/%d/%Y, %H:%M:%S")
        return json
        # return dict(
        #     _id = self._id,
        #     full_name = self.full_name,
        #     email = self.email,
        #     phone_number = self.phone_number,
        #     date_of_birth = self.date_of_birth,
        #     residence = self.residence,
        #     gender = self.gender,
        #     pre_army = self.pre_army,
        #     army_service = self.army_service,
        #     education = self.education,
        #     hobbies = self.hobbies,
        #     interes = self.interes,
        #     hashtags = self.hashtags,
        #     ready_to_asist = self.ready_to_asist,
        #     image_location = self.image_location,
        #     creation_date = self.creation_date.strftime("%m/%d/%Y, %H:%M:%S")
        # )

    def save_to_database(self):
        Database.insert('profiles',self.__dict__)
            
    @staticmethod
    def update(user_data, email):
        Database.update_one('profiles',{'email' : email}, user_data) 
    
    @classmethod
    def from_id(cls, id):
        data = Database.find_one('profiles',{'_id' : id})
        if data is not None:
            return cls(**data)

    @classmethod
    def from_email(cls, email):
        data = Database.find_one('profiles',{'email' : email})
        if data is not None:
            return cls(**data)

    @classmethod
    def register(cls, user_data):
        email = user_data['email']
        profile = cls.from_email(email)
        if profile is None:
            new_profile = cls(**user_data)
            new_profile.save_to_database()
            new_profile.login(email)
            return True
        else:
            return False

    @classmethod
    def login_valid(cls,email, password):
        user_data = Database.find_one('profiles',{'email' : email})
        if user_data is not None:
            if str(user_data['password']) == str(password):
                cls.login(user_data['email'])
                print("LOGIN VALID")
                return True
        print("NOT VALID",email, password)
        return False

    @staticmethod
    def login(email):
        session['email'] = email
        print(f"{session['email']} LOGED IN")
        return True

    @staticmethod
    def logout():
        session['email'] = None

if __name__ == '__main__':
    Database.initialize(MONGO_URI)
    a = Database.get_all_profiles()
    b = a[0]
    user = Profile(**b)
    print(user.json())
