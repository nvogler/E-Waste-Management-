from datetime import datetime
from collections import namedtuple
from flask import Flask, flash, render_template, request, Blueprint, jsonify, session, redirect, current_app as app
import string, re, hashlib, uuid
import requests
import time

admin_api = Blueprint('admin_api', __name__)

@admin_api.route('/api/v1/admin/login', methods=['POST'])
def login():
	# Link with DB
	conn = app.config['CONNECTION']
	cursor = conn.cursor()

	response = {}
	
	try:
		# Clean input
		login = request.form['login'].lower()
		pin = request.form['pin']
		
		# Run Query
		exec_string = "SELECT ID, FirstName, LastName  FROM Users WHERE Login = %s AND PIN = %s;"
		cursor.execute(exec_string, [login, pin])
		result = cursor.fetchone()

		if type(result) != type(None):
			session['userid'] = result[0]
			session['name'] = result[1] + " " + result[2]
			
			response['status'] = 1
		else:
			response['status'] = 0

	except Exception as e:
		response['status'] = 0
		response['message'] = str(e)
		
	return jsonify(response)

@admin_api.route('/api/v1/admin/logout', methods=['POST'])
def logout():
	response = {}

	try:
		session.clear()
		response['status'] = 1

	except Exception as e:
		response['status'] = 0
		response['message'] = str(e)
		
	return jsonify(response)
	
@admin_api.route('/api/v1/admin/createAccount', methods=['POST'])
def create_account():
	# Link with DB
	conn = app.config['CONNECTION']
	cursor = conn.cursor()

	response = {}
	
	try:
		# Clean input
		fname = request.form['fname']
		lname = request.form['lname']
		uname = request.form['uname']
		city = request.form['city']
		state = request.form['state']
		zip_ = request.form['zip']
		pw = request.form['pw']
		
		# Pull location if exists, else create and get key
		lockey = None
		exec_string = "SELECT ID FROM Locations WHERE City = %s AND State = %s AND Zip = %s"
		try:
			cursor.execute(exec_string, [city, state, zip_])
			lockey = cursor.fetchone()[0]
		except:
			exec_string_two = "INSERT INTO Locations (City, State, Zip) VALUES (%s, %s, %s)"
			cursor.execute(exec_string_two, [city, state, zip_])
			conn.commit()
			cursor.execute(exec_string, [city, state, zip_])
			lockey = cursor.fetchone()[0]
		
		# Add user
		exec_string = "INSERT INTO Users (FirstName, LastName, LocationKey, Login, PIN) VALUES (%s, %s, %s, %s, %s)"
		cursor.execute(exec_string, [fname, lname, lockey, uname, pw])
		conn.commit()

		# Try login
		exec_string = "SELECT ID, FirstName, LastName  FROM Users WHERE Login = %s AND PIN = %s;"
		cursor.execute(exec_string, [uname, pw])
		result = cursor.fetchone()
		
		if type(result) != type(None):
			session['userid'] = result[0]
			session['name'] = result[1] + " " + result[2]
			
			response['status'] = 0
		else:
			response['status'] = 1

	except Exception as e:
		response['status'] = 1
		response['message'] = str(e)
		
	return jsonify(response)