import pytest
from sqlalchemy.exc import IntegrityError

from twydter_app.models import Post, User


def test_post_base(session):
    assert session.query(Post).count() == 0

    post = Post(body='foo')
    session.add(post)
    session.commit()

    assert session.query(Post).count() == 1

    session.delete(post)
    session.commit()
    assert session.query(Post).count() == 0


def test_post_empty_exception(session):
    with pytest.raises(IntegrityError):
        session.add(Post())
        session.commit()


def test_post_user_relation(session):
    user1 = User(username='foo', email='1@2.nl')
    user2 = User(username='bar', email='3@4.nl')
    session.add_all([user1, user2])
    session.commit()

    post1 = Post(author=user1, body='byfoo')
    post2 = Post(author=user1, body='byfoo2')
    post3 = Post(author=user2, body='bybar')
    session.add_all([post1, post2, post3])
    session.commit()

    assert session.query(Post).count() == 3
    assert len(user1.posts.all()) == 2
    assert len(user2.posts.all()) == 1

    assert set(user1.posts.all()) == set([post1, post2])
    assert user2.posts.all() == [post3]

    assert post3 not in user1.posts

    session.delete(user1)
    session.commit()

    # Don't cascade the deletion, keep the posts but delete association with user 1
    assert session.query(Post).count() == 3

    assert not (post1.author or post2.author)
