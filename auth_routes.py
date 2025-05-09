from flask import Blueprint

bp = Blueprint('auth_routes', __name__)

@bp.route('/login')
def login():
    return "Auth Routes Placeholder"
