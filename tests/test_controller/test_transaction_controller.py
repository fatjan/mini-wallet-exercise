import uuid
from unittest import TestCase
from unittest.mock import patch
from app import create_app
from app.main.util.helper import create_token


class TestTransactionEndpoints(TestCase):
    def setUp(self):
        self.app = create_app(config_object="tests.settings")
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch("app.main.controller.transaction_controller.view_wallet_transactions")
    def test_view_wallet_transactions_success(self, mock_view_wallet_trancations):
        # ARRANGE
        expected_response = {
            "status": "success",
            "data": {
                "transactions": [
                    {
                        "id": str(uuid.uuid4()),
                        "status": "success",
                        "transacted_at": "2024-01-24T08:15:30+07:00",
                        "type": "withdrawal",
                        "amount": 14000,
                        "reference_id": str(uuid.uuid4()),
                    },
                    {
                        "id": str(uuid.uuid4()),
                        "status": "success",
                        "transacted_at": "2024-01-15T09:15:30+07:00",
                        "type": "deposit",
                        "amount": 14000,
                        "reference_id": str(uuid.uuid4()),
                    },
                ]
            },
        }
        mock_view_wallet_trancations.return_value = expected_response

        customer_xid = "test-customer-xid"
        wallet_db_id = 1
        token = create_token(customer_xid, wallet_db_id)
        headers = {"Authorization": f"Token {token}"}

        expected_transactions = expected_response["data"]["transactions"]

        # ACT
        with self.app.test_client() as client:
            response = client.get("/api/v1/wallet/transactions", headers=headers)
            res = response.get_json()
            transactions_list = res["data"]["transactions"]

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(expected_transactions), len(transactions_list))
        self.assertEqual(expected_transactions[0]["id"], transactions_list[0]["id"])
        self.assertEqual(
            expected_transactions[0]["status"], transactions_list[0]["status"]
        )
        self.assertEqual(
            expected_transactions[0]["transacted_at"],
            transactions_list[0]["transacted_at"],
        )
        self.assertEqual(expected_transactions[0]["type"], transactions_list[0]["type"])
        self.assertEqual(
            expected_transactions[0]["amount"], transactions_list[0]["amount"]
        )
        self.assertEqual(
            expected_transactions[0]["reference_id"],
            transactions_list[0]["reference_id"],
        )
        mock_view_wallet_trancations.assert_called_once()

    @patch("app.main.controller.transaction_controller.view_wallet_transactions")
    def test_view_wallet_transactions_fail(self, mock_view_wallet_trancations):
        # ARRANGE
        excepted_response = {"status": "fail", "data": {"error": "Wallet disabled"}}
        mock_view_wallet_trancations.return_value = excepted_response, 404

        customer_xid = "test-customer-xid"
        wallet_db_id = 1
        token = create_token(customer_xid, wallet_db_id)
        headers = {"Authorization": f"Token {token}"}

        # ACT
        with self.app.test_client() as client:
            response = client.get(
                "/api/v1/wallet/transactions", json={}, headers=headers
            )
            res = response.get_json()

        # ASSERT
        self.assertEqual(response.status_code, 404)
        self.assertEqual(excepted_response["status"], res.get("status"))
        self.assertEqual(excepted_response["data"]["error"], res["data"]["error"])
        mock_view_wallet_trancations.assert_called_once()

    @patch("app.main.controller.transaction_controller.deposit_to_wallet")
    def test_deposit_to_wallet_success(self, mock_deposit_to_wallet):
        # ARRANGE
        customer_xid = str(uuid.uuid4())
        expected_response = {
            "status": "success",
            "data": {
                "deposit": {
                    "id": str(uuid.uuid4()),
                    "deposited_by": customer_xid,
                    "status": "success",
                    "deposited_at": "2024-11-05T08:15:30+07:00",
                    "amount": "150000",
                    "reference_id": str(uuid.uuid4()),
                }
            },
        }
        mock_deposit_to_wallet.return_value = expected_response

        wallet_db_id = 1
        token = create_token(customer_xid, wallet_db_id)
        headers = {"Authorization": f"Token {token}"}

        payload = {"amount": "10000", "reference_id": str(uuid.uuid4())}

        # ACT
        with self.app.test_client() as client:
            response = client.post(
                "/api/v1/wallet/deposits", json=payload, headers=headers
            )
            res = response.get_json()

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_response["status"], res.get("status"))
        self.assertEqual(
            expected_response["data"]["deposit"]["id"], res["data"]["deposit"]["id"]
        )
        self.assertEqual(
            expected_response["data"]["deposit"]["deposited_by"],
            res["data"]["deposit"]["deposited_by"],
        )
        self.assertEqual(
            expected_response["data"]["deposit"]["status"],
            res["data"]["deposit"]["status"],
        )
        self.assertEqual(
            expected_response["data"]["deposit"]["deposited_at"],
            res["data"]["deposit"]["deposited_at"],
        )
        self.assertEqual(
            expected_response["data"]["deposit"]["amount"],
            res["data"]["deposit"]["amount"],
        )
        self.assertEqual(
            expected_response["data"]["deposit"]["reference_id"],
            res["data"]["deposit"]["reference_id"],
        )
        mock_deposit_to_wallet.assert_called_once()

    @patch("app.main.controller.transaction_controller.withdraw_from_wallet")
    def test_withdraw_from_wallet(self, mock_withdraw_from_wallet):
        # ARRANGE
        customer_xid = str(uuid.uuid4())
        expected_response = {
            "status": "success",
            "data": {
                "withdrawal": {
                    "id": str(uuid.uuid4()),
                    "withdrawn_by": customer_xid,
                    "status": "success",
                    "withdrawn_at": "1994-11-05T08:15:30-05:00",
                    "amount": "60000",
                    "reference_id": "c4cee01f-2188-4a29-aa9a-cb7fb97d8e0a",
                }
            },
        }
        mock_withdraw_from_wallet.return_value = expected_response
        expected_withdrawal = expected_response["data"]["withdrawal"]

        wallet_db_id = 1
        token = create_token(customer_xid, wallet_db_id)
        headers = {"Authorization": f"Token {token}"}

        paylod = {"amount": "60000", "reference_id": str(uuid.uuid4())}

        # ACT
        with self.app.test_client() as client:
            response = client.post(
                "/api/v1/wallet/withdrawals", json=paylod, headers=headers
            )
            res = response.get_json()
            res_withdrawal = res["data"]["withdrawal"]

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_response["status"], res.get("status"))
        self.assertEqual(expected_withdrawal["id"], res_withdrawal["id"])
        self.assertEqual(
            expected_withdrawal["withdrawn_by"], res_withdrawal["withdrawn_by"]
        )
        self.assertEqual(expected_withdrawal["status"], res_withdrawal["status"])
        self.assertEqual(expected_withdrawal["amount"], res_withdrawal["amount"])
        mock_withdraw_from_wallet.assert_called_once()
