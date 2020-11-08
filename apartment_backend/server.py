from flask import Flask
from .addons import cors, db
from . import settings

from .endpoints.parse import bp as parse_bp
from .endpoints.apart import bp as apart_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(settings)

    app.register_blueprint(parse_bp)
    app.register_blueprint(apart_bp)

    cors.init_app(app)

    return app


wsgi_app = create_app()

if __name__ == '__main__':
    debuging = settings.FLASK_ENV=='development'
    wsgi_app.run(debug=debuging)
