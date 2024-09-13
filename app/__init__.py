from datetime import timedelta
from mimetypes import init
import os

from flask import Flask, render_template, session
from flask_session import Session
from cachelib.simple import SimpleCache

INSTANCE_LIFETIME = 1 # Lifetime of each instance, in minutes

def create_app(test_config=None):
    """
    
    Create and configure an instance of the Flask application.

    :param test_config: dict, optional
        A dictionary containing the configuration for the application.
        If provided, this configuration will be used instead of the default
        values.
    :return: Flask
        The created Flask application
    
    """

    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
        SESSION_TYPE = 'cachelib',
        SESSION_SERIALIZATION_FORMAT = 'json',
        SESSION_CACHELIB = SimpleCache(threshold=500, default_timeout=300),
        SESSION_PERMANENT = False,
        PERMANENT_SESSION_LIFETIME = timedelta(minutes=INSTANCE_LIFETIME),
    )

    # TODO: Follow before deploying to prod: https://flask-session.readthedocs.io/en/latest/security.html
    # TODO: Consider using flask-talisman: https://github.com/wntrblm/flask-talisman
    # Start server-side sessions
    #TODO: Change to Redis
    Session(app)

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #TODO: Use test_config to set up the app for testing here

    from .instance import init_launcher
    init_launcher()    # Init the instance launcher #? Should this be done here? Maybe an HTTP Method should be used to start the instance
    # TODO: call cleanup_launcher in some sort of a cleanup function

    @app.route('/')
    def home():
        return render_template("index.html")

    from . import instance_page
    app.register_blueprint(instance_page.bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=5000)
