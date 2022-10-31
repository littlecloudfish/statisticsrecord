"""Database models."""
from .. import db


class VideoSubmitStatus(db.Model):
    """Video Submit Status model."""

    __tablename__ = "submit_status"
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(10), nullable=False, unique=True)

    submits = db.relationship(
        'VideoSubmit', backref='submit_status', lazy=True)

    def __repr__(self):
        return "<Video Submit Status {}>".format(self.name)
