from flask import Flask, Blueprint
from .namespaces import main_ns, user_ns
from .config import configure_namespaces

API_VERSION="v1"
def create_app() -> Flask:
    """
    Creates and returns a flask application.

    Returns:
        app: Our main flask app with our api and blueprints linked.
    """

    app = Flask(__name__, instance_relative_config=False)
    blueprint = Blueprint("Home", __name__)

    configure_namespaces(blueprint, main_ns, user_ns)

    app.register_blueprint(blueprint, url_prefix=f"/api/{API_VERSION}")

    return app
