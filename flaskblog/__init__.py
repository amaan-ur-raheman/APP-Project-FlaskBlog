from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flaskblog.config import Config



db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.login_message_category = "info"
mail = Mail()
migrate = Migrate()



def create_app(config_class=Config):
    """
    Creates and configures an instance of the Flask application.

    This function implements the application factory pattern, which allows for
    the creation of multiple application instances with different configurations.
    It initializes the database, bcrypt, login manager, mail, and migration
    services, and registers all blueprints.

    Args:
        config_class (object): The configuration class to use for the application.
                               Defaults to the `Config` class from `flaskblog.config`.

    Returns:
        Flask: A configured instance of the Flask application.
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    mail.init_app(app)
    migrate.init_app(app, db)

    from flaskblog.users.routes import users
    from flaskblog.posts.routes import posts
    from flaskblog.main.routes import main
    from flaskblog.errors.handlers import errors

    app.register_blueprint(users)
    app.register_blueprint(posts)
    app.register_blueprint(main)
    app.register_blueprint(errors)

    return app