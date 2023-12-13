from flask import Blueprint, render_template, request, send_from_directory, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
from flask_login import login_required
from . import db
import tensorflow as tf
import numpy as np
from PIL import Image
from prediction import generate_caption
from instagram_posting import post_to_instagram
from gpt_integration import generate_gpt_caption  
from twitter_posting import tweet_post

views = Blueprint('views', __name__)

# Allowable image extensions 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
# Image Upload Folder
UPLOAD_FOLDER = 'website/static/uploads/'

# This route handles the home page of the website
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            # Generate the image caption
            generated_caption = generate_caption(file_path)
            
            # Get the sentiment from the form
            sentiment = request.form['sentiment']

            # Generate a better caption using GPT-3
            better_caption = generate_gpt_caption(generated_caption, sentiment)  

            # Display the image caption
            flash('Image Caption Generated and Displayed Below!')
            return render_template('home.html', filename=filename, better_caption=better_caption)

        else:
            flash('Allowed image types are - png, jpg, jpeg, gif')

    # If the request method is GET, then render the home page
    filename = request.args.get('filename', None)
    better_caption = None  # Initialize to None if no caption is generated
    return render_template('home.html', filename=filename, better_caption=better_caption)

# This handles the image upload
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#  This route handles the image display
@views.route('/uploads/<filename>')
def display_image(filename):
    return send_from_directory('static/uploads', filename)

# This route handles the Instagram post action
@views.route('/post_to_instagram_action', methods=['POST'])
def post_to_instagram_action():
    # This route handles the actual Instagram post action
    caption = request.form.get('caption')  # Get the caption from the form
    filename = request.form.get('filename')  # Get the filename from the form
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    # Post the image to Instagram using the post_to_instagram function
    post_to_instagram(caption, file_path)
    # Display a success message
    flash('Image posted to Instagram successfully!', category='success')
    return redirect(url_for('views.home'))

#this route handles the twitter post action
@views.route('/post_to_twitter_action', methods=['POST'])
def post_to_twitter_action():
    caption = request.form.get('caption')
    filename = request.form.get('filename')
    file_path = os.path.join(UPLOAD_FOLDER, filename)

    # Post the image to Instagram using the tweet_post function
    tweet_post(file_path, caption)

    flash('Image posted to Twitter successfully!', category='success')
    return redirect(url_for('views.home'))
