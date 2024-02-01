import logging as log
from app.main.model.transaction import Transaction

transaction_model = Transaction()

def view_wallet_transactions(wallet_id):
    try:
        transactions = transaction_model.view_wallet_transactions(wallet_id)
        response_object = {"data": {"transactions": transactions}, "status": "success"}
        return response_object, 200
    except Exception as e:
        log.error(f"Error in view_wallet_transactions: {str(e)}")
        return {"status": "error", "message": "Internal Server Error"}, 500