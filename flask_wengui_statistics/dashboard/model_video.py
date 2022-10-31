"""Database models."""
from .. import db
from enum import IntEnum, unique

# class Category(db.Model):

# 	__tablename__ = "submit_type"(A)
#     	submits = db.relationship('Submit', backref='submit_type'(A), lazy=True)

#     	videos = db.relationship('VideoType', backref='submit_type'(A), lazy=True)

#     	musics = db.relationship('MusicType', backref='submit_type'(A), lazy=True)


# class Submit(db.Model):

#     __tablename__ = "submit"
#     submit_type_id = db.Column(db.Integer, db.ForeignKey(
#     	'submit_type(A).id'), nullable=False)

"""Database models."""


@unique
class E_VIDEO_TYPE (IntEnum):
    MIC_VIDEO = 0
    SIM_VIDEO = 1
    REF_VIDEO = 2
    CRT_VIDEO = 3
    RCD_VIDEO = 4
    UGT_VIDEO = 5
    CHT_VIDEO = 6


class Video(db.Model):
    """Video type model."""

    __tablename__ = "video"
    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(10), nullable=False, unique=True)

    point = db.Column(db.Integer)
    # submits = db.relationship(
    #     'Submit', backref='video_type', lazy=True)

    category_id = db.Column(db.Integer, db.ForeignKey(
        'category.id'), nullable=False)

    # 444-B, YES ???
    operations = db.relationship(
        'Operation', backref='video', lazy=True)

    def __repr__(self):
        return "<Video type {}>".format(self.name)
