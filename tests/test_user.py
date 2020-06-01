import pytest
from sqlalchemy.exc import IntegrityError

from twydter_app.models import User


def test_user_base(session):
    assert session.query(User).count() == 0

    user = User(username='foo', email='bar@baz.nl')
    session.add(user)
    session.commit()

    assert session.query(User).count() == 1

    session.delete(user)
    session.commit()
    assert session.query(User).count() == 0


def test_user_dupe_exception(session):
    with pytest.raises(IntegrityError):
        session.add_all(
            [
                User(username='foo', email='bar@baz.nl'),
                User(username='foo', email='bar@baz.nl')
            ]
        )
        session.commit()


def test_user_empty_exception(session):
    with pytest.raises(IntegrityError):
        session.add(User())
        session.commit()


def test_user_password(session):
    user = User(username='foo', email='bar@baz.nl')
    session.add(user)
    session.commit()
    password = 'password'

    user.set_password(password)

    # Sanity check: cipher != plaintext
    assert user.password_hash != password

    assert user.check_password(password)

    new_password = 'newpassword'
    user.set_password(new_password)
    assert not user.check_password(password)
    assert user.check_password(new_password)
