from datetime import datetime
from collections import namedtuple
from flask import Flask, flash, render_template, request, Blueprint, jsonify, session, redirect
from pyad import aduser, adquery
import sqlite3, string, re, hashlib, uuid
import requests
import werkzeug
import time
import pypyodbc
import binascii

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

@admin_api.route('/api/v1/admin/queryUserById', methods=['GET', 'POST'])
def queryUserById():
	#Establishes connection
	conn = pypyodbc.connect("DRIVER={SQL Server};"
							"SERVER=eim-db-ag40;"
							"DATABASE=j69338_dev;"
							"Trusted_Connection=yes;")
	cursor = conn.cursor()
	
	# Clean input
	id = request.form['id']
	
	# Run Query
	result = {}
	
	try:
		# Pull User Data
		exec_string = "SELECT Email, FName, LName, MyID, Cast(Admin AS int), PrcAuditsPermission, SupAuditsPermission FROM Users WHERE ID = ?"
		result['data'] = cursor.execute(exec_string, [id]).fetchone()
		result['status'] = 1
		
	except Exception as e:
		result['status'] = 0
		result['message'] = str(e)
		
	finally:
		return jsonify(result)

@admin_api.route('/api/v1/admin/queryGenById', methods=['GET', 'POST'])
def queryGenById():
	#Establishes connection
	conn = pypyodbc.connect("DRIVER={SQL Server};"
							"SERVER=eim-db-ag40;"
							"DATABASE=j69338_dev;"
							"Trusted_Connection=yes;")
	cursor = conn.cursor()
	
	# Clean input
	id = request.form['id']
	table = request.form['table']
	
	# Run Query
	result = {}
	
	try:
		# Pull [general] Data
		exec_string = "SELECT * FROM " + table + " WHERE ID = ?"
		result['data'] = cursor.execute(exec_string, [id]).fetchone()
		result['status'] = 1
		
	except Exception as e:
		result['status'] = 0
		result['message'] = str(e)
		
	finally:
		return jsonify(result)

@admin_api.route('/api/v1/admin/createUpdateUser', methods=['POST'])
def createUpdateUser():
	#Establishes connection
	conn = pypyodbc.connect("DRIVER={SQL Server};"
							"SERVER=eim-db-ag40;"
							"DATABASE=j69338_dev;"
							"Trusted_Connection=yes;")
	cursor = conn.cursor()
	
	response = {}
	
	try:
		# Clean input
		email = request.form['email']
		fname = request.form['fname']
		lname = request.form['lname']
		myid = request.form['myid'].lower()
		password = myid #request.form['password']
		admin = 1 if request.form['admin'] == 'true' else 0
		prc_lead = 3 if request.form['prc_lead'] == 'true' else 1
		prc_auditor = 5 if request.form['prc_auditor'] == 'true' else 1
		prc_auditee = 7 if request.form['prc_auditee'] == 'true' else 1
		prc_assignee = 11 if request.form['prc_assignee'] == 'true' else 1
		sup_lead = 3 if request.form['sup_lead'] == 'true' else 1
		sup_auditor = 5 if request.form['sup_auditor'] == 'true' else 1
		sup_auditee = 7 if request.form['sup_auditee'] == 'true' else 1
		sup_assignee = 11 if request.form['sup_assignee'] == 'true' else 1
		field = request.form['field']

		exec_string = "SELECT COUNT(*) FROM " + field + "s WHERE MyID = '" + myid + "'"

		# Update
		if (cursor.execute(exec_string).fetchone()[0] > 0):
			exec_string = "UPDATE " + field + "s SET FName = ?, LName = ?, Password = ?, Email = ?, Admin = ?, PrcAuditsPermission = ?, SupAuditsPermission = ? WHERE MyID = ?"

			cursor.execute(exec_string, [fname, lname, password, email, admin, prc_lead * prc_assignee * prc_auditor * prc_auditee, sup_assignee * sup_auditee * sup_auditor * sup_lead, myid])
			conn.commit()
			response['status'] = 2
			
		# Insert
		else:
			exec_string = "INSERT INTO " + field + "s (FName, LName, MyID, Password, Email, Admin, PrcAuditsPermission, SupAuditsPermission) OUTPUT INSERTED.ID VALUES (?, ?, ?, ?, ?, ?, ?, ?);"

			id = cursor.execute(exec_string, [fname, lname, myid, password, email, admin, prc_lead * prc_assignee * prc_auditor * prc_auditee, sup_assignee * sup_auditee * sup_auditor * sup_lead]).fetchone()[0]

			conn.commit()
			response['status'] = 1
			response['id'] = id

	except Exception as e:
		response['status'] = 0
		response['message'] = str(e)
		
	finally:
		return jsonify(response)

@admin_api.route('/api/v1/admin/createRowShort', methods=['POST'])
def createRowShort():
	#Establishes connection
	conn = pypyodbc.connect("DRIVER={SQL Server};"
							"SERVER=eim-db-ag40;"
							"DATABASE=j69338_dev;"
							"Trusted_Connection=yes;")
	cursor = conn.cursor()
		
	try:
		# Clean input
		name = request.form['name']
		field = request.form['field']
		
		# Run Query
		exec_string = "INSERT INTO " + field + "s (name) OUTPUT INSERTED.ID VALUES (?);"
		id = cursor.execute(exec_string, [name]).fetchone()[0]

		conn.commit()
		response = {}
		response['status'] = 1
		response['id'] = id
	except Exception as e:
		response = {}
		response['status'] = 0
		response['message'] = e
	finally:
		return jsonify(response)

@admin_api.route('/api/v1/admin/createUpdateGen', methods=['POST'])
def createUpdateGen():
	#Establishes connection
	conn = pypyodbc.connect("DRIVER={SQL Server};"
							"SERVER=eim-db-ag40;"
							"DATABASE=j69338_dev;"
							"Trusted_Connection=yes;")
	cursor = conn.cursor()
	
	response = {}
	
	try:
		# Clean input
		field = request.form['field']
		name = request.form['name']
		exec_string = "SELECT COUNT(*) FROM " + field + "s WHERE Name = '" + name + "'"

		# Update
		if (cursor.execute(exec_string).fetchone()[0] > 0):
			values = []
			exec_string = "UPDATE " + field + "s SET "
			
			# Parse/clean input
			keys = list(request.form.keys())
			keys.remove('field')
			keys.remove('name')
			for key in keys:
				values.append(request.form[key])
				exec_string += key + ' = ?, '
			
			exec_string = exec_string.rstrip(', ') + " WHERE Name = ?"
			values.append(name)
			
			cursor.execute(exec_string, values)
			conn.commit()
			response['status'] = 2
			
		# Insert
		else:
			values = []
			exec_string_ini = "INSERT INTO " + request.form['field'] + 's '
			exec_string_mid = "("
			exec_string_end = " VALUES ("
			
			# Parse/clean input
			keys = list(request.form.keys())
			keys.remove('field')
			for key in keys:
				values.append(request.form[key])
				exec_string_mid += key + ', '
				exec_string_end += "?, "
				
			exec_string_ini = exec_string_ini.rstrip(',')
			exec_string_mid = exec_string_mid.rstrip(', ') + ")"
			exec_string_end = exec_string_end.rstrip(', ') + ");"
			
			exec_string = exec_string_ini + exec_string_mid + " OUTPUT INSERTED.ID" + exec_string_end
			
			# Run Query
			id = cursor.execute(exec_string, values).fetchone()[0]

			conn.commit()
			response = {}
			response['status'] = 1
			response['id'] = id
		
	except Exception as e:
		response = {}
		response['status'] = 0
		response['message'] = str(e)
		
	finally:
		return jsonify(response)
		
@admin_api.route('/api/v1/admin/deleteRow', methods=['GET', 'POST'])
def deleteRow():
	#Establishes connection
	conn = pypyodbc.connect("DRIVER={SQL Server};"
							"SERVER=eim-db-ag40;"
							"DATABASE=j69338_dev;"
							"Trusted_Connection=yes;")
	cursor = conn.cursor()
	print ("hre")
	response = {}
	try:
		id = int(request.form['id'])
		field = request.form['field']
		
		if field in ['Assignee', 'IPT', 'Cause']:
			exec_string = """
							SELECT DISTINCT ? FROM processfindings
							UNION
							SELECT DISTINCT ? FROM supplierfindings
						"""
		else:
			exec_string = """
							SELECT DISTINCT ? FROM processaudits
							UNION
							SELECT DISTINCT ? FROM supplieraudits
						"""
			
		result = list(sum(cursor.execute(exec_string, [field, field]).fetchall(), ()))

		if id in result:
			response['status'] = 0
			response['message'] = "Cannot delete " + field + "s with existing relationships."
			
		else:
			exec_string = "DELETE FROM " + field + "s WHERE ID = ?"
			cursor.execute(exec_string, [id])
			conn.commit()

			response['status'] = 1
			response['message'] = "Success"
			
	except Exception as e:
		response['status'] = 0
		response['message'] = (str(e))
		
	finally:
		return jsonify(response)
		

@admin_api.route('/api/v1/admin/login', methods=['POST'])
def login_route():
	#Establishes connection
	conn = pypyodbc.connect("DRIVER={SQL Server};"
							"SERVER=eim-db-ag40;"
							"DATABASE=j69338_dev;"
							"Trusted_Connection=yes;")
	cursor = conn.cursor()
	response = {}
	
	try:
		# Clean input
		username = request.form['username'].lower()
		password = username #request.form['password']
		
		# Run Query
		exec_string = "SELECT ID, Admin, PrcAuditsPermission, PrcAuditsPermission FROM Users WHERE MyID = ? AND Password = ?;"
		result = cursor.execute(exec_string, [username, password]).fetchone()

		if type(result) != type(None):
			session['userid'] = result[0]
			session['admin'] = int(binascii.b2a_hex(result[1]), 2)
			session['process_perms'] = result[2]
			session['supplier_perms'] = result[3]
			session['username'] = username
			
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