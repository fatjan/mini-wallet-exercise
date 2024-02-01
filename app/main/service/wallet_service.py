import logging as log
from app.main.model.wallet import Wallet

wallet_model = Wallet()


def init_wallet(customer_id):
    try:
        token = wallet_model.init_wallet(customer_id)
        response_object = {"data": {"token": token}, "status": "success"}
        return response_object, 201
    except Exception as e:
        log.error(f"Error in init_report: {str(e)}")
        return {"status": "error", "message": "Internal Server Error"}, 500


def enable_wallet(customer_id):
    try:
        wallet = wallet_model.enable_wallet(customer_id)
        if not wallet:
            return {"status": "error", "message": "Wallet not found"}, 404

        response_object = {"data": {"wallet": wallet}, "status": "success"}
        return response_object, 200
    except Exception as e:
        log.error(f"Error in enable_wallet: {str(e)}")
        return {"status": "error", "message": "Internal Server Error"}, 500


def view_wallet_balance(customer_id):
    try:
        wallet = wallet_model.view_wallet_balance(customer_id)
        if not wallet:
            return {"status": "error", "message": "Wallet not found"}, 404

        response_object = {"data": {"wallet": wallet}, "status": "success"}
        return response_object, 200
    except Exception as e:
        log.error(f"Error in view_wallet_balance: {str(e)}")
        return {"status": "error", "message": "Internal Server Error"}, 500