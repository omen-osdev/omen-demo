import os

from flask import Flask, render_template

from instance import *

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
    )

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

    # use test_config here


    @app.route('/')
    def home():
        return render_template("index.html")

    return app
    
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
