from flask import Blueprint

bp = Blueprint('admin_routes', __name__)

@bp.route('/admin')
def admin_home():
    return "Admin Routes Placeholder"
