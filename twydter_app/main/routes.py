from flask import Blueprint
from flask import render_template
from flask_login import login_required
from twydter_app.models import User

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
@main_bp.route('/index')
@login_required
def index():
    return render_template('main/index.html', title='Home')


@main_bp.route('/user/<username>')
@login_required
def user(username):
    u = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': u, 'body': 'Test post #1'},
        {'author': u, 'body': 'Test post #2'}
    ]

    return render_template('main/user.html', user=u, posts=posts)