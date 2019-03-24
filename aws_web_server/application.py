from flask import Flask, redirect, session
import sqlite3
from waitress import serve
import os

# Initialize Flask app with the template folder address
application = Flask(__name__, template_folder='templates')

# Session key
application.secret_key = os.urandom(24).hex()

# Register the controllers
import controllers
application.register_blueprint(controllers.upload)
application.register_blueprint(controllers.admin)

# Register the apis
import API
application.register_blueprint(API.upload_api)
application.register_blueprint(API.admin_api)

# Globals
application.config['UPLOAD_FOLDER'] = 'static/uploads/'
#application.config['CONNECTION'] = sqlite3.connect("ewaste_data.db")

@application.route('/')
def index():
	if 'userid' in session:
		return redirect('/user_classifier')
	else:
		return redirect('/login')

######################################################
# Listen on external IPs
if __name__ == '__main__':
    serve(application)
