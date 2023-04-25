# Import necessary modules and libraries
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path



db = SQLAlchemy()


def create_database(app):
    # Check if the database file exists
    if not path.exists("database.db"):
        # Create the database tables
        db.create_all(app=app)
        print("Created database!")