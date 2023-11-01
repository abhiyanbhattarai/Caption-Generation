from flask import Blueprint, render_template, request, send_from_directory, flash, redirect, url_for, session, current_app
from werkzeug.utils import secure_filename
import os
from flask_login import login_required
from . import db
import tensorflow as tf
import numpy as np
from PIL import Image
from prediction import generate_caption, model1, EncoderDecoder
# from datetime import datetime, timedelta, timezone
from instagram_posting import post_to_instagram

views = Blueprint('views', __name__)

# Allowable image extensions 
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
# Image Upload Folder
UPLOAD_FOLDER = 'website/static/uploads/'


# def check_session_timeout():
#     last_activity = session.get('last_activity')
#     now = datetime.now(timezone.utc)
#     session_timeout = timedelta(seconds=600)  # Set the session timeout to 10 minutes (adjust as needed)
#     if last_activity is not None and now - last_activity > session_timeout:
#         flash('Session timed out. Please log in again.', category='error')
#         return redirect(url_for('auth.login'))

# This route handles the home page of the website
@views.route('/', methods=['GET', 'POST'])
@login_required
def home():
    # check_session_timeout()  # Apply session timeout check before processing the /home route
    if request.method == 'POST':
        file = request.files['file']
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(file_path)

            # Generate the image caption
            generated_caption = generate_caption(file_path,model1())
            flash('Image Caption Generated and Displayed Below!')
            return render_template('home.html', filename=filename, generated_caption=generated_caption)

        else:
            flash('Allowed image types are - png, jpg, jpeg, gif')

    filename = request.args.get('filename', None)
    generated_caption = None  # Initialize to None if no caption is generated
    return render_template('home.html', filename=filename, generated_caption=generated_caption)

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

    flash('Image posted to Instagram successfully!', category='success')
    return redirect(url_for('views.home'))