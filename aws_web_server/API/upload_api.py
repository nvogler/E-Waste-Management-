from flask import Flask, request, Blueprint, session, jsonify, redirect, abort, current_app as app
import os
from datetime import datetime

upload_api = Blueprint('upload_api', __name__, template_folder='templates')


@upload_api.route('/add_item', methods = ['POST'])
def add_item():
	if 'userid' in session and request.method == 'POST':
		# Link with DB
		conn = app.config['CONNECTION']
		cursor = conn.cursor()
		
		response = {}
		try:
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
						ret_classes.append(class_)
						
						# Insert Image to DB
						exec_string = """
						Insert INTO Items (DateAdded, Image, User, Type, Notes) VALUES (%s, %s, %s, %s, %s);
						"""
						
						cursor.execute(exec_string, [datetime.now().date(), filename, int(session['userid']), class_[2], notes])
						conn.commit()
				
				response['status'] = 0
				response['classes'] = ret_classes
				response['message'] = "Item(s) added."
	
		except Exception as e:
			response['status'] = q
			response['message'] = (str(e))
			
		finally:
			return jsonify(response)
			
	return abort(500)
					
@upload_api.route('/update_item', methods = ['POST'])
def update_item():

	if 'userid' in session and request.method == 'POST':
		# Link with DB
		conn = app.config['CONNECTION']
		cursor = conn.cursor()
		
		response = {}
		try:
			id = int(request.form['id'])
			if str(request.form['dispo_val']) == '1':
				dispo_date = datetime.now().date()
			else:
				dispo_date = None
			notes = request.form['notes_val']
			print (notes)
			exec_string = """
			UPDATE Items SET DateDisposed = %s, Notes = %s WHERE ID = %s
			"""
			
			cursor.execute(exec_string, [dispo_date, notes, id])
			conn.commit()

			response['status'] = 1
			response['message'] = "Item updated."
				
		except Exception as e:
			response['status'] = 0
			response['message'] = (str(e))
			
		finally:
			return jsonify(response)
			
	return abort(403)
	
@upload_api.route('/delete_item', methods = ['POST'])
def delete_item():

	if 'userid' in session and request.method == 'POST':
		# Link with DB
		conn = app.config['CONNECTION']
		cursor = conn.cursor()
		
		response = {}
		try:
			id = int(request.form['id'])

			exec_string = """
			DELETE FROM Items WHERE ID = %s
			"""
			
			cursor.execute(exec_string, [id])
			conn.commit()

			response['status'] = 1
			response['message'] = "Item deleted."
				
		except Exception as e:
			response['status'] = 0
			response['message'] = (str(e))
			
		finally:
			return jsonify(response)
			
	return abort(403)


