import os
import jwt
import time
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash


def convert_to_local_time(utc_datetime):
    now_timestamp = time.time()
    offset = datetime.fromtimestamp(now_timestamp) - datetime.utcfromtimestamp(
        now_timestamp
    )
    return utc_datetime + offset


def hash_password(password):
    return generate_password_hash(password)


def error_handler(error):
    message = ""
    error_message = str(error)
    if "The email is invalid" in error_message:
        message = f"Registration failed : {error_message}"

    elif "This email has already registered" in error_message:
        message = f"Register user failed : Your email is already registered"

    elif "Duplicate entry" in error_message:
        message = f"Insert data failed : Data already exist, cannot duplicate data"

    elif "User not found" in error_message:
        message = f"Error get user : {error_message}"

    elif "Incorrect password" in error_message:
        message = f"Login Failed : {error_message}"

    elif "Access denied" in error_message:
        message = f"Access denied: You are not authorized for this operation"

    else:
        message = "Internal Server Error"

    return {"status": "error", "message": message}, 500


def create_token(customer_id, secret_key="secret_key"):
    token = jwt.encode(
        {
            "customer_id": customer_id,
            "exp": datetime.utcnow() + timedelta(days=1),
        },
        secret_key,
    )
    return token
