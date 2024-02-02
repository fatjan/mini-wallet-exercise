import uuid
import unittest
from unittest.mock import patch
from app.extensions import db
from app.main import create_app
from app.main.model.wallet import Wallet
from app.main.model.transaction import Transaction


def fake_id():
    return str(uuid.uuid4())


customer_id = fake_id()


def initialize_wallet():
    global wallet
    wallet_model = Wallet()
    wallet_model.init_wallet(customer_id)
    wallet = wallet_model.enable_wallet(customer_id)


class TestTransactionModel(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_object="tests.settings")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        initialize_wallet()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_view_wallet_transactions(self):
        # Arrange
        transaction_model = Transaction()

        # Act
        result = transaction_model.view_wallet_transactions(wallet["id"])

        # Assert
        assert isinstance(result, list)
        assert len(result) == 0

    def test_deposit_to_wallet_success(self):
        # Arrange
        transaction_model = Transaction()
        amount = 1000
        reference_id = fake_id()

        # Act
        result = transaction_model.deposit_to_wallet(
            customer_id, wallet["id"], amount, reference_id
        )

        # Assert
        assert isinstance(result, dict)
        assert result["deposited_by"] == customer_id
        assert result["status"] == "success"
        self.assertIn("deposited_at", result)
        assert result["type"] == "deposit"
        assert result["amount"] == amount
        assert result["reference_id"] == reference_id

    def test_withdraw_from_wallet(self):
        # Arrange
        transaction_model = Transaction()
        transaction_model.deposit_to_wallet(customer_id, wallet["id"], 2000, fake_id())
        amount = 1000
        reference_id = fake_id()

        # Act
        result = transaction_model.withdraw_from_wallet(
            customer_id, wallet["id"], amount, reference_id
        )

        # Assert
        assert isinstance(result, dict)
        assert result["withdrawn_by"] == customer_id
        assert result["status"] == "success"
        self.assertIn("withdrawn_at", result)
        assert result["type"] == "withdraw"
        assert result["amount"] == amount
        assert result["reference_id"] == reference_id

    def test_update_wallet_balance(self):
        # Arrange
        transaction_model = Transaction()
        amount = 1000

        # Act
        result = transaction_model.update_wallet_balance(
            wallet["id"], "deposit", amount
        )

        # Assert
        assert isinstance(result, int)


if __name__ == "__main__":
    unittest.main()
