"""Database models."""
from datetime import datetime
# from werkzeug.security import check_password_hash, generate_password_hash
from .. import db
# from .account_type import AccountType


class WhiteIP(db.Model):
    """White list model."""

    __tablename__ = "ip_white"
    id = db.Column(db.Integer, primary_key=True)

    # 192.168.123.333
    ip = db.Column(db.String(16), nullable=False, unique=True)

    note = db.Column(db.String(35), nullable=True)

    def __repr__(self):
        return "<IP(white): {}>".format(self.ip)
