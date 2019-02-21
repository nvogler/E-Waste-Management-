from datetime import datetime
from collections import namedtuple
from flask import Flask, flash, render_template, request, Blueprint, abort, jsonify, session, redirect, url_for, current_app as app
import requests
import werkzeug
from werkzeug.utils import secure_filename
import time
import pypyodbc
import os
from baseline import BaselineClassifier

admin_api = Blueprint('admin_api', __name__)

@admin_api.route('/api/v1/admin/queryUserDetails', methods=['GET', 'POST'])
def getUserADInfoFromEmail():

	# Clean input
	email = request.args.get('email').lower().strip()

	# Run Query
	try:
		qry = adquery.ADQuery()
		qry.execute_query(attributes=["extensionAttribute6", "givenName", "sn"], where_clause="mail = '" + email + "'")
		result = qry.get_all_results()[0]
		result['status'] = 1
		
	except:
		result = {}
		result['status'] = 0
		
	finally:
		return jsonify(result)

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@admin_api.route('/upload', methods = ['GET', 'POST'])
def upload_file():
	return render_template('upload.html')
	
@admin_api.route('/uploader', methods = ['POST'])
def uploader():
	if request.method == 'POST':
		file = request.files['file']
		
		if file and allowed_file(file.filename):
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
			
			return render_template('upload.html',
									filename=os.path.join(app.config['UPLOAD_FOLDER'],filename))
	return abort(403)
	
@admin_api.route('/classifier', methods = ['POST'])
def classifier():
	if request.method == 'POST':
		file = request.files['file']
		
		if file and allowed_file(file.filename):
			# Create temp copy of user's photo
			filename = os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(file.filename))
			file.save(filename)
			
			# Classify
			classifier = BaselineClassifier()
			classified_file = classifier.classify_objects(filename)

			return render_template('upload.html',
									filename=classified_file)
	return abort(403)
	
		