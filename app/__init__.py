import config
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import os



mail = Mail()
db = SQLAlchemy()


def create_app(config_class=config.Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    mail.init_app(app)
    
    from app.routes import main
    app.register_blueprint(main)

    with app.app_context():
        from . import models, routes, forms
        db.create_all()
    return app