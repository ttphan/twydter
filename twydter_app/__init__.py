import os
import logging
from logging.handlers import RotatingFileHandler

from flask import Flask

from twydter_app.main.routes import main_bp
from twydter_app.auth.routes import auth_bp
from twydter_app.errors.routes import errors_bp
from config import Config

from twydter_app.extensions import *


def create_app(config_class=Config):
    """
    Application factory to initialize Flask app.
    Can be supplied with an optional config object, useful for testing
    :param config_class: Config object detailing initialization parameters, for example database location and type
    :return: Fully initialized Flask object
    """
    app = Flask(__name__)
    app.config.from_object(config_class)

    if not app.debug:
        logger = logging.getLogger('app_logger')
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/twydter.log', maxBytes=10240, backupCount=10)

        file_handler.setFormatter(
            logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
        )
        file_handler.setLevel(logging.INFO)
        logger.addHandler(file_handler)

        logger.setLevel(logging.INFO)
        logger.info('Twydter startup')

    init_extensions(app)
    register_blueprints(app)

    return app


def init_extensions(app):
    """
    Initialize Flask extensions, which are accessible externally to avoid circular imports
    :param app: Flask object
    """
    logger = logging.getLogger('app_logger')

    logger.info('Initializing database')
    db.init_app(app)

    logger.info('Initializing database migration')
    migrate.init_app(app, db)

    logger.info('Initializing login manager')
    login.init_app(app)

    logger.info('Initializing Bootstrap')
    bootstrap.init_app(app)


def register_blueprints(app):
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(main_bp)
    app.register_blueprint(errors_bp)
