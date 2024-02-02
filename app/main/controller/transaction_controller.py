from flask_restx import Resource
from flask import request
from ...extensions import ns
from ..util.dto import WalletDto
from ..util.verify_token import token_required
from ..service.transaction_service import (
    view_wallet_transactions,
    deposit_to_wallet,
    withdraw_from_wallet,
)

wallet_dto = WalletDto()
_wallet = wallet_dto.wallet_form_parser


@ns.route("/wallet/transactions")
class WalletTransaction(Resource):
    @ns.doc(security="bearer")
    @ns.doc(responses={400: "Validation Error"})
    @token_required
    def get(self, decoded_token):
        """View wallet transactions"""
        wallet_id = decoded_token["wallet_id"]
        return view_wallet_transactions(wallet_id)


@ns.route("/wallet/deposits")
class WalletDeposit(Resource):
    @ns.expect(_wallet, validate=True)
    @ns.doc(security="bearer")
    @ns.doc(responses={400: "Validation Error"})
    @token_required
    def post(self, decoded_token):
        """View wallet transactions"""
        customer_id = decoded_token["customer_id"]
        wallet_id = decoded_token["wallet_id"]
        args = _wallet.parse_args(req=request)
        amount = args["amount"]
        reference_id = args["reference_id"]
        return deposit_to_wallet(customer_id, wallet_id, amount, reference_id)


@ns.route("/wallet/withdrawals")
class WalletWithdrawal(Resource):
    @ns.expect(_wallet, validate=True)
    @ns.doc(security="bearer")
    @ns.doc(responses={400: "Validation Error"})
    @token_required
    def post(self, decoded_token):
        """View wallet transactions"""
        customer_id = decoded_token["customer_id"]
        wallet_id = decoded_token["wallet_id"]
        args = _wallet.parse_args(req=request)
        amount = args["amount"]
        reference_id = args["reference_id"]
        return withdraw_from_wallet(customer_id, wallet_id, amount, reference_id)
