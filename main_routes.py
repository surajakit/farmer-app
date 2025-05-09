from flask import Blueprint

bp = Blueprint('main_routes', __name__)

@bp.route('/')
def index():
    return "Main Routes Placeholder"
