import enum


class BaseError(enum.Enum):
    def __init__(self, code: str, msg: str):
        self.code = code
        self.msg = msg


class CommonError(BaseError):
    INVALID_INPUT = ("00010001", "Invalid input for {field}")


class AuthError(BaseError):
    EXISTING_USERNAME = ("00020001", "User [{username}] already exists")
    INVALID_PASSWORD = ("00020002", "Password is incorrect")
    USERID_NOT_FOUND = ("00020003", "User ID: [{uid}] not found")
    USERNAME_NOT_FOUND = ("0002004", "Username: [{username}] not found")