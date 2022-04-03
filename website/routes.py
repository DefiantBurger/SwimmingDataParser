from flask import Blueprint, render_template

from dir_routes.times import time_routes

all_routes = Blueprint('all_routes', __name__, template_folder='templates')
all_routes.register_blueprint(time_routes, url_prefix='/times')


@all_routes.route("/")
def home():
    return render_template("index.html")