import os

from flask import Flask, render_template, request
from flask_turnstile import Turnstile
import requests

def verify(request):
    data = {
        "secret": app.config["TURNSTILE_SECRET_KEY"],
        "response": request.form.get('cf-turnstile-response'),
        "remoteip": request.headers.get("CF-Connecting-IP")
    }
    print("Request form data: ", flush=True)
    #print inmutablemultidict
    for key in request.form.keys():
        print(key, request.form[key], flush=True)
    print("Request headers: ", flush=True)
    print(request.headers, flush=True)
    print("Data: ", flush=True)
    print(data, flush=True)

    response = requests.post("https://challenges.cloudflare.com/turnstile/v0/siteverify", data=data)
    return response.json()["success"] if response.status_code == 200 else False

def create_app(test_config=None):
    global app
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY=os.environ.get('SECRET_KEY', 'dev'),
        TURNSTILE_SECRET_KEY=os.environ.get('TURNSTILE_SECRET_KEY', None),
        DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
    )

    if app.config["TURNSTILE_SECRET_KEY"] is None:
        raise ValueError("TURNSTILE_SECRET_KEY is not set")

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


    @app.route('/')
    def home():
        return render_template("index.html")
    
    @app.route('/run', methods=["POST"])
    #call verify function
    def run():
        if verify(request):
            return "You are not a robot!"
        else:
            return "You are a robot!"

    return app