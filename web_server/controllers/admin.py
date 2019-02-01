from flask import Flask, flash, render_template, request, Blueprint, session, redirect, abort
import os
import sqlite3
import pypyodbc

admin = Blueprint('admin', __name__, template_folder='templates')

@admin.route('/admin', methods = ['GET'])
def admin_route():
	if not ('admin' in session.keys()) or session['admin'] != 1:
		return abort(403)
	
	#Establishes connection
	conn = pypyodbc.connect("DRIVER={SQL Server};"
							"SERVER=eim-db-ag40;"
							"DATABASE=j69338_dev;"
							"Trusted_Connection=yes;")
	cursor = conn.cursor()
	
	if request.method == 'GET':
		
		# Pull Users
		exec_string = "SELECT ID, FName, LName, MyID, Email FROM Users;"
		users = cursor.execute(exec_string).fetchall()
		
		# Pull Sites
		exec_string = "SELECT ID, Name, City, State FROM Sites;"
		sites = cursor.execute(exec_string).fetchall()

		# Pull IPTs
		exec_string = "SELECT ID, Name FROM IPTs;"
		ipts = cursor.execute(exec_string).fetchall()
		
		# Pull Causes
		exec_string = "SELECT ID, Name, Category FROM Causes;"
		causes = cursor.execute(exec_string).fetchall()
		
		# Pull Suppliers
		exec_string = "SELECT ID, Name, Code, DateAddedToProgram, City, State FROM Suppliers;"
		suppliers = cursor.execute(exec_string).fetchall()
		
		# Pull Work Breakdown Structures
		exec_string = "SELECT ID, Name, Code, SQARelevant FROM WorkBreakdownStructures;"
		wbss = cursor.execute(exec_string).fetchall()
		
		return render_template("admin.html",
								users = users,
								sites = sites,
								ipts = ipts,
								causes = causes,
								suppliers = suppliers,
								wbss = wbss,
								breadcrumbs = [
									("Administrator's Portal", "#")
								])

	else:
		return abort(403)

@admin.route('/login', methods = ['GET'])
def login():
	#Establishes connection
	conn = pypyodbc.connect("DRIVER={SQL Server};"
							"SERVER=eim-db-ag40;"
							"DATABASE=j69338_dev;"
							"Trusted_Connection=yes;")
	cursor = conn.cursor()
	
	if 'username' not in session:
		return render_template("login.html")
	else:
		return redirect ('/audits')

