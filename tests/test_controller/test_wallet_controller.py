import uuid
from unittest import TestCase
from unittest.mock import patch
from app import create_app
from app.main.util.helper import create_token

error_message = "Input payload validation failed"


class TestWalletEndpoints(TestCase):
    def setUp(self):
        self.app = create_app(config_object="tests.settings")
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        self.app_context.pop()

    @patch("app.main.controller.wallet_controller.init_wallet")
    def test_init_wallet_success(self, mock_init_wallet):
        # ARRANGE
        expected_response = {
            "status": "success",
            "data": {
                "token": "some_token",
            },
        }
        mock_init_wallet.return_value = expected_response

        payload = {
            "customer_xid": "ea0212d3-abd6-406f-8c67-868e814a2436",
        }

        # ACT
        with self.app.test_client() as client:
            response = client.post("/api/v1/init", json=payload)
            res = response.get_json()

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_response["status"], res.get("status"))
        self.assertEqual(expected_response["data"]["token"], res["data"]["token"])
        mock_init_wallet.assert_called_once()

    def test_init_wallet_missing_required_fields(self):
        # ACT
        with self.app.test_client() as client:
            response = client.post("/api/v1/init", json={})

        # ASSERT
        self.assertEqual(response.status_code, 400)

    @patch("app.main.controller.wallet_controller.enable_wallet")
    def test_enable_wallet_success(self, mock_enable_wallet):
        # ARRANGE
        customer_xid = "test-customer-xid"
        expected_response = {
            "status": "success",
            "data": {
                "wallet": {
                    "id": "test-wallet-id",
                    "owned_by": customer_xid,
                    "status": "enabled",
                    "balance": 0,
                }
            },
        }
        mock_enable_wallet.return_value = expected_response

        wallet_db_id = 1
        token = create_token(customer_xid, wallet_db_id)
        headers = {"Authorization": f"Token {token}"}

        # ACT
        with self.app.test_client() as client:
            response = client.post("/api/v1/wallet", headers=headers)
            res = response.get_json()

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_response["status"], res.get("status"))
        self.assertEqual(
            expected_response["data"]["wallet"]["id"], res["data"]["wallet"]["id"]
        )
        self.assertEqual(
            expected_response["data"]["wallet"]["owned_by"],
            res["data"]["wallet"]["owned_by"],
        )
        self.assertEqual(
            expected_response["data"]["wallet"]["status"],
            res["data"]["wallet"]["status"],
        )
        self.assertEqual(
            expected_response["data"]["wallet"]["balance"],
            res["data"]["wallet"]["balance"],
        )
        mock_enable_wallet.assert_called_once()

    @patch("app.main.controller.wallet_controller.enable_wallet")
    def test_enable_wallet_fail(self, mock_enable_wallet):
        # ARRANGE
        customer_xid = "test-customer-xid"
        expected_response = {"status": "fail", "data": {"error": "Already enabled"}}
        mock_enable_wallet.return_value = expected_response, 400

        wallet_db_id = 1
        token = create_token(customer_xid, wallet_db_id)
        headers = {"Authorization": f"Token {token}"}

        # ACT
        with self.app.test_client() as client:
            response = client.post("/api/v1/wallet", headers=headers)
            res = response.get_json()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(expected_response["status"], res.get("status"))
        self.assertEqual(expected_response["data"]["error"], res["data"]["error"])

    @patch("app.main.controller.wallet_controller.view_wallet_balance")
    def test_view_wallet_balance(self, mock_view_wallet_balance):
        # ARRANGE
        customer_xid = "test-customer-xid"
        expected_response = {
            "status": "success",
            "data": {
                "wallet": {
                    "id": "test-wallet-id",
                    "owned_by": customer_xid,
                    "status": "enabled",
                    "balance": 0,
                }
            },
        }
        mock_view_wallet_balance.return_value = expected_response

        wallet_db_id = 1
        token = create_token(customer_xid, wallet_db_id)
        headers = {"Authorization": f"Token {token}"}

        # ACT
        with self.app.test_client() as client:
            response = client.get("/api/v1/wallet", headers=headers)
            res = response.get_json()

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_response["status"], res.get("status"))
        self.assertEqual(
            expected_response["data"]["wallet"]["id"], res["data"]["wallet"]["id"]
        )
        self.assertEqual(
            expected_response["data"]["wallet"]["owned_by"],
            res["data"]["wallet"]["owned_by"],
        )
        self.assertEqual(
            expected_response["data"]["wallet"]["status"],
            res["data"]["wallet"]["status"],
        )
        self.assertEqual(
            expected_response["data"]["wallet"]["balance"],
            res["data"]["wallet"]["balance"],
        )
        mock_view_wallet_balance.assert_called_once()

    @patch("app.main.controller.wallet_controller.view_wallet_balance")
    def test_view_wallet_balance_fail(self, mock_view_wallet_balance):
        # ARRANGE
        customer_xid = "test-customer-xid"
        expected_response = {"status": "fail", "data": {"error": "Wallet disabled"}}
        mock_view_wallet_balance.return_value = expected_response, 404

        wallet_db_id = 1
        token = create_token(customer_xid, wallet_db_id)
        headers = {"Authorization": f"Token {token}"}

        # ACT
        with self.app.test_client() as client:
            response = client.get("/api/v1/wallet", headers=headers)
            res = response.get_json()

        # ASSERT
        self.assertEqual(response.status_code, 404)
        self.assertEqual(expected_response["status"], res.get("status"))
        self.assertEqual(expected_response["data"]["error"], res["data"]["error"])
        mock_view_wallet_balance.assert_called_once()

    @patch("app.main.controller.wallet_controller.disable_wallet")
    def test_disable_wallet_success(self, mock_disable_wallet):
        # ARRANGE
        customer_xid = "test-customer-xid"
        expected_response = {
            "status": "success",
            "data": {
                "wallet": {
                    "id": "test-wallet-id",
                    "owned_by": customer_xid,
                    "status": "disabled",
                    "balance": 0,
                }
            },
        }
        mock_disable_wallet.return_value = expected_response

        wallet_db_id = 1
        token = create_token(customer_xid, wallet_db_id)
        headers = {"Authorization": f"Token {token}"}
        payload = {"is_disabled": True}

        # ACT
        with self.app.test_client() as client:
            response = client.patch("/api/v1/wallet", headers=headers, json=payload)
            res = response.get_json()

        # ASSERT
        self.assertEqual(response.status_code, 200)
        self.assertEqual(expected_response["status"], res.get("status"))
        self.assertEqual(
            expected_response["data"]["wallet"]["id"], res["data"]["wallet"]["id"]
        )
        self.assertEqual(
            expected_response["data"]["wallet"]["owned_by"],
            res["data"]["wallet"]["owned_by"],
        )
        self.assertEqual(
            expected_response["data"]["wallet"]["status"],
            res["data"]["wallet"]["status"],
        )
        self.assertEqual(
            expected_response["data"]["wallet"]["balance"],
            res["data"]["wallet"]["balance"],
        )
        mock_disable_wallet.assert_called_once()

    @patch("app.main.controller.wallet_controller.disable_wallet")
    def test_disable_wallet_fail(self, mock_disable_wallet):
        # ARRANGE
        customer_xid = "test-customer-xid"
        expected_response = {"status": "fail", "data": {"error": "Already disabled"}}
        mock_disable_wallet.return_value = expected_response, 400

        wallet_db_id = 1
        token = create_token(customer_xid, wallet_db_id)
        headers = {"Authorization": f"Token {token}"}
        payload = {"is_disabled": True}

        # ACT
        with self.app.test_client() as client:
            response = client.patch("/api/v1/wallet", headers=headers, json=payload)
            res = response.get_json()

        # ASSERT
        self.assertEqual(response.status_code, 400)
        self.assertEqual(expected_response["status"], res.get("status"))
        self.assertEqual(expected_response["data"]["error"], res["data"]["error"])
        mock_disable_wallet.assert_called_once()
