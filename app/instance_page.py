import functools
import time

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Response, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash

from .models import InstanceModel
from .instance import create_instance

bp = Blueprint("instance_page", __name__, url_prefix="/instance")

# Note: Please docker kill <id> manually for now :)
@bp.route("/", methods=["GET"])
def launch_instance():
    # Make sure that we can reach here only after passing the captcha
    if session.get("instance_key", None) is None:
        current_app.session_interface.regenerate(session)   # Protection against session fixation attacks
        port = create_instance()
        if port == -1:
            return "Could not create an instance!"
        session["instance_key"] = InstanceModel(port, int(time.time()))
        return "Welcome! A New Instance Has Been Launched For You!"
    else:
        return str(session["instance_key"].port) + " " + str(session["instance_key"].startup_time)
