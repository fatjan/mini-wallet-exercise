from flask_restx import fields
from app.extensions import api

"""
DTO (Data Transfer Object) is a simple object which is used to pass data between software components.
"""


class WalletDto:
    init = api.model(
        "init",
        {
            "customer_xid": fields.String(required=True, description="Customer xid of the wallet owner"),
        },
    )

    wallet = api.model(
        "wallet",
        {
            "amount": fields.Integer(required=True, description="The amount of money in the transaction/deposit/withdrawal"),
            "reference_id": fields.String(description="Reference Identifier"),
        },
    )

    disable_wallet = api.model(
        "disable_wallet",
        {
            "is_disabled": fields.Boolean(required=True, description="The status of the wallet"),
        },
    )
