from common.errors import BaseError

class ServiceException(Exception):
    def __init__(self, error: BaseError, params: dict):
        self.error = error
        self.params = params

    def __str__(self):
        return self.error.msg.format(**self.params)
