from flask import Flask
import os
from flask_smorest import Api
from flask_cors import CORS

from db import db
from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint

from resources.user import blp as UserBlueprint


def create_app(db_url=None):
    
    app = Flask(__name__)
    
    CORS(app)
    
    
    app.config["PROPAGATE_EXCEPTIONS"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    # just tell flask smorest where the root of api is
    app.config["OPENAPI_URL_PREFIX"] = "/"
    # use swagger to use documentation
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    # connect flask-smorest extension to flask app
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    
    api = Api(app)
    
    with app.app_context():
        db.create_all()
    
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(UserBlueprint)

    return app