from fastapi import HTTPException


class UndefinedException(HTTPException):
    def __init__(self):
        self.status_code = 500
        self.detail = "Server error, investigation ongoing"


class ValueErrorException(HTTPException):
    def __init__(self, detail):
        self.status_code = 422
        self.detail = detail


class ValueTooLargeException(HTTPException):
    def __init__(self):
        self.status_code = 422
        self.detail = "Request input contains an int larger than max int"
