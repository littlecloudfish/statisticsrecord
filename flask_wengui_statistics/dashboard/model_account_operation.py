"""Database models."""
from .. import db

"""Database models."""


class AccountOperation(db.Model):
    """账号Video操作模型."""
    __tablename__ = "account_operation"

    id = db.Column(db.Integer, primary_key=True)

    # N002 每一个表项基于一个提交id
    # 111-A, YES
    submit_id = db.Column(db.Integer, db.ForeignKey(
        'submit.id'), nullable=True)

    # N003 每一个表项有对应的账号id
    # 222-A, YES
    account_id = db.Column(db.Integer, db.ForeignKey(
        'account.id'), nullable=True)

    # N004 每一个表项有对应的Video操作id
    #  333-A, YES，Video操作
    operation_id = db.Column(db.Integer, db.ForeignKey(
        'operation.id'), nullable=True)

    # N005 每一个表项在特定账号和特定操作的基础上产生一个积分
    point = db.Column(db.Integer)

    def __repr__(self):
        return "<账号Video操作模型 {}>".format('AccountOperation')

