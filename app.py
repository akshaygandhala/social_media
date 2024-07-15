from flask import Flask, render_template 
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask_login import LoginManager
from bson.objectid import ObjectId
from models import User  # Import the User class

app = Flask(__name__)
from blueprints.auth.routes import auth_blueprint
from blueprints.discussion.routes import discussions_blueprint

uri = "mongodb+srv://traininglatrics2:eyBNCmy294K5Xipi@main.lab28gt.mongodb.net/?retryWrites=true&w=majority&appName=social"
app.config['SECRET_KEY'] = 'sadfghewrtyujikl' 
# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
app.register_blueprint(auth_blueprint, url_prefix='/user')
app.register_blueprint(discussions_blueprint, url_prefix='/discussions')

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.init_app(app)

# User loader
@login_manager.user_loader
def user_loader(user_id):
    return User.get(user_id, client)

@app.route('/')
def index():
    # Example: fetching some data from MongoDB 
    return render_template('base.html')

if __name__ == '__main__':
    app.run(debug=True)


 