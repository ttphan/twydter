from twydter_app import create_app, extensions
from twydter_app.models import User, Post

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': extensions.db, 'User': User, 'Post': Post}