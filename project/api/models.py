import datetime

from project import db, bcrypt


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    active = db.Column(db.Boolean, default=True, nullable=False)
#   admin = db.Column(db.Boolean, default=False, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)

    def __init__(self, username, email, password, created_at=datetime.datetime.utcnow()):
        self.username = username
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode()
        self.created_at = created_at
