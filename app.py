__author__ = 'Raz_Zeevy'

from flask import Flask, render_template, redirect
from flask import session, request, url_for
from models.profile import Profile
from common.db import Database
from common.s3 import AWS
import secrets, os, datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)

is_prod = os.environ.get('IS_HEROKU', None)

if is_prod:
    MONGO_URI = os.environ.get('MONGO_URI', None)
    app.secret_key = os.environ.get('SECRET_KEY', None)
elif not is_prod:
    import env.config as config
    app.secret_key = secrets.token_hex()
    MONGO_URI = config.MONGO_URI

UPLOAD_FOLDER = '/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def parse_form(form_data):
    user_data = form_data
    for key in user_data:
        try:
            if isinstance(user_data[key],list):
                if len(user_data[key]) < 2:
                    user_data[key] = user_data[key][0].strip()
                else:
                    to_keep = False
                    for i, item in enumerate(user_data[key]):
                        if len(item) > 0:
                            user_data[key] = user_data[key][i].strip()
                            to_keep = True
                    if not to_keep:
                        user_data[key] = None
        except:
            pass
    return user_data

def if_logged_in(f):
    def wrap(*args, **kwargs):
        if session.get('email') is not None:
            return f(*args, **kwargs)
        else:
            return redirect(url_for('login'))
    wrap.__name__ = f.__name__
    return wrap

@app.before_first_request
def initialize_database():
    try:
        Database.initialize(MONGO_URI)
    except Exception as e:
        print(e)
        return "FAILED TO CONNECT"

@app.route('/', methods=['POST','GET'])
@if_logged_in
def index():
    return redirect(url_for('search'))

@app.route('/login', methods=['GET','POST'])
def login():
    if session.get('email') is None:
        message = None
        if request.method == 'POST':
            email = request.form.get('email').lower()
            password = request.form.get('password')
            if Profile.login_valid(email, password):
                Profile.login(email)
                return redirect('search')
            else:
                message = dict(
                    type ='Failure',
                    content =  'פרטי התחברות לא תקינים, נסה שוב'
                )
                return render_template('login.html', message=message)
        return render_template('login.html', message=message)
    else:
        return index()

@app.route('/register')
def register():
    af = Database.get_approved_phones()
    return render_template('register.html', approved_phones=af)

@app.route('/register/submit', methods=['POST'])
def register_submit():
    if request.method == 'POST':
        user_data = request.form.to_dict(flat=False)
        user_data = parse_form(user_data)
        while 'image' in request.files:
            file = request.files['image']
            if file.filename == '':
                break
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                # Here should be the Amazon Savings
                AWS.initialize()    
                image_location = AWS.upload(file_name=filename, file=file.read())
                user_data['image_location'] = image_location
                break 
        if Profile.register(user_data):
           return redirect(url_for('search'))
    return 'Error in Registerarion Form'

@app.route('/search', methods=['GET'])
@if_logged_in
def search(message = None):
    profiles = [Profile(**profile) for profile in Database.get_all_profiles()]
    matched_profiles = []
    search_query = request.args.get('search_query')
    if search_query is not None:
        if is_prod:
            search_data = dict(time=datetime.datetime.now(),user=session['email'],string=search_query)
            Database.insert('searches',search_data)
        for profile in profiles:
            user_string = ''
            for value in profile.json().values():
                if isinstance(value,list):
                    user_string+=','.join(value)
                elif isinstance(value,(str,int,float)):
                    user_string+=str(value)
                else:
                    print("I won't try to search",value)
            if search_query in user_string:
                matched_profiles.append(profile)
    search_results = [profile.json() for profile in matched_profiles]
    return render_template('search.html', title="search", users=search_results, message=message)

@app.route('/about')
@if_logged_in
def about():
    return render_template('about.html', title='about')

@app.route('/my-profile')
@if_logged_in
def my_profile(message=None):
    profile = Profile.from_email(session['email'])
    return render_template('my-profile.html', profile=profile, title="my-profile", message=message)

@app.route('/my-profile/update', methods=['POST'])
@if_logged_in
def update_profile():
    if request.method == 'POST':
        message = dict(
                type ='Success',
                content =  'פרטי הפרופיל עודכנו')
        user_data = request.form.to_dict(flat=False)
        user_data = parse_form(user_data)
        Profile.update(user_data, session['email'])
    return my_profile(message)
 
@app.route('/my-profile/delete', methods=['POST'])
@if_logged_in
def delete_profile():
    if request.method == 'POST':
        user_email = session['email']
        former_image = Profile.data_from_email(session['email'])['image_location']
        AWS.initialize()  
        AWS.delete(file_name=former_image)
        Database.delete_one('profiles',{'email' : user_email})
    return logout()

@app.route('/my-profile/update-image', methods=['POST'])
@if_logged_in
def update_image():
    message = None
    if request.method == 'POST':
        former_image = Profile.data_from_email(session['email'])['image_location']
        file_index = former_image.rfind('/')
        former_image = former_image[file_index+1:]
        message = dict(
            type ='Warning',
            content =  'לא נבחרה אף תמונה')
        while 'image' in request.files:
            file = request.files['image']
            if file.filename == '':
                break
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                AWS.initialize()  
                print(former_image)
                AWS.delete(file_key=former_image)
                new_image_location = AWS.upload(file_name=filename, file=file.read())
                Profile.update(email=session['email'], user_data={'image_location' : new_image_location})
                message = dict(
                   type ='Success',
                    content =  'התמונה עודכנה בהצלחה')
                break
    return my_profile(message)

@app.route('/user-profile/', methods=["GET"])
@if_logged_in
def user_profile():
    if request.method == 'GET':
        user_id = request.args.get('user_id')
        profile = Profile.from_id(user_id)
    return render_template('user-profile.html', profile=profile.json())

@app.route('/logout/')
@if_logged_in
def logout():
    Profile.logout()
    return redirect(url_for('login'))

if __name__ == '__main__':
    if is_prod:
        pass
    else:
        app.run(debug=True)
