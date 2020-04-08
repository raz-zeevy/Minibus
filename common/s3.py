import os
import boto3
from botocore.client import Config
import uuid
import os.path
from PIL import Image
import io

class AWS(object):
    bucket = 'minibus-photos'
    s3 = None
    
    @classmethod
    def initialize(cls):
        if os.environ.get('IS_HEROKU',False):
            AWS_ID = os.environ.get('AWS_ID')
            AWS_KEY = os.environ.get('AWS_KEY')
            region = os.environ.get('AWS_REGION')
        else:
            from env.config import AWS_ID, AWS_KEY, AWS_REGION            
        s3 = boto3.resource('s3', aws_access_key_id=AWS_ID, aws_secret_access_key=AWS_KEY, region_name=AWS_REGION)
        cls.s3 = s3.Bucket(cls.bucket)
        
    @staticmethod
    def upload(file, file_name):
        image = Image.open(file)
        image = image.resize((800,960),Image.ANTIALIAS)
        extension = os.path.splitext(file_name)[1]
        file_key = uuid.uuid4().hex+".jpeg"
        out_image = io.BytesIO()
        image.save(out_image, format="JPEG")
        out_image.seek(0) 
        AWS.s3.put_object(Key=file_key, Body=out_image, ACL='public-read')
        return f'https://minibus-photos.s3.us-east-2.amazonaws.com/{file_key}'
    
    @staticmethod
    def get(file_key):
        obj = AWS.s3.Object(key=file_key)
        response = obj.get()
        return response
    
    @staticmethod
    def delete(file_key):
        obj = AWS.s3.Object(key=file_key)
        return obj.delete()
    
if __name__ == '__main__':
    AWS.initialize()
    image = open(r"C:\Users\Raz_Z\Projects\Minibus-new\common\image.jpeg", 'rb')
    AWS.upload(image, 'image2.jpg')
    # with open(r"C:\Users\Raz_Z\Projects\Minibus-new\common\test.png", 'rb') as image:
    #     file = image
    #     AWS.upload(file,'test4.png')
    # AWS.delete('test3.png')  
        
      
    
