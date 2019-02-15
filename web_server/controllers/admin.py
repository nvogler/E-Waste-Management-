from flask import Flask, flash, render_template, request, Blueprint, session, redirect, abort
import os
import sqlite3
import pypyodbc

admin = Blueprint('admin', __name__, template_folder='templates')

@admin.route('/admin', methods = ['GET'])
def admin_route():

	return render_template("admin.html")


