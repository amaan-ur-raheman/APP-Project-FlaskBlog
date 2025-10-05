from flaskblog.models import User, Post
from flask import render_template, url_for, flash, redirect, request, Blueprint
from flaskblog.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from flaskblog import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog.users.utils import send_reset_email, save_picture



users = Blueprint("users", __name__)

@users.route("/register", methods=["POST", "GET"])
def register():
    """
    Handles user registration.

    If the user is already authenticated, they are redirected to the home page.
    Otherwise, it processes the registration form. On successful submission,
    a new user is created and saved to the database.

    Returns:
        A rendered registration template, a redirect to the home page when the user is already
        authenticated, or a redirect to the login page after successful registration.
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f"Your account has been created! You are now able to log in ", "success")
        return redirect(url_for("users.login"))
    return render_template('register.html', title="Register", form=form)


@users.route("/login", methods=["POST", "GET"])
def login():
    """
    Handles user login.

    If the user is already authenticated, they are redirected to the home page.
    Otherwise, it processes the login form. On successful validation, the user
    is logged in and redirected to the home page or their intended destination.

    Returns:
        A rendered login template or a redirect to the home page.
    """
    if current_user.is_authenticated:
        return redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for("main.home"))
        else:
            flash("Login Unsuccessful! Please check email and password", "danger")
    return render_template('login.html', title="Login", form=form)


@users.route("/logout")
def logout():
    """
    Logs out the current user.

    Returns:
        A redirect to the home page.
    """
    logout_user()
    return redirect(url_for("main.home"))


@users.route("/account", methods=["POST", "GET"])
@login_required
def account():
    """
    Handles user account management.

    Allows authenticated users to update their username, email, and profile picture.

    Returns:
        A rendered account template with the user's information.
    """
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash("Your account has been updated", "success")
        return redirect(url_for("users.account"))
    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for("static", filename="/profile_pics/" + current_user.image_file)
    return render_template("account.html", title="Account", image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    """
    Displays all posts by a specific user.

    Args:
        username (str): The username of the user whose posts are to be displayed.

    Returns:
        A rendered template showing a paginated list of the user's posts.
    """
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
            .order_by(Post.date.desc())\
            .paginate(page=page, per_page=5)
    return render_template('user_posts.html', title='Post By ' + user.username, posts=posts, user=user)


@users.route("/reset_password", methods=["POST", "GET"])
def reset_request():
    """
    Handles the request for a password reset email.

    If the user is authenticated, they are redirected to the home page.
    Otherwise, it processes a form where users can enter their email to
    receive a password reset link.

    Returns:
        A rendered password reset request template, a redirect to the home page when the user is
        already authenticated, or a redirect to the login page after sending the reset email.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    form = RequestResetForm()

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password", "info")
        return redirect(url_for("users.login"))

    return render_template("reset_request.html", form=form, title="Reset Password")


@users.route("/reset_password/<token>", methods=["POST", "GET"])
def reset_token(token):
    """
    Handles the password reset using a token.

    If the user is authenticated, they are redirected to the home page.
    Verifies the provided token and, if valid, allows the user to set a
    new password.

    Args:
        token (str): The password reset token from the email link.

    Returns:
        A rendered password reset form, a redirect to the login page after a successful reset,
        a redirect to the home page if the user is already authenticated, or a redirect back to
        the password reset request page when the token is invalid or expired.
    """
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    
    user = User.verify_reset_token(token)

    if user is None:
        flash("That is an invalid or expired token", "warning")
        return redirect(url_for('users.reset_request'))
    
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
        user.password = hashed_password
        db.session.commit()
        flash(f"Your password has been updated! You are now able to log in ", "success")
        return redirect(url_for("users.login"))
    return render_template("reset_token.html", title="Reset Password", form=form)