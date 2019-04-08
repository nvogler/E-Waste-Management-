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

@admin.route('/join', methods = ['GET', 'POST'])
def create():
	if 'username' not in session:
		return render_template("create.html")
	else:
		return redirect ('/home')

@admin.route('/', methods = ['GET'])
def home():
	return render_template("home.html")
	
@admin.route('/about', methods = ['GET'])
def about():
	return render_template("about.html")