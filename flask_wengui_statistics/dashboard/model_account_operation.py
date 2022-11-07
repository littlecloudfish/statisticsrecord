"""Database models."""
from .. import db

"""Database models."""


class AccountOperation(db.Model):
    """AccountVideo操作模型."""
    __tablename__ = "account_operation"

    id = db.Column(db.Integer, primary_key=True)

    # N002 每一个表项基于一个Submitid
    # 111-A, YES
    submit_id = db.Column(db.Integer, db.ForeignKey(
        'submit.id'), nullable=True)

    # N003 每一个表项有对应的Accountid
    # 222-A, YES
    account_id = db.Column(db.Integer, db.ForeignKey(
        'account.id'), nullable=True)

    # N004 每一个表项有对应的Video操作id
    #  333-A, YES，Video操作
    operation_id = db.Column(db.Integer, db.ForeignKey(
        'operation.id'), nullable=True)

    # N005 每一个表项在特定Account和特定操作的基础上产生一个Point
    point = db.Column(db.Integer)

    def __repr__(self):
        return "<AccountVideo操作模型 {}>".format('AccountOperation')

