"""Database models."""
from datetime import datetime
# from werkzeug.security import check_password_hash, generate_password_hash
from .. import db
# from .account_type import AccountType


class Theme(db.Model):
    """Theme model."""

    __tablename__ = "theme"
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(10), nullable=False, unique=True)

    # Data Type: Accepts one of the following:
    # String(size), Text, DateTime, Float, Boolean, PickleType, or LargeBinary.Integer
    accounts = db.relationship(
        'Account', backref='theme', lazy=True)

    def __repr__(self):
        return "<Theme {}>".format(self.name)
