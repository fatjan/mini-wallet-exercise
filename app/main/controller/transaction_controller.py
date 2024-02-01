from flask_restx import Resource
from ..service.transaction_service import view_wallet_transactions
from ...extensions import ns
from ..util.verify_token import token_required


@ns.route("/wallet/transactions")
class WalletTransaction(Resource):
    @ns.doc(security="bearer")
    @ns.doc(responses={400: "Validation Error"})
    @token_required
    def get(self, decoded_token):
        """View wallet transactions"""
        customer_id = decoded_token["customer_id"]
        return view_wallet_transactions(customer_id)