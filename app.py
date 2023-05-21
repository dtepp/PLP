# Import necessary modules and libraries
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager
from application.views import views
from application.authentication import authentication
from application.models import User,Post,Comment,Like
from application.Database import db,create_database

# Create a SQLAlchemy object for database management
def create_app():
    # Create a Flask app instance
    app = Flask(__name__)
    # Set the secret key for the app
    app.config['SECRET_KEY'] = "perfetchworld"
    # Set the database URI for the app
    app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///database.db"
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize the SQLAlchemy object with the app
    db.init_app(app)
    # Push the app context
    app.app_context().push()
  

    #  register the views blueprint
    
    app.register_blueprint(views,url_prefix="/")
    
    # register the authentication blueprint
    
    app.register_blueprint(authentication,url_prefix="/")

    # Create the database if it does not exist
    create_database(app)
    
    # Initialize the LoginManager
    login_manager = LoginManager()
    login_manager.login_view = "authentication.log_in"
    login_manager.init_app(app)
    
    # Define a user loader function for the LoginManager
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
        
    # Return the app instance
    return app

if __name__=="__main__":
    app = create_app()
    app.run(debug=True)