from datetime import datetime
from collections import namedtuple
from flask import Flask, flash, render_template, request, Blueprint, jsonify, session, redirect, current_app as app
import string, re, hashlib, uuid
import requests
import time
import sqlite3

admin_api = Blueprint('admin_api', __name__)

@admin_api.route('/api/v1/admin/login', methods=['POST'])
def login():
	# Link with DB
	conn = sqlite3.connect("ewaste_data.db")
	cursor = conn.cursor()

	response = {}
	
	try:
		# Clean input
		login = request.form['login'].lower()
		pin = request.form['pin']
		
		# Run Query
		exec_string = "SELECT ID, FirstName, LastName  FROM Users WHERE Login = ? AND PIN = ?;"
		result = cursor.execute(exec_string, [login, pin]).fetchone()

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