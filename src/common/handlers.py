from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from common.exceptions import ServiceException


async def service_exception_handler(_, exc: ServiceException):
    return JSONResponse(
        content={
            "error": exc.error.code,
            "msg": exc.error.msg.format(**exc.params)
        }
    )

async def request_validation_handler(_, exc: RequestValidationError):
    errors = []
    for err in exc.errors():
        field = " -> ".join(str(loc) for loc in err["loc"])
        errors.append({"field": field, "msg": err["msg"]})
    return JSONResponse(
        content={
            "error": "Invalid input",
            "msg": errors
        },
        status_code=400,
    )
