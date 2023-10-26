from flask import Blueprint, render_template, request,send_from_directory, flash, redirect, url_for
from werkzeug.utils import secure_filename
import os
from . import db
import tensorflow as tf
import numpy as np
from PIL import Image
from prediction import generate_caption, model1, EncoderDecoder

views = Blueprint('views', __name__)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
UPLOAD_FOLDER = 'website/static/uploads/'

@views.route('/', methods=['GET', 'POST'])
def home():
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

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@views.route('/uploads/<filename>')
def display_image(filename):
    return send_from_directory('static/uploads', filename)
