from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_babel import Babel

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///jaikishanjaijawan.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['BABEL_DEFAULT_LOCALE'] = 'en'

db = SQLAlchemy(app)
login_manager = LoginManager(app)
babel = Babel(app)

# Import routes
from routes import main_routes, auth_routes, market_routes, chatbot_routes, forum_routes, admin_routes, weather_routes

app.register_blueprint(main_routes)
app.register_blueprint(auth_routes)
app.register_blueprint(market_routes)
app.register_blueprint(chatbot_routes)
app.register_blueprint(forum_routes)
app.register_blueprint(admin_routes)
app.register_blueprint(weather_routes)

if __name__ == '__main__':
    app.run(debug=True)
