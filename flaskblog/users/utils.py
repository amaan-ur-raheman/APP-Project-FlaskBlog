import os
import secrets
from PIL import Image
from flask import url_for, current_app
from flask_mail import Message
from flaskblog import mail



def save_picture(form_picture):
    """
    Saves and resizes a user's profile picture.

    The function generates a random hex filename to prevent collisions, resizes
    the image to 125x125 pixels, and saves it to the `static/profile_pics`
    directory.

    Args:
        form_picture (FileStorage): The picture file uploaded by the user
                                    through the form.

    Returns:
        str: The filename of the saved picture.
    """
    random_hex = secrets.token_hex(8)
    _, file_extension = os.path.splitext(form_picture.filename)
    picture_filename = random_hex + file_extension
    picture_path = os.path.join(current_app.root_path, "static/profile_pics", picture_filename)

    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_filename


def send_reset_email(user):
    """
    Sends a password reset email to the specified user.

    The email contains a unique token that the user can use to reset their
    password.

    Args:
        user (User): The user object to whom the reset email will be sent.
    """
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender="noreply@demo.com", recipients=[user.email])
    msg.body = f"""To reset your passsword visit the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
"""
    mail.send(msg)