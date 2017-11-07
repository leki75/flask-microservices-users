import os

from flask import Flask
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy


bcrypt = Bcrypt()
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)

    CORS(app)

    app_settings = os.getenv('APP_SETTINGS')
    app.config.from_object(app_settings)

    bcrypt.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)

    from project.api.views import users_blueprint
    app.register_blueprint(users_blueprint)

    return app
