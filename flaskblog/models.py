from itsdangerous import TimedSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager
from datetime import datetime
from flask_login import UserMixin



@login_manager.user_loader
def load_user(user_id):
    """
    Loads a user from the database given their user ID.

    This function is required by Flask-Login to manage user sessions.

    Args:
        user_id (str): The ID of the user to load.

    Returns:
        User: The user object corresponding to the given ID, or None if not found.
    """
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """
    Represents a user in the database.

    Attributes:
        id (int): The primary key for the user.
        username (str): The user's unique username.
        email (str): The user's unique email address.
        image_file (str): The filename of the user's profile picture.
        password (str): The user's hashed password.
        posts (relationship): A relationship to the posts created by the user.
    """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default="default.jpg")
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship("Post", backref="author", lazy=True)

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

    def get_reset_token(self, expires_sec=1800):
        """
        Generates a password reset token for the user.

        Args:
            expires_sec (int): The number of seconds until the token expires.
                               Defaults to 1800 (30 minutes).

        Returns:
            str: A timed-serialized token for password reset.
        """
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}, salt='reset-password')

    @staticmethod
    def verify_reset_token(token):
        """
        Verifies a password reset token.

        Args:
            token (str): The password reset token to verify.

        Returns:
            User: The user object corresponding to the token, or None if the
                  token is invalid or expired.
        """
        s = Serializer(current_app.config['SECRET_KEY'])

        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        
        return User.query.get(user_id)


class Post(db.Model):
    """
    Represents a blog post in the database.

    Attributes:
        id (int): The primary key for the post.
        title (str): The title of the post.
        date (datetime): The date and time the post was created.
        content (str): The content of the post.
        user_id (int): The foreign key of the user who created the post.
        likes (relationship): A relationship to the likes on the post.
    """
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    # Relationship to track likes
    likes = db.relationship('Like', backref='post', lazy=True)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date}')"


class Like(db.Model):
    """
    Represents a "like" on a post by a user.

    This model creates a many-to-many relationship between users and posts,
    where each row signifies that a user has liked a specific post.

    Attributes:
        id (int): The primary key for the like.
        user_id (int): The foreign key of the user who liked the post.
        post_id (int): The foreign key of the post that was liked.
    """
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    def __repr__(self):
        return f"Like('{self.user_id}', '{self.post_id}')"


class Comment(db.Model):
    """
    Represents a comment on a blog post.

    Attributes:
        id (int): The primary key for the comment.
        content (str): The text content of the comment.
        date_posted (datetime): The date and time the comment was posted.
        user_id (int): The foreign key of the user who wrote the comment.
        post_id (int): The foreign key of the post that was commented on.
        author (relationship): A relationship to the user who wrote the comment.
    """
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    post_id = db.Column(db.Integer, db.ForeignKey('post.id'), nullable=False)

    # Relationship to access the user who wrote the comment
    author = db.relationship('User', backref='comments', lazy=True)

    def __repr__(self):
        return f"Comment('{self.content}', '{self.date_posted}')"