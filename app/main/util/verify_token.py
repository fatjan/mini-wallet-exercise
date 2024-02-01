import jwt
import os
from dotenv import load_dotenv
from flask import request
from functools import wraps
import logging as log

log.basicConfig(level=log.ERROR)

load_dotenv()

secret_key = "secret_key"


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        if "Authorization" in request.headers:
            token_string = request.headers.get("Authorization")
            token = token_string.split()[1]
        if not token:
            return {
                "message": "Access Denied: Unauthorized operation. Please log in to proceed."
            }, 401

        try:
            data = jwt.decode(token, secret_key, algorithms=["HS256"])
            return f(decoded_token=data, *args, **kwargs)

        except jwt.ExpiredSignatureError:
            return {
                "message": "Your current session has expired. Please log in again to continue."
            }, 401
        except Exception as e:
            log.error(f"Error: {str(e)}")
            return {"message": "Access Denied: Token is invalid"}, 401

    return decorated
