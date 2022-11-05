from fastapi import HTTPException


class RequestException(HTTPException):
    status_code = HTTPException.status_code
    detail = HTTPException.detail


class UndefinedException(HTTPException):
    status_code = 500,
    detail = "Server error, investigation ongoing"


class NegativeIntegerException(RequestException):
    status_code = 422
    detail = "Request input is not a positive integer"


class RedundantBlacklistValueException(RequestException):
    status_code = 422

    def __init__(self, detail):
        self.detail = detail

    detail = "Request input already exist in the blacklist"


class BlacklistException(RequestException):
    status_code = 422

    def __init__(self, detail):
        self.detail = detail
