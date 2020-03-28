__author__ = 'Raz_Zeevy'

from flask import Flask, render_template, redirect, flash
from flask import session, request, url_for
from models.profile import Profile
from common.db import Database
import secrets, os

app = Flask(__name__)
app.secret_key = secrets.token_hex()

is_prod = os.environ.get('IS_HEROKU', None)

if is_prod:
    MONGO_URI = os.environ.get('MONGO_URI', None)
else:
    import env.config as config
    MONGO_URI = config.MONGO_URI

def if_logged_in(f):
    def wrap(*args, **kwargs):
        if session.get('email') is not None:
            return f(*args, **kwargs)
        else:
            flash('You need to login first')
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
    error = None
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        if Profile.login_valid(email, password):
            Profile.login(email)
            return redirect('search')
        else:
            error = 'Invalid credentials. Try again'
            return render_template('login.html', error=error)

    return render_template('login.html', error=error)

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/register/submit', methods=['POST'])
def register_submit():
    if request.method == 'POST':
        user_data = request.form.to_dict()
        if Profile.register(user_data):
           return redirect(url_for('search'))
    return 'Error in Registerarion Form'

@app.route('/search', methods=['GET'])
@if_logged_in
def search():
    profiles = [Profile(**profile) for profile in Database.get_all_profiles()]
    matched_profiles = []
    search_query = request.args.get('search_query')
    print(search_query)
    if search_query is not None:
        for profile in profiles:
            user_string = ''
            for value in profile.json().values():
                try:
                    user_string+=str(value)
                except:
                    pass
            if search_query in user_string:
                matched_profiles.append(profile)

    search_results = [profile.json() for profile in matched_profiles]
    return render_template('search.html', title="search", users=search_results)

@app.route('/about')
@if_logged_in
def about():
    return render_template('about.html')

@app.route('/my-profile')
@if_logged_in
def my_profile():
    profile = Profile.from_email(session['email'])
    return render_template('my-profile.html', profile=profile, title="my-profile")

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
