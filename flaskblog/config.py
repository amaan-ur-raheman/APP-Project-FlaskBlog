import os


class Config:
    """
    Configuration class for the Flask application.

    This class holds all the configuration variables for the application.
    The values are loaded from environment variables to keep sensitive
    information secure.

    Attributes:
        SECRET_KEY (str): A secret key for signing session cookies and other
                          security-related needs.
        SQLALCHEMY_DATABASE_URI (str): The database URI that should be used
                                       for the connection.
        MAIL_SERVER (str): The hostname or IP address of the mail server.
        MAIL_PORT (int): The port number of the mail server.
        MAIL_USE_TLS (bool): A boolean indicating whether to use TLS.
        MAIL_USERNAME (str): The username for the email account.
        MAIL_PASSWORD (str): The password for the email account.
    """
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = os.environ.get("SQLALCHEMY_DATABASE_URI")
    MAIL_SERVER = "smtp.googlemail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USERNAME = os.environ.get("EMAIL_USERNAME")
    MAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")