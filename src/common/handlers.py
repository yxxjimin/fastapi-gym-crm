from fastapi.responses import JSONResponse

from common.exceptions import ServiceException


async def service_exception_handler(_, exc: ServiceException):
    return JSONResponse(
        content={
            "error": exc.error.code,
            "msg": exc.error.msg.format(**exc.params)
        }
    )
