from flask import Blueprint, render_template

errors = Blueprint("errors", __name__)



@errors.app_errorhandler(404)
def error_404(error):
    """
    Handles 404 Not Found errors.

    Renders a custom 404 error page.

    Args:
        error: The error object.

    Returns:
        A tuple containing the rendered 404 template and the 404 status code.
    """
    return render_template("errors/404.html"), 404



@errors.app_errorhandler(403)
def error_403(error):
    """
    Handles 403 Forbidden errors.

    Renders a custom 403 error page.

    Args:
        error: The error object.

    Returns:
        A tuple containing the rendered 403 template and the 403 status code.
    """
    return render_template("errors/403.html"), 403



@errors.app_errorhandler(500)
def error_500(error):
    """
    Handles 500 Internal Server Error errors.

    Renders a custom 500 error page.

    Args:
        error: The error object.

    Returns:
        A tuple containing the rendered 500 template and the 500 status code.
    """
    return render_template("errors/500.html"), 500