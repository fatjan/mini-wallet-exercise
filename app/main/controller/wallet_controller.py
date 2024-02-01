from flask_restx import Resource
from flask import request
from ..service.wallet_service import (
    init_wallet, 
    enable_wallet, 
    view_wallet_balance,
)
from ...extensions import ns
from ..util.dto import WalletDto
from ..util.verify_token import token_required

wallet_dto = WalletDto()
_init = wallet_dto.init_form_parser
_wallet = wallet_dto.wallet_form_parser
_disable_wallet = wallet_dto.disable_wallet_form_parser


@ns.route("/init")
class InitWallet(Resource):
    @ns.expect(_init, validate=True)
    @ns.doc(responses={400: "Validation Error"})
    def post(self):
        """Initialize a wallet"""
        args = _init.parse_args(req=request)
        customer_xid = args["customer_xid"]
        return init_wallet(customer_xid)


@ns.route("/wallet")
class Wallet(Resource):
    @ns.doc(security="bearer")
    @ns.doc(responses={400: "Validation Error"})
    @token_required
    def post(self, decoded_token):
        """Enable a wallet"""
        customer_id = decoded_token["customer_id"]
        return enable_wallet(customer_id)
    
    @ns.doc(security="bearer")
    @ns.doc(responses={400: "Validation Error"})
    @token_required
    def get(self, decoded_token):
        """View wallet balance"""
        customer_id = decoded_token["customer_id"]
        return view_wallet_balance(customer_id)