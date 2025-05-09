from flask import Blueprint

bp = Blueprint('forum_routes', __name__)

@bp.route('/forum')
def forum_home():
    return "Forum Routes Placeholder"
