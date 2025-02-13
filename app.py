# Starting of the app
from flask import Flask
from backend.models import db

app = None

def setup_app():
    global app  
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///service_app.sqlite3"  # Ensure correct SQLite URI
    db.init_app(app)  
    app.app_context().push() 
    app.debug = True
    print("app is started...")

# Call the setup
setup_app()

from backend.controllers import *  

if __name__ == "__main__":
    app.run()
