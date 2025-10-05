from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    """
    Form for creating and updating a blog post.

    Attributes:
        title (StringField): The title of the post, which is a required field.
        content (TextAreaField): The content of the post, which is a required field.
        submit (SubmitField): The button to submit the form.
    """
    title = StringField("Title", validators=[DataRequired()])
    content = TextAreaField("Content", validators=[DataRequired()])
    submit = SubmitField("Post")


class CommentForm(FlaskForm):
    """
    Form for submitting a comment on a blog post.

    Attributes:
        content (TextAreaField): The content of the comment, which is a required field.
        submit (SubmitField): The button to submit the comment.
    """
    content = TextAreaField("Comment", validators=[DataRequired()])
    submit = SubmitField("Post Comment")