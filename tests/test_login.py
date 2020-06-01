from flask import url_for

from twydter_app.models import User


def test_login(client, session):
    response = client.post(url_for('auth.login'), follow_redirects=True, data=dict(
        username='foo',
        password='bar',
    ))

    assert b'Invalid username or password' in response.data

    user = User(username='foo', email='e@mail.com')
    user.set_password('bar')

    session.add(user)
    session.commit()

    response = client.post(url_for('auth.login'), follow_redirects=True, data=dict(
        username='foo',
        password='bar',
    ))
    assert b'Invalid username or password' not in response.data