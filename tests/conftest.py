import pytest

from twydter_app import create_app, extensions
from config import Config


@pytest.fixture(scope='session')
def app(request):
    """
    Session-wide test `Flask` application.
    """
    config = Config()
    config.SQLALCHEMY_DATABASE_URI = 'sqlite:///'
    config.PRESERVE_CONTEXT_ON_EXCEPTION = False
    config.TESTING = True

    app = create_app(config)

    with app.app_context():
        yield app


@pytest.fixture(scope='session')
def db(app, request):
    """
    Session-wide test database.
    """
    extensions.db.create_all()
    yield extensions.db
    extensions.db.drop_all()


@pytest.fixture(scope='function')
def session(db, request):
    """
    Creates a new database session for a test.
    """
    connection = db.engine.connect()
    transaction = connection.begin()

    options = dict(bind=connection, binds={})
    session = db.create_scoped_session(options=options)

    db.session = session

    yield session

    transaction.rollback()
    connection.close()
    session.remove()
