from flask import Flask, redirect

# Initialize Flask app with the template folder address
application = Flask(__name__, template_folder='templates')

# Register the controllers
import controllers
application.register_blueprint(controllers.upload)

# Globals
application.config['UPLOAD_FOLDER'] = 'static/tmp/'

@application.route('/')
def index():
    return redirect('/upload')

######################################################
# Listen on external IPs
if __name__ == '__main__':

    application.run()
