"""Database models."""
from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import check_password_hash, generate_password_hash
from .. import db
# from ..dashboard.model_submit_type import Category
# from sqlalchemy import Column
# from sqlalchemy import Integer
# from sqlalchemy import ForeignKey
# from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref


class Account(UserMixin, db.Model):
    """User account model."""

    __tablename__ = "account"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=False)
    email = db.Column(db.String(35), unique=True, nullable=False)
    # password = db.Column(
    #     db.String(200), primary_key=False, unique=False, nullable=False
    # )
    discord = db.Column(db.String(15), nullable=True, unique=False)
    farm = db.Column(db.String(25), nullable=True, unique=False)
    twitter = db.Column(db.String(25), nullable=True, unique=False)
    gettr = db.Column(db.String(15), nullable=True, unique=False)

    # Data Type: Accepts one of the following:
    # String(size), Text, DateTime, Float, Boolean, PickleType, or LargeBinary.Integer
    # datetime.now().strftime("%m-%d-%Y %H:%M:%S")

    created_on = db.Column(db.DateTime, index=False, unique=False,
                           nullable=True, default=datetime.now())
    last_login = db.Column(db.DateTime, index=False,
                           unique=False, nullable=True)

    ###################################################################
    theme_id = db.Column(db.Integer, db.ForeignKey(
        'theme.id'), nullable=False)

    account_status_id = db.Column(db.Integer, db.ForeignKey(
        'account_status.id'), nullable=False)

    account_type_id = db.Column(db.Integer, db.ForeignKey(
        'account_type.id'), nullable=False)

    ###################################################################
    team_id = db.Column(db.Integer, db.ForeignKey('account.id'), index=True)

    team_name = db.Column(db.String(25), nullable=True, unique=False)

    # N001 每一个账号有多个submits
    submits = db.relationship(
        'VideoSubmit', backref='account', lazy=True)

    members = db.relationship(
        'Account', backref=backref('member', remote_side='Account.id'))
    ###################################################################

    # N003- 每一个账号有多个【Video操作】表项
    # 222-B, YES
    operations = db.relationship(
        'AccountOperation', backref='account', lazy=True)

    password = db.Column(
        db.String(200), primary_key=False, unique=False, nullable=False
    )

    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method="sha256")

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def datetime_serialize(self, value):
        # """Deserialize datetime object into string form for JSON processing."""
        if value is None:
            return None
        return value.strftime("%Y-%m-%d,")+value.strftime("%H:%M:%S")

    # for error in form.password.errors
    @property
    def serialize(self):
        # Return object data in easily serializable format
        members = [{'id': member.id, 'name': member.name} for member in self.members]
        return {'id': self.id,
                'name': self.name,
                'members': members,
                'last_login': self.datetime_serialize(self.last_login),
                'created_on': self.datetime_serialize(self.created_on)}

    def __repr__(self):
        return "<Account {}>".format(self.name)
