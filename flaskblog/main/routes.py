from flask import render_template, Blueprint, request
from flaskblog.models import Post

main = Blueprint("main", __name__)

@main.route("/")
@main.route("/home")
def home():
    """
    Renders the home page with a paginated list of blog posts.

    The posts are ordered by date in descending order. The current page number
    is retrieved from the request arguments.

    Returns:
        A rendered template of the home page.
    """
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date.desc()).paginate(page=page, per_page=5)
    return render_template("home.html", posts=posts)


@main.route("/about")
def about():
    """
    Renders the about page.

    Returns:
        A rendered template of the about page with the title "About".
    """
    return render_template("about.html", title="About")