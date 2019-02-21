from flask import Flask, render_template, request, Blueprint, session, redirect
from werkzeug.serving import run_simple
import os
import pypyodbc

# Initialize Flask app with the template folder address
app = Flask(__name__, template_folder='templates')

# Register the controllers
import controllers
app.register_blueprint(controllers.admin)

# Register the APIs
import API
app.register_blueprint(API.admin_api)

# Session key
app.secret_key = os.urandom(24).hex()
		
# Globals
app.config['UPLOAD_FOLDER'] = 'static/tmp/'

@app.route('/')
#@login_required
def index():
	return redirect('/upload')

######################################################
# Listen on external IPs
if __name__ == '__main__':
	app.run('0.0.0.0', port=80)

