"""
Main entry point for the Flask blog application.

This script initializes and runs the Flask application using the application factory pattern.
To run the application, execute this script directly. For example:
    $ python app.py
"""
from flaskblog import create_app

app = create_app()


if __name__ == "__main__":
    app.run(debug=True)