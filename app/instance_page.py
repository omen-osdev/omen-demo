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


@bp.route("/", methods=["GET"])
def launch_instance():
    try:
        if session.get("instance_key", None) is None:
            current_app.session_interface.regenerate(session)
            port = create_instance()
    
            if port == -1:
                return render_template("error.html", error="Unable to create a new instance")
            instance = InstanceModel(port, int(time.time()))
            session["instance_key"] = instance
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop = asyncio.get_event_loop()
            loop.run_in_executor(
                    None,
                    loop.run_until_complete,
                    instance.check_and_shutdown(INSTANCE_LIFETIME * 60)
            )

            return render_template("instance.html")
        else:
            return render_template("error.html", error="You already have an instance running, please close it before launching a new one.")
            # TODO:
            # Add a button to close the instance
            # *OR*
            # just redirect to the original instance
    except Exception as e:
            return render_template("error.html", error=str(e))
