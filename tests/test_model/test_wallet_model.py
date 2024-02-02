import uuid
import unittest
from app.extensions import db
from app.main import create_app
from app.main.model.wallet import Wallet


def fake_id():
    return str(uuid.uuid4())


class TestWalletModel(unittest.TestCase):
    def setUp(self):
        self.app = create_app(config_object="tests.settings")
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_init_wallet(self):
        # Arrange
        wallet_model = Wallet()
        customer_id = fake_id()

        # Act
        result = wallet_model.init_wallet(customer_id)

        # Assert
        assert isinstance(result, str)

    def test_enable_wallet(self):
        # Arrange
        customer_id = fake_id()
        wallet_model = Wallet()
        wallet_model.init_wallet(customer_id)

        # Act
        result = wallet_model.enable_wallet(customer_id)

        # Assert
        self.assertEqual(result["owned_by"], customer_id)
        self.assertEqual(result["status"], "enabled")
        self.assertIn("enabled_at", result)
        self.assertEqual(result["balance"], 0)

    def test_view_wallet_balance(self):
        # Arrange
        customer_id = fake_id()
        wallet_model = Wallet()
        wallet_model.init_wallet(customer_id)
        wallet_model.enable_wallet(customer_id)

        # Act
        result = wallet_model.view_wallet_balance(customer_id)

        # Assert
        self.assertEqual(result["owned_by"], customer_id)
        self.assertEqual(result["status"], "enabled")
        self.assertIn("enabled_at", result)
        self.assertEqual(result["balance"], 0)

    def test_view_wallet_balance_when_wallet_disabled(self):
        # Arrange
        customer_id = fake_id()
        wallet_model = Wallet()
        wallet_model.init_wallet(customer_id)

        # Act
        result = wallet_model.view_wallet_balance(customer_id)

        # Assert
        self.assertIsNone(result)

    def test_update_balance_deposit(self):
        # Arrange
        customer_id = fake_id()
        wallet_model = Wallet()
        wallet_model.init_wallet(customer_id)
        wallet = wallet_model.enable_wallet(customer_id)

        # Act
        result = wallet_model.update_balance(wallet["id"], "deposit", 100)

        # Assert
        self.assertEqual(result.balance, 100)

    def test_update_balance_withdraw(self):
        # Arrange
        customer_id = fake_id()
        wallet_model = Wallet()
        wallet_model.init_wallet(customer_id)
        wallet = wallet_model.enable_wallet(customer_id)
        wallet_model.update_balance(wallet["id"], "deposit", 100)

        # Act
        result = wallet_model.update_balance(wallet["id"], "withdraw", 50)

        # Assert
        self.assertEqual(result.balance, 50)

    def test_update_balance_withdraw_more_than_balance(self):
        # Arrange
        customer_id = fake_id()
        wallet_model = Wallet()
        wallet_model.init_wallet(customer_id)
        wallet = wallet_model.enable_wallet(customer_id)
        wallet_model.update_balance(wallet["id"], "deposit", 100)

        # Act
        result = wallet_model.update_balance(wallet["id"], "withdraw", 150)

        # Assert
        self.assertIsNone(result)

    def test_update_balance_wallet_not_found(self):
        # Arrange
        wallet_model = Wallet()

        # Act
        result = wallet_model.update_balance(100, "deposit", 100)

        # Assert
        self.assertIsNone(result)

    def test_update_balance_wallet_disabled(self):
        # Arrange
        customer_id = fake_id()
        wallet_model = Wallet()
        wallet_model.init_wallet(customer_id)
        wallet = wallet_model.enable_wallet(customer_id)
        wallet_model.disable_wallet(wallet["id"], True)

        # Act
        result = wallet_model.update_balance(wallet["id"], "deposit", 100)

        # Assert
        self.assertIsNone(result)

    def test_disable_wallet(self):
        # Arrange
        customer_id = fake_id()
        wallet_model = Wallet()
        wallet_model.init_wallet(customer_id)
        wallet = wallet_model.enable_wallet(customer_id)

        # Act
        result = wallet_model.disable_wallet(wallet["id"], True)

        # Assert
        self.assertEqual(result["owned_by"], customer_id)
        self.assertEqual(result["status"], "disabled")
        self.assertEqual(result["balance"], 0)

    def test_disable_wallet_already_disabled(self):
        # Arrange
        customer_id = fake_id()
        wallet_model = Wallet()
        wallet_model.init_wallet(customer_id)
        wallet = wallet_model.enable_wallet(customer_id)
        wallet_model.disable_wallet(wallet["id"], True)

        # Act
        result = wallet_model.disable_wallet(wallet["id"], True)

        # Assert
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
