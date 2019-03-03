from flask import Flask, flash, render_template, request, Blueprint, session, redirect, abort, current_app as app
import werkzeug
from werkzeug.utils import secure_filename
import os

from baseline import BaselineClassifier

upload = Blueprint('upload', __name__, template_folder='templates')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

	
@upload.route('/upload', methods = ['GET', 'POST'])
def uploader():
	if request.method == 'POST':
		file = request.files['file']
		
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
			
			return render_template('upload.html',
									filename=os.path.join(app.config['UPLOAD_FOLDER'],filename))
	else:
		return render_template('upload.html')

	
@upload.route('/classifier', methods = ['POST'])
def classifier():
	if request.method == 'POST':
		file = request.files['file']
		
		if file and allowed_file(file.filename):
			# Create temp copy of user's photo
			filename = os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(file.filename))
			file.save(filename)
			
			# Classify
			classifier = BaselineClassifier()
			classes = classifier.classify_objects(filename)

			return render_template('upload.html',
									classes=classes,
									filename=filename)
	return abort(403)

