from flask import render_template

from twydter import app
from twydter.forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = {'username': 'Foo'}
    posts = [
        {
            'author': {'username': 'Bar'},
            'body': 'Lorem'
        },
        {
            'author': {'username': 'Baz'},
            'body': 'Ipsum'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign up', form=form)