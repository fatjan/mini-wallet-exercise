import uuid
from unittest import TestCase
from unittest.mock import patch
from app import create_app
from app.main.service.transaction_service import (
    view_wallet_transactions,
    deposit_to_wallet,
    withdraw_from_wallet,
)


def fake_id():
    return str(uuid.uuid4())


class TestTransactionService(TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = create_app(config_object="tests.settings")
        cls.app_context = cls.app.app_context()
        cls.app_context.push()

    @classmethod
    def tearDownClass(cls):
        cls.app_context.pop()

    @patch("app.main.model.transaction.Transaction.view_wallet_transactions")
    def test_view_wallet_transactions(self, mock_view_wallet_transactions):
        # Arrange
        wallet_id = fake_id()
        expected_response = [
            {
                "id": fake_id(),
                "status": "success",
                "transacted_at": "2024-01-24T08:15:30+07:00",
                "type": "withdrawal",
                "amount": "14000",
                "reference_id": fake_id(),
            },
            {
                "id": fake_id(),
                "status": "success",
                "transacted_at": "2024-01-15T09:15:30+07:00",
                "type": "deposit",
                "amount": "14000",
                "reference_id": fake_id(),
            },
        ]
        mock_view_wallet_transactions.return_value = expected_response

        # Act
        response, status_code = view_wallet_transactions(wallet_id)
        result = response["data"]["transactions"]

        # Assert
        self.assertEqual(status_code, 200)
        self.assertEqual(response["status"], "success")
        self.assertEqual(len(result), len(expected_response))
        self.assertEqual(result, expected_response)
        mock_view_wallet_transactions.assert_called_once_with(wallet_id)

    @patch("app.main.model.transaction.Transaction.deposit_to_wallet")
    def test_deposit_to_wallet(self, mock_deposit_to_wallet):
        # Arrange
        customer_id = fake_id()
        wallet_id = fake_id()
        amount = 14000
        reference_id = fake_id()
        expected_response = {
            "id": fake_id(),
            "status": "success",
            "transacted_at": "2024-01-24T08:15:30+07:00",
            "type": "deposit",
            "amount": amount,
            "reference_id": reference_id,
        }
        mock_deposit_to_wallet.return_value = expected_response

        # Act
        response, status_code = deposit_to_wallet(
            customer_id, wallet_id, amount, reference_id
        )
        result = response["data"]["deposit"]

        # Assert
        self.assertEqual(status_code, 200)
        self.assertEqual(response["status"], "success")
        self.assertEqual(result, expected_response)
        mock_deposit_to_wallet.assert_called_once_with(
            customer_id, wallet_id, amount, reference_id
        )

    @patch("app.main.model.transaction.Transaction.withdraw_from_wallet")
    def test_withdraw_from_wallet(self, mock_withdraw_from_wallet):
        # Arrange
        customer_id = fake_id()
        wallet_id = fake_id()
        amount = 14000
        reference_id = fake_id()
        expected_response = {
            "id": fake_id(),
            "status": "success",
            "transacted_at": "2024-01-24T08:15:30+07:00",
            "type": "withdrawal",
            "amount": amount,
            "reference_id": reference_id,
        }
        mock_withdraw_from_wallet.return_value = expected_response

        # Act
        response, status_code = withdraw_from_wallet(
            customer_id, wallet_id, amount, reference_id
        )
        result = response["data"]["withdraw"]

        # Assert
        self.assertEqual(status_code, 200)
        self.assertEqual(response["status"], "success")
        self.assertEqual(result, expected_response)
        mock_withdraw_from_wallet.assert_called_once_with(
            customer_id, wallet_id, amount, reference_id
        )
