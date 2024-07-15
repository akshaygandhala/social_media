from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId

# from .forms import LoginForm, RegisterForm
from  models import User
from blueprints.discussion.routes import discussions_blueprint

uri = "mongodb+srv://traininglatrics2:eyBNCmy294K5Xipi@main.lab28gt.mongodb.net/?retryWrites=true&w=majority&appName=social"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
auth_blueprint = Blueprint('auth', __name__) 

# @auth_blueprint.route('/login', methods=['GET', 'POST'])
# def login():
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.get_user(form.email.data)
#         if user and check_password_hash(user.password, form.password.data):
#             login_user(user)
#             return redirect(url_for('discussions.discussions'))
#         else:
#             flash('Login Unsuccessful. Please check email and password', 'danger')
#     return render_template('login.html', form=form)

# @auth_blueprint.route('/register', methods=['GET', 'POST'])
# def register():
#     form = RegisterForm()
#     if form.validate_on_submit():
#         hashed_password = generate_password_hash(form.password.data)
#         user = {
#             "name": form.name.data,
#             "contact": form.contact.data,
#             "email": form.email.data,
#             "password": hashed_password
#         }
#         mongo.db.users.insert_one(user)
#         flash('Your account has been created! You are now able to log in', 'success')
#         return redirect(url_for('auth.login'))
#     return render_template('register.html', form=form)

# @auth_blueprint.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('auth.login'))


@auth_blueprint.route('/login', methods=['GET', 'POST' ])
def login(): 

    if request.method == 'GET':
        return render_template('login.html' )
    
    if request.method == 'POST': 
        email = request.form.get('email')
        password = request.form.get('password')  
        res = client.db.users.find_one({"email": email})
        if res is None:
            return redirect(url_for('auth.register'))
        if check_password_hash(res.get('password'), password) is False:
            return redirect(url_for('auth.login')) 
    user_obj = User(res)
    login_user(user_obj)
    return redirect(url_for('discussion.discussions')) 

@auth_blueprint.route('/register', methods=['GET', 'POST' ])
def register():  

    if request.method == 'GET':
        return render_template('register.html' )
    
    if request.method == 'POST': 
        res = client.db.users.find_one({"email": request.form.get('email')})
        if res is not None:
            return redirect(url_for('auth.login'))
        hashed_password = generate_password_hash(request.form.get('password'))
        user = {
            "name": request.form.get('name'),
            "email": request.form.get('email'),
            "contact": request.form.get('contact'),
            "password": hashed_password
        } 
    if "users" not in client.db.list_collection_names():
        client.db.create_collection("users")    
    res = client.db.users.insert_one(user)
    user_obj = User(user)
    login_user(user_obj)
    return redirect(url_for('discussion.discussions'))

@auth_blueprint.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

