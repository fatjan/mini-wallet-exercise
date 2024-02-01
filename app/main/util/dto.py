from flask_restx import fields, reqparse
from app.extensions import api

"""
DTO (Data Transfer Object) is a simple object which is used to pass data between software components.
"""


class WalletDto:
    init_form_parser = reqparse.RequestParser()
    init_form_parser.add_argument(
        "customer_xid",
        type=str,
        required=True,
        help="Customer XID is required for wallet initialization",
    )

    wallet_form_parser = reqparse.RequestParser()
    wallet_form_parser.add_argument(
        "amount",
        type=int,
        required=True,
        help="Amount is required for wallet operation",
    )
    wallet_form_parser.add_argument(
        "reference_id", type=str, required=True, help="Reference Identifier for the wallet operation"
    )

    disable_wallet_form_parser = reqparse.RequestParser()
    disable_wallet_form_parser.add_argument(
        "is_disabled",
        type=bool,
        required=True,
        help="Wallet status is required for disabling the wallet",
    )

error_model = api.model("Error", {
    "status": fields.String(default="fail"),
    "data": fields.Nested(api.model("ErrorData", {
        "error": fields.Raw()
    }))
})
