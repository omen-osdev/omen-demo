import asyncio
import functools
import time

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for, Response, current_app
)
from werkzeug.security import check_password_hash, generate_password_hash

from .models import InstanceModel
from .instance import create_instance
from app import INSTANCE_LIFETIME

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
        instance = InstanceModel(port, int(time.time()))
        session["instance_key"] = instance
        
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop = asyncio.get_event_loop()
        loop.run_in_executor(None, loop.run_until_complete, instance.check_and_shutdown(INSTANCE_LIFETIME * 60))

    return render_template("instance.html", timeout=INSTANCE_LIFETIME*60*1000)
