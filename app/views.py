import os
from app import app, db, login_manager
from flask import render_template, request, redirect, url_for, flash, session, abort, send_from_directory, jsonify
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.utils import secure_filename
from werkzeug.security import check_password_hash
from datetime import datetime
from flask_wtf.csrf import generate_csrf
from app.models import UserProfile, FollowTB, LikesTB, PostsTB
from app.forms import UserRegistrationForm, LoginForm, MovieForm, NewPostForm


def form_errors(form):
    error_messages = []
    """Collects form errors"""
    for field, errors in form.errors.items():
        for error in errors:
            message = u"Error in the %s field - %s" % (
                    getattr(form, field).label.text,
                    error
                )
            error_messages.append(message)

    return error_messages

@app.route('/<file_name>.txt')
def send_text_file(file_name):
    """Send your static text file."""
    file_dot_text = file_name + '.txt'
    return app.send_static_file(file_dot_text)


@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also tell the browser not to cache the rendered page. If we wanted
    to we could change max-age to 600 seconds which would be 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response


@app.errorhandler(404)
def page_not_found(error):
    """Custom 404 page."""
    return render_template('404.html'), 404

@app.route('/')
def index():
    return jsonify(message="This is the beginning of our API")


#Accepts user information and saves it to the database
@app.route('/api/v1/register', methods=['POST'])
def register_user():
    form = UserRegistrationForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        email = form.email.data
        location = form.location.data
        biography = form.biography.data
        joined_on = datetime.now()

        profile_photo = form.profile_photo.data
        filename = secure_filename(profile_photo.filename)
        profile_photo.save(os.path.join(app.config['PROFILE_UPLOAD_FOLDER'], filename))

        user = UserProfile(username, password, first_name, last_name, email, location, biography, filename, joined_on)

        db.session.add(user)
        db.session.commit()

        return jsonify({
            "message": "User Successfully added",
            "username" : user.username,
            "first_name" : user.first_name,
            "last_name" : user.last_name,
            "email" : user.email,
            "location" : user.location,
            "biography" : user.biography
        }), 201
    else:
        errors = form_errors(form)
        return jsonify({"errors": errors}), 400
    

#user login
@app.route('/api/v1/auth/login', methods=['POST'])
def login():
    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = UserProfile.query.filter_by(username = username).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                return jsonify({
                    "message": "Login Successful",
                    "username" : user.username,
                    "first_name" : user.first_name,
                    "last_name" : user.last_name,
                    "email" : user.email,
                    "location" : user.location,
                    "biography" : user.biography
                }), 200
            else:
                #If password is incorrect
                return jsonify({"message": "Incorrect Password"}), 401
        else:
            #If username is not found
            return jsonify({"message": "User not found"}), 404
    else:
        #Error with form
        errors = form_errors(form)
        return jsonify({"errors": errors}), 400
    

#user logout
@app.route('/api/v1/auth/logout')
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout Successful"}), 200


#allows user to add a post
@app.route('/api/v1/users/<user_id>/posts', methods=['POST'])
@login_required
def add_post(user_id):
    form = NewPostForm()

    if form.validate_on_submit():
        photo = form.photo.data
        filename = secure_filename(photo.filename)
        photo.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        caption = form.caption.data
        created_on = datetime.now()
        post = PostsTB(caption, photo, user_id, created_on)

        db.session.add(post)
        db.session.commit()
        return jsonify({"message": "Post Added"}), 201
    else:
        #Error with form
        errors = form_errors(form)
        return jsonify({"errors": errors}), 400


#returns all posts for all users
@app.route('/api/v1/posts', methods=['GET'])
@login_required
def get_posts():
    posts = PostsTB.query.all()
    allposts = []

    for post in posts:
        data = {
            "photo" : post.photo,
            "caption" : post.caption
        }
        allposts.append(data)
        
    return jsonify({"posts" : allposts})


#returns all of a specific users posts
@app.route('/api/v1/users/<user_id>/posts', methods=['GET'])
@login_required
def get_user_post(user_id):
    posts = PostsTB.query.filter_by(user_id = user_id).all()
    allposts = []

    for post in posts:
        data = {
            "photo" : post.photo,
            "caption" : post.caption
        }
        allposts.append(data)
        
    return jsonify({"posts" : allposts})


#allows users to follow each other
@app.route('/api/users/<user_id>/follow', methods=['POST'])
@login_required
def follow(user_id):
    if UserProfile.query.get(user_id):
        currentuser = current_user.id
        follower_relationship = FollowTB(currentuser, user_id)
        
        db.session.add(follower_relationship)
        db.session.commit()
        return jsonify({"message": "User Followed"}), 201
    else:
        return jsonify({"message": "User not found"}), 404
    

#allows users to like posts
@app.route('/api/v1/posts/<post_id>/like', methods=['POST'])
@login_required
def like_post(post_id):
    if PostsTB.query.get(post_id):
        currentuser = current_user.id
        #checks to see if user has already liked the post
        liked_post = LikesTB.query.filter_by(post_id = post_id, user_id = currentuser).first()
        if liked_post:
            return jsonify({"message": "Post already liked"}), 400
        else:
            like = LikesTB(post_id, currentuser)          
            db.session.add(like)
            db.session.commit()
            return jsonify({"message": "Post liked"}), 201
    else:
        return jsonify({"message": "Post not found"}), 404

@app.route('/api/v1/csrf-token', methods=['GET']) 
def get_csrf(): 
    return jsonify({'csrf_token': generate_csrf()}) 