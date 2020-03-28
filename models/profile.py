import datetime
from common.db import Database
import random
from flask import session

default_image_locations = {'male' : 'images/male-profile-image.png',
                               'female' : 'images/female-profile-image.png',
                               'no-gender' : 'images/no-gender-profile-image.jpg',
                                '' : 'images/no-gender-profile-image.jpg'}

class Profile():
    def __init__(self, full_name, email, password='123', phone_number=None ,date_of_birth=None, residence=None,
                 gender='male',pre_army=None, army_service=None, education=None, hobbies=None,
                 interes=None, hashtags=None, ready_to_asist=None, _id=None, image_location=None,
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
        self.army_service = army_service
        self.education = education
        self.hobbies = hobbies
        self.interes = interes
        self.hashtags = hashtags
        self.ready_to_asist = ready_to_asist
        self.image_location = default_image_locations[gender] if image_location in [None,'']  else image_location
        self.creation_date = creation_date

    def __repr__(self):
        return f"{self._id}-{self.full_name}"

    def json(self):
        return dict(
            _id = self._id,
            full_name = self.full_name,
            email = self.email,
            phone_number = self.phone_number,
            date_of_birth = self.date_of_birth,
            residence = self.residence,
            gender = self.gender,
            pre_army = self.pre_army,
            army_service = self.army_service,
            education = self.education,
            hobbies = self.hobbies,
            interes = self.interes,
            hashtags = self.hashtags,
            ready_to_asist = self.ready_to_asist,
            image_location = self.image_location,
            creation_date = self.creation_date.strftime("%m/%d/%Y, %H:%M:%S")
        )

    def save_to_database(self):
        Database.insert('profiles',self.__dict__)

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
    Database.initialize()
    print(Profile.from_mongo('asd708'))