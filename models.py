from app import db
from flask_login import UserMixin
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User {self.username}>"

class CropInfo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    sowing_tips = db.Column(db.Text)
    pest_control = db.Column(db.Text)
    seasonal_tips = db.Column(db.Text)

    def __repr__(self):
        return f"<CropInfo {self.name}>"

class MarketPrice(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    mandi = db.Column(db.String(100), index=True)
    crop = db.Column(db.String(100))
    variety = db.Column(db.String(100))
    arrival_date = db.Column(db.Date, index=True)
    min_price = db.Column(db.Float)
    max_price = db.Column(db.Float)
    modal_price = db.Column(db.Float)

    def __repr__(self):
        return f"<MarketPrice mandi={self.mandi} crop={self.crop} arrival_date={self.arrival_date}>"

class ForumPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    replies = db.relationship('ForumReply', backref='post', lazy=True)

    def __repr__(self):
        return f"<ForumPost id={self.id} user_id={self.user_id}>"

class ForumReply(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    post_id = db.Column(db.Integer, db.ForeignKey('forum_post.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<ForumReply id={self.id} post_id={self.post_id} user_id={self.user_id}>"
