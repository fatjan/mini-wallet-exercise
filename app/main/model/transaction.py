import uuid
import datetime
import logging
from .. import db
from ..util.helper import convert_to_local_time
from .wallet import Wallet


class Transaction(db.Model):
    __tablename__ = "transaction"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), nullable=False)
    wallet_id = db.Column(db.Integer, db.ForeignKey("wallet.id"), nullable=False)
    customer_id = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    transacted_at = db.Column(db.DateTime, nullable=False)
    type = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    reference_id = db.Column(db.String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"<Transaction(reference_id={self.reference_id}, status={self.status})>"

    def serialize(self):
        try:
            transacted_at = convert_to_local_time(self.transacted_at)
            return {
                "id": self.public_id,
                "status": self.status,
                "transacted_at": transacted_at.isoformat()
                if self.transacted_at
                else None,
                "type": self.type,
                "amount": self.amount,
                "reference_id": self.reference_id,
            }
        except Exception as e:
            logging.exception(
                "An error occurred while serializing transaction: %s", str(e)
            )
            return None

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
        except Exception as e:
            logging.exception("An error occurred while saving transaction: %s", str(e))
            return None

    def view_wallet_transactions(self, wallet_id):
        try:
            wallet_model = Wallet()
            wallet = wallet_model.get_wallet(wallet_id)
            transactions = Transaction.query.filter_by(wallet_id=wallet.id).all()
            if not transactions:
                return []
            return [transaction.serialize() for transaction in transactions]
        except Exception as e:
            logging.exception(
                "An error occurred while viewing wallet transactions: %s", str(e)
            )
            return None

    def deposit_serialized(self):
        try:
            transacted_at = convert_to_local_time(self.transacted_at)
            return {
                "id": self.public_id,
                "deposited_by": self.customer_id,
                "status": self.status,
                "deposited_at": transacted_at.isoformat()
                if self.transacted_at
                else None,
                "type": self.type,
                "amount": self.amount,
                "reference_id": self.reference_id,
            }
        except Exception as e:
            logging.exception("An error occurred while serializing deposit: %s", str(e))
            return None

    def update_wallet_balance(self, wallet_id, transaction_type, amount=0):
        try:
            wallet_model = Wallet()
            wallet = wallet_model.get_wallet(wallet_id)
            if not wallet:
                return None

            try:
                if transaction_type == "deposit":
                    updated_wallet = wallet_model.update_balance(wallet_id, "deposit", amount)
                else:
                    updated_wallet = wallet_model.update_balance(wallet_id, "withdraw", amount)
                
                if updated_wallet:
                    return updated_wallet.id
                else:
                    return None
            
            except Exception as e:
                logging.exception(
                    "An error occurred while updating wallet balance: %s", str(e)
                )
                return None

        except Exception as e:
            logging.exception(
                "An error occurred while updating wallet balance: %s", str(e)
            )
            return None

    def deposit_to_wallet(self, customer_id, wallet_id, amount, reference_id):
        try:
            ref_exist = self.check_reference(reference_id)
            if ref_exist:
                return None
            
            wallet_db_id = self.update_wallet_balance(wallet_id, "deposit", amount)     
            transaction = Transaction(
                public_id=str(uuid.uuid4()),
                wallet_id=wallet_db_id,
                customer_id=customer_id,
                status="success",
                transacted_at=datetime.datetime.utcnow(),
                type="deposit",
                amount=amount,
                reference_id=reference_id,
            )
            transaction.save()

            return transaction.deposit_serialized()
        except Exception as e:
            logging.exception(
                "An error occurred while depositing to wallet: %s", str(e)
            )
            return None

    def withdraw_serialized(self):
        try:
            transacted_at = convert_to_local_time(self.transacted_at)
            return {
                "id": self.public_id,
                "withdrawn_by": self.customer_id,
                "status": self.status,
                "withdrawn_at": transacted_at.isoformat()
                if self.transacted_at
                else None,
                "type": self.type,
                "amount": self.amount,
                "reference_id": self.reference_id,
            }
        except Exception as e:
            logging.exception(
                "An error occurred while serializing withdrawal: %s", str(e)
            )
            return None

    def withdraw_from_wallet(self, customer_id, wallet_id, amount, reference_id):
        try:
            ref_exist = self.check_reference(reference_id)
            if ref_exist:
                return "exists"
            
            wallet_db_id = self.update_wallet_balance(wallet_id, "withdraw", amount)
            if not wallet_db_id:
                return None
            
            transaction = Transaction(
                public_id=str(uuid.uuid4()),
                wallet_id=wallet_db_id,
                customer_id=customer_id,
                status="success",
                transacted_at=datetime.datetime.utcnow(),
                type="withdraw",
                amount=amount,
                reference_id=reference_id,
            )
            transaction.save()

            return transaction.withdraw_serialized()

        except Exception as e:
            logging.exception(
                "An error occurred while withdrawing from wallet: %s", str(e)
            )
            return None

    def check_reference(self, reference_id):
        try:
            transaction = Transaction.query.filter_by(reference_id=reference_id).first()
            if not transaction:
                return False
            return True
        except Exception as e:
            logging.exception("An error occurred while checking reference: %s", str(e))
            return None