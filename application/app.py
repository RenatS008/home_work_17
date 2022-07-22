from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy


db = SQLAlchemy()


def create_app():

    app = Flask(__name__)
    app.config.from_object('config.Config')
    db.init_app(app)

    with app.app_context():
        api = Api(app)
        app.config['api'] = api

        from application import views  # noqa

        return app

