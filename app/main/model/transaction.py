import uuid
import datetime
import logging
from .. import db
from ..util.helper import convert_to_local_time


class Transaction(db.Model):
    __tablename__ = "transaction"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), nullable=False)
    wallet_id = db.Column(db.Integer, db.ForeignKey("wallet.id"), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    transacted_at = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    reference_id = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Transaction(reference_id={self.reference_id}, status={self.status})>"

    def serialize(self):
        transacted_at = convert_to_local_time(self.transacted_at)
        return {
            "id": self.public_id,
            "status": self.status,
            "transacted_at": transacted_at.isoformat() if self.transacted_at else None,
            "type": self.type,
            "amount": self.amount,
            "reference_id": self.reference_id,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()
    

    def view_wallet_transactions(self, wallet_id):
        transactions = Transaction.query.filter_by(wallet_id=wallet_id).all()
        if not transactions:
            return []
        return [transaction.serialize() for transaction in transactions]