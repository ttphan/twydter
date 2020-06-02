from flask import url_for
from flask_login import current_user

from tests.helper import check_status
from twydter_app.models import User

INVALID: bytes = b'Invalid username or password'
USERNAME = 'foo'
PASSWORD = 'bar'
EMAIL = '1@2.nl'


def test_login_200(client):
    assert check_status(client, url_for('auth.login')) == 200


def test_login_wrong_credentials(client, session):
    response = client.post(url_for('auth.login'), data=dict(
        username=USERNAME,
        password=PASSWORD,
    ))

    # Not redirected to the home page
    assert response.status_code == 200
    assert INVALID in response.data
    assert b'Hi, foo!' not in response.data


def test_login_successful(user, client, session):
    response = client.post(url_for('auth.login'), data=dict(
        username=USERNAME,
        password=PASSWORD,
    ))

    # Redirected successfully to the home page
    assert response.status_code == 302
    assert b'Invalid username or password' not in response.data

    response = client.post(url_for('auth.login'), follow_redirects=True, data=dict(
        username=USERNAME,
        password=PASSWORD,
    ))

    assert bytes(f'Hi, {USERNAME}!', encoding='utf8') in response.data
    assert b'Invalid username or password' not in response.data


def test_register_200(client):
    assert check_status(client, url_for('auth.register')) == 200


def test_register_invalid_email(client, session):
    response = client.post(url_for('auth.register'), data=dict(
        username=USERNAME,
        email='invalidemail',
        password=PASSWORD,
        confirm=PASSWORD
    ))

    # No redirect
    assert response.status_code == 200
    assert b'Invalid email address' in response.data

    assert session.query(User).count() == 0


def test_register_passwords_not_matching(client, session):
    response = client.post(url_for('auth.register'), data=dict(
        username=USERNAME,
        email=EMAIL,
        password='pass',
        confirm='differentpass'
    ))

    # No redirect
    assert response.status_code == 200
    assert b'Passwords must match' in response.data

    assert session.query(User).count() == 0


def test_register_duplicate(user, client, session):
    assert session.query(User).count() == 1

    response = client.post(url_for('auth.register'), data=dict(
        username=USERNAME,
        email=EMAIL+'x',
        password=PASSWORD,
        confirm=PASSWORD
    ))

    # No redirect
    assert response.status_code == 200
    assert b'Please use a different username' in response.data

    response = client.post(url_for('auth.register'), data=dict(
        username=USERNAME+'x',
        email=EMAIL,
        password=PASSWORD,
        confirm=PASSWORD
    ))

    # No redirect
    assert response.status_code == 200
    assert b'Please use a different email address' in response.data

    assert session.query(User).count() == 1


def test_register_successfully(client, session):
    assert session.query(User).count() == 0

    response = client.post(url_for('auth.register'), data=dict(
        username=USERNAME,
        email=EMAIL,
        password=PASSWORD,
        confirm=PASSWORD
    ))

    assert response.status_code == 302

    response = client.post(url_for('auth.register'), follow_redirects=True, data=dict(
        username=USERNAME,
        email=EMAIL,
        password=PASSWORD,
        confirm=PASSWORD
    ))

    assert b'Congratulations, welcome to Twydter' in response.data

    assert session.query(User).count() == 1


def test_login_required(user, client, session):
    assert client.get(url_for('main.index')).status_code == 302
    assert b'Please log in to access this page.' in client.get(url_for('main.index'), follow_redirects=True).data

    assert check_status(client, url_for('main.user', username='foo')) == 302
    assert b'Please log in to access this page.' in client.get(url_for('main.index'), follow_redirects=True).data

    client.post(url_for('auth.login'), data=dict(
        username=USERNAME,
        password=PASSWORD,
    ))

    # Logged in now, so no redirects
    assert check_status(client, url_for('main.index')) == 200
    assert check_status(client, url_for('main.user', username='foo')) == 200


def test_logout(user, logged_in, client, session):
    assert int(current_user.get_id()) == user.id
    client.get(url_for('auth.logout'), follow_redirects=True)
    assert not current_user.get_id()

