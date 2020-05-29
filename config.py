import os
basedir = os.path.abspath(os.path.dirname(__name__))

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_to_be_determined'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URI') or f"sqlite:///{os.path.join(basedir, 'twydter_app.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False