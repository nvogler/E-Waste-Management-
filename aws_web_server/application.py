from flask import Flask, redirect, session
import pymysql
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

host="w210-e-waste.cah8dllkneeh.us-east-2.rds.amazonaws.com"
port=3306
dbname="w210ewaste"
user="ewasteadmin"
password="admin12345"

conn = pymysql.connect(host, user=user,port=port,
                           passwd=password, db=dbname)
application.config['CONNECTION'] = conn

@application.route('/index')
def index():
	if 'userid' in session:
		return redirect('/user_classifier')
	else:
		return redirect('/login')

######################################################
# Listen on external IPs
if __name__ == '__main__':
    #serve(application)
	application.run(debug=True)
