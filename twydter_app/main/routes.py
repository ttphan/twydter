from flask import Blueprint, flash, redirect, url_for
from flask import render_template
from flask_login import login_required, current_user

from twydter_app.main.forms import PostForm
from twydter_app.models import User, Post
from twydter_app.extensions import db

main_bp = Blueprint('main', __name__)


@main_bp.route('/', methods=['GET', 'POST'])
@main_bp.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Post submitted!')

        # Post/redirect/get pattern
        return redirect(url_for('main.index'))

    posts = db.session.query(Post).all()

    return render_template('main/index.html', title='Home', form=form, posts=posts)


@main_bp.route('/user/<username>')
@login_required
def user(username):
    u = User.query.filter_by(username=username).first_or_404()

    return render_template('main/user.html', user=u, posts=u.posts)
