"""Database models."""
from .. import db

"""Database models."""


class Operation(db.Model):
    """Video操作模型."""
    __tablename__ = "operation"

    #    222
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(10), nullable=False, unique=True)

    weight = db.Column(db.Integer)

    # 444-A, YES ???
    video_id = db.Column(db.Integer, db.ForeignKey(
        'video.id'), nullable=False)

    # N004 每一个？？？
    #  333-B, YES，Video操作
    operations = db.relationship(
        'AccountOperation', backref='operation', lazy=True)

    @property
    def serialize(self):
        # Return object data in easily serializable format
        return {'id': self.id,
                'name': self.name,
                'weight': self.weight}

    def __repr__(self):
        return "<Video操作 {}>".format(self.name)
