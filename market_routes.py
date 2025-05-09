from flask import Blueprint

bp = Blueprint('market_routes', __name__)

@bp.route('/market')
def market_home():
    return "Market Routes Placeholder"

from flask import render_template
from models import MarketPrice
from app import db

@bp.route('/market-prices/')
def market_prices():
    prices = MarketPrice.query.order_by(MarketPrice.arrival_date.desc()).limit(50).all()
    return render_template('market_prices.html', prices=prices)
