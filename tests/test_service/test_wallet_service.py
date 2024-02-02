import uuid
from unittest import TestCase
from unittest.mock import patch
from app import create_app
from app.main.service.wallet_service import init_wallet, enable_wallet, view_wallet_balance, disable_wallet


def fake_id():
    return str(uuid.uuid4())


class TestReviewService(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app(config_object="tests.settings")
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()

    @patch("app.main.model.wallet.Wallet.init_wallet")
    def test_init_wallet(self, mock_init_wallet):
        # Arrange
        customer_id = fake_id()
        mock_init_wallet.return_value = "some-token"

        # Act
        response, status_code = init_wallet(customer_id)
        result = response["data"]

        # Assert
        self.assertEqual(status_code, 201)
        self.assertEqual(response["status"], "success")
        self.assertIn("token", result)
        self.assertEqual(result["token"], "some-token")
        mock_init_wallet.assert_called_once_with(customer_id)

    @patch("app.main.model.wallet.Wallet.enable_wallet")
    def test_enable_wallet_success(self, mock_enable_wallet):
        # Arrange
        customer_id = fake_id()
        expected_response = {
            "id": fake_id(),
            "owned_by": customer_id,
            "status": "enabled",
            "balance": 0
        }
        mock_enable_wallet.return_value = expected_response

        # Act
        response, status_code = enable_wallet(customer_id)
        result = response["data"]["wallet"]

        # Assert
        self.assertEqual(status_code, 200)
        self.assertEqual(response["status"], "success")
        self.assertEqual(result, expected_response)
        mock_enable_wallet.assert_called_once_with(customer_id)
    
    @patch("app.main.model.wallet.Wallet.enable_wallet")
    def test_enable_wallet_fail(self, mock_enable_wallet):
        # Arrange
        customer_id = fake_id()
        mock_enable_wallet.return_value = False

        # Act
        response, status_code = enable_wallet(customer_id)

        # Assert
        self.assertEqual(status_code, 400)
        self.assertEqual(response["status"], "fail")
        self.assertEqual(response["data"]["error"], "Already enabled")
        mock_enable_wallet.assert_called_once_with(customer_id)
    
    @patch("app.main.model.wallet.Wallet.view_wallet_balance")
    def test_view_wallet_balance_success(self, mock_view_wallet_balance):
        # Arrange
        customer_id = fake_id()
        expected_response = {
            "id": fake_id(),
            "owned_by": customer_id,
            "status": "enabled",
            "balance": 0
        }
        mock_view_wallet_balance.return_value = expected_response

        # Act
        response, status_code = view_wallet_balance(customer_id)
        result = response["data"]["wallet"]

        # Assert
        self.assertEqual(status_code, 200)
        self.assertEqual(response["status"], "success")
        self.assertEqual(result, expected_response)
        mock_view_wallet_balance.assert_called_once_with(customer_id)
    
    @patch("app.main.model.wallet.Wallet.view_wallet_balance")
    def test_view_wallet_balance_fail(self, mock_view_wallet_balance):
        # Arrange
        customer_id = fake_id()
        mock_view_wallet_balance.return_value = None

        # Act
        response, status_code = view_wallet_balance(customer_id)

        # Assert
        self.assertEqual(status_code, 404)
        self.assertEqual(response["status"], "fail")
        self.assertEqual(response["data"]["error"], "Wallet disabled")
        mock_view_wallet_balance.assert_called_once_with(customer_id)
    
    @patch("app.main.model.wallet.Wallet.disable_wallet")
    def test_disable_wallet(self, mock_disable_wallet):
        # Arrange
        wallet_id = 1
        is_disabled = True
        expected_response = {
            "id": fake_id(),
            "owned_by": fake_id(),
            "status": "disabled",
            "balance": 0
        }
        mock_disable_wallet.return_value = expected_response

        # Act
        response, status_code = disable_wallet(wallet_id, is_disabled)
        result = response["data"]["wallet"]

        # Assert
        self.assertEqual(status_code, 200)
        self.assertEqual(response["status"], "success")
        self.assertEqual(result, expected_response)
        mock_disable_wallet.assert_called_once_with(wallet_id, is_disabled)

    @patch("app.main.model.wallet.Wallet.disable_wallet")
    def test_disable_wallet_fail(self, mock_disable_wallet):
        # Arrange
        wallet_id = 1
        mock_disable_wallet.return_value = None

        # Act
        response, status_code = disable_wallet(wallet_id, True)

        # Assert
        self.assertEqual(status_code, 400)
        self.assertEqual(response["status"], "fail")
        self.assertEqual(response["data"]["error"], "Already disabled")
        mock_disable_wallet.assert_called_once_with(wallet_id, True)