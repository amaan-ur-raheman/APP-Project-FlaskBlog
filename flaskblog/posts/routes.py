from flask import render_template, redirect, request, Blueprint, url_for, flash, abort
from flask_login import login_required, current_user
from flaskblog import db
from flaskblog.models import Post, Comment, Like
from flaskblog.posts.forms import PostForm, CommentForm

posts = Blueprint("posts", __name__)



@posts.route("/post/new", methods=["POST", "GET"])
@login_required
def new_post():
    """
    Renders the form to create a new post and handles form submission.

    If the form is submitted and valid, a new post is created and saved to the
    database. The user is then redirected to the home page.

    Returns:
        A rendered template for creating a new post or a redirect to the home page.
    """
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post have been created", "success")
        return redirect(url_for("main.home"))
    return render_template("create_post.html", title="New Post", form=form, legend="New Post")


@posts.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post(post_id):
    """
    Displays a single post and handles new comments.

    Args:
        post_id (int): The ID of the post to display.

    Returns:
        A rendered template of the post page, including its content and comments.
    """
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.content.data, user_id=current_user.id, post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been posted!', 'success')
        return redirect(url_for('posts.post', post_id=post.id))
    comments = Comment.query.filter_by(post_id=post.id).order_by(Comment.date_posted.desc()).all()
    return render_template('post.html', title=post.title, post=post, form=form, comments=comments)


@posts.route("/post/<int:post_id>/update", methods=["POST", "GET"])
@login_required
def update_post(post_id):
    """
    Renders the form to update an existing post and handles form submission.

    The user must be the author of the post to update it. If the form is
    submitted and valid, the post is updated in the database.

    Args:
        post_id (int): The ID of the post to update.

    Returns:
        A rendered template for updating a post or a redirect to the post page.
    """
    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash("Your post has been upadated!", "success")
        return redirect(url_for("posts.post", post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template("create_post.html", title="Update Post", form=form, legend="Update Post")


@posts.route("/post/<int:post_id>/delete", methods=["POST"])
@login_required
def delete_post(post_id):
    """
    Deletes a specific post from the database.

    The user must be the author of the post to delete it. This route only
    accepts POST requests.

    Args:
        post_id (int): The ID of the post to delete.

    Returns:
        A redirect to the home page after deleting the post.
    """
    post = Post.query.get_or_404(post_id)

    if post.author != current_user:
        abort(403)

    db.session.delete(post)
    db.session.commit()

    flash("Your post has been deleted!", "success")
    return redirect(url_for("main.home"))


@posts.route("/post/<int:post_id>/like", methods=['POST'])
@login_required
def like_post(post_id):
    """
    Toggles the like status of a post for the current user.

    If the user has already liked the post, the like is removed. Otherwise,
    a new like is added.

    Args:
        post_id (int): The ID of the post to like or dislike.

    Returns:
        A redirect to the post page.
    """
    post = Post.query.get_or_404(post_id)
    like = Like.query.filter_by(user_id=current_user.id, post_id=post_id).first()

    if like:
        # If the user already liked the post, remove the like
        db.session.delete(like)
        db.session.commit()
        flash('You disliked the post.', 'info')
    else:
        # Otherwise, add a new like
        new_like = Like(user_id=current_user.id, post_id=post_id)
        db.session.add(new_like)
        db.session.commit()
        flash('You liked the post!', 'success')

    return redirect(url_for('posts.post', post_id=post_id))