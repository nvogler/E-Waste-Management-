from flask import Flask, flash, render_template, request, Blueprint, session, redirect, abort, current_app as app
import werkzeug
from werkzeug.utils import secure_filename
import os
import sqlite3
from baseline import BaselineClassifier
from datetime import date, datetime

upload = Blueprint('upload', __name__, template_folder='templates')

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
	return '.' in filename and \
		filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@upload.route('/community_classifier', methods = ['GET', 'POST'])
def community_classifier():
	if 'userid' not in session:
		return redirect('/login')
		
	# Link with DB
	conn = sqlite3.connect("ewaste_data.db")
	cursor = conn.cursor()
	
	classes = None
	filename = None
	scroll = None

	if request.method == 'POST':
		file = request.files['file']
		notes = request.form['notes']
		
		if file and allowed_file(file.filename):
			# Save user's photo
			filename = os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(file.filename))
			file.save(filename)
			
			# Classify
			classifier = BaselineClassifier()
			classes = classifier.classify_objects(filename)
			
			for class_ in classes:
				if class_[1]:
					# Scroll down to image div on page load
					scroll = True
					
					# Insert Image to DB
					exec_string = """
					Insert INTO Items (DateAdded, Image, User, Type, Notes) VALUES (?, ?, ?, ?, ?);
					"""
					print (class_)
					cursor.execute(exec_string, [datetime.now().date(), filename, int(session['userid']), class_[2], notes])
					conn.commit()
		
	# Pull Items
	exec_string = """
	SELECT  i.ID,
			i.Image,
			it.Category,
			DateAdded,
			DateDisposed,
			dt.Type,
			Notes,
			u.FirstName + " " + u.LastName AS User
	FROM Items AS i
	INNER JOIN 
		Users AS u ON u.ID = i.User
	INNER JOIN
		ItemTypes AS it ON it.ID = i.Type
	INNER JOIN 
		DisposalTypes AS dt ON dt.ID = it.DisposalType
	"""
	items = cursor.execute(exec_string).fetchall()
	
	return render_template('upload.html',
							items=items,
							classes=classes,
							scroll=scroll,
							community=True,
							filename=filename)

@upload.route('/user_classifier', methods = ['GET', 'POST'])
def user_classifier():
	if 'userid' not in session:
		return redirect('/login')
		
	# Link with DB
	conn = sqlite3.connect("ewaste_data.db")
	cursor = conn.cursor()
	
	classes = None
	filename = None
	scroll = None

	if request.method == 'POST':
		file = request.files['file']
		notes = request.form['notes']
		
		if file and allowed_file(file.filename):
			# Save user's photo
			filename = os.path.join(app.config['UPLOAD_FOLDER'],secure_filename(file.filename))
			file.save(filename)
			
			# Classify
			classifier = BaselineClassifier()
			classes = classifier.classify_objects(filename)
			
			for class_ in classes:
				if class_[1]:
					# Scroll down to image div on page load
					scroll = True
					
					# Insert Image to DB
					exec_string = """
					Insert INTO Items (DateAdded, Image, User, Type, Notes) VALUES (?, ?, ?, ?, ?);
					"""
					print (class_)
					cursor.execute(exec_string, [datetime.now().date(), filename, int(session['userid']), class_[2], notes])
					conn.commit()
		
	# Pull Items
	exec_string = """
	SELECT  i.ID,
			i.Image,
			it.Category,
			DateAdded,
			DateDisposed,
			dt.Type,
			Notes,
			u.FirstName + " " + u.LastName AS User
	FROM Items AS i
	INNER JOIN 
		Users AS u ON u.ID = i.User
	INNER JOIN
		ItemTypes AS it ON it.ID = i.Type
	INNER JOIN 
		DisposalTypes AS dt ON dt.ID = it.DisposalType
	WHERE i.User = ?
	"""
	items = cursor.execute(exec_string, [ session['userid'] ]).fetchall()
	
	return render_template('upload.html',
							items=items,
							classes=classes,
							scroll=scroll,
							community=False,
							filename=filename)
