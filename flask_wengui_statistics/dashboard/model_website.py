"""Database models."""
from .. import db


class Website(db.Model):
    """Website model."""

    __tablename__ = "website"
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(10), nullable=False, unique=True)

    point = db.Column(db.Integer)
    # submits = db.relationship(
    #     'Submit', backref='video_type', lazy=True)

    category_id = db.Column(db.Integer, db.ForeignKey(
        'category.id'), nullable=False)

    def __repr__(self):
        return "<Website {}>".format(self.name)
