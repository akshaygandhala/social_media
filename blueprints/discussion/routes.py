from flask import Blueprint, render_template, request, redirect, url_for
from flask_login import login_required
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from bson.objectid import ObjectId
from flask_login import login_required, current_user

discussions_blueprint = Blueprint('discussion', __name__)
# Create a new client and connect to the server
uri = "mongodb+srv://traininglatrics2:eyBNCmy294K5Xipi@main.lab28gt.mongodb.net/?retryWrites=true&w=majority&appName=social"
client = MongoClient(uri, server_api=ServerApi('1'))
auth_blueprint = Blueprint('auth', __name__) 


@discussions_blueprint.route('/discussions') 
@login_required
def discussions():
    res = client.db.discussions.find({})
    data = list(res)
    for post in data:
        post['_id'] = str(post['_id'])
    print(data)
    return render_template('discussions.html', data=data)

@discussions_blueprint.route('/users') 
@login_required
def users():
    res = client.db.users.find({})
    data = list(res)
    for post in data:
        post['_id'] = str(post['_id'])
    print(data)
    return render_template('users.html', data=data)

@discussions_blueprint.route('/posts') 
@login_required
def posts():
    res = client.db.discussions.find({"user": ObjectId(current_user.id)})
    data = list(res)
    for post in data:
        post['_id'] = str(post['_id'])
    print(data)
    return render_template('user_posts.html', data=data)

@discussions_blueprint.route('/create', methods=['GET', 'POST' ]) 
@login_required
def create(): 

    if request.method == 'GET':
        return render_template('create_post.html')
    
    if request.method == 'POST':   
        post = {
            "user": ObjectId(current_user.id),
            "title": request.form.get('title'),
            "discuss": request.form.get('discuss'),
            "image": request.form.get('url'),
            "tag": request.form.get('tag').split(', '),
        } 
    if "discussions" not in client.db.list_collection_names():
        client.db.create_collection("discussions")    
    res = client.db.discussions.insert_one(post) 
    print(res)
    return redirect(url_for('discussion.discussions'))

@discussions_blueprint.route('/submit_edit', methods=['POST']) 
@login_required
def submit_edit():  
    if request.method == 'POST':   
        post_id = request.form.get('postId')
        post = { 
            "title": request.form.get('title'),
            "discuss": request.form.get('discuss'),
            "image": request.form.get('url'),
            "tag": request.form.get('tag').split(', '),
        }    
    res = client.db.discussions.update_one(
            {"_id": ObjectId(post_id)},
            {"$set": post}
        )  
    print(res)
    return redirect(url_for('discussion.posts'))

@discussions_blueprint.route('/delete_post', methods=['POST']) 
@login_required
def delete_post():  
    if request.method == 'POST':       
        post_id = request.form.get('postId').strip()  
    res = client.db.discussions.delete_one({"_id": ObjectId(post_id)}) 
    print(res)
    return redirect(url_for('discussion.posts'))

@discussions_blueprint.route('/edit_post', methods=['GET']) 
@login_required
def edit_post():  
    if request.method == 'GET':         
        post_id = request.args.get('post_id') 
        res = client.db.discussions.find_one({"_id": ObjectId(post_id)})   
        print(res)
        return render_template('edit.html', discussion=res, post_id=post_id)


@discussions_blueprint.route('/comment', methods=['POST']) 
@login_required
def comment():  
    if request.method == 'POST':   
        post_id = request.form.get('postId').strip()
        comment_text = request.form.get('comment')
        user_id = str(request.form.get('userId'))  # Ensure the user ID is a string
    name = client.db.users.find_one({"_id": ObjectId(user_id)})
    comment = {"user_id": user_id, "comment": comment_text, "name": name['name']}
    print(post_id, "vnsdkok")
    # Update the discussion document by adding the comment
    res = client.db.discussions.update_one(
        {"_id": ObjectId(post_id)},
        {"$push": {"comments": comment}},
        upsert=True  # Create the document if it doesn't exist
    )
    return redirect(url_for('discussion.discussions'))

@discussions_blueprint.route('/like', methods=['POST']) 
@login_required
def like():  
    if request.method == 'POST':   
        post_id = request.form.get('postId').strip() 
        user_id = str(request.form.get('userId'))  # Ensure the user ID is a string   

    post = client.db.discussions.find_one({"_id": ObjectId(post_id)})
    if 'likes' in post:
        if user_id in post['likes']:
            return redirect(url_for('discussion.discussions'))
    res = client.db.discussions.update_one(
        {"_id": ObjectId(post_id)},
        {   
            "$addToSet": {"likes": user_id},  # Add to likes array if not already present
            "$inc": {"count": 1}  # Increment the count field by 1
        },
        upsert=True  # Create the document if it doesn't exist
    )
    return redirect(url_for('discussion.discussions'))

@discussions_blueprint.route('/follow', methods=['POST']) 
@login_required
def follow():  
    if request.method == 'POST':   
        profile = request.form.get('profile').strip()
        user_id = str(request.form.get('userId')).strip() # Ensure the user ID is a string   

    user = client.db.users.find_one({"_id": ObjectId(profile)})
    print(user)
    if 'followings' in user:
        if user_id in user['followings']:
            return redirect(url_for('discussion.users'))
    res = client.db.users.update_one(
        {"_id": ObjectId(profile)},
        {   
            "$addToSet": {"followings": user_id},  # Add to likes array if not already present 
        },
        upsert=True  # Create the document if it doesn't exist
    )
    print("this is the,", res)
    return redirect(url_for('discussion.users'))

@discussions_blueprint.route('/delete_profile', methods=['POST']) 
@login_required
def delete_profile():  
    if request.method == 'POST':       
        post_id = request.form.get('postId').strip()  
    res = client.db.users.delete_one({"_id": ObjectId(post_id)}) 
    res1 = client.db.discussions.delete_many({"user": ObjectId(post_id)})
    print(res)
    return redirect(url_for('auth.register'))




