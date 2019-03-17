from flask import Flask, request, Blueprint, session, jsonify, redirect, abort, current_app as app
import os
import sqlite3

upload_api = Blueprint('upload_api', __name__, template_folder='templates')


@upload_api.route('/update_item', methods = ['POST'])
def update_item():

	if 'userid' in session and request.method == 'POST':
		# Link with DB
		conn = sqlite3.connect("ewaste_data.db")
		cursor = conn.cursor()
		
		response = {}
		try:
			id = int(request.form['id'])
			dispo_date = request.form['dispo_date']
			
			exec_string = """
			UPDATE Items SET DateDisposed = ? WHERE ID = ?
			"""
			
			cursor.execute(exec_string, [dispo_date, id])
			conn.commit()

			response['status'] = 1
			response['message'] = "Item updated."
				
		except Exception as e:
			response['status'] = 0
			response['message'] = (str(e))
			
		finally:
			return jsonify(response)
			
	return abort(403)

