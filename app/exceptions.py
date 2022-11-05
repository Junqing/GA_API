from fastapi import HTTPException


class UndefinedException(HTTPException):
    def __init__(self):
        self.status_code = 500
        self.detail = "Server error, investigation ongoing"


class NegativeIntegerException(HTTPException):
    def __init__(self):
        self.status_code = 422
        self.detail = "Request input is not a positive integer larger than 0"


class ValueTooLargeException(HTTPException):
    def __init__(self):
        self.status_code = 422
        self.detail = "Request input contains an int larger than max int"
