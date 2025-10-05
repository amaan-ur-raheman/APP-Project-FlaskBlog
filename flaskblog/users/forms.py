from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User
from flask_login import current_user



class RegistrationForm(FlaskForm):
    """
    Form for user registration.

    Attributes:
        username (StringField): The user's chosen username.
        email (StringField): The user's email address.
        password (PasswordField): The user's chosen password.
        confirm_password (PasswordField): Password confirmation field.
        submit (SubmitField): The button to submit the form.
    """
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField(
        "email",
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Sign Up")

    def validate_username(self, username):
        """
        Validates that the username is not already taken.

        Args:
            username (StringField): The username field to validate.

        Raises:
            ValidationError: If the username is already in use.
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That username is taken. Please choose a different one.")

    def validate_email(self, email):
        """
        Validates that the email is not already registered.

        Args:
            email (StringField): The email field to validate.

        Raises:
            ValidationError: If the email is already in use.
        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is taken. Please choose a different one.")


class LoginForm(FlaskForm):
    """
    Form for user login.

    Attributes:
        email (StringField): The user's email address.
        password (PasswordField): The user's password.
        remember (BooleanField): A checkbox to remember the user's session.
        submit (SubmitField): The button to submit the form.
    """
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()]
    )
    remember = BooleanField("Remember Me")
    submit = SubmitField("Login")


class UpdateAccountForm(FlaskForm):
    """
    Form for updating a user's account information.

    Attributes:
        username (StringField): The user's new username.
        email (StringField): The user's new email address.
        picture (FileField): The user's new profile picture.
        submit (SubmitField): The button to submit the form.
    """
    username = StringField(
        "Username",
        validators=[DataRequired(), Length(min=2, max=20)]
    )
    email = StringField(
        "Email",
        validators=[DataRequired(), Email()]
    )
    picture = FileField(
        "Update Profile Picture",
          validators=[FileAllowed(['jpg', 'png'])]
    )
    submit = SubmitField("Update")

    def validate_username(self, username):
        """
        Validates that the new username is not already taken by another user.

        Args:
            username (StringField): The username field to validate.

        Raises:
            ValidationError: If the new username is already in use.
        """
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("This username is taken. Please choose a different one")

    def validate_email(self, email):
        """
        Validates that the new email is not already registered by another user.

        Args:
            email (StringField): The email field to validate.

        Raises:
            ValidationError: If the new email is already in use.
        """
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("This email is taken. Please choose a different one")


class RequestResetForm(FlaskForm):
    """
    Form for requesting a password reset email.

    Attributes:
        email (StringField): The email address of the account to reset.
        submit (SubmitField): The button to request the reset.
    """
    email = StringField("Email", validators=[DataRequired(), Email()])
    submit = SubmitField("Request Password Reset")

    def validate_email(self, email):
        """
        Validates that an account exists with the given email address.

        Args:
            email (StringField): The email field to validate.

        Raises:
            ValidationError: If no user with the given email is found.
        """
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            raise ValidationError("There is no account with that email. You must register first.")


class ResetPasswordForm(FlaskForm):
    """
    Form for resetting a user's password.

    Attributes:
        password (PasswordField): The new password.
        confirm_password (PasswordField): Confirmation of the new password.
        submit (SubmitField): The button to reset the password.
    """
    password = PasswordField("Password", validators=[DataRequired()])
    confirm_password = PasswordField(
        "Confirm Password",
        validators=[DataRequired(), EqualTo("password")]
    )
    submit = SubmitField("Reset Password")