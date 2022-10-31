"""Database models."""
from .. import db


class Category(db.Model):
    """Category model."""

    __tablename__ = "category"
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(10), nullable=False, unique=True)

    # point = db.Column(db.Integer)

    submits = db.relationship(
        'VideoSubmit', backref='category', lazy=True)

    videos = db.relationship(
        'Video', backref='category', lazy=True)

    musics = db.relationship(
        'Music', backref='category', lazy=True)

    streams = db.relationship(
        'Stream', backref='category', lazy=True)

    websites = db.relationship(
        'Website', backref='category', lazy=True)

    def __repr__(self):
        return "<Category {}>".format(self.name)
