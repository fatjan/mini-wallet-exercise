import uuid
import datetime
import logging
from .. import db
from ..util.helper import convert_to_local_time, create_token


class Wallet(db.Model):
    __tablename__ = "wallet"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    public_id = db.Column(db.String(100), nullable=False)
    owned_by = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(100), nullable=False)
    enabled_at = db.Column(db.DateTime, nullable=False)
    balance = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Wallet(owned_by={self.owned_by}, status={self.status})>"

    def serialize(self):
        enabled_at = convert_to_local_time(self.enabled_at)
        return {
            "id": self.public_id,
            "owned_by": self.owned_by,
            "status": self.status,
            "enabled_at": enabled_at.isoformat() if self.enabled_at else None,
            "balance": self.balance,
        }

    def save(self):
        db.session.add(self)
        db.session.commit()

    def init_wallet(self, customer_id):
        try:
            self.public_id = str(uuid.uuid4())
            self.owned_by = customer_id
            self.status = "disabled"
            self.balance = 0

            self.save()
            token = create_token(customer_id)
            return token

        except Exception as e:
            logging.exception("An error occurred while initiaing a wallet: %s", str(e))
            return None
        
    def enable_wallet(self, customer_id):
        try:
            wallet = self.query.filter_by(owned_by=customer_id).first()
            if not wallet:
                return None
            
            self.status = "enabled"
            self.enabled_at = datetime.datetime.utcnow()

            self.save()
            return self.serialize()
        
        except Exception as e:
            logging.exception("An error occurred while enabling a wallet: %s", str(e))
            return None
