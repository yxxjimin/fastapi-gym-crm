import enum


class BaseError(enum.Enum):
    def __init__(self, code: str, msg: str):
        self.code = code
        self.msg = msg


class CommonError(BaseError):
    INVALID_INPUT = ("00010001", "Invalid input for {field}")


class AuthError(BaseError):
    EXISTING_USERNAME = ("00020001", "User [{username}] already exists")
    INCORRECT_PASSWORD = ("00020002", "Password is incorrect")
