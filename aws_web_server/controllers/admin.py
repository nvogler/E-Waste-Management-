from flask import Flask, flash, render_template, request, Blueprint, session, redirect, abort, current_app as app
import os
import sqlite3

admin = Blueprint('admin', __name__, template_folder='templates')

@admin.route('/login', methods = ['GET'])
def login():
	
	if 'username' not in session:
		return render_template("login.html")
	else:
		return redirect ('/classifier')