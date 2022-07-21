from fastapi import status
from fastapi.responses import JSONResponse


async def timeout_exception_handler():
    message = 'Timeout occurred. Please try again.'
    return JSONResponse(
        status_code=status.HTTP_408_REQUEST_TIMEOUT,
        content=message,
    )


async def global_exception_handler():
    message = 'Something went wrong. Please try again.'
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content=message,
    )
