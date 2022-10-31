"""Database models."""
from datetime import datetime
# from werkzeug.security import check_password_hash, generate_password_hash
from .. import db
# from .account_type import AccountType


class AccountStatus(db.Model):
    """Account Status model."""

    __tablename__ = "account_status"
    id = db.Column(db.Integer, primary_key=True)
    # nullable=False, unique=True, autoincrement=True
    # image_id = db.Column(db.Integer, db.ForeignKey('images.id', onupdate='CASCADE', ondelete='CASCADE'))

    name = db.Column(db.String(10), nullable=False, unique=True)

    # Data Type: Accepts one of the following:
    # String(size), Text, DateTime, Float, Boolean, PickleType, or LargeBinary.Integer
    accounts = db.relationship(
        'Account', backref='account_status', lazy=True)

    def __repr__(self):
        return "<Account Status {}>".format(self.name)
