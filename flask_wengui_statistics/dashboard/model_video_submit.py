"""Database models."""
from enum import IntEnum, unique

from datetime import datetime
from .. import db


@unique
class E_SUBMIT_TYPE(IntEnum):
    VIDEO = 0
    MUSIC = 1
    STREAM = 2
    WEBSITE = 3


class VideoSubmit(db.Model):
    """VideoSubmit model."""

    __tablename__ = "submit"
    id = db.Column(db.Integer, primary_key=True)

    category_id = db.Column(db.Integer, db.ForeignKey(
        'category.id'), nullable=False)

    title = db.Column(db.String(50), nullable=False, unique=False)

    global_code = db.Column(db.String(10), nullable=False, unique=True)
    team_code = db.Column(db.String(10), nullable=True, unique=True)

    link = db.Column(db.String(100), nullable=True)
    disk_link = db.Column(db.String(100), nullable=True)

    # point = db.Column(db.Integer, default=0)
    length = db.Column(db.Integer)

    comment = db.Column(db.Text, nullable=True)

    submit_status_id = db.Column(db.Integer, db.ForeignKey(
        'submit_status.id'), nullable=False)

    # team account id
    team_id = db.Column(db.Integer, db.ForeignKey(
        'account.id'), nullable=False)

    # N002- 每一个Submit产生多个【Account-Video操作】表项
    #  111-B, YES
    # ************************ 多对多 AccountOperation 表的submit_id  ************************** #
    account_operations = db.relationship(
        'AccountOperation', backref='submit', lazy=True)

    created_on = db.Column(db.DateTime, index=False, unique=False,
                           nullable=True, default=datetime.now)

    def __repr__(self):
        return "<VideoSubmit {}>".format(self.title)
