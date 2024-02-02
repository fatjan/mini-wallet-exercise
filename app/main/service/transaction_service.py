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


def deposit_to_wallet(customer_id, wallet_id, amount, reference_id):
    try:
        deposit = transaction_model.deposit_to_wallet(
            customer_id, wallet_id, amount, reference_id
        )
        if not deposit:
            return {"status": "fail", "data": {"error": "Reference ID already exists"}}, 404

        response_object = {"data": {"deposit": deposit}, "status": "success"}
        return response_object, 200
    except Exception as e:
        log.error(f"Error in deposit_to_wallet: {str(e)}")
        return {"status": "error", "message": "Internal Server Error"}, 500


def withdraw_from_wallet(customer_id, wallet_id, amount, reference_id):
    try:
        withdraw = transaction_model.withdraw_from_wallet(
            customer_id, wallet_id, amount, reference_id
        )
        if withdraw == "exists":
            return {"status": "fail", "data": {"error": "Reference ID already exists"}}, 404

        if not withdraw:
            return {"status": "fail", "data": {"error": "Insufficient funds"}}, 404
        
        response_object = {"data": {"withdraw": withdraw}, "status": "success"}
        return response_object, 200
    except Exception as e:
        log.error(f"Error in withdraw_from_wallet: {str(e)}")
        return {"status": "error", "message": "Internal Server Error"}, 500
